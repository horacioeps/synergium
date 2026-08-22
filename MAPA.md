# Mapa del repo

Árbol **área → categoría → ítem** (disciplina Johnny Decimal, sin números). Índice vivo: si no sabes dónde va algo, empieza aquí.

Raíz: `README.md`, `AGENTS.md`, `MAPA.md`, `HISTORICO.md`, `sesiones/` (volcado de agentes; no se mueve).

Rollback de esta pasada: [archivo/REORGANIZACION-2026-08-21.md](archivo/REORGANIZACION-2026-08-21.md) · tag git `pre-orden-arbol-2026-08-21` (SHA `2fe97c5`).

```text
hoy/tableros/          EMBUDOS, MATCHES, TODO
comunidad/
  formulario/nexus-input
  formulario/match-align   fase 2 alineación (post-match)
  matching/            top3, top4
  casos/               formulario-agosto-2026, engagement-julio-2026
clientes/
  piloto/matias-rodriguez-rivas
  matches/             ferran-elena, causa-yen-na, …
comercial/
  estrategia/
  prospectos/buscador-v1
  outreach/tec-monterrey
producto/
  web/synergium-net    casos + docs
  web/backups
  web/mockups
  forms/deploy         código vivo PocketBase
  forms/docs
ops/
  scripts/             vault_ssh, publish, sheet-sync
  infra/               infraestructura, vault-acceso
  que-es/              synergium, rol-consultor, nuevo-proyecto-local
  procedimientos/      cómo repetir este orden en otro repo
archivo/
  chats/
  historial-trabajo.md
  legacy-obsidian.md
  REORGANIZACION-2026-08-21.md
sesiones/              (raíz; contrato de agentes)
```

Procedimiento para repetir esto en otro repo: en ese chat, `Aplica orden jerárquico a este repo`. Skill `orden-jerarquico-repo` (`~/.cursor/skills/orden-jerarquico-repo/`) y copia [ops/procedimientos/orden-jerarquico-repo.md](ops/procedimientos/orden-jerarquico-repo.md).

## Dónde va lo de esta semana

| Buscas | Sitio |
|--------|--------|
| Embudo / match / tarea abierta | [hoy/tableros/](hoy/tableros/) |
| Schema y auditoría nexus-input | [comunidad/formulario/nexus-input/](comunidad/formulario/nexus-input/) |
| Expediente de un investigador | [clientes/](clientes/) |
| Deploy PocketBase | [producto/forms/deploy/](producto/forms/deploy/) |
| Cambio synergium.net | [producto/web/synergium-net/casos/](producto/web/synergium-net/casos/) |
| Vault SSH | [ops/scripts/vault_ssh_ro.sh](ops/scripts/vault_ssh_ro.sh) |
| Qué es Synergium | [ops/que-es/synergium.md](ops/que-es/synergium.md) |
