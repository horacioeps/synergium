#!/usr/bin/env bash
# Apply nexus-input slug + source field + updated front on the VPS.
# Requires: EXPLORE_LABS_SSH_HOST, EXPLORE_LABS_SSH_HORACIO_USER, EXPLORE_LABS_SSH_HORACIO_PASSWORD
# Optional local: SYNERGIUM_FORMS_PB_* to rename via public HTTPS API instead of SSH.
set -euo pipefail

FROM_ID="${FROM_PUBLIC_ID:-0mn7nfs5kqsi8g}"
TO_ID="${TO_PUBLIC_ID:-nexus-input}"
REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

if [[ -n "${SYNERGIUM_FORMS_PB_ADMIN_EMAIL:-}" && -n "${SYNERGIUM_FORMS_PB_ADMIN_PASSWORD:-}" ]]; then
  echo "== rename via public API =="
  export SYNERGIUM_FORMS_PB_URL="${SYNERGIUM_FORMS_PB_URL:-https://forms.synergium.net}"
  python3 "$REPO_ROOT/scripts/synergium_forms_publish.py" rename --from "$FROM_ID" --to "$TO_ID"
fi

if [[ -z "${EXPLORE_LABS_SSH_HOST:-}" || -z "${EXPLORE_LABS_SSH_HORACIO_USER:-}" || -z "${EXPLORE_LABS_SSH_HORACIO_PASSWORD:-}" ]]; then
  echo "Missing EXPLORE_LABS_SSH_HORACIO_* — front/hooks/source field not deployed." >&2
  echo "New URL (after rename+deploy): https://forms.synergium.net/${TO_ID}" >&2
  exit 0
fi

HOST="$EXPLORE_LABS_SSH_HOST"
USER="$EXPLORE_LABS_SSH_HORACIO_USER"
PASS="$EXPLORE_LABS_SSH_HORACIO_PASSWORD"
REMOTE_ROOT="/home/${USER}/synergium-forms"
export SSHPASS="$PASS"
SSH=(sshpass -e ssh -o StrictHostKeyChecking=accept-new)
RSYNC=(sshpass -e rsync -az -e "ssh -o StrictHostKeyChecking=accept-new")

echo "== rsync front + hooks + setup_collections =="
"${RSYNC[@]}" "$REPO_ROOT/forms/deploy/pb_public/" "${USER}@${HOST}:${REMOTE_ROOT}/pb_public/"
"${RSYNC[@]}" "$REPO_ROOT/forms/deploy/pb_hooks/" "${USER}@${HOST}:${REMOTE_ROOT}/pb_hooks/"
"${RSYNC[@]}" "$REPO_ROOT/forms/deploy/scripts/setup_collections.py" "${USER}@${HOST}:${REMOTE_ROOT}/scripts/setup_collections.py"
"${RSYNC[@]}" "$REPO_ROOT/scripts/synergium_forms_publish.py" "${USER}@${HOST}:${REMOTE_ROOT}/scripts/synergium_forms_publish.py"

echo "== add source field + rename public_id + reload pm2 =="
"${SSH[@]}" "${USER}@${HOST}" bash -s <<REMOTE
set -euo pipefail
set -a
source "\$HOME/synergium-forms/.env"
set +a
python3 "\$HOME/synergium-forms/scripts/setup_collections.py"
python3 "\$HOME/synergium-forms/scripts/synergium_forms_publish.py" rename --from '${FROM_ID}' --to '${TO_ID}' || true
# Serve SPA from Apache docroot if used; also keep PB public in sync
if [[ -d /var/www/forms.synergium.net ]]; then
  printf '%s\n' '${PASS}' | sudo -S rsync -a "\$HOME/synergium-forms/pb_public/" /var/www/forms.synergium.net/
fi
pm2 restart synergium-forms || true
REMOTE

echo "OK → https://forms.synergium.net/${TO_ID}"
