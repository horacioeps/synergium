# Historial de trabajo Synergium

Cronología de lo hecho en el repo Obsidian (copiado aquí). Detalle en archivo/chats/ y sesiones/.

---

## 2026-04-11 — Estrategia e ideas de negocio

- Análisis crítico de **13 ideas** de negocio (Synergium + derivadas)
- Plantillas email broker Synergium (2 variantes LATAM)
- Plantillas podcast de pago (investigadores + empresas biotech LATAM)
- 12 empresas target + 10 mensajes LinkedIn

**Artefactos:** [comercial/estrategia/](../comercial/estrategia/), [archivo/chats/2026-04-11-analisis-ideas-negocio-synergium-podcast.md](chats/2026-04-11-analisis-ideas-negocio-synergium-podcast.md)

---

## 2026-05-03 / 2026-05-05 — Direcciones web

- Propuesta arquitectura **Synergium-first** para horacio-ps.com
- Mockups HTML estáticos (d2-synergium-first, derivadas A/B/C)

**Artefactos:** [producto/web/mockups/](../producto/web/mockups/)

---

## 2026-06-21 — Buscador de prospectos v1

- Brief: señales de dolor en web + NCPs Horizon
- Implementación Python en `comercial/prospectos/buscador-v1/scripts/buscador_prospectos/`
- Casos piloto: v1-web-ncps, cordis-piloto, smoke

**Artefactos:** [comercial/prospectos/buscador-v1/](../comercial/prospectos/buscador-v1/), [archivo/chats/2026-06-21-buscador-prospectos-synergium-v1.md](chats/2026-06-21-buscador-prospectos-synergium-v1.md)

---

## 2026-06-29 — Propuesta bioestadística (encaje)

- Análisis de encaje oferta bioestadística con Synergium

**Artefactos:** [archivo/chats/2026-06-29-synergium-propuesta-bioestadistica-encaje.md](chats/2026-06-29-synergium-propuesta-bioestadistica-encaje.md)

---

## 2026-06-29 — Outreach Tec Monterrey

- Mensajes y plantilla para doctorandos Tec Monterrey

**Artefactos:** [comercial/outreach/tec-monterrey/](../comercial/outreach/tec-monterrey/)

---

## 2026-08-14 — Community directory (Google Forms)

- Formularios ES/EN para matching en comunidad WhatsApp
- Playbook intros, mensajes WhatsApp, campos y privacidad
- Synergium no se nombra en el formulario

**Artefactos:** [comunidad/casos/formulario-agosto-2026/](../comunidad/casos/formulario-agosto-2026/)

---

## 2026-08-16 / 2026-08-17 — Web synergium.net

Intervenciones vía WordPress REST API (patrón bio-hpc.eu):

| Fecha | Caso | Qué |
|-------|------|-----|
| 2026-08-16 | selectores | Menú, iconos, páginas ES/EN |
| 2026-08-16 | upgrade-contenido | Contenido enganche + plugin SEO |
| 2026-08-17 | skus-restantes | Páginas SKU pendientes |
| 2026-08-17 | quitar-aviso-idiomas | Pie sin aviso idiomas duplicado |

**Artefactos:** [producto/web/synergium-net/casos/](../producto/web/synergium-net/casos/), backups en [producto/web/backups/](../producto/web/backups/)

---

## 2026-08-18 — Synergium Forms (forms.synergium.net)

- Decisión: PocketBase aparte de WordPress
- Deploy en VPS Explore Labs (217.154.191.98)
- Community directory EN publicado (`0mn7nfs5kqsi8g`)
- Pendiente: registro DNS A `forms` → IP en IONOS + SSL

**Artefactos:** [producto/forms/](../producto/forms/), [ops/scripts/synergium_forms_publish.py](../ops/scripts/synergium_forms_publish.py)

---

## 2026-08-19 — Copia local + push siempre

- Workspace local = clone de `horacioeps/synergium`
- Regla Cursor: `.cursor/rules/local-clone-siempre-push.mdc` (commit + push a `main` tras cada interacción, también si Horacio edita a mano)
- `HISTORICO.md` enlazado desde README

**Artefactos:** [AGENTS.md](../AGENTS.md), [HISTORICO.md](../HISTORICO.md)

---

## Pendientes conocidos

1. DNS `forms.synergium.net` en IONOS
2. SSL tras DNS (`producto/forms/deploy/scripts/enable_ssl.sh`)
3. Formulario Community directory ES
4. Buscador prospectos v2 (LinkedIn semi-manual)
5. Cierre comercial / primer contrato broker
