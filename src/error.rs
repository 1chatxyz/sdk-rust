//! Error types for the 1Chat SDK.

use thiserror::Error;

/// Result alias for SDK operations.
pub type Result<T> = std::result::Result<T, Error>;

/// Errors returned by the SDK.
#[derive(Debug, Error)]
pub enum Error {
    /// Invalid or incomplete configuration.
    #[error("config error: {0}")]
    Config(String),

    /// Transport or URL construction failure.
    #[error("transport error: {0}")]
    Transport(String),

    /// gRPC status from the server.
    #[error(transparent)]
    Status(#[from] tonic::Status),
}
