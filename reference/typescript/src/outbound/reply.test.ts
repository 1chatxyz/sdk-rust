import { ConnectError, Code } from "@connectrpc/connect";
import { describe, expect, it, vi } from "vitest";

import type { MyConversationConnectClient } from "../connect/client.js";
import {
  MYCONVERSATION_TEXT_CHUNK_LIMIT,
  chunkChatGroupReplyText,
  createChatGroupTypingSession,
  deliverReplyWithTyping,
  isTypingUnsupportedError,
  sendChatGroupReply,
  sendChatGroupReplyChunked,
  signalChatGroupTypingBestEffort,
} from "./reply.js";

describe("chunkChatGroupReplyText", () => {
  it("returns one chunk for short text", () => {
    const text = "a".repeat(100);
    const chunks = chunkChatGroupReplyText(text);
    expect(chunks).toHaveLength(1);
    expect(chunks[0]).toBe(text);
  });

  it("returns multiple chunks each within the limit for long text", () => {
    const text = "x".repeat(5000);
    const chunks = chunkChatGroupReplyText(text);
    expect(chunks.length).toBeGreaterThan(1);
    for (const chunk of chunks) {
      expect(chunk.length).toBeLessThanOrEqual(MYCONVERSATION_TEXT_CHUNK_LIMIT);
    }
    expect(chunks.join("")).toBe(text);
  });

  it("returns no chunks for empty text", () => {
    expect(chunkChatGroupReplyText("")).toEqual([]);
    expect(chunkChatGroupReplyText("   ")).toEqual([]);
  });
});

function makeMessage(id: number, content: string) {
  return {
    message: { id: BigInt(id), groupId: 16n, senderUserId: 92n, content },
    duplicate: false,
  };
}

describe("sendChatGroupReply", () => {
  it("extracts [42] from [[@Alice:42]] done, content unchanged", async () => {
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValue(makeMessage(99, "[[@Alice:42]] done"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReply(client, {
      groupId: 16,
      text: "[[@Alice:42]] done",
    });

    expect(sendChatGroupMessage).toHaveBeenCalledOnce();
    expect(sendChatGroupMessage.mock.calls[0][0].content).toBe(
      "[[@Alice:42]] done",
    );
    expect(sendChatGroupMessage.mock.calls[0][0].mentionedUserIds).toEqual([
      42,
    ]);
  });

  it("passes empty mentionedUserIds for plain text", async () => {
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValue(makeMessage(99, "hello"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReply(client, {
      groupId: 16,
      text: "hello",
    });

    expect(sendChatGroupMessage.mock.calls[0][0].mentionedUserIds).toEqual([]);
  });
});

describe("sendChatGroupReplyChunked", () => {
  it("sends one RPC for short text", async () => {
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValue(makeMessage(99, "short"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    const reply = await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: "hello",
    });

    expect(sendChatGroupMessage).toHaveBeenCalledOnce();
    expect(reply.message?.content).toBe("short");
  });

  it("sends multiple RPCs for long text", async () => {
    const longText = "x".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "part1"))
      .mockResolvedValueOnce(makeMessage(2, "part2"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    const reply = await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: longText,
    });

    expect(sendChatGroupMessage).toHaveBeenCalledTimes(2);
    expect(reply.message?.id).toBe(2n);
    for (const call of sendChatGroupMessage.mock.calls) {
      expect(call[0].content.length).toBeLessThanOrEqual(
        MYCONVERSATION_TEXT_CHUNK_LIMIT,
      );
    }
  });

  it("fail-fast when a chunk RPC throws", async () => {
    const longText = "y".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "ok"))
      .mockRejectedValueOnce(new Error("rpc failed"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await expect(
      sendChatGroupReplyChunked(client, { groupId: 16, text: longText }),
    ).rejects.toThrow("rpc failed");
    expect(sendChatGroupMessage).toHaveBeenCalledTimes(2);
  });

  it("does not call RPC for empty text", async () => {
    const sendChatGroupMessage = vi.fn();
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    const reply = await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: "   ",
    });

    expect(sendChatGroupMessage).not.toHaveBeenCalled();
    expect(reply.duplicate).toBe(false);
    expect(reply.message).toBeUndefined();
  });

  it("passes mentionedUserIds only on the first chunk", async () => {
    const longText = "z".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "a"))
      .mockResolvedValueOnce(makeMessage(2, "b"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: longText,
      mentionedUserIds: [42, 43],
    });

    expect(sendChatGroupMessage.mock.calls[0][0].mentionedUserIds).toEqual([
      42, 43,
    ]);
    expect(sendChatGroupMessage.mock.calls[1][0].mentionedUserIds).toEqual([]);
  });

  it("extracts mention ids only on the first chunk from text", async () => {
    const longText = "[[@Alice:42]] " + "x".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "a"))
      .mockResolvedValueOnce(makeMessage(2, "b"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: longText,
    });

    expect(sendChatGroupMessage.mock.calls.length).toBeGreaterThan(1);
    expect(sendChatGroupMessage.mock.calls[0][0].mentionedUserIds).toEqual([
      42,
    ]);
    expect(sendChatGroupMessage.mock.calls[1][0].mentionedUserIds).toEqual([]);
  });

  it("sends file-only message when text is empty but files present", async () => {
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValue(makeMessage(99, ""));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: "   ",
      files: ["api/v1/upload/92/a.pdf"],
    });

    expect(sendChatGroupMessage).toHaveBeenCalledOnce();
    expect(sendChatGroupMessage.mock.calls[0][0].content).toBe("");
    expect(sendChatGroupMessage.mock.calls[0][0].files).toEqual([
      "api/v1/upload/92/a.pdf",
    ]);
  });

  it("attaches images/files only on the first chunk", async () => {
    const longText = "x".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "a"))
      .mockResolvedValueOnce(makeMessage(2, "b"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: longText,
      images: ["api/v1/upload/92/a.png"],
      files: ["api/v1/upload/92/a.pdf"],
    });

    expect(sendChatGroupMessage.mock.calls[0][0].images).toEqual([
      "api/v1/upload/92/a.png",
    ]);
    expect(sendChatGroupMessage.mock.calls[0][0].files).toEqual([
      "api/v1/upload/92/a.pdf",
    ]);
    expect(sendChatGroupMessage.mock.calls[1][0].images).toEqual([]);
    expect(sendChatGroupMessage.mock.calls[1][0].files).toEqual([]);
  });
});

describe("isTypingUnsupportedError", () => {
  it("detects Connect Unimplemented", () => {
    expect(
      isTypingUnsupportedError(
        new ConnectError("SignalChatGroupTyping unimplemented", Code.Unimplemented),
      ),
    ).toBe(true);
  });

  it("detects legacy UNIMPLEMENTED error text", () => {
    expect(
      isTypingUnsupportedError(
        new Error(
          "12 UNIMPLEMENTED: unknown method SignalChatGroupTyping for service genjutsu.myconversation.v1.MyConversation",
        ),
      ),
    ).toBe(true);
  });

  it("returns false for unrelated errors", () => {
    expect(isTypingUnsupportedError(new Error("14 UNAVAILABLE: timeout"))).toBe(
      false,
    );
  });
});

describe("signalChatGroupTypingBestEffort", () => {
  it("does not throw when typing RPC is unimplemented", async () => {
    const client = {
      signalChatGroupTyping: vi.fn().mockRejectedValue(
        new ConnectError("SignalChatGroupTyping unimplemented", Code.Unimplemented),
      ),
    } as unknown as MyConversationConnectClient;

    await expect(
      signalChatGroupTypingBestEffort(client, 16, true),
    ).resolves.toBeUndefined();
  });
});

describe("createChatGroupTypingSession", () => {
  it("signals on at start, keepalives, then off at stop", async () => {
    vi.useFakeTimers();
    const signalChatGroupTyping = vi.fn().mockResolvedValue({});
    const client = {
      signalChatGroupTyping,
    } as unknown as MyConversationConnectClient;

    const session = createChatGroupTypingSession(client, 16, undefined, {
      keepaliveIntervalMs: 5000,
    });

    await session.start();
    expect(signalChatGroupTyping).toHaveBeenCalledWith({
      groupId: 16,
      typing: true,
    });

    await vi.advanceTimersByTimeAsync(5000);
    expect(signalChatGroupTyping).toHaveBeenCalledTimes(2);

    await session.stop();
    expect(signalChatGroupTyping).toHaveBeenLastCalledWith({
      groupId: 16,
      typing: false,
    });

    vi.useRealTimers();
  });
});

describe("deliverReplyWithTyping", () => {
  it("still sends the reply when typing RPC is unimplemented", async () => {
    const client = {
      signalChatGroupTyping: vi.fn().mockRejectedValue(
        new ConnectError("SignalChatGroupTyping unimplemented", Code.Unimplemented),
      ),
      sendChatGroupMessage: vi.fn().mockResolvedValue({
        message: { id: 99n, groupId: 16n, senderUserId: 92n, content: "hi" },
      }),
    } as unknown as MyConversationConnectClient;

    const reply = await deliverReplyWithTyping(client, {
      groupId: 16,
      text: "hello from bot",
    });

    expect(client.sendChatGroupMessage).toHaveBeenCalledOnce();
    expect(reply.message?.content).toBe("hi");
  });
});
