//! Group chat send / typing APIs.

use uuid::Uuid;

use crate::chunking::chunk_text;
use crate::client::Client;
use crate::error::{Error, Result};
use crate::media::MediaUrls;
use crate::mention::extract_mentioned_user_ids;
use crate::pb::genjutsu::myconversation::v1::{
    SendChatGroupMessageRequest, SignalChatGroupTypingRequest,
};

/// Result of sending one or more group message chunks.
#[derive(Debug, Clone)]
pub struct SendGroupMessageResult {
    /// Message ids returned by the server (one per successful chunk).
    pub message_ids: Vec<i64>,
}

/// Optional fields for group sends (reply/thread / Telegram mentions / `@all`).
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct GroupSendOptions {
    /// Quote/reply parent message id (`0` = none).
    pub reply_to_message_id: i64,
    /// Thread root id (`0` = top-level timeline).
    pub message_thread_root_id: i64,
    /// Also project a thread reply onto the parent timeline (requires `message_thread_root_id > 0`).
    pub also_send_to_timeline: bool,
    /// Telegram guest mention targets (mutually exclusive with staff mentions / `mention_all`).
    pub mentioned_telegram_user_ids: Vec<i64>,
    /// Expand mentions to all active group members at send time.
    pub mention_all: bool,
}

impl GroupSendOptions {
    /// Empty options (top-level send, no special mentions).
    pub fn new() -> Self {
        Self::default()
    }

    pub(crate) fn validate(&self, mentioned_user_ids: &[i64]) -> Result<()> {
        if self.also_send_to_timeline && self.message_thread_root_id <= 0 {
            return Err(Error::Config(
                "also_send_to_timeline requires message_thread_root_id > 0".into(),
            ));
        }
        if !self.mentioned_telegram_user_ids.is_empty()
            && (!mentioned_user_ids.is_empty() || self.mention_all)
        {
            return Err(Error::Config(
                "mentioned_telegram_user_ids is mutually exclusive with mentioned_user_ids and mention_all"
                    .into(),
            ));
        }
        Ok(())
    }
}

impl Client {
    /// Send a single group message chunk (no auto-chunking).
    pub async fn send_group_text(
        &self,
        group_id: i64,
        text: impl Into<String>,
        mentioned_user_ids: impl IntoIterator<Item = i64>,
    ) -> Result<i64> {
        self.send_group_message(group_id, text, mentioned_user_ids, MediaUrls::default())
            .await
    }

    /// Send a single group message with optional pre-uploaded media URLs.
    pub async fn send_group_message(
        &self,
        group_id: i64,
        text: impl Into<String>,
        mentioned_user_ids: impl IntoIterator<Item = i64>,
        media: MediaUrls,
    ) -> Result<i64> {
        self.send_group_message_with_options(
            group_id,
            text,
            mentioned_user_ids,
            media,
            GroupSendOptions::new(),
        )
        .await
    }

    /// Send a single group message with [`GroupSendOptions`].
    pub async fn send_group_message_with_options(
        &self,
        group_id: i64,
        text: impl Into<String>,
        mentioned_user_ids: impl IntoIterator<Item = i64>,
        media: MediaUrls,
        options: GroupSendOptions,
    ) -> Result<i64> {
        media.validate()?;
        let content = text.into();
        let mentioned_user_ids: Vec<i64> = mentioned_user_ids.into_iter().collect();
        options.validate(&mentioned_user_ids)?;
        let req = SendChatGroupMessageRequest {
            group_id,
            content,
            mentioned_user_ids,
            client_message_id: Uuid::new_v4().to_string(),
            images: media.images,
            files: media.files,
            reply_to_message_id: options.reply_to_message_id,
            message_thread_root_id: options.message_thread_root_id,
            also_send_to_timeline: options.also_send_to_timeline,
            mentioned_telegram_user_ids: options.mentioned_telegram_user_ids,
            mention_all: options.mention_all,
            ..Default::default()
        };
        let mut client = self.unary_rpc();
        let reply = client.send_chat_group_message(req).await?.into_inner();
        let message_id = reply
            .message
            .map(|m| m.id)
            .ok_or_else(|| Error::Transport("send reply missing message".into()))?;
        Ok(message_id)
    }

    /// Reply in a group: chunk text, extract mentions on the first chunk only.
    pub async fn reply_group(
        &self,
        group_id: i64,
        text: impl AsRef<str>,
    ) -> Result<SendGroupMessageResult> {
        self.reply_group_with_media(group_id, text, MediaUrls::default())
            .await
    }

    /// Reply in a group with media attached to the first chunk only.
    pub async fn reply_group_with_media(
        &self,
        group_id: i64,
        text: impl AsRef<str>,
        media: MediaUrls,
    ) -> Result<SendGroupMessageResult> {
        self.reply_group_with_options(group_id, text, media, GroupSendOptions::new())
            .await
    }

    /// Reply in a group with media and [`GroupSendOptions`] (options apply to the first chunk only).
    pub async fn reply_group_with_options(
        &self,
        group_id: i64,
        text: impl AsRef<str>,
        media: MediaUrls,
        options: GroupSendOptions,
    ) -> Result<SendGroupMessageResult> {
        media.validate()?;
        options.validate(&extract_mentioned_user_ids(text.as_ref()))?;
        let chunks = chunk_text(text.as_ref());
        if chunks.is_empty() && media.images.is_empty() && media.files.is_empty() {
            return Ok(SendGroupMessageResult {
                message_ids: Vec::new(),
            });
        }
        let chunks = if chunks.is_empty() {
            vec![String::new()]
        } else {
            chunks
        };

        let mentions = extract_mentioned_user_ids(text.as_ref());
        let mut message_ids = Vec::with_capacity(chunks.len());
        for (i, chunk) in chunks.into_iter().enumerate() {
            let ids = if i == 0 { mentions.clone() } else { Vec::new() };
            let media = if i == 0 {
                media.clone()
            } else {
                MediaUrls::default()
            };
            let opts = if i == 0 {
                options.clone()
            } else {
                GroupSendOptions::new()
            };
            match self
                .send_group_message_with_options(group_id, chunk, ids, media, opts)
                .await
            {
                Ok(id) => message_ids.push(id),
                Err(e) => {
                    if message_ids.is_empty() {
                        return Err(e);
                    }
                    return Err(Error::Transport(format!(
                        "failed after sending {} chunk(s): {e}",
                        message_ids.len()
                    )));
                }
            }
        }
        Ok(SendGroupMessageResult { message_ids })
    }

    /// Signal typing in a group. `UNIMPLEMENTED` is treated as success (best-effort).
    pub async fn set_typing(&self, group_id: i64, typing: bool) -> Result<()> {
        let req = SignalChatGroupTypingRequest {
            group_id,
            typing,
            topic_id: 0,
        };
        let mut client = self.unary_rpc();
        match client.signal_chat_group_typing(req).await {
            Ok(_) => Ok(()),
            Err(status) if status.code() == tonic::Code::Unimplemented => Ok(()),
            Err(status) => Err(status.into()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn also_send_to_timeline_requires_thread_root() {
        let opts = GroupSendOptions {
            also_send_to_timeline: true,
            message_thread_root_id: 0,
            ..GroupSendOptions::new()
        };
        assert!(matches!(opts.validate(&[]), Err(Error::Config(_))));
    }

    #[test]
    fn telegram_mentions_exclusive_with_staff() {
        let opts = GroupSendOptions {
            mentioned_telegram_user_ids: vec![9],
            ..GroupSendOptions::new()
        };
        assert!(matches!(opts.validate(&[1]), Err(Error::Config(_))));

        let opts = GroupSendOptions {
            mentioned_telegram_user_ids: vec![9],
            mention_all: true,
            ..GroupSendOptions::new()
        };
        assert!(matches!(opts.validate(&[]), Err(Error::Config(_))));
    }

    #[test]
    fn telegram_mentions_ok_alone() {
        let opts = GroupSendOptions {
            mentioned_telegram_user_ids: vec![9],
            message_thread_root_id: 3,
            also_send_to_timeline: true,
            ..GroupSendOptions::new()
        };
        assert!(opts.validate(&[]).is_ok());
    }
}
