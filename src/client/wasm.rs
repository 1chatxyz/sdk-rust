//! `wasm32` transport via Fetch (`tonic-web-wasm-client`).

use std::fmt;

use http::Uri;
use tonic_web_wasm_client::Client as WasmGrpcClient;
use tonic_web_wasm_client::options::{Credentials, FetchOptions};

use crate::error::Result;
use crate::pb::genjutsu::myconversation::v1::my_conversation_client::MyConversationClient;
use crate::transport::AuthInterceptor;

pub(crate) type AuthedGrpcWeb =
    tonic::service::interceptor::InterceptedService<WasmGrpcClient, AuthInterceptor>;

#[derive(Clone)]
pub(crate) struct UnaryHandle {
    pub(crate) base_uri: Uri,
    pub(crate) transport: WasmGrpcClient,
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
    pub(crate) transport: WasmGrpcClient,
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
    transport: WasmGrpcClient,
    auth: AuthInterceptor,
    _base_uri: Uri,
) -> MyConversationClient<AuthedGrpcWeb> {
    // Do not use `with_origin`: tonic-web-wasm-client already owns `base_url` and
    // concatenates it with the request path. Absolute origins double-prefix URLs.
    MyConversationClient::with_interceptor(transport, auth)
}

pub(crate) fn build_transport(base_url: &str) -> Result<WasmGrpcClient> {
    let options = FetchOptions::default().credentials(Credentials::Omit);
    Ok(WasmGrpcClient::new_with_options(
        base_url.to_string(),
        options,
    ))
}
