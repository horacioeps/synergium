# Opciones de URL legible (sin aplicar aún)

Hoy: `https://forms.synergium.net/0mn7nfs5kqsi8g` (id opaco).

Propuesta: `public_id` legible (slug) en lugar del nanoid. El id interno de PocketBase sigue siendo opaco.

## Opciones para el Community directory EN

| # | URL | Notas |
|---|-----|--------|
| A | `/community-directory` | Clara, larga, SEO-friendly |
| B | `/researcher-match` | Enfoque matching |
| C | `/collaboration-input` | Como pediste; un poco genérica |
| D | `/match` | Corta; puede chocar con futuros forms |
| E | `/directory` | Corta y clara |
| F | `/c/directory` | Prefijo `c/` = campaign/community |
| G | `/en/community-directory` | Deja hueco para `/es/directorio-comunidad` |
| H | Híbrido: slug + corto opaco `/directory-x7k2` | Legible y difícil de adivinar listados |

**Recomendación A–H (obsoleta para Horacio):** no le gustó ninguna.

## Ronda 2 — top / sub (I–P)

Patrón: **`/palabra-top/sub`**. La top es el namespace de todos los forms (ganar, colaborar…); la sub es *este* form. Luego pueden existir `/win/snapshot`, `/collab/brief`, etc. Sesgo de la sub: **input**.

| # | URL | Top | Por qué |
|---|-----|-----|---------|
| I | `/win/input` | win | Ganar; corta y potente |
| J | `/gain/input` | gain | Ganar, tono más institucional |
| K | `/collab/input` | collab | Colaboración explícita |
| L | `/bridge/input` | bridge | Puente LATAM–Europa (on-brand) |
| M | `/rise/input` | rise | Subir / crecer |
| N | `/forge/input` | forge | Forjar alianzas |
| O | `/leap/input` | leap | Salto; acción |
| P | `/nexus/input` | nexus | Nodo de conexión (cerca de Synergium) |

Ejemplos de hermanos futuros: `/win/snapshot`, `/bridge/match`, `/collab/brief`.

**Recomendación ronda 2:** **I** (`/win/input`) si prima el golpe; **L** (`/bridge/input`) si prima el relato Synergium; **K** (`/collab/input`) si quieres que se lea solo.

Forms internos/privados pueden seguir con id opaco.

No se cambia nada en producción hasta que elijas.
