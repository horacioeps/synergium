#!/usr/bin/env bash
# Deploy Synergium Forms from this workspace to the Explore Labs VPS.
set -euo pipefail

HOST="${EXPLORE_LABS_SSH_HOST:?}"
USER="${EXPLORE_LABS_SSH_HORACIO_USER:?}"
PASS="${EXPLORE_LABS_SSH_HORACIO_PASSWORD:?}"
REMOTE_ROOT="/home/${USER}/synergium-forms"
REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${REPO_ROOT}" ]]; then
  REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
fi
# Prefer in-repo deploy; fall back to Obsidian-legacy Cloud Agent layout.
if [[ -d "${REPO_ROOT}/producto/forms/deploy" ]]; then
  DEPLOY_SRC="${REPO_ROOT}/producto/forms/deploy"
  PUBLISH_PY="${REPO_ROOT}/ops/scripts/synergium_forms_publish.py"
  SCHEMA_EN="${REPO_ROOT}/comunidad/formulario/nexus-input/schema-en.json"
elif [[ -d /workspace/generado/synergium-forms/deploy ]]; then
  DEPLOY_SRC=/workspace/generado/synergium-forms/deploy
  PUBLISH_PY=/workspace/scripts/synergium_forms_publish.py
  SCHEMA_EN=/workspace/generado/synergium-forms/casos/community-directory-matching/schema-en.json
else
  DEPLOY_SRC="$(cd "$(dirname "$0")/.." && pwd)"
  PUBLISH_PY="${REPO_ROOT}/ops/scripts/synergium_forms_publish.py"
  SCHEMA_EN="${REPO_ROOT}/comunidad/formulario/nexus-input/schema-en.json"
fi

export SSHPASS="$PASS"
SSH=(sshpass -e ssh -o StrictHostKeyChecking=accept-new)
SCP=(sshpass -e scp -o StrictHostKeyChecking=accept-new)
RSYNC=(sshpass -e rsync -az -e "ssh -o StrictHostKeyChecking=accept-new")

echo "== mkdir remote =="
"${SSH[@]}" "${USER}@${HOST}" "mkdir -p '${REMOTE_ROOT}'/{pb_public,pb_hooks,pb_data,logs,bin,scripts}"

echo "== rsync deploy assets =="
"${RSYNC[@]}" \
  "${DEPLOY_SRC}/pb_public/" "${USER}@${HOST}:${REMOTE_ROOT}/pb_public/"
"${RSYNC[@]}" \
  "${DEPLOY_SRC}/pb_hooks/" "${USER}@${HOST}:${REMOTE_ROOT}/pb_hooks/"
"${RSYNC[@]}" \
  "${DEPLOY_SRC}/scripts/" "${USER}@${HOST}:${REMOTE_ROOT}/scripts/"
"${RSYNC[@]}" \
  "${PUBLISH_PY}" \
  "${USER}@${HOST}:${REMOTE_ROOT}/scripts/synergium_forms_publish.py"
"${SSH[@]}" "${USER}@${HOST}" "mkdir -p '${REMOTE_ROOT}/schemas'"
"${RSYNC[@]}" \
  "${SCHEMA_EN}" \
  "${USER}@${HOST}:${REMOTE_ROOT}/schemas/schema-en.json"

echo "== secrets file on VPS (chmod 600) =="
# Generate admin password if not present remotely
"${SSH[@]}" "${USER}@${HOST}" bash -s <<'REMOTE'
set -euo pipefail
ROOT="$HOME/synergium-forms"
ENVF="$ROOT/.env"
if [[ ! -f "$ENVF" ]]; then
  umask 077
  python3 - <<'PY'
import configparser, pathlib, secrets
c=configparser.ConfigParser()
c.read(str(pathlib.Path.home()/"EmailerX/config/config.test.ini"))
smtp=c["SMTP"]
env=pathlib.Path.home()/"synergium-forms/.env"
admin_pass=secrets.token_urlsafe(21)
def q(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'
lines = [
    f"SYNERGIUM_FORMS_PB_ADMIN_EMAIL={q('forms-admin@synergium.net')}",
    f"SYNERGIUM_FORMS_PB_ADMIN_PASSWORD={q(admin_pass)}",
    f"SYNERGIUM_FORMS_PB_URL={q('http://127.0.0.1:8090')}",
    f"SYNERGIUM_FORMS_NOTIFY_EMAIL={q('horacio@horacio-ps.com')}",
    f"SYNERGIUM_FORMS_SMTP_HOST={q(smtp.get('smtp_host'))}",
    f"SYNERGIUM_FORMS_SMTP_PORT={q(smtp.get('smtp_port','587'))}",
    f"SYNERGIUM_FORMS_SMTP_USER={q(smtp.get('smtp_login'))}",
    f"SYNERGIUM_FORMS_SMTP_PASS={q(smtp.get('smtp_pass'))}",
    f"SYNERGIUM_FORMS_SENDER_ADDRESS={q('horacio@horacio-ps.com')}",
    f"SYNERGIUM_FORMS_SENDER_NAME={q('Synergium Forms')}",
    f"SYNERGIUM_FORMS_SMTP_TLS={q('false')}",
]
env.write_text("\n".join(lines) + "\n")
env.chmod(0o600)
print("wrote", env)
PY
else
  echo "keep existing $ENVF"
fi
REMOTE

echo "== install pocketbase + pm2 =="
"${SSH[@]}" "${USER}@${HOST}" bash -s <<'REMOTE'
set -euo pipefail
set -a
source "$HOME/synergium-forms/.env"
set +a
chmod +x "$HOME/synergium-forms/scripts/install_on_vps.sh"
bash "$HOME/synergium-forms/scripts/install_on_vps.sh"
sleep 2
curl -fsS "http://127.0.0.1:8090/api/health" || curl -fsS "http://127.0.0.1:8090/" >/dev/null || true
python3 "$HOME/synergium-forms/scripts/setup_collections.py"
REMOTE

echo "== apache vhost =="
"${SCP[@]}" "${DEPLOY_SRC}/apache/forms.synergium.net.conf" "${USER}@${HOST}:/tmp/forms.synergium.net.conf"
"${SSH[@]}" "${USER}@${HOST}" bash -s <<REMOTE
set -euo pipefail
printf '%s\n' "$PASS" | sudo -S cp /tmp/forms.synergium.net.conf /etc/apache2/sites-available/forms.synergium.net.conf
printf '%s\n' "$PASS" | sudo -S a2enmod proxy proxy_http rewrite headers ssl >/dev/null
printf '%s\n' "$PASS" | sudo -S a2ensite forms.synergium.net.conf >/dev/null
printf '%s\n' "$PASS" | sudo -S apache2ctl configtest
printf '%s\n' "$PASS" | sudo -S systemctl reload apache2
REMOTE

echo "Deploy done. Next: DNS A forms.synergium.net -> ${HOST} then certbot."
