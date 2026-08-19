# Sesión 2026-08-17 — synergium.net: quitar aviso de idiomas del pie

Fecha: 2026-08-17 ~22:22 UTC

## Pedido (Horacio)

en cada una de las paginas independientemente del idioma sales este mensakea "info@synergium.net

The site is in English and Spanish. Other languages use the globe in the header." qmejorq uitarlo

## Qué era

No estaba en el contenido de cada página. Era el **template part footer** de Twenty Twenty-Five (WP id 16), visible en todas las URLs:

- `mailto:info@synergium.net`
- párrafo `#syn-footer-langs`: «The site is in English and Spanish. Other languages use the globe in the header.»

El JS de la cabecera (template part header, WP id 55) reescribía ese párrafo en español si el idioma de UI era `es`. Por eso el bloque salía en todas las páginas y en todos los idiomas (en EN/otros idiomas, siempre en inglés).

El email de las secciones Contact / Contacto del cuerpo **no** se tocó.

## Qué se hizo

1. Acceso WP igual que el arco 16–17 ago: credenciales vault (fila Synergium.net) + Application Password REST. Vault por SSH (ASKPASS; `sshpass` instalado en el entorno).
2. Backup de footer y header en `generado/web-synergium/wp-backups/pre-footer-langs-2026-08-17/`.
3. Footer publicado vacío (solo grupo con borde superior fino, sin texto).
4. Header: eliminado el bloque JS de `#syn-footer-langs`.
5. Verificado en vivo: `/`, `/es/`, `/services/`, `/es/servicios/`, `/about/`, `/contact/`, `/es/contacto/`, `/method/`, `/?lang=de`. Cero coincidencias de `syn-footer-langs` / «Other languages use the globe» / «El sitio está en inglés y español». El `<footer>` queda sin el email ni el aviso.

Caso: `generado/web-synergium/casos/2026-08-17-quitar-aviso-idiomas/` (`apply.py`, `rollback.py`, `header.html`, `footer.html`).

## URLs

- https://synergium.net/
- https://synergium.net/es/

## Notas

- No se tocó la vault.
- Rama `main`. Application Password no va al repo (`/tmp/synergium-app-pass.txt`).
