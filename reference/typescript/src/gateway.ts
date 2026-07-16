import type { OpenClawConfig } from "openclaw/plugin-sdk/channel-core";

import {
  resolveMyConversationAccount,
  type ResolvedMyConversationAccount,
} from "./channel.js";
import { handleMyConversationInbound } from "./inbound/dispatch.js";
import { asNumber } from "./connect/types.js";
import { ChatGroupStreamController } from "./inbound/stream.js";
import {
  isChannelRuntimeReady,
  resolveStreamClientForAccount,
  waitForChannelRuntimeReady,
  type MyConversationPluginRuntime,
} from "./runtime.js";

type GatewayLog = {
  info?(message: string, meta?: Record<string, unknown>): void;
  warn?(message: string, meta?: Record<string, unknown>): void;
  error?(message: string, meta?: Record<string, unknown>): void;
  debug?(message: string, meta?: Record<string, unknown>): void;
};

export type MyConversationGatewayContext = {
  cfg: OpenClawConfig;
  accountId: string;
  account: ResolvedMyConversationAccount;
  runtime: MyConversationPluginRuntime;
  channelRuntime?: MyConversationPluginRuntime["channel"];
  abortSignal: AbortSignal;
  log?: GatewayLog;
  setStatus: (next: Record<string, unknown>) => void;
};

export async function startMyConversationGatewayAccount(
  ctx: MyConversationGatewayContext,
): Promise<void> {
  if (!isChannelRuntimeReady(ctx.channelRuntime)) {
    await waitForChannelRuntimeReady({
      gatewayChannelRuntime: ctx.channelRuntime,
      log: ctx.log ?? console,
    });
  }

  const account = resolveMyConversationAccount(ctx.cfg, ctx.accountId);
  const streamClient = resolveStreamClientForAccount(account);
  let stream: ChatGroupStreamController | undefined;

  ctx.setStatus({
    accountId: ctx.accountId,
    running: true,
    configured: true,
    enabled: account.enabled,
    connected: false,
    endpoint: account.endpoint,
    tenantId: account.tenantId,
    userId: account.userId,
    tokenConfigured: true,
  });

  if (!account.userId) {
    ctx.log?.warn?.(
      `[${ctx.accountId}] myconversation: userId missing; outbound media uploads will fail`,
    );
  }

  ctx.log?.info?.(`[${ctx.accountId}] starting myconversation stream`, {
    endpoint: account.endpoint,
    tenantId: account.tenantId,
    userId: account.userId,
  });

  await new Promise<void>((resolve) => {
    stream = new ChatGroupStreamController({
      client: streamClient,
      config: account,
      username: account.username,
      logger: ctx.log ?? console,
      onMessage: async (message) => {
        try {
          await handleMyConversationInbound({
            cfg: ctx.cfg,
            account,
            message,
            log: ctx.log ?? console,
            gatewayChannelRuntime: ctx.channelRuntime,
          });
        } catch (error) {
          ctx.log?.error?.("myconversation: inbound dispatch failed", {
            groupId: asNumber(message.groupId),
            messageId: asNumber(message.id),
            error: String(error),
          });
        }
      },
    });

    stream.start();
    ctx.setStatus({
      accountId: ctx.accountId,
      running: true,
      configured: true,
      enabled: account.enabled,
      connected: true,
      endpoint: account.endpoint,
      tenantId: account.tenantId,
      userId: account.userId,
      tokenConfigured: true,
    });

    const onAbort = () => {
      stream?.stop();
      streamClient.close();
      ctx.setStatus({
        accountId: ctx.accountId,
        running: false,
        configured: true,
        enabled: account.enabled,
        connected: false,
        endpoint: account.endpoint,
        tenantId: account.tenantId,
        userId: account.userId,
        tokenConfigured: true,
      });
      ctx.log?.info?.(`[${ctx.accountId}] stopped myconversation stream`);
      resolve();
    };

    if (ctx.abortSignal.aborted) {
      onAbort();
      return;
    }

    ctx.abortSignal.addEventListener("abort", onAbort, { once: true });
  });
}
