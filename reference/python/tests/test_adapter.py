import types

from myconversation.adapter import MyConversationAdapter, register


def make_platform_config(extra=None):
    return types.SimpleNamespace(extra=extra or {})


class RecordingClient:
    def __init__(self):
        self.calls = []
        self.typing_calls = []

    async def signal_chat_group_typing(self, group_id, typing):
        self.typing_calls.append({"group_id": group_id, "typing": typing})

    async def send_chat_group_message(self, group_id, content, mentioned_user_ids=None):
        self.calls.append(
            {
                "group_id": group_id,
                "content": content,
                "mentioned_user_ids": list(mentioned_user_ids or []),
            }
        )
        return {"message_id": f"msg-{len(self.calls)}"}


async def test_send_chunks_long_text_and_only_mentions_first_chunk():
    adapter = MyConversationAdapter(make_platform_config())
    adapter._client = RecordingClient()

    first_chunk = "[[@Hermes:100]] " + ("a" * 3990)
    content = first_chunk + ("b" * 50)

    result = await adapter.send(chat_id="42", content=content)

    assert result.success is True
    assert len(adapter._client.calls) == 2
    assert adapter._client.calls[0]["mentioned_user_ids"] == [100]
    assert adapter._client.calls[1]["mentioned_user_ids"] == []


async def test_handle_inbound_skips_message_without_required_mention():
    adapter = MyConversationAdapter(
        make_platform_config(
            {
                "endpoint": "https://gw.example.com",
                "tenant_id": "tenant-1",
                "token": "token-1",
                "user_id": "100",
                "username": "Hermes",
                "groups": {"42": {"require_mention": True}},
            }
        )
    )
    adapter._runtime_config = adapter._load_runtime_config()
    seen = []

    async def handler(event):
        seen.append(event)

    adapter._message_handler = handler

    await adapter._handle_inbound(
        {
            "id": 5,
            "group_id": 42,
            "sender_user_id": 200,
            "sender_username": "Alice",
            "content": "hello there",
            "mentioned_user_ids": [],
        }
    )

    assert seen == []


async def test_send_typing_signals_on():
    adapter = MyConversationAdapter(make_platform_config())
    adapter._client = RecordingClient()

    await adapter.send_typing("42")

    assert adapter._client.typing_calls == [{"group_id": "42", "typing": True}]


async def test_stop_typing_signals_off():
    adapter = MyConversationAdapter(make_platform_config())
    adapter._client = RecordingClient()

    await adapter.stop_typing("42")

    assert adapter._client.typing_calls == [{"group_id": "42", "typing": False}]


async def test_send_typing_swallows_client_errors():
    class FailingClient:
        async def signal_chat_group_typing(self, group_id, typing):
            raise RuntimeError("network down")

    adapter = MyConversationAdapter(make_platform_config())
    adapter._client = FailingClient()

    await adapter.send_typing("42")  # must not raise


async def test_stop_typing_swallows_client_errors():
    class FailingClient:
        async def signal_chat_group_typing(self, group_id, typing):
            raise RuntimeError("network down")

    adapter = MyConversationAdapter(make_platform_config())
    adapter._client = FailingClient()

    await adapter.stop_typing("42")  # must not raise


async def test_handle_inbound_normalizes_sethome_after_mention():
    adapter = MyConversationAdapter(
        make_platform_config(
            {
                "endpoint": "https://gw.example.com",
                "tenant_id": "tenant-1",
                "token": "token-1",
                "user_id": "100",
                "username": "Bot Hermes",
                "groups": {"4": {"require_mention": True}},
            }
        )
    )
    adapter._runtime_config = adapter._load_runtime_config()
    seen = []

    async def handler(event):
        seen.append(event)

    adapter._message_handler = handler

    await adapter._handle_inbound(
        {
            "id": 6,
            "group_id": 4,
            "sender_user_id": 200,
            "sender_username": "nemo",
            "content": "@Bot Hermes /sethome",
            "mentioned_user_ids": [100],
        }
    )

    assert len(seen) == 1
    assert seen[0].text == "/sethome"
    assert seen[0].raw_message["raw_content"] == "@Bot Hermes /sethome"


async def test_handle_inbound_allows_sethome_without_mention():
    adapter = MyConversationAdapter(
        make_platform_config(
            {
                "endpoint": "https://gw.example.com",
                "tenant_id": "tenant-1",
                "token": "token-1",
                "user_id": "100",
                "username": "Bot Hermes",
                "groups": {"4": {"require_mention": True}},
            }
        )
    )
    adapter._runtime_config = adapter._load_runtime_config()
    seen = []

    async def handler(event):
        seen.append(event)

    adapter._message_handler = handler

    await adapter._handle_inbound(
        {
            "id": 7,
            "group_id": 4,
            "sender_user_id": 200,
            "sender_username": "nemo",
            "content": "/sethome",
            "mentioned_user_ids": [],
        }
    )

    assert len(seen) == 1
    assert seen[0].text == "/sethome"


def test_register_exposes_myconversation_platform():
    registrations = []

    class Ctx:
        def register_platform(self, **kwargs):
            registrations.append(kwargs)

    register(Ctx())

    assert len(registrations) == 1
    registration = registrations[0]
    assert registration["name"] == "myconversation"
    assert registration["label"] == "MyConversation"
    assert registration["required_env"] == [
        "MYCONVERSATION_GATEWAY_ENDPOINT",
        "MYCONVERSATION_TENANT_ID",
        "MYCONVERSATION_TOKEN",
    ]
    assert isinstance(registration["adapter_factory"](make_platform_config()), MyConversationAdapter)
