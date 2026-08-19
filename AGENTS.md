# Guía para agentes — repo Synergium

**Este es el repo canónico.** Todo lo relacionado con Synergium se crea, modifica y commitea aquí.

## Reglas de oro

| Regla | Descripción |
|-------|-------------|
| **Trabajar aquí** | Web, forms, estrategia, prospectos, comunidad, scripts, chats, sesiones → **este repo** |
| **Vault solo lectura** | Notas fuente en vault del VPS (SSH). Leer cuando haga falta; no escribir salvo petición explícita |
| **No duplicar en Obsidian** | No añadir material nuevo Synergium en carpetas legacy del repo Obsidian |
| **Rama main** | Trabajar en `main`; commit + push tras cada avance material |
| **Sesiones** | Volcado completo en `chats/` y `sesiones/`; actualizar índices |

## Dónde escribir

| Tarea | Carpeta |
|-------|---------|
| Cambios synergium.net | `web/casos/<fecha-tema>/` |
| Forms / PocketBase | `forms/` |
| Estrategia comercial | `estrategia/` |
| Buscador prospectos | `prospectos/` + `prospectos/scripts/` |
| Comunidad / matching | `comunidad/` |
| Outreach | `outreach/` |
| Scripts operativos | `scripts/` |
| Documentación | `docs/` |

## Vault en el VPS (Cloud Agents)

Cuando necesites contexto de notas que no están en git:

```bash
scripts/vault_ssh_ro.sh cat "ruta/relativa/nota.md"
scripts/vault_ssh_ro.sh ls Inbox
scripts/vault_ssh_ro.sh count-md
```

- **Secrets:** `EXPLORE_LABS_SSH_*` (inyectados en Cloud Agents).
- **Regla:** `.cursor/rules/vault-cloud-ssh.mdc`
- **Guía:** [docs/VAULT-ACCESO.md](docs/VAULT-ACCESO.md)

## Repo Obsidian (legacy)

Copias antiguas (pre-2026-08-19): [REFERENCIAS-LEGACY-OBSIDIAN.md](REFERENCIAS-LEGACY-OBSIDIAN.md). Consultar solo si hace falta contexto histórico; no editar allí.

## Workflow

1. Leer `docs/QUE-ES-SYNERGIUM.md` y caso/README relevante
2. Si falta contexto → vault vía `scripts/vault_ssh_ro.sh`
3. Implementar en la carpeta correspondiente
4. Documentar en `docs/HISTORIAL-TRABAJO.md` si es hito relevante
5. Volcado sesión en `chats/` + `sesiones/`
6. `git add` + commit + push a `origin/main`
