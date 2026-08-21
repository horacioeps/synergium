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
