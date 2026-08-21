# Sesión 2026-08-18 — Synergium Forms (arquitectura + Community directory)

## Contexto

Pedido sobre la web de Synergium: formularios tipo Google Forms en `forms.synergium.net/<codigo>`, abiertos por enlace, respuestas en BD, email al completar. Ejemplo = Community directory (matching), el mismo que ya se especificó el 2026-08-14 para Google Forms.

Relacionado:

- WP synergium.net ya tocado (selectores, SKUs, etc.)
- Caso Google: `generado/comunidad-whatsapp/casos/2026-08-14-formulario-matching/`

## Pedido del usuario (completo)

Quiere formularios tipo Google Form cuya URL sea algo como `forms.synergium.net/jha76sd8a78sda` con un código, abiertos en libre para quien tenga el enlace, almacenar respuestas en base de datos, y que digamos cuál es el mejor candidato de almacenaje (¿dentro del WordPress de Synergium u otra cosa?), más email cada vez que alguien complete. Como ejemplo, el Community directory completo (campos Full name … Anything else to match you).

## Respuesta / decisión documentada

**Veredicto:** no usar la BD de WordPress de synergium.net como almacén principal. Mejor: app en `forms.synergium.net` + PostgreSQL (o MariaDB aparte del WP) + email SMTP/Resend.

WordPress = marketing. Forms = servicio al lado.

Alternativas evaluadas: plugins WP (Fluent/Gravity) solo si se quiere velocidad y se acepta mezclar PII; Tally/Fillout como puente; Google Forms solo mientras se migra.

## Artefactos creados

```
generado/synergium-forms/
├── docs/
│   ├── README.md
│   ├── COMO-HACERLO.md   ← decisión única (PocketBase)
│   ├── arquitectura.md
│   └── modelo-datos.md
└── casos/
    └── community-directory-matching/
        ├── README.md
        └── schema-en.json
```

También: enlace desde `generado/comunidad-whatsapp/docs/README.md`.

## Pendiente (siguiente paso si confirma “adelante”)

1. DNS `forms.` → IP VPS Explore Labs + Docker PocketBase + Caddy.
2. Secrets agente + script publish/close/export.
3. Front + email.
4. Publicar Community directory EN (y ES).
5. Migrar respuestas Google si las hay.

## Interacciones

1. **Usuario:** arquitectura forms Synergium + BD + email + ejemplo Community directory.
2. **Agente:** docs en `generado/synergium-forms/`, schema JSON EN, sesión + HISTORICO + push `main`.
3. **Usuario:** no queda claro cómo lo sugieres al final.
4. **Agente:** decisión única documentada en `COMO-HACERLO.md`: PocketBase en `forms.synergium.net`, front mínimo, email SMTP; WP fuera. Actualiza docs + push `main`.
5. **Usuario:** quiere dar directrices y que el agente cree/publique sin tocar paneles; ¿VPS = Explore Labs?
6. **Agente:** Sí flujo 100 % agente vía API. VPS = Explore Labs (`217.154.191.98`), **distinto** del WP synergium.net (`217.160.0.160`). Actualiza `COMO-HACERLO.md` + push.
7. **Usuario:** ¿La URL visible del form es tipo forms.synergium.net?
8. **Agente:** Sí. `https://forms.synergium.net/<codigo>`; el VPS es solo el hosting detrás del DNS.
9. **Usuario:** implementa.
10. **Agente:** Implementado en VPS Explore Labs:
    - PocketBase (pm2) + Apache vhost + front SPA + hooks email SES
    - CLI `scripts/synergium_forms_publish.py`
    - Community directory EN: public_id `0mn7nfs5kqsi8g`
    - Email de prueba enviado a horacio@horacio-ps.com
    - Pendiente: DNS A `forms` → `217.154.191.98` en IONOS + `enable_ssl.sh`
    - Doc: `generado/synergium-forms/docs/ESTADO-DEPLOY.md`
