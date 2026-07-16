//! URL normalization and auth metadata for gRPC-Web.

use tonic::metadata::{AsciiMetadataValue, MetadataMap};

use crate::error::{Error, Result};

/// Normalize a gateway endpoint into an absolute `http(s)://` base URL.
///
/// Ported from the Python reference `normalize_grpc_base_url`. The SDK always
/// speaks gRPC-Web to this URL (Envoy); it does not implement a proxy.
pub fn normalize_api_url(endpoint: &str) -> Result<String> {
    let trimmed = endpoint.trim();
    if trimmed.is_empty() {
        return Err(Error::Transport("api_url must not be empty".into()));
    }

    if trimmed.starts_with("http://") || trimmed.starts_with("https://") {
        return Ok(trimmed.to_string());
    }

    // host:443 without scheme → HTTPS.
    if trimmed.ends_with(":443") {
        return Ok(format!("https://{trimmed}"));
    }

    // host:port without scheme — numeric port implies plain HTTP (in-cluster).
    if let Some((host, port)) = trimmed.rsplit_once(':') {
        if !host.is_empty() && port.chars().all(|c| c.is_ascii_digit()) {
            return Ok(format!("http://{trimmed}"));
        }
    }

    let looks_internal =
        trimmed.contains(".svc.") || trimmed.starts_with("127.") || trimmed == "localhost";
    if looks_internal {
        return Ok(format!("http://{trimmed}"));
    }

    Ok(format!("https://{trimmed}:443"))
}

/// Build auth metadata: `authorization` + `x-tenant-id`.
#[allow(dead_code)] // Used by unit tests and upcoming RPC wrappers.
pub(crate) fn auth_metadata(tenant_id: &str, bot_token: &str) -> Result<MetadataMap> {
    let mut map = MetadataMap::new();
    let auth = format!("Bearer {bot_token}");
    let auth_value = AsciiMetadataValue::try_from(auth.as_str())
        .map_err(|e| Error::Config(format!("invalid bot_token for metadata: {e}")))?;
    let tenant_value = AsciiMetadataValue::try_from(tenant_id)
        .map_err(|e| Error::Config(format!("invalid tenant_id for metadata: {e}")))?;
    map.insert("authorization", auth_value);
    map.insert("x-tenant-id", tenant_value);
    Ok(map)
}

/// Auth interceptor attached to every tonic call.
#[derive(Clone, Debug)]
pub struct AuthInterceptor {
    tenant_id: String,
    bot_token: String,
}

impl AuthInterceptor {
    /// Create an interceptor from tenant id and bot token.
    pub fn new(tenant_id: impl Into<String>, bot_token: impl Into<String>) -> Self {
        Self {
            tenant_id: tenant_id.into(),
            bot_token: bot_token.into(),
        }
    }
}

impl tonic::service::Interceptor for AuthInterceptor {
    fn call(
        &mut self,
        mut request: tonic::Request<()>,
    ) -> std::result::Result<tonic::Request<()>, tonic::Status> {
        let meta = request.metadata_mut();
        let auth = format!("Bearer {}", self.bot_token);
        let auth_value = AsciiMetadataValue::try_from(auth.as_str()).map_err(|_| {
            tonic::Status::invalid_argument("bot_token is not valid ASCII metadata")
        })?;
        let tenant_value = AsciiMetadataValue::try_from(self.tenant_id.as_str()).map_err(|_| {
            tonic::Status::invalid_argument("tenant_id is not valid ASCII metadata")
        })?;
        meta.insert("authorization", auth_value);
        meta.insert("x-tenant-id", tenant_value);
        Ok(request)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normalize_https_host() {
        assert_eq!(
            normalize_api_url("gateway01.example.com").unwrap(),
            "https://gateway01.example.com:443"
        );
    }

    #[test]
    fn normalize_http_with_port() {
        assert_eq!(
            normalize_api_url("myconversation.svc:8080").unwrap(),
            "http://myconversation.svc:8080"
        );
    }

    #[test]
    fn normalize_keeps_scheme() {
        assert_eq!(
            normalize_api_url("https://gateway.example.com").unwrap(),
            "https://gateway.example.com"
        );
    }

    #[test]
    fn auth_metadata_pairs() {
        let md = auth_metadata("tenant-1", "tok123").unwrap();
        assert_eq!(
            md.get("authorization").unwrap().to_str().unwrap(),
            "Bearer tok123"
        );
        assert_eq!(md.get("x-tenant-id").unwrap().to_str().unwrap(), "tenant-1");
    }
}
