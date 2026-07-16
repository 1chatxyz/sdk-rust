import type {
  ChatGroupMessageInfo,
  ChatGroupStreamEvent,
  ChatGroupTypingIndicator,
  SendChatGroupMessageReply,
} from "@genjutsu/myconversation-connect/myconversation_pb";

export type {
  ChatGroupMessageInfo,
  ChatGroupStreamEvent,
  ChatGroupTypingIndicator,
  SendChatGroupMessageReply,
};

export function asNumber(value: bigint | number | undefined): number {
  if (value == null) {
    return 0;
  }
  return typeof value === "bigint" ? Number(value) : value;
}

export function asBigInt(value: bigint | number | undefined): bigint {
  if (value == null) {
    return 0n;
  }
  return typeof value === "bigint" ? value : BigInt(value);
}

export function getStreamEventMessage(
  event: ChatGroupStreamEvent,
): ChatGroupMessageInfo | undefined {
  if (event.item?.case !== "message") {
    return undefined;
  }
  return event.item.value;
}

export function getStreamEventTyping(
  event: ChatGroupStreamEvent,
): ChatGroupTypingIndicator | undefined {
  if (event.item?.case !== "typing") {
    return undefined;
  }
  return event.item.value;
}
