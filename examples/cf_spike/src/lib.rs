//! Phase 0 spike: gRPC-Web over Fetch on Cloudflare Workers.
//!
//! Proves unary send + `StreamChatGroups` + alarm-driven resume. Not the SDK.

mod pb {
    pub mod genjutsu {
        pub mod myconversation {
            pub mod model {
                pub mod v1 {
                    include!(concat!(
                        env!("OUT_DIR"),
                        "/genjutsu.myconversation.model.v1.rs"
                    ));
                }
            }

            pub mod v1 {
                include!(concat!(env!("OUT_DIR"), "/genjutsu.myconversation.v1.rs"));
            }
        }
    }
}

use std::time::Duration;

use futures_util::future::{Either, select};
use gloo_timers::future::TimeoutFuture;
use pb::genjutsu::myconversation::v1::chat_group_stream_event::Item as StreamItem;
use pb::genjutsu::myconversation::v1::my_conversation_client::MyConversationClient;
use pb::genjutsu::myconversation::v1::{SendChatGroupMessageRequest, StreamChatGroupsRequest};
use serde::Serialize;
use tonic::Status;
use tonic::metadata::{Ascii, MetadataValue};
use tonic::service::Interceptor;
use tonic_web_wasm_client::Client as WasmGrpcClient;
use tonic_web_wasm_client::options::{Credentials, FetchOptions};
use uuid::Uuid;
use worker::{
    Context, DurableObject, Env, Error, Method, Request, Response, Result, State, Storage,
    console_error, console_log, durable_object, event,
};

const STORAGE_RESUME: &str = "resume_after_message_id";
const STORAGE_LAST_STATUS: &str = "last_status";
const STORAGE_RUNNING: &str = "session_running";
const STORAGE_RUNNING_SINCE_MS: &str = "session_running_since_ms";
const DEFAULT_SESSION_SECS: u64 = 120;
const IDLE_SECS: u64 = 90;

#[derive(Clone)]
struct AuthInterceptor {
    authorization: MetadataValue<Ascii>,
    tenant_id: MetadataValue<Ascii>,
}

impl Interceptor for AuthInterceptor {
    fn call(
        &mut self,
        mut request: tonic::Request<()>,
    ) -> std::result::Result<tonic::Request<()>, Status> {
        request
            .metadata_mut()
            .insert("authorization", self.authorization.clone());
        request
            .metadata_mut()
            .insert("x-tenant-id", self.tenant_id.clone());
        Ok(request)
    }
}

fn env_string(env: &Env, name: &str) -> Result<String> {
    if let Ok(secret) = env.secret(name) {
        return Ok(secret.to_string());
    }
    if let Ok(var) = env.var(name) {
        return Ok(var.to_string());
    }
    Err(Error::RustError(format!("missing env/secret: {name}")))
}

fn parse_u64_env(env: &Env, name: &str, default: u64) -> u64 {
    env_string(env, name)
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(default)
}

/// Returns true when the request presents a valid control bearer token.
/// Missing/misconfigured secrets intentionally look the same as a bad token
/// so unauthenticated callers cannot probe config.
fn control_authorized(req: &Request, env: &Env) -> bool {
    let Ok(expected) = env_string(env, "CONTROL_TOKEN") else {
        return false;
    };
    if expected.is_empty() {
        return false;
    }
    let Ok(Some(header)) = req.headers().get("Authorization") else {
        return false;
    };
    let token = header
        .strip_prefix("Bearer ")
        .or_else(|| header.strip_prefix("bearer "))
        .unwrap_or(header.as_str());
    token == expected
}

fn unauthorized() -> Result<Response> {
    Response::error("unauthorized", 401)
}

fn grpc_client(
    env: &Env,
) -> Result<
    MyConversationClient<
        tonic::service::interceptor::InterceptedService<WasmGrpcClient, AuthInterceptor>,
    >,
> {
    let base_url = env_string(env, "API_1CHAT_URL")?;
    let tenant_id = env_string(env, "TENANT_ID")?;
    let bot_token = env_string(env, "BOT_TOKEN")?;
    let authorization = MetadataValue::try_from(format!("Bearer {bot_token}"))
        .map_err(|e| Error::RustError(format!("authorization metadata: {e}")))?;
    let tenant_meta = MetadataValue::try_from(tenant_id)
        .map_err(|e| Error::RustError(format!("tenant metadata: {e}")))?;
    let options = FetchOptions::default().credentials(Credentials::Omit);
    let transport = WasmGrpcClient::new_with_options(base_url, options);
    let auth = AuthInterceptor {
        authorization,
        tenant_id: tenant_meta,
    };
    Ok(MyConversationClient::with_interceptor(transport, auth))
}

async fn send_unary(env: &Env, group_id: i64, text: &str) -> Result<i64> {
    let mut client = grpc_client(env)?;
    let req = SendChatGroupMessageRequest {
        group_id,
        content: text.to_string(),
        mentioned_user_ids: Vec::new(),
        client_message_id: Uuid::new_v4().to_string(),
        images: Vec::new(),
        videos: Vec::new(),
        files: Vec::new(),
        topic_id: 0,
        reply_to_message_id: 0,
        reply_quote_text: String::new(),
        reply_quote_position: 0,
        message_thread_root_id: 0,
        sticker_id: 0,
        link_previews: Vec::new(),
        shared_message_hash: String::new(),
        file_metas: Vec::new(),
        mention_all: false,
    };
    let reply = client
        .send_chat_group_message(req)
        .await
        .map_err(|e| Error::RustError(format!("unary send: {e}")))?
        .into_inner();
    reply
        .message
        .map(|m| m.id)
        .ok_or_else(|| Error::RustError("send reply missing message".into()))
}

#[derive(Debug, Serialize)]
struct SessionReport {
    resume_after_message_id: i64,
    messages_seen: u32,
    pings_seen: u32,
    unary_replies: u32,
    ended_reason: String,
    session_secs: u64,
}

async fn run_stream_session(env: &Env, storage: &Storage) -> Result<SessionReport> {
    let session_secs = parse_u64_env(env, "SESSION_SECS", DEFAULT_SESSION_SECS).min(14 * 60);
    let mut resume_after_message_id = storage.get::<i64>(STORAGE_RESUME).await?.unwrap_or(0);
    let mut messages_seen = 0u32;
    let mut pings_seen = 0u32;
    let unary_replies = 0u32;

    let mut client = grpc_client(env)?;
    let request = StreamChatGroupsRequest {
        resume_after_message_id,
        resume_after_event_id: 0,
    };
    let mut stream = client
        .stream_chat_groups(request)
        .await
        .map_err(|e| Error::RustError(format!("open stream: {e}")))?
        .into_inner();

    let started = js_sys::Date::now();
    let session_ms = (session_secs as f64) * 1000.0;
    let idle_ms = (IDLE_SECS * 1000) as u32;
    let mut last_event = js_sys::Date::now();
    let ended_reason;

    loop {
        if js_sys::Date::now() - started >= session_ms {
            ended_reason = "session_cap".into();
            break;
        }
        if unary_replies >= 50 {
            ended_reason = "subrequest_budget".into();
            break;
        }

        let wait_ms = idle_ms.saturating_sub((js_sys::Date::now() - last_event) as u32);
        let next = select(
            Box::pin(stream.message()),
            TimeoutFuture::new(wait_ms.max(1)),
        )
        .await;

        match next {
            Either::Right((_, _)) => {
                ended_reason = "idle_timeout".into();
                break;
            }
            Either::Left((Ok(None), _)) => {
                ended_reason = "stream_ended".into();
                break;
            }
            Either::Left((Err(status), _)) => {
                ended_reason = format!("stream_error:{status}");
                break;
            }
            Either::Left((Ok(Some(event)), _)) => {
                last_event = js_sys::Date::now();
                match event.item {
                    Some(StreamItem::Ping(_)) => {
                        pings_seen += 1;
                    }
                    Some(StreamItem::Message(msg)) => {
                        if msg.id > resume_after_message_id {
                            resume_after_message_id = msg.id;
                        }
                        messages_seen += 1;
                        console_log!(
                            "spike message id={} group={} text_len={}",
                            msg.id,
                            msg.group_id,
                            msg.content.len()
                        );
                    }
                    _ => {}
                }
            }
        }
    }

    storage.put(STORAGE_RESUME, resume_after_message_id).await?;
    let report = SessionReport {
        resume_after_message_id,
        messages_seen,
        pings_seen,
        unary_replies,
        ended_reason,
        session_secs,
    };
    let status_json = serde_json::to_string(&report)
        .map_err(|e| Error::RustError(format!("serialize status: {e}")))?;
    storage.put(STORAGE_LAST_STATUS, status_json).await?;
    Ok(report)
}

#[durable_object]
pub struct BotSession {
    state: State,
    env: Env,
}

impl BotSession {
    async fn is_running(&self) -> Result<bool> {
        Ok(self
            .state
            .storage()
            .get::<bool>(STORAGE_RUNNING)
            .await?
            .unwrap_or(false))
    }

    async fn set_running(&self, running: bool) -> Result<()> {
        let storage = self.state.storage();
        storage.put(STORAGE_RUNNING, running).await?;
        if running {
            storage
                .put(STORAGE_RUNNING_SINCE_MS, js_sys::Date::now())
                .await?;
        } else {
            let _ = storage.delete(STORAGE_RUNNING_SINCE_MS).await;
        }
        Ok(())
    }

    fn session_cap_ms(&self) -> f64 {
        (parse_u64_env(&self.env, "SESSION_SECS", DEFAULT_SESSION_SECS).min(14 * 60) as f64)
            * 1000.0
            + 30_000.0
    }
}

impl DurableObject for BotSession {
    fn new(state: State, env: Env) -> Self {
        Self { state, env }
    }

    async fn fetch(&self, req: Request) -> Result<Response> {
        let path = req.path();
        let protected = matches!(
            (req.method(), path.as_str()),
            (Method::Get, "/status")
                | (Method::Post, "/ensure")
                | (Method::Post, "/stop")
                | (Method::Post, "/unary")
                | (Method::Post, "/session-once")
        );
        if protected && !control_authorized(&req, &self.env) {
            return unauthorized();
        }

        match (req.method(), path.as_str()) {
            (Method::Get, "/status") => {
                let resume = self
                    .state
                    .storage()
                    .get::<i64>(STORAGE_RESUME)
                    .await?
                    .unwrap_or(0);
                let last = self
                    .state
                    .storage()
                    .get::<String>(STORAGE_LAST_STATUS)
                    .await?
                    .unwrap_or_else(|| "{}".into());
                let alarm = self.state.storage().get_alarm().await?;
                Response::from_json(&serde_json::json!({
                    "running": self.is_running().await?,
                    "resume_after_message_id": resume,
                    "alarm_ms": alarm,
                    "last_status": serde_json::from_str::<serde_json::Value>(&last).unwrap_or_default(),
                }))
            }
            (Method::Post, "/ensure") => {
                // Clear a stale running flag after isolate eviction mid-session.
                self.set_running(false).await?;
                self.state
                    .storage()
                    .set_alarm(Duration::from_secs(0))
                    .await?;
                Response::ok("alarm scheduled")
            }
            (Method::Post, "/stop") => {
                self.state.storage().delete_alarm().await?;
                self.set_running(false).await?;
                Response::ok("alarm cleared")
            }
            (Method::Post, "/unary") => {
                let group_id: i64 = env_string(&self.env, "CHANNEL_ID_TEST")?
                    .parse()
                    .map_err(|e| Error::RustError(format!("CHANNEL_ID_TEST: {e}")))?;
                let id = send_unary(
                    &self.env,
                    group_id,
                    &format!("cf_spike unary {}", Uuid::new_v4()),
                )
                .await?;
                Response::ok(format!("sent message_id={id}"))
            }
            (Method::Post, "/session-once") => {
                if self.is_running().await? {
                    return Response::error("session already running", 409);
                }
                self.set_running(true).await?;
                let report = match run_stream_session(&self.env, &self.state.storage()).await {
                    Ok(r) => {
                        self.set_running(false).await?;
                        r
                    }
                    Err(e) => {
                        self.set_running(false).await?;
                        let _ = self.state.storage().set_alarm(Duration::from_secs(2)).await;
                        return Err(e);
                    }
                };
                Response::from_json(&report)
            }
            _ => Response::error("not found", 404),
        }
    }

    async fn alarm(&self) -> Result<Response> {
        if self.is_running().await? {
            let since = self
                .state
                .storage()
                .get::<f64>(STORAGE_RUNNING_SINCE_MS)
                .await?
                .unwrap_or(0.0);
            let age_ms = js_sys::Date::now() - since;
            if age_ms > self.session_cap_ms() {
                console_log!("alarm cleared stale running flag (age_ms={age_ms})");
                self.set_running(false).await?;
                self.state
                    .storage()
                    .set_alarm(Duration::from_secs(0))
                    .await?;
                return Response::ok("stale_running_cleared");
            }
            console_log!("alarm deferred: session still running (age_ms={age_ms})");
            self.state
                .storage()
                .set_alarm(Duration::from_secs(30))
                .await?;
            return Response::ok("deferred");
        }
        self.set_running(true).await?;
        let result = run_stream_session(&self.env, &self.state.storage()).await;
        self.set_running(false).await?;

        match result {
            Ok(report) => {
                console_log!(
                    "alarm session done reason={} resume={} msgs={} pings={}",
                    report.ended_reason,
                    report.resume_after_message_id,
                    report.messages_seen,
                    report.pings_seen
                );
                self.state
                    .storage()
                    .set_alarm(Duration::from_secs(0))
                    .await?;
                Response::from_json(&report)
            }
            Err(e) => {
                console_error!("alarm session error: {e:?}");
                self.state
                    .storage()
                    .set_alarm(Duration::from_secs(5))
                    .await?;
                Err(e)
            }
        }
    }
}

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let url = req.url()?;
    let path = url.path().to_string();

    // Route control plane to the single spike DO.
    let namespace = env.durable_object("BOT_SESSION")?;
    let id = namespace.id_from_name("spike")?;
    let stub = id.get_stub()?;

    match path.as_str() {
        "/" => Response::ok(
            "onechat-cf-spike: POST /ensure|/stop|/unary|/session-once GET /status (Bearer CONTROL_TOKEN)",
        ),
        "/ensure" | "/stop" | "/unary" | "/session-once" | "/status" => {
            stub.fetch_with_request(req).await
        }
        _ => Response::error("not found", 404),
    }
}
