# onechat-cf-spike (Phase 0)

Independent Cloudflare Workers (workers-rs) spike for gRPC-Web over Fetch.

**Not** production SDK code. Proves:

1. Unary `SendChatGroupMessage` via `tonic-web-wasm-client`
2. Server-stream `StreamChatGroups` (pings + messages)
3. Durable Object **alarm-driven** bounded sessions with persisted `resume_after_message_id`

## Prerequisites

- Rust 1.85+ with `wasm32-unknown-unknown` (`rustup target add wasm32-unknown-unknown`)
- `protoc` on `PATH`
- Node.js + npm (for Wrangler)

## Configure secrets (never commit)

Copy `.dev.vars.example` → `.dev.vars` and fill from repo-root `.env.local`:

```bash
cp .dev.vars.example .dev.vars
# edit .dev.vars
```

## Build / run locally

```bash
cd examples/cf_spike
npm install
npm run check          # cargo check --target wasm32-unknown-unknown
npx wrangler dev
```

## Control API

All routes except `/` require `Authorization: Bearer $CONTROL_TOKEN`.

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | resume id, last session report, alarm |
| POST | `/ensure` | schedule alarm now |
| POST | `/stop` | clear alarm |
| POST | `/unary` | send one group message (`CHANNEL_ID_TEST`) |
| POST | `/session-once` | run one bounded stream session (no reschedule loop) |

Example:

```bash
curl -s -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/status
curl -s -X POST -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/unary
curl -s -X POST -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/session-once
curl -s -X POST -H "Authorization: Bearer $CONTROL_TOKEN" http://127.0.0.1:8787/ensure
```

## Session knobs

| Var | Default | Notes |
|-----|---------|-------|
| `SESSION_SECS` | `120` | Cap per alarm/session; hard max clamped to 14m |
| Idle | 90s | Same as native SDK |

## Go / no-go

See [SPIKE_RESULTS.md](SPIKE_RESULTS.md). **Verdict: GO** (2026-07-17).

Vendored note: `vendor/tonic-web-wasm-client` is upstream 0.9.1 with only
`wasm-streams` bumped to `0.6` for compatibility with `worker` 0.8.x.
