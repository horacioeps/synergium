# Estado del despliegue — 2026-08-18

## Hecho

- PocketBase 0.39.11 en VPS Explore Labs (`217.154.191.98`), pm2 `synergium-forms`, `127.0.0.1:8090`
- Apache vhost HTTP `forms.synergium.net` → static `/var/www/forms.synergium.net` + proxy `/api` y `/_/`
- Colecciones `forms` / `submissions`
- API pública `GET /api/sf/form/{publicId}`
- Front SPA en `pb_public/index.html`
- Email al enviar vía SES (EmailerX SMTP), notifica a `horacio@horacio-ps.com`
- CLI agente: `scripts/synergium_forms_publish.py`
- **Community directory EN publicado**

## URL del primer form (cuando DNS+SSL estén)

`https://forms.synergium.net/0mn7nfs5kqsi8g`

Mientras DNS no exista, el stack responde por IP con cabecera Host:

```bash
curl -H 'Host: forms.synergium.net' http://217.154.191.98/0mn7nfs5kqsi8g
```

## Pendiente (1 paso manual)

En el panel DNS de IONOS para **synergium.net**, crear:

| Tipo | Nombre | Valor |
|------|--------|-------|
| **A** | `forms` | `217.154.191.98` |

Luego, en el VPS (o pedir al agente):

```bash
bash ~/synergium-forms/scripts/enable_ssl.sh
```

No hay API/token IONOS en secrets; por eso el registro DNS no se puede crear desde el agente.

## Credenciales (VPS, no en git)

`~/synergium-forms/.env` (chmod 600) — admin PocketBase + SMTP.

## Publicar otra encuesta (agente)

```bash
# con env cargado desde VPS .env o secrets Cursor
python3 scripts/synergium_forms_publish.py publish --schema generado/synergium-forms/casos/.../schema.json
```
