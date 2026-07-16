import type { ChatGroupMessageInfo } from "@genjutsu/myconversation-connect/myconversation_pb";

import type { MyConversationChannelConfig } from "./config.js";
import { MyConversationConnectClient } from "./connect/client.js";

export type StreamLogger = {
  debug?(message: string, meta?: Record<string, unknown>): void;
  info?(message: string, meta?: Record<string, unknown>): void;
  warn?(message: string, meta?: Record<string, unknown>): void;
  error?(message: string, meta?: Record<string, unknown>): void;
};

export type MyConversationPluginRuntime = StreamLogger & {
  log?: StreamLogger;
  config?: unknown;
  getConfig?(): unknown;
  channel?: MyConversationChannelRuntime;
};

export type MyConversationChannelRuntime = {
  routing?: {
    resolveAgentRoute?: (params: Record<string, unknown>) => {
      agentId: string;
      sessionKey: string;
      accountId?: string;
    };
  };
  session?: {
    resolveStorePath?: (
      store: unknown,
      params: { agentId: string },
    ) => string;
    readSessionUpdatedAt?: (params: {
      storePath: string;
      sessionKey: string;
    }) => number | undefined;
    recordInboundSession?: (...args: unknown[]) => Promise<unknown> | unknown;
  };
  reply?: {
    formatAgentEnvelope?: (params: Record<string, unknown>) => string;
    resolveEnvelopeFormatOptions?: (cfg: unknown) => Record<string, unknown>;
    finalizeInboundContext?: (
      params: Record<string, unknown>,
    ) => Record<string, unknown>;
    dispatchReplyWithBufferedBlockDispatcher?: (
      params: Record<string, unknown>,
    ) => Promise<unknown>;
  };
  text?: {
    hasControlCommand?: (body: string, cfg: unknown) => boolean;
  };
  commands?: {
    shouldHandleTextCommands?: (params: {
      cfg: unknown;
      surface: string;
    }) => boolean;
  };
  mentions?: Record<string, unknown>;
};

let currentRuntime: MyConversationPluginRuntime | undefined;

const streamClients = new Map<string, MyConversationConnectClient>();
const unaryClients = new Map<string, MyConversationConnectClient>();

function makeStreamClientKey(config: MyConversationChannelConfig): string {
  return `${config.tenantId}:${config.endpoint}:stream`;
}

function makeUnaryClientKey(config: MyConversationChannelConfig): string {
  return `${config.tenantId}:${config.endpoint}:unary`;
}

export function setMyConversationChannelRuntime(
  runtime: MyConversationPluginRuntime | undefined,
): void {
  currentRuntime = runtime;
}

export function getMyConversationRuntime():
  | MyConversationPluginRuntime
  | undefined {
  return currentRuntime;
}

export type ReadyChannelRuntime = MyConversationChannelRuntime & {
  routing: NonNullable<MyConversationChannelRuntime["routing"]> & {
    resolveAgentRoute: NonNullable<
      NonNullable<MyConversationChannelRuntime["routing"]>["resolveAgentRoute"]
    >;
  };
  session: NonNullable<MyConversationChannelRuntime["session"]> & {
    resolveStorePath: NonNullable<
      NonNullable<MyConversationChannelRuntime["session"]>["resolveStorePath"]
    >;
    readSessionUpdatedAt: NonNullable<
      NonNullable<MyConversationChannelRuntime["session"]>["readSessionUpdatedAt"]
    >;
    recordInboundSession: NonNullable<
      NonNullable<MyConversationChannelRuntime["session"]>["recordInboundSession"]
    >;
  };
  reply: NonNullable<MyConversationChannelRuntime["reply"]> & {
    formatAgentEnvelope: NonNullable<
      NonNullable<MyConversationChannelRuntime["reply"]>["formatAgentEnvelope"]
    >;
    resolveEnvelopeFormatOptions: NonNullable<
      NonNullable<MyConversationChannelRuntime["reply"]>["resolveEnvelopeFormatOptions"]
    >;
    finalizeInboundContext: NonNullable<
      NonNullable<MyConversationChannelRuntime["reply"]>["finalizeInboundContext"]
    >;
    dispatchReplyWithBufferedBlockDispatcher: NonNullable<
      NonNullable<
        MyConversationChannelRuntime["reply"]
      >["dispatchReplyWithBufferedBlockDispatcher"]
    >;
  };
  text: NonNullable<MyConversationChannelRuntime["text"]> & {
    hasControlCommand: NonNullable<
      NonNullable<MyConversationChannelRuntime["text"]>["hasControlCommand"]
    >;
  };
  commands: NonNullable<MyConversationChannelRuntime["commands"]> & {
    shouldHandleTextCommands: NonNullable<
      NonNullable<MyConversationChannelRuntime["commands"]>["shouldHandleTextCommands"]
    >;
  };
};

export function isChannelRuntimeReady(
  channel: MyConversationChannelRuntime | undefined,
): channel is ReadyChannelRuntime {
  if (!channel?.routing?.resolveAgentRoute) {
    return false;
  }

  const session = channel.session;
  const reply = channel.reply;
  return Boolean(
    session?.resolveStorePath &&
      session.readSessionUpdatedAt &&
      session.recordInboundSession &&
      reply?.formatAgentEnvelope &&
      reply.resolveEnvelopeFormatOptions &&
      reply.finalizeInboundContext &&
      reply.dispatchReplyWithBufferedBlockDispatcher &&
      channel.text?.hasControlCommand &&
      channel.commands?.shouldHandleTextCommands,
  );
}

/** Prefer ctx.channelRuntime from gateway startAccount; fall back to setRuntime(). */
export function resolveInboundPluginRuntime(
  fallback?: MyConversationPluginRuntime,
  channelRuntime?: MyConversationChannelRuntime,
): MyConversationPluginRuntime {
  if (channelRuntime && isChannelRuntimeReady(channelRuntime)) {
    return { ...(fallback ?? getMyConversationRuntime() ?? {}), channel: channelRuntime };
  }

  const global = getMyConversationRuntime();
  if (global?.channel && isChannelRuntimeReady(global.channel)) {
    return global;
  }

  return fallback ?? global ?? {};
}

export function resolveReadyChannelRuntime(params: {
  channelRuntime?: MyConversationChannelRuntime;
  fallback?: MyConversationPluginRuntime;
}): ReadyChannelRuntime | undefined {
  const resolved = resolveInboundPluginRuntime(
    params.fallback,
    params.channelRuntime,
  );
  const channel = resolved.channel;
  return isChannelRuntimeReady(channel) ? channel : undefined;
}

const DEFAULT_CHANNEL_RUNTIME_WAIT_MS = 60_000;
const CHANNEL_RUNTIME_POLL_MS = 250;

export async function waitForChannelRuntimeReady(params: {
  resolveRuntime?: () => MyConversationPluginRuntime;
  gatewayChannelRuntime?: MyConversationChannelRuntime;
  log?: StreamLogger;
  timeoutMs?: number;
  pollMs?: number;
}): Promise<{
  runtime: MyConversationPluginRuntime;
  channel: ReadyChannelRuntime;
}> {
  const timeoutMs = params.timeoutMs ?? DEFAULT_CHANNEL_RUNTIME_WAIT_MS;
  const pollMs = params.pollMs ?? CHANNEL_RUNTIME_POLL_MS;
  const deadline = Date.now() + timeoutMs;
  let loggedWait = false;

  while (Date.now() < deadline) {
    const runtime = resolveInboundPluginRuntime(
      params.resolveRuntime?.() ?? getMyConversationRuntime(),
      params.gatewayChannelRuntime,
    );
    const channel = runtime.channel;
    if (isChannelRuntimeReady(channel)) {
      return { runtime, channel };
    }

    if (!loggedWait) {
      params.log?.info?.(
        "myconversation: waiting for OpenClaw channel runtime to become ready",
      );
      loggedWait = true;
    }

    await new Promise((resolve) => setTimeout(resolve, pollMs));
  }

  throw new Error(
    `myconversation: OpenClaw channel runtime not ready after ${timeoutMs}ms`,
  );
}

export async function ensureInboundChannelRuntime(params: {
  gatewayChannelRuntime?: MyConversationChannelRuntime;
  log?: StreamLogger;
  timeoutMs?: number;
}): Promise<ReadyChannelRuntime> {
  const ready = resolveReadyChannelRuntime({
    channelRuntime: params.gatewayChannelRuntime,
    fallback: getMyConversationRuntime(),
  });
  if (ready) {
    return ready;
  }

  const { channel } = await waitForChannelRuntimeReady({
    gatewayChannelRuntime: params.gatewayChannelRuntime,
    log: params.log,
    timeoutMs: params.timeoutMs,
  });
  return channel;
}

function resolveCachedClient(
  cache: Map<string, MyConversationConnectClient>,
  key: string,
  config: MyConversationChannelConfig,
): MyConversationConnectClient {
  const existing = cache.get(key);
  if (existing) {
    return existing;
  }

  const client = new MyConversationConnectClient(config);
  cache.set(key, client);
  return client;
}

/** Long-lived StreamChatGroups client — do not share with unary RPCs on grpc-web. */
export function resolveStreamClientForAccount(
  config: MyConversationChannelConfig,
): MyConversationConnectClient {
  return resolveCachedClient(
    streamClients,
    makeStreamClientKey(config),
    config,
  );
}

/** Unary RPCs (typing, send message) — isolated from the stream transport. */
export function resolveUnaryClientForAccount(
  config: MyConversationChannelConfig,
): MyConversationConnectClient {
  return resolveCachedClient(
    unaryClients,
    makeUnaryClientKey(config),
    config,
  );
}

/** @deprecated Use resolveUnaryClientForAccount or resolveStreamClientForAccount. */
export function resolveClientForAccount(
  config: MyConversationChannelConfig,
): MyConversationConnectClient {
  return resolveUnaryClientForAccount(config);
}

export function stopAllMyConversationRuntime(): void {
  for (const client of streamClients.values()) {
    client.close();
  }
  for (const client of unaryClients.values()) {
    client.close();
  }
  streamClients.clear();
  unaryClients.clear();
}

export function resolveGroupIdFromOutboundParams(params: unknown): number {
  const queue = [params];
  const visited = new Set<unknown>();

  while (queue.length > 0) {
    const candidate = queue.shift();
    if (candidate == null || visited.has(candidate)) {
      continue;
    }
    visited.add(candidate);

    if (
      typeof candidate === "number" &&
      Number.isInteger(candidate) &&
      candidate > 0
    ) {
      return candidate;
    }

    if (typeof candidate === "string") {
      const trimmed = candidate.trim();
      const match = trimmed.match(/^myconversation:group:(\d+)$/);
      if (match) {
        return Number(match[1]);
      }
      if (/^\d+$/.test(trimmed)) {
        return Number(trimmed);
      }
      continue;
    }

    if (typeof candidate === "object") {
      const record = candidate as Record<string, unknown>;
      queue.push(
        record.groupId,
        record.group_id,
        record.threadId,
        record.thread_id,
        record.to,
        record.sessionKey,
        record.session_key,
        record.target,
        record.route,
      );
    }
  }

  throw new Error(
    "myconversation: could not resolve group id from outbound OpenClaw params",
  );
}

export type { ChatGroupMessageInfo };
