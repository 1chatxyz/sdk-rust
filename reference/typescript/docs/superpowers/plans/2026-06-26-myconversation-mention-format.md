# myconversation Mention Wire Format — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Teach the OpenClaw myconversation plugin and win-helpers skill to recognize `[[@DisplayName:userId]]` mention tokens on inbound messages, pass sender mention context to the agent, and set `mentionedUserIds` on outbound replies when the agent includes the same wire format.

**Architecture:** Add a small `src/mention/format.ts` parser shared by inbound gating (`mention.ts`), `WasMentioned` / `SenderMention` in `dispatch.ts`, and outbound send (`reply.ts`). Agent writes `[[@Name:id]]` in replies when a ping is needed; plugin never prepends mentions. win-helpers gets a skill doc describing the format and `SenderMention` context field.

**Tech Stack:** TypeScript, Vitest, `@genjutsu/myconversation-connect` ^1.191.0, OpenClaw channel plugin SDK

**Spec:** `docs/superpowers/specs/2026-06-26-myconversation-mention-format-design.md`

---

## File map

| File | Responsibility |
|------|----------------|
| `src/mention/format.ts` | Parse `[[@Name:id]]`, `formatMention`, `extractMentionedUserIds`, `contentMentionsUserId` |
| `src/mention/format.test.ts` | Unit tests for parser |
| `src/inbound/mention.ts` | Bracket-format gating in `shouldHandleInboundMessage`; export `wasInboundBotMentioned` |
| `src/inbound/mention.test.ts` | Bracket gating cases |
| `src/inbound/dispatch.ts` | `SenderMention`, fix `WasMentioned`, outbound parse via `sendChatGroupReply` |
| `src/outbound/reply.ts` | Auto-extract `mentionedUserIds` from reply text in `sendChatGroupReply` |
| `src/outbound/reply.test.ts` | Outbound parse tests |
| `README.md` | Document mention wire format |
| `package.json` | Bump plugin version (e.g. `1.0.12`) after implementation |
| `win369/sysops/backend/win-helpers/skills/win-helpers/myconversation-mentions.md` | Agent mention guide |
| `win369/sysops/.../SKILL.md`, `AGENTS.md`, `TOOLS.md` | Cross-links |

---

### Task 1: Mention format parser (TDD)

**Files:**
- Create: `src/mention/format.ts`
- Create: `src/mention/format.test.ts`

- [ ] **Step 1: Write failing tests**

Create `src/mention/format.test.ts`:

```typescript
import { describe, expect, it } from "vitest";

import {
  contentMentionsUserId,
  extractMentionedUserIds,
  formatMention,
  parseMentionsFromContent,
} from "./format.js";

describe("parseMentionsFromContent", () => {
  it("parses a single mention with spaces in the display name", () => {
    expect(parseMentionsFromContent("[[@Win Helpers:100]] hello")).toEqual([
      { displayName: "Win Helpers", userId: 100 },
    ]);
  });

  it("parses multiple mentions", () => {
    expect(
      parseMentionsFromContent("[[@Alice:1]] and [[@Bob:2]]"),
    ).toEqual([
      { displayName: "Alice", userId: 1 },
      { displayName: "Bob", userId: 2 },
    ]);
  });

  it("ignores malformed tokens", () => {
    expect(parseMentionsFromContent("[[@no-id]] plain @text")).toEqual([]);
  });
});

describe("extractMentionedUserIds", () => {
  it("returns deduped user ids in encounter order", () => {
    expect(
      extractMentionedUserIds("[[@A:5]] [[@B:7]] [[@A:5]]"),
    ).toEqual([5, 7]);
  });
});

describe("contentMentionsUserId", () => {
  it("matches numeric and string user ids", () => {
    expect(contentMentionsUserId("[[@Win Helpers:100]]", 100)).toBe(true);
    expect(contentMentionsUserId("[[@Win Helpers:100]]", "100")).toBe(true);
    expect(contentMentionsUserId("[[@Other:999]]", 100)).toBe(false);
  });
});

describe("formatMention", () => {
  it("builds wire-format token", () => {
    expect(formatMention("Alice", 42)).toBe("[[@Alice:42]]");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/nemo/go/src/gitlab.genjutsu.ai/marketplace/openclaw/myconversation
pnpm test src/mention/format.test.ts
```

Expected: FAIL — `./format.js` not found.

- [ ] **Step 3: Implement parser**

Create `src/mention/format.ts`:

```typescript
const MENTION_TOKEN_RE = /\[\[@([^:\]]+):(\d+)\]\]/g;

export type ParsedMention = {
  displayName: string;
  userId: number;
};

export function parseMentionsFromContent(content: string): ParsedMention[] {
  if (!content) {
    return [];
  }
  const mentions: ParsedMention[] = [];
  for (const match of content.matchAll(MENTION_TOKEN_RE)) {
    const displayName = match[1]?.trim();
    const userId = Number(match[2]);
    if (!displayName || !Number.isFinite(userId) || userId <= 0) {
      continue;
    }
    mentions.push({ displayName, userId });
  }
  return mentions;
}

export function extractMentionedUserIds(content: string): number[] {
  const seen = new Set<number>();
  const ids: number[] = [];
  for (const mention of parseMentionsFromContent(content)) {
    if (seen.has(mention.userId)) {
      continue;
    }
    seen.add(mention.userId);
    ids.push(mention.userId);
  }
  return ids;
}

export function contentMentionsUserId(
  content: string | undefined,
  userId: number | string | undefined,
): boolean {
  if (!content || userId == null) {
    return false;
  }
  const normalizedUserId = String(userId).trim();
  if (normalizedUserId === "") {
    return false;
  }
  return parseMentionsFromContent(content).some(
    (mention) => String(mention.userId) === normalizedUserId,
  );
}

export function formatMention(
  displayName: string,
  userId: number | string,
): string {
  return `[[@${displayName}:${userId}]]`;
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pnpm test src/mention/format.test.ts
```

Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add src/mention/format.ts src/mention/format.test.ts
git commit -m "feat(mention): add [[@Name:id]] wire-format parser"
```

---

### Task 2: Inbound mention gating

**Files:**
- Modify: `src/inbound/mention.ts`
- Modify: `src/inbound/mention.test.ts`

- [ ] **Step 1: Write failing tests**

Add to `src/inbound/mention.test.ts`:

```typescript
import { wasInboundBotMentioned } from "./mention.js";

// inside describe("shouldHandleInboundMessage"):
  it("accepts [[@DisplayName:userId]] bracket mentions for the bot", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "[[@Win Helpers:123]] please help",
          mentionedUserIds: [],
        },
        config,
        { username: "Win Helpers" },
      ),
    ).toBe(true);
  });

  it("rejects bracket mention of a different user in mention-only group", () => {
    expect(
      shouldHandleInboundMessage(
        {
          groupId: 42,
          senderUserId: 456,
          content: "[[@Alice:999]] please help",
          mentionedUserIds: [],
        },
        config,
        { username: "Win Helpers" },
      ),
    ).toBe(false);
  });

describe("wasInboundBotMentioned", () => {
  const account = {
    userId: "123",
    username: "Win Helpers",
  };

  it("detects mentioned_user_ids", () => {
    expect(
      wasInboundBotMentioned("hello", [123], account, {
        username: "Win Helpers",
      }),
    ).toBe(true);
  });

  it("detects bracket format", () => {
    expect(
      wasInboundBotMentioned("[[@Win Helpers:123]] hi", [], account, {
        username: "Win Helpers",
      }),
    ).toBe(true);
  });

  it("detects @username text", () => {
    expect(
      wasInboundBotMentioned("@Win Helpers hi", [], account, {
        username: "Win Helpers",
      }),
    ).toBe(true);
  });

  it("returns false for unrelated text", () => {
    expect(
      wasInboundBotMentioned("plain hello", [], account, {
        username: "Win Helpers",
      }),
    ).toBe(false);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pnpm test src/inbound/mention.test.ts
```

Expected: FAIL — `wasInboundBotMentioned` not exported; bracket gating test fails.

- [ ] **Step 3: Update `mention.ts`**

Add import at top:

```typescript
import { contentMentionsUserId } from "../mention/format.js";
```

After the `mentionedUserIdsInclude` block inside `shouldHandleInboundMessage` (before `return matchesUsernameMention`), add:

```typescript
  if (
    config.userId != null &&
    contentMentionsUserId(candidate.content, config.userId)
  ) {
    return true;
  }
```

Add new export at bottom of file:

```typescript
export function wasInboundBotMentioned(
  rawBody: string,
  mentionedUserIds: number[],
  config: Pick<MyConversationChannelConfig, "userId" | "username">,
  context: MentionContext = {},
): boolean {
  if (
    config.userId != null &&
    mentionedUserIdsInclude(config.userId, mentionedUserIds)
  ) {
    return true;
  }
  if (
    config.userId != null &&
    contentMentionsUserId(rawBody, config.userId)
  ) {
    return true;
  }
  return matchesUsernameMention(rawBody, context.username ?? config.username);
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pnpm test src/inbound/mention.test.ts
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/inbound/mention.ts src/inbound/mention.test.ts
git commit -m "feat(mention): gate inbound on [[@Name:id]] bracket tokens"
```

---

### Task 3: Dispatch context — `SenderMention` and `WasMentioned`

**Files:**
- Modify: `src/inbound/dispatch.ts`

- [ ] **Step 1: Update imports**

Replace:

```typescript
import { mentionedUserIdsInclude } from "../config.js";
import { shouldHandleInboundMessage } from "./mention.js";
```

With:

```typescript
import { formatMention } from "../mention/format.js";
import { shouldHandleInboundMessage, wasInboundBotMentioned } from "./mention.js";
```

- [ ] **Step 2: Compute `senderMention` and fix `wasMentioned`**

After `const senderName = ...` and `const rawBody = ...`, add:

```typescript
  const senderUserId = asNumber(message.senderUserId);
  const senderUsername = message.senderUsername?.trim() ?? "";
  const senderMention =
    senderUserId > 0 && senderUsername !== ""
      ? formatMention(senderUsername, senderUserId)
      : undefined;
```

Replace the `wasMentioned` block:

```typescript
  const wasMentioned = wasInboundBotMentioned(
    rawBody,
    (message.mentionedUserIds ?? []).map(asNumber),
    account,
    { username: account.username },
  );
```

- [ ] **Step 3: Add `SenderMention` to inbound context**

In `finalizeInboundContext({ ... })`, add after `SenderId`:

```typescript
    ...(senderMention ? { SenderMention: senderMention } : {}),
```

- [ ] **Step 4: Run full test suite**

```bash
pnpm test
pnpm run typecheck
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/inbound/dispatch.ts
git commit -m "feat(mention): expose SenderMention and fix WasMentioned detection"
```

---

### Task 4: Outbound mention extraction (TDD)

**Files:**
- Modify: `src/outbound/reply.ts`
- Modify: `src/outbound/reply.test.ts`

- [ ] **Step 1: Write failing tests**

Add to `src/outbound/reply.test.ts`:

```typescript
import { sendChatGroupReply } from "./reply.js";

describe("sendChatGroupReply", () => {
  it("extracts mentionedUserIds from [[@Name:id]] in reply text", async () => {
    const sendChatGroupMessage = vi.fn().mockResolvedValue(makeMessage(99, "ok"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReply(client, {
      groupId: 16,
      text: "[[@Alice:42]] done",
    });

    expect(sendChatGroupMessage).toHaveBeenCalledWith(
      expect.objectContaining({
        content: "[[@Alice:42]] done",
        mentionedUserIds: [42],
      }),
    );
  });

  it("sends plain text with empty mentionedUserIds", async () => {
    const sendChatGroupMessage = vi.fn().mockResolvedValue(makeMessage(99, "ok"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReply(client, {
      groupId: 16,
      text: "plain reply",
    });

    expect(sendChatGroupMessage).toHaveBeenCalledWith(
      expect.objectContaining({
        content: "plain reply",
        mentionedUserIds: [],
      }),
    );
  });
});

describe("sendChatGroupReplyChunked mention parsing", () => {
  it("extracts mentionedUserIds from bracket tokens on first chunk only", async () => {
    const longPrefix = "[[@Alice:42]] " + "z".repeat(5000);
    const sendChatGroupMessage = vi
      .fn()
      .mockResolvedValueOnce(makeMessage(1, "a"))
      .mockResolvedValueOnce(makeMessage(2, "b"));
    const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

    await sendChatGroupReplyChunked(client, {
      groupId: 16,
      text: longPrefix,
    });

    expect(sendChatGroupMessage.mock.calls[0][0].mentionedUserIds).toEqual([42]);
    expect(sendChatGroupMessage.mock.calls[1][0].mentionedUserIds).toEqual([]);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: FAIL — `mentionedUserIds` not extracted from text.

- [ ] **Step 3: Update `sendChatGroupReply` in `reply.ts`**

Add import:

```typescript
import { extractMentionedUserIds } from "../mention/format.js";
```

Replace `sendChatGroupReply` body:

```typescript
export async function sendChatGroupReply(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
): Promise<SendChatGroupMessageReplyType> {
  const parsedMentionIds = extractMentionedUserIds(params.text);
  const mentionedUserIds =
    params.mentionedUserIds != null && params.mentionedUserIds.length > 0
      ? params.mentionedUserIds
      : parsedMentionIds;

  return client.sendChatGroupMessage({
    groupId: params.groupId,
    content: params.text,
    images: params.images ?? [],
    videos: params.videos ?? [],
    files: params.files ?? [],
    mentionedUserIds,
    clientMessageId: randomUUID(),
  });
}
```

Note: explicit `mentionedUserIds` in params still wins when non-empty (backward compat). Chunked send path passes `mentionedUserIds` only on chunk 0 from existing logic — when agent text contains tokens, first chunk parse applies.

- [ ] **Step 4: Run test to verify it passes**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/outbound/reply.ts src/outbound/reply.test.ts
git commit -m "feat(mention): extract mentionedUserIds from outbound reply text"
```

---

### Task 5: README and version bump

**Files:**
- Modify: `README.md`
- Modify: `package.json`

- [ ] **Step 1: Document mention format in README**

Under the "What the plugin does" section, add a bullet:

```markdown
- Recognizes myconversation mention wire format `[[@DisplayName:userId]]` in message text for inbound gating and outbound `mentionedUserIds`. Inbound context includes `SenderMention` (e.g. `[[@Alice:42]]`) when sender fields are present; the agent may include the same format in replies when a ping is needed.
```

Under Config notes, add:

```markdown
- Mention gating also accepts `[[@<bot display name>:<bot user id>]]` in message `content` when the UI embeds mentions in text instead of `mentioned_user_ids`.
```

- [ ] **Step 2: Bump version**

In `package.json`, change `"version": "1.0.11"` → `"version": "1.0.12"`.

- [ ] **Step 3: Run full verification**

```bash
pnpm test
pnpm run typecheck
pnpm run build
```

Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add README.md package.json
git commit -m "docs: mention wire format; chore: bump to 1.0.12"
```

---

### Task 6: win-helpers skill docs

**Files:**
- Create: `/Users/nemo/go/src/gitlab.nautilusgames.tech/win369/sysops/backend/win-helpers/skills/win-helpers/myconversation-mentions.md`
- Modify: `.../skills/win-helpers/SKILL.md`
- Modify: `.../workspace/AGENTS.md`
- Modify: `.../workspace/TOOLS.md`

- [ ] **Step 1: Create `myconversation-mentions.md`**

```markdown
# Skill: myconversation Mentions

## Wire format

Staff Group Chat stores UI mentions in message text as:

```text
[[@Display Name:userId]]
```

Example: `@Win Helpers` with user id `100` → `[[@Win Helpers:100]]`.

The UI renders `@Display Name`; the wire text keeps the bracket form.

## Inbound

- Read `[[@Name:id]]` tokens in message text to see who was mentioned.
- `SenderId` / `SenderName` identify who sent the message.
- `SenderMention` is the ready-made token for the sender, e.g. `[[@Alice:42]]` — use it when you need to ping the person who asked.

## Outbound

Mention someone **only when a notification/ping is needed** — not on every reply.

When mentioning, include the wire token in your reply text:

```text
[[@Alice:42]] Stream đang ON_AIR.
```

The plugin sets `mentionedUserIds` from your text automatically. Do not prepend mentions unless you intend to notify that person.

### How to get user ids

| Target | Source |
|--------|--------|
| Person who asked | `SenderMention` or `SenderName` + `SenderId` from inbound context |
| Someone else | Copy `id` from `[[@Name:id]]` in earlier messages in the chat |

No `ListChatGroupMembers` lookup is required or available.
```

- [ ] **Step 2: Update `SKILL.md`**

After the `win-livestream` section, add:

```markdown
### myconversation-mentions

Staff Group Chat mention wire format (`[[@Name:id]]`) and when/how the agent should mention users in replies.

Xem chi tiết tại `myconversation-mentions.md`.
```

- [ ] **Step 3: Update `AGENTS.md`**

Under Available Skills, add:

```markdown
- **win-helpers/myconversation-mentions** — Mention wire format `[[@Name:id]]`; use `SenderMention` to ping the asker when needed
```

Under Rules, add:

```markdown
- In Staff Group Chat, mention users with `[[@DisplayName:userId]]` only when a ping/notification is needed; use `SenderMention` from inbound context for the person who asked
```

- [ ] **Step 4: Update `TOOLS.md`**

Under Skills, add:

```markdown
- `win-helpers/myconversation-mentions` — Mention format for Staff Group Chat (`[[@Name:id]]`)
```

- [ ] **Step 5: Commit (win-helpers repo)**

```bash
cd /Users/nemo/go/src/gitlab.nautilusgames.tech/win369/sysops
git add backend/win-helpers/skills/win-helpers/myconversation-mentions.md \
  backend/win-helpers/skills/win-helpers/SKILL.md \
  backend/win-helpers/workspace/AGENTS.md \
  backend/win-helpers/workspace/TOOLS.md
git commit -m "docs(win-helpers): add myconversation mention wire format skill"
```

---

### Task 7: Publish and deploy (manual)

- [ ] **Step 1: Publish plugin npm**

```bash
cd /Users/nemo/go/src/gitlab.genjutsu.ai/marketplace/openclaw/myconversation
git push origin HEAD
# tag per project release process, e.g.:
git tag v1.0.12 && git push origin v1.0.12
```

- [ ] **Step 2: Bump win-helpers helm pin**

In `win369/sysops/backend/win-helpers/helm/stg/values.yaml`, set `myconversationPluginVersion: "1.0.12"`.

- [ ] **Step 3: Manual E2E** (from spec §10)

1. Staff @mentions `@Win Helpers` in UI → bot responds in mention-only group.
2. Agent reply with `[[@StaffName:staffId]]` → staff gets mention notification.
3. Agent reply without `[[@…]]` → normal message, no mention.

---

## Spec coverage checklist

| Spec requirement | Task |
|------------------|------|
| `mention/format.ts` parser | Task 1 |
| Inbound gating on bracket format | Task 2 |
| `SenderMention` + fix `WasMentioned` | Task 3 |
| Outbound parse → `mentionedUserIds` | Task 4 |
| No plugin prepend | Tasks 3–4 (no prepend code) |
| win-helpers skill docs | Task 6 |
| Tests | Tasks 1, 2, 4 |
| README + version | Task 5 |
| Release / E2E | Task 7 |
