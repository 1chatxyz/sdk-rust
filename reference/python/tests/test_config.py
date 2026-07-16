import pytest
from myconversation.config import (
    GroupConfig,
    MyConversationConfig,
    load_config_from_extra,
    should_accept_group,
    should_require_mention,
)


def test_should_accept_group_allowlist():
    cfg = MyConversationConfig(
        endpoint="https://gw.example.com",
        tenant_id="t1",
        token="tok",
        user_id="100",
        username="Hermes",
        active_groups_policy="allowlist",
        groups={"4": GroupConfig(require_mention=True)},
    )
    assert should_accept_group(cfg, 4) is True
    assert should_accept_group(cfg, 99) is False


def test_should_require_mention_defaults_true():
    cfg = MyConversationConfig(
        endpoint="https://gw.example.com",
        tenant_id="t1",
        token="tok",
        user_id="100",
        username="Hermes",
        active_groups_policy="allowlist",
        groups={"4": GroupConfig()},
    )
    assert should_require_mention(cfg, 4) is True


def test_load_config_from_extra_env_override(monkeypatch):
    monkeypatch.setenv("MYCONVERSATION_GATEWAY_ENDPOINT", "https://gw.prod")
    monkeypatch.setenv("MYCONVERSATION_TENANT_ID", "tenant-x")
    monkeypatch.setenv("MYCONVERSATION_TOKEN", "secret")
    monkeypatch.setenv("MYCONVERSATION_USER_ID", "200")
    monkeypatch.setenv("MYCONVERSATION_USERNAME", "Hermes")
    cfg = load_config_from_extra({"groups": {"4": {"require_mention": True}}})
    assert cfg.endpoint == "https://gw.prod"
    assert cfg.user_id == "200"
