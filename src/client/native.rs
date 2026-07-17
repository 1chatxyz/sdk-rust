//! Native (Tokio + Hyper + tonic-web) transport.

use std::fmt;

use http::Uri;
use hyper_util::client::legacy::Client as HyperClient;
use hyper_util::client::legacy::connect::HttpConnector;
use hyper_util::rt::TokioExecutor;
use tonic::body::Body;
use tonic::service::interceptor::InterceptedService;
use tonic_web::{GrpcWebCall, GrpcWebClientLayer};
use tower::ServiceBuilder;

use crate::error::Result;
use crate::pb::genjutsu::myconversation::v1::my_conversation_client::MyConversationClient;
use crate::transport::AuthInterceptor;

pub(crate) type AuthedGrpcWeb =
    InterceptedService<tonic_web::GrpcWebClientService<HttpClient>, AuthInterceptor>;

pub(crate) type HttpClient =
    HyperClient<hyper_rustls::HttpsConnector<HttpConnector>, GrpcWebCall<Body>>;

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

pub(crate) fn bind_rpc(
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

pub(crate) fn build_http_client() -> Result<HttpClient> {
    let https = hyper_rustls::HttpsConnectorBuilder::new()
        .with_webpki_roots()
        .https_or_http()
        .enable_http1()
        .build();

    Ok(HyperClient::builder(TokioExecutor::new()).build(https))
}
