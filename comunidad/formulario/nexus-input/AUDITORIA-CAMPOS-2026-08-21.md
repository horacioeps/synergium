# Auditoría copy + campos — nexus-input (2026-08-21)

## Aplicado (pase completo)

- Etiquetas ES/EN profesionalizadas (usted / tono formal).
- Eliminados: `three_words`, `also_spanish_community`.
- Opcionales: `years_in_research` + bloque mercado (`last_unknown_collab_via`, `last_email_paper_author`, `follow_up_problem`, `recent_pubs_same_circle`, `institution_funds_intl`).
- Nuevos: `orcid`, `collab_modality`, `data_consent`.
- `how_found_form` al final (antes de `anything_else`).
- Mensaje de éxito y pie profesionales; notify incluye ORCID, consent y how found.

## Orden actual (37 campos)

## Heterogeneidad BD (aceptada)

Las submissions previas (sobre todo `source=google`) no se migran. Pueden tener claves que el form vivo ya no pide, y faltar las nuevas. Matching/exports: campos opcionales.

El sync Google usa `schema-en-google-sync.json` (labels antiguas ≈ Sheet), no el schema profesional vivo. Ver [GOOGLE-SHEET-SYNC.md](../../../producto/forms/docs/GOOGLE-SHEET-SYNC.md).
