# Quitar aviso de idiomas del pie (synergium.net)

Pedido: en todas las páginas, independiente del idioma, salía:

```
info@synergium.net
The site is in English and Spanish. Other languages use the globe in the header.
```

Ese bloque era el **template part footer** (id WP 16), no el contenido de cada página. El JS de la cabecera reescribía el segundo párrafo según idioma (`#syn-footer-langs`).

## Cambio

- Footer: se eliminan el `mailto` duplicado y el aviso de idiomas. Queda solo un borde superior fino, sin texto.
- Header: se quita el JS que pintaba `#syn-footer-langs`.
- El email de contacto **sigue** en las secciones Contact / Contacto de cada página.

## Publicar / revertir

Application Password en `/tmp/synergium-app-pass.txt`.

```bash
python3 generado/web-synergium/casos/2026-08-17-quitar-aviso-idiomas/apply.py
python3 generado/web-synergium/casos/2026-08-17-quitar-aviso-idiomas/rollback.py
```

Backup previo: `generado/web-synergium/wp-backups/pre-footer-langs-2026-08-17/`.
