# Infraestructura Synergium

## synergium.net (WordPress)

- **Hosting:** VPS Explore Labs
- **Gestión:** REST API desde agente Cursor (scripts en `producto/web/synergium-net/casos/*/apply.py`)
- **Patrón:** backup JSON antes de escribir → apply → rollback si falla
- **Idiomas:** ES + EN (TranslatePress u equivalente)

Casos documentados en [producto/web/synergium-net/casos/](../../producto/web/synergium-net/casos/).

## forms.synergium.net (PocketBase)

- **Stack:** PocketBase 0.39.11, pm2 `synergium-forms`, puerto local 8090
- **Proxy:** Apache vhost → static + `/api` y `/_/`
- **Email:** SES (EmailerX SMTP) → `horacio@horacio-ps.com` en cada envío
- **VPS IP:** `217.154.191.98`

### DNS pendiente (IONOS)

| Tipo | Nombre | Valor |
|------|--------|-------|
| A | `forms` | `217.154.191.98` |

Tras crear el registro:

```bash
bash ~/synergium-forms/scripts/enable_ssl.sh
```

### Primer formulario publicado

- **Public ID:** `nexus-input` (legacy: `0mn7nfs5kqsi8g`)
- **URL:** `https://forms.synergium.net/nexus-input`

Estado detallado: [producto/forms/docs/ESTADO-DEPLOY.md](../../producto/forms/docs/ESTADO-DEPLOY.md)

## Scripts operativos

| Script | Uso |
|--------|-----|
| `ops/scripts/synergium_forms_publish.py` | Publicar/cerrar/exportar forms |
| `producto/forms/deploy/scripts/deploy_from_agent.sh` | Deploy desde agente |
| `producto/web/synergium-net/casos/*/apply.py` | Cambios WP synergium.net |

## Secrets

Credenciales en VPS `~/synergium-forms/.env` (no en git). Secrets Cursor para SSH/API según [Obsidian vault-cloud-ssh](https://github.com/horacioeps/Obsidian/blob/main/.cursor/rules/vault-cloud-ssh.mdc).
