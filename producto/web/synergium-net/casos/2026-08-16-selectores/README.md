# Selectores de idioma y tema en synergium.net

Landing WordPress (Twenty Twenty-Five, una sola página). Acceso igual que bio-hpc.eu: REST API + Application Password `cursor` (usuario `admin`).

## Qué hay en vivo

- [synergium.net](https://synergium.net/) — español (página 35, portada)
- [synergium.net/en/](https://synergium.net/en/) — inglés (página 53)
- Cabecera: selector **ES | EN** con bandera del idioma actual (España / UK) y botón **claro/oscuro** (paleta Crepúsculo: base `#131313`)
- El modo se guarda en `localStorage` (`syn-theme`); si no hay preferencia, usa `prefers-color-scheme`
- Corregido el enlace de contacto: `mailto:info@synergium.net`
- Favicon / apple-touch / TileImage vía `site_icon` (media 63)
- OG + Twitter `summary_large_image` en ES y EN
- Icono: https://synergium.net/wp-content/uploads/2026/08/synergium-icon-1024.png
- OG: https://synergium.net/wp-content/uploads/2026/08/synergium-og-1200x630-1.png

No se instaló Polylang. Dos páginas + conmutador en la cabecera. El `lang` de `/en/` se ajusta por JS.

## Título de página oculto (2026-08-16)

El H1 grande «Synergium» lo pintaba el tema (título de página), no el contenido. Redundante con el site-title de la cabecera.

Ambas páginas usan la plantilla `page-no-title` (`template` REST = `page-no-title`):

- id 35 → https://synergium.net/
- id 53 → https://synergium.net/en/

Verificado en vivo: 0 `<h1>` en `<main>`; el site-title de la cabecera se mantiene. Copy no tocado.

## Cómo volver a publicar

Application Password en `/tmp/synergium-app-pass.txt` (no va al repo).

```bash
python3 generado/web-synergium/casos/2026-08-16-selectores/apply.py
python3 generado/web-synergium/casos/2026-08-16-selectores/apply_icons.py
```

Backups previos: `generado/web-synergium/wp-backups/`.
