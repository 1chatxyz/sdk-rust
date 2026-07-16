import { describe, expect, it } from "vitest";

import { ChatGroupMessageInfo } from "@genjutsu/myconversation-connect/myconversation_pb";

import {
  formatMyConversationInboundLogLine,
  formatMyConversationInboundSkipLogLine,
  formatMyConversationOutboundLogLine,
  serializeChatGroupMessageRawJson,
} from "./channel-log.js";

describe("formatMyConversationInboundLogLine", () => {
  it("matches the gateway/channels inbound log shape", () => {
    expect(
      formatMyConversationInboundLogLine({
        from: "myconversation:group:44",
        to: "@winhelpers",
        body: "/status",
      }),
    ).toBe(
      'Inbound message myconversation:group:44 -> @winhelpers (group, 7 chars) preview="/status"',
    );
  });
});

describe("formatMyConversationOutboundLogLine", () => {
  it("includes message id when present", () => {
    expect(
      formatMyConversationOutboundLogLine({
        to: "myconversation:group:44",
        chars: 42,
        messageId: "991",
      }),
    ).toBe(
      "Outbound message -> myconversation:group:44 (group, 42 chars, messageId=991)",
    );
  });
});

describe("serializeChatGroupMessageRawJson", () => {
  it("serializes bigint fields as strings in proto JSON", () => {
    const message = new ChatGroupMessageInfo({
      id: 991n,
      groupId: 44n,
      senderUserId: 92n,
      senderUsername: "alice",
      content: "hello",
      mentionedUserIds: [100n],
    });

    expect(serializeChatGroupMessageRawJson(message)).toBe(
      JSON.stringify({
        id: "991",
        groupId: "44",
        senderUserId: "92",
        senderUsername: "alice",
        content: "hello",
        mentionedUserIds: ["100"],
      }),
    );
  });
});

describe("formatMyConversationInboundSkipLogLine", () => {
  it("includes full raw message json", () => {
    const rawMessageJson =
      '{"id":"991","groupId":"44","senderUserId":"92","content":"hello","mentionedUserIds":[]}';

    expect(
      formatMyConversationInboundSkipLogLine({
        reason: "missing-mention",
        groupId: 44,
        messageId: 991,
        senderUserId: 92,
        contentPreview: "hello",
        rawMessageJson,
        debug: {
          requireMention: true,
          wasMentioned: false,
          mentionMatch: "none",
          mentionedUserIds: [],
          botUserId: 100,
          allowTextCommands: true,
          hasControlCommand: false,
        },
      }),
    ).toBe(
      'Skipped inbound message (missing-mention) group=44 messageId=991 sender=92 requireMention=true wasMentioned=false mentionMatch=none mentionedUserIds=[] botUserId=100 allowTextCommands=true hasControlCommand=false preview="hello" rawMessage={"id":"991","groupId":"44","senderUserId":"92","content":"hello","mentionedUserIds":[]}',
    );
  });
});
