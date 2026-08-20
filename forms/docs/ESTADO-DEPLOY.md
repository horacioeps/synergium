# Estado del despliegue — actualizado 2026-08-20

## En vivo (OK)

- DNS: `forms.synergium.net` → `217.154.191.98`
- HTTPS Let’s Encrypt (caduca 2026-11-18; renovación automática certbot)
- HTTP → HTTPS (301 301)
- PocketBase pm2 `synergium-forms` online
- Community directory EN:

**https://forms.synergium.net/nexus-input**

(legacy temporal: `…/0mn7nfs5kqsi8g` — alias/redirect hasta rename en PocketBase)

## Google Forms / Spreadsheet vs Synergium Forms

**Hoy NO conviven solos en la misma BD.**

| Canal | Dónde caen las respuestas |
|-------|---------------------------|
| Enlace Google Forms (`forms.gle`) | Google Spreadsheet (filas nuevas; normalmente **al final**, no “arriba”) |
| Enlace `forms.synergium.net/nexus-input` | PocketBase (`submissions`) + email; campo `source=web` |

Son dos tuberías independientes hasta que importemos / sincronicemos (objetivo: cron **cada 15 min**, `source=google`).

### Qué hacer con gente que aún tiene el enlace Google

1. **Importar** lo ya recogido en el Sheet → PocketBase (script; una vez o bajo demanda).
2. Elegir una de estas políticas:
   - **A (recomendada):** cerrar o dejar de compartir el Google Form; en WhatsApp/comunidad publicar solo el enlace Synergium; si alguien envía al Sheet, no entra a la BD hasta un import/sync.
   - **B:** dejar Google abierto un tiempo y **sincronizar** Sheet → BD cada 15 min; hace falta acceso lectura al spreadsheet.
3. Campo `source` = `web` \| `google` en cada submission.

## Pendiente (prioridad)

1. **Deploy** rename `0mn7nfs5kqsi8g` → `nexus-input` + front/alias (`apply_nexus_input.sh`) — necesita secrets SSH/API.
2. **Campo `source`** en PocketBase + marcar submissions previas.
3. **Import / cron 15 min** Sheet → PocketBase (credenciales Sheets).
4. Publicar **versión ES** + selector idioma ([IDIOMA-SELECTOR.md](IDIOMA-SELECTOR.md)).
5. Cerrar/actualizar mensajes WhatsApp con la URL nueva.
6. (Opcional) Secrets Cursor: `SYNERGIUM_FORMS_PB_*` / `EXPLORE_LABS_SSH_HORACIO_*`.
7. (Opcional) Borrar submissions de prueba (`PublicTest*`) en PocketBase.

## Publicar otra encuesta

Tú das el texto en el chat → el agente corre `scripts/synergium_forms_publish.py` → te devuelve `https://forms.synergium.net/<codigo>`.
