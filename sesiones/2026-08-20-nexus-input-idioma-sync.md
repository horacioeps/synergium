# Sesión 2026-08-20 — nexus-input + idioma + sheet sync + source

## Usuario

> la P nexus-input, ok? dame el nuevo enlace e implemente. y otra cosa, si podemos tener selector de idioma, que te parece? y otra cosa, en la base de datos si puede ir leyendo cada 15 mintuso del google spreadsheet pro si hay algin uevo y añadirlo a nuestra base de datos aqui, no se si te dije esto antes. y aañadir una nueva columna en la BD que diga de dónde viene, si de Google Spreadsheet o de aqui de la web, ok? dime dudas y sugerencias

## Agente

### Slug
- Elegido: **P** → `public_id` = `nexus-input` (hyphen; la API no admite `/` en el id).
- URL canónica: https://forms.synergium.net/nexus-input
- Front: alias temporal al id legacy `0mn7nfs5kqsi8g`; `/nexus/input` se normaliza a `nexus-input`.
- CLI: `rename` en `scripts/synergium_forms_publish.py`.
- Script VPS: `forms/deploy/scripts/apply_nexus_input.sh`.
- **Bloqueo:** en esta copia local no hay `EXPLORE_LABS_SSH_HORACIO_*` ni `SYNERGIUM_FORMS_PB_*` → rename/deploy en vivo pendiente.

### Idioma
- Sí; doc `forms/docs/IDIOMA-SELECTOR.md`. Recomendación: un enlace + toggle EN/ES (schemas alineados). ES aún no existe.

### Sheet cada 15 min + `source`
- Doc actualizado `GOOGLE-SHEET-SYNC.md`.
- Campo `source` = `web` \| `google` en `setup_collections.py` + front envía `web` (retry si columna no existe).
- Sheet ID conocido; export público no funciona → hace falta service account o compartir lectura.

### Docs tocados
URL-OPTIONS, ESTADO-DEPLOY, README forms, PUENTE, modelo-datos, caso README, IDIOMA-SELECTOR.
