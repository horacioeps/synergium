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

| # | id | type | required | label / opciones |
|---|-----|------|----------|------------------|
| 1 | `full_name` | text | sí | Full name |
| 2 | `email` | email | sí | Email (one you actually check) |
| 3 | `whatsapp` | phone | sí | WhatsApp with country code (e.g. +1 415 555 2671) |
| 4 | `country` | text | sí | Country you live/work in |
| 5 | `city` | text | no | City (optional; timezone/local) |
| 6 | `match_language` | single_select + other | sí | Spanish / English / Either/both / Other |
| 7 | `role` | single_select + other | sí | Undergrad/master, PhD, Postdoc, Researcher (not PI), PI/group leader, Technician/lab manager, TTO/innovation office, Vice-rectorate/research mgmt, Science agency/funding, Company/startup/industry, Independent, Other |
| 8 | `institution` | text | sí | Institution (or independent) |
| 9 | `institution_type` | single_select + other | sí | Public uni, Private uni, Research centre, Hospital/clinic, Company/startup, NGO/foundation, Independent, Other |
| 10 | `years_in_research` | single_select | sí | \<2, 2–5, 6–10, 11–20, \>20, N/A |
| 11 | `areas` | multi_select + other | sí | Biomed/health/pharma, Bioinformatics, Chemistry/materials/nano, AI/data for science, HPC/simulation, Agri-food/bioeconomy, Energy/environment, Engineering/devices, Social sciences, Humanities/phil of science/history, Archaeology/heritage, Education, Tech transfer/spin-offs, Other |
| 12 | `what_you_do` | textarea | sí | In 3–5 sentences, what you do now… |
| 13 | `methods` | multi_select + other | sí | Experimental, Computational/data, Theoretical, Clinical, Fieldwork, Archive/humanities, Transfer/project mgmt, Other |
| 14 | `keywords` | textarea | sí | Keywords/techniques (5–12 terms) |
| 15 | `profile_urls` | url_list | no | ORCID/Scholar/LinkedIn/web (one URL per line) |
| 16 | `offer_next_months` | multi_select + other | sí | Method/protocol, Data/samples/field/archive, Compute/HPC, Clinical access, Host a stay, Students/lab hands, Review/feedback, Industry contacts, Europe/Horizon network, LATAM/local network, Teaching, Thesis co-supervision, Not sure, Other |
| 17 | `need_now` | multi_select + other | sí | Joint paper, Grant/consortium partner, Method I lack, Data/samples/clinical/field, Stay/mobility, Industry/transfer partner, Thesis co-supervision, Review/feedback, Career mentoring, Outreach/podcast, Compute/HPC, Not sure want directory, Other |
| 18 | `what_you_seek` | textarea | sí | In your words: what you seek… |
| 19 | `geo_preferences` | multi_select | sí | Same country, Latin America, Europe, North America, Anywhere, Specific country (write it in “what you seek”) |
| 20 | `time_horizon` | single_select | sí | This month, ~3 months, This year, No rush |
| 21 | `specific_call` | textarea | no | Specific call now? Name, role needed, deadline. Else blank. |
| 22 | `blockers` | multi_select + other | sí | Authors don't reply, Always same coauthors, Don't know who, Ignored as junior/not PI, No follow-up, Trust/fit, Language, No institutional funds, TTO slow, Visa/admin, Time zone, Haven't tried, Other |
| 23 | `last_unknown_collab_via` | single_select + other | sí | PhD/diaspora/supervisor, Conference, Email paper author, LinkedIn, TTO, Formal network (COST etc), This community/podcast, Almost never, Other |
| 24 | `last_email_paper_author` | single_select | sí | Replied+led somewhere, Replied+died, No reply, Never, \>1 year don't remember |
| 25 | `follow_up_problem` | single_select | sí | Yes routinely, Sometimes, No, No external collabs yet |
| 26 | `recent_pubs_same_circle` | single_select | sí | Almost always, Half, Different groups, Publish little/N/A |
| 27 | `institution_funds_intl` | single_select | sí | Yes I know, Think so, No, Don't know |
| 28 | `match_me` | single_select | sí | Yes / Only you see data, no intro yet / Directory only, no intros |
| 29 | `share_with_match` | multi_select | cond. | Si match_me=Yes: Name/area/country, Email, WhatsApp, LinkedIn/ORCID, The need I described, Nothing only you |
| 30 | `intro_channel` | single_select | sí | WhatsApp, Email, LinkedIn, Whatever |
| 31 | `later_write` | single_select | sí | Yes / Only if clearly useful / No, matching only |
| 32 | `english_for_collab` | single_select | sí | Fluent, Get by, Spanish only, English is working language |
| 33 | `also_spanish_community` | single_select | sí | Both / Only this (EN) / Didn't know there was another |
| 34 | `three_words` | text | sí | 3 words to be found by |
| 35 | `how_found_form` | single_select | sí | WhatsApp, Discord, Email, colleague, university, LinkedIn, podcast, Synergium web (+ Other) |
| 36 | `anything_else` | textarea | no | Anything else to match you |

Auditoría tono/campos: [AUDITORIA-CAMPOS-2026-08-21.md](AUDITORIA-CAMPOS-2026-08-21.md).

## Condicionales

- `share_with_match` visible/required solo si `match_me === "yes"`.
- Mensaje de confirmación (ajustes, no en descripción): “Thanks — saved. If you authorised intros, I may contact you on the channel you chose.”

## Email de aviso (plantilla)

**Asunto:** `[Synergium Forms] Community directory — {full_name}`

**Cuerpo (resumen):**

```
New submission ({created_at} UTC)
Form: Community directory
URL admin: …

Name: {full_name}
Email: {email}
WhatsApp: {whatsapp}
Country / city: {country} / {city}
Role: {role} @ {institution}
Match me?: {match_me}
Need NOW: {need_now}
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
