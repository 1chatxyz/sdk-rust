from __future__ import annotations

import asyncio
import inspect
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import suppress
from typing import Any

from .config import MyConversationConfig
from .mention import should_accept_group_message

DEFAULT_STREAM_IDLE_TIMEOUT_MS = 90_000
DEFAULT_STREAM_MAX_AGE_MS = 25 * 60 * 1000
DEFAULT_MIN_RECONNECT_DELAY_MS = 2_000
DEFAULT_MAX_RECONNECT_DELAY_MS = 60_000


def compute_reconnect_delay_ms(attempt: int, min_delay_ms: int, max_delay_ms: int) -> int:
    exponent = max(0, attempt)
    return min(max_delay_ms, min_delay_ms * (2**exponent))


class ChatGroupStreamController:
    def __init__(
        self,
        client: Any,
        config: MyConversationConfig,
        on_message: Callable[[dict[str, Any]], Awaitable[None] | None] | None,
        logger: Any | None = None,
        *,
        min_reconnect_delay_ms: int = DEFAULT_MIN_RECONNECT_DELAY_MS,
        max_reconnect_delay_ms: int = DEFAULT_MAX_RECONNECT_DELAY_MS,
        stream_idle_timeout_ms: int = DEFAULT_STREAM_IDLE_TIMEOUT_MS,
        stream_max_age_ms: int = DEFAULT_STREAM_MAX_AGE_MS,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        now_ms: Callable[[], int] | None = None,
    ) -> None:
        self._client = client
        self._config = config
        self._on_message = on_message
        self._logger = logger
        self._min_reconnect_delay_ms = min_reconnect_delay_ms
        self._max_reconnect_delay_ms = max_reconnect_delay_ms
        self._stream_idle_timeout_ms = stream_idle_timeout_ms
        self._stream_max_age_ms = stream_max_age_ms
        self._sleep = sleep
        self._now_ms = now_ms or (lambda: int(asyncio.get_running_loop().time() * 1000))

        self.resume_after_message_id = 0
        self._reconnect_attempt = 0
        self._running = False
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is not None and not self._task.done():
            return

        self._running = True
        self._task = asyncio.create_task(self.run_stream_loop())

    async def stop(self) -> None:
        self._running = False
        task = self._task
        if task is None:
            return

        task.cancel()
        if asyncio.current_task() is task:
            return

        with suppress(asyncio.CancelledError):
            await task
        self._task = None

    async def run_stream_loop(self) -> None:
        self._running = True
        try:
            while self._running:
                stream_started_at_ms = self._now_ms()
                last_event_at_ms = stream_started_at_ms
                self._log(
                    "info",
                    "myconversation: opening StreamChatGroups",
                    resume_after_message_id=self.resume_after_message_id,
                    reconnect_attempt=self._reconnect_attempt,
                )

                try:
                    stream = self._client.stream_chat_groups(
                        resume_after_message_id=self.resume_after_message_id
                    )
                    iterator = aiter(stream)

                    while self._running:
                        try:
                            message = await self._wait_for_next_message(
                                iterator,
                                stream_started_at_ms=stream_started_at_ms,
                                last_event_at_ms=last_event_at_ms,
                            )
                        except StopAsyncIteration:
                            self._log("info", "myconversation: stream ended")
                            break
                        except asyncio.TimeoutError:
                            self._log_timeout(
                                stream_started_at_ms=stream_started_at_ms,
                                last_event_at_ms=last_event_at_ms,
                            )
                            break

                        last_event_at_ms = self._now_ms()
                        self._reconnect_attempt = 0
                        await self._handle_message(message)
                except asyncio.CancelledError:
                    raise
                except Exception as error:
                    if not self._running:
                        break
                    self._log(
                        "warn",
                        "myconversation: stream error",
                        error=str(error),
                        reconnect_attempt=self._reconnect_attempt,
                    )

                if not self._running:
                    break

                delay_ms = compute_reconnect_delay_ms(
                    self._reconnect_attempt,
                    self._min_reconnect_delay_ms,
                    self._max_reconnect_delay_ms,
                )
                self._reconnect_attempt += 1
                self._log(
                    "warn",
                    "myconversation: scheduling stream reconnect",
                    delay_ms=delay_ms,
                    attempt=self._reconnect_attempt,
                    resume_after_message_id=self.resume_after_message_id,
                )
                await self._sleep(delay_ms / 1000)
        finally:
            if asyncio.current_task() is self._task:
                self._task = None

    async def _wait_for_next_message(
        self,
        iterator: AsyncIterator[dict[str, Any]],
        *,
        stream_started_at_ms: int,
        last_event_at_ms: int,
    ) -> dict[str, Any]:
        now_ms = self._now_ms()
        idle_remaining_ms = self._stream_idle_timeout_ms - (now_ms - last_event_at_ms)
        age_remaining_ms = self._stream_max_age_ms - (now_ms - stream_started_at_ms)
        timeout_ms = min(idle_remaining_ms, age_remaining_ms)
        if timeout_ms <= 0:
            raise asyncio.TimeoutError
        return await asyncio.wait_for(iterator.__anext__(), timeout=timeout_ms / 1000)

    def _log_timeout(self, *, stream_started_at_ms: int, last_event_at_ms: int) -> None:
        now_ms = self._now_ms()
        idle_ms = now_ms - last_event_at_ms
        age_ms = now_ms - stream_started_at_ms
        if idle_ms >= self._stream_idle_timeout_ms:
            self._log(
                "warn",
                "myconversation: stream idle timeout, reconnecting",
                idle_ms=idle_ms,
                resume_after_message_id=self.resume_after_message_id,
            )
            return

        self._log(
            "info",
            "myconversation: stream max age reached, reconnecting",
            age_ms=age_ms,
            resume_after_message_id=self.resume_after_message_id,
        )

    async def _handle_message(self, message: dict[str, Any]) -> None:
        message_id = int(message.get("id", 0) or 0)
        if message_id > self.resume_after_message_id:
            self.resume_after_message_id = message_id

        group_id = int(message.get("group_id", 0) or 0)
        sender_user_id = int(message.get("sender_user_id", 0) or 0)
        if not should_accept_group_message(
            self._config,
            group_id=group_id,
            sender_user_id=sender_user_id,
        ):
            self._log(
                "debug",
                "myconversation: skipped inbound chat group message",
                group_id=group_id,
                sender_user_id=sender_user_id,
            )
            return

        if self._on_message is None:
            return

        result = self._on_message(message)
        if inspect.isawaitable(result):
            await result

    def _log(self, level: str, message: str, **meta: Any) -> None:
        if self._logger is None:
            return

        logger_method = getattr(self._logger, level, None)
        if logger_method is None and level == "warn":
            logger_method = getattr(self._logger, "warning", None)
        if logger_method is None:
            return

        if meta:
            logger_method(f"{message} | {meta}")
            return

        logger_method(message)
