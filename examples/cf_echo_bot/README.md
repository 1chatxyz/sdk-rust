# onechat-cf-echo-bot (Phase 3)

Cloudflare Workers Durable Object that echoes group messages using **`onechat-sdk`**
(`Client::run_group_session` + alarm resume).

Standalone package (not a Cargo workspace member) so host `cargo test` / clippy stay focused on the SDK — same layout as `cf_spike`.

## Prerequisites

- Rust 1.85+ with `wasm32-unknown-unknown`
- `protoc` on `PATH` (SDK build script)
- Node.js + npm (Wrangler)

## Configure secrets

```bash
cd examples/cf_echo_bot
cp .dev.vars.example .dev.vars
# fill API_1CHAT_URL, TENANT_ID, BOT_TOKEN, ONECHAT_USER_ID, CONTROL_TOKEN
# optional: ONECHAT_USERNAME
```

`ONECHAT_USER_ID` is **required** so `ignore_self` prevents the bot from echoing its own replies.

## Build / run

```bash
npm install
npm run check          # cargo check --target wasm32-unknown-unknown
npx wrangler dev
```

## Control API

All routes except `/` require `Authorization: Bearer $CONTROL_TOKEN`.

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | resume id, last session report, alarm |
| POST | `/ensure` | schedule alarm now (start / keep listening) |
| POST | `/stop` | clear alarm |
| POST | `/session-once` | one SDK session without the alarm reschedule loop |

```bash
curl -s -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/status
curl -s -X POST -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/ensure
```

Each alarm runs `run_group_session` until idle (~90s) / max age (~14m) / stream end, persists `resume_after_message_id`, then schedules the next alarm.
