# Estado del despliegue — actualizado 2026-08-20

## En vivo (OK)

- DNS: `forms.synergium.net` → `217.154.191.98`
- HTTPS Let’s Encrypt (caduca 2026-11-18; renovación automática certbot)
- HTTP → HTTPS (301 301)
- PocketBase pm2 `synergium-forms` online
- Community directory EN:

**https://forms.synergium.net/0mn7nfs5kqsi8g**

## Google Forms / Spreadsheet vs Synergium Forms

**Hoy NO conviven solos en la misma BD.**

| Canal | Dónde caen las respuestas |
|-------|---------------------------|
| Enlace Google Forms (`forms.gle`) | Google Spreadsheet (filas nuevas; normalmente **al final**, no “arriba”) |
| Enlace `forms.synergium.net/…` | PocketBase (`submissions`) + email |

Son dos tuberías independientes hasta que importemos / sincronicemos.

### Qué hacer con gente que aún tiene el enlace Google

1. **Importar** lo ya recogido en el Sheet → PocketBase (script; una vez o bajo demanda).
2. Elegir una de estas políticas:
   - **A (recomendada):** cerrar o dejar de compartir el Google Form; en WhatsApp/comunidad publicar solo el enlace Synergium; si alguien envía al Sheet, no entra a la BD hasta un import manual.
   - **B:** dejar Google abierto un tiempo y **sincronizar** Sheet → BD (cron o al pedir “importa el sheet”); hace falta el ID del spreadsheet + acceso (cuenta de servicio / export CSV).
3. Marcar en cada submission un campo `source` = `synergium` | `google` para no mezclar ciegos.

“Encima” en Google Sheets: las respuestas del Form se **añaden como filas nuevas** (casi siempre al final de la hoja de respuestas). No pisan filas viejas.

## Pendiente (prioridad)

1. **Import CSV/Sheet → PocketBase** del Community directory (y deduplicar por email si hace falta).
2. Decidir política A o B para el enlace Google; si B, montar sync.
3. Publicar **versión ES** del mismo directorio (mismos `field id`).
4. Cerrar/actualizar mensajes WhatsApp con la URL nueva.
5. (Opcional) Secrets Cursor: `SYNERGIUM_FORMS_PB_*` para publicar desde el agente sin leer `.env` del VPS.
6. (Opcional) Borrar submissions de prueba (`PublicTest*`) en PocketBase.
7. Formulario ES Community directory + más forms Synergium (Snapshot, etc.) cuando los pidas.

## Publicar otra encuesta

Tú das el texto en el chat → el agente corre `scripts/synergium_forms_publish.py` → te devuelve `https://forms.synergium.net/<codigo>`.
