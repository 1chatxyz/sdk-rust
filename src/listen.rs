//! In-task group/DM listen loops (native + wasm).
//!
//! Unlike [`crate::Client::subscribe_groups`], these methods do not spawn a
//! background Tokio task — required for Cloudflare Workers / Durable Objects.
//!
//! On Workers, call [`Client::run_group_session`] / [`Client::run_dm_session`]
//! once per alarm (they return after idle / max age / stream end). Persist
//! [`ListenSessionOutcome::resume_after_message_id`] (also present on
//! [`Error::Listen`]) and schedule the next alarm.
//! Use [`Client::run_group_bot`] / [`Client::run_dm_bot`] on native for a
//! forever reconnecting loop.

use std::collections::VecDeque;
use std::future::Future;
use std::time::Duration;

use futures_util::future::{Either, select};
use tracing::{debug, warn};
use web_time::Instant;

#[cfg(not(target_arch = "wasm32"))]
use crate::async_time::sleep;
use crate::async_time::timeout;
use crate::client::Client;
use crate::error::{Error, Result};
use crate::pb::genjutsu::myconversation::v1::chat_group_stream_event::Item as StreamItem;
use crate::pb::genjutsu::myconversation::v1::direct_message_stream_event::Item as DmStreamItem;
use crate::pb::genjutsu::myconversation::v1::{
    ChatGroupStreamEvent, DirectMessageStreamEvent, StreamChatGroupsRequest,
    StreamDirectMessagesRequest,
};
#[cfg(not(target_arch = "wasm32"))]
use crate::reconnect::compute_reconnect_delay;
use crate::types::{IncomingDirectMessage, IncomingMessage, SubscribeOptions};

const DEFAULT_IDLE: Duration = Duration::from_secs(90);

#[cfg(not(target_arch = "wasm32"))]
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(25 * 60);
/// Workers DO alarm wall time is 15m; keep a margin.
#[cfg(target_arch = "wasm32")]
const DEFAULT_MAX_AGE: Duration = Duration::from_secs(14 * 60);

/// Why a listen session ended (non-fatal).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ListenEndReason {
    /// No events (including pings) within the idle window.
    IdleTimeout,
    /// Session hit the max-age budget (native ~25m, wasm ~14m).
    MaxAge,
    /// Server closed the stream cleanly.
    StreamEnded,
    /// Stream RPC failed; caller should reconnect / reschedule.
    StreamError,
}

/// Result of one bounded listen session.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ListenSessionOutcome {
    /// Last successfully handled (or intentionally skipped) message id.
    pub resume_after_message_id: i64,
    /// Non-fatal end reason.
    pub reason: ListenEndReason,
}

enum SessionControl {
    Done(ListenSessionOutcome),
    Fatal {
        resume_after_message_id: i64,
        source: Error,
    },
}

impl Client {
    /// One bounded group-stream session (idle / max age / stream end).
    ///
    /// Preferred entry point on Cloudflare Workers: await inside `alarm` /
    /// fetch, persist [`ListenSessionOutcome::resume_after_message_id`], then
    /// schedule the next alarm. On handler failure, persist the resume id from
    /// [`Error::Listen`] before retrying.
    pub async fn run_group_session<F, Fut>(
        &self,
        resume_after_message_id: i64,
        options: SubscribeOptions,
        mut handler: F,
    ) -> Result<ListenSessionOutcome>
    where
        F: FnMut(Client, IncomingMessage) -> Fut,
        Fut: Future<Output = Result<()>>,
    {
        let mut resume = resume_after_message_id;
        let started = Instant::now();
        let mut last_event = Instant::now();
        debug!(
            resume_after_message_id = resume,
            "opening StreamChatGroups (session)"
        );

        match run_one_group_session(
            self,
            &options,
            &mut resume,
            &mut last_event,
            started,
            &mut handler,
        )
        .await
        {
            SessionControl::Done(out) => Ok(out),
            SessionControl::Fatal {
                resume_after_message_id,
                source,
            } => Err(Error::Listen {
                resume_after_message_id,
                source: Box::new(source),
            }),
        }
    }

    /// One bounded DM-stream session (idle / max age / stream end).
    pub async fn run_dm_session<F, Fut>(
        &self,
        resume_after_message_id: i64,
        mut handler: F,
    ) -> Result<ListenSessionOutcome>
    where
        F: FnMut(Client, IncomingDirectMessage) -> Fut,
        Fut: Future<Output = Result<()>>,
    {
        let mut resume = resume_after_message_id;
        let started = Instant::now();
        let mut last_event = Instant::now();
        debug!(
            resume_after_message_id = resume,
            "opening StreamDirectMessages (session)"
        );

        match run_one_dm_session(self, &mut resume, &mut last_event, started, &mut handler).await {
            SessionControl::Done(out) => Ok(out),
            SessionControl::Fatal {
                resume_after_message_id,
                source,
            } => Err(Error::Listen {
                resume_after_message_id,
                source: Box::new(source),
            }),
        }
    }

    /// Forever reconnecting group listen loop (native 24/7 bots).
    ///
    /// On `wasm32`, use [`Self::run_group_session`] from a Durable Object alarm.
    #[cfg(not(target_arch = "wasm32"))]
    pub async fn run_group_bot<F, Fut>(&self, mut handler: F) -> Result<()>
    where
        F: FnMut(Client, IncomingMessage) -> Fut,
        Fut: Future<Output = Result<()>>,
    {
        let options = SubscribeOptions::new();
        let mut resume_after_message_id: i64 = 0;
        let mut reconnect_attempt: u32 = 0;

        loop {
            match self
                .run_group_session(resume_after_message_id, options.clone(), &mut handler)
                .await
            {
                Ok(out) => {
                    resume_after_message_id = out.resume_after_message_id;
                    match out.reason {
                        ListenEndReason::StreamEnded => {
                            reconnect_attempt = 0;
                        }
                        ListenEndReason::IdleTimeout
                        | ListenEndReason::MaxAge
                        | ListenEndReason::StreamError => {
                            let delay = compute_reconnect_delay(reconnect_attempt);
                            warn!(
                                ?delay,
                                reconnect_attempt,
                                ?out.reason,
                                "group stream reconnecting"
                            );
                            reconnect_attempt = reconnect_attempt.saturating_add(1);
                            sleep(delay).await;
                        }
                    }
                }
                Err(err) => return Err(err),
            }
        }
    }

    /// Forever reconnecting DM listen loop (native 24/7 bots).
    #[cfg(not(target_arch = "wasm32"))]
    pub async fn run_dm_bot<F, Fut>(&self, mut handler: F) -> Result<()>
    where
        F: FnMut(Client, IncomingDirectMessage) -> Fut,
        Fut: Future<Output = Result<()>>,
    {
        let mut resume_after_message_id: i64 = 0;
        let mut reconnect_attempt: u32 = 0;

        loop {
            match self
                .run_dm_session(resume_after_message_id, &mut handler)
                .await
            {
                Ok(out) => {
                    resume_after_message_id = out.resume_after_message_id;
                    match out.reason {
                        ListenEndReason::StreamEnded => {
                            reconnect_attempt = 0;
                        }
                        ListenEndReason::IdleTimeout
                        | ListenEndReason::MaxAge
                        | ListenEndReason::StreamError => {
                            let delay = compute_reconnect_delay(reconnect_attempt);
                            warn!(
                                ?delay,
                                reconnect_attempt,
                                ?out.reason,
                                "dm stream reconnecting"
                            );
                            reconnect_attempt = reconnect_attempt.saturating_add(1);
                            sleep(delay).await;
                        }
                    }
                }
                Err(err) => return Err(err),
            }
        }
    }
}

fn done(resume_after_message_id: i64, reason: ListenEndReason) -> SessionControl {
    SessionControl::Done(ListenSessionOutcome {
        resume_after_message_id,
        reason,
    })
}

fn fatal(resume_after_message_id: i64, source: Error) -> SessionControl {
    SessionControl::Fatal {
        resume_after_message_id,
        source,
    }
}

fn bump_resume(resume_after_message_id: &mut i64, message_id: i64) {
    if message_id > *resume_after_message_id {
        *resume_after_message_id = message_id;
    }
}

async fn run_one_group_session<F, Fut>(
    client: &Client,
    options: &SubscribeOptions,
    resume_after_message_id: &mut i64,
    last_event: &mut Instant,
    started: Instant,
    handler: &mut F,
) -> SessionControl
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    let mut rpc = client.stream_rpc();
    let request = StreamChatGroupsRequest {
        resume_after_message_id: *resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = match rpc.stream_chat_groups(request).await {
        Ok(s) => s.into_inner(),
        Err(status) => return fatal(*resume_after_message_id, status.into()),
    };

    let mut pending: VecDeque<IncomingMessage> = VecDeque::new();

    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            debug!("stream max age reached; ending session");
            return finish_group_pending(
                client,
                handler,
                &mut pending,
                resume_after_message_id,
                started,
                ListenEndReason::MaxAge,
            )
            .await;
        }

        while let Some(incoming) = pending.pop_front() {
            if let Err(control) = await_group_handler(
                client,
                handler,
                incoming,
                &mut stream,
                last_event,
                &mut pending,
                options,
                resume_after_message_id,
                started,
            )
            .await
            {
                return settle_group_control(
                    control,
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                )
                .await;
            }
            if started.elapsed() >= DEFAULT_MAX_AGE {
                return finish_group_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::MaxAge,
                )
                .await;
            }
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        match timeout(wait, stream.message()).await {
            Err(()) => {
                debug!("stream idle timeout; ending session");
                return finish_group_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::IdleTimeout,
                )
                .await;
            }
            Ok(Ok(None)) => {
                debug!("stream ended by server");
                return finish_group_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::StreamEnded,
                )
                .await;
            }
            Ok(Err(status)) => {
                warn!(%status, "stream error");
                return finish_group_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::StreamError,
                )
                .await;
            }
            Ok(Ok(Some(event))) => {
                *last_event = Instant::now();
                if let Err(control) = apply_group_event(
                    event,
                    client,
                    options,
                    resume_after_message_id,
                    handler,
                    &mut stream,
                    last_event,
                    &mut pending,
                    started,
                )
                .await
                {
                    return settle_group_control(
                        control,
                        client,
                        handler,
                        &mut pending,
                        resume_after_message_id,
                        started,
                    )
                    .await;
                }
            }
        }
    }
}

async fn settle_group_control<F, Fut>(
    control: SessionControl,
    client: &Client,
    handler: &mut F,
    pending: &mut VecDeque<IncomingMessage>,
    resume_after_message_id: &mut i64,
    started: Instant,
) -> SessionControl
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    match control {
        SessionControl::Fatal { .. } => control,
        SessionControl::Done(out) => {
            *resume_after_message_id = out.resume_after_message_id;
            finish_group_pending(
                client,
                handler,
                pending,
                resume_after_message_id,
                started,
                out.reason,
            )
            .await
        }
    }
}

async fn settle_dm_control<F, Fut>(
    control: SessionControl,
    client: &Client,
    handler: &mut F,
    pending: &mut VecDeque<IncomingDirectMessage>,
    resume_after_message_id: &mut i64,
    started: Instant,
) -> SessionControl
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    match control {
        SessionControl::Fatal { .. } => control,
        SessionControl::Done(out) => {
            *resume_after_message_id = out.resume_after_message_id;
            finish_dm_pending(
                client,
                handler,
                pending,
                resume_after_message_id,
                started,
                out.reason,
            )
            .await
        }
    }
}

async fn run_one_dm_session<F, Fut>(
    client: &Client,
    resume_after_message_id: &mut i64,
    last_event: &mut Instant,
    started: Instant,
    handler: &mut F,
) -> SessionControl
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    let mut rpc = client.stream_rpc();
    let request = StreamDirectMessagesRequest {
        resume_after_message_id: *resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = match rpc.stream_direct_messages(request).await {
        Ok(s) => s.into_inner(),
        Err(status) => return fatal(*resume_after_message_id, status.into()),
    };

    let mut pending: VecDeque<IncomingDirectMessage> = VecDeque::new();

    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            return finish_dm_pending(
                client,
                handler,
                &mut pending,
                resume_after_message_id,
                started,
                ListenEndReason::MaxAge,
            )
            .await;
        }

        while let Some(incoming) = pending.pop_front() {
            if let Err(control) = await_dm_handler(
                client,
                handler,
                incoming,
                &mut stream,
                last_event,
                &mut pending,
                resume_after_message_id,
                started,
            )
            .await
            {
                return settle_dm_control(
                    control,
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                )
                .await;
            }
            if started.elapsed() >= DEFAULT_MAX_AGE {
                return finish_dm_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::MaxAge,
                )
                .await;
            }
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        match timeout(wait, stream.message()).await {
            Err(()) => {
                return finish_dm_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::IdleTimeout,
                )
                .await;
            }
            Ok(Ok(None)) => {
                return finish_dm_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::StreamEnded,
                )
                .await;
            }
            Ok(Err(_)) => {
                return finish_dm_pending(
                    client,
                    handler,
                    &mut pending,
                    resume_after_message_id,
                    started,
                    ListenEndReason::StreamError,
                )
                .await;
            }
            Ok(Ok(Some(event))) => {
                *last_event = Instant::now();
                if let Err(control) = apply_dm_event(
                    event,
                    client,
                    resume_after_message_id,
                    handler,
                    &mut stream,
                    last_event,
                    &mut pending,
                    started,
                )
                .await
                {
                    return settle_dm_control(
                        control,
                        client,
                        handler,
                        &mut pending,
                        resume_after_message_id,
                        started,
                    )
                    .await;
                }
            }
        }
    }
}

/// Drain queued messages without the stream (session is ending).
async fn finish_group_pending<F, Fut>(
    client: &Client,
    handler: &mut F,
    pending: &mut VecDeque<IncomingMessage>,
    resume_after_message_id: &mut i64,
    started: Instant,
    reason: ListenEndReason,
) -> SessionControl
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    while let Some(incoming) = pending.pop_front() {
        if started.elapsed() >= DEFAULT_MAX_AGE && reason != ListenEndReason::MaxAge {
            return done(*resume_after_message_id, ListenEndReason::MaxAge);
        }
        let id = incoming.id;
        match handler(client.clone(), incoming).await {
            Ok(()) => bump_resume(resume_after_message_id, id),
            Err(err) => return fatal(*resume_after_message_id, err),
        }
        if started.elapsed() >= DEFAULT_MAX_AGE {
            // Leave remaining pending unhandled so the next session redelivers.
            return done(*resume_after_message_id, ListenEndReason::MaxAge);
        }
    }
    done(*resume_after_message_id, reason)
}

async fn finish_dm_pending<F, Fut>(
    client: &Client,
    handler: &mut F,
    pending: &mut VecDeque<IncomingDirectMessage>,
    resume_after_message_id: &mut i64,
    started: Instant,
    reason: ListenEndReason,
) -> SessionControl
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    while let Some(incoming) = pending.pop_front() {
        if started.elapsed() >= DEFAULT_MAX_AGE && reason != ListenEndReason::MaxAge {
            return done(*resume_after_message_id, ListenEndReason::MaxAge);
        }
        let id = incoming.id;
        match handler(client.clone(), incoming).await {
            Ok(()) => bump_resume(resume_after_message_id, id),
            Err(err) => return fatal(*resume_after_message_id, err),
        }
        if started.elapsed() >= DEFAULT_MAX_AGE {
            return done(*resume_after_message_id, ListenEndReason::MaxAge);
        }
    }
    done(*resume_after_message_id, reason)
}

#[allow(clippy::too_many_arguments)]
async fn apply_group_event<F, Fut>(
    event: ChatGroupStreamEvent,
    client: &Client,
    options: &SubscribeOptions,
    resume_after_message_id: &mut i64,
    handler: &mut F,
    stream: &mut tonic::Streaming<ChatGroupStreamEvent>,
    last_event: &mut Instant,
    pending: &mut VecDeque<IncomingMessage>,
    started: Instant,
) -> std::result::Result<(), SessionControl>
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    match event.item {
        Some(StreamItem::Ping(_)) => Ok(()),
        Some(StreamItem::Message(msg)) => {
            if let Some(incoming) = map_group_message(msg.clone(), client, options) {
                await_group_handler(
                    client,
                    handler,
                    incoming,
                    stream,
                    last_event,
                    pending,
                    options,
                    resume_after_message_id,
                    started,
                )
                .await
            } else {
                bump_resume(resume_after_message_id, msg.id);
                Ok(())
            }
        }
        _ => Ok(()),
    }
}

#[allow(clippy::too_many_arguments)]
async fn apply_dm_event<F, Fut>(
    event: DirectMessageStreamEvent,
    client: &Client,
    resume_after_message_id: &mut i64,
    handler: &mut F,
    stream: &mut tonic::Streaming<DirectMessageStreamEvent>,
    last_event: &mut Instant,
    pending: &mut VecDeque<IncomingDirectMessage>,
    started: Instant,
) -> std::result::Result<(), SessionControl>
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    match event.item {
        Some(DmStreamItem::Ping(_)) => Ok(()),
        Some(DmStreamItem::Message(msg)) => {
            let incoming = IncomingDirectMessage {
                id: msg.id,
                thread_id: msg.thread_id,
                sender_user_id: msg.sender_user_id,
                sender_username: msg.sender_username,
                text: msg.content,
                images: msg.images,
                files: msg.files,
            };
            await_dm_handler(
                client,
                handler,
                incoming,
                stream,
                last_event,
                pending,
                resume_after_message_id,
                started,
            )
            .await
        }
        _ => Ok(()),
    }
}

/// Run the handler while still reading the stream so pings reset idle and
/// additional messages are queued (FIFO) for the session loop.
#[allow(clippy::too_many_arguments)]
async fn await_group_handler<F, Fut>(
    client: &Client,
    handler: &mut F,
    incoming: IncomingMessage,
    stream: &mut tonic::Streaming<ChatGroupStreamEvent>,
    last_event: &mut Instant,
    pending: &mut VecDeque<IncomingMessage>,
    options: &SubscribeOptions,
    resume_after_message_id: &mut i64,
    started: Instant,
) -> std::result::Result<(), SessionControl>
where
    F: FnMut(Client, IncomingMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    let message_id = incoming.id;
    let mut work = Box::pin(handler(client.clone(), incoming));
    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            return match work.await {
                Ok(()) => {
                    bump_resume(resume_after_message_id, message_id);
                    Err(done(*resume_after_message_id, ListenEndReason::MaxAge))
                }
                Err(err) => Err(fatal(*resume_after_message_id, err)),
            };
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        let next = stream.message();
        futures_util::pin_mut!(next);
        match timeout(wait, select(&mut work, next)).await {
            Err(()) => {
                return Err(done(*resume_after_message_id, ListenEndReason::IdleTimeout));
            }
            Ok(Either::Left((result, _))) => {
                return match result {
                    Ok(()) => {
                        bump_resume(resume_after_message_id, message_id);
                        Ok(())
                    }
                    Err(err) => Err(fatal(*resume_after_message_id, err)),
                };
            }
            Ok(Either::Right((msg_res, _))) => match msg_res {
                Ok(None) => {
                    return match work.await {
                        Ok(()) => {
                            bump_resume(resume_after_message_id, message_id);
                            Err(done(*resume_after_message_id, ListenEndReason::StreamEnded))
                        }
                        Err(err) => Err(fatal(*resume_after_message_id, err)),
                    };
                }
                Err(status) => {
                    warn!(%status, "stream error during handler");
                    return match work.await {
                        Ok(()) => {
                            bump_resume(resume_after_message_id, message_id);
                            Err(done(*resume_after_message_id, ListenEndReason::StreamError))
                        }
                        Err(err) => Err(fatal(*resume_after_message_id, err)),
                    };
                }
                Ok(Some(event)) => {
                    *last_event = Instant::now();
                    match event.item {
                        Some(StreamItem::Ping(_)) => {}
                        Some(StreamItem::Message(msg)) => {
                            if let Some(incoming) = map_group_message(msg.clone(), client, options)
                            {
                                pending.push_back(incoming);
                            } else {
                                bump_resume(resume_after_message_id, msg.id);
                            }
                        }
                        _ => {}
                    }
                }
            },
        }
    }
}

#[allow(clippy::too_many_arguments)]
async fn await_dm_handler<F, Fut>(
    client: &Client,
    handler: &mut F,
    incoming: IncomingDirectMessage,
    stream: &mut tonic::Streaming<DirectMessageStreamEvent>,
    last_event: &mut Instant,
    pending: &mut VecDeque<IncomingDirectMessage>,
    resume_after_message_id: &mut i64,
    started: Instant,
) -> std::result::Result<(), SessionControl>
where
    F: FnMut(Client, IncomingDirectMessage) -> Fut,
    Fut: Future<Output = Result<()>>,
{
    let message_id = incoming.id;
    let mut work = Box::pin(handler(client.clone(), incoming));
    loop {
        if started.elapsed() >= DEFAULT_MAX_AGE {
            return match work.await {
                Ok(()) => {
                    bump_resume(resume_after_message_id, message_id);
                    Err(done(*resume_after_message_id, ListenEndReason::MaxAge))
                }
                Err(err) => Err(fatal(*resume_after_message_id, err)),
            };
        }

        let wait = DEFAULT_IDLE.saturating_sub(last_event.elapsed());
        let next = stream.message();
        futures_util::pin_mut!(next);
        match timeout(wait, select(&mut work, next)).await {
            Err(()) => {
                return Err(done(*resume_after_message_id, ListenEndReason::IdleTimeout));
            }
            Ok(Either::Left((result, _))) => {
                return match result {
                    Ok(()) => {
                        bump_resume(resume_after_message_id, message_id);
                        Ok(())
                    }
                    Err(err) => Err(fatal(*resume_after_message_id, err)),
                };
            }
            Ok(Either::Right((msg_res, _))) => match msg_res {
                Ok(None) => {
                    return match work.await {
                        Ok(()) => {
                            bump_resume(resume_after_message_id, message_id);
                            Err(done(*resume_after_message_id, ListenEndReason::StreamEnded))
                        }
                        Err(err) => Err(fatal(*resume_after_message_id, err)),
                    };
                }
                Err(_) => {
                    return match work.await {
                        Ok(()) => {
                            bump_resume(resume_after_message_id, message_id);
                            Err(done(*resume_after_message_id, ListenEndReason::StreamError))
                        }
                        Err(err) => Err(fatal(*resume_after_message_id, err)),
                    };
                }
                Ok(Some(event)) => {
                    *last_event = Instant::now();
                    match event.item {
                        Some(DmStreamItem::Ping(_)) => {}
                        Some(DmStreamItem::Message(msg)) => {
                            pending.push_back(IncomingDirectMessage {
                                id: msg.id,
                                thread_id: msg.thread_id,
                                sender_user_id: msg.sender_user_id,
                                sender_username: msg.sender_username,
                                text: msg.content,
                                images: msg.images,
                                files: msg.files,
                            });
                        }
                        _ => {}
                    }
                }
            },
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
