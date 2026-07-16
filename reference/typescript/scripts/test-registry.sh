#!/usr/bin/env sh
# Verify GitLab npm can pack the plugin (same path as win-helpers init-plugins).
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export BOT_PRIVATE_TOKEN="${BOT_PRIVATE_TOKEN:-${GENJUTSU_BOT_PRIVATE_TOKEN:-}}"

if [ -z "$BOT_PRIVATE_TOKEN" ]; then
  echo "Set GENJUTSU_BOT_PRIVATE_TOKEN (or BOT_PRIVATE_TOKEN) in your shell."
  exit 1
fi

VERSION="${1:-$(node -p "require('$ROOT/package.json').version")}"
PACK_DIR=$(mktemp -d)
trap 'rm -rf "$PACK_DIR"' EXIT

cp "$ROOT/.npmrc" "$PACK_DIR/.npmrc"
export NPM_CONFIG_USERCONFIG="$PACK_DIR/.npmrc"

echo "npm view @marketplace/openclaw-myconversation@${VERSION}"
npm view "@marketplace/openclaw-myconversation@${VERSION}" version

echo "npm pack @marketplace/openclaw-myconversation@${VERSION}"
cd "$PACK_DIR"
npm pack "@marketplace/openclaw-myconversation@${VERSION}"

TGZ=$(ls -1 *.tgz | head -1)
tar -xzf "$TGZ"
test -f package/dist/index.js || {
  echo "ERROR: missing package/dist/index.js in tarball"
  exit 1
}

echo "OK: registry pack for ${VERSION} succeeded ($(basename "$TGZ"))"
