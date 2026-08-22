
## 2026-08-22 ~18:05 CEST — Basic Auth match-dashboard (urgente)

**Pedido:** Proteger `https://forms.synergium.net/match-dashboard/` con HTTP Basic Auth (usuario `horacio`; contraseña solo en VPS/htpasswd, no en git).

**Hecho en VPS:**
- `~/synergium-forms/.htpasswd-match-dashboard` (htpasswd usuario horacio)
- Bloque `<Directory /var/www/forms.synergium.net/match-dashboard>` en `forms.synergium.net.conf` y `forms.synergium.net-le-ssl.conf`
- `a2enmod auth_basic authn_file`; `apache2ctl configtest`; reload apache
- Pruebas: sin auth → HTTP 401; con auth → HTTP 200

**Repo:**
- Templates Apache actualizados (`AuthUserFile` path, sin contraseña)
- `MATCH-TRACKING.md`: fila Auth en tabla dashboard

