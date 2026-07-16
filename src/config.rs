//! Client configuration.

use crate::error::{Error, Result};

/// Configuration for connecting to the 1Chat Envoy gateway.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Config {
    /// Envoy gateway base URL (`API_1CHAT_URL`). Already the gateway; no proxy needed.
    pub api_url: String,
    /// Tenant id sent as `x-tenant-id` (`TENANT_ID`).
    pub tenant_id: String,
    /// Bot token sent as `Authorization: Bearer …` (`BOT_TOKEN`).
    pub bot_token: String,
    /// Optional bot user id (self-filter / mentions).
    pub user_id: Option<String>,
    /// Optional bot username (mention matching).
    pub username: Option<String>,
}

impl Config {
    /// Validate required fields.
    pub fn validate(&self) -> Result<()> {
        if self.api_url.trim().is_empty() {
            return Err(Error::Config("api_url must not be empty".into()));
        }
        if self.tenant_id.trim().is_empty() {
            return Err(Error::Config("tenant_id must not be empty".into()));
        }
        if self.bot_token.trim().is_empty() {
            return Err(Error::Config("bot_token must not be empty".into()));
        }
        Ok(())
    }

    /// Load from `API_1CHAT_URL`, `TENANT_ID`, and `BOT_TOKEN`.
    pub fn from_env() -> Result<Self> {
        let api_url = std::env::var("API_1CHAT_URL")
            .map_err(|_| Error::Config("missing environment variable API_1CHAT_URL".into()))?;
        let tenant_id = std::env::var("TENANT_ID")
            .map_err(|_| Error::Config("missing environment variable TENANT_ID".into()))?;
        let bot_token = std::env::var("BOT_TOKEN")
            .map_err(|_| Error::Config("missing environment variable BOT_TOKEN".into()))?;
        let user_id = std::env::var("ONECHAT_USER_ID")
            .ok()
            .filter(|s| !s.trim().is_empty());
        let username = std::env::var("ONECHAT_USERNAME")
            .ok()
            .filter(|s| !s.trim().is_empty());
        let config = Self {
            api_url,
            tenant_id,
            bot_token,
            user_id,
            username,
        };
        config.validate()?;
        Ok(config)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_empty_fields() {
        let err = Config {
            api_url: String::new(),
            tenant_id: "t".into(),
            bot_token: "b".into(),
            user_id: None,
            username: None,
        }
        .validate()
        .unwrap_err();
        assert!(matches!(err, Error::Config(_)));
    }
}
