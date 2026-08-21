# Guía para agentes — repo Synergium

**Este es el repo canónico.** Todo lo relacionado con Synergium se crea, modifica y commitea aquí.

Índice de carpetas: **[MAPA.md](MAPA.md)**.

## Reglas de oro

| Regla | Descripción |
|-------|-------------|
| **Trabajar aquí** | Web, forms, estrategia, prospectos, comunidad, scripts, chats, sesiones → **este repo** |
| **Vault solo lectura** | Notas fuente en vault del VPS (SSH). Leer cuando haga falta; no escribir salvo petición explícita |
| **No duplicar en Obsidian** | No añadir material nuevo Synergium en carpetas legacy del repo Obsidian |
| **Rama main** | Trabajar en `main`; commit + push tras cada avance material |
| **Copia local** | Este workspace es el clone de `horacioeps/synergium`. Tras cada interacción, subir a `origin/main` **también** los ficheros que Horacio haya modificado a mano. Regla: `.cursor/rules/local-clone-siempre-push.mdc` |
| **Otro repo** | Frase de arranque (skill personal `nuevo-proyecto-local`): ver [ops/que-es/nuevo-proyecto-local.md](ops/que-es/nuevo-proyecto-local.md) |
| **Forms idiomas** | Selector = synergium.net en **todos** los forms; default EN. Regla: `.cursor/rules/forms-idioma-selector.mdc` |

## Dónde escribir

| Tarea | Carpeta |
|-------|---------|
| Tableros de esta semana | `hoy/tableros/` |
| Cambios synergium.net | `producto/web/synergium-net/casos/<fecha-tema>/` |
| Forms / PocketBase (deploy) | `producto/forms/` |
| Schema / i18n nexus-input | `comunidad/formulario/nexus-input/` |
| Estrategia comercial | `comercial/estrategia/` |
| Buscador prospectos | `comercial/prospectos/buscador-v1/` |
| Comunidad / matching | `comunidad/` |
| Expedientes investigadores | `clientes/piloto/` o `clientes/matches/` |
| Outreach | `comercial/outreach/` |
| Scripts operativos | `ops/scripts/` |
| Qué es / infra / vault | `ops/que-es/`, `ops/infra/` |

## Vault en el VPS (Cloud Agents)

Cuando necesites contexto de notas que no están en git:

```bash
ops/scripts/vault_ssh_ro.sh cat "ruta/relativa/nota.md"
ops/scripts/vault_ssh_ro.sh ls Inbox
ops/scripts/vault_ssh_ro.sh count-md
```

- **Secrets:** `EXPLORE_LABS_SSH_*` (inyectados en Cloud Agents).
- **Regla:** `.cursor/rules/vault-cloud-ssh.mdc`
- **Guía:** [ops/infra/vault-acceso.md](ops/infra/vault-acceso.md)

## Repo Obsidian (legacy)

Copias antiguas (pre-2026-08-19): [archivo/legacy-obsidian.md](archivo/legacy-obsidian.md). Consultar solo si hace falta contexto histórico; no editar allí.

## Workflow

1. Leer [ops/que-es/synergium.md](ops/que-es/synergium.md) y [MAPA.md](MAPA.md)
2. Si falta contexto → vault vía `ops/scripts/vault_ssh_ro.sh`
3. Implementar en la carpeta del mapa
4. Documentar en [archivo/historial-trabajo.md](archivo/historial-trabajo.md) si es hito relevante
5. Volcado sesión en `sesiones/` (y `archivo/chats/` si aplica)
6. `git add` + commit + push a `origin/main`
