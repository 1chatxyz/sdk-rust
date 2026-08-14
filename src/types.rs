//! Domain types for inbound events (stable for bots / agents).

use std::collections::HashSet;

use crate::pb::genjutsu::myconversation::model::v1::ChatGroupMessageSenderKind as ProtoSenderKind;

/// Attribution kind for a chat group message sender.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum SenderKind {
    /// Proto unspecified / unknown.
    Unspecified,
    /// Tenant staff (myid user).
    User,
    /// Telegram guest via ChatGroup bridge.
    TelegramGuest,
    /// Automated system notice (e.g. keyword → share card).
    System,
}

impl SenderKind {
    pub(crate) fn from_proto(value: i32) -> Self {
        match ProtoSenderKind::try_from(value).unwrap_or(ProtoSenderKind::Unspecified) {
            ProtoSenderKind::Unspecified => Self::Unspecified,
            ProtoSenderKind::User => Self::User,
            ProtoSenderKind::TelegramGuest => Self::TelegramGuest,
            ProtoSenderKind::System => Self::System,
        }
    }
}

/// A chat group message delivered to the bot.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct IncomingMessage {
    /// Server message id.
    pub id: i64,
    /// Chat group id.
    pub group_id: i64,
    /// Sender user id (0 for Telegram guests / system / anonymous).
    pub sender_user_id: i64,
    /// Sender username (may be empty).
    pub sender_username: String,
    /// Message text content.
    pub text: String,
    /// Mentioned staff user ids from the wire payload.
    pub mentioned_user_ids: Vec<i64>,
    /// Image attachment paths/URLs.
    pub images: Vec<String>,
    /// File attachment paths/URLs.
    pub files: Vec<String>,
    /// Who sent this message (staff / Telegram guest / system).
    pub sender_kind: SenderKind,
    /// Telegram user id when [`SenderKind::TelegramGuest`]; otherwise `None`.
    pub telegram_user_id: Option<i64>,
    /// Telegram @username without `@` when guest (may be empty).
    pub telegram_username: String,
    /// Display name snapshot for Telegram guests (may be empty).
    pub telegram_display_name: String,
    /// Guest avatar URL/path (may be empty).
    pub telegram_avatar_url: String,
    /// Telegram guest mention targets (bridged rooms).
    pub mentioned_telegram_user_ids: Vec<i64>,
    /// Voice-note paths/URLs (Telegram bridge ogg/opus).
    pub voices: Vec<String>,
    /// Parent message id when this is a quote/reply; 0 otherwise.
    pub reply_to_message_id: i64,
    /// Thread root id when this is a thread reply; 0 for top-level.
    pub message_thread_root_id: i64,
    /// Group topic id (`0` = main channel).
    pub topic_id: i64,
    /// True when the sender targeted `@all` (staff mentions may be omitted on the wire).
    pub mentions_all: bool,
    /// True when the server hydrates an anonymous sender (staff id hidden).
    pub sender_anonymous: bool,
    /// True when a thread reply was also projected onto the parent timeline.
    pub also_sent_to_timeline: bool,
}

/// Typing indicator in a group.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
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
#[non_exhaustive]
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
    /// Parent message id when this is a quote/reply; 0 otherwise.
    pub reply_to_message_id: i64,
    /// Thread root id when this is a thread reply; 0 for top-level.
    pub message_thread_root_id: i64,
    /// True when a thread reply was also projected onto the main DM timeline.
    pub also_sent_to_timeline: bool,
}

/// Telegram guest join/leave in a bridged chat group.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct IncomingGuestPresence {
    /// Chat group id.
    pub group_id: i64,
    /// `true` when the guest joined; `false` when they left.
    pub joined: bool,
    /// Telegram user id.
    pub telegram_user_id: i64,
    /// Display name snapshot (may be empty).
    pub display_name: String,
    /// Telegram @username without `@` (may be empty).
    pub username: String,
    /// Avatar URL/path (may be empty).
    pub avatar_url: String,
    /// Stream event log id (for resume).
    pub event_id: i64,
}

/// Staff presence state from live stream fanout.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum PresenceState {
    /// Proto unspecified / unknown.
    Unspecified,
    /// Actively online.
    Online,
    /// Idle / away from keyboard.
    Idle,
    /// Offline.
    Offline,
    /// Explicitly away.
    Away,
    /// Do not disturb.
    DoNotDisturb,
}

impl PresenceState {
    #[cfg_attr(target_arch = "wasm32", allow(dead_code))]
    pub(crate) fn from_proto(value: i32) -> Self {
        use crate::pb::genjutsu::myconversation::v1::PresenceState as P;
        match P::try_from(value).unwrap_or(P::Unspecified) {
            P::Unspecified => Self::Unspecified,
            P::Online => Self::Online,
            P::Idle => Self::Idle,
            P::Offline => Self::Offline,
            P::Away => Self::Away,
            P::DoNotDisturb => Self::DoNotDisturb,
        }
    }
}

/// Live staff presence change (not replayed on reconnect).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct IncomingPresence {
    /// Staff user id.
    pub user_id: i64,
    /// Effective presence badge.
    pub presence: PresenceState,
    /// Custom status emoji (may be empty).
    pub custom_status_emoji: String,
    /// Custom status text (may be empty).
    pub custom_status_text: String,
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
    /// Telegram guest joined/left a bridged group.
    GuestPresence(IncomingGuestPresence),
    /// Staff presence change (group or DM stream).
    Presence(IncomingPresence),
}

/// Filters applied inside [`crate::Client::subscribe_groups`] / listen sessions.
#[derive(Debug, Clone)]
#[non_exhaustive]
pub struct SubscribeOptions {
    /// When set, only these group ids are yielded.
    pub allowlist: Option<HashSet<i64>>,
    /// Drop messages from the configured bot `user_id` (default true when user_id is set).
    pub ignore_self: bool,
    /// When true, only yield messages that mention the bot (by id, username, or `@all`).
    pub require_mention: bool,
    /// Drop automated system notices (`SenderKind::System`). Default true.
    pub ignore_system: bool,
}

impl Default for SubscribeOptions {
    fn default() -> Self {
        Self::new()
    }
}

impl SubscribeOptions {
    /// Defaults: ignore self when `user_id` is configured; ignore system; no allowlist / mention gate.
    pub fn new() -> Self {
        Self {
            allowlist: None,
            ignore_self: true,
            require_mention: false,
            ignore_system: true,
        }
    }
}
