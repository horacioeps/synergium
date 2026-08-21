# Estado del despliegue — actualizado 2026-08-20

## En vivo (OK)

- DNS: `forms.synergium.net` → `217.154.191.98`
- HTTPS Let’s Encrypt (caduca 2026-11-18; renovación automática certbot)
- HTTP → HTTPS (301 301)
- PocketBase pm2 `synergium-forms` online
- Community directory EN:

**https://forms.synergium.net/nexus-input**

(legacy `…/0mn7nfs5kqsi8g` → el front redirige / resuelve a `nexus-input`)

## Aplicado en vivo (2026-08-20)

- Rename PocketBase `public_id` → `nexus-input`
- Campo `source` (`web` \| `google`) en `submissions`
- Front desplegado (alias legacy + submit `source=web`)
- Secrets locales: `~/.cursor/secrets.env` (SSH Horacio)

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

1. ~~Import / cron 15 min~~ → **hecho** (26 filas + cron VPS).
2. Marcar submissions previas con `source` si hace falta.
3. Selector idioma = web (todos los forms; ES nativo en nexus-input). Ver [IDIOMA-SELECTOR.md](IDIOMA-SELECTOR.md).
4. Cerrar/actualizar mensajes WhatsApp con la URL nueva *(decisión 5 pendiente)*.
5. (Opcional) Borrar submissions de prueba (`PublicTest*`) en PocketBase.

Decisiones Horacio: [DECISIONES-2026-08-20.md](DECISIONES-2026-08-20.md).


## Publicar otra encuesta

Tú das el texto en el chat → el agente corre `ops/scripts/synergium_forms_publish.py` → te devuelve `https://forms.synergium.net/<codigo>`.
