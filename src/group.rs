//! Group chat send / typing APIs.

use uuid::Uuid;

use crate::chunking::chunk_text;
use crate::client::Client;
use crate::error::{Error, Result};
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

impl Client {
    /// Send a single group message chunk (no auto-chunking).
    pub async fn send_group_text(
        &self,
        group_id: i64,
        text: impl Into<String>,
        mentioned_user_ids: impl IntoIterator<Item = i64>,
    ) -> Result<i64> {
        let content = text.into();
        let mentioned_user_ids: Vec<i64> = mentioned_user_ids.into_iter().collect();
        let req = SendChatGroupMessageRequest {
            group_id,
            content,
            mentioned_user_ids,
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
        let chunks = chunk_text(text.as_ref());
        if chunks.is_empty() {
            return Ok(SendGroupMessageResult {
                message_ids: Vec::new(),
            });
        }

        let mentions = extract_mentioned_user_ids(text.as_ref());
        let mut message_ids = Vec::with_capacity(chunks.len());
        for (i, chunk) in chunks.into_iter().enumerate() {
            let ids = if i == 0 { mentions.clone() } else { Vec::new() };
            match self.send_group_text(group_id, chunk, ids).await {
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
