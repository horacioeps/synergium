#!/usr/bin/env bash
# Create / refresh Apache basic-auth file for /match-dashboard/ (run on VPS or via deploy).
set -euo pipefail

AUTH_USER="${SYNERGIUM_MATCH_DASHBOARD_USER:-horacio}"
AUTH_PASS="${SYNERGIUM_MATCH_DASHBOARD_PASSWORD:-}"
HTPASSWD="${HOME}/synergium-forms/.htpasswd-match-dashboard"

if [[ -z "$AUTH_PASS" ]]; then
  echo "SYNERGIUM_MATCH_DASHBOARD_PASSWORD not set — skip htpasswd (dashboard will 401 until configured)." >&2
  exit 0
fi

if ! command -v htpasswd >/dev/null 2>&1; then
  echo "Installing apache2-utils for htpasswd…" >&2
  sudo apt-get update -qq && sudo apt-get install -y apache2-utils
fi

mkdir -p "$(dirname "$HTPASSWD")"
htpasswd -bc "$HTPASSWD" "$AUTH_USER" "$AUTH_PASS"
chmod 640 "$HTPASSWD"
echo "Wrote $HTPASSWD for user $AUTH_USER"
