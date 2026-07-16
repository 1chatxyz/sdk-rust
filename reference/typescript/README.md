# openclaw-channel-myconversation

OpenClaw channel plugin that connects to [myconversation](https://gitlab.genjutsu.ai/marketplace/myconversation) Staff Group Chat over gRPC.

Design spec and implementation plan: `docs/superpowers/specs/` and `docs/superpowers/plans/`.

## Install

```bash
pnpm install
pnpm run build
openclaw plugins install . --link
```

Run `pnpm run build` first so `dist/` exists (published package and `--link` both use `./dist/*.js` entrypoints).

**Requires OpenClaw >= 2026.6.5** (`openclaw/plugin-sdk/channel-core`).

## Config

Add this under `channels.myconversation` in `openclaw.json`:

```json5
{
  channels: {
    myconversation: {
      endpoint: "https://gateway01.example.com",
      tenantId: "tenant-abc",
      token: "eyJ...",
      userId: "123456789",
      username: "OpenClaw",
      activeGroupsPolicy: "allowlist",
      groupPolicy: "open",
      groups: {
        "42": { requireMention: true }
      }
    }
  }
}
```

Notes:

- `endpoint` should be **gateway01** (Envoy), not the raw myconversation gRPC listener. Use `https://host` or `host:443` (plain hostname defaults to `https://host:443`). HTTPS endpoints use **grpc-web** automatically; in-cluster `http://…:8080` uses native gRPC.
- Every gRPC call includes `x-tenant-id: <tenantId>` and `authorization: Bearer <token>`.
- Optional `userId` is plugin-local only (self-message drop + mention-by-id).
- Optional `username` enables `@mention` text matching when `requireMention: true` (without relying on `mentioned_user_ids`).
- `activeGroupsPolicy: "allowlist"` means only groups listed in `groups` are active (`"all"` = every group the bot belongs to).
- `groupPolicy` is OpenClaw's sender security for group messages. Use `"open"` when filtering groups via `activeGroupsPolicy` + `groups`.
- Groups default to `requireMention: true` unless explicitly overridden.
- Mention gating supports `mentioned_user_ids` (needs `userId`), `@username` in text (needs `username`), and `[[@DisplayName:userId]]` wire tokens in `content` (needs `userId`).

## Media (images + files)

- Bidirectional: staff attachments are downloaded to a local temp dir and passed to the agent as `MediaPaths`; agent media replies are uploaded via **myEdge multipart** then sent as `images[]` / `files[]` on `SendChatGroupMessage`.
- **Supported:** images and documents. **Not supported (v1):** videos (inbound skipped; outbound skipped with warning).
- **Limits:** max 5 attachments per message; 20MB per file.
- **`userId` is required** for outbound uploads (object key prefix).
- Optional `staticUrl`: public static host for inbound reads (fallback to authenticated gateway fetch).
- Optional `mediaTempDir`: override temp root (default `{os.tmpdir()}/openclaw-myconversation`).

## What the plugin does

- Uses `@genjutsu/myconversation-connect` (Connect RPC) for typed gRPC calls to `genjutsu.myconversation.v1.MyConversation`.
- Connects to **gateway01** (`endpoint`) with `x-tenant-id` + `Authorization: Bearer <token>` on every RPC.
- Opens `StreamChatGroups` on full plugin load and reconnects with `resumeAfterMessageId`.
- Drops self-messages when `userId` is configured (`senderUserId == userId`).
- Applies allowlist and mention gating before emitting inbound events to OpenClaw.
- Uses `SignalChatGroupTyping(true)` for heartbeat typing and `SignalChatGroupTyping(false)` plus `SendChatGroupMessage` for final text replies.
- Splits outbound replies longer than 4000 characters into multiple group messages (same pattern as OpenClaw Telegram) so the server 4096-character limit is never exceeded.

## Mentions

Staff Group Chat UI shows `@Display Name`, but message `content` on the wire uses bracket tokens:

```text
[[@Display Name:userId]]
```

Example: `@Win Helpers` in the UI is stored as `[[@Win Helpers:100]]` where `100` is the mentioned user's myid.

- **Wire format:** `\[\[@DisplayName:userId\]\]` — display name may contain spaces; multiple tokens per message are allowed.
- **Agent inbound body:** `BodyForAgent` / `RawBody` stay raw (no normalization); the agent sees bracket tokens in message text.
- **Inbound gating** (`requireMention: true`): passes when `mentioned_user_ids` contains configured `userId`, when `content` matches `@username`, or when `content` contains a `[[@…:userId]]` token for the bot's `userId`.
- **`SenderMention` context:** when the sender has a user id and display name, inbound dispatch sets `SenderMention` to `[[@senderUsername:senderUserId]]` so the agent can ping the asker without id lookup.
- **Outbound mentions:** agent-authored only — the plugin never auto-preps `[[@…]]` into reply text. Before send, `mentionedUserIds` is extracted (deduped) from bracket tokens in the agent reply; `content` is sent verbatim. On multi-chunk replies, `mentionedUserIds` is set on the first chunk only.

Design spec: `docs/superpowers/specs/2026-06-26-myconversation-mention-format-design.md`.

## Bot setup in myconversation

Create or reuse a myid service user for the bot, then add it to the target group with the existing chat-group API/UI flow. The plugin does not create or manage group membership itself.

At minimum:

1. Configure `tenantId`, `token`, and `endpoint` in OpenClaw (optionally `userId` for mention/self filtering).
2. Add the bot user to the group via `AddChatGroupMember`.
3. Put the group id in `channels.myconversation.groups`.

## Manual E2E with the dev UI

The dev test UI lives in the **myconversation** backend repo at `web/chatgroup-test/`:

```bash
cd ../myconversation/web/chatgroup-test   # adjust path to your checkout
npm install
npm run dev
```

Suggested E2E flow:

1. Start the OpenClaw gateway with this plugin linked in.
2. Open the chat-group test UI.
3. Create or open a test group.
4. Add the bot service user with `AddChatGroupMember`.
5. Send `@OpenClaw hello` in a mention-only group.
6. Verify the UI shows typing, then the bot reply.

## Build

```bash
pnpm install
pnpm test
pnpm run typecheck
pnpm run build   # tsc → dist/ (use build:bundle only for experiments; win-helpers uses tsc)
```

Requires GitLab npm registry auth for `@genjutsu/*` (see `.npmrc`). Locally, export either `BOT_PRIVATE_TOKEN` or `GENJUTSU_BOT_PRIVATE_TOKEN` (`.npmrc` reads `BOT_PRIVATE_TOKEN`; map your local token with `export BOT_PRIVATE_TOKEN="$GENJUTSU_BOT_PRIVATE_TOKEN"`).

Verify registry access (same `npm pack` path as win-helpers `init-plugins`):

```bash
export BOT_PRIVATE_TOKEN="$GENJUTSU_BOT_PRIVATE_TOKEN"
pnpm run test:registry          # current package.json version
pnpm run test:registry 1.0.9    # explicit version
```

## Publish

Same npm-library pattern as `@marketplace/mycommunication` (nautilus): scoped package, `.npmrc` registry + token, `.npmignore`, no `publishConfig` (registry from `@marketplace` scope).

CI: `marketplace/cicd` → `frontend.gitlab-ci.yml`, **`BUILD_PACKAGE: "true"`**. Merge to **main** → `frontend-release` (myops tag). Push **tag** → **`publish-npm`**.

```bash
# after bot tag (or manual tag with v1.0.0 in name)
git push origin <tag>
```

Requires `BOT_PRIVATE_TOKEN` in CI (genjutsu) / `.npmrc`.

win-helpers: pin `myconversationPluginVersion` after publish.

## Status

This is a working scaffold, not a production-complete transport:

- Runtime hook names in `src/runtime.ts` are intentionally tolerant because the exact OpenClaw gateway runtime surface can vary by SDK version.
- Media send/receive is supported for images and documents (not videos in v1); richer envelope mapping and setup UX can be expanded later.
- For a real published plugin, add compatibility metadata, contract tests, and stricter runtime integration against the target OpenClaw version.
