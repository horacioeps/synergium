# Synergium.net — upgrade de contenido (corto)

Fecha: 2026-08-16 / 2026-08-17
Sitio: [synergium.net](https://synergium.net/)

## En vivo

| URL | Idioma |
|---|---|
| https://synergium.net/ | Inglés (portada, idioma por defecto) |
| https://synergium.net/es/ | Español |
| https://synergium.net/en/ | 301 → `/` |

Otros idiomas (zh-CN, ar, ja, pt-BR, it, de): selector con icono de globo. Traducción automática a partir del inglés. Árabe pone `dir=rtl`.

## Qué se publicó

Home corta: qué hacemos, cómo (3 pasos del brochure), para quién (un bloque), quiénes somos (un párrafo), logros ya existentes, contacto mailto. Sin precios. Plantilla `page-no-title`. Cabecera: globo + código de idioma + claro/oscuro.

Contenido posterior (SKUs + Partner Snapshot, misma home): [2026-08-17-skus-restantes](../2026-08-17-skus-restantes/README.md).

## Rollback

```bash
python3 generado/web-synergium/casos/2026-08-16-upgrade-contenido/rollback.py
```

Backups: `generado/web-synergium/wp-backups/pre-upgrade-2026-08-16/`
Application Password: `/tmp/synergium-app-pass.txt`

## Republicar

```bash
python3 generado/web-synergium/casos/2026-08-16-upgrade-contenido/apply.py
```
