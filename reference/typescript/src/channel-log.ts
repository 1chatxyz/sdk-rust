import { ChatGroupMessageInfo } from "@genjutsu/myconversation-connect/myconversation_pb";
import { createSubsystemLogger } from "openclaw/plugin-sdk/runtime";

import type { MentionGateDebug } from "./inbound/mention.js";

export function serializeChatGroupMessageRawJson(
  message: ChatGroupMessageInfo,
): string {
  return JSON.stringify(message.toJson());
}

const inboundLog = createSubsystemLogger(
  "gateway/channels/myconversation",
).child("inbound");
const outboundLog = createSubsystemLogger(
  "gateway/channels/myconversation",
).child("outbound");

export function formatMyConversationInboundLogLine(params: {
  from: string;
  to: string;
  body: string;
}): string {
  const preview =
    params.body.length > 120
      ? `${params.body.slice(0, 117)}...`
      : params.body;
  return `Inbound message ${params.from} -> ${params.to} (group, ${params.body.length} chars) preview="${preview}"`;
}

export function formatMyConversationOutboundLogLine(params: {
  to: string;
  chars: number;
  messageId?: string;
}): string {
  const idSuffix = params.messageId ? `, messageId=${params.messageId}` : "";
  return `Outbound message -> ${params.to} (group, ${params.chars} chars${idSuffix})`;
}

export function logMyConversationInbound(params: {
  from: string;
  to: string;
  body: string;
  meta?: Record<string, unknown>;
}): void {
  inboundLog.info(formatMyConversationInboundLogLine(params), params.meta);
}

export function logMyConversationOutbound(params: {
  to: string;
  chars: number;
  messageId?: string;
  meta?: Record<string, unknown>;
}): void {
  outboundLog.info(formatMyConversationOutboundLogLine(params), params.meta);
}

export function formatMyConversationInboundSkipLogLine(params: {
  reason: string;
  groupId: number;
  messageId?: number;
  senderUserId: number;
  contentPreview: string;
  rawMessageJson: string;
  debug: MentionGateDebug;
}): string {
  const { debug } = params;
  return [
    `Skipped inbound message (${params.reason})`,
    `group=${params.groupId}`,
    `messageId=${params.messageId ?? "?"}`,
    `sender=${params.senderUserId}`,
    `requireMention=${debug.requireMention}`,
    `wasMentioned=${debug.wasMentioned}`,
    `mentionMatch=${debug.mentionMatch}`,
    `mentionedUserIds=[${debug.mentionedUserIds.join(",")}]`,
    `botUserId=${debug.botUserId ?? "?"}`,
    `allowTextCommands=${debug.allowTextCommands}`,
    `hasControlCommand=${debug.hasControlCommand}`,
    `preview="${params.contentPreview}"`,
    `rawMessage=${params.rawMessageJson}`,
  ].join(" ");
}

export function logMyConversationInboundSkip(params: {
  reason: string;
  groupId: number;
  messageId?: number;
  senderUserId: number;
  contentPreview: string;
  message: ChatGroupMessageInfo;
  debug?: MentionGateDebug;
}): void {
  const rawMessageJson = serializeChatGroupMessageRawJson(params.message);
  const line = params.debug
    ? formatMyConversationInboundSkipLogLine({
        reason: params.reason,
        groupId: params.groupId,
        messageId: params.messageId,
        senderUserId: params.senderUserId,
        contentPreview: params.contentPreview,
        rawMessageJson,
        debug: params.debug,
      })
    : [
        `Skipped inbound message (${params.reason})`,
        `group=${params.groupId}`,
        `messageId=${params.messageId ?? "?"}`,
        `sender=${params.senderUserId}`,
        `preview="${params.contentPreview}"`,
        `rawMessage=${rawMessageJson}`,
      ].join(" ");
  inboundLog.info(line, {
    groupId: params.groupId,
    messageId: params.messageId,
    senderUserId: params.senderUserId,
    reason: params.reason,
    contentPreview: params.contentPreview,
    rawMessage: rawMessageJson,
    mentionDebug: params.debug,
  });
}
