#!/usr/bin/env bash
# Run ON the VPS after DNS A record forms.synergium.net -> 217.154.191.98 exists.
set -euo pipefail
PASS="${EXPLORE_LABS_SSH_HORACIO_PASSWORD:-${SUDO_PASS:-}}"
if [[ -z "$PASS" ]]; then
  echo "Set EXPLORE_LABS_SSH_HORACIO_PASSWORD or SUDO_PASS" >&2
  exit 1
fi

printf '%s\n' "$PASS" | sudo -S rsync -a --delete /home/horacio/synergium-forms/pb_public/ /var/www/forms.synergium.net/
printf '%s\n' "$PASS" | sudo -S chown -R www-data:www-data /var/www/forms.synergium.net

printf '%s\n' "$PASS" | sudo -S certbot --apache -d forms.synergium.net \
  --non-interactive --agree-tos -m horacio@horacio-ps.com --redirect

printf '%s\n' "$PASS" | sudo -S apache2ctl configtest
printf '%s\n' "$PASS" | sudo -S systemctl reload apache2
echo "SSL OK: https://forms.synergium.net/"
