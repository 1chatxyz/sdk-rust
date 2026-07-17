//! Client configuration.

use std::fmt;

use crate::error::{Error, Result};

/// Configuration for connecting to the 1Chat Envoy gateway.
#[derive(Clone, PartialEq, Eq)]
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

impl fmt::Debug for Config {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Config")
            .field("api_url", &self.api_url)
            .field("tenant_id", &self.tenant_id)
            .field("bot_token", &"[redacted]")
            .field("user_id", &self.user_id)
            .field("username", &self.username)
            .finish()
    }
}

impl Config {
    /// Trim whitespace on string fields (safe for `.env` copy/paste).
    pub fn normalized(mut self) -> Self {
        self.api_url = self.api_url.trim().to_string();
        self.tenant_id = self.tenant_id.trim().to_string();
        self.bot_token = self.bot_token.trim().to_string();
        self.user_id = self
            .user_id
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());
        self.username = self
            .username
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());
        self
    }

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
    ///
    /// Not available on `wasm32` (use [`Config`] + [`crate::Client::try_new`] with
    /// Wrangler secrets / bindings).
    #[cfg(not(target_arch = "wasm32"))]
    pub fn from_env() -> Result<Self> {
        let config = Self {
            api_url: require_env("API_1CHAT_URL")?,
            tenant_id: require_env("TENANT_ID")?,
            bot_token: require_env("BOT_TOKEN")?,
            user_id: std::env::var("ONECHAT_USER_ID").ok(),
            username: std::env::var("ONECHAT_USERNAME").ok(),
        }
        .normalized();
        config.validate()?;
        Ok(config)
    }
}

#[cfg(not(target_arch = "wasm32"))]
fn require_env(key: &str) -> Result<String> {
    std::env::var(key).map_err(|_| Error::Config(format!("missing environment variable {key}")))
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

    #[test]
    fn debug_redacts_bot_token() {
        let cfg = Config {
            api_url: "https://gw.example".into(),
            tenant_id: "t".into(),
            bot_token: "super-secret".into(),
            user_id: None,
            username: None,
        };
        let rendered = format!("{cfg:?}");
        assert!(!rendered.contains("super-secret"));
        assert!(rendered.contains("[redacted]"));
    }

    #[test]
    fn normalized_trims_whitespace() {
        let cfg = Config {
            api_url: "  https://gw.example  ".into(),
            tenant_id: " tenant \n".into(),
            bot_token: " tok ".into(),
            user_id: Some(" 42 ".into()),
            username: Some(" bot ".into()),
        }
        .normalized();
        assert_eq!(cfg.api_url, "https://gw.example");
        assert_eq!(cfg.tenant_id, "tenant");
        assert_eq!(cfg.bot_token, "tok");
        assert_eq!(cfg.user_id.as_deref(), Some("42"));
        assert_eq!(cfg.username.as_deref(), Some("bot"));
    }
}
