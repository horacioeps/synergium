# Sesión 2026-08-22 — Match #7 expediente + ERP tracking PB

## Usuario (tareas secuenciales)

### TASK 1: Match #7 expediente
- Michelle Viera Romero (EC, U. Guayaquil) ↔ Kinndle Blanco Peña (CR, UNA) — sustainability/One Health
- Carpeta `clientes/matches/michelle-kinndle/` con README, emails-optin-borrador (ES/EN), historial, fichas
- Contactos desde Google Sheet / PB
- Actualizar MATCHES.md y clientes/README.md
- No enviar emails

### TASK 2: ERP-like tracking en PocketBase
- Track step por persona/match, emails enviados, contenido completo
- Colecciones PB + schema JSON + backfill desde historial-contacto + doc

## Agente

### Match #7
- Expediente completo en `clientes/matches/michelle-kinndle/`:
  - README.md (estado Pendiente, `match-2026-007`)
  - ficha-michelle.md, ficha-kinndle.md
  - emails-optin-borrador.md: Michelle **EN**, Kinndle **ES** (both either; working language / get by)
  - historial-contacto.md (log inicial)
- Contactos Sheet: michelle.vierarom@ug.edu.ec (+593986815603), kblanco@una.cr (+50683970508)
- MATCHES.md: enlace expediente + idiomas contacto
- clientes/README.md: fila Match #7
- FLUJO-v0.md: `match-2026-007`

### ERP PocketBase
- Schema: `producto/forms/deploy/schemas/match-tracking.schema.json`
- `setup_collections.py` extendido: colecciones `matches`, `match_participants`, `contact_events`
- `backfill_match_tracking.py`: seed matches #1–#7 (idempotente)
- Doc: `producto/forms/docs/MATCH-ERP-TRACKING.md`
- **Deploy producción ejecutado:**
  - `setup_collections.py` → colecciones creadas en forms.synergium.net
  - `backfill_match_tracking.py` → 7 matches, 14 participants, 24 events

### Manual steps pendientes
- Ninguno crítico: colecciones ya en VPS
- Opcional: enlazar `match_participants.submission` por email con nexus-input
- Al enviar opt-in #7: crear `contact_events` + actualizar steps en PB y historial.md
