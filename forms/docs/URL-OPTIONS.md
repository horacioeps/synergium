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

**Recomendación:** **G** si habrá ES pronto; si no, **A** o **E**.  
Forms internos/privados pueden seguir con id opaco.

No se cambia nada en producción hasta que elijas.
