import { randomUUID } from "node:crypto";

import { ConnectError, Code } from "@connectrpc/connect";
import { chunkTextForOutbound } from "openclaw/plugin-sdk/text-chunking";

import { SendChatGroupMessageReply } from "@genjutsu/myconversation-connect/myconversation_pb";

import type { MyConversationConnectClient } from "../connect/client.js";
import type { SendChatGroupMessageReply as SendChatGroupMessageReplyType } from "../connect/types.js";
import { extractMentionedUserIds } from "../mention/format.js";

export const MYCONVERSATION_TEXT_CHUNK_LIMIT = 4000;

export function chunkChatGroupReplyText(text: string): string[] {
  const trimmed = text.trim();
  if (!trimmed) {
    return [];
  }
  return chunkTextForOutbound(trimmed, MYCONVERSATION_TEXT_CHUNK_LIMIT);
}

export type ChatGroupReplyParams = {
  groupId: number;
  text: string;
  images?: string[];
  videos?: string[];
  files?: string[];
  mentionedUserIds?: number[];
};

export type TypingLogger = {
  debug?(message: string, meta?: Record<string, unknown>): void;
  warn?(message: string, meta?: Record<string, unknown>): void;
};

export function isTypingUnsupportedError(error: unknown): boolean {
  if (error instanceof ConnectError) {
    return error.code === Code.Unimplemented;
  }
  const message = error instanceof Error ? error.message : String(error);
  return (
    message.includes("SignalChatGroupTyping") &&
    (message.includes("UNIMPLEMENTED") || message.includes("unimplemented"))
  );
}

/** Refresh cadence while the agent is thinking (myconversation UI typing timeout ~10s). */
const DEFAULT_TYPING_KEEPALIVE_MS = 5000;

export type ChatGroupTypingSession = {
  start: () => Promise<void>;
  stop: () => Promise<void>;
};

/** Typing on at start, keepalive pulses, typing off on stop — independent of OpenClaw typingMode. */
export function createChatGroupTypingSession(
  client: MyConversationConnectClient,
  groupId: number,
  log?: TypingLogger,
  options?: { keepaliveIntervalMs?: number },
): ChatGroupTypingSession {
  const keepaliveIntervalMs =
    options?.keepaliveIntervalMs ?? DEFAULT_TYPING_KEEPALIVE_MS;
  let active = false;
  let timer: ReturnType<typeof setInterval> | undefined;

  const pulseOn = () =>
    signalChatGroupTypingBestEffort(client, groupId, true, log);

  return {
    start: async () => {
      if (active) {
        return;
      }
      active = true;
      await pulseOn();
      if (keepaliveIntervalMs > 0) {
        timer = setInterval(() => {
          void pulseOn();
        }, keepaliveIntervalMs);
        timer.unref?.();
      }
    },
    stop: async () => {
      if (!active) {
        return;
      }
      active = false;
      if (timer) {
        clearInterval(timer);
        timer = undefined;
      }
      await signalChatGroupTypingBestEffort(client, groupId, false, log);
    },
  };
}

export async function signalChatGroupTypingBestEffort(
  client: MyConversationConnectClient,
  groupId: number,
  typing: boolean,
  log?: TypingLogger,
): Promise<void> {
  try {
    await client.signalChatGroupTyping({
      groupId,
      typing,
    });
  } catch (error) {
    if (isTypingUnsupportedError(error)) {
      log?.debug?.(
        "myconversation: SignalChatGroupTyping not available on server; skipping",
        { groupId, typing },
      );
      return;
    }
    log?.warn?.("myconversation: SignalChatGroupTyping failed", {
      groupId,
      typing,
      error: String(error),
    });
  }
}

/** @deprecated Use signalChatGroupTypingBestEffort — typing must not block replies. */
export async function signalChatGroupTyping(
  client: MyConversationConnectClient,
  groupId: number,
  typing: boolean,
): Promise<void> {
  await signalChatGroupTypingBestEffort(client, groupId, typing);
}

export async function sendChatGroupReply(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
): Promise<SendChatGroupMessageReplyType> {
  const parsedMentionIds = extractMentionedUserIds(params.text);
  const mentionedUserIds =
    params.mentionedUserIds != null && params.mentionedUserIds.length > 0
      ? params.mentionedUserIds
      : parsedMentionIds;

  return client.sendChatGroupMessage({
    groupId: params.groupId,
    content: params.text,
    images: params.images ?? [],
    videos: params.videos ?? [],
    files: params.files ?? [],
    mentionedUserIds,
    clientMessageId: randomUUID(),
  });
}

export async function sendChatGroupReplyChunked(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
): Promise<SendChatGroupMessageReplyType> {
  const chunks = chunkChatGroupReplyText(params.text);
  const hasMedia =
    (params.images?.length ?? 0) > 0 ||
    (params.videos?.length ?? 0) > 0 ||
    (params.files?.length ?? 0) > 0;

  if (chunks.length === 0 && !hasMedia) {
    return new SendChatGroupMessageReply({ duplicate: false });
  }

  if (chunks.length === 0 && hasMedia) {
    return sendChatGroupReply(client, {
      groupId: params.groupId,
      text: "",
      images: params.images,
      videos: params.videos,
      files: params.files,
      mentionedUserIds: params.mentionedUserIds,
    });
  }

  let lastReply: SendChatGroupMessageReplyType | undefined;
  for (let i = 0; i < chunks.length; i++) {
    lastReply = await sendChatGroupReply(client, {
      groupId: params.groupId,
      text: chunks[i],
      images: i === 0 ? params.images : undefined,
      videos: i === 0 ? params.videos : undefined,
      files: i === 0 ? params.files : undefined,
      mentionedUserIds: i === 0 ? params.mentionedUserIds : undefined,
    });
  }
  return lastReply!;
}

export async function deliverReplyWithTyping(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
  log?: TypingLogger,
): Promise<SendChatGroupMessageReplyType> {
  await signalChatGroupTypingBestEffort(client, params.groupId, true, log);
  try {
    return await sendChatGroupReplyChunked(client, params);
  } finally {
    await signalChatGroupTypingBestEffort(client, params.groupId, false, log);
  }
}
