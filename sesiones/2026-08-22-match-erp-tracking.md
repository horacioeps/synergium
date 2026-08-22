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

---

## Ampliación — campos emparejamiento (v2)

### Usuario
- Columna ERP: ¿emparejado ya? + cómo/when propuesto
- Campos en `matches` y `match_participants`; backfill #1–#7; doc; commit+push

### Agente
- Schema v2: `pairing_status`, `pairing_method`, `proposed_at`, `paired_at` en `matches`
- `is_paired`, `paired_with_email`, `pairing_proposed_at` en `match_participants`
- `setup_collections.py`: merge de campos faltantes en colecciones existentes
- `backfill_match_tracking.py`: seed pairing para #1–#7 (`curated_manual`, proposed_at 2026-08-21)
- MATCH-ERP-TRACKING.md: sección Emparejamiento + ejemplo #7
- No conflicto con opt-in #7 (borrador, no enviado): solo campos ERP

### Match #7 ejemplo
- `pairing_status=proposed`, `pairing_method=curated_manual`, `proposed_at=2026-08-21`
- Michelle `is_paired=true`, `paired_with_email=kblanco@una.cr`
- Kinndle `paired_with_email=michelle.vierarom@ug.edu.ec`

---

## Ampliación — naming, roadmap, dashboard HTML

### Usuario
1. Sugerir campos futuros al tracking PB
2. Recomendar naming (ERP vs otro término, contexto ES Synergium)
3. Vista tabular HTML (estilo hoja de cálculo) + export JSON
4. Sesión + commit + push

### Agente

**Naming canónico:** **Pipeline de matching** (ES) · **Match Pipeline** (EN). Evitar «ERP» en UI; colecciones PB sin renombrar.

**Roadmap:** `producto/forms/docs/MATCH-ERP-ROADMAP.md` — must-have (`intro_at`, `follow_up_due`, `opt_in_deadline`, `submission` link, `urgency`) + nice-to-have.

**Dashboard:**
- `producto/forms/deploy/scripts/export_match_dashboard.py` → `pb_public/match-dashboard/data.json`
- `producto/forms/deploy/pb_public/match-dashboard/index.html` — tabs por match / participante, búsqueda, badges, cabecera fija
- Doc principal: `MATCH-TRACKING.md` (alias `MATCH-ERP-TRACKING.md`)
- Enlace en `hoy/tableros/MATCHES.md`
- URL prod tras deploy: `https://forms.synergium.net/match-dashboard/`

**Código:**
- `setup_collections.py`: merge pairing fields en colecciones existentes (`patch_collection_fields`)
- `backfill_match_tracking.py`: corregido syntax error match #7; seed vuelve a `curated` sin opt-in enviado
- `MATCHES.md`: match #7 opt-in **pendiente** (no enviado)

**Export ejecutado:** 7 matches, 14 participants, 24 events desde PocketBase prod.

### Manual pendiente
- `setup_collections.py` + `backfill_match_tracking.py` en VPS (pairing fields aún vacíos en prod para #7)
- Rsync `pb_public/match-dashboard/` a forms.synergium.net
- Enviar opt-in #7 (ambos borradores ES) + actualizar PB/historial
- Unificar borrador Michelle a ES en expediente (antes EN en sesión anterior)
