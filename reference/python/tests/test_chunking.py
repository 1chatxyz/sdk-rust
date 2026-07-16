from myconversation.chunking import MYCONVERSATION_TEXT_CHUNK_LIMIT, chunk_chat_group_reply_text


def test_chunk_empty():
    assert chunk_chat_group_reply_text("   ") == []


def test_short_text_single_chunk():
    assert chunk_chat_group_reply_text("hello") == ["hello"]


def test_long_text_splits_at_limit():
    text = "a" * (MYCONVERSATION_TEXT_CHUNK_LIMIT + 100)
    chunks = chunk_chat_group_reply_text(text)
    assert len(chunks) == 2
    assert len(chunks[0]) == MYCONVERSATION_TEXT_CHUNK_LIMIT
    assert len(chunks[1]) == 100
