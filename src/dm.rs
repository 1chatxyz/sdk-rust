//! Direct message send / typing / stream APIs.

use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::{Duration, Instant};

use futures_util::Stream;
use tokio::sync::mpsc;
use tokio::time::timeout;
use tracing::{debug, warn};
use uuid::Uuid;

use crate::chunking::chunk_text;
use crate::client::Client;
use crate::error::{Error, Result};
use crate::group::SendGroupMessageResult;
use crate::pb::genjutsu::myconversation::v1::direct_message_stream_event::Item as DmStreamItem;
use crate::pb::genjutsu::myconversation::v1::{
    CreateOrGetDirectMessageRequest, SendDirectMessageRequest, SignalDirectMessageTypingRequest,
    StreamDirectMessagesRequest,
};
use crate::stream::compute_reconnect_delay;
use crate::types::{IncomingDirectMessage, IncomingEvent};

const DEFAULT_IDLE: Duration = Duration::from_secs(90);
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(25 * 60);

/// Async stream of DM [`IncomingEvent`]s with automatic reconnect.
pub struct DirectEventStream {
    rx: mpsc::Receiver<Result<IncomingEvent>>,
    join: Option<tokio::task::JoinHandle<()>>,
}

impl Stream for DirectEventStream {
    type Item = Result<IncomingEvent>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.rx.poll_recv(cx)
    }
}

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
        let req = SendDirectMessageRequest {
            thread_id,
            other_user_id,
            content: text.into(),
            images: Vec::new(),
            videos: Vec::new(),
            files: Vec::new(),
            client_message_id: Uuid::new_v4().to_string(),
            reply_to_message_id: 0,
            reply_quote_text: String::new(),
            reply_quote_position: 0,
            message_thread_root_id: 0,
            sticker_id: 0,
            link_previews: Vec::new(),
            shared_message_hash: String::new(),
            file_metas: Vec::new(),
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
        let chunks = chunk_text(text.as_ref());
        let mut message_ids = Vec::with_capacity(chunks.len());
        for chunk in chunks {
            message_ids.push(self.send_dm_text(thread_id, other_user_id, chunk).await?);
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
                            let incoming = IncomingDirectMessage {
                                id: msg.id,
                                thread_id: msg.thread_id,
                                sender_user_id: msg.sender_user_id,
                                sender_username: msg.sender_username,
                                text: msg.content,
                                images: msg.images,
                                files: msg.files,
                            };
                            if tx
                                .send(Ok(IncomingEvent::DirectMessage(incoming)))
                                .await
                                .is_err()
                            {
                                return;
                            }
                        }
                        Some(DmStreamItem::Typing(t)) => {
                            if tx
                                .send(Ok(IncomingEvent::DirectTyping {
                                    thread_id: t.thread_id,
                                    user_id: t.user_id,
                                    typing: t.typing,
                                }))
                                .await
                                .is_err()
                            {
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
