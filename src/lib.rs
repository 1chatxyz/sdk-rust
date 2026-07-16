//! Rust SDK for [1chat.xyz](https://1chat.xyz).
//!
//! Speaks **gRPC-Web** to the Envoy gateway URL in `API_1CHAT_URL`.
//! Authenticate with `TENANT_ID` + `BOT_TOKEN`.
//!
//! # M0 status
//!
//! Construction and transport only. Group reply arrives in M1; subscribe /
//! reconnect in M2. See `AGENTS.md` and `.cursor/plans/2_roadmap.md`.
//!
//! ```rust,no_run
//! use onechat_sdk::{Client, Config};
//!
//! let client = Client::try_new(Config {
//!     api_url: std::env::var("API_1CHAT_URL").unwrap(),
//!     tenant_id: std::env::var("TENANT_ID").unwrap(),
//!     bot_token: std::env::var("BOT_TOKEN").unwrap(),
//!     user_id: None,
//!     username: None,
//! })
//! .unwrap();
//! let _ = client.base_url();
//! ```

#![deny(missing_docs)]

mod client;
mod config;
mod error;
mod pb;
mod transport;

pub use client::Client;
pub use config::Config;
pub use error::{Error, Result};
