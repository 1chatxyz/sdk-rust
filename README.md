# 1Chat Rust SDK

Rust SDK for [1chat.xyz](https://1chat.xyz). Talks to the Envoy gateway over **gRPC-Web** (server-streaming for inbound messages).

Crate name on crates.io: `onechat-sdk`  
Rust library name: `onechat_sdk`

## Install

```toml
[dependencies]
onechat-sdk = "0.1"
```

## Configure

```bash
export API_1CHAT_URL=https://your-envoy-gateway.example
export TENANT_ID=...
export BOT_TOKEN=...
```

`API_1CHAT_URL` is already the Envoy gateway — the SDK does not set up a proxy.

## Quick start (M0)

```rust
use onechat_sdk::{Client, Config};

fn main() -> onechat_sdk::Result<()> {
    let client = Client::from_env()?;
    println!("gateway: {}", client.base_url());
    Ok(())
}
```

Group send (M1), listen with auto-reconnect (M2), and a full agent integration guide (M6) are on the [roadmap](.cursor/plans/2_roadmap.md).

## Develop

Requires [Rust](https://rustup.rs/) 1.85+ and [`protoc`](https://grpc.io/docs/protoc-installation/).

```bash
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt
```

See [AGENTS.md](AGENTS.md) for agent-oriented integration notes.
