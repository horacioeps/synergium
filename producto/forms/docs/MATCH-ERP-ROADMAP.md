# Match Pipeline — roadmap de campos

Complemento de [MATCH-TRACKING.md](MATCH-TRACKING.md). Colecciones PB actuales: `matches`, `match_participants`, `contact_events`.

## Must-have (próxima iteración)

| Campo | Colección | Tipo | Por qué |
|-------|-----------|------|---------|
| `intro_at` | `matches` | date | Fecha real de la intro conjunta; hoy solo `current_step=intro_done`. |
| `follow_up_due` | `matches` | date | Próxima acción de Horacio (nudge, paso 2, intro). Evita depender de memoria o tablero markdown. |
| `opt_in_deadline` | `matches` | date | Plazo acordado para respuesta opt-in; útil en pares geo distantes (#3, #5). |
| `submission` (enlace) | `match_participants` | relation → `submissions` | Ya existe el campo; falta poblarlo desde nexus-input por `respondent_email`. |
| `urgency` | `matches` | select (`low` / `normal` / `high`) | Priorizar bandeja cuando hay >10 pares activos. |

## Nice-to-have

| Campo | Colección | Tipo | Por qué |
|-------|-----------|------|---------|
| `geo_bridge` | `matches` | text | Nota operativa: husos, idioma puente, «HK↔AR async». |
| `wa_thread_id` | `match_participants` | text | Referencia a hilo WA (sin integrar API). |
| `last_contact_at` | `matches` | date | Denormalizado desde `contact_events` (el dashboard ya lo calcula al exportar). |
| `match_align_url` | `match_participants` | url | Enlace directo al form match-align con ref pre-rellenada. |
| `curator` | `matches` | text | Quién curó (`horacio`, agente, futuro operador). |
| `score_at_pairing` | `matches` | number | Score automático nexus-input en momento de curación (auditoría vs criterio manual). |
| `opt_in_language` | `match_participants` | select | `es` / `en` / … — idioma del borrador enviado (hoy en markdown). |
| `paired_at` auto | `matches` | date | Rellenar al pasar a `pairing_status=active` o doble sí opt-in. |

## Eventos / contact_events

| Mejora | Prioridad | Nota |
|--------|-----------|------|
| `body` completo en todos los outbound | must-have | Varios eventos del backfill solo tienen `notes`. |
| `thread_id` / `message_id` (email) | nice-to-have | Trazabilidad con Gmail/IMAP. |
| `response_latency_hours` (computed) | nice-to-have | Métrica comunidad. |

## UI / operaciones

| Ítem | Estado |
|------|--------|
| Dashboard HTML estático | Hecho — [match-dashboard](../deploy/pb_public/match-dashboard/index.html) |
| Export periódico | Script `export_match_dashboard.py`; re-ejecutar tras cambios en PB |
| Alertas vencidas (`follow_up_due`) | Pendiente — requiere campos + cron o revisión manual |

## No añadir (por ahora)

- Duplicar expediente markdown en PB (mantener `expediente_path` + historial humano).
- Renombrar colecciones PB (nombres técnicos estables; la marca es **Pipeline de matching** en UI).
