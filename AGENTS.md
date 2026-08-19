# Guía para agentes — repo Synergium

**Este es el repo canónico.** Todo lo relacionado con Synergium se crea, modifica y commitea aquí.

## Reglas de oro

| Regla | Descripción |
|-------|-------------|
| **Trabajar aquí** | Web, forms, estrategia, prospectos, comunidad, scripts, chats, sesiones → **este repo** |
| **Vault solo lectura** | Notas fuente en vault Obsidian (SSH). No escribir salvo petición explícita |
| **No duplicar en Obsidian** | No añadir material nuevo Synergium en `generado/web-synergium/` etc. del repo Obsidian |
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

## Vault (Cloud Agents)

Helper en repo Obsidian (solo lectura): `scripts/vault_ssh_ro.sh` — requiere secrets `EXPLORE_LABS_*`. Ver reglas vault en repo Obsidian `.cursor/rules/vault-cloud-ssh.mdc`.

## Repo Obsidian (legacy)

Copias antiguas (pre-2026-08-19): [REFERENCIAS-LEGACY-OBSIDIAN.md](REFERENCIAS-LEGACY-OBSIDIAN.md). Consultar solo si hace falta contexto histórico; no editar allí.

## Workflow

1. Leer `docs/QUE-ES-SYNERGIUM.md` y caso/README relevante
2. Implementar en la carpeta correspondiente
3. Documentar en `docs/HISTORIAL-TRABAJO.md` si es hito relevante
4. Volcado sesión en `chats/` + `sesiones/`
5. `git add` + commit + push a `origin/main`
