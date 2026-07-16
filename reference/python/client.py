from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from urllib.parse import urlparse

import grpc
from connectrpc.protocol import ProtocolType

from .config import MyConversationConfig
from .proto.myconversation_connect import MyConversationClient as ConnectMyConversationClient
from .proto.myconversation_pb2 import (
    SendChatGroupMessageRequest,
    SignalChatGroupTypingRequest,
    StreamChatGroupsRequest,
)
from .proto.myconversation_pb2_grpc import MyConversationStub
from .transport import auth_metadata, normalize_grpc_base_url, should_use_grpc_web_transport


def _grpc_target(base_url: str) -> str:
    parsed = urlparse(base_url)
    if not parsed.hostname:
        raise ValueError(f"myconversation: invalid endpoint {base_url!r}")
    if parsed.port is not None:
        return f"{parsed.hostname}:{parsed.port}"
    if parsed.scheme == "https":
        return f"{parsed.hostname}:443"
    return f"{parsed.hostname}:80"


def _auth_headers(cfg: MyConversationConfig) -> dict[str, str]:
    return {
        "authorization": f"Bearer {cfg.token}",
        "x-tenant-id": cfg.tenant_id,
    }


def _is_unimplemented_error(error: BaseException) -> bool:
    if isinstance(error, grpc.aio.AioRpcError):
        return error.code() == grpc.StatusCode.UNIMPLEMENTED
    message = str(error)
    return "UNIMPLEMENTED" in message or "unimplemented" in message


class MyConversationClient:
    def __init__(self, cfg: MyConversationConfig):
        self.cfg = cfg
        self.base_url = normalize_grpc_base_url(cfg.endpoint)
        self.uses_grpc_web = should_use_grpc_web_transport(self.base_url)
        self._grpc_channel: grpc.aio.Channel | None = None
        self._grpc_stub: MyConversationStub | None = None
        self._grpc_web_client: ConnectMyConversationClient | None = None

    def _get_grpc_stub(self) -> MyConversationStub:
        if self._grpc_stub is not None:
            return self._grpc_stub

        target = _grpc_target(self.base_url)
        self._grpc_channel = grpc.aio.insecure_channel(target)
        self._grpc_stub = MyConversationStub(self._grpc_channel)
        return self._grpc_stub

    def _get_grpc_web_client(self) -> ConnectMyConversationClient:
        if self._grpc_web_client is None:
            self._grpc_web_client = ConnectMyConversationClient(
                self.base_url,
                protocol=ProtocolType.GRPC_WEB,
            )
        return self._grpc_web_client

    @staticmethod
    def _message_to_dict(message: Any) -> dict[str, Any]:
        return {
            "id": int(message.id),
            "group_id": int(message.group_id),
            "sender_user_id": int(message.sender_user_id),
            "sender_username": message.sender_username,
            "content": message.content,
            "mentioned_user_ids": [int(user_id) for user_id in message.mentioned_user_ids],
        }

    async def stream_chat_groups(
        self,
        resume_after_message_id: int = 0,
    ) -> AsyncIterator[dict[str, Any]]:
        request = StreamChatGroupsRequest(
            resume_after_message_id=resume_after_message_id,
        )

        if self.uses_grpc_web:
            stream = self._get_grpc_web_client().stream_chat_groups(
                request,
                headers=_auth_headers(self.cfg),
            )
            async for event in stream:
                if event.WhichOneof("item") != "message":
                    continue
                yield self._message_to_dict(event.message)
            return

        call = self._get_grpc_stub().StreamChatGroups(
            request,
            metadata=auth_metadata(self.cfg.tenant_id, self.cfg.token),
        )
        async for event in call:
            if event.WhichOneof("item") != "message":
                continue
            yield self._message_to_dict(event.message)

    async def send_chat_group_message(
        self,
        group_id: int | str,
        content: str,
        mentioned_user_ids: list[int] | None = None,
    ):
        request = SendChatGroupMessageRequest(
            group_id=int(group_id),
            content=content,
            mentioned_user_ids=[int(user_id) for user_id in (mentioned_user_ids or [])],
        )

        if self.uses_grpc_web:
            return await self._get_grpc_web_client().send_chat_group_message(
                request,
                headers=_auth_headers(self.cfg),
            )

        return await self._get_grpc_stub().SendChatGroupMessage(
            request,
            metadata=auth_metadata(self.cfg.tenant_id, self.cfg.token),
        )

    async def signal_chat_group_typing(self, group_id: int | str, typing: bool):
        request = SignalChatGroupTypingRequest(
            group_id=int(group_id),
            typing=typing,
        )

        try:
            if self.uses_grpc_web:
                await self._get_grpc_web_client().signal_chat_group_typing(
                    request,
                    headers=_auth_headers(self.cfg),
                )
                return

            await self._get_grpc_stub().SignalChatGroupTyping(
                request,
                metadata=auth_metadata(self.cfg.tenant_id, self.cfg.token),
            )
        except Exception as error:
            if _is_unimplemented_error(error):
                return
            raise

    async def close(self) -> None:
        if self._grpc_web_client is not None:
            await self._grpc_web_client.close()
            self._grpc_web_client = None
        if self._grpc_channel is not None:
            await self._grpc_channel.close()
            self._grpc_channel = None
            self._grpc_stub = None
