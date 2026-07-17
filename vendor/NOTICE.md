# Vendored `onechat-tonic-web-wasm-client`

Upstream: https://github.com/devashishdxt/tonic-web-wasm-client (v0.9.1)

Published crate name: `onechat-tonic-web-wasm-client` (lib name remains
`tonic_web_wasm_client`). Licenses: MIT / Apache-2.0 (see `LICENSE_*`).

## Local patch

- `wasm-streams = "0.5"` → `"0.6"` for Cloudflare `worker` 0.8.x (dual 0.5+0.6
  breaks wasm-bindgen linking).
