# 1Chat SDK Roadmap — from scaffold to working agent-friendly SDK

## M0 — Foundation

Crate metadata, proto codegen (`build.rs`), `Config` / `Error` / `transport` / `Client` skeleton (gRPC-Web to `API_1CHAT_URL`), CI (fmt/clippy/test), seeded agent docs. No live RPCs.

## M1 — Auth + group send (bot reply path)

Auth on every call; `reply_group` / `send_group_text` → `SendChatGroupMessage`; mention helpers `[[@Name:id]]`; 4000-char chunking; `set_typing`; example.

## M2 — Group listen path + reconnect

`subscribe_groups()` / `run_group_bot` over `StreamChatGroups`:

- Reconnect on disconnect / stream end / error
- Resume via `resume_after_message_id`
- Idle 90s (reset on `ping`), max age ~25m, backoff 2s→60s
- High-level `IncomingEvent`s only; optional `SubscribeOptions`

## M3 — Direct messages

`subscribe_dms` / `reply_dm`; shared reconnect controller.

## M4 — Media

myEdge multipart upload; 5×20MB; inbound download; no video in v1.

## M5 — Reactions

`SetChatGroupMessageReaction` / `SetDirectMessageReaction`.

## M6 — Agent-handoff docs

`AGENTS.md` + README + examples + rustdoc so another agent can integrate from the repo link alone.

## M7 — crates.io publish pipeline

GitHub Actions on merge to `main`: build + `cargo publish` with secret `CARGO_REGISTRY_TOKEN` (idempotent if version exists). Semver bump in the releasing PR.
