//! Direct message send / typing / stream APIs.

#[cfg(not(target_arch = "wasm32"))]
use std::pin::Pin;
#[cfg(not(target_arch = "wasm32"))]
use std::task::{Context, Poll};
#[cfg(not(target_arch = "wasm32"))]
use std::time::{Duration, Instant};

#[cfg(not(target_arch = "wasm32"))]
use futures_util::Stream;
#[cfg(not(target_arch = "wasm32"))]
use tokio::sync::mpsc;
#[cfg(not(target_arch = "wasm32"))]
use tokio::time::timeout;
#[cfg(not(target_arch = "wasm32"))]
use tracing::{debug, warn};
use uuid::Uuid;

use crate::chunking::chunk_text;
use crate::client::Client;
use crate::error::{Error, Result};
use crate::group::SendGroupMessageResult;
#[cfg(not(target_arch = "wasm32"))]
use crate::listen::map_dm_message;
#[cfg(not(target_arch = "wasm32"))]
use crate::pb::genjutsu::myconversation::v1::StreamDirectMessagesRequest;
#[cfg(not(target_arch = "wasm32"))]
use crate::pb::genjutsu::myconversation::v1::direct_message_stream_event::Item as DmStreamItem;
use crate::pb::genjutsu::myconversation::v1::{
    CreateOrGetDirectMessageRequest, SendDirectMessageRequest, SignalDirectMessageTypingRequest,
};
#[cfg(not(target_arch = "wasm32"))]
use crate::reconnect::compute_reconnect_delay;
#[cfg(not(target_arch = "wasm32"))]
use crate::types::IncomingEvent;

/// Optional fields for DM sends (reply/thread / timeline projection).
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct DmSendOptions {
    /// Quote/reply parent message id (`0` = none).
    pub reply_to_message_id: i64,
    /// Thread root id (`0` = top-level timeline).
    pub message_thread_root_id: i64,
    /// Also project a thread reply onto the main DM timeline (requires `message_thread_root_id > 0`).
    pub also_send_to_timeline: bool,
}

impl DmSendOptions {
    /// Empty options (top-level send).
    pub fn new() -> Self {
        Self::default()
    }

    pub(crate) fn validate(&self) -> Result<()> {
        if self.also_send_to_timeline && self.message_thread_root_id <= 0 {
            return Err(Error::Config(
                "also_send_to_timeline requires message_thread_root_id > 0".into(),
            ));
        }
        Ok(())
    }
}

#[cfg(not(target_arch = "wasm32"))]
const DEFAULT_IDLE: Duration = Duration::from_secs(90);
#[cfg(not(target_arch = "wasm32"))]
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(25 * 60);

/// Async stream of DM [`IncomingEvent`]s with automatic reconnect.
#[cfg(not(target_arch = "wasm32"))]
pub struct DirectEventStream {
    rx: mpsc::Receiver<Result<IncomingEvent>>,
    join: Option<tokio::task::JoinHandle<()>>,
}

#[cfg(not(target_arch = "wasm32"))]
impl Stream for DirectEventStream {
    type Item = Result<IncomingEvent>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.rx.poll_recv(cx)
    }
}

#[cfg(not(target_arch = "wasm32"))]
impl Drop for DirectEventStream {
    fn drop(&mut self) {
        if let Some(join) = self.join.take() {
            join.abort();
        }
    }
}

impl Client {
    /// Create or fetch a DM thread with `other_user_id`. Returns thread id.
    pub async fn create_or_get_dm(&self, other_user_id: i64) -> Result<i64> {
        let mut client = self.unary_rpc();
        let reply = client
            .create_or_get_direct_message(CreateOrGetDirectMessageRequest { other_user_id })
            .await?
            .into_inner();
        reply
            .thread
            .map(|t| t.id)
            .ok_or_else(|| Error::Transport("create_or_get_dm missing thread".into()))
    }

    /// Send a single DM chunk (no auto-chunking).
    pub async fn send_dm_text(
        &self,
        thread_id: i64,
        other_user_id: i64,
        text: impl Into<String>,
    ) -> Result<i64> {
        self.send_dm_text_with_options(thread_id, other_user_id, text, DmSendOptions::new())
            .await
    }

    /// Send a single DM chunk with [`DmSendOptions`].
    pub async fn send_dm_text_with_options(
        &self,
        thread_id: i64,
        other_user_id: i64,
        text: impl Into<String>,
        options: DmSendOptions,
    ) -> Result<i64> {
        options.validate()?;
        let req = SendDirectMessageRequest {
            thread_id,
            other_user_id,
            content: text.into(),
            client_message_id: Uuid::new_v4().to_string(),
            reply_to_message_id: options.reply_to_message_id,
            message_thread_root_id: options.message_thread_root_id,
            also_send_to_timeline: options.also_send_to_timeline,
            ..Default::default()
        };
        let mut client = self.unary_rpc();
        let reply = client.send_direct_message(req).await?.into_inner();
        reply
            .message
            .map(|m| m.id)
            .ok_or_else(|| Error::Transport("send_dm reply missing message".into()))
    }

    /// Reply in a DM thread with chunking.
    pub async fn reply_dm(
        &self,
        thread_id: i64,
        other_user_id: i64,
        text: impl AsRef<str>,
    ) -> Result<SendGroupMessageResult> {
        self.reply_dm_with_options(thread_id, other_user_id, text, DmSendOptions::new())
            .await
    }

    /// Reply in a DM thread with [`DmSendOptions`] (options apply to the first chunk only).
    pub async fn reply_dm_with_options(
        &self,
        thread_id: i64,
        other_user_id: i64,
        text: impl AsRef<str>,
        options: DmSendOptions,
    ) -> Result<SendGroupMessageResult> {
        options.validate()?;
        let chunks = chunk_text(text.as_ref());
        let mut message_ids = Vec::with_capacity(chunks.len());
        for (i, chunk) in chunks.into_iter().enumerate() {
            let opts = if i == 0 {
                options.clone()
            } else {
                DmSendOptions::new()
            };
            message_ids.push(
                self.send_dm_text_with_options(thread_id, other_user_id, chunk, opts)
                    .await?,
            );
        }
        Ok(SendGroupMessageResult { message_ids })
    }

    /// Signal DM typing (best-effort; UNIMPLEMENTED is ignored).
    pub async fn set_dm_typing(&self, thread_id: i64, typing: bool) -> Result<()> {
        let mut client = self.unary_rpc();
        match client
            .signal_direct_message_typing(SignalDirectMessageTypingRequest { thread_id, typing })
            .await
        {
            Ok(_) => Ok(()),
            Err(status) if status.code() == tonic::Code::Unimplemented => Ok(()),
            Err(status) => Err(status.into()),
        }
    }

    /// Subscribe to DM events with the same reconnect policy as groups.
    ///
    /// Not available on `wasm32` yet (Phase 2: in-task Durable Object sessions).
    #[cfg(not(target_arch = "wasm32"))]
    pub async fn subscribe_dms(&self) -> Result<DirectEventStream> {
        let (tx, rx) = mpsc::channel(64);
        let client = self.clone();
        let join = tokio::spawn(async move {
            run_dm_stream_loop(client, tx).await;
        });
        Ok(DirectEventStream {
            rx,
            join: Some(join),
        })
    }
}

#[cfg(not(target_arch = "wasm32"))]
async fn run_dm_stream_loop(client: Client, tx: mpsc::Sender<Result<IncomingEvent>>) {
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
            reconnect_attempt, "opening StreamDirectMessages"
        );

        let mut rpc = client.stream_rpc();
        let request = StreamDirectMessagesRequest {
            resume_after_message_id,
            resume_after_event_id: 0,
        };
        let mut stream = match rpc.stream_direct_messages(request).await {
            Ok(s) => s.into_inner(),
            Err(status) => {
                let _ = tx.send(Err(status.into())).await;
                break;
            }
        };

        'session: loop {
            if started.elapsed() >= DEFAULT_MAX_AGE {
                break 'session;
            }
            let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
            match timeout(wait, stream.message()).await {
                Err(_) | Ok(Ok(None)) | Ok(Err(_)) => break 'session,
                Ok(Ok(Some(event))) => {
                    last_event = Instant::now();
                    reconnect_attempt = 0;
                    match event.item {
                        Some(DmStreamItem::Ping(_)) => {}
                        Some(DmStreamItem::Message(msg)) => {
                            if msg.id > resume_after_message_id {
                                resume_after_message_id = msg.id;
                            }
                            let incoming = map_dm_message(msg);
                            if tx
                                .send(Ok(IncomingEvent::DirectMessage(incoming)))
                                .await
                                .is_err()
                            {
                                return;
                            }
                        }
                        Some(DmStreamItem::Typing(t)) => {
                            let typing = IncomingEvent::DirectTyping {
                                thread_id: t.thread_id,
                                user_id: t.user_id,
                                typing: t.typing,
                            };
                            if tx.send(Ok(typing)).await.is_err() {
                                return;
                            }
                        }
                        _ => {}
                    }
                }
            }
        }

        if tx.is_closed() {
            break;
        }
        let delay = compute_reconnect_delay(reconnect_attempt);
        warn!(?delay, reconnect_attempt, "dm stream reconnecting");
        reconnect_attempt = reconnect_attempt.saturating_add(1);
        tokio::time::sleep(delay).await;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn also_send_to_timeline_requires_thread_root() {
        let opts = DmSendOptions {
            also_send_to_timeline: true,
            message_thread_root_id: 0,
            ..DmSendOptions::new()
        };
        assert!(matches!(opts.validate(), Err(Error::Config(_))));
    }
}
