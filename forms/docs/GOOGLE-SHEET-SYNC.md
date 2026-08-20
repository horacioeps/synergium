# Import Google Sheet → PocketBase (pendiente de datos)

Las respuestas del Google Form **no** entran solas en Synergium Forms.

## Flujo previsto

1. Export CSV del spreadsheet de respuestas (o API Sheets).
2. Mapear columnas Google → `field_id` del schema (`schema-en.json`).
3. `POST` a `submissions` con `answers` JSON + `respondent_email`.
4. Guardar `source: "google"` dentro de `answers` o campo dedicado cuando exista.
5. Deduplicar por email (skip si ya hay submission con mismo email en ese form).

## Qué necesita el agente para ejecutarlo

- CSV exportado pegado en el repo (`generado/synergium-forms/casos/.../google-export.csv`), **o**
- ID del Google Spreadsheet + acceso lectura (service account / OAuth).

Hasta entonces: Sheet y BD son paralelos.
