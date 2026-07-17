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
    Status(Box<tonic::Status>),

    /// Listen session failed after advancing the resume cursor.
    ///
    /// Persist [`Self::Listen::resume_after_message_id`] before retrying so
    /// Durable Object alarms do not redeliver already-handled messages.
    #[error("listen error after resume {resume_after_message_id}: {source}")]
    Listen {
        /// Last successfully handled message id (safe to persist).
        resume_after_message_id: i64,
        /// Underlying failure (handler error or stream open failure).
        #[source]
        source: Box<Error>,
    },
}

impl From<tonic::Status> for Error {
    fn from(status: tonic::Status) -> Self {
        Self::Status(Box::new(status))
    }
}
