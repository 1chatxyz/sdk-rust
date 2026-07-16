import asyncio

from myconversation.config import GroupConfig, MyConversationConfig
from myconversation.stream import ChatGroupStreamController, compute_reconnect_delay_ms


def make_config() -> MyConversationConfig:
    return MyConversationConfig(
        endpoint="https://gw.example.com",
        tenant_id="t1",
        token="tok",
        user_id="100",
        username="Hermes",
        active_groups_policy="allowlist",
        groups={"4": GroupConfig(require_mention=True)},
    )


def test_reconnect_delay_exponential_cap():
    assert compute_reconnect_delay_ms(0, 2000, 60000) == 2000
    assert compute_reconnect_delay_ms(1, 2000, 60000) == 4000
    assert compute_reconnect_delay_ms(10, 2000, 60000) == 60000


class BlockingClient:
    def __init__(self) -> None:
        self.calls: list[int] = []
        self.started = asyncio.Event()
        self.cancelled = asyncio.Event()

    async def stream_chat_groups(self, resume_after_message_id: int = 0):
        self.calls.append(resume_after_message_id)
        self.started.set()
        try:
            await asyncio.Event().wait()
            if False:  # pragma: no cover
                yield {}
        finally:
            self.cancelled.set()


async def test_controller_start_stop_cancels_active_stream():
    client = BlockingClient()
    controller = ChatGroupStreamController(client, make_config(), lambda _: None)

    controller.start()
    await asyncio.wait_for(client.started.wait(), timeout=1)
    await controller.stop()

    assert client.calls == [0]
    assert client.cancelled.is_set()


class ScriptedReconnectClient:
    def __init__(self) -> None:
        self.calls: list[int] = []
        self.second_stream_cancelled = asyncio.Event()

    async def stream_chat_groups(self, resume_after_message_id: int = 0):
        call_index = len(self.calls)
        self.calls.append(resume_after_message_id)

        if call_index == 0:
            yield {
                "id": 1,
                "group_id": 4,
                "sender_user_id": 100,
                "content": "self message",
                "mentioned_user_ids": [],
            }
            raise RuntimeError("stream broke")

        if call_index == 1:
            yield {
                "id": 2,
                "group_id": 4,
                "sender_user_id": 42,
                "content": "hello",
                "mentioned_user_ids": [],
            }
            try:
                await asyncio.Event().wait()
                if False:  # pragma: no cover
                    yield {}
            finally:
                self.second_stream_cancelled.set()
            return

        raise AssertionError("unexpected reconnect")


async def test_run_stream_loop_reconnects_with_resume_id_and_filters_messages():
    client = ScriptedReconnectClient()
    accepted_messages: list[dict] = []
    accepted = asyncio.Event()

    async def on_message(message: dict) -> None:
        accepted_messages.append(message)
        accepted.set()

    controller = ChatGroupStreamController(
        client,
        make_config(),
        on_message,
        min_reconnect_delay_ms=0,
        max_reconnect_delay_ms=0,
    )

    controller.start()
    await asyncio.wait_for(accepted.wait(), timeout=1)
    await controller.stop()

    assert client.calls[:2] == [0, 1]
    assert [message["id"] for message in accepted_messages] == [2]
    assert controller.resume_after_message_id == 2
    assert client.second_stream_cancelled.is_set()


class IdleReconnectClient:
    def __init__(self) -> None:
        self.calls: list[int] = []
        self.second_started = asyncio.Event()
        self.second_cancelled = asyncio.Event()

    async def stream_chat_groups(self, resume_after_message_id: int = 0):
        call_index = len(self.calls)
        self.calls.append(resume_after_message_id)

        if call_index == 1:
            self.second_started.set()

        try:
            await asyncio.Event().wait()
            if False:  # pragma: no cover
                yield {}
        finally:
            if call_index == 1:
                self.second_cancelled.set()


async def test_run_stream_loop_reconnects_after_idle_timeout():
    client = IdleReconnectClient()
    controller = ChatGroupStreamController(
        client,
        make_config(),
        lambda _: None,
        min_reconnect_delay_ms=0,
        max_reconnect_delay_ms=0,
        stream_idle_timeout_ms=10,
    )

    controller.start()
    await asyncio.wait_for(client.second_started.wait(), timeout=1)
    await controller.stop()

    assert client.calls[:2] == [0, 0]
    assert client.second_cancelled.is_set()
