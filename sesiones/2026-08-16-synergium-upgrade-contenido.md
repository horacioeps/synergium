# Sesión 2026-08-16/17 — synergium.net upgrade de contenido

## Pedido

Implementar el upgrade de contenido de synergium.net aprobado, luego recortado (menos es más), con SEO, idiomas automáticos y inglés como idioma por defecto.

## Hecho

- Backups REST en `generado/web-synergium/wp-backups/pre-upgrade-2026-08-16/`
- Rollback: `python3 generado/web-synergium/casos/2026-08-16-upgrade-contenido/rollback.py`
- Portada `/` en inglés (página 35). Español en `/es/` (página 53, antes `/en/`). `/en/` redirige a `/`.
- Copy corto del brochure (proceso, 3 pasos, un bloque para quién, quiénes somos de un párrafo). Sin precios. Logros existentes sin ampliar.
- Cabecera: globo + código de idioma (lista es/en/zh-CN/ar/ja/pt/it/de) + claro/oscuro. Plantilla `page-no-title`.
- SEO: plugin Synergium SEO (title, description, canonical, hreflang en/es/x-default→EN, OG, Twitter, JSON-LD). Sitemap core `/wp-sitemap.xml`. `siteurl` a https. Alt en icono/OG.
- GTranslate instalado; otros idiomas se traducen desde el inglés. Árabe: `dir=rtl`.

## Omitido a propósito

- Sitio de 8 páginas, 3 landings «para quién», casos inventados, equipo largo, blog, brochure PDF (lleva precio), Rank Math, Search Console, precios, nombre de Horacio (se mantiene equipo anónimo).
