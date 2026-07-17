//! In-task group/DM listen loops (native + wasm).
//!
//! Unlike [`crate::Client::subscribe_groups`], these methods do not spawn a
//! background Tokio task — required for Cloudflare Workers / Durable Objects.

use std::time::Duration;

use tracing::{debug, warn};
use web_time::Instant;

use crate::async_time::{sleep, timeout};
use crate::client::Client;
use crate::error::{Error, Result};
use crate::pb::genjutsu::myconversation::v1::chat_group_stream_event::Item as StreamItem;
use crate::pb::genjutsu::myconversation::v1::direct_message_stream_event::Item as DmStreamItem;
use crate::pb::genjutsu::myconversation::v1::{
    StreamChatGroupsRequest, StreamDirectMessagesRequest,
};
use crate::reconnect::compute_reconnect_delay;
use crate::types::{IncomingDirectMessage, IncomingMessage, SubscribeOptions};

const DEFAULT_IDLE: Duration = Duration::from_secs(90);

#[cfg(not(target_arch = "wasm32"))]
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(25 * 60);
/// Workers DO alarm wall time is 15m; keep a margin.
#[cfg(target_arch = "wasm32")]
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(14 * 60);

enum SessionOutcome {
    EndedClean,
    Transient,
    Fatal(Error),
}

impl Client {
    /// Convenience loop: invoke `handler` for each group message until fatal error.
    ///
    /// Reconnects on idle / max age / transient errors (same policy as
    /// [`Self::subscribe_groups`] on native). Safe to `await` inside a Workers
    /// Durable Object alarm/fetch handler.
    pub async fn run_group_bot<F, Fut>(&self, mut handler: F) -> Result<()>
    where
        F: FnMut(Client, IncomingMessage) -> Fut,
        Fut: std::future::Future<Output = Result<()>>,
    {
        let options = SubscribeOptions::new();
        let mut resume_after_message_id: i64 = 0;
        let mut reconnect_attempt: u32 = 0;

        loop {
            let started = Instant::now();
            let mut last_event = Instant::now();
            debug!(
                resume_after_message_id,
                reconnect_attempt, "opening StreamChatGroups (in-task)"
            );

            let outcome = run_one_group_session(
                self,
                &options,
                &mut resume_after_message_id,
                &mut last_event,
                started,
                &mut handler,
            )
            .await;

            match outcome {
                SessionOutcome::EndedClean => {
                    reconnect_attempt = 0;
                }
                SessionOutcome::Transient => {
                    let delay = compute_reconnect_delay(reconnect_attempt);
                    warn!(?delay, reconnect_attempt, "group stream reconnecting");
                    reconnect_attempt = reconnect_attempt.saturating_add(1);
                    sleep(delay).await;
                }
                SessionOutcome::Fatal(err) => return Err(err),
            }
        }
    }

    /// Convenience loop for direct messages (in-task reconnect).
    pub async fn run_dm_bot<F, Fut>(&self, mut handler: F) -> Result<()>
    where
        F: FnMut(Client, IncomingDirectMessage) -> Fut,
        Fut: std::future::Future<Output = Result<()>>,
    {
        let mut resume_after_message_id: i64 = 0;
        let mut reconnect_attempt: u32 = 0;

        loop {
            let started = Instant::now();
            let mut last_event = Instant::now();
            debug!(
                resume_after_message_id,
                reconnect_attempt, "opening StreamDirectMessages (in-task)"
            );

            let outcome = run_one_dm_session(
                self,
                &mut resume_after_message_id,
                &mut last_event,
                started,
                &mut handler,
            )
            .await;

            match outcome {
                SessionOutcome::EndedClean => {
                    reconnect_attempt = 0;
                }
                SessionOutcome::Transient => {
                    let delay = compute_reconnect_delay(reconnect_attempt);
                    warn!(?delay, reconnect_attempt, "dm stream reconnecting");
                    reconnect_attempt = reconnect_attempt.saturating_add(1);
                    sleep(delay).await;
                }
                SessionOutcome::Fatal(err) => return Err(err),
            }
        }
    }
}

async fn run_one_group_session<F, Fut>(
    client: &Client,
    options: &SubscribeOptions,
    resume_after_message_id: &mut i64,
    last_event: &mut Instant,
    started: Instant,
    handler: &mut F,
) -> SessionOutcome
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: std::future::Future<Output = Result<()>>,
{
    let mut rpc = client.stream_rpc();
    let request = StreamChatGroupsRequest {
        resume_after_message_id: *resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = match rpc.stream_chat_groups(request).await {
        Ok(s) => s.into_inner(),
        Err(status) => return SessionOutcome::Fatal(status.into()),
    };

    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            debug!("stream max age reached; reconnecting");
            return SessionOutcome::Transient;
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        match timeout(wait, stream.message()).await {
            Err(()) => {
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
                    Some(StreamItem::Ping(_)) => {}
                    Some(StreamItem::Message(msg)) => {
                        if msg.id > *resume_after_message_id {
                            *resume_after_message_id = msg.id;
                        }
                        if let Some(incoming) = map_group_message(msg, client, options) {
                            if let Err(err) = handler(client.clone(), incoming).await {
                                return SessionOutcome::Fatal(err);
                            }
                        }
                    }
                    Some(StreamItem::Typing(_)) => {}
                    _ => {}
                }
            }
        }
    }
}

async fn run_one_dm_session<F, Fut>(
    client: &Client,
    resume_after_message_id: &mut i64,
    last_event: &mut Instant,
    started: Instant,
    handler: &mut F,
) -> SessionOutcome
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: std::future::Future<Output = Result<()>>,
{
    let mut rpc = client.stream_rpc();
    let request = StreamDirectMessagesRequest {
        resume_after_message_id: *resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = match rpc.stream_direct_messages(request).await {
        Ok(s) => s.into_inner(),
        Err(status) => return SessionOutcome::Fatal(status.into()),
    };

    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            return SessionOutcome::Transient;
        }
        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        match timeout(wait, stream.message()).await {
            Err(()) => return SessionOutcome::Transient,
            Ok(Ok(None)) => return SessionOutcome::EndedClean,
            Ok(Err(_)) => return SessionOutcome::Transient,
            Ok(Ok(Some(event))) => {
                *last_event = Instant::now();
                match event.item {
                    Some(DmStreamItem::Ping(_)) => {}
                    Some(DmStreamItem::Message(msg)) => {
                        if msg.id > *resume_after_message_id {
                            *resume_after_message_id = msg.id;
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
                        if let Err(err) = handler(client.clone(), incoming).await {
                            return SessionOutcome::Fatal(err);
                        }
                    }
                    Some(DmStreamItem::Typing(_)) => {}
                    _ => {}
                }
            }
        }
    }
}

pub(crate) fn map_group_message(
    msg: crate::pb::genjutsu::myconversation::v1::ChatGroupMessageInfo,
    client: &Client,
    options: &SubscribeOptions,
) -> Option<IncomingMessage> {
    if let Some(allow) = &options.allowlist {
        if !allow.contains(&msg.group_id) {
            return None;
        }
    }

    if options.ignore_self {
        if let Some(self_id) = client.config().user_id.as_deref() {
            if let Ok(self_id) = self_id.parse::<i64>() {
                if self_id == msg.sender_user_id {
                    return None;
                }
            }
        }
    }

    if options.require_mention {
        let cfg = client.config();
        let by_id = cfg
            .user_id
            .as_deref()
            .and_then(|s| s.parse::<i64>().ok())
            .is_some_and(|id| msg.mentioned_user_ids.contains(&id));
        let by_name = cfg
            .username
            .as_deref()
            .is_some_and(|u| !u.is_empty() && msg.content.contains(u));
        if !by_id && !by_name {
            return None;
        }
    }

    Some(IncomingMessage {
        id: msg.id,
        group_id: msg.group_id,
        sender_user_id: msg.sender_user_id,
        sender_username: msg.sender_username,
        text: msg.content,
        mentioned_user_ids: msg.mentioned_user_ids,
        images: msg.images,
        files: msg.files,
    })
}
