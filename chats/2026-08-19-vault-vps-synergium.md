# Sesión 2026-08-19 — Vault VPS desde repo synergium

## Pedido

Que el repo synergium también acceda a la vault en el VPS cuando sea necesario.

## Hecho

**Repo synergium:**
- `scripts/vault_ssh_ro.sh` — copia del helper SSH solo lectura
- `.cursor/rules/vault-cloud-ssh.mdc` — regla para agentes
- `docs/VAULT-ACCESO.md` — guía de uso y notas Synergium útiles
- Actualizados: README, AGENTS.md, synergium-canonical.mdc

**Repo Obsidian (legacy):**
- `generado/synergium-repo/docs/README.md` — apunta al helper en synergium
- LEGACY-MAPEO: vault_ssh_ro.sh

## Uso

```bash
scripts/vault_ssh_ro.sh count-md
scripts/vault_ssh_ro.sh cat "nota.md"
```

Secrets: `EXPLORE_LABS_SSH_*` (mismos que Cloud Agents Obsidian).
