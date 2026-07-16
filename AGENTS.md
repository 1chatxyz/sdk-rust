# AGENTS.md

Guidance for agents and contributors working on **1Chat SDK** (`onechat_sdk`), a Rust chat SDK for [1chat.xyz](https://1chat.xyz).

Read [`.cursor/rules/1-project-overview.mdc`](.cursor/rules/1-project-overview.mdc) for product scope and [`.cursor/plans/2_roadmap.md`](.cursor/plans/2_roadmap.md) for milestones.

## Start here (integrate a bot)

Required env (see `.env.example`; use `.env.local` locally — do not commit):

| Variable | Role |
|----------|------|
| `API_1CHAT_URL` | Envoy gateway base URL (gRPC-Web). Already the gateway — no proxy. |
| `TENANT_ID` | Sent as `x-tenant-id` |
| `BOT_TOKEN` | Sent as `Authorization: Bearer …` |

```rust
use onechat_sdk::{Client, Config};

let client = Client::try_new(Config {
    api_url: std::env::var("API_1CHAT_URL")?,
    tenant_id: std::env::var("TENANT_ID")?,
    bot_token: std::env::var("BOT_TOKEN")?,
    user_id: None,
    username: None,
})?;
// Or: Client::from_env()?
```

**Milestone status:** M0 = construct client + transport only.  
- **M1:** `reply_group` / typing  
- **M2:** `subscribe_groups` with reconnect (listen → reply)  
- **M6:** full agent-handoff docs + copyable examples  

Target listen→reply shape (M2+):

```rust
let mut events = client.subscribe_groups().await?;
while let Some(event) = events.next().await { /* reply_group */ }
```

## Repository layout

| Path | Purpose |
|------|---------|
| `src/` | SDK library (`onechat_sdk`) |
| `proto/` | Protobuf sources + vendored `google/api`, `validate` |
| `build.rs` | `tonic-build` client codegen into `OUT_DIR` (`src/pb.rs` includes it) |
| `reference/typescript` | OpenClaw-oriented reference |
| `reference/python` | Hermes-oriented reference |
| `.cursor/plans/2_roadmap.md` | Milestones M0–M7 |

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

## Do / Don’t

- **Do** call the Envoy URL with **gRPC-Web** only.
- **Do** use the public `Client` / `Config` API; keep generated tonic types private.
- **Don’t** invent REST or WebSocket transports.
- **Don’t** commit `.env.local` or `CARGO_REGISTRY_TOKEN`.
- **Don’t** send `x-user-id` — the gateway injects it from the bot token.

## Authentication

Headers on every RPC:

- `authorization: Bearer <BOT_TOKEN>`
- `x-tenant-id: <TENANT_ID>`
