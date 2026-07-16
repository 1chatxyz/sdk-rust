//! Outbound text chunking (server max 4096; we use 4000).

/// Soft limit matching the TypeScript / Python references.
pub const TEXT_CHUNK_LIMIT: usize = 4000;

/// Split reply text into chunks of at most [`TEXT_CHUNK_LIMIT`] characters.
///
/// Empty / whitespace-only input yields an empty vec.
pub fn chunk_text(text: &str) -> Vec<String> {
    let trimmed = text.trim();
    if trimmed.is_empty() {
        return Vec::new();
    }
    if trimmed.len() <= TEXT_CHUNK_LIMIT {
        return vec![trimmed.to_string()];
    }

    let mut chunks = Vec::new();
    let mut rest = trimmed;
    while !rest.is_empty() {
        if rest.len() <= TEXT_CHUNK_LIMIT {
            chunks.push(rest.to_string());
            break;
        }
        // Prefer splitting on a char boundary near the limit.
        let mut end = TEXT_CHUNK_LIMIT;
        while end > 0 && !rest.is_char_boundary(end) {
            end -= 1;
        }
        if end == 0 {
            end = rest.chars().next().map(|c| c.len_utf8()).unwrap_or(1);
        }
        chunks.push(rest[..end].to_string());
        rest = &rest[end..];
    }
    chunks
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_yields_nothing() {
        assert!(chunk_text("   ").is_empty());
    }

    #[test]
    fn splits_at_limit() {
        let text = "a".repeat(TEXT_CHUNK_LIMIT + 10);
        let chunks = chunk_text(&text);
        assert_eq!(chunks.len(), 2);
        assert_eq!(chunks[0].len(), TEXT_CHUNK_LIMIT);
        assert_eq!(chunks[1].len(), 10);
    }
}
