from __future__ import annotations

import re
from dataclasses import dataclass

from .config import MyConversationConfig, should_accept_group, should_require_mention, user_id_matches

MENTION_TOKEN_RE = re.compile(r"\[\[@([^:\]]+):(\d+)\]\]")


def strip_mention_tokens_for_command_detection(content: str) -> str:
    collapsed = MENTION_TOKEN_RE.sub(" ", content)
    return " ".join(collapsed.split()).strip()


def strip_leading_bot_username(content: str, username: str | None) -> str:
    text = content.strip()
    if not text or not username:
        return text
    uname = username.strip().lstrip("@")
    lowered = text.lower()
    for prefix in (f"@{uname}", uname):
        if lowered.startswith(prefix.lower()):
            return text[len(prefix) :].strip()
    return text


def looks_like_slash_command(body: str) -> bool:
    trimmed = body.strip()
    if not trimmed.startswith("/"):
        return False
    parts = trimmed.split(maxsplit=1)
    raw = parts[0][1:].lower() if parts else ""
    if not raw:
        return False
    if "@" in raw:
        raw = raw.split("@", 1)[0]
    if "/" in raw:
        return False
    return True


def detect_inbound_control_command(raw_body: str, username: str | None = None) -> bool:
    trimmed = raw_body.strip()
    if not trimmed:
        return False
    if looks_like_slash_command(trimmed):
        return True
    without_tokens = strip_mention_tokens_for_command_detection(trimmed)
    if without_tokens and without_tokens != trimmed and looks_like_slash_command(without_tokens):
        return True
    if username:
        without_user = strip_leading_bot_username(without_tokens or trimmed, username)
        if without_user and looks_like_slash_command(without_user):
            return True
    return False


def extract_command_body(raw_body: str, username: str | None = None) -> str | None:
    trimmed = raw_body.strip()
    candidates = [trimmed]
    without_tokens = strip_mention_tokens_for_command_detection(trimmed)
    if without_tokens:
        candidates.append(without_tokens)
    if username:
        candidates.append(strip_leading_bot_username(without_tokens or trimmed, username))
    for candidate in candidates:
        if candidate and looks_like_slash_command(candidate):
            return candidate
    return None


@dataclass
class MentionGateResult:
    should_skip: bool
    reason: str
    effective_was_mentioned: bool


def format_mention(display_name: str, user_id: int | str) -> str:
    return f"[[@{display_name}:{user_id}]]"


def extract_mentioned_user_ids(content: str) -> list[int]:
    seen: set[int] = set()
    ids: list[int] = []
    for match in MENTION_TOKEN_RE.finditer(content):
        user_id = int(match.group(2))
        if user_id not in seen:
            seen.add(user_id)
            ids.append(user_id)
    return ids


def content_contains_username(content: str | None, username: str | None) -> bool:
    if not content or not username:
        return False
    return username in content


def describe_bot_mention(
    cfg: MyConversationConfig,
    mentioned_user_ids: list[int],
    content: str | None,
) -> tuple[bool, str]:
    if cfg.user_id and any(user_id_matches(cfg.user_id, uid) for uid in mentioned_user_ids):
        return True, "mentioned-user-ids"
    if content_contains_username(content, cfg.username):
        return True, "username-in-content"
    return False, "none"


def should_accept_group_message(
    cfg: MyConversationConfig,
    group_id: int,
    sender_user_id: int,
) -> bool:
    if cfg.user_id and user_id_matches(cfg.user_id, sender_user_id):
        return False
    return should_accept_group(cfg, group_id)


def resolve_mention_gate(
    cfg: MyConversationConfig,
    group_id: int,
    raw_body: str,
    mentioned_user_ids: list[int],
    has_control_command: bool = False,
) -> MentionGateResult:
    if not should_require_mention(cfg, group_id):
        was_mentioned, _ = describe_bot_mention(cfg, mentioned_user_ids, raw_body)
        return MentionGateResult(False, "mention-not-required", was_mentioned)

    was_mentioned, match = describe_bot_mention(cfg, mentioned_user_ids, raw_body)
    if was_mentioned:
        return MentionGateResult(False, "mentioned", True)

    if has_control_command:
        return MentionGateResult(False, "authorized-command", True)

    return MentionGateResult(True, "missing-mention", False)
