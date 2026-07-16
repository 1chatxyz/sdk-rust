import { readFile } from "node:fs/promises";

import {
  createChannelPluginBase,
  createChatChannelPlugin,
} from "openclaw/plugin-sdk/channel-core";
import type { OpenClawConfig } from "openclaw/plugin-sdk/channel-core";
import {
  createTopLevelChannelConfigAdapter,
  mapAllowFromEntries,
} from "openclaw/plugin-sdk/compat";

import {
  parseMyConversationChannelConfig,
  shouldRequireMention,
} from "./config.js";
import type { MyConversationChannelConfig } from "./config.js";
import { createMyEdgeClient } from "./connect/myedge.js";
import {
  parseGroupTarget,
} from "./inbound/dispatch.js";
import { prepareOutboundMedia } from "./media/outbound.js";
import {
  uploadFileForAccount,
  type MyEdgeUploadApi,
} from "./media/upload.js";
import {
  sendChatGroupReplyChunked,
  signalChatGroupTypingBestEffort,
} from "./outbound/reply.js";
import {
  resolveClientForAccount,
  resolveGroupIdFromOutboundParams,
} from "./runtime.js";
import {
  startMyConversationGatewayAccount,
  type MyConversationGatewayContext,
} from "./gateway.js";

export type ResolvedMyConversationAccount = MyConversationChannelConfig & {
  accountId: string;
  enabled: boolean;
  configured: boolean;
};

const CHANNEL_ID = "myconversation";

function readChannelSection(
  config: OpenClawConfig,
): Record<string, unknown> | undefined {
  const section = (config.channels as Record<string, unknown> | undefined)?.[
    CHANNEL_ID
  ];
  if (typeof section !== "object" || section == null || Array.isArray(section)) {
    return undefined;
  }
  return section as Record<string, unknown>;
}

export function resolveMyConversationAccount(
  config: OpenClawConfig,
  accountId?: string | null,
): ResolvedMyConversationAccount {
  const section = readChannelSection(config);
  const resolved = parseMyConversationChannelConfig(section);
  return {
    ...resolved,
    accountId: accountId?.trim() || "default",
    enabled: section?.enabled !== false,
    configured: true,
  };
}

function isMyConversationConfigured(config: OpenClawConfig): boolean {
  try {
    resolveMyConversationAccount(config);
    return true;
  } catch {
    return false;
  }
}

const myConversationConfigAdapter = createTopLevelChannelConfigAdapter({
  sectionKey: CHANNEL_ID,
  resolveAccount: (cfg) => resolveMyConversationAccount(cfg),
  listAccountIds: (cfg) => (isMyConversationConfigured(cfg) ? ["default"] : []),
  defaultAccountId: () => "default",
  deleteMode: "clear-fields",
  clearBaseFields: [
    "endpoint",
    "tenantId",
    "token",
    "userId",
    "activeGroupsPolicy",
    "groups",
    "username",
  ],
  resolveAllowFrom: () => [],
  formatAllowFrom: (allowFrom) => mapAllowFromEntries(allowFrom),
});

export const myConversationChannelPlugin = createChatChannelPlugin({
  base: {
    ...createChannelPluginBase({
      id: CHANNEL_ID,
      meta: {
        id: CHANNEL_ID,
        label: "myconversation",
        selectionLabel: "myconversation (self-hosted)",
        docsPath: "/channels/myconversation",
        docsLabel: "myconversation",
        blurb: "Connect OpenClaw to myconversation staff group chat over internal gRPC.",
      },
      capabilities: {
        chatTypes: ["group"],
        media: true,
      },
      reload: { configPrefixes: ["channels.myconversation"] },
      config: {
        ...myConversationConfigAdapter,
        isConfigured: (account: ResolvedMyConversationAccount) => account.configured,
        describeAccount: (account: ResolvedMyConversationAccount) => ({
          accountId: account.accountId,
          enabled: account.enabled,
          configured: account.configured,
          endpoint: account.endpoint,
          tenantId: account.tenantId,
          tokenConfigured: Boolean(account.token),
          userId: account.userId,
          username: account.username,
        }),
      },
      setup: {
        resolveAccount: resolveMyConversationAccount,
        inspectAccount(config: OpenClawConfig) {
          try {
            const resolved = resolveMyConversationAccount(config);
            return {
              enabled: resolved.enabled,
              configured: true,
              endpoint: resolved.endpoint,
              tenantId: resolved.tenantId,
              tokenConfigured: Boolean(resolved.token),
              userId: resolved.userId,
            };
          } catch {
            return {
              enabled: false,
              configured: false,
            };
          }
        },
      },
    }),
    groups: {
      resolveRequireMention: ({
        cfg,
        accountId,
        groupId,
      }: {
        cfg: OpenClawConfig;
        accountId?: string | null;
        groupId?: string | null;
      }) => {
        try {
          const account = resolveMyConversationAccount(cfg, accountId);
          return shouldRequireMention(account, groupId ?? "");
        } catch {
          return true;
        }
      },
    },
    messaging: {
      targetPrefixes: ["myconversation"],
      normalizeTarget: (target: string) => target.trim(),
      inferTargetChatType: ({ to }: { to: string }) =>
        parseGroupTarget(to) != null ? "group" : "direct",
      targetResolver: {
        looksLikeId: (target: string) => parseGroupTarget(target) != null,
        hint: "myconversation:group:<id>",
      },
    },
    gateway: {
      startAccount: async (ctx: MyConversationGatewayContext) =>
        startMyConversationGatewayAccount(ctx),
    },
    heartbeat: {
      sendTyping: async ({
        cfg,
        to,
        accountId,
      }: {
        cfg: OpenClawConfig;
        to: string;
        accountId?: string | null;
      }) => {
        const account = resolveMyConversationAccount(cfg, accountId);
        const client = resolveClientForAccount(account);
        const groupId =
          parseGroupTarget(to) ?? resolveGroupIdFromOutboundParams({ to });
        await signalChatGroupTypingBestEffort(client, groupId, true);
      },
      clearTyping: async ({
        cfg,
        to,
        accountId,
      }: {
        cfg: OpenClawConfig;
        to: string;
        accountId?: string | null;
      }) => {
        const account = resolveMyConversationAccount(cfg, accountId);
        const client = resolveClientForAccount(account);
        const groupId =
          parseGroupTarget(to) ?? resolveGroupIdFromOutboundParams({ to });
        await signalChatGroupTypingBestEffort(client, groupId, false);
      },
    },
  },
  threading: {
    topLevelReplyToMode: "reply",
  },
  outbound: {
    attachedResults: {
      sendText: async ({
        cfg,
        to,
        text,
        accountId,
      }: {
        cfg: OpenClawConfig;
        to: string;
        text?: string;
        accountId?: string | null;
      }) => {
        const account = resolveMyConversationAccount(cfg, accountId);
        const client = resolveClientForAccount(account);
        const groupId = resolveGroupIdFromOutboundParams({ to, text });
        const reply = await sendChatGroupReplyChunked(client, {
          groupId,
          text: String(text ?? ""),
        });
        return {
          messageId: String(reply.message?.id ?? ""),
          duplicate: Boolean(reply.duplicate),
        };
      },
      sendMedia: async ({
        cfg,
        to,
        text,
        mediaUrl,
        accountId,
        mediaReadFile,
      }: {
        cfg: OpenClawConfig;
        to: string;
        text?: string;
        mediaUrl?: string;
        accountId?: string | null;
        mediaReadFile?: (filePath: string) => Promise<Buffer>;
      }) => {
        const account = resolveMyConversationAccount(cfg, accountId);
        if (!account.userId) {
          throw new Error(
            "myconversation: userId is required to upload outbound media",
          );
        }
        const client = resolveClientForAccount(account);
        const groupId = resolveGroupIdFromOutboundParams({ to, text });
        const edge = createMyEdgeClient(account) as unknown as MyEdgeUploadApi;
        const prepared = await prepareOutboundMedia({
          userId: account.userId,
          mediaUrls: mediaUrl ? [mediaUrl] : [],
          uploadFile: (args) =>
            uploadFileForAccount({
              edge,
              userId: account.userId!,
              ...args,
            }),
          readLocalFile: async (p) =>
            mediaReadFile ? mediaReadFile(p) : readFile(p),
        });
        for (const v of prepared.skippedVideos) {
          void v;
        }
        const reply = await sendChatGroupReplyChunked(client, {
          groupId,
          text: String(text ?? ""),
          images: prepared.images,
          files: prepared.files,
        });
        return {
          messageId: String(reply.message?.id ?? ""),
          duplicate: Boolean(reply.duplicate),
        };
      },
    },
  },
});
