# Phase 0 spike results — GO

Date: 2026-07-17 (local wrangler dev against live Envoy)

## Checklist

| Check | Result |
|-------|--------|
| Unary `SendChatGroupMessage` | PASS (`message_id=3590`, `3591`) |
| Stream pings | PASS (13 pings / 60s session) |
| Stream messages + resume id | PASS (`messages_seen=1`, `resume_after_message_id=3591`) |
| Alarm `/ensure` + `/stop` | PASS |
| `Credentials::Omit` | PASS (no SameOrigin fork) |
| Gzip Worker upload size | **282.27 KiB** (`wrangler deploy --dry-run`) |
| Free-tier 3 MB limit | PASS (well under) |

## Build notes

- `tonic` **0.14** + `tonic-web-wasm-client` (vendored): bumped `wasm-streams` **0.5 → 0.6** to match `worker` 0.8.5 (dual versions break wasm-bindgen link).
- Do **not** set `strip = true` in release profile until worker-build/wasm-bindgen fix lands (externref / catch wrappers).
- Standalone package under `examples/cf_spike` (not a workspace member) so host `cargo test` / clippy stay unchanged.

## Verdict

**GO** for Phase 1 (target-gated transport in `onechat-sdk`).
