import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { parseMyConversationChannelConfig } from "../config.js";
import type { MyConversationConnectClient } from "../connect/client.js";
import {
  ChatGroupStreamController,
  computeReconnectDelayMs,
} from "./stream.js";

describe("computeReconnectDelayMs", () => {
  it("uses exponential backoff capped by max delay", () => {
    expect(computeReconnectDelayMs(0, 2_000, 60_000)).toBe(2_000);
    expect(computeReconnectDelayMs(1, 2_000, 60_000)).toBe(4_000);
    expect(computeReconnectDelayMs(5, 2_000, 60_000)).toBe(60_000);
  });
});

describe("ChatGroupStreamController reconnect", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("backs off reconnect attempts after stream errors", async () => {
    let callCount = 0;
    const client = {
      streamChatGroups: vi.fn((_request: unknown, signal?: AbortSignal) => {
        callCount += 1;
        return (async function* () {
          if (callCount === 1) {
            yield {
              item: {
                case: "message" as const,
                value: { id: 7n, groupId: 16n, senderUserId: 1n },
              },
            };
            throw new Error("14 UNAVAILABLE: timeout");
          }
          if (callCount === 2) {
            throw new Error("14 UNAVAILABLE: timeout again");
          }
          yield {
            item: {
              case: "ping" as const,
              value: { serverTimeUnixMs: 1n },
            },
          };
          while (!signal?.aborted) {
            await new Promise((resolve) => setTimeout(resolve, 60_000));
          }
        })();
      }),
    } as unknown as MyConversationConnectClient;

    const logger = {
      info: vi.fn(),
      warn: vi.fn(),
      debug: vi.fn(),
    };

    const controller = new ChatGroupStreamController({
      client,
      config: parseMyConversationChannelConfig({
        endpoint: "mc:8080",
        tenantId: "tenant-abc",
        token: "token",
        userId: 92,
        activeGroupsPolicy: "allowlist",
        groups: { "16": { requireMention: false } },
      }),
      reconnectDelayMs: 1_000,
      maxReconnectDelayMs: 8_000,
      logger,
    });

    controller.start();
    await vi.waitFor(() => expect(client.streamChatGroups).toHaveBeenCalledTimes(1));

    await vi.waitFor(() =>
      expect(logger.warn).toHaveBeenCalledWith(
        "myconversation: scheduling stream reconnect",
        expect.objectContaining({ delayMs: 1_000, attempt: 1 }),
      ),
    );

    await vi.advanceTimersByTimeAsync(1_000);
    await vi.waitFor(() => expect(client.streamChatGroups).toHaveBeenCalledTimes(2));

    await vi.waitFor(() =>
      expect(logger.warn).toHaveBeenCalledWith(
        "myconversation: scheduling stream reconnect",
        expect.objectContaining({ delayMs: 2_000, attempt: 2 }),
      ),
    );

    await vi.advanceTimersByTimeAsync(2_000);
    await vi.waitFor(() => expect(client.streamChatGroups).toHaveBeenCalledTimes(3));
    await vi.waitFor(() =>
      expect(logger.info).toHaveBeenCalledWith("myconversation: stream connected"),
    );

    controller.stop();
  });
});

describe("ChatGroupStreamController health check", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("reconnects when the stream goes idle without events", async () => {
    let callCount = 0;
    const client = {
      streamChatGroups: vi.fn((_request: unknown, signal?: AbortSignal) => {
        callCount += 1;
        return (async function* () {
          if (callCount === 1) {
            yield {
              item: {
                case: "ping" as const,
                value: { serverTimeUnixMs: 1n },
              },
            };
          }

          await new Promise<void>((resolve, reject) => {
            const onAbort = () => {
              signal?.removeEventListener("abort", onAbort);
              reject(Object.assign(new Error("aborted"), { name: "AbortError" }));
            };
            if (signal?.aborted) {
              onAbort();
              return;
            }
            signal?.addEventListener("abort", onAbort, { once: true });
          });
        })();
      }),
    } as unknown as MyConversationConnectClient;

    const logger = {
      info: vi.fn(),
      warn: vi.fn(),
      debug: vi.fn(),
    };

    const controller = new ChatGroupStreamController({
      client,
      config: parseMyConversationChannelConfig({
        endpoint: "mc:8080",
        tenantId: "tenant-abc",
        token: "token",
        userId: 92,
        activeGroupsPolicy: "allowlist",
        groups: { "16": { requireMention: false } },
      }),
      reconnectDelayMs: 1_000,
      maxReconnectDelayMs: 8_000,
      streamIdleTimeoutMs: 30_000,
      streamMaxAgeMs: 60 * 60_000,
      logger,
    });

    controller.start();
    await vi.waitFor(() => expect(client.streamChatGroups).toHaveBeenCalledTimes(1));

    await vi.advanceTimersByTimeAsync(45_000);

    await vi.waitFor(() =>
      expect(logger.warn).toHaveBeenCalledWith(
        "myconversation: stream idle timeout, reconnecting",
        expect.objectContaining({ idleMs: expect.any(Number) }),
      ),
    );

    await vi.advanceTimersByTimeAsync(1_000);
    await vi.waitFor(() => expect(client.streamChatGroups).toHaveBeenCalledTimes(2));

    controller.stop();
  });
});
