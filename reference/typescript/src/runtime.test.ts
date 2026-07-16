import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  getMyConversationRuntime,
  isChannelRuntimeReady,
  resolveInboundPluginRuntime,
  resolveReadyChannelRuntime,
  setMyConversationChannelRuntime,
  waitForChannelRuntimeReady,
  type MyConversationPluginRuntime,
} from "./runtime.js";

function makeReadyChannelRuntime(): NonNullable<
  MyConversationPluginRuntime["channel"]
> {
  return {
    routing: {
      resolveAgentRoute: vi.fn(() => ({
        agentId: "main",
        sessionKey: "session",
      })),
    },
    session: {
      resolveStorePath: vi.fn(() => "/tmp/sessions"),
      readSessionUpdatedAt: vi.fn(),
      recordInboundSession: vi.fn(),
    },
    reply: {
      formatAgentEnvelope: vi.fn(({ body }: { body: string }) => body),
      resolveEnvelopeFormatOptions: vi.fn(() => ({})),
      finalizeInboundContext: vi.fn((ctx) => ctx),
      dispatchReplyWithBufferedBlockDispatcher: vi.fn(),
    },
    text: {
      hasControlCommand: vi.fn(() => false),
    },
    commands: {
      shouldHandleTextCommands: vi.fn(() => true),
    },
  };
}

describe("isChannelRuntimeReady", () => {
  it("returns false when dispatch helpers are missing", () => {
    expect(isChannelRuntimeReady(undefined)).toBe(false);
    expect(
      isChannelRuntimeReady({
        routing: {},
      }),
    ).toBe(false);
  });

  it("returns true when the full channel surface is present", () => {
    expect(isChannelRuntimeReady(makeReadyChannelRuntime())).toBe(true);
  });
});

describe("resolveInboundPluginRuntime", () => {
  afterEach(() => {
    setMyConversationChannelRuntime(undefined);
  });

  it("prefers gateway channelRuntime over a partial global runtime", () => {
    const readyChannel = makeReadyChannelRuntime();
    setMyConversationChannelRuntime({ channel: { routing: {} } });

    expect(
      resolveInboundPluginRuntime({ log: { info: vi.fn() } }, readyChannel).channel,
    ).toBe(readyChannel);
  });

  it("prefers the global runtime from setRuntime when gateway runtime is absent", () => {
    const globalRuntime = { channel: makeReadyChannelRuntime() };
    setMyConversationChannelRuntime(globalRuntime);
    const fallback = { channel: { routing: {} } };

    expect(resolveInboundPluginRuntime(fallback)).toBe(globalRuntime);
  });

  it("falls back when the global runtime has no channel surface", () => {
    const fallback = { channel: makeReadyChannelRuntime() };
    setMyConversationChannelRuntime({ log: { info: vi.fn() } });

    expect(resolveInboundPluginRuntime(fallback)).toBe(fallback);
  });
  it("returns ready channelRuntime immediately without polling", () => {
    const readyChannel = makeReadyChannelRuntime();
    expect(
      resolveReadyChannelRuntime({ channelRuntime: readyChannel }),
    ).toBe(readyChannel);
  });
});

describe("waitForChannelRuntimeReady", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    setMyConversationChannelRuntime(undefined);
  });

  afterEach(() => {
    vi.useRealTimers();
    setMyConversationChannelRuntime(undefined);
  });

  it("resolves once the gateway channel runtime becomes ready", async () => {
    const gatewayChannel: MyConversationPluginRuntime["channel"] = { routing: {} };
    const promise = waitForChannelRuntimeReady({
      gatewayChannelRuntime: gatewayChannel,
      pollMs: 100,
      timeoutMs: 1_000,
    });
    const expectation = expect(promise).resolves.toEqual(
      expect.objectContaining({
        channel: expect.objectContaining({
          reply: expect.objectContaining({
            dispatchReplyWithBufferedBlockDispatcher: expect.any(Function),
          }),
        }),
      }),
    );

    await vi.advanceTimersByTimeAsync(100);
    Object.assign(gatewayChannel, makeReadyChannelRuntime());
    await vi.advanceTimersByTimeAsync(100);
    await expectation;
  });

  it("resolves once the global runtime becomes ready", async () => {
    const promise = waitForChannelRuntimeReady({
      gatewayChannelRuntime: { routing: {} },
      pollMs: 100,
      timeoutMs: 1_000,
    });
    const expectation = expect(promise).resolves.toEqual(
      expect.objectContaining({
        channel: expect.objectContaining({
          reply: expect.objectContaining({
            dispatchReplyWithBufferedBlockDispatcher: expect.any(Function),
          }),
        }),
      }),
    );

    await vi.advanceTimersByTimeAsync(250);
    setMyConversationChannelRuntime({ channel: makeReadyChannelRuntime() });
    await vi.advanceTimersByTimeAsync(100);
    await expectation;
  });

  it("throws when the runtime never becomes ready", async () => {
    const promise = waitForChannelRuntimeReady({
      gatewayChannelRuntime: { routing: {} },
      pollMs: 100,
      timeoutMs: 300,
    });
    const expectation = expect(promise).rejects.toThrow(
      "myconversation: OpenClaw channel runtime not ready after 300ms",
    );
    await vi.advanceTimersByTimeAsync(350);
    await expectation;
  });
});

describe("getMyConversationRuntime", () => {
  afterEach(() => {
    setMyConversationChannelRuntime(undefined);
  });

  it("returns the latest runtime set by OpenClaw", () => {
    const runtime = { channel: makeReadyChannelRuntime() };
    setMyConversationChannelRuntime(runtime);
    expect(getMyConversationRuntime()).toBe(runtime);
  });
});
