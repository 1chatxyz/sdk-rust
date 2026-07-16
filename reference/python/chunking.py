MYCONVERSATION_TEXT_CHUNK_LIMIT = 4000


def chunk_chat_group_reply_text(text: str) -> list[str]:
    trimmed = text.strip()
    if not trimmed:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(trimmed):
        chunks.append(trimmed[start : start + MYCONVERSATION_TEXT_CHUNK_LIMIT])
        start += MYCONVERSATION_TEXT_CHUNK_LIMIT
    return chunks
