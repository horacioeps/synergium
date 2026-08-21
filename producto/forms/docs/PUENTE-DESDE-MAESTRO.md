# Puente desde el workspace maestro (repo maestro)

Últimas implementaciones de Forms hechas desde el repo maestro; a partir de ahora el canónico es **este** repo (`synergium` → `producto/forms/` + `comunidad/formulario/`).

| Qué | Dónde trackear |
|-----|----------------|
| Sesión completa (volcado) | Repo maestro: `chats/2026-08-18-synergium-forms-arquitectura.md` |
| Resumen sesión | Repo maestro: `sesiones/2026-08-18-synergium-forms-arquitectura.md` |
| HISTORICO maestro | filas 2026-08-18 / 2026-08-20 Synergium Forms |
| Código/docs canónicos | **Aquí:** `producto/forms/` + `comunidad/formulario/nexus-input/` |
| Legacy mirror (no ampliar) | maestro `generado/synergium-forms/` (banner LEGACY) |

## Hitos vivos

- URL EN: https://forms.synergium.net/nexus-input
- HTTPS + DNS OK (2026-08-20)
- Estilo alineado a synergium.net (Manrope, Crepúsculo `#131313` / `#4B52FF`) — 2026-08-20
- URL legible: **nexus-input** (elegida); apply con `producto/forms/deploy/scripts/apply_nexus_input.sh`
- Google Sheet ↔ BD: cron 15 min pendiente (`GOOGLE-SHEET-SYNC.md`); columna `source` web|google
- Idioma: propuesta en `IDIOMA-SELECTOR.md`

Trabajo futuro de Forms: **solo en este repo**.
