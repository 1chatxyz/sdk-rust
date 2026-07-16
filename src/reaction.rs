//! Emoji reactions on group and DM messages.

use crate::client::Client;
use crate::error::Result;
use crate::pb::genjutsu::myconversation::v1::{
    SetChatGroupMessageReactionRequest, SetDirectMessageReactionRequest,
};

/// A reaction row returned by the API.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Reaction {
    /// Reaction row id.
    pub id: i64,
    /// User who reacted.
    pub user_id: i64,
    /// Emoji string.
    pub emoji: String,
}

impl Client {
    /// Add or remove a reaction on a group message.
    pub async fn react_group_message(
        &self,
        message_id: i64,
        emoji: impl Into<String>,
        remove: bool,
    ) -> Result<Vec<Reaction>> {
        let mut client = self.unary_rpc();
        let reply = client
            .set_chat_group_message_reaction(SetChatGroupMessageReactionRequest {
                message_id,
                emoji: emoji.into(),
                remove,
            })
            .await?
            .into_inner();
        Ok(reply
            .reactions
            .into_iter()
            .map(|r| Reaction {
                id: r.id,
                user_id: r.user_id,
                emoji: r.emoji,
            })
            .collect())
    }

    /// Add or remove a reaction on a direct message.
    pub async fn react_dm_message(
        &self,
        message_id: i64,
        emoji: impl Into<String>,
        remove: bool,
    ) -> Result<Vec<Reaction>> {
        let mut client = self.unary_rpc();
        let reply = client
            .set_direct_message_reaction(SetDirectMessageReactionRequest {
                message_id,
                emoji: emoji.into(),
                remove,
            })
            .await?
            .into_inner();
        Ok(reply
            .reactions
            .into_iter()
            .map(|r| Reaction {
                id: r.id,
                user_id: r.user_id,
                emoji: r.emoji,
            })
            .collect())
    }
}
