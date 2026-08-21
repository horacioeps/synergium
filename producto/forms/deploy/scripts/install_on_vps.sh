#!/usr/bin/env bash
# Install / update Synergium Forms on the Explore Labs VPS (run ON the VPS as horacio).
set -euo pipefail

ROOT="${HOME}/synergium-forms"
PB_VERSION="${PB_VERSION:-0.39.11}"
ARCH="linux_amd64"
ZIP="pocketbase_${PB_VERSION}_${ARCH}.zip"
URL="https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/${ZIP}"

mkdir -p "$ROOT" "$ROOT/pb_data" "$ROOT/logs" "$ROOT/bin"

if [[ ! -x "$ROOT/bin/pocketbase" ]]; then
  echo "Downloading PocketBase ${PB_VERSION}..."
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/$ZIP" "$URL"
  unzip -o "$tmp/$ZIP" -d "$tmp"
  install -m 0755 "$tmp/pocketbase" "$ROOT/bin/pocketbase"
  rm -rf "$tmp"
fi

# Front + hooks are rsynced from the repo into $ROOT

# Superuser (idempotent)
if [[ -z "${SYNERGIUM_FORMS_PB_ADMIN_EMAIL:-}" || -z "${SYNERGIUM_FORMS_PB_ADMIN_PASSWORD:-}" ]]; then
  echo "Set SYNERGIUM_FORMS_PB_ADMIN_EMAIL and SYNERGIUM_FORMS_PB_ADMIN_PASSWORD" >&2
  exit 1
fi

"$ROOT/bin/pocketbase" superuser upsert \
  "$SYNERGIUM_FORMS_PB_ADMIN_EMAIL" \
  "$SYNERGIUM_FORMS_PB_ADMIN_PASSWORD" \
  --dir "$ROOT/pb_data"

# pm2 process
if ! command -v pm2 >/dev/null; then
  echo "pm2 required" >&2
  exit 1
fi

cd "$ROOT"
pm2 delete synergium-forms >/dev/null 2>&1 || true
pm2 start "$ROOT/bin/pocketbase" \
  --name synergium-forms \
  --cwd "$ROOT" \
  -- serve \
  --http=127.0.0.1:8090 \
  --dir="$ROOT/pb_data" \
  --hooksDir="$ROOT/pb_hooks" \
  --publicDir="$ROOT/pb_public"
pm2 save

echo "PocketBase up on 127.0.0.1:8090"
