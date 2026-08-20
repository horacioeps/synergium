# Synergium Forms (canónico)

Formularios públicos en `https://forms.synergium.net/<id>`.

## Vivo

- Community directory EN: https://forms.synergium.net/nexus-input
- Deploy: VPS Explore Labs (PocketBase + Apache + SES)
- Estilo: misma base que synergium.net (Manrope, paleta Crepúsculo)

## Docs

| Doc | Contenido |
|-----|-----------|
| [ESTADO-DEPLOY.md](ESTADO-DEPLOY.md) | Estado HTTPS/DNS/pendientes |
| [URL-OPTIONS.md](URL-OPTIONS.md) | Slug elegido: **nexus-input** |
| [IDIOMA-SELECTOR.md](IDIOMA-SELECTOR.md) | Selector = web (EN default + mismos idiomas); regla para todos los forms |
| [GOOGLE-SHEET-SYNC.md](GOOGLE-SHEET-SYNC.md) | Sheet Google ↔ BD (cada 15 min) |
| [COMO-HACERLO.md](COMO-HACERLO.md) | Flujo agente publica por API |
| [PUENTE-DESDE-MAESTRO.md](PUENTE-DESDE-MAESTRO.md) | Enlace a sesión/HISTORICO del repo maestro |
| [arquitectura.md](arquitectura.md) | Diseño |
| [modelo-datos.md](modelo-datos.md) | Colecciones |

## Publicar

```bash
python3 scripts/synergium_forms_publish.py publish --schema forms/casos/.../schema.json
```

Credenciales: secrets / `~/synergium-forms/.env` en el VPS (no en git).
