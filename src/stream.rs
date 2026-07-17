//! Group stream with resume + reconnect.

use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};

use futures_util::Stream;
use tokio::sync::mpsc;
use tokio::time::timeout;
use tracing::{debug, warn};

use crate::client::Client;
use crate::error::{Error, Result};
use crate::listen::map_group_message;
use crate::pb::genjutsu::myconversation::v1::StreamChatGroupsRequest;
use crate::pb::genjutsu::myconversation::v1::chat_group_stream_event::Item as StreamItem;
use crate::reconnect::compute_reconnect_delay;
use crate::types::{IncomingEvent, IncomingTyping, SubscribeOptions};

const DEFAULT_IDLE: Duration = Duration::from_secs(90);
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(25 * 60);

/// Async stream of [`IncomingEvent`] with automatic reconnect.
pub struct GroupEventStream {
    rx: mpsc::Receiver<Result<IncomingEvent>>,
    join: Option<tokio::task::JoinHandle<()>>,
}

impl Stream for GroupEventStream {
    type Item = Result<IncomingEvent>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.rx.poll_recv(cx)
    }
}

impl Drop for GroupEventStream {
    fn drop(&mut self) {
        if let Some(join) = self.join.take() {
            join.abort();
        }
    }
}

impl Client {
    /// Subscribe to chat-group events. Reconnects on disconnect / idle / max age.
    ///
    /// Pings are consumed internally (they reset the idle timer) and never yielded.
    pub async fn subscribe_groups(&self, options: SubscribeOptions) -> Result<GroupEventStream> {
        let (tx, rx) = mpsc::channel::<Result<IncomingEvent>>(64);
        let client = self.clone();
        let join = tokio::spawn(async move {
            run_group_stream_loop(client, options, tx).await;
        });
        Ok(GroupEventStream {
            rx,
            join: Some(join),
        })
    }
}

async fn run_group_stream_loop(
    client: Client,
    options: SubscribeOptions,
    tx: mpsc::Sender<Result<IncomingEvent>>,
) {
    let mut resume_after_message_id: i64 = 0;
    let mut reconnect_attempt: u32 = 0;

    loop {
        if tx.is_closed() {
            break;
        }

        let started = Instant::now();
        let mut last_event = Instant::now();
        debug!(
            resume_after_message_id,
            reconnect_attempt, "opening StreamChatGroups"
        );

        let outcome = run_one_stream_session(
            &client,
            &options,
            &tx,
            &mut resume_after_message_id,
            &mut last_event,
            started,
        )
        .await;

        if tx.is_closed() {
            break;
        }

        match outcome {
            SessionOutcome::EndedClean => {
                reconnect_attempt = 0;
            }
            SessionOutcome::Transient => {
                let delay = compute_reconnect_delay(reconnect_attempt);
                warn!(?delay, reconnect_attempt, "stream reconnecting");
                reconnect_attempt = reconnect_attempt.saturating_add(1);
                tokio::time::sleep(delay).await;
            }
            SessionOutcome::Fatal(err) => {
                let _ = tx.send(Err(err)).await;
                break;
            }
        }
    }
}

enum SessionOutcome {
    EndedClean,
    Transient,
    Fatal(Error),
}

async fn run_one_stream_session(
    client: &Client,
    options: &SubscribeOptions,
    tx: &mpsc::Sender<Result<IncomingEvent>>,
    resume_after_message_id: &mut i64,
    last_event: &mut Instant,
    started: Instant,
) -> SessionOutcome {
    let mut rpc = client.stream_rpc();
    let request = StreamChatGroupsRequest {
        resume_after_message_id: *resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = match rpc.stream_chat_groups(request).await {
        Ok(s) => s.into_inner(),
        Err(status) => {
            return SessionOutcome::Fatal(status.into());
        }
    };

    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            debug!("stream max age reached; reconnecting");
            return SessionOutcome::Transient;
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        let next = timeout(wait, stream.message()).await;
        match next {
            Err(_) => {
                debug!("stream idle timeout; reconnecting");
                return SessionOutcome::Transient;
            }
            Ok(Ok(None)) => {
                debug!("stream ended by server");
                return SessionOutcome::EndedClean;
            }
            Ok(Err(status)) => {
                warn!(%status, "stream error");
                return SessionOutcome::Transient;
            }
            Ok(Ok(Some(event))) => {
                *last_event = Instant::now();
                match event.item {
                    Some(StreamItem::Ping(_)) => {
                        // Keepalive only — do not yield.
                    }
                    Some(StreamItem::Message(msg)) => {
                        if msg.id > *resume_after_message_id {
                            *resume_after_message_id = msg.id;
                        }
                        if let Some(incoming) = map_group_message(msg, client, options) {
                            if tx
                                .send(Ok(IncomingEvent::GroupMessage(incoming)))
                                .await
                                .is_err()
                            {
                                return SessionOutcome::EndedClean;
                            }
                        }
                    }
                    Some(StreamItem::Typing(t)) => {
                        let incoming = IncomingTyping {
                            group_id: t.group_id,
                            user_id: t.user_id,
                            username: t.username,
                            typing: t.typing,
                        };
                        if tx.send(Ok(IncomingEvent::Typing(incoming))).await.is_err() {
                            return SessionOutcome::EndedClean;
                        }
                    }
                    _ => {
                        // Forward-compatible: ignore other variants.
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn backoff_grows_and_caps() {
        assert_eq!(compute_reconnect_delay(0), Duration::from_secs(2));
        assert_eq!(compute_reconnect_delay(1), Duration::from_secs(4));
        assert_eq!(compute_reconnect_delay(10), Duration::from_secs(60));
    }
}
