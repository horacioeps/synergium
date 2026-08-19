# Sesión 2026-08-18 — Synergium Forms (arquitectura + Community directory)

Volcado completo: [chats/2026-08-18-synergium-forms-arquitectura.md](../chats/2026-08-18-synergium-forms-arquitectura.md).

## Interacciones

1–8. Arquitectura, PocketBase, flujo agente, VPS Explore Labs, URL `forms.synergium.net`.
9. **Usuario:** implementa.
10. **Agente:** Deploy en VPS Explore Labs (PocketBase + Apache + SES email + CLI). Community directory EN publicado (`0mn7nfs5kqsi8g`). Falta DNS A en IONOS para `forms` → `217.154.191.98` y certbot SSL.

## Artefactos

- `generado/synergium-forms/deploy/` (pb_public, pb_hooks, apache, scripts)
- `scripts/synergium_forms_publish.py`
- `generado/synergium-forms/docs/ESTADO-DEPLOY.md`
- VPS: `~/synergium-forms/` + pm2 `synergium-forms` + Apache site

## Pendiente

DNS A `forms.synergium.net` → `217.154.191.98` (panel IONOS). Luego `enable_ssl.sh`.
