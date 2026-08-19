#!/usr/bin/env bash
# Read-only vault access from Cloud Agents (SSH + injected secrets).
#
# Required env/secrets:
#   EXPLORE_LABS_SSH_HOST  # pragma: allowlist secret
#   EXPLORE_LABS_SSH_OBISIDIAN_USER  # pragma: allowlist secret
#   EXPLORE_LABS_SSH_OBSIDIAN_PASSWORD  # pragma: allowlist secret
#   EXPLORE_LABS_OBSIDIAN_VAULT_PATH  # pragma: allowlist secret
# Vault root remote (Obsidian Sync / Headless): $EXPLORE_LABS_OBSIDIAN_VAULT_PATH/Horacio  # pragma: allowlist secret
# Legacy FS (pre-Sync, no usar): $EXPLORE_LABS_OBSIDIAN_VAULT_PATH/Horacio.legacy-pre-sync-20260814  # pragma: allowlist secret
#
# Usage:
#   scripts/vault_ssh_ro.sh ls [relpath]
#   scripts/vault_ssh_ro.sh cat <relpath>
#   scripts/vault_ssh_ro.sh find [find-args...]
#   scripts/vault_ssh_ro.sh count-md
#   scripts/vault_ssh_ro.sh get <relpath> <dest-local>
#   scripts/vault_ssh_ro.sh sh '<remote read-only command>'
#   scripts/vault_ssh_ro.sh root
set -euo pipefail

need() {
  local k="$1"
  if [[ -z "${!k:-}" ]]; then
    echo "Missing secret/env: $k" >&2
    exit 1
  fi
}

need EXPLORE_LABS_SSH_HOST  # pragma: allowlist secret
need EXPLORE_LABS_SSH_OBISIDIAN_USER  # pragma: allowlist secret
need EXPLORE_LABS_SSH_OBSIDIAN_PASSWORD  # pragma: allowlist secret
need EXPLORE_LABS_OBSIDIAN_VAULT_PATH  # pragma: allowlist secret

if ! command -v sshpass >/dev/null 2>&1; then
  echo "Install sshpass first (apt-get install -y sshpass)" >&2
  exit 1
fi

VAULT_ROOT="${EXPLORE_LABS_OBSIDIAN_VAULT_PATH%/}/Horacio"  # pragma: allowlist secret
SSH_USER="$EXPLORE_LABS_SSH_OBISIDIAN_USER"  # pragma: allowlist secret
SSH_HOST="$EXPLORE_LABS_SSH_HOST"  # pragma: allowlist secret
export SSHPASS="$EXPLORE_LABS_SSH_OBSIDIAN_PASSWORD"  # pragma: allowlist secret

ssh_ro() {
  sshpass -e ssh \
    -o StrictHostKeyChecking=accept-new \
    -o ConnectTimeout=20 \
    -o BatchMode=no \
    "${SSH_USER}@${SSH_HOST}" \
    "$@"
}

remote_path() {
  local rel="${1:-.}"
  rel="${rel#/}"
  if [[ "$rel" == "." || -z "$rel" ]]; then
    printf '%s' "$VAULT_ROOT"
  else
    printf '%s/%s' "$VAULT_ROOT" "$rel"
  fi
}

cmd="${1:-}"
shift || true

case "$cmd" in
  ls)
    rp="$(remote_path "${1:-.}")"
    ssh_ro "ls -la $(printf %q "$rp")"
    ;;
  cat)
    [[ $# -ge 1 ]] || { echo "Usage: $0 cat <relpath>" >&2; exit 2; }
    rp="$(remote_path "$1")"
    ssh_ro "test -f $(printf %q "$rp") && cat $(printf %q "$rp")"
    ;;
  find)
    ssh_ro "find $(printf %q "$VAULT_ROOT") $*"
    ;;
  count-md)
    ssh_ro "find $(printf %q "$VAULT_ROOT") -type f -name '*.md' | wc -l"
    ;;
  get)
    [[ $# -ge 2 ]] || { echo "Usage: $0 get <relpath> <dest-local>" >&2; exit 2; }
    rp="$(remote_path "$1")"
    dest="$2"
    mkdir -p "$(dirname "$dest")"
    sshpass -e scp \
      -o StrictHostKeyChecking=accept-new \
      -o ConnectTimeout=20 \
      "${SSH_USER}@${SSH_HOST}:${rp}" "$dest"
    ;;
  sh)
    [[ $# -ge 1 ]] || { echo "Usage: $0 sh '<remote command>'" >&2; exit 2; }
    ssh_ro "VAULT_ROOT=$(printf %q "$VAULT_ROOT"); $*"
    ;;
  root)
    printf '%s\n' "$VAULT_ROOT"
    ;;
  ""|-h|--help|help)
    sed -n '2,20p' "$0"
    ;;
  *)
    echo "Unknown command: $cmd (try help)" >&2
    exit 2
    ;;
esac
