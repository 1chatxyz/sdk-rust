# myconversation Plugin — Mention Wire Format

**Date:** 2026-06-26  
**Status:** Approved (brainstorming)  
**Scope:** OpenClaw channel plugin (`openclaw/myconversation`) + win-helpers skill docs.

**Dependency:** `@genjutsu/myconversation-connect` **>= 1.191.0** (stream `ChatGroupMessageInfo` includes `sender_user_id` + `sender_username`).

---

## 1. Summary

Staff Group Chat UI shows mentions as `@Display Name`, but message `content` on the wire uses:

```text
[[@Display Name:userId]]
```

Example: `@Win Helpers` in the UI is stored as `[[@Win Helpers:100]]` where `100` is the mentioned user's myid.

The plugin and win-helpers skill must understand this format for **inbound mention gating** and **agent-authored outbound mentions**. The plugin does **not** auto-prepend mentions; the agent decides when to mention and writes the wire format in reply text.

---

## 2. Decisions (locked)

| Topic | Decision |
|-------|----------|
| Agent sees inbound body | **Raw wire format** — `BodyForAgent` / `RawBody` unchanged (`[[@Win Helpers:100]] …`) |
| Inbound mention gating | Parse `[[@Name:id]]` in `content`; pass gate when `id === config.userId` (in addition to `mentionedUserIds[]` and `@username` text) |
| Outbound mention source | **Agent-authored** — agent writes `[[@Name:id]]` in reply when needed |
| Plugin outbound prepend | **No** — plugin never injects `[[@…]]` into reply text |
| Outbound RPC | Parse `[[@Name:id]]` from agent reply → set `mentionedUserIds`; send `content` verbatim |
| ID lookup for mentions | **Sender context** (`SenderId`, `SenderName`, new `SenderMention`) + ids from `[[@…]]` in chat history |
| `ListChatGroupMembers` | **Out of scope** — no mcporter `myconversation` server, no member-list RPC in plugin |
| `mentionedUserIds` on multi-chunk send | First chunk only (existing behavior) |

---

## 3. Wire format

### Pattern

```text
[[@DisplayName:userId]]
```

- **Regex:** `\[\[@([^:\]]+):(\d+)\]\]` (global)
- Display name may contain spaces (e.g. `Win Helpers`)
- Display name must not contain `:` or `]`
- Multiple mentions per message are allowed

### Proto fields (`ChatGroupMessageInfo` v1.191.0)

| Field | Use |
|-------|-----|
| `sender_user_id` | Inbound sender; `SenderId` context |
| `sender_username` | Inbound sender display name; `SenderName` context |
| `content` | May contain `[[@…]]` tokens |
| `mentioned_user_ids` | Parallel mention list from UI (may be empty when UI embeds only in `content`) |

---

## 4. Plugin — inbound

### 4.1 New module: `src/mention/format.ts`

```ts
type ParsedMention = { displayName: string; userId: number };

parseMentionsFromContent(content: string): ParsedMention[]
extractMentionedUserIds(content: string): number[]   // deduped
contentMentionsUserId(content: string, userId: number | string): boolean
formatMention(displayName: string, userId: number | string): string  // [[@Name:id]]
```

### 4.2 Update `src/inbound/mention.ts`

In `shouldHandleInboundMessage`, when `requireMention` is true, accept if any of:

1. `mentionedUserIds` contains `config.userId` (existing)
2. `content` matches `@username` text (existing)
3. **`contentMentionsUserId(content, config.userId)`** (new — bracket format)

### 4.3 Update `src/inbound/dispatch.ts`

**WasMentioned** — replace `rawBody.includes("@")` with unified logic:

- `mentionedUserIds` contains bot `userId`, OR
- `contentMentionsUserId(rawBody, account.userId)`, OR
- `matchesUsernameMention(rawBody, account.username)` (export or duplicate check from `mention.ts`)

**Agent context** — add field to `finalizeInboundContext`:

| Field | Value | When |
|-------|-------|------|
| `SenderId` | `String(senderUserId)` | always (existing) |
| `SenderName` | `senderUsername` or `user:{id}` | always (existing) |
| `SenderMention` | `[[@senderUsername:senderUserId]]` | when `senderUserId > 0` and `senderUsername` non-empty after trim |

`BodyForAgent` / `RawBody` remain the raw `message.content` (no normalization).

---

## 5. Plugin — outbound

### 5.1 Parse agent reply before send

In `sendChatGroupReply` / delivery path (`dispatch.ts` deliver callback and any other send sites):

1. `mentionedUserIds = extractMentionedUserIds(text)`
2. Send `content: text` unchanged
3. Pass `mentionedUserIds` to `SendChatGroupMessage` (first chunk only when chunked)

No rewrite, no prepend, no name→id resolution in the plugin.

### 5.2 Agent responsibility

Agent mentions only when notification is needed (e.g. ping the asker). Format:

```text
[[@Alice:42]] Đã check xong, stream đang ON_AIR.
```

Use `SenderMention` from inbound context to mention the person who asked. For others, reuse `[[@Name:id]]` seen in prior messages in the session.

---

## 6. win-helpers skill

### New file: `backend/win-helpers/skills/win-helpers/myconversation-mentions.md`

Contents:

- Explain wire format `[[@DisplayName:userId]]`
- Inbound: tokens in message text identify who was mentioned
- Outbound: agent writes `[[@Name:id]]` only when a ping/notify is needed — not on every reply
- Mention the asker: use `SenderMention` from inbound context (or `SenderName` + `SenderId`)
- Mention someone else: copy `id` from `[[@Name:id]]` in chat history
- Plugin sets `mentionedUserIds` from parsed reply; agent does not set RPC fields

### Updates

| File | Change |
|------|--------|
| `skills/win-helpers/SKILL.md` | Link `myconversation-mentions.md` |
| `workspace/AGENTS.md` | Note mention format + `SenderMention` |
| `workspace/TOOLS.md` | Optional one-line mention format reference |

No helm/mcporter changes.

---

## 7. Testing

### `src/mention/format.test.ts`

| Case | Expected |
|------|----------|
| `[[@Win Helpers:100]] hello` | one mention, id 100 |
| Multiple tokens in one message | all parsed, ids deduped |
| Plain `@Win Helpers` text | no bracket parse (gating may still use `@username` path) |
| Malformed `[[@no-id]]` | ignored |

### `src/inbound/mention.test.ts`

| Case | Expected |
|------|----------|
| `[[@Win Helpers:123]]` in content, empty `mentionedUserIds`, `userId=123` | `shouldHandleInboundMessage` → true |
| `[[@Other:999]]` only, bot `userId=123` | false (mention-only group) |

### `src/outbound/reply.test.ts`

| Case | Expected |
|------|----------|
| `"[[@Alice:42]] done"` | `mentionedUserIds: [42]`, content unchanged |
| `"plain reply"` | `mentionedUserIds: []` |
| Multi-chunk with mention in first chunk | ids only on first RPC |

### `dispatch` (optional unit or integration)

- `SenderMention` populated when sender fields present
- `SenderMention` omitted when `senderUsername` empty

---

## 8. Out of scope

- Plugin auto-prepend of sender mention
- `ListChatGroupMembers` / mcporter `myconversation` server
- Normalizing inbound content for the agent (`@Name` instead of `[[@Name:id]]`)
- Mentioning users whose id is not in `SenderMention` or chat history
- Changes to myconversation backend mention encoding

---

## 9. Release

1. Implement in `openclaw/myconversation`; bump plugin version; publish npm.
2. Update win-helpers skill files in image (no plugin version pin change required for skill-only, but plugin publish should ship with connect `^1.191.0`).
3. win-helpers: bump `myconversationPluginVersion` in `helm/stg/values.yaml` after npm publish.

---

## 10. Manual E2E

1. Staff sends message with UI mention of `@Win Helpers` → content contains `[[@Win Helpers:<botId]]`.
2. Bot receives and responds in mention-only group.
3. Agent reply includes `[[@StaffName:<staffId]]` when ping needed → staff gets mention notification in UI.
4. Agent reply without `[[@…]]` → normal message, no mention notification.
