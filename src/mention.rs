//! Mention token helpers (`[[@DisplayName:userId]]`).

use regex::Regex;
use std::sync::OnceLock;

fn mention_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\[\[@([^:\]]+):(\d+)\]\]").expect("mention regex"))
}

/// Format a wire mention token.
pub fn format_mention(display_name: &str, user_id: i64) -> String {
    format!("[[@{display_name}:{user_id}]]")
}

/// Extract unique mentioned user ids from content (first-seen order).
pub fn extract_mentioned_user_ids(content: &str) -> Vec<i64> {
    let mut seen = std::collections::HashSet::new();
    let mut ids = Vec::new();
    for caps in mention_re().captures_iter(content) {
        if let Ok(user_id) = caps[2].parse::<i64>() {
            if seen.insert(user_id) {
                ids.push(user_id);
            }
        }
    }
    ids
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formats_and_extracts() {
        let text = format!(
            "hi {} and {}",
            format_mention("Alice", 1),
            format_mention("Bob", 2)
        );
        assert_eq!(extract_mentioned_user_ids(&text), vec![1, 2]);
        assert_eq!(
            extract_mentioned_user_ids(&format!(
                "{} {}",
                format_mention("A", 1),
                format_mention("A", 1)
            )),
            vec![1]
        );
    }
}
