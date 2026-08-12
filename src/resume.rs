//! Stream resume cursors for group/DM listen loops.

/// Cursor pair for reconnecting [`crate::Client::run_group_session`] /
/// [`crate::Client::subscribe_groups`] (and DM twins).
///
/// Message id advances on chat messages; event id advances on replayable
/// non-message stream mutations (guest presence, pins, member/meta/topic).
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
#[non_exhaustive]
pub struct StreamResume {
    /// Last consumed message id (`resume_after_message_id`).
    pub after_message_id: i64,
    /// Last consumed stream event log id (`resume_after_event_id`).
    pub after_event_id: i64,
}

impl StreamResume {
    /// Empty cursor (start live).
    pub fn new() -> Self {
        Self::default()
    }

    /// Message-only resume (event id `0`).
    pub fn after_message(after_message_id: i64) -> Self {
        Self {
            after_message_id,
            after_event_id: 0,
        }
    }

    pub(crate) fn bump_message(&mut self, message_id: i64) {
        if message_id > self.after_message_id {
            self.after_message_id = message_id;
        }
    }

    pub(crate) fn bump_event(&mut self, event_id: i64) {
        if event_id > self.after_event_id {
            self.after_event_id = event_id;
        }
    }
}

impl From<i64> for StreamResume {
    fn from(after_message_id: i64) -> Self {
        Self::after_message(after_message_id)
    }
}
