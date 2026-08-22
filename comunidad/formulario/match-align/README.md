# Caso: match-align — fase 2 (condiciones y alineación)

Brief corto **después** del sí al match en `nexus-input` y **antes** de la intro conjunta. Cada parte del par lo rellena por separado.

## Metadatos

| Campo | Valor |
|-------|--------|
| `public_id` | `match-align` |
| `locale` | `en` (ES nativo vía `i18n/match-align.es.json`) |
| `status` | `open` (v0) |
| URL | `https://forms.synergium.net/match-align` |

## Flujo

1. Opt-in bilateral (email/WhatsApp) sin nombre del otro hasta que ambos digan sí.
2. Enlace `match-align` a cada uno con referencia `matias-valentina` (campo `match_reference`).
3. Cuando **ambos** envían → resumen 1 página → intro conjunta (playbook).

## Campos (v2)

26 campos: identidad, objetivo 4–12 semanas, rol/tiempo, idioma (`match_language` = selector web), autoría, datos/ética, NDA (`nda_required`), patentes (`patent_intention`), otra PI, plan de no negocio (`not_this_collab`), bifurcación A3 (`conditions_clarity` = aclaración email/WA), check-in Synergium, consentimiento resumen.

Opciones en orden alfabético; `allow_other` en selects (excepto consentimiento binario). Referencia abstracta (`match-2026-042`), sin nombres de personas.

Fuente de verdad: `schema-en.json` / `schema-es.json`.

## Próximas mejoras (v1+)

- Pre-relleno por URL (`?ref=matias-valentina`)
- Bloque contexto del match (solo lectura)
- Versión abreviada si ambos marcan `conditions_clarity=clear`
- Export automático del resumen para la intro

## Relacionado

- Embudo A2: `hoy/tableros/EMBUDOS.md`
- Piloto: `clientes/piloto/matias-rodriguez-rivas/`
