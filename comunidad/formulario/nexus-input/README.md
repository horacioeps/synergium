# Caso: Community directory — matching researchers

Formulario de ejemplo para arrancar Synergium Forms.  
Origen: copy vivo del form EN (Google) + spec `generado/comunidad-whatsapp/casos/2026-08-14-formulario-matching/`.

## Metadatos sugeridos

| Campo | Valor |
|-------|--------|
| `title` | Community directory — matching researchers with each other |
| `locale` | `en` (ES = segundo form o `locale=es` con mismo schema ids) |
| `status` | `open` |
| `notify_email` | email que uses para intros (personal o info@) |
| `public_id` | `nexus-input` (antes nanoid `0mn7nfs5kqsi8g`) |
| URL | `https://forms.synergium.net/nexus-input` |

## Descripción (intro)

```
This is a one-time directory of this community. I will use the answers to introduce members who could collaborate — a joint paper, a grant partner, a method, a research stay, or feedback. It is free and takes about 8–10 minutes. Please be specific: vague answers are hard to match. I will not sell or share your data with third parties. If I make an introduction, I will pass on only the details you authorise at the end. To request deletion, message me on WhatsApp.
```

## Campos (orden de UI)

Fuente de verdad: `schema-en.json` / `schema-es.json` e i18n desplegado (`37` campos tras pase 2026-08-21).

Cambios relevantes:

- Tono profesional ES/EN; mensaje de éxito formal.
- Eliminados: `three_words`, `also_spanish_community`.
- Opcionales: `years_in_research` + bloque mercado (últimas vías de colaboración / email a autores / follow-up / círculo de pubs / fondos intl).
- Nuevos: `orcid`, `collab_modality`, `data_consent`, `how_found_form`.

Detalle: [AUDITORIA-CAMPOS-2026-08-21.md](AUDITORIA-CAMPOS-2026-08-21.md).

## Condicionales

- `share_with_match` visible solo si `match_me === "yes"`.
- Mensaje de confirmación: formal (equipo Synergium; canal indicado).

## Email de aviso (plantilla)

**Asunto:** `[Synergium Forms] Community directory - {full_name}`

**Cuerpo (resumen):**

```
New submission ({created_at} UTC)
Form: Community directory
URL admin: …

Name: {full_name}
Email: {email}
WhatsApp: {whatsapp}
ORCID: {orcid}
Data consent: {data_consent}
How found form: {how_found_form}
Country / city: {country} / {city}
Role: {role} @ {institution}
Match me?: {match_me}
Need: {need_now}
Offer: {offer_next_months}
Seek: {what_you_seek}
Intro channel: {intro_channel}
```

## Notas de producto

- No nombrar Synergium en el copy del form (comunidad WhatsApp / podcast); la marca solo en el dominio si quieres, o footer neutro.
- Misma estructura ids para versión ES → matching unificado en BD.
- Migración desde Google Forms: export CSV → mapear columnas a `field_id` → `INSERT` en `submissions`.

## Archivos relacionados

- Spec Google previo: `generado/comunidad-whatsapp/casos/2026-08-14-formulario-matching/`
- Arquitectura: `generado/synergium-forms/docs/arquitectura.md`
