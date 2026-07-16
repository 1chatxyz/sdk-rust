//! Domain types for inbound events (stable for bots / agents).

use std::collections::HashSet;

/// A chat group message delivered to the bot.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncomingMessage {
    /// Server message id.
    pub id: i64,
    /// Chat group id.
    pub group_id: i64,
    /// Sender user id.
    pub sender_user_id: i64,
    /// Sender username (may be empty).
    pub sender_username: String,
    /// Message text content.
    pub text: String,
    /// Mentioned user ids from the wire payload.
    pub mentioned_user_ids: Vec<i64>,
    /// Image attachment paths/URLs.
    pub images: Vec<String>,
    /// File attachment paths/URLs.
    pub files: Vec<String>,
}

/// Typing indicator in a group.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncomingTyping {
    /// Chat group id.
    pub group_id: i64,
    /// User who is typing.
    pub user_id: i64,
    /// Username (may be empty).
    pub username: String,
    /// Whether typing started or stopped.
    pub typing: bool,
}

/// A direct-message payload.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncomingDirectMessage {
    /// Server message id.
    pub id: i64,
    /// DM thread id.
    pub thread_id: i64,
    /// Sender user id.
    pub sender_user_id: i64,
    /// Sender username (may be empty).
    pub sender_username: String,
    /// Message text content.
    pub text: String,
    /// Image attachment paths/URLs.
    pub images: Vec<String>,
    /// File attachment paths/URLs.
    pub files: Vec<String>,
}

/// High-level inbound events (pings never surface here).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum IncomingEvent {
    /// A chat group message.
    GroupMessage(IncomingMessage),
    /// A typing indicator in a group.
    Typing(IncomingTyping),
    /// A direct message.
    DirectMessage(IncomingDirectMessage),
    /// A typing indicator in a DM thread.
    DirectTyping {
        /// DM thread id.
        thread_id: i64,
        /// User who is typing.
        user_id: i64,
        /// Whether typing started or stopped.
        typing: bool,
    },
}

/// Filters applied inside [`crate::Client::subscribe_groups`].
#[derive(Debug, Clone, Default)]
pub struct SubscribeOptions {
    /// When set, only these group ids are yielded.
    pub allowlist: Option<HashSet<i64>>,
    /// Drop messages from the configured bot `user_id` (default true when user_id is set).
    pub ignore_self: bool,
    /// When true, only yield messages that mention the bot (by id or username).
    pub require_mention: bool,
}

impl SubscribeOptions {
    /// Defaults: ignore self when `user_id` is configured; no allowlist / mention gate.
    pub fn new() -> Self {
        Self {
            allowlist: None,
            ignore_self: true,
            require_mention: false,
        }
    }
}
