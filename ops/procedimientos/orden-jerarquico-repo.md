# Orden jerárquico de un repo (sin números)

Copia de documentación. El skill que el agente carga en **cualquier** proyecto de Horacio es:

`~/.cursor/skills/orden-jerarquico-repo/`

En el chat del repo a ordenar:

```
Aplica orden jerárquico a este repo
```

Disciplina Johnny Decimal (**área → categoría → ítem**, ~10 × ~10, contenido solo en el tercer nivel) **sin numerar**.

## Checklist

1. Diagnosticar solapes; proponer el árbol; esperar OK (no copiar carpetas de Synergium a ciegas).
2. Snapshot en `main` (sesión + HISTORICO + commit + **push**) **antes** de mover. Tag `pre-orden-arbol-AAAA-MM-DD`.
3. Escribir el registro de cada `git mv`.
4. `git mv`. Actualizar solo enlaces vivos. `MAPA.md` en la raíz.
5. Commit + push del reorg.

Raíz que no se mueve: `README.md`, `AGENTS.md`, `HISTORICO.md`, `sesiones/`.

## Rollback

```bash
git revert --no-edit SHA_DEL_REORG
git push origin main
```

`--force` solo si Horacio lo pide.

Pasada Synergium 2026-08-21: [archivo/REORGANIZACION-2026-08-21.md](../../archivo/REORGANIZACION-2026-08-21.md) · [MAPA.md](../../MAPA.md).
