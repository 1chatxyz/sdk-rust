from myconversation.config import GroupConfig, MyConversationConfig
from myconversation.mention import (
    detect_inbound_control_command,
    extract_command_body,
    extract_mentioned_user_ids,
    format_mention,
    looks_like_slash_command,
    resolve_mention_gate,
    should_accept_group_message,
    strip_mention_tokens_for_command_detection,
)

CFG = MyConversationConfig(
    endpoint="https://gw.example.com",
    tenant_id="t1",
    token="tok",
    user_id="100",
    username="Hermes",
    active_groups_policy="allowlist",
    groups={"4": GroupConfig(require_mention=True)},
)


def test_format_and_extract_mention():
    token = format_mention("Alice", 42)
    assert token == "[[@Alice:42]]"
    assert extract_mentioned_user_ids(f"hi {token}") == [42]


def test_should_accept_group_message_drops_self():
    assert should_accept_group_message(CFG, group_id=4, sender_user_id=100) is False
    assert should_accept_group_message(CFG, group_id=4, sender_user_id=42) is True
    assert should_accept_group_message(CFG, group_id=99, sender_user_id=42) is False


def test_resolve_mention_gate_missing_mention():
    result = resolve_mention_gate(
        cfg=CFG,
        group_id=4,
        raw_body="hello everyone",
        mentioned_user_ids=[],
    )
    assert result.should_skip is True
    assert result.reason == "missing-mention"


def test_resolve_mention_gate_by_user_id():
    result = resolve_mention_gate(
        cfg=CFG,
        group_id=4,
        raw_body="[[@Hermes:100]] check this",
        mentioned_user_ids=[100],
    )
    assert result.should_skip is False
    assert result.effective_was_mentioned is True


def test_strip_mention_tokens_for_command_detection():
    raw = "[[@Hermes:100]] /sethome"
    assert strip_mention_tokens_for_command_detection(raw) == "/sethome"


def test_looks_like_slash_command():
    assert looks_like_slash_command("/sethome") is True
    assert looks_like_slash_command("@Bot Hermes /sethome") is False
    assert looks_like_slash_command("hello") is False


def test_detect_inbound_control_command_with_mention_token():
    assert detect_inbound_control_command("[[@Hermes:100]] /sethome", "Hermes") is True


def test_detect_inbound_control_command_with_username_prefix():
    assert detect_inbound_control_command("@Bot Hermes /sethome", "Bot Hermes") is True


def test_detect_inbound_control_command_plain_chat():
    assert detect_inbound_control_command("hello everyone", "Hermes") is False


def test_extract_command_body_normalizes_mention_prefix():
    assert extract_command_body("@Bot Hermes /sethome", "Bot Hermes") == "/sethome"
    assert extract_command_body("[[@Hermes:100]] /help", "Hermes") == "/help"


def test_resolve_mention_gate_authorized_command_without_mention():
    result = resolve_mention_gate(
        cfg=CFG,
        group_id=4,
        raw_body="/sethome",
        mentioned_user_ids=[],
        has_control_command=True,
    )
    assert result.should_skip is False
    assert result.reason == "authorized-command"
