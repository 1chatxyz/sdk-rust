//! Rust SDK for [1chat.xyz](https://1chat.xyz).
//!
//! Speaks **gRPC-Web** to the Envoy gateway URL in `API_1CHAT_URL`.
//! Authenticate with `TENANT_ID` + `BOT_TOKEN`.
//!
//! # Status
//!
//! - M0: construction + transport
//! - M1: `reply_group` / `send_group_text` / `set_typing`
//! - M2+: `subscribe_groups` with reconnect
//!
//! See `AGENTS.md` and `.cursor/plans/2_roadmap.md`.
//!
//! ```rust,no_run
//! use onechat_sdk::{Client, Config};
//!
//! # async fn demo() -> onechat_sdk::Result<()> {
//! let client = Client::from_env()?;
//! client.reply_group(123, "hello").await?;
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
mod transport;

pub use chunking::{TEXT_CHUNK_LIMIT, chunk_text};
pub use client::Client;
pub use config::Config;
pub use error::{Error, Result};
pub use group::SendGroupMessageResult;
pub use mention::{extract_mentioned_user_ids, format_mention};
