import { describe, expect, it } from "vitest";

import { parseMyConversationChannelConfig } from "../config.js";
import {
  detectInboundControlCommand,
  normalizeMentionedUserIds,
  resolveMyConversationMentionGate,
  shouldHandleInboundMessage,
  stripMentionTokensForCommandDetection,
  wasInboundBotMentioned,
} from "./mention.js";

describe("shouldHandleInboundMessage", () => {
  const config = parseMyConversationChannelConfig({
    endpoint: "mc:8080",
    tenantId: "tenant-abc",
    token: "token",
    userId: "123",
    username: "OpenClaw",
    groupPolicy: "allowlist",
    groups: {
      "42": { requireMention: true },
      "43": { requireMention: false },
    },
  });

  it("skips groups outside the allowlist", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 99,
          senderUserId: 456,
          content: "@OpenClaw hello",
          mentionedUserIds: [123],
        },
        config,
      ),
    ).toBe(false);
  });

  it("skips self-authored events", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 123,
          content: "@OpenClaw hello",
          mentionedUserIds: [123],
        },
        config,
      ),
    ).toBe(false);
  });

  it("accepts explicit mentionedUserIds", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "hello there",
          mentionedUserIds: [123],
        },
        config,
      ),
    ).toBe(true);
  });

  it("ignores bracket mention tokens in content when mentionedUserIds is empty", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "[[@Win Helpers:123]] can you help?",
          mentionedUserIds: [],
        },
        config,
      ),
    ).toBe(false);
  });

  it("accepts content containing bot username when mentionedUserIds is empty", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "@OpenClaw can you help?",
          mentionedUserIds: [],
        },
        config,
      ),
    ).toBe(true);

    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "hey OpenClaw can you help?",
          mentionedUserIds: [],
        },
        config,
      ),
    ).toBe(true);
  });

  it("requires mentions only for groups configured that way", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "plain text",
          mentionedUserIds: [],
        },
        config,
      ),
    ).toBe(false);

    expect(
      shouldHandleInboundMessage(
        {
          groupId: 43,
          senderUserId: 456,
          content: "plain text",
          mentionedUserIds: [],
        },
        config,
      ),
    ).toBe(true);
  });
});

describe("resolveMyConversationMentionGate", () => {
  const config = parseMyConversationChannelConfig({
    endpoint: "mc:8080",
    tenantId: "tenant-abc",
    token: "token",
    userId: "123",
    username: "OpenClaw",
    groupPolicy: "allowlist",
    groups: {
      "42": { requireMention: true },
      "43": { requireMention: false },
    },
  });

  it("allows authorized control commands without mention in mention-only groups", () => {
    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 42,
      rawBody: "/status",
      mentionedUserIds: [],
      allowTextCommands: true,
      hasControlCommand: true,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(false);
    expect(gate.reason).toBe("authorized-command");
    expect(gate.effectiveWasMentioned).toBe(true);
    expect(gate.debug.hasControlCommand).toBe(true);
  });

  it("allows /status after a bracket mention prefix via command bypass only", () => {
    const hasControlCommand = (body: string) => body.trim() === "/status";
    expect(
      detectInboundControlCommand({
        rawBody: "[[@Win Helpers:123]] /status",
        cfg: {},
        hasControlCommand,
      }),
    ).toBe(true);

    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 42,
      rawBody: "[[@Win Helpers:123]] /status",
      mentionedUserIds: [],
      allowTextCommands: true,
      hasControlCommand: true,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(false);
    expect(gate.reason).toBe("authorized-command");
  });

  it("accepts when content contains bot username", () => {
    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 42,
      rawBody: "@OpenClaw hello",
      mentionedUserIds: [],
      allowTextCommands: true,
      hasControlCommand: false,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(false);
    expect(gate.reason).toBe("mentioned");
    expect(gate.debug.mentionMatch).toBe("username-in-content");
  });

  it("prioritizes mentionedUserIds over content", () => {
    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 42,
      rawBody: "plain text",
      mentionedUserIds: [123],
      allowTextCommands: true,
      hasControlCommand: false,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(false);
    expect(gate.reason).toBe("mentioned");
    expect(gate.debug.mentionMatch).toBe("mentioned-user-ids");
  });

  it("normalizes mentioned user ids", () => {
    expect(normalizeMentionedUserIds([99, 0, -1, 123, 99])).toEqual([99, 123]);
  });

  it("strips bracket mentions before command detection", () => {
    expect(
      stripMentionTokensForCommandDetection("[[@Win Helpers:123]] /status"),
    ).toBe("/status");
  });

  it("skips plain text without mentionedUserIds in mention-only groups", () => {
    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 42,
      rawBody: "plain text",
      mentionedUserIds: [],
      allowTextCommands: true,
      hasControlCommand: false,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(true);
    expect(gate.reason).toBe("missing-mention");
  });

  it("accepts all messages in groups without mention requirement", () => {
    const gate = resolveMyConversationMentionGate({
      account: config,
      groupId: 43,
      rawBody: "plain text",
      mentionedUserIds: [],
      allowTextCommands: true,
      hasControlCommand: false,
      commandAuthorized: true,
    });

    expect(gate.shouldSkip).toBe(false);
    expect(gate.reason).toBe("mention-not-required");
  });
});

describe("wasInboundBotMentioned", () => {
  const config = parseMyConversationChannelConfig({
    endpoint: "mc:8080",
    tenantId: "tenant-abc",
    token: "token",
    userId: "123",
    username: "OpenClaw",
    groupPolicy: "allowlist",
    groups: {
      "42": { requireMention: true },
    },
  });

  it("returns true for mentionedUserIds array", () => {
    expect(wasInboundBotMentioned("hello", [123], config)).toBe(true);
  });

  it("returns false for bracket mention in body without mentionedUserIds", () => {
    expect(
      wasInboundBotMentioned("[[@Win Helpers:123]] help", [], config),
    ).toBe(false);
  });

  it("returns true when content contains bot username", () => {
    expect(wasInboundBotMentioned("@OpenClaw help", [], config)).toBe(true);
    expect(wasInboundBotMentioned("hey OpenClaw help", [], config)).toBe(true);
  });

  it("returns false for plain text without mention", () => {
    expect(wasInboundBotMentioned("plain text", [], config)).toBe(false);
  });
});
