# Import Google Sheet → PocketBase

## En castellano

Hay **dos sitios** de respuestas:

1. **Google Form** → esta hoja de Google Sheets  
2. **forms.synergium.net/nexus-input** → nuestra base PocketBase  

No se copian solos. El sync cada 15 min baja el CSV de la hoja e importa filas nuevas con `source=google`.

**2026-08-20:** la hoja **sí se puede leer** con el enlace (compartida). El error anterior fue usar mal el `gid` (`0` en vez de `1537513728`). No hace falta service account mientras siga “cualquiera con el enlace → Visor”.

## Sheet

| | |
|--|--|
| Spreadsheet | [respuestas](https://docs.google.com/spreadsheets/d/19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w/edit?gid=1537513728#gid=1537513728) |
| Sheet ID | `19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w` |
| gid | `1537513728` |
| CSV | `…/export?format=csv&gid=1537513728` → **200 OK** |
| Filas (2026-08-20) | **26** respuestas (+ cabecera) |

## Objetivo

Cada **15 min**: filas nuevas → PocketBase, `source=google`. Deduplicar por email. Envíos web: `source=web`.

## Flujo previsto

1. Cron VPS `*/15`.
2. Script `scripts/synergium_forms_sheet_sync.py` (pendiente de implementar).
3. Mapear columnas Google → `field_id`.
4. `POST` submissions.
5. Log nuevas / skipped / errores.

## Pendiente

- [x] Acceso lectura CSV público (gid correcto)
- [ ] Script de import + mapeo columnas
- [ ] Cron 15 min en VPS
- [x] Campo `source` en PocketBase
