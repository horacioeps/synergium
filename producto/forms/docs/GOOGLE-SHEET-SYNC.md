# Import Google Sheet → PocketBase

## Estado (2026-08-21)

- CSV público OK (`gid=1537513728`).
- Import masivo: **26** filas → `nexus-input`, `source=google`, dedupe email.
- Cron VPS cada **15 min**: `~/synergium-forms/scripts/run_sheet_sync.sh`.
- Decisiones: [DECISIONES-2026-08-20.md](DECISIONES-2026-08-20.md) — **ambos** canales (Google + web).

## Heterogeneidad de `answers` (vivir con ello)

Tras el pase 2026-08-21 del form Synergium, en PocketBase conviven filas con esquemas distintos en el JSON `answers`:

| Origen | `source` | Qué esperar |
|--------|----------|-------------|
| Google Form (histórico / sync) | `google` | Columnas del Google Form; ids clásicos (`three_words`, `also_spanish_community`, …). Sin `orcid`, `data_consent`, `collab_modality`, `how_found_form` salvo que el Sheet los tenga. |
| Web `nexus-input` (actual) | `web` | Schema nuevo (37 campos): labels profesionales; sin `three_words` / `also_spanish_community`; con consent, ORCID, modalidad, how_found. |

No hay migración de filas antiguas. Matching y exports deben tratar campos como **opcionales** (`.get`, defaults). El sync Sheet mapea con un schema **congelado** (`schema-en-google-sync.json`), no con el schema vivo profesional (`schema-en.json`).

Detalle de cambios de schema: [../casos/community-directory-matching/AUDITORIA-CAMPOS-2026-08-21.md](../casos/community-directory-matching/AUDITORIA-CAMPOS-2026-08-21.md).

## En castellano

1. Google Form → Spreadsheet  
2. forms.synergium.net → PocketBase  
3. Cada 15 min el VPS baja el CSV e importa lo nuevo (`source=google`). Si el email ya está, skip.

## Sheet

| | |
|--|--|
| URL | [respuestas](https://docs.google.com/spreadsheets/d/19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w/edit?gid=1537513728#gid=1537513728) |
| Sheet ID | `19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w` |
| gid | `1537513728` |

## Script

```bash
set -a; source ~/.cursor/secrets.env; set +a
# strip quotes if needed, or run on VPS:
python3 ops/scripts/synergium_forms_sheet_sync.py --public-id nexus-input
python3 ops/scripts/synergium_forms_sheet_sync.py --public-id nexus-input --dry-run
```
