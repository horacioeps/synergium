# Import Google Sheet → PocketBase

Las respuestas del Google Form **no** entran solas en Synergium Forms hasta que corra el sync.

## Objetivo

Cada **15 minutos**: leer filas nuevas del spreadsheet de respuestas → `submissions` en PocketBase, con:

| Campo | Valor |
|-------|--------|
| `source` | `google` |
| (web) | `source` = `web` |

Deduplicar por **email** (+ form id): si ya existe submission con ese `respondent_email` en ese form, skip.

## Sheet

| | |
|--|--|
| Spreadsheet | [Community directory EN responses](https://docs.google.com/spreadsheets/d/19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w/edit) |
| Sheet ID | `19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w` |

Hoy el export CSV público **no** funciona (403/login). Hace falta una de:

1. **Service account** Google con la hoja compartida (lectura) + JSON key en el VPS (`chmod 600`), o
2. Export CSV manual periódico, o
3. Compartir la hoja como “cualquiera con el enlace → visor” y usar export URL (menos seguro).

## Flujo previsto

1. Cron cada 15 min en VPS (`*/15 * * * *`) o pm2-cron.
2. Script `scripts/synergium_forms_sheet_sync.py` (pendiente de credenciales Sheets).
3. Mapear columnas Google → `field_id` de `schema-en.json`.
4. `POST` submissions con `source: "google"`.
5. Log: nuevas / skipped / errores.

## Columna `source` en BD

Valores: `web` \| `google`. Se añade con `setup_collections.py` (campo select en `submissions`).

Envíos desde la web ya intentan mandar `source: "web"` (con fallback si el campo aún no existe).

## Pendiente para activar el cron

- [ ] Acceso lectura al Sheet (service account o CSV)
- [ ] Mapeo columnas confirmado (cabeceras Google vs schema)
- [ ] Campo `source` creado en PocketBase
- [ ] Cron en VPS
