# Import Google Sheet → PocketBase

## En castellano (qué pasa)

Hay **dos sitios** donde caen respuestas hoy:

1. **Google Form** → se guarda en un **Google Spreadsheet** (la hoja de respuestas).
2. **forms.synergium.net/nexus-input** → se guarda en **nuestra base PocketBase**.

No se mezclan solos. Para que lo nuevo del Sheet entre en nuestra BD cada 15 min, un script en el VPS tiene que **leer la hoja**.

Sabemos **cuál** es la hoja (ID `19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w`).  
Lo que no tenemos es **permiso técnico** para que el servidor la lea sin que tú estés logueado en Google:

- Probamos el “exportar CSV por enlace” y Google pide login (no es público).
- Por eso hace falta una de estas vías (elige tú en las dudas numeradas):

| Opción | Qué es | Pros / contras |
|--------|--------|----------------|
| **Service account** | Usuario-robot de Google; compartes la hoja con su email; el VPS usa una clave JSON | Automático y seguro; un poco de setup una vez |
| **Hoja “cualquiera con el enlace → Visor”** | El CSV se puede bajar sin login | Fácil; menos privado (quien tenga el enlace ve datos) |
| **CSV a mano** | Tú exportas y lo pegas / subes de vez en cuando | Sin setup; no es cada 15 min |

Hasta elegir eso, el cron de 15 min **no puede arrancar**.

## Objetivo técnico

Cada **15 minutos**: filas nuevas del Sheet → `submissions` en PocketBase.

| Campo | Valor |
|-------|--------|
| `source` | `google` (vienen del Sheet) |
| envíos web | `source` = `web` |

Deduplicar por **email** (+ form): si ya está, no duplicar.

## Sheet

| | |
|--|--|
| Spreadsheet | [Community directory EN responses](https://docs.google.com/spreadsheets/d/19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w/edit) |
| Sheet ID | `19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w` |

## Flujo previsto (cuando haya acceso)

1. Cron VPS cada 15 min.
2. Script `scripts/synergium_forms_sheet_sync.py`.
3. Mapear columnas Google → `field_id` del schema.
4. `POST` con `source: "google"`.
5. Log: nuevas / skipped / errores.

## Pendiente

- [ ] Decidir cómo leer el Sheet (dudas **1–2** abajo / en sesión)
- [ ] Mapeo columnas
- [ ] Cron en VPS  
  (campo `source` en PocketBase: ya creado)
