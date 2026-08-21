# 2026-08-17 — synergium.net: quitar aviso de idiomas del pie

**Session ID:** (cloud agent 2026-08-17)

Volcado bruto: [sesiones/2026-08-17-synergium-quitar-aviso-idiomas.md](../sesiones/2026-08-17-synergium-quitar-aviso-idiomas.md).

## Pedido

En cada página, independiente del idioma, salía:

```
info@synergium.net
The site is in English and Spanish. Other languages use the globe in the header.
```

Mejor quitarlo.

## Hecho

Ese bloque era el footer global (template part), no el copy de cada página. El JS de la cabecera lo reescribía en ES. Se eliminó el `mailto` duplicado y el aviso; el email sigue en Contact / Contacto.

Verificado en `/`, `/es/`, servicios, about, contact, método y `/?lang=de`.

Caso: `generado/web-synergium/casos/2026-08-17-quitar-aviso-idiomas/`. Backup: `wp-backups/pre-footer-langs-2026-08-17/`. Rollback: `rollback.py`.
