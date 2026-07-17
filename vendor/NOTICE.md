# Vendored `tonic-web-wasm-client`

Source: https://github.com/devashishdxt/tonic-web-wasm-client (v0.9.1)

Licenses: MIT / Apache-2.0 (see `tonic-web-wasm-client/LICENSE_*`).

## Local patch

- `Cargo.toml`: `wasm-streams = "0.5"` → `"0.6"` for compatibility with
  Cloudflare `worker` 0.8.x (duplicate 0.5+0.6 breaks wasm-bindgen linking).
