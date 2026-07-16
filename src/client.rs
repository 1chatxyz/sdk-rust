//! High-level 1Chat client.
//!
//! The SDK always speaks **gRPC-Web** (HTTP/1.1) to `API_1CHAT_URL`, which is
//! expected to be the Envoy gateway. Plain `http://` URLs are still framed as
//! gRPC-Web (not native gRPC).

use std::fmt;
use std::sync::Arc;

use http::Uri;
use hyper_util::client::legacy::Client as HyperClient;
use hyper_util::client::legacy::connect::HttpConnector;
use hyper_util::rt::TokioExecutor;
use tonic::body::Body;
use tonic::service::interceptor::InterceptedService;
use tonic_web::{GrpcWebCall, GrpcWebClientLayer};
use tower::ServiceBuilder;

use crate::config::Config;
use crate::error::{Error, Result};
use crate::pb::genjutsu::myconversation::v1::my_conversation_client::MyConversationClient;
use crate::transport::{AuthInterceptor, normalize_api_url};

/// Authenticated gRPC-Web service stack.
pub(crate) type AuthedGrpcWeb =
    InterceptedService<tonic_web::GrpcWebClientService<HttpClient>, AuthInterceptor>;

/// Hyper client body type expected by `tonic_web::GrpcWebClientLayer`.
pub(crate) type HttpClient =
    HyperClient<hyper_rustls::HttpsConnector<HttpConnector>, GrpcWebCall<Body>>;

/// Opaque gRPC-Web handle used for unary RPCs.
#[derive(Clone)]
pub(crate) struct UnaryHandle {
    pub(crate) base_uri: Uri,
    pub(crate) http: HttpClient,
    pub(crate) auth: AuthInterceptor,
}

impl fmt::Debug for UnaryHandle {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("UnaryHandle")
            .field("base_uri", &self.base_uri)
            .field("auth", &self.auth)
            .finish_non_exhaustive()
    }
}

/// Opaque gRPC-Web handle used for server streams.
///
/// Kept separate from [`UnaryHandle`] so long-lived streams do not share a
/// connection with unary traffic (parity with the TypeScript reference).
#[derive(Clone)]
pub(crate) struct StreamHandle {
    pub(crate) base_uri: Uri,
    pub(crate) http: HttpClient,
    pub(crate) auth: AuthInterceptor,
}

impl fmt::Debug for StreamHandle {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("StreamHandle")
            .field("base_uri", &self.base_uri)
            .field("auth", &self.auth)
            .finish_non_exhaustive()
    }
}

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
        let unary_http = build_http_client()?;
        let stream_http = build_http_client()?;

        Ok(Self {
            config: Arc::new(config),
            base_url,
            unary: UnaryHandle {
                base_uri: base_uri.clone(),
                http: unary_http,
                auth: auth.clone(),
            },
            stream: StreamHandle {
                base_uri,
                http: stream_http,
                auth,
            },
        })
    }

    /// Load config from the environment and construct a client.
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
        bind_rpc(
            self.unary.http.clone(),
            self.unary.auth.clone(),
            self.unary.base_uri.clone(),
        )
    }

    /// Tonic client bound to the stream HTTP stack.
    pub(crate) fn stream_rpc(&self) -> MyConversationClient<AuthedGrpcWeb> {
        bind_rpc(
            self.stream.http.clone(),
            self.stream.auth.clone(),
            self.stream.base_uri.clone(),
        )
    }
}

fn bind_rpc(
    http: HttpClient,
    auth: AuthInterceptor,
    base_uri: Uri,
) -> MyConversationClient<AuthedGrpcWeb> {
    let svc = ServiceBuilder::new()
        .layer(GrpcWebClientLayer::new())
        .service(http);
    let svc = InterceptedService::new(svc, auth);
    MyConversationClient::with_origin(svc, base_uri)
}

fn build_http_client() -> Result<HttpClient> {
    let https = hyper_rustls::HttpsConnectorBuilder::new()
        .with_webpki_roots()
        .https_or_http()
        .enable_http1()
        .build();

    Ok(HyperClient::builder(TokioExecutor::new()).build(https))
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
