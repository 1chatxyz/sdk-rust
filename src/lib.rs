//! Rust SDK for [1chat.xyz](https://1chat.xyz).
//!
//! Speaks **gRPC-Web** to the Envoy gateway URL in `API_1CHAT_URL`.
//! Authenticate with `TENANT_ID` + `BOT_TOKEN`.
//!
//! # Features
//!
//! - Groups: `reply_group`, `run_group_bot` (in-task reconnect; all targets), `subscribe_groups` (native)
//! - DMs: `reply_dm`, `run_dm_bot`, `subscribe_dms` (native), `create_or_get_dm`
//! - Media: `reply_group_with_media`, `download_media_bytes`, `download_media` (native path write)
//! - Reactions: `react_group_message`, `react_dm_message`
//! - Mentions: [`format_mention`], chunking via [`chunk_text`]
//! - `wasm32`: Fetch gRPC-Web + in-task `run_*_bot` (use inside a Durable Object session)
//!
//! Agent integration guide: `AGENTS.md`. Roadmap: `.cursor/plans/2_roadmap.md`.
//!
//! ```rust,no_run
//! use futures_util::StreamExt;
//! use onechat_sdk::{Client, IncomingEvent, SubscribeOptions};
//!
//! # async fn demo() -> onechat_sdk::Result<()> {
//! let client = Client::from_env()?;
//! let mut events = client.subscribe_groups(SubscribeOptions::new()).await?;
//! while let Some(event) = events.next().await {
//!     if let IncomingEvent::GroupMessage(msg) = event? {
//!         client.reply_group(msg.group_id, "hello").await?;
//!     }
//! }
//! # Ok(())
//! # }
//! ```

#![deny(missing_docs)]

mod async_time;
mod chunking;
mod client;
mod config;
mod dm;
mod error;
mod group;
mod listen;
mod media;
mod mention;
mod pb;
mod reaction;
mod reconnect;
#[cfg(not(target_arch = "wasm32"))]
mod stream;
mod transport;
mod types;

pub use chunking::{TEXT_CHUNK_LIMIT, chunk_text};
pub use client::Client;
pub use config::Config;
#[cfg(not(target_arch = "wasm32"))]
pub use dm::DirectEventStream;
pub use error::{Error, Result};
pub use group::SendGroupMessageResult;
pub use media::{
    MAX_ATTACHMENTS, MAX_FILE_BYTES, MediaKind, MediaUrls, classify_media_path,
    media_urls_from_paths,
};
pub use mention::{extract_mentioned_user_ids, format_mention};
pub use reaction::Reaction;
pub use reconnect::compute_reconnect_delay;
#[cfg(not(target_arch = "wasm32"))]
pub use stream::GroupEventStream;
pub use types::{
    IncomingDirectMessage, IncomingEvent, IncomingMessage, IncomingTyping, SubscribeOptions,
};
