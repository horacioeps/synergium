# Reorganización 2026-08-21 — árbol jerárquico (sin números)

Registro de **todo** lo movido, para poder volver atrás.

- **Repo:** `horacioeps/synergium`
- **Tag de rollback:** `pre-orden-arbol-2026-08-21`
- **Snapshot (SHA):** `2fe97c552ee69e5497352c0e7a8aae6613d35d79`  
  Commit: `docs: snapshot antes de reorganizar carpetas (punto de rollback)`  
  En `origin/main` y en GitHub: https://github.com/horacioeps/synergium/commit/2fe97c552ee69e5497352c0e7a8aae6613d35d79
- **Mapa vivo:** [MAPA.md](../MAPA.md)
- **Procedimiento reutilizable:** skill `~/.cursor/skills/orden-jerarquico-repo/` + [ops/procedimientos/orden-jerarquico-repo.md](../ops/procedimientos/orden-jerarquico-repo.md)

`sesiones/` e `HISTORICO.md` **no se movieron** (contrato de agentes).

## Cómo volver atrás

Si el árbol nuevo rompe algo y Horacio pide deshacer:

```bash
# Ver el snapshot
git log --oneline --decorate pre-orden-arbol-2026-08-21 -1

# Opción segura (no reescribe GitHub): revertir el commit del reorg
git revert --no-edit SHA_DEL_REORG
git push origin main

# Opción local: recuperar ficheros del tag
git checkout pre-orden-arbol-2026-08-21 -- .

# Opción destructiva (SOLO si Horacio lo autoriza explícitamente):
# git reset --hard pre-orden-arbol-2026-08-21
# git push origin main --force
```

## git mv (viejo → nuevo)

### Tableros

- `EMBUDOS.md` → `hoy/tableros/EMBUDOS.md`
- `MATCHES.md` → `hoy/tableros/MATCHES.md`
- `TODO.md` → `hoy/tableros/TODO.md`

### Comunidad

- `forms/casos/community-directory-matching` → `comunidad/formulario/nexus-input`
- `comunidad/matching/2026-08-21-top3-nexus-input.md` → `comunidad/matching/top3.md`
- `comunidad/matching/2026-08-21-top4-nexus-input.md` → `comunidad/matching/top4.md`
- `comunidad/casos/2026-08-14-formulario-matching` → `comunidad/casos/formulario-agosto-2026`
- `comunidad/casos/analisis-engagement-2026-07` → `comunidad/casos/engagement-julio-2026`
- `comunidad/docs/README.md` → `comunidad/README.md`

### Clientes

- `clientes/matias-rodriguez-rivas` → `clientes/piloto/matias-rodriguez-rivas`
- `clientes/match-02-ferran-elena` → `clientes/matches/ferran-elena`
- `clientes/match-03-causa-yen-na` → `clientes/matches/causa-yen-na`
- `clientes/match-04-driselda-tatiana` → `clientes/matches/driselda-tatiana`
- `clientes/match-05-erdogan-antonio` → `clientes/matches/erdogan-antonio`
- `clientes/match-06-karen-veronica` → `clientes/matches/karen-veronica`

### Comercial

- `estrategia/` → `comercial/estrategia/`
- `prospectos/` → `comercial/prospectos/buscador-v1/`
- `outreach/tec_monterrey_doctorandos` → `comercial/outreach/tec-monterrey`

### Producto

- `web/casos` → `producto/web/synergium-net/casos`
- `web/docs` → `producto/web/synergium-net/docs`
- `web/wp-backups` → `producto/web/backups`
- `web-direcciones` → `producto/web/mockups`
- `forms/deploy` → `producto/forms/deploy`
- `forms/docs` → `producto/forms/docs`

### Ops

- `scripts/` → `ops/scripts/`
- `docs/INFRAESTRUCTURA.md` → `ops/infra/infraestructura.md`
- `docs/VAULT-ACCESO.md` → `ops/infra/vault-acceso.md`
- `docs/QUE-ES-SYNERGIUM.md` → `ops/que-es/synergium.md`
- `docs/rol-consultor-negocio.md` → `ops/que-es/rol-consultor.md`
- `docs/NUEVO-PROYECTO-LOCAL.md` → `ops/que-es/nuevo-proyecto-local.md`

### Archivo

- `chats/` → `archivo/chats/`
- `REFERENCIAS-LEGACY-OBSIDIAN.md` → `archivo/legacy-obsidian.md`
- `docs/HISTORIAL-TRABAJO.md` → `archivo/historial-trabajo.md`

## Enlaces y scripts tocados (vivos)

No se reescribieron `sesiones/` históricas.

- `README.md`, `AGENTS.md`, `MAPA.md`
- `.cursor/rules/forms-idioma-selector.mdc`, `vault-cloud-ssh.mdc`, `synergium-canonical.mdc`, `local-clone-siempre-push.mdc`
- `ops/scripts/synergium_forms_sheet_sync.py` (raíz via `.git`; schema en `comunidad/formulario/nexus-input/`)
- `producto/forms/deploy/scripts/apply_nexus_input.sh`, `deploy_from_agent.sh`
- `producto/web/synergium-net/casos/*/apply.py` y `rollback.py` (ruta `producto/web/backups`)
- Tableros `hoy/tableros/*`, `clientes/README.md`, README de matches, `comunidad/README.md`
- Docs ops/forms/archivo vivos (infra, vault, qué-es, historial, legacy)
- Skill `~/.cursor/skills/orden-jerarquico-repo/` + `ops/procedimientos/orden-jerarquico-repo.md`
