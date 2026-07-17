//! High-level 1Chat client.
//!
//! The SDK always speaks **gRPC-Web** (HTTP/1.1) to `API_1CHAT_URL`, which is
//! expected to be the Envoy gateway. Plain `http://` URLs are still framed as
//! gRPC-Web (not native gRPC).

use std::fmt;
use std::sync::Arc;

use http::Uri;

use crate::config::Config;
use crate::error::{Error, Result};
use crate::pb::genjutsu::myconversation::v1::my_conversation_client::MyConversationClient;
use crate::transport::{AuthInterceptor, normalize_api_url};

#[cfg(not(target_arch = "wasm32"))]
mod native;
#[cfg(target_arch = "wasm32")]
mod wasm;

#[cfg(not(target_arch = "wasm32"))]
use native::{AuthedGrpcWeb, StreamHandle, UnaryHandle, bind_rpc, build_http_client};
#[cfg(target_arch = "wasm32")]
use wasm::{AuthedGrpcWeb, StreamHandle, UnaryHandle, bind_rpc, build_transport};

/// 1Chat SDK client.
///
/// Construct with [`Client::from_env`] or [`Client::try_new`], then use the
/// group / DM / media / reaction methods on this type.
#[derive(Clone)]
pub struct Client {
    config: Arc<Config>,
    base_url: String,
    unary: UnaryHandle,
    stream: StreamHandle,
}

impl fmt::Debug for Client {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Client")
            .field("config", &self.config)
            .field("base_url", &self.base_url)
            .field("unary", &self.unary)
            .field("stream", &self.stream)
            .finish()
    }
}

impl Client {
    /// Build a client from [`Config`] without dialing the network.
    pub fn try_new(config: Config) -> Result<Self> {
        let config = config.normalized();
        config.validate()?;
        let base_url = normalize_api_url(&config.api_url)?;
        let base_uri: Uri = base_url
            .parse()
            .map_err(|e| Error::Transport(format!("invalid api_url after normalize: {e}")))?;

        let auth = AuthInterceptor::new(&config.tenant_id, &config.bot_token);

        #[cfg(not(target_arch = "wasm32"))]
        let (unary, stream) = {
            let unary_http = build_http_client()?;
            let stream_http = build_http_client()?;
            (
                UnaryHandle {
                    base_uri: base_uri.clone(),
                    http: unary_http,
                    auth: auth.clone(),
                },
                StreamHandle {
                    base_uri,
                    http: stream_http,
                    auth,
                },
            )
        };

        #[cfg(target_arch = "wasm32")]
        let (unary, stream) = {
            let transport = build_transport(&base_url)?;
            (
                UnaryHandle {
                    base_uri: base_uri.clone(),
                    transport: transport.clone(),
                    auth: auth.clone(),
                },
                StreamHandle {
                    base_uri,
                    transport,
                    auth,
                },
            )
        };

        Ok(Self {
            config: Arc::new(config),
            base_url,
            unary,
            stream,
        })
    }

    /// Load config from the environment and construct a client.
    ///
    /// Not available on `wasm32` (use [`Client::try_new`] with Wrangler secrets).
    #[cfg(not(target_arch = "wasm32"))]
    pub fn from_env() -> Result<Self> {
        Self::try_new(Config::from_env()?)
    }

    /// Borrow the validated configuration.
    pub fn config(&self) -> &Config {
        &self.config
    }

    /// Normalized gateway base URL.
    pub fn base_url(&self) -> &str {
        &self.base_url
    }

    /// Tonic client bound to the unary HTTP stack.
    pub(crate) fn unary_rpc(&self) -> MyConversationClient<AuthedGrpcWeb> {
        #[cfg(not(target_arch = "wasm32"))]
        {
            bind_rpc(
                self.unary.http.clone(),
                self.unary.auth.clone(),
                self.unary.base_uri.clone(),
            )
        }
        #[cfg(target_arch = "wasm32")]
        {
            bind_rpc(
                self.unary.transport.clone(),
                self.unary.auth.clone(),
                self.unary.base_uri.clone(),
            )
        }
    }

    /// Tonic client bound to the stream HTTP stack.
    pub(crate) fn stream_rpc(&self) -> MyConversationClient<AuthedGrpcWeb> {
        #[cfg(not(target_arch = "wasm32"))]
        {
            bind_rpc(
                self.stream.http.clone(),
                self.stream.auth.clone(),
                self.stream.base_uri.clone(),
            )
        }
        #[cfg(target_arch = "wasm32")]
        {
            bind_rpc(
                self.stream.transport.clone(),
                self.stream.auth.clone(),
                self.stream.base_uri.clone(),
            )
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_config(api_url: &str) -> Config {
        Config {
            api_url: api_url.into(),
            tenant_id: "tenant".into(),
            bot_token: "token".into(),
            user_id: None,
            username: None,
        }
    }

    #[test]
    fn try_new_https_lazy() {
        let client = Client::try_new(sample_config("https://gateway.example.com")).unwrap();
        assert_eq!(client.base_url(), "https://gateway.example.com");
        let _ = client.unary_rpc();
        let _ = client.stream_rpc();
    }

    #[test]
    fn try_new_http_lazy() {
        let client = Client::try_new(sample_config("http://127.0.0.1:9")).unwrap();
        assert_eq!(client.base_url(), "http://127.0.0.1:9");
    }

    #[test]
    fn try_new_rejects_empty_token() {
        let mut cfg = sample_config("https://gateway.example.com");
        cfg.bot_token.clear();
        assert!(matches!(
            Client::try_new(cfg).unwrap_err(),
            Error::Config(_)
        ));
    }
}
