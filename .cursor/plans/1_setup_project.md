# Setup Project

Status: In progress (M0)

## Dev tooling

- **Rust:** `rust-toolchain.toml` pins `1.85` (+ rustfmt, clippy).
- **protoc:** required on `PATH` for `build.rs` (`tonic-build`). macOS: `brew install protobuf`.
- **Local API testing:** copy `.env.example` → `.env.local` with `API_1CHAT_URL`, `TENANT_ID`, `BOT_TOKEN`. Never commit `.env.local`.

## Commands

```bash
cargo fmt
cargo clippy --all-targets -- -D warnings
cargo test
# Force proto regen:
cargo clean -p onechat-sdk && cargo build
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) on PR + push to `main`:

- Install `protoc`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Release (M7 — not wired in M0)

Using GitHub Actions to build & push to crates.io when a PR is merged to `main`.

- Workflow: `.github/workflows/publish.yml` (added in M7)
- Secret: `CARGO_REGISTRY_TOKEN` (create from local `.env.local`; never commit)
- Releasing PR must bump `Cargo.toml` version (semver)
- Publish is idempotent if that version already exists on crates.io
