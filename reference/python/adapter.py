from __future__ import annotations

import inspect
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .chunking import chunk_chat_group_reply_text
from .client import MyConversationClient
from .config import MyConversationConfig, load_config_from_extra
from .mention import (
    detect_inbound_control_command,
    extract_command_body,
    extract_mentioned_user_ids,
    resolve_mention_gate,
)
from .stream import ChatGroupStreamController

_logger = logging.getLogger(__name__)

try:
    from gateway.config import Platform
    from gateway.platforms.base import (
        BasePlatformAdapter,
        MessageEvent,
        MessageType,
        SendResult,
    )
except ImportError:
    class Platform:
        def __init__(self, value: str):
            self.value = value

    class MessageType(str, Enum):
        TEXT = "text"

    @dataclass
    class SessionSource:
        platform: Platform
        chat_id: str
        chat_name: str | None = None
        chat_type: str = "dm"
        user_id: str | None = None
        user_name: str | None = None
        thread_id: str | None = None
        chat_topic: str | None = None
        user_id_alt: str | None = None
        chat_id_alt: str | None = None
        is_bot: bool = False

    @dataclass
    class MessageEvent:
        text: str
        message_type: MessageType = MessageType.TEXT
        source: SessionSource | None = None
        raw_message: Any = None
        message_id: str | None = None

    @dataclass
    class SendResult:
        success: bool
        message_id: str | None = None
        error: str | None = None
        raw_response: Any = None
        retryable: bool = False

    class BasePlatformAdapter:
        def __init__(self, config: Any, platform: Platform):
            self.config = config
            self.platform = platform
            self._message_handler = None
            self._running = False
            self._fatal_error_code: str | None = None
            self._fatal_error_message: str | None = None
            self._fatal_error_retryable = True

        def _mark_connected(self) -> None:
            self._running = True

        def _mark_disconnected(self) -> None:
            self._running = False

        def _set_fatal_error(self, code: str, message: str, *, retryable: bool) -> None:
            self._running = False
            self._fatal_error_code = code
            self._fatal_error_message = message
            self._fatal_error_retryable = retryable

        def set_message_handler(self, handler: Any) -> None:
            self._message_handler = handler

        async def handle_message(self, event: MessageEvent) -> None:
            if self._message_handler is None:
                return
            result = self._message_handler(event)
            if inspect.isawaitable(result):
                await result

        def build_source(
            self,
            chat_id: str,
            chat_name: str | None = None,
            chat_type: str = "dm",
            user_id: str | None = None,
            user_name: str | None = None,
            thread_id: str | None = None,
            chat_topic: str | None = None,
            user_id_alt: str | None = None,
            chat_id_alt: str | None = None,
            is_bot: bool = False,
        ) -> SessionSource:
            return SessionSource(
                platform=self.platform,
                chat_id=str(chat_id),
                chat_name=chat_name,
                chat_type=chat_type,
                user_id=str(user_id) if user_id is not None else None,
                user_name=user_name,
                thread_id=str(thread_id) if thread_id is not None else None,
                chat_topic=chat_topic,
                user_id_alt=user_id_alt,
                chat_id_alt=chat_id_alt,
                is_bot=is_bot,
            )


class MyConversationAdapter(BasePlatformAdapter):
    def __init__(self, config: Any, **kwargs: Any):
        super().__init__(config=config, platform=Platform("myconversation"))
        self._runtime_config: MyConversationConfig | None = None
        self._client: MyConversationClient | None = None
        self._stream_controller: ChatGroupStreamController | None = None

    @property
    def name(self) -> str:
        return "MyConversation"

    def _load_runtime_config(self) -> MyConversationConfig:
        extra = getattr(self.config, "extra", None)
        if extra is None and isinstance(self.config, dict):
            extra = self.config
        return load_config_from_extra(extra)

    def _ensure_runtime_config(self) -> MyConversationConfig:
        if self._runtime_config is None:
            self._runtime_config = self._load_runtime_config()
        return self._runtime_config

    async def connect(self, *, is_reconnect: bool = False) -> bool:
        del is_reconnect
        try:
            cfg = self._load_runtime_config()
            self._runtime_config = cfg
            self._client = MyConversationClient(cfg)
            self._stream_controller = ChatGroupStreamController(
                self._client,
                cfg,
                on_message=self._handle_inbound,
            )
            self._stream_controller.start()
            self._mark_connected()
            return True
        except Exception as error:
            self._set_fatal_error(
                "connect_failed",
                f"myconversation: failed to connect: {error}",
                retryable=False,
            )
            return False

    async def disconnect(self) -> None:
        stream_controller = self._stream_controller
        self._stream_controller = None
        if stream_controller is not None:
            await stream_controller.stop()

        client = self._client
        self._client = None

        if client is not None:
            await client.close()

        self._mark_disconnected()

    async def _handle_inbound(self, message: dict[str, Any]) -> None:
        cfg = self._ensure_runtime_config()
        group_id = int(message.get("group_id", 0) or 0)
        raw_body = str(message.get("content", "") or "")
        mentioned_user_ids = [int(user_id) for user_id in message.get("mentioned_user_ids", [])]
        has_control_command = detect_inbound_control_command(raw_body, cfg.username)

        gate = resolve_mention_gate(
            cfg,
            group_id=group_id,
            raw_body=raw_body,
            mentioned_user_ids=mentioned_user_ids,
            has_control_command=has_control_command,
        )
        if gate.should_skip:
            return

        sender_user_id = int(message.get("sender_user_id", 0) or 0)
        sender_username = str(message.get("sender_username", "") or "")
        event_text = raw_body
        if has_control_command:
            command_body = extract_command_body(raw_body, cfg.username)
            if command_body:
                event_text = command_body
        raw_message = dict(message)
        raw_message["raw_content"] = raw_body
        event = MessageEvent(
            text=event_text,
            message_type=MessageType.TEXT,
            source=self.build_source(
                chat_id=str(group_id),
                chat_name=str(group_id),
                chat_type="group",
                user_id=str(sender_user_id) if sender_user_id else None,
                user_name=sender_username or None,
            ),
            raw_message=raw_message,
            message_id=self._coerce_message_id(message),
        )

        result = self.handle_message(event)
        if inspect.isawaitable(result):
            await result

    async def send(
        self,
        chat_id: str,
        content: str,
        reply_to: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SendResult:
        del reply_to, metadata
        if self._client is None:
            return SendResult(success=False, error="Not connected")

        chunks = chunk_chat_group_reply_text(content)
        if not chunks:
            return SendResult(success=False, error="Empty message")

        last_response: Any = None
        last_message_id: str | None = None
        try:
            for index, chunk in enumerate(chunks):
                mentioned_user_ids = extract_mentioned_user_ids(chunk) if index == 0 else []
                last_response = await self._client.send_chat_group_message(
                    group_id=chat_id,
                    content=chunk,
                    mentioned_user_ids=mentioned_user_ids,
                )
                message_id = self._coerce_message_id(last_response)
                if message_id is not None:
                    last_message_id = message_id
            return SendResult(
                success=True,
                message_id=last_message_id,
                raw_response=last_response,
            )
        except Exception as error:
            return SendResult(success=False, error=str(error), retryable=True)

    async def _signal_typing_best_effort(self, chat_id: str, typing: bool) -> None:
        if self._client is None:
            return
        try:
            await self._client.signal_chat_group_typing(chat_id, typing)
        except Exception as error:
            _logger.warning(
                "myconversation: SignalChatGroupTyping failed group_id=%s typing=%s error=%s",
                chat_id,
                typing,
                error,
            )

    async def send_typing(self, chat_id: str, metadata: dict[str, Any] | None = None) -> None:
        del metadata
        await self._signal_typing_best_effort(str(chat_id), True)

    async def stop_typing(self, chat_id: str) -> None:
        await self._signal_typing_best_effort(str(chat_id), False)

    async def get_chat_info(self, chat_id: str) -> dict[str, Any]:
        chat_key = str(chat_id)
        return {
            "chat_id": chat_key,
            "name": chat_key,
            "type": "group",
        }

    @staticmethod
    def _coerce_message_id(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, dict):
            for key in ("message_id", "id"):
                raw = value.get(key)
                if raw not in (None, "", 0):
                    return str(raw)
            nested = value.get("message")
            if nested is not None:
                return MyConversationAdapter._coerce_message_id(nested)
            return None

        for attr in ("message_id", "id"):
            raw = getattr(value, attr, None)
            if raw not in (None, "", 0):
                return str(raw)

        nested = getattr(value, "message", None)
        if nested is not None:
            return MyConversationAdapter._coerce_message_id(nested)
        return None


def register(ctx):
    ctx.register_platform(
        name="myconversation",
        label="MyConversation",
        adapter_factory=lambda cfg: MyConversationAdapter(cfg),
        check_fn=lambda: True,
        required_env=[
            "MYCONVERSATION_GATEWAY_ENDPOINT",
            "MYCONVERSATION_TENANT_ID",
            "MYCONVERSATION_TOKEN",
        ],
        allow_all_env="MYCONVERSATION_ALLOW_ALL_USERS",
        allowed_users_env="MYCONVERSATION_ALLOWED_USERS",
        max_message_length=4000,
        platform_hint="You are in myconversation Staff Group Chat. Mentions use [[@DisplayName:userId]].",
        emoji="💬",
    )
