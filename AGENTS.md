# AGENTS.md

Guidance for agents and contributors working on **1Chat SDK** (`onechat_sdk`), a Rust chat SDK for [1chat.xyz](https://1chat.xyz).

Read [`.cursor/rules/1-project-overview.mdc`](.cursor/rules/1-project-overview.mdc) for product scope and [`.cursor/plans/2_roadmap.md`](.cursor/plans/2_roadmap.md) for milestones.

## Start here (integrate a bot)

Required env (see [`.env.example`](.env.example); use `.env.local` locally — do not commit):

| Variable | Role |
|----------|------|
| `API_1CHAT_URL` | Envoy gateway base URL (gRPC-Web). Already the gateway — no proxy. |
| `TENANT_ID` | Sent as `x-tenant-id` |
| `BOT_TOKEN` | Sent as `Authorization: Bearer …` |
| `ONECHAT_USER_ID` | Optional bot user id (self-filter / mention matching) |
| `ONECHAT_USERNAME` | Optional bot username (mention matching) |

```rust
use onechat_sdk::Client;

let client = Client::from_env()?;
// Or: Client::try_new(Config { ... })?
```

**Status:** M0–M5 shipped (groups, DMs, media URLs, reactions). Use this file + `README.md` + `examples/` to integrate without reading the roadmap.

### Minimal listen → reply

```rust
use futures_util::StreamExt;
use onechat_sdk::{Client, IncomingEvent, SubscribeOptions};

let client = Client::from_env()?;
let mut events = client.subscribe_groups(SubscribeOptions::new()).await?;
while let Some(event) = events.next().await {
    if let IncomingEvent::GroupMessage(msg) = event? {
        client.reply_group(msg.group_id, "hello").await?;
    }
}
```

Or use the convenience loop:

```rust
client
    .run_group_bot(|client, msg| async move {
        client.reply_group(msg.group_id, format!("echo: {}", msg.text)).await?;
        Ok(())
    })
    .await?;
```

Live templates:

```bash
cargo run --example echo_bot
cargo run --example send_group_message -- "hello"
# needs CHANNEL_ID_TEST
```

## Public API map

| Area | Methods / types |
|------|-----------------|
| Config | `Config`, `Client::from_env`, `Client::try_new` |
| Groups | `reply_group`, `send_group_text`, `send_group_message`, `reply_group_with_media`, `set_typing` |
| Group stream | `subscribe_groups`, `run_group_bot`, `SubscribeOptions`, `IncomingEvent` |
| DMs | `create_or_get_dm`, `reply_dm`, `send_dm_text`, `set_dm_typing`, `subscribe_dms` |
| Media | `MediaUrls`, `media_urls_from_paths`, `download_media` (max 5×20MB; **no video**) |
| Reactions | `react_group_message`, `react_dm_message` |
| Mentions | `format_mention` → `[[@Name:id]]`, `extract_mentioned_user_ids` |
| Chunking | `chunk_text` / `TEXT_CHUNK_LIMIT` (4000) — applied inside send helpers |

### Mentions

```rust
use onechat_sdk::format_mention;

let text = format!("Hi {}", format_mention("Alice", 42));
client.reply_group(group_id, text).await?;
```

### Media (pre-uploaded URLs)

Multipart myEdge upload is **not** in this crate yet. Pass already-uploaded object paths/URLs:

```rust
use onechat_sdk::{MediaUrls, media_urls_from_paths};

let media = media_urls_from_paths(["https://cdn.example/a.png", "docs/report.pdf"])?;
client.reply_group_with_media(group_id, "see attached", &media).await?;

// Download inbound `api/v1/upload/...` paths with bot auth:
let path = client.download_media(&msg.images[0], "/tmp/onechat-media").await?;
```

### Reactions

```rust
client.react_group_message(msg.id, "👍", false).await?; // add
client.react_dm_message(dm.id, "👍", true).await?;      // remove
```

### Direct messages

```rust
use futures_util::StreamExt;

let thread_id = client.create_or_get_dm(other_user_id).await?;
client.reply_dm(thread_id, other_user_id, "hello").await?;

let mut dms = client.subscribe_dms().await?;
while let Some(event) = dms.next().await {
    if let IncomingEvent::DirectMessage(msg) = event? {
        client
            .reply_dm(msg.thread_id, msg.sender_user_id, "got it")
            .await?;
    }
}
```

### Stream reconnect (built-in)

`subscribe_groups` / `subscribe_dms` reconnect on disconnect, idle (~90s; pings reset idle), and max age (~25m). Resume uses the last message id. Backoff is 2s → 60s. Pings never surface as `IncomingEvent`.

## Repository layout

| Path | Purpose |
|------|---------|
| `src/` | SDK library (`onechat_sdk`) |
| `proto/` | Protobuf sources + vendored `google/api`, `validate` |
| `build.rs` | `tonic-build` client codegen into `OUT_DIR` (`src/pb.rs` includes it) |
| `examples/` | Runnable bot templates |
| `reference/` (gitignored) | Local-only OpenClaw/Hermes samples — do not commit or push |
| `.cursor/plans/2_roadmap.md` | Milestones M0–M7 |
| `.github/workflows/` | CI + crates.io publish |

## GitHub identity

Use the **1chatxyz** account only (not personal accounts such as `tiennv147`):

- Credentials file: `~/.git-credentials-1chatxyz`
- Local: `credential.helper=store --file=$HOME/.git-credentials-1chatxyz`, `user.name=1chatxyz`
- `gh` commands: export `GH_TOKEN` from that file’s GitHub password/token

## Commands (run from repo root)

```bash
cargo fmt
cargo clippy --all-targets -- -D warnings
cargo test
cargo clean -p onechat-sdk && cargo build   # regen protos
```

Requires Rust **1.85+** (toolchain pin: **1.97** via `rust-toolchain.toml`) and [`protoc`](https://grpc.io/docs/protoc-installation/).

## Proto regeneration

When upstream protos change, update files under `proto/` (mirror of `profo/` when provided), then:

```bash
cargo clean -p onechat-sdk && cargo build
```

Keep generated tonic types private; expose only the high-level `Client` API.

## Publishing (crates.io)

- Crate: `onechat-sdk` (lib: `onechat_sdk`)
- Semver: bump `version` in `Cargo.toml` in the releasing PR
- Workflow: [`.github/workflows/publish.yml`](.github/workflows/publish.yml) runs on push to `main` (and `workflow_dispatch`)
- Uses GitHub secret `CARGO_REGISTRY_TOKEN` (never commit it)
- Idempotent: skips `cargo publish` when `https://crates.io/api/v1/crates/onechat-sdk/<version>` already returns 200

## Do / Don’t

- **Do** call the Envoy URL with **gRPC-Web** only.
- **Do** use the public `Client` / `Config` API; keep generated tonic types private.
- **Don’t** invent REST or WebSocket transports.
- **Don’t** commit `.env.local`, `reference/`, or `CARGO_REGISTRY_TOKEN`.
- **Don’t** send `x-user-id` — the gateway injects it from the bot token.
- **Don’t** attach videos in v1.

## Authentication

Headers on every RPC:

- `authorization: Bearer <BOT_TOKEN>`
- `x-tenant-id: <TENANT_ID>`
