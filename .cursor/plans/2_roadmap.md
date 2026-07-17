# 1Chat SDK Roadmap — from scaffold to working agent-friendly SDK

## M0 — Foundation ✅

Crate metadata, proto codegen (`build.rs`), `Config` / `Error` / `transport` / `Client` skeleton (gRPC-Web to `API_1CHAT_URL`), CI (fmt/clippy/test), seeded agent docs. No live RPCs.

## M1 — Auth + group send (bot reply path) ✅

Auth on every call; `reply_group` / `send_group_text` → `SendChatGroupMessage`; mention helpers `[[@Name:id]]`; 4000-char chunking; `set_typing`; example.

## M2 — Group listen path + reconnect ✅

`subscribe_groups()` / `run_group_bot` over `StreamChatGroups`:

- Reconnect on disconnect / stream end / error
- Resume via `resume_after_message_id`
- Idle 90s (reset on `ping`), max age ~25m, backoff 2s→60s
- High-level `IncomingEvent`s only; optional `SubscribeOptions`

## M3 — Direct messages ✅

`subscribe_dms` / `reply_dm`; shared reconnect controller.

## M4 — Media ✅ (pre-uploaded URLs)

Pre-uploaded URL lists + authenticated download; 5×20MB; no video in v1. myEdge multipart upload deferred (needs separate proto).

## M5 — Reactions ✅

`SetChatGroupMessageReaction` / `SetDirectMessageReaction`.

## M6 — Agent-handoff docs ✅

`AGENTS.md` + README + examples + rustdoc so another agent can integrate from the repo link alone.

## M7 — crates.io publish pipeline ✅

GitHub Actions on merge to `main`: build + `cargo publish` with secret `CARGO_REGISTRY_TOKEN` (idempotent if version exists). Semver bump in the releasing PR.

## M8 — Cloudflare Workers WASM (in progress)

Phase 0 spike **GO** (`examples/cf_spike`, see `SPIKE_RESULTS.md`): unary + `StreamChatGroups` over Fetch, alarm-driven DO sessions, ~282 KiB gzip. Next: target-gated transport in `onechat-sdk`, then `cf_echo_bot` + docs.
