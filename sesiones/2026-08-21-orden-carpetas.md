# Sesión 2026-08-21 — orden jerárquico de docs y carpetas

## Contexto

Repo Synergium (copia local `horacioeps/synergium`). Horacio percibe docs y carpetas desordenados; pide 3 maneras muy diversas de ganar orden, jerárquicas por área, para encontrar las cosas más fácil.

## Usuario

me d ala impresion que tengot ods los docs y carpetas un poco desordenadas, sugiere 3 maneras muy diversas de ganar en orden p aras i encontrar mas facilmente las cosas, de manera jerarquica por area

## Agente

Revisión de la raíz y de cómo se solapan las carpetas actuales (sin mover nada).

Diagnóstico breve:

- Raíz con 7 md de “tablero” (README, AGENTS, EMBUDOS, MATCHES, TODO, HISTORICO, REFERENCIAS-LEGACY).
- Comercial partido: `estrategia/`, `outreach/`, `prospectos/`.
- Matching partido: `comunidad/`, `clientes/`, `MATCHES.md`, `EMBUDOS.md`.
- Producto partido: `web/`, `web-direcciones/`, `forms/`.
- Docs en 4 sitios: `docs/`, `forms/docs/`, `web/docs/`, `comunidad/docs/`.
- Archivo duplicado: `chats/` + `sesiones/`; `HISTORICO.md` vs `docs/HISTORIAL-TRABAJO.md`.

Tres esquemas propuestos (solo sugerencia, sin reorganizar):

1. Cadena de valor (10–50 + 90): comunidad → clientes → comercial → producto → ops → archivo.
2. Johnny Decimal (10/20/30… con máximo dos niveles y un MAPA.md).
3. Tres capas por frescura (`vivo/` / `sistemas/` / `conocimiento/` / `archivo/`) y raíz mínima.

Recomendación: empezar por 3 (índice + raíz limpia) si no se quiere romper rutas de agentes; pasar a 1 si se acepta un movimiento grande.

No se movió ninguna carpeta en este turno.

---

## Usuario

en la 2, los nuneros que hay, son realmente de johny decimal?

## Agente

No del todo. Lo de la opción 2 era JD *inspirado*: usé 10/20/30 como si fueran áreas y 11/12/21 como categorías, pero Johnny Decimal real es de tres niveles.

- Área = rango `10-19`, no carpeta `10`.
- Categoría = `11`, `12`… (esto sí coincidía).
- El número de verdad es `AC.ID`, p.ej. `12.04`. Ahí vive el contenido; no se guarda en el área ni en la categoría.

Corrección: lo propuesto era numeración jerárquica al estilo JD, no un sistema Johnny Decimal completo. Sin mover ficheros.

---

## Usuario

la idea es buena pero no quiero nuneros, a ver como qedaria

## Agente

Redibujo JD con nombres (área → categoría → ítem). Mismas reglas: ≤10 áreas, ≤10 categorías, contenido solo en el tercer nivel. Árbol propuesto sobre el repo actual; sin mover ficheros hasta que Horacio elija.

---

## Usuario

si, me parece muy buena idea, te pediria que lo hagas todo. y que por otra parte antes subas a main y demas y luego hagas todo esto y tambien que registres en un archvo todo lo que haces por si se rompe ealgo y luego hay que volver hacia atrás

## Agente

Orden pedido: 1) volcado + commit + push + **tag** de restauración **antes** de mover nada. 2) Reorganizar al árbol área/categoría/ítem (sin números). 3) Archivo de registro de cada `git mv` y cómo volver atrás.

Excepción: `sesiones/` y `HISTORICO.md` se quedan en la raíz (contrato del skill guarda-sesion-y-demas y reglas del repo).

**Paso 1 (este commit):** punto de restauración. Tag `pre-orden-arbol-2026-08-21`.
**Paso 2:** movimientos + `archivo/REORG-2026-08-21.md` + actualización de enlaces/reglas/scripts.

---

## Usuario

si, me parece muy buena idea, te pediria que lo hagas todo. y que por otra parte antes subas a main y demas y luego hagas todo esto y tambien que registres en un archvo todo lo que haces por si se rompe ealgo y luego hay que volver hacia atrás

## Usuario (turno siguiente)

y otra cosa, este procedimiento que lo guardes en algun sitio par aluego aplicar este tipo de clasifiacion a otros proyectos

## Agente

Plan acordado:

1. Snapshot en `main` (sesión + HISTORICO + push) **antes** de mover nada. SHA de rollback = ese commit.
2. Skill personal reutilizable `orden-jerarquico-repo` (otros proyectos) + copia en el repo.
3. Archivo de registro/rollback con cada `git mv` y cómo volver atrás.
4. Mover el árbol área → categoría → ítem (sin números). `sesiones/` e `HISTORICO.md` se quedan en la raíz (regla de agentes).
5. Actualizar README, AGENTS, reglas Cursor, scripts, enlaces vivos. Push del reorg.

### Hecho (2026-08-21 ~22:00 CEST)

- Snapshot en `origin/main`: `2fe97c552ee69e5497352c0e7a8aae6613d35d79`. Tag `pre-orden-arbol-2026-08-21`.
- Registro: [REORGANIZACION-2026-08-21.md](../REORGANIZACION-2026-08-21.md) (cada `git mv` + cómo volver).
- Árbol aplicado (área → categoría → ítem). `sesiones/` e `HISTORICO.md` en la raíz.
- Índice: [MAPA.md](../MAPA.md).
- Skill personal `~/.cursor/skills/orden-jerarquico-repo/` + copia `ops/procedimientos/orden-jerarquico-repo.md`. Puntero en `nuevo-proyecto-local`.
- Enlaces vivos, reglas Cursor y scripts de publish/sync/deploy actualizados.

## Agente (ejecución)

1. Snapshot ya en `origin/main`: `2fe97c5`. Tag `pre-orden-arbol-2026-08-21` empujado.
2. `git mv` al árbol área → categoría → ítem (sin números). `sesiones/` + `HISTORICO.md` en la raíz.
3. Registro: [archivo/REORGANIZACION-2026-08-21.md](../archivo/REORGANIZACION-2026-08-21.md). Índice: [MAPA.md](../MAPA.md).
4. Enlaces vivos, reglas Cursor, scripts (sheet-sync, apply_nexus_input, rollbacks WP).
5. Skill `~/.cursor/skills/orden-jerarquico-repo/` + copia `ops/procedimientos/orden-jerarquico-repo.md`.

