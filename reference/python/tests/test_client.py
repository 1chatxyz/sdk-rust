from myconversation.client import MyConversationClient
from myconversation.config import MyConversationConfig


def test_client_selects_grpc_web_for_https():
    cfg = MyConversationConfig(
        endpoint="https://gateway01.example.com",
        tenant_id="t1",
        token="tok",
    )
    client = MyConversationClient(cfg)
    assert client.uses_grpc_web is True


def test_client_selects_native_grpc_for_http():
    cfg = MyConversationConfig(
        endpoint="http://myconversation.svc:8080",
        tenant_id="t1",
        token="tok",
    )
    client = MyConversationClient(cfg)
    assert client.uses_grpc_web is False
