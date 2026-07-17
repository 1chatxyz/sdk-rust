//! Shared reconnect backoff helpers.

use std::time::Duration;

const MIN_RECONNECT: Duration = Duration::from_secs(2);
const MAX_RECONNECT: Duration = Duration::from_secs(60);

/// Compute exponential reconnect delay (2s … 60s).
pub fn compute_reconnect_delay(attempt: u32) -> Duration {
    let exp = attempt.min(16);
    let ms = MIN_RECONNECT.as_millis() * (1u128 << exp);
    Duration::from_millis(ms.min(MAX_RECONNECT.as_millis()) as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn backoff_bounds() {
        assert_eq!(compute_reconnect_delay(0), Duration::from_secs(2));
        assert_eq!(compute_reconnect_delay(100), Duration::from_secs(60));
    }
}
