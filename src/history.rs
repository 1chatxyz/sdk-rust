//! History / reply-thread list helpers.

use crate::client::Client;
use crate::error::{Error, Result};
use crate::listen::{map_dm_message, map_group_message};
use crate::pb::genjutsu::myconversation::v1::{
    ListChatGroupMessageThreadsRequest, ListChatGroupMessagesRequest,
    ListChatGroupThreadMessagesRequest, ListDirectMessageReplyMessagesRequest,
    ListDirectMessageReplyThreadsRequest, ListDirectMessagesRequest,
};
use crate::types::{IncomingDirectMessage, IncomingMessage, SubscribeOptions};

/// Pagination / filter options for listing timeline messages.
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct ListMessagesOptions {
    /// Page size (server default when `0`).
    pub page_size: i32,
    /// Exclusive upper bound (older page).
    pub before_message_id: i64,
    /// Exclusive lower bound (newer page).
    pub after_message_id: i64,
    /// Inclusive anchor window.
    pub around_message_id: i64,
    /// Group topic id (`0` = main channel). Ignored for DMs.
    pub topic_id: i64,
}

impl ListMessagesOptions {
    /// Defaults (newest page, main channel).
    pub fn new() -> Self {
        Self::default()
    }
}

/// One page of group timeline messages (message items only).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct GroupMessagesPage {
    /// Messages oldest-first within the page.
    pub messages: Vec<IncomingMessage>,
    /// More older messages exist.
    pub has_older: bool,
    /// More newer messages exist.
    pub has_newer: bool,
}

/// One page of DM timeline messages.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct DmMessagesPage {
    /// Messages in server order.
    pub messages: Vec<IncomingDirectMessage>,
    /// More older messages exist.
    pub has_older: bool,
    /// More newer messages exist.
    pub has_newer: bool,
}

/// Summary of an active reply thread.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct MessageThreadInfo {
    /// Root (parent) message id.
    pub root_message_id: i64,
    /// Number of replies (excludes root).
    pub reply_count: i64,
    /// Last reply message id (`0` when none).
    pub last_reply_message_id: i64,
    /// Caller unread reply count.
    pub unread_count: i64,
    /// Topic id for group threads (`0` for main / DMs).
    pub topic_id: i64,
    /// Root message when the server includes it.
    pub root_message: Option<IncomingMessage>,
    /// Last reply when the server includes it.
    pub last_reply: Option<IncomingMessage>,
}

/// DM reply-thread summary (root/last as DM payloads).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct DmMessageThreadInfo {
    /// Root (parent) message id.
    pub root_message_id: i64,
    /// Number of replies (excludes root).
    pub reply_count: i64,
    /// Last reply message id (`0` when none).
    pub last_reply_message_id: i64,
    /// Caller unread reply count.
    pub unread_count: i64,
    /// Root message when present.
    pub root_message: Option<IncomingDirectMessage>,
    /// Last reply when present.
    pub last_reply: Option<IncomingDirectMessage>,
}

/// Page of group reply threads.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct GroupThreadsPage {
    /// Threads sorted by last reply.
    pub threads: Vec<MessageThreadInfo>,
    /// More threads exist.
    pub has_more: bool,
}

/// Page of DM reply threads.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct DmThreadsPage {
    /// Threads sorted by last reply.
    pub threads: Vec<DmMessageThreadInfo>,
    /// More threads exist.
    pub has_more: bool,
}

/// Page of replies inside one thread.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct GroupThreadMessagesPage {
    /// Reply messages (excludes root).
    pub messages: Vec<IncomingMessage>,
    /// Total replies in the thread.
    pub total_count: i64,
}

/// Page of DM replies inside one thread.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct DmThreadMessagesPage {
    /// Reply messages (excludes root).
    pub messages: Vec<IncomingDirectMessage>,
    /// Total replies in the thread.
    pub total_count: i64,
}

impl Client {
    /// List top-level group timeline messages (filters via [`SubscribeOptions`]).
    pub async fn list_group_messages(
        &self,
        group_id: i64,
        options: ListMessagesOptions,
        filter: SubscribeOptions,
    ) -> Result<GroupMessagesPage> {
        let mut client = self.unary_rpc();
        let reply = client
            .list_chat_group_messages(ListChatGroupMessagesRequest {
                group_id,
                page_size: options.page_size,
                topic_id: options.topic_id,
                before_message_id: options.before_message_id,
                after_message_id: options.after_message_id,
                around_message_id: options.around_message_id,
            })
            .await?
            .into_inner();

        let mut messages = Vec::new();
        for event in reply.items {
            if let Some(
                crate::pb::genjutsu::myconversation::v1::chat_group_stream_event::Item::Message(
                    msg,
                ),
            ) = event.item
            {
                if let Some(incoming) = map_group_message(msg, self, &filter) {
                    messages.push(incoming);
                }
            }
        }
        Ok(GroupMessagesPage {
            messages,
            has_older: reply.has_older,
            has_newer: reply.has_newer,
        })
    }

    /// List active reply threads in a group channel/topic.
    pub async fn list_group_threads(
        &self,
        group_id: i64,
        topic_id: i64,
        page_size: i32,
        unread_only: bool,
    ) -> Result<GroupThreadsPage> {
        let mut client = self.unary_rpc();
        let reply = client
            .list_chat_group_message_threads(ListChatGroupMessageThreadsRequest {
                group_id,
                topic_id,
                unread_only,
                page_size,
                page_before_last_message_at: None,
                page_before_root_message_id: 0,
            })
            .await?
            .into_inner();

        let filter = SubscribeOptions {
            ignore_self: false,
            ignore_system: false,
            ..SubscribeOptions::new()
        };
        let threads = reply
            .threads
            .into_iter()
            .map(|t| {
                let summary = t.thread.unwrap_or_default();
                MessageThreadInfo {
                    root_message_id: summary.root_message_id,
                    reply_count: summary.reply_count,
                    last_reply_message_id: summary.last_reply_message_id,
                    unread_count: summary.unread_count,
                    topic_id: t.topic_id,
                    root_message: t
                        .root_message
                        .and_then(|m| map_group_message(m, self, &filter)),
                    last_reply: t
                        .last_reply
                        .and_then(|m| map_group_message(m, self, &filter)),
                }
            })
            .collect();
        Ok(GroupThreadsPage {
            threads,
            has_more: reply.has_more,
        })
    }

    /// List replies inside one group message thread.
    pub async fn list_group_thread_messages(
        &self,
        group_id: i64,
        root_message_id: i64,
        options: ListMessagesOptions,
        filter: SubscribeOptions,
    ) -> Result<GroupThreadMessagesPage> {
        if root_message_id <= 0 {
            return Err(Error::Config(
                "list_group_thread_messages requires root_message_id > 0".into(),
            ));
        }
        let mut client = self.unary_rpc();
        let reply = client
            .list_chat_group_thread_messages(ListChatGroupThreadMessagesRequest {
                group_id,
                topic_id: options.topic_id,
                root_message_id,
                page_size: options.page_size,
                before_message_id: options.before_message_id,
                after_message_id: options.after_message_id,
                around_message_id: options.around_message_id,
            })
            .await?
            .into_inner();
        let messages = reply
            .messages
            .into_iter()
            .filter_map(|m| map_group_message(m, self, &filter))
            .collect();
        Ok(GroupThreadMessagesPage {
            messages,
            total_count: reply.total_count,
        })
    }

    /// List top-level DM timeline messages.
    pub async fn list_dm_messages(
        &self,
        thread_id: i64,
        options: ListMessagesOptions,
    ) -> Result<DmMessagesPage> {
        let mut client = self.unary_rpc();
        let reply = client
            .list_direct_messages(ListDirectMessagesRequest {
                thread_id,
                page_size: options.page_size,
                before_message_id: options.before_message_id,
                after_message_id: options.after_message_id,
                around_message_id: options.around_message_id,
            })
            .await?
            .into_inner();
        Ok(DmMessagesPage {
            messages: reply.messages.into_iter().map(map_dm_message).collect(),
            has_older: reply.has_older,
            has_newer: reply.has_newer,
        })
    }

    /// List active reply threads under a DM conversation.
    pub async fn list_dm_threads(
        &self,
        thread_id: i64,
        page_size: i32,
        unread_only: bool,
    ) -> Result<DmThreadsPage> {
        let mut client = self.unary_rpc();
        let reply = client
            .list_direct_message_reply_threads(ListDirectMessageReplyThreadsRequest {
                thread_id,
                unread_only,
                page_size,
                page_before_last_message_at: None,
                page_before_root_message_id: 0,
            })
            .await?
            .into_inner();
        let threads = reply
            .threads
            .into_iter()
            .map(|t| {
                let summary = t.thread.unwrap_or_default();
                DmMessageThreadInfo {
                    root_message_id: summary.root_message_id,
                    reply_count: summary.reply_count,
                    last_reply_message_id: summary.last_reply_message_id,
                    unread_count: summary.unread_count,
                    root_message: t.root_message.map(map_dm_message),
                    last_reply: t.last_reply.map(map_dm_message),
                }
            })
            .collect();
        Ok(DmThreadsPage {
            threads,
            has_more: reply.has_more,
        })
    }

    /// List replies inside one DM message thread.
    pub async fn list_dm_thread_messages(
        &self,
        thread_id: i64,
        root_message_id: i64,
        options: ListMessagesOptions,
    ) -> Result<DmThreadMessagesPage> {
        if root_message_id <= 0 {
            return Err(Error::Config(
                "list_dm_thread_messages requires root_message_id > 0".into(),
            ));
        }
        let mut client = self.unary_rpc();
        let reply = client
            .list_direct_message_reply_messages(ListDirectMessageReplyMessagesRequest {
                thread_id,
                root_message_id,
                page_size: options.page_size,
                before_message_id: options.before_message_id,
                after_message_id: options.after_message_id,
                around_message_id: options.around_message_id,
            })
            .await?
            .into_inner();
        Ok(DmThreadMessagesPage {
            messages: reply.messages.into_iter().map(map_dm_message).collect(),
            total_count: reply.total_count,
        })
    }
}
