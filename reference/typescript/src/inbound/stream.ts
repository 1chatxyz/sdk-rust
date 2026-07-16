import type { ChatGroupStreamEvent } from "@genjutsu/myconversation-connect/myconversation_pb";

import type { MyConversationChannelConfig } from "../config.js";
import type { MyConversationConnectClient } from "../connect/client.js";
import {
  formatConnectError,
  formatLogLine,
} from "../connect/errors.js";
import {
  normalizeGrpcBaseUrl,
  shouldUseGrpcWebTransport,
} from "../connect/transport.js";
import type {
  ChatGroupMessageInfo,
  ChatGroupTypingIndicator,
} from "../connect/types.js";
import {
  asNumber,
  getStreamEventMessage,
  getStreamEventTyping,
} from "../connect/types.js";
import { shouldAcceptGroupMessage } from "./mention.js";

export type StreamLogger = {
  debug?(message: string, meta?: Record<string, unknown>): void;
  info?(message: string, meta?: Record<string, unknown>): void;
  warn?(message: string, meta?: Record<string, unknown>): void;
  error?(message: string, meta?: Record<string, unknown>): void;
};

export type ChatGroupStreamControllerOptions = {
  client: MyConversationConnectClient;
  config: MyConversationChannelConfig;
  username?: string;
  reconnectDelayMs?: number;
  maxReconnectDelayMs?: number;
  /** Reconnect when no stream events (ping/message/typing) arrive within this window. */
  streamIdleTimeoutMs?: number;
  /** Proactively reconnect before common gateway/LB max stream duration (~30m). */
  streamMaxAgeMs?: number;
  logger?: StreamLogger;
  onMessage?(message: ChatGroupMessageInfo): void | Promise<void>;
  onTyping?(typing: ChatGroupTypingIndicator): void | Promise<void>;
};

export function computeReconnectDelayMs(
  attempt: number,
  minDelayMs: number,
  maxDelayMs: number,
): number {
  const exponent = Math.max(0, attempt);
  return Math.min(maxDelayMs, minDelayMs * 2 ** exponent);
}

function isAbortError(error: unknown): boolean {
  return (
    error instanceof Error &&
    (error.name === "AbortError" || error.message.includes("aborted"))
  );
}

const DEFAULT_STREAM_IDLE_TIMEOUT_MS = 90_000;
const DEFAULT_STREAM_MAX_AGE_MS = 25 * 60_000;
const STREAM_HEALTH_CHECK_INTERVAL_MS = 15_000;

export class ChatGroupStreamController {
  private readonly minReconnectDelayMs: number;
  private readonly maxReconnectDelayMs: number;
  private readonly streamIdleTimeoutMs: number;
  private readonly streamMaxAgeMs: number;
  private reconnectTimer: NodeJS.Timeout | undefined;
  private streamAbort: AbortController | undefined;
  private streamTask: Promise<void> | undefined;
  private healthCheckTimer: NodeJS.Timeout | undefined;
  private lastEventAtMs = 0;
  private streamStartedAtMs = 0;
  private resumeAfterMessageId = 0;
  private reconnectAttempt = 0;
  private running = false;

  constructor(private readonly options: ChatGroupStreamControllerOptions) {
    this.minReconnectDelayMs = options.reconnectDelayMs ?? 2_000;
    this.maxReconnectDelayMs = options.maxReconnectDelayMs ?? 60_000;
    this.streamIdleTimeoutMs =
      options.streamIdleTimeoutMs ?? DEFAULT_STREAM_IDLE_TIMEOUT_MS;
    this.streamMaxAgeMs = options.streamMaxAgeMs ?? DEFAULT_STREAM_MAX_AGE_MS;
  }

  start(): void {
    if (this.running) {
      return;
    }
    this.running = true;
    this.reconnectAttempt = 0;
    this.streamTask = this.runStreamLoop();
  }

  stop(): void {
    this.running = false;
    this.stopHealthCheck();
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = undefined;
    }
    this.streamAbort?.abort();
    this.streamAbort = undefined;
  }

  private async runStreamLoop(): Promise<void> {
    while (this.running) {
      this.streamAbort = new AbortController();
      const signal = this.streamAbort.signal;

      const baseUrl = normalizeGrpcBaseUrl(this.options.config.endpoint);
      const transport = shouldUseGrpcWebTransport(baseUrl) ? "grpc-web" : "grpc";
      this.options.logger?.info?.(
        formatLogLine("myconversation: opening StreamChatGroups", {
          endpoint: this.options.config.endpoint,
          baseUrl,
          transport,
          tenantId: this.options.config.tenantId,
          resumeAfterMessageId: this.resumeAfterMessageId,
          reconnectAttempt: this.reconnectAttempt,
        }),
      );

      try {
        const stream = this.options.client.streamChatGroups(
          { resumeAfterMessageId: this.resumeAfterMessageId },
          signal,
        );

        this.startHealthCheck(signal);

        try {
          for await (const event of stream) {
            if (!this.running || signal.aborted) {
              return;
            }
            this.touchStreamActivity();
            this.markStreamHealthy();
            await this.handleEvent(event);
          }

          if (!this.running || signal.aborted) {
            return;
          }

          this.options.logger?.info?.("myconversation: stream ended", {
            reconnectAttempt: this.reconnectAttempt,
          });
          await this.waitBeforeReconnect();
        } finally {
          this.stopHealthCheck();
        }
      } catch (error) {
        if (!this.running) {
          return;
        }

        if (isAbortError(error)) {
          this.options.logger?.info?.(
            "myconversation: stream aborted, reconnecting",
            {
              resumeAfterMessageId: this.resumeAfterMessageId,
              reconnectAttempt: this.reconnectAttempt,
            },
          );
          await this.waitBeforeReconnect();
          continue;
        }

        this.options.logger?.warn?.(
          formatLogLine("myconversation: stream error", {
            ...formatConnectError(error),
            endpoint: this.options.config.endpoint,
            baseUrl,
            transport,
            tenantId: this.options.config.tenantId,
            reconnectAttempt: this.reconnectAttempt,
          }),
        );
        await this.waitBeforeReconnect();
      }
    }
  }

  private markStreamHealthy(): void {
    if (this.reconnectAttempt === 0) {
      return;
    }
    this.reconnectAttempt = 0;
    this.options.logger?.info?.("myconversation: stream connected");
  }

  private touchStreamActivity(): void {
    this.lastEventAtMs = Date.now();
  }

  private startHealthCheck(signal: AbortSignal): void {
    this.stopHealthCheck();
    const now = Date.now();
    this.lastEventAtMs = now;
    this.streamStartedAtMs = now;

    this.healthCheckTimer = setInterval(() => {
      if (!this.running || signal.aborted) {
        return;
      }

      const idleMs = Date.now() - this.lastEventAtMs;
      const ageMs = Date.now() - this.streamStartedAtMs;

      if (idleMs >= this.streamIdleTimeoutMs) {
        this.options.logger?.warn?.(
          "myconversation: stream idle timeout, reconnecting",
          {
            idleMs,
            streamIdleTimeoutMs: this.streamIdleTimeoutMs,
            resumeAfterMessageId: this.resumeAfterMessageId,
          },
        );
        this.streamAbort?.abort();
        return;
      }

      if (ageMs >= this.streamMaxAgeMs) {
        this.options.logger?.info?.(
          "myconversation: stream max age reached, reconnecting",
          {
            ageMs,
            streamMaxAgeMs: this.streamMaxAgeMs,
            resumeAfterMessageId: this.resumeAfterMessageId,
          },
        );
        this.streamAbort?.abort();
      }
    }, STREAM_HEALTH_CHECK_INTERVAL_MS);
  }

  private stopHealthCheck(): void {
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
      this.healthCheckTimer = undefined;
    }
  }

  private async handleEvent(event: ChatGroupStreamEvent): Promise<void> {
    const message = getStreamEventMessage(event);
    if (message) {
      const messageId = asNumber(message.id);
      if (messageId > this.resumeAfterMessageId) {
        this.resumeAfterMessageId = messageId;
      }

      const shouldAccept = shouldAcceptGroupMessage(
        {
          groupId: asNumber(message.groupId),
          senderUserId: asNumber(message.senderUserId),
          content: message.content,
          mentionedUserIds: (message.mentionedUserIds ?? []).map(asNumber),
        },
        this.options.config,
      );

      if (!shouldAccept) {
        this.options.logger?.debug?.(
          "myconversation: skipped inbound chat group message",
          {
            groupId: asNumber(message.groupId),
            senderUserId: asNumber(message.senderUserId),
            reason: "self-or-group-filter",
          },
        );
        return;
      }

      await this.options.onMessage?.(message);
      return;
    }

    const typing = getStreamEventTyping(event);
    if (typing) {
      await this.options.onTyping?.(typing);
    }
  }

  private waitBeforeReconnect(): Promise<void> {
    if (!this.running) {
      return Promise.resolve();
    }

    if (this.reconnectTimer) {
      return Promise.resolve();
    }

    const delayMs = computeReconnectDelayMs(
      this.reconnectAttempt,
      this.minReconnectDelayMs,
      this.maxReconnectDelayMs,
    );
    const attempt = this.reconnectAttempt + 1;
    this.reconnectAttempt = attempt;

    this.options.logger?.warn?.("myconversation: scheduling stream reconnect", {
      delayMs,
      attempt,
      resumeAfterMessageId: this.resumeAfterMessageId,
    });

    return new Promise((resolve) => {
      this.reconnectTimer = setTimeout(() => {
        this.reconnectTimer = undefined;
        resolve();
      }, delayMs);
    });
  }
}
