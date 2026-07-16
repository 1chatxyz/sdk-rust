//! Rust SDK for [1chat.xyz](https://1chat.xyz).
//!
//! Speaks **gRPC-Web** to the Envoy gateway URL in `API_1CHAT_URL`.
//! Authenticate with `TENANT_ID` + `BOT_TOKEN`.
//!
//! # Status
//!
//! - M1: `reply_group` / `send_group_text` / `set_typing`
//! - M2: `subscribe_groups` / `run_group_bot` with reconnect
//!
//! See `AGENTS.md` and `.cursor/plans/2_roadmap.md`.
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

mod chunking;
mod client;
mod config;
mod error;
mod group;
mod mention;
mod pb;
mod stream;
mod transport;
mod types;

pub use chunking::{TEXT_CHUNK_LIMIT, chunk_text};
pub use client::Client;
pub use config::Config;
pub use error::{Error, Result};
pub use group::SendGroupMessageResult;
pub use mention::{extract_mentioned_user_ids, format_mention};
pub use stream::{GroupEventStream, compute_reconnect_delay};
pub use types::{IncomingEvent, IncomingMessage, IncomingTyping, SubscribeOptions};
