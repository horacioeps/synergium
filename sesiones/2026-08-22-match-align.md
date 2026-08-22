# Sesión 2026-08-22 — match-align v0 + email Rivas

## Usuario

> otra cosa para la segunda fase, creo que habria que pasar un formulario… (diseño fase 2, preguntas, monetización Synergium)

> crea la v0 del nuevo formulario match aling… y preparar correo para enviar al rivas… ¿lo hemos hecho?

## Agente

- Opinión: form A2 antes de intro conjunta; ambos rellenan; separa encaje / condiciones / acompañamiento.
- **v0 `match-align`:** `comunidad/formulario/match-align/schema-en.json` + `schema-es.json` + i18n desplegado.
- Publicado en PB: https://forms.synergium.net/match-align (status open).
- Borrador opt-in Matías: `clientes/piloto/matias-rodriguez-rivas/emails-optin-borrador.md`.
- **No** se había enviado opt-in del match a Matías (solo email PDF 6-ago + form 14-ago). Valentina sí dijo sí por WA.

---

## Usuario (2026-08-22 ~16:43)

> Referencia abstracta (no matias-valentina). Opciones alfabéticas + Otro. Idioma como nexus-input. Cambiar «reunión facilitada» → aclaración email/WA. Añadir NDA e intención de patentar.

## Agente (v2)

- `schema-en.json` / `schema-es.json` → **version 2** (26 campos).
- `match_reference` ejemplo `match-2026-042`; `work_language` → `match_language` (8 idiomas + Other).
- `conditions_clarity`: `clarification` (email/WhatsApp Synergium).
- Nuevos: `nda_required`, `patent_intention`; `possible_ip` renombrado (otra PI).
- `allow_other` en selects; opciones orden alfabético.
- Publicado PB + i18n `match-align.es.json` desplegado en VPS.
- URL: https://forms.synergium.net/match-align

---

## Usuario (2026-08-22 ~16:54)

> mira lo que hesta puesto en esta sesion "" y haz lo pendiente de mejorar el formulario, te queda clar o??

(Referencia: sesión match-align + feedback 16:43 que no se había desplegado del todo.)

## Agente

- Schemas v2 ya en disco; completado: i18n ES sincronizado, publish PB, rsync i18n VPS, README v2.

---

## Usuario (2026-08-22 ~17:01)

> /guarda-sesion-y-demas

## Agente

- Volcado sesión + README; commit + push `main`.
