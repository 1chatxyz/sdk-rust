# 1Chat Rust SDK

Rust SDK for [1chat.xyz](https://1chat.xyz). Talks to the Envoy gateway over **gRPC-Web** (server-streaming for inbound messages).

Crate name on crates.io: `onechat-sdk`  
Rust library name: `onechat_sdk`

## Install

```toml
[dependencies]
onechat-sdk = "0.1"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
futures-util = "0.3"
```

## Configure

```bash
export API_1CHAT_URL=https://your-envoy-gateway.example
export TENANT_ID=...
export BOT_TOKEN=...
# optional: ONECHAT_USER_ID / ONECHAT_USERNAME
```

`API_1CHAT_URL` is already the Envoy gateway — the SDK does not set up a proxy.

## Quick start

```rust
use futures_util::StreamExt;
use onechat_sdk::{Client, IncomingEvent, SubscribeOptions};

#[tokio::main]
async fn main() -> onechat_sdk::Result<()> {
    let client = Client::from_env()?;
    let mut events = client.subscribe_groups(SubscribeOptions::new()).await?;
    while let Some(event) = events.next().await {
        if let IncomingEvent::GroupMessage(msg) = event? {
            client.set_typing(msg.group_id, true).await?;
            client.reply_group(msg.group_id, format!("echo: {}", msg.text)).await?;
            client.set_typing(msg.group_id, false).await?;
        }
    }
    Ok(())
}
```

### Also supported

- **DMs:** `create_or_get_dm`, `reply_dm(thread_id, other_user_id, text)`, `subscribe_dms`
- **Media:** `reply_group_with_media` / `download_media` (pre-uploaded URLs; no video)
- **Reactions:** `react_group_message` / `react_dm_message`
- **Mentions:** `format_mention` → `[[@Name:id]]`

See [AGENTS.md](AGENTS.md) for the full agent-oriented API map.

## Examples

```bash
cargo run --example echo_bot
cargo run --example send_group_message -- "hello"   # needs CHANNEL_ID_TEST
```

## Develop

Requires [Rust](https://rustup.rs/) 1.85+ (pin: 1.97 via `rust-toolchain.toml`) and [`protoc`](https://grpc.io/docs/protoc-installation/).

```bash
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt
```

## Publish

Merges to `main` trigger crates.io publish via GitHub Actions (`CARGO_REGISTRY_TOKEN` secret). Bump `version` in `Cargo.toml` before releasing a new crate version.
