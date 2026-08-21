---
name: orden-jerarquico-repo
description: Reorganizes a messy repo into a named three-level tree (area → category → item), Johnny Decimal discipline without numbers. Snapshots main first, logs every git mv for rollback, updates live links and agent paths. Use when Horacio asks to order folders, clasificar por área, reorganizar docs, aplicar orden jerárquico, Johnny Decimal sin números, or to reuse the Synergium folder scheme on another project.
---

# Orden jerárquico de un repo (sin números)

Disciplina de Johnny Decimal (**área → categoría → ítem**, máximo ~10 × ~10, contenido solo en el tercer nivel) **sin numerar**. Nombres de carpeta, no `10-19` ni `12.04`.

Ejemplo aplicado: repo Synergium (`hoy/`, `comunidad/`, `clientes/`, `comercial/`, `producto/`, `ops/`, `archivo/`). Registro de aquella pasada: `REORGANIZACION-2026-08-21.md` en ese repo.

## Disparadores

Horacio dice cosas como: ordena las carpetas, clasifica por área, aplica el orden de Synergium a este repo, Johnny Decimal sin números, mapa jerárquico.

## Convenciones Horacio (no negociar)

Dejar en la **raíz**: `README.md`, `AGENTS.md` (si existe), `HISTORICO.md`, `sesiones/`, y tras la pasada `MAPA.md` + el archivo de rollback. No mover `sesiones/` a archivo: la regla de volcado exige esa carpeta en la raíz.

## Checklist

```
- [ ] 1. Diagnosticar solapes (misma cosa en varias carpetas; tableros en la raíz)
- [ ] 2. Proponer el árbol en chat; esperar OK
- [ ] 3. Snapshot: sesión + HISTORICO + commit + push origin main
- [ ] 4. Anotar SHA de ese commit como punto de rollback
- [ ] 5. Escribir el archivo de registro (plantilla abajo) ANTES de mover
- [ ] 6. git mv (no cp/rm); no dejar stubs en las rutas viejas
- [ ] 7. Actualizar solo enlaces VIVOS (README, AGENTS, rules, scripts, tableros). No reescribir sesiones/chats históricas
- [ ] 8. MAPA.md = índice del árbol (única brújula)
- [ ] 9. Commit + push del reorg; ampliar sesión + HISTORICO
```

## Cómo diseñar el árbol

1. Listar carpetas de primer y segundo nivel + md de la raíz.
2. Agrupar por **área de trabajo** (no por tipo de fichero). Típico: `hoy` (tableros), áreas de negocio, `ops`, `archivo`.
3. Dentro de cada área, **categorías** (cajones). Dentro, **ítems** (un tema, un cliente, un caso).
4. Un ítem tiene un solo sitio. Si hoy vive en dos lados, elige uno y mueve.
5. Código que se despliega (p. ej. `deploy/`) se anida, no se parte.
6. Máximo ~10 áreas y ~10 categorías por área. Si no cabe, las áreas están mal cortadas.

## Snapshot y rollback (obligatorio)

Antes de cualquier `git mv`:

```bash
git rev-parse HEAD   # guardar este SHA en el registro
git push origin main # el snapshot ya tiene que estar en remoto
```

Volver atrás si se rompe algo (solo si Horacio lo pide; es destructivo en local):

```bash
git reset --hard SHA_DEL_SNAPSHOT
git push origin main --force
```

En Horacio **no** hacer `--force` salvo petición explícita. Alternativa segura: `git revert` del commit de reorg, o checkout de ficheros desde el SHA.

## Plantilla del archivo de registro

Crear en la raíz `REORGANIZACION-AAAA-MM-DD.md`:

```markdown
# Reorganización AAAA-MM-DD

- Repo:
- Snapshot (rollback): `SHA`
- Commit del reorg: (rellenar al final)

## Cómo volver

git checkout SHA -- .   # o reset --hard si Horacio lo pide

## git mv (viejo → nuevo)

- `ruta/vieja` → `ruta/nueva`

## Enlaces y scripts tocados

- fichero: qué cambió
```

Cada `git mv` real se añade a esa lista. Si un comando falla, parar y anotar.

## Tras mover

- `MAPA.md` en la raíz con el árbol y una tabla viejo → nuevo.
- Actualizar `AGENTS.md` / `.cursor/rules` que citen rutas.
- Scripts: resolver la raíz del repo con `git rev-parse --show-toplevel` o buscando `.git`, no con `../` contados a mano.
- Históricos (`sesiones/`, `chats/`): dejar las rutas antiguas como relato; el MAPA basta para el presente.

## Qué no hacer

- No numerar (`10-19`, `11.01`).
- No crear una cuarta capa de carpetas “por si acaso”.
- No dejar la raíz llena de tableros (`EMBUDOS.md`, `TODO.md`, …): van a `hoy/tableros/` o equivalente.
- No duplicar un doc en área y en archivo.
