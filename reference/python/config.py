from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GroupConfig:
    require_mention: bool = True


@dataclass
class MyConversationConfig:
    endpoint: str
    tenant_id: str
    token: str
    user_id: str | None = None
    username: str | None = None
    active_groups_policy: str = "allowlist"
    groups: dict[str, GroupConfig] = field(default_factory=dict)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is not None and value.strip() != "":
        return value.strip()
    return default


def _parse_groups(raw: dict[str, Any]) -> dict[str, GroupConfig]:
    groups: dict[str, GroupConfig] = {}
    for group_id, group_cfg in raw.items():
        require = True
        if isinstance(group_cfg, dict) and "require_mention" in group_cfg:
            require = bool(group_cfg["require_mention"])
        groups[str(group_id)] = GroupConfig(require_mention=require)
    return groups


def load_config_from_extra(extra: dict[str, Any] | None = None) -> MyConversationConfig:
    extra = extra or {}
    endpoint = _env("MYCONVERSATION_GATEWAY_ENDPOINT") or str(extra.get("endpoint", "")).strip()
    tenant_id = _env("MYCONVERSATION_TENANT_ID") or str(extra.get("tenant_id", "")).strip()
    token = _env("MYCONVERSATION_TOKEN") or str(extra.get("token", "")).strip()
    if not endpoint or not tenant_id or not token:
        raise ValueError("myconversation: endpoint, tenant_id, and token are required")

    user_id = _env("MYCONVERSATION_USER_ID") or extra.get("user_id")
    username = _env("MYCONVERSATION_USERNAME") or extra.get("username")
    policy = str(extra.get("active_groups_policy", "allowlist"))
    groups_raw = extra.get("groups") or {}
    if not isinstance(groups_raw, dict):
        raise ValueError("myconversation: groups must be an object")

    return MyConversationConfig(
        endpoint=endpoint,
        tenant_id=tenant_id,
        token=token,
        user_id=str(user_id).strip() if user_id else None,
        username=str(username).strip().lstrip("@") if username else None,
        active_groups_policy=policy,
        groups=_parse_groups(groups_raw),
    )


def should_accept_group(cfg: MyConversationConfig, group_id: int | str) -> bool:
    if cfg.active_groups_policy == "all":
        return True
    return str(group_id) in cfg.groups


def should_require_mention(cfg: MyConversationConfig, group_id: int | str) -> bool:
    group = cfg.groups.get(str(group_id))
    return group.require_mention if group else True


def user_id_matches(config_user_id: str, candidate: int) -> bool:
    if candidate <= 0:
        return False
    if str(candidate) == config_user_id:
        return True
    try:
        return int(config_user_id) == candidate
    except ValueError:
        return False
