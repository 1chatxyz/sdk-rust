# myconversation Plugin — Outbound Text Chunking

**Date:** 2026-06-12  
**Status:** Approved (brainstorming)  
**Scope:** OpenClaw channel plugin (`openclaw/myconversation`) — outbound reply delivery only.

---

## 1. Summary

The myconversation server rejects `SendChatGroupMessage` when `content` exceeds **4096** characters (proto `max_len: 4096`). The plugin currently sends the full agent reply in a single RPC, which fails for long responses.

This change adds **Telegram-style multi-message delivery**: split outbound text into chunks of at most **4000** characters and send each chunk as a separate `SendChatGroupMessage`. Short replies behave unchanged (one RPC).

Chunking is centralized in `src/outbound/reply.ts` so both inbound dispatch and gateway outbound paths are covered.

---

## 2. Decisions (locked)

| Topic | Decision |
|-------|----------|
| UX for long replies | Multiple consecutive group messages (like Telegram) |
| Chunk limit | Hardcoded **4000** (safety margin under server 4096) |
| Config | No new `channels.myconversation.textChunkLimit` in v1 |
| Error policy | **Fail-fast**: stop on first chunk RPC failure; already-sent chunks remain visible |
| Chunk algorithm | Reuse OpenClaw `chunkTextForOutbound` from `openclaw/plugin-sdk/text-chunking` |
| Mentions / media | Mentions and attachments only on first chunk; media out of scope (`media: false`) |
| Outbound adapter metadata | Not added in v1 (centralized send covers all call sites) |

---

## 3. Background

### Server limit

```protobuf
message SendChatGroupMessageRequest {
  string content = 2 [(validate.rules).string = { max_len: 4096 }];
}
```

### OpenClaw Telegram reference

- `TELEGRAM_TEXT_CHUNK_LIMIT = 4000`
- Outbound adapter uses `chunker` + `textChunkLimit` before `sendMessageTelegram`
- Generic helper: `chunkTextForOutbound(text, limit)` — prefers newline/space breaks, hard-splits when needed

### Plugin gap

Inbound replies use a custom `delivery.deliver` callback in `dispatch.ts`. This path does **not** pass through the channel outbound adapter chunking layer. Chunking must happen inside the plugin before gRPC.

---

## 4. Architecture

```
Agent reply (may exceed 4096)
  └─ delivery.deliver / outbound.sendText
       └─ sendChatGroupReplyChunked()
            ├─ chunks = chunkTextForOutbound(text, 4000)
            └─ for each chunk (sequential):
                 SendChatGroupMessage({
                   content: chunk,
                   clientMessageId: randomUUID(),
                   mentionedUserIds: first chunk only,
                   images/videos/files: first chunk only
                 })
                 on RPC error → throw (fail-fast)
```

### Call sites (all route through chunked send)

| Call site | File |
|-----------|------|
| Inbound group reply | `src/inbound/dispatch.ts` |
| Gateway outbound `sendText` | `src/channel.ts` |
| `deliverReplyWithTyping` | `src/outbound/reply.ts` |

### Typing

No change. `createChatGroupTypingSession` wraps the full agent turn; chunks are sent while typing is active; typing stops in `finally` after dispatch completes or throws.

---

## 5. Components

### 5.1 Constants

```typescript
export const MYCONVERSATION_TEXT_CHUNK_LIMIT = 4000;
```

### 5.2 `chunkChatGroupReplyText(text: string): string[]`

- Thin wrapper: `chunkTextForOutbound(text, MYCONVERSATION_TEXT_CHUNK_LIMIT)`
- Exported for unit tests

### 5.3 `sendChatGroupReplyChunked(client, params): Promise<SendChatGroupMessageReply>`

- Split `params.text` into chunks
- If zero chunks after trim (empty text): return without RPC (caller may already guard; function is safe either way)
- For each chunk index `i`:
  - Call existing `sendChatGroupReply` with:
    - `text: chunk`
    - `mentionedUserIds`: only when `i === 0`
    - `images` / `videos` / `files`: only when `i === 0`
  - On error: rethrow immediately (fail-fast)
- Return the **last** successful `SendChatGroupMessageReply` (preserves existing callers that read `message.id`)

### 5.4 `sendChatGroupReply`

Keep as the single-RPC primitive (one chunk, one UUID). `sendChatGroupReplyChunked` orchestrates multiple calls.

Callers switch from `sendChatGroupReply` to `sendChatGroupReplyChunked` at delivery boundaries.

---

## 6. Error handling & edge cases

| Case | Behavior |
|------|----------|
| Empty / whitespace-only text | No RPC; return early |
| `text.length ≤ 4000` | Single RPC (same as today) |
| `text.length > 4000` | Multiple sequential RPCs |
| Chunk *k* fails after *k-1* succeeded | Throw; chunks 1..k-1 remain in group; log `{ groupId, sentChunks: k-1, totalChunks, error }` |
| Block streaming (multiple `deliver` calls) | Each deliver invocation chunks independently if its payload exceeds 4000 |
| Per-chunk idempotency | Each chunk gets a new `clientMessageId`; no cross-chunk dedup (acceptable) |

**Out of scope:**

- Configurable limit / chunk mode
- Rollback or delete partially sent chunks
- Media on follow-up chunks
- Outbound adapter `textChunkLimit` + `chunker` declaration

---

## 7. Logging

On successful multi-chunk send (inbound path):

```
myconversation: sent chat group reply
  groupId, messageId, duplicate, chunkIndex, chunkCount
```

On failure:

```
myconversation: SendChatGroupMessage failed
  groupId, sentChunks, totalChunks, error
```

---

## 8. Files to change

| File | Change |
|------|--------|
| `src/outbound/reply.ts` | Add constant, `chunkChatGroupReplyText`, `sendChatGroupReplyChunked`; update `deliverReplyWithTyping` |
| `src/inbound/dispatch.ts` | Use `sendChatGroupReplyChunked`; extend success/error logs |
| `src/channel.ts` | Outbound `sendText` uses `sendChatGroupReplyChunked` |
| `src/outbound/reply.test.ts` | Unit tests for chunking and fail-fast |
| `README.md` | Note that long replies are split into multiple messages |

**Dependency:** `openclaw/plugin-sdk/text-chunking` (already available via peer `openclaw >= 2026.6.5`).

---

## 9. Testing

### Unit tests (`reply.test.ts`)

1. **Short text** — 100 chars → `chunkChatGroupReplyText` returns 1 chunk; `sendChatGroupReplyChunked` calls client once
2. **Long text** — 5000 chars → ≥2 chunks; every chunk length ≤ 4000; client called once per chunk
3. **Fail-fast** — mock client: chunk 1 ok, chunk 2 throws → exactly 2 calls, error propagates
4. **Empty text** — 0 client calls
5. **Mentions on first chunk only** — multi-chunk send passes `mentionedUserIds` only on first RPC

### Manual

- E2E with dev UI: prompt agent for reply >4096 chars; verify multiple bubbles, no gRPC validation error

---

## 10. Relationship to prior spec

The 2026-06-08 chatgroup design stated "one complete message" for v1. This spec **updates delivery semantics** for replies exceeding the server limit: users see multiple consecutive bot messages instead of a failed send. Typing + final delivery model is unchanged; only long text is split.

---

## 11. Non-goals

- Changing myconversation server `max_len`
- Block streaming / preview streaming configuration
- `channels.myconversation.textChunkLimit` config schema
