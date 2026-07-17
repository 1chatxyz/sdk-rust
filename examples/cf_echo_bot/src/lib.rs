//! Cloudflare Workers echo bot powered by `onechat-sdk`.
//!
//! Alarm-driven Durable Object sessions call [`onechat_sdk::Client::run_group_session`],
//! persist `resume_after_message_id`, and reschedule. Control routes require
//! `Authorization: Bearer $CONTROL_TOKEN`.

use std::cell::Cell;
use std::rc::Rc;
use std::time::Duration;

use gloo_timers::future::TimeoutFuture;
use onechat_sdk::{Client, Config, Error as SdkError, ListenEndReason, SubscribeOptions};
use serde::Serialize;
use worker::{
    Context, DurableObject, Env, Error, Method, Request, Response, Result, State, Storage,
    console_error, console_log, durable_object, event,
};

const STORAGE_RESUME: &str = "resume_after_message_id";
const STORAGE_LAST_STATUS: &str = "last_status";
const STORAGE_RUNNING: &str = "session_running";
const STORAGE_RUNNING_SINCE_MS: &str = "session_running_since_ms";
/// Soft wall used only for stale `session_running` recovery (SDK caps ~14m).
const STALE_RUNNING_MS: f64 = 15.0 * 60.0 * 1000.0;

#[derive(Debug, Serialize)]
struct SessionReport {
    resume_after_message_id: i64,
    messages_echoed: u32,
    ended_reason: String,
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

/// Returns true when the request presents a valid control bearer token.
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

fn sdk_client(env: &Env) -> Result<Client> {
    // Required so SubscribeOptions::ignore_self can drop the bot's own echoes.
    let user_id = env_string(env, "ONECHAT_USER_ID")?;
    let user_id = user_id.trim().to_string();
    if user_id.is_empty() {
        return Err(Error::RustError(
            "ONECHAT_USER_ID is required (self-filter for echo replies)".into(),
        ));
    }
    if user_id.parse::<i64>().is_err() {
        return Err(Error::RustError(
            "ONECHAT_USER_ID must be a numeric user id".into(),
        ));
    }
    let config = Config {
        api_url: env_string(env, "API_1CHAT_URL")?,
        tenant_id: env_string(env, "TENANT_ID")?,
        bot_token: env_string(env, "BOT_TOKEN")?,
        user_id: Some(user_id),
        username: env_string(env, "ONECHAT_USERNAME")
            .ok()
            .filter(|s| !s.is_empty()),
    }
    .normalized();
    Client::try_new(config).map_err(|e| Error::RustError(format!("client: {e}")))
}

fn end_reason_label(reason: ListenEndReason) -> &'static str {
    match reason {
        ListenEndReason::IdleTimeout => "idle_timeout",
        ListenEndReason::MaxAge => "max_age",
        ListenEndReason::StreamEnded => "stream_ended",
        ListenEndReason::StreamError => "stream_error",
    }
}

async fn run_echo_session(env: &Env, storage: &Storage) -> Result<SessionReport> {
    let client = sdk_client(env)?;
    let mut resume_after_message_id = storage.get::<i64>(STORAGE_RESUME).await?.unwrap_or(0);
    let messages_echoed = Rc::new(Cell::new(0u32));
    let inflight = Rc::new(Cell::new(0u32));
    let echoed = Rc::clone(&messages_echoed);
    let inflight_h = Rc::clone(&inflight);

    // Cannot `await` unary while the listen stream is open (Workers Fetch deadlock).
    // Spawn replies and wait for in-flight work before the alarm returns.
    let outcome = match client
        .run_group_session(
            resume_after_message_id,
            SubscribeOptions::new(),
            move |client, msg| {
                let echoed = Rc::clone(&echoed);
                let inflight_h = Rc::clone(&inflight_h);
                async move {
                    console_log!(
                        "echo inbound id={} group={} from={} text_len={}",
                        msg.id,
                        msg.group_id,
                        msg.sender_user_id,
                        msg.text.len()
                    );
                    let group_id = msg.group_id;
                    let reply = format!("echo: {}", msg.text);
                    inflight_h.set(inflight_h.get().saturating_add(1));
                    let inflight_done = Rc::clone(&inflight_h);
                    let echoed_done = Rc::clone(&echoed);
                    wasm_bindgen_futures::spawn_local(async move {
                        match client.reply_group(group_id, reply).await {
                            Ok(_) => {
                                console_log!("echo reply ok group={group_id}");
                                echoed_done.set(echoed_done.get().saturating_add(1));
                            }
                            Err(err) => console_log!("echo reply err: {err}"),
                        }
                        inflight_done.set(inflight_done.get().saturating_sub(1));
                    });
                    Ok(())
                }
            },
        )
        .await
    {
        Ok(out) => out,
        Err(SdkError::Listen {
            resume_after_message_id: r,
            source,
        }) => {
            resume_after_message_id = r;
            storage.put(STORAGE_RESUME, resume_after_message_id).await?;
            return Err(Error::RustError(format!("listen: {source} (resume={r})")));
        }
        Err(err) => return Err(Error::RustError(format!("listen: {err}"))),
    };

    // Drain background replies so the DO invocation does not finish early.
    for _ in 0..200 {
        if inflight.get() == 0 {
            break;
        }
        TimeoutFuture::new(50).await;
    }
    if inflight.get() != 0 {
        console_log!(
            "warning: {} echo replies still in flight at session end",
            inflight.get()
        );
    }

    resume_after_message_id = outcome.resume_after_message_id;
    storage.put(STORAGE_RESUME, resume_after_message_id).await?;

    let report = SessionReport {
        resume_after_message_id,
        messages_echoed: messages_echoed.get(),
        ended_reason: end_reason_label(outcome.reason).into(),
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
            (Method::Post, "/session-once") => {
                if self.is_running().await? {
                    return Response::error("session already running", 409);
                }
                self.set_running(true).await?;
                let report = match run_echo_session(&self.env, &self.state.storage()).await {
                    Ok(r) => {
                        self.set_running(false).await?;
                        r
                    }
                    Err(e) => {
                        self.set_running(false).await?;
                        // Do not schedule an alarm — this route is one-shot only.
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
            if age_ms > STALE_RUNNING_MS {
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
        let result = run_echo_session(&self.env, &self.state.storage()).await;
        self.set_running(false).await?;

        match result {
            Ok(report) => {
                console_log!(
                    "alarm session done reason={} resume={} echoed={}",
                    report.ended_reason,
                    report.resume_after_message_id,
                    report.messages_echoed
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

    let namespace = env.durable_object("BOT_SESSION")?;
    let id = namespace.id_from_name("echo")?;
    let stub = id.get_stub()?;

    match path.as_str() {
        "/" => Response::ok(
            "onechat-cf-echo-bot: POST /ensure|/stop|/session-once GET /status (Bearer CONTROL_TOKEN)",
        ),
        "/ensure" | "/stop" | "/session-once" | "/status" => stub.fetch_with_request(req).await,
        _ => Response::error("not found", 404),
    }
}
