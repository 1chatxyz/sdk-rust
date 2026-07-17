# Vendored `tonic-web-wasm-client`

Source: https://github.com/devashishdxt/tonic-web-wasm-client (v0.9.1)

Licenses: MIT / Apache-2.0 (see `LICENSE_MIT`, `LICENSE_APACHE`).

## Local patch

- `Cargo.toml`: `wasm-streams = "0.5"` → `"0.6"` so the crate links cleanly with
  Cloudflare `worker` 0.8.x (which also depends on `wasm-streams` 0.6). Linking
  both 0.5 and 0.6 produces duplicate wasm-bindgen symbols.
