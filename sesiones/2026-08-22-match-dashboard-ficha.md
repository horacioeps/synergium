# Sesión 2026-08-22 — Pestaña Ficha match dashboard

## Pedido

Añadir pestaña avanzada al match dashboard donde por cada persona se vean todos los campos: respuestas completas nexus-input, pipeline, y todos los emails (contact_events con cuerpo completo). Export, deploy VPS, documentación.

## Hecho

### Export (`export_match_dashboard.py`)

- Nuevo array `profiles` en `data.json` (30 personas desde PB producción).
- Por email: identidad, `nexus_form` (etiquetas de `schema-en.json`), `pipeline`, `contact_events` (subject, body, notes, direction…), `match_align` si existe.
- Excluye PublicTest; une emails de submissions, participantes y contact_events.
- Fix `multi_select` con valores dict (opción «Otro»).

### UI (`match-dashboard/index.html`)

- Pestaña **Ficha**: master-detail (lista izquierda + panel derecho).
- Secciones: Identidad | Formulario nexus-input | Pipeline | Emails y contacto | Match-align.
- Búsqueda global incluye cuerpos de email y campos del formulario.

### Deploy

- `export_match_dashboard.py` contra forms.synergium.net → 30 profiles, 68 events.
- `deploy_from_agent.sh` rsync a VPS.

### Docs

- `MATCH-TRACKING.md`: pestaña Ficha, PII ampliado, match-align por email.

## Stats export

- 7 matches, 14 participants, 28 directory, **30 profiles**, 68 events (pocketbase)

## URL

https://forms.synergium.net/match-dashboard/ (Basic Auth)
