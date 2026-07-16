import type { OpenClawConfig } from "openclaw/plugin-sdk/channel-core";
import { recordChannelActivity } from "openclaw/plugin-sdk/channel-activity-runtime";
import { dispatchInboundReplyWithBase } from "openclaw/plugin-sdk/inbound-reply-dispatch";
import type { FinalizedMsgContext } from "openclaw/plugin-sdk/reply-runtime";
import { readFile } from "node:fs/promises";

import type { ChatGroupMessageInfo } from "@genjutsu/myconversation-connect/myconversation_pb";

import { formatMention } from "../mention/format.js";
import {
  detectInboundControlCommand,
  resolveMyConversationMentionGate,
  shouldAcceptGroupMessage,
  wasInboundBotMentioned,
  normalizeMentionedUserIds,
} from "./mention.js";
import type { ResolvedMyConversationAccount } from "../channel.js";
import {
  logMyConversationInbound,
  logMyConversationInboundSkip,
  logMyConversationOutbound,
} from "../channel-log.js";
import { createMyEdgeClient } from "../connect/myedge.js";
import type {
  MyConversationChannelRuntime,
  ReadyChannelRuntime,
  StreamLogger,
} from "../runtime.js";
import { asNumber } from "../connect/types.js";
import {
  chunkChatGroupReplyText,
  createChatGroupTypingSession,
  sendChatGroupReplyChunked,
} from "../outbound/reply.js";
import {
  ensureInboundChannelRuntime,
  resolveUnaryClientForAccount,
} from "../runtime.js";
import {
  buildInboundMediaBody,
  successfulLocalPaths,
} from "../media/context.js";
import {
  cleanupTempDir,
  defaultMediaTempRoot,
  downloadInboundAttachments,
} from "../media/download.js";
import { selectInboundAttachments } from "../media/limits.js";
import {
  prepareOutboundMedia,
  resolveOutboundMediaUrlList,
} from "../media/outbound.js";
import {
  uploadFileForAccount,
  type MyEdgeUploadApi,
} from "../media/upload.js";

const CHANNEL_ID = "myconversation";

export function buildGroupTarget(groupId: number | string): string {
  return `${CHANNEL_ID}:group:${groupId}`;
}

export function parseGroupTarget(target: string): number | null {
  const match = target.trim().match(/^myconversation:group:(\d+)$/);
  return match ? Number(match[1]) : null;
}

export async function handleMyConversationInbound(params: {
  cfg: OpenClawConfig;
  account: ResolvedMyConversationAccount;
  message: ChatGroupMessageInfo;
  log?: StreamLogger;
  gatewayChannelRuntime?: MyConversationChannelRuntime;
}): Promise<void> {
  const { cfg, account, message, gatewayChannelRuntime } = params;
  const log = params.log ?? {};
  let channelRuntime: ReadyChannelRuntime;
  try {
    channelRuntime = await ensureInboundChannelRuntime({
      gatewayChannelRuntime,
      log,
      timeoutMs: 30_000,
    });
  } catch (error) {
    logMyConversationInboundSkip({
      reason: "runtime-unavailable",
      groupId: asNumber(message.groupId),
      messageId: asNumber(message.id),
      senderUserId: asNumber(message.senderUserId),
      contentPreview: (message.content ?? "").slice(0, 120),
      message,
    });
    log.warn?.(
      "myconversation: channel runtime unavailable; inbound message skipped",
      {
        groupId: asNumber(message.groupId),
        messageId: asNumber(message.id),
        error: String(error),
      },
    );
    return;
  }

  const groupId = asNumber(message.groupId);
  const senderUserId = asNumber(message.senderUserId);
  const messageId = asNumber(message.id);
  const rawBody = message.content ?? "";
  const apiMentionedUserIds = normalizeMentionedUserIds(
    (message.mentionedUserIds ?? []).map(asNumber),
  );

  if (
    !shouldAcceptGroupMessage(
      {
        groupId,
        senderUserId,
        content: rawBody,
        mentionedUserIds: apiMentionedUserIds,
      },
      account,
    )
  ) {
    logMyConversationInboundSkip({
      reason: "self-or-group-filter",
      groupId,
      messageId,
      senderUserId,
      contentPreview: rawBody.slice(0, 120),
      message,
    });
    log.debug?.("myconversation: skipped inbound chat group message", {
      groupId,
      senderUserId,
      reason: "self-or-group-filter",
    });
    return;
  }

  const allowTextCommands = channelRuntime.commands.shouldHandleTextCommands({
    cfg,
    surface: CHANNEL_ID,
  });
  const hasControlCommand = detectInboundControlCommand({
    rawBody,
    cfg,
    hasControlCommand: (body, config) =>
      channelRuntime.text.hasControlCommand(body, config),
  });
  const commandAuthorized = true;

  const mentionGate = resolveMyConversationMentionGate({
    account,
    groupId,
    rawBody,
    mentionedUserIds: apiMentionedUserIds,
    allowTextCommands,
    hasControlCommand,
    commandAuthorized,
  });
  if (mentionGate.shouldSkip) {
    logMyConversationInboundSkip({
      reason: mentionGate.reason,
      groupId,
      messageId,
      senderUserId,
      contentPreview: rawBody.slice(0, 120),
      message,
      debug: mentionGate.debug,
    });
    log.info?.("myconversation: skipped inbound chat group message", {
      groupId,
      messageId,
      senderUserId,
      reason: mentionGate.reason,
      contentPreview: rawBody.slice(0, 120),
      mentionDebug: mentionGate.debug,
    });
    return;
  }

  if ((message.videos?.length ?? 0) > 0) {
    log.debug?.("myconversation: skipped inbound videos", {
      reason: "skipped-videos",
      count: message.videos?.length ?? 0,
      messageId,
      groupId,
    });
  }

  let tempDir: string | undefined;
  let agentBody = rawBody;
  let mediaPaths: string[] = [];
  const inboundAttachments = selectInboundAttachments({
    images: message.images,
    files: message.files,
  });
  if (inboundAttachments.length > 0) {
    const downloaded = await downloadInboundAttachments({
      attachments: inboundAttachments,
      account: {
        endpoint: account.endpoint,
        tenantId: account.tenantId,
        token: account.token,
        staticUrl: account.staticUrl,
        mediaTempDir: account.mediaTempDir,
      },
      tempRoot: defaultMediaTempRoot(account),
      messageId: String(messageId),
    });
    tempDir = downloaded.tempDir;
    agentBody = buildInboundMediaBody({
      content: rawBody,
      results: downloaded.results,
    });
    mediaPaths = successfulLocalPaths(downloaded.results);
  }

  const target = buildGroupTarget(groupId);
  const route = channelRuntime.routing.resolveAgentRoute({
    cfg,
    channel: CHANNEL_ID,
    accountId: account.accountId,
    peer: {
      kind: "group",
      id: String(groupId),
    },
  });
  const senderName =
    message.senderUsername?.trim() || `user:${senderUserId}`;
  const senderUsername = message.senderUsername?.trim() ?? "";
  const senderMention =
    senderUserId > 0 && senderUsername !== ""
      ? formatMention(senderUsername, senderUserId)
      : undefined;
  const session = channelRuntime.session;
  const reply = channelRuntime.reply;
  const storePath = session.resolveStorePath(
    (cfg as { session?: { store?: unknown } }).session?.store,
    {
      agentId: route.agentId,
    },
  );
  const previousTimestamp = session.readSessionUpdatedAt({
    storePath,
    sessionKey: route.sessionKey,
  });
  const body = reply.formatAgentEnvelope({
    channel: "myconversation",
    from: senderName,
    timestamp: new Date(),
    previousTimestamp,
    envelope: reply.resolveEnvelopeFormatOptions(cfg),
    body: agentBody,
  });
  const wasMentioned = wasInboundBotMentioned(
    rawBody,
    apiMentionedUserIds,
    account,
  );

  const ctxPayload = reply.finalizeInboundContext({
    Body: body,
    BodyForAgent: agentBody,
    RawBody: agentBody,
    CommandBody: rawBody,
    MediaPaths: mediaPaths.length > 0 ? mediaPaths : undefined,
    From: target,
    To: target,
    SessionKey: route.sessionKey,
    AccountId: route.accountId ?? account.accountId,
    ChatType: "group",
    WasMentioned: wasMentioned || mentionGate.effectiveWasMentioned,
    ConversationLabel: `group:${groupId}`,
    GroupChannel: String(groupId),
    NativeChannelId: String(groupId),
    SenderName: senderName,
    SenderId: String(senderUserId),
    ...(senderMention ? { SenderMention: senderMention } : {}),
    Provider: CHANNEL_ID,
    Surface: CHANNEL_ID,
    MessageSid: String(asNumber(message.id)),
    MessageSidFull: String(asNumber(message.id)),
    ReplyToId: String(asNumber(message.id)),
    OriginatingChannel: CHANNEL_ID,
    OriginatingTo: target,
    CommandAuthorized: commandAuthorized,
  }) as FinalizedMsgContext;

  logMyConversationInbound({
    from: String(ctxPayload.From ?? target),
    to: (() => {
      const username = account.username?.trim();
      return username ? `@${username}` : String(ctxPayload.To ?? target);
    })(),
    body: rawBody,
    meta: {
      messageId: asNumber(message.id),
      groupId,
      senderUserId,
      senderUsername: message.senderUsername?.trim() || undefined,
      mentionReason: mentionGate.reason,
    },
  });
  log.info?.("myconversation: received inbound chat group message", {
    messageId: asNumber(message.id),
    groupId,
    senderUserId,
    senderUsername: message.senderUsername?.trim() || undefined,
    mentionReason: mentionGate.reason,
  });

  recordChannelActivity({
    channel: CHANNEL_ID,
    accountId: account.accountId,
    direction: "inbound",
  });

  const unaryClient = resolveUnaryClientForAccount(account);
  const typingSession = createChatGroupTypingSession(unaryClient, groupId, log);
  try {
    await typingSession.start();
    await dispatchInboundReplyWithBase({
      cfg,
      channel: CHANNEL_ID,
      accountId: account.accountId,
      route,
      storePath,
      ctxPayload,
      core: { channel: channelRuntime } as Parameters<
        typeof dispatchInboundReplyWithBase
      >[0]["core"],
      deliver: async (payload) => {
        const text = String(payload.text ?? "");
        const payloadWithMedia = payload as {
          mediaUrl?: string;
          mediaUrls?: string[];
        };
        // Prefer mediaUrls[]; do not concat mediaUrl (OpenClaw often sets both to the same path).
        const mediaUrls = resolveOutboundMediaUrlList({
          mediaUrls: Array.isArray(payloadWithMedia.mediaUrls)
            ? payloadWithMedia.mediaUrls
            : undefined,
          mediaUrl:
            typeof payloadWithMedia.mediaUrl === "string"
              ? payloadWithMedia.mediaUrl
              : undefined,
        });
        if (!text.trim() && mediaUrls.length === 0) {
          return;
        }
        let media = { images: [] as string[], files: [] as string[], skippedVideos: [] as string[] };
        if (mediaUrls.length > 0) {
          const edge = createMyEdgeClient(account) as unknown as MyEdgeUploadApi;
          media = await prepareOutboundMedia({
            userId: account.userId ?? "",
            mediaUrls,
            uploadFile: async (args) =>
              uploadFileForAccount({
                edge,
                userId: account.userId!,
                ...args,
              }),
            readLocalFile: readFile,
          });
        }
        if (media.skippedVideos.length > 0) {
          log.debug?.("myconversation: skipped outbound videos", {
            groupId,
            count: media.skippedVideos.length,
          });
        }
        if (!text.trim() && media.images.length === 0 && media.files.length === 0) {
          return;
        }
        const chunkCount = chunkChatGroupReplyText(text).length;
        try {
          const sent = await sendChatGroupReplyChunked(unaryClient, {
            groupId,
            text,
            images: media.images,
            files: media.files,
          });
          const sentMessageId = asNumber(sent.message?.id);
          logMyConversationOutbound({
            to: target,
            chars: text.length,
            messageId: sentMessageId > 0 ? String(sentMessageId) : undefined,
            meta: {
              groupId,
              duplicate: Boolean(sent.duplicate),
              chunkCount,
            },
          });
          log.info?.("myconversation: sent chat group reply", {
            groupId,
            messageId: sentMessageId,
            duplicate: Boolean(sent.duplicate),
            chunkCount,
          });
          recordChannelActivity({
            channel: CHANNEL_ID,
            accountId: account.accountId,
            direction: "outbound",
          });
        } catch (error) {
          log.error?.("myconversation: SendChatGroupMessage failed", {
            groupId,
            totalChunks: chunkCount,
            error: String(error),
          });
          throw error;
        }
      },
      onRecordError: (error) => {
        log.warn?.("myconversation: session record failed", {
          error: String(error),
        });
      },
      onDispatchError: (error, info) => {
        log.error?.("myconversation: reply dispatch failed", {
          groupId,
          kind: info.kind,
          error: String(error),
        });
        throw error instanceof Error
          ? error
          : new Error(`myconversation dispatch failed: ${String(error)}`);
      },
    });
  } finally {
    await typingSession.stop();
    if (tempDir) {
      await cleanupTempDir(tempDir);
    }
  }
}
