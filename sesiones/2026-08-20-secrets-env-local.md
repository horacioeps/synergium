# Sesión 2026-08-20 — secrets.env local Cursor

## Pedido

Horacio mostró captura de secrets del dashboard de Cloud Agents (disponibles allí, no en el agente local IDE). Pidió un fichero tipo `.env` (o similar) que sirva para **todos** los proyectos locales de Cursor IDE, con valores vacíos para rellenarlos a pelo.

Secrets listados en la captura:

- `API_KEY_OPEN_AI`
- `EXPLORE_LABS_OBSIDIAN_VAULT_PATH`
- `EXPLORE_LABS_PODCAST_USER`
- `EXPLORE_LABS_PODCAST_USER_PASSWORD`
- `EXPLORE_LABS_SSH_HORACIO_PASSWORD`
- `EXPLORE_LABS_SSH_HORACIO_USER`
- `EXPLORE_LABS_SSH_HOST`
- `EXPLORE_LABS_SSH_OBISIDIAN_USER`
- `EXPLORE_LABS_SSH_OBSIDIAN_PASSWORD`
- `GITHUB_HORACIO_EPS_GMAIL_COM_TOKEN…` (truncado en UI)

## Hecho

1. Creado **`~/.cursor/secrets.env`** (fuera de repos, `chmod 600`) con esas claves vacías.
2. Carga automática en **`~/.zshrc`** (`set -a; source …; set +a`).
3. Regla usuario always-apply: **`~/.cursor/rules/local-secrets.mdc`**.
4. Nota en `docs/VAULT-ACCESO.md` (ruta local vs Cloud Agents).

No se sube `secrets.env` a git (vive en home).

## Turno 2 — comprobar secrets rellenados

**Pedido:** comprobar si `~/.cursor/secrets.env` funciona y es legible.

**Hecho:**
- Fichero UTF-8 legible; 10/10 claves con valor.
- Fallo de formato: espacio tras `=` → `source` no exportaba y el shell interpretaba valores como comandos.
- Corregido: valores entre comillas simples, sin espacio tras `=`.
- `EXPLORE_LABS_OBSIDIAN_VAULT_PATH` ajustado a padre `/home/obsidian` (el script añade `/Horacio`).
- Prueba funcional: SSH OK; `vault_ssh_ro.sh root` → `/home/obsidian/Horacio`; `count-md` → 8192; `ls Inbox` OK.
- Aviso: en el primer intento fallido salieron valores en stderr del shell → rotar OpenAI + GitHub token.

