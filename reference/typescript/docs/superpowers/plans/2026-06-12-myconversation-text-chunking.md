# myconversation Text Chunking — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split outbound chat-group replies longer than 4000 characters into multiple `SendChatGroupMessage` RPCs so the myconversation server (4096-char limit) never rejects agent replies.

**Architecture:** Centralize chunking in `src/outbound/reply.ts` using OpenClaw's `chunkTextForOutbound`. `sendChatGroupReply` remains the single-RPC primitive; new `sendChatGroupReplyChunked` orchestrates sequential sends with fail-fast error handling. All delivery call sites (`dispatch.ts`, `channel.ts`, `deliverReplyWithTyping`) route through the chunked helper.

**Tech Stack:** TypeScript, Vitest, `@connectrpc/connect`, `openclaw/plugin-sdk/text-chunking`, `@genjutsu/myconversation-connect`

**Spec:** `docs/superpowers/specs/2026-06-12-myconversation-text-chunking-design.md`

---

## File map

| File | Responsibility |
|------|----------------|
| `src/outbound/reply.ts` | `MYCONVERSATION_TEXT_CHUNK_LIMIT`, `chunkChatGroupReplyText`, `sendChatGroupReplyChunked`; update `deliverReplyWithTyping` |
| `src/outbound/reply.test.ts` | Unit tests for chunking, fail-fast, mentions-on-first-chunk |
| `src/inbound/dispatch.ts` | Call `sendChatGroupReplyChunked`; log `chunkIndex` / `chunkCount`; fail log with `sentChunks` |
| `src/channel.ts` | Outbound `sendText` → `sendChatGroupReplyChunked` |
| `README.md` | Document multi-message behavior for long replies |

---

### Task 1: `chunkChatGroupReplyText` (TDD)

**Files:**
- Modify: `src/outbound/reply.ts`
- Test: `src/outbound/reply.test.ts`

- [ ] **Step 1: Write failing tests**

Add to `src/outbound/reply.test.ts`:

```typescript
import {
  MYCONVERSATION_TEXT_CHUNK_LIMIT,
  chunkChatGroupReplyText,
  sendChatGroupReplyChunked,
} from "./reply.js";

describe("chunkChatGroupReplyText", () => {
  it("returns one chunk for short text", () => {
    const text = "a".repeat(100);
    const chunks = chunkChatGroupReplyText(text);
    expect(chunks).toHaveLength(1);
    expect(chunks[0]).toBe(text);
  });

  it("returns multiple chunks each within the limit for long text", () => {
    const text = "word ".repeat(1200).trim(); // ~6000 chars
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/nemo/go/src/gitlab.genjutsu.ai/marketplace/openclaw/myconversation
pnpm test src/outbound/reply.test.ts
```

Expected: FAIL — `chunkChatGroupReplyText` / `MYCONVERSATION_TEXT_CHUNK_LIMIT` not exported.

- [ ] **Step 3: Implement `chunkChatGroupReplyText`**

At top of `src/outbound/reply.ts`, add import and exports:

```typescript
import { chunkTextForOutbound } from "openclaw/plugin-sdk/text-chunking";

export const MYCONVERSATION_TEXT_CHUNK_LIMIT = 4000;

export function chunkChatGroupReplyText(text: string): string[] {
  const trimmed = text.trim();
  if (!trimmed) {
    return [];
  }
  return chunkTextForOutbound(trimmed, MYCONVERSATION_TEXT_CHUNK_LIMIT);
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: PASS for `chunkChatGroupReplyText` tests (other suites may still pass).

- [ ] **Step 5: Commit**

```bash
git add src/outbound/reply.ts src/outbound/reply.test.ts
git commit -m "feat(myconversation): add chunkChatGroupReplyText helper"
```

---

### Task 2: `sendChatGroupReplyChunked` (TDD)

**Files:**
- Modify: `src/outbound/reply.ts`
- Test: `src/outbound/reply.test.ts`

- [ ] **Step 1: Write failing tests**

Add to `src/outbound/reply.test.ts`:

```typescript
function makeMessage(id: number, content: string) {
  return {
    message: { id: BigInt(id), groupId: 16n, senderUserId: 92n, content },
    duplicate: false,
  };
}

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
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: FAIL — `sendChatGroupReplyChunked` not defined.

- [ ] **Step 3: Implement `sendChatGroupReplyChunked`**

Add after `sendChatGroupReply` in `src/outbound/reply.ts`:

```typescript
export async function sendChatGroupReplyChunked(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
): Promise<SendChatGroupMessageReply> {
  const chunks = chunkChatGroupReplyText(params.text);
  if (chunks.length === 0) {
    return { duplicate: false };
  }

  let lastReply: SendChatGroupMessageReply | undefined;
  for (let i = 0; i < chunks.length; i++) {
    lastReply = await sendChatGroupReply(client, {
      groupId: params.groupId,
      text: chunks[i],
      images: i === 0 ? params.images : undefined,
      videos: i === 0 ? params.videos : undefined,
      files: i === 0 ? params.files : undefined,
      mentionedUserIds: i === 0 ? params.mentionedUserIds : undefined,
    });
  }
  return lastReply!;
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/outbound/reply.ts src/outbound/reply.test.ts
git commit -m "feat(myconversation): send long replies as chunked messages"
```

---

### Task 3: Wire callers

**Files:**
- Modify: `src/outbound/reply.ts` (`deliverReplyWithTyping`)
- Modify: `src/inbound/dispatch.ts`
- Modify: `src/channel.ts`

- [ ] **Step 1: Update `deliverReplyWithTyping`**

In `src/outbound/reply.ts`, change the send inside `deliverReplyWithTyping`:

```typescript
return await sendChatGroupReplyChunked(client, params);
```

(replace `sendChatGroupReply`)

- [ ] **Step 2: Update inbound dispatch**

In `src/inbound/dispatch.ts`:

1. Change import:

```typescript
import {
  createChatGroupTypingSession,
  sendChatGroupReplyChunked,
  chunkChatGroupReplyText,
} from "../outbound/reply.js";
```

2. Inside `delivery.deliver`, replace `sendChatGroupReply` with chunked send and extended logging:

```typescript
const chunks = chunkChatGroupReplyText(text);
const totalChunks = chunks.length;
try {
  const reply = await sendChatGroupReplyChunked(unaryClient, {
    groupId,
    text,
  });
  log.info?.("myconversation: sent chat group reply", {
    groupId,
    messageId: asNumber(reply.message?.id),
    duplicate: Boolean(reply.duplicate),
    chunkCount: totalChunks,
  });
} catch (error) {
  log.error?.("myconversation: SendChatGroupMessage failed", {
    groupId,
    totalChunks,
    error: String(error),
  });
  throw error;
}
```

Note: `sentChunks` on failure is optional v1 — OpenClaw rethrow preserves fail-fast; exact sent count can be added later if needed.

- [ ] **Step 3: Update outbound `sendText` in `channel.ts`**

Change import to include `sendChatGroupReplyChunked` and replace call:

```typescript
import {
  sendChatGroupReplyChunked,
  signalChatGroupTypingBestEffort,
} from "./outbound/reply.js";
```

```typescript
const reply = await sendChatGroupReplyChunked(client, {
  groupId,
  text: String(params.text ?? ""),
});
```

- [ ] **Step 4: Run full test suite + typecheck**

```bash
pnpm test
pnpm run typecheck
```

Expected: all PASS, no type errors.

- [ ] **Step 5: Commit**

```bash
git add src/outbound/reply.ts src/inbound/dispatch.ts src/channel.ts
git commit -m "feat(myconversation): route all outbound replies through chunked send"
```

---

### Task 4: README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add note under "What the plugin does"**

After the bullet about `SendChatGroupMessage`, add:

```markdown
- Splits outbound replies longer than 4000 characters into multiple group messages (same pattern as OpenClaw Telegram) so the server 4096-character limit is never exceeded.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs(myconversation): document long-reply chunking"
```

---

### Task 5: Final verification

- [ ] **Step 1: Run CI-equivalent checks**

```bash
pnpm test
pnpm run typecheck
pnpm run build
```

Expected: all exit 0.

- [ ] **Step 2: Manual smoke (optional)**

With gateway + dev UI running, trigger an agent reply >4096 chars. Confirm multiple bot bubbles and no `max_len` validation error in logs.

---

## Plan self-review

| Spec requirement | Task |
|------------------|------|
| Hardcoded 4000 limit | Task 1 |
| `chunkTextForOutbound` | Task 1 |
| `sendChatGroupReplyChunked` orchestration | Task 2 |
| Fail-fast on RPC error | Task 2 test + implementation |
| Mentions first chunk only | Task 2 |
| Wire dispatch + channel + deliverReplyWithTyping | Task 3 |
| Logging chunkCount | Task 3 |
| README | Task 4 |
| Unit tests (short, long, fail-fast, empty, mentions) | Tasks 1–2 |

No placeholders. Types consistent across tasks.
