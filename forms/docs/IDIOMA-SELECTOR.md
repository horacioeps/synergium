# Selector de idioma (EN / ES) — propuesta

Sí, tiene sentido: el mismo “input” Nexus para LATAM y Europa.

## Recomendación

| Opción | Cómo | Pros | Contras |
|--------|------|------|---------|
| **A (recomendada)** | Un `public_id` (`nexus-input`) + toggle EN/ES que carga `schema-en` / `schema-es` (mismo `field id`) | Un enlace; matching unificado | Hay que mantener dos schemas alineados |
| B | Dos URLs: `nexus-input` y `nexus-input-es` | Simple | Dos enlaces en WhatsApp |
| C | Query `?lang=es` | Fácil compartir | Menos “producto” |

UI: al lado del toggle claro/oscuro, **EN \| ES**. Preferencia en `localStorage`.

## Ahora

Solo existe `schema-en.json`. El toggle se puede pintar ya, pero ES no hasta tener el schema traducido (mismos `id` de campo).

## Decisión pendiente

¿Misma URL con toggle (A) o URL ES separada (B)?
