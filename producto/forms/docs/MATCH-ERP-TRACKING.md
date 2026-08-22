# Match pipeline ERP — PocketBase

**Estado:** implementado en repo 2026-08-22. Colecciones creadas por `setup_collections.py`; datos iniciales vía `backfill_match_tracking.py`.

## Por qué

Los expedientes en `clientes/matches/` siguen siendo la fuente legible para humanos y agentes. PocketBase añade **consulta estructurada**: paso actual, emails enviados/recibidos, y cuerpo completo de mensajes sin depender de parsear markdown.

## Colecciones

| Colección | Nivel | Uso |
|-----------|-------|-----|
| `matches` | Par | Un registro por match curado (#1–#7). `match_reference`, `current_step`, contactos A/B, ruta expediente. |
| `match_participants` | Persona × match | Paso individual (`opt_in_yes`, `match_align_done`, …), WhatsApp, enlace opcional a `submissions`. |
| `contact_events` | Evento | Cada email/WA/nota: tipo, canal, dirección, fechas, asunto, **body**, emails. |

Schema JSON (referencia): [deploy/schemas/match-tracking.schema.json](../deploy/schemas/match-tracking.schema.json).

### `matches.current_step`

| Valor | Significado |
|-------|-------------|
| `curated` | Match elegido; opt-in no enviado |
| `opt_in_sent` | Opt-in enviado a ambos; sin respuestas |
| `opt_in_partial` | Al menos un sí, otro pendiente |
| `opt_in_complete` | Doble sí opt-in |
| `match_align_partial` | Al menos un brief enviado/completado |
| `match_align_complete` | Ambos briefs |
| `intro_done` | Intro conjunta hecha |
| `closed` | Cerrado sin intro |

### `match_participants.current_step`

`directory` → `opt_in_pending` → `opt_in_yes` / `opt_in_no` → `match_align_pending` → `match_align_done` → `intro_done`.

### `contact_events.event_type`

`opt_in` | `match_align` | `intro` | `follow_up` | `inbound_reply` | `note`

## Flujo operativo (agente)

1. **Curar match** → crear expediente en `clientes/matches/<slug>/` (como siempre) **y** registro en PB (`matches` + 2 `match_participants`).
2. **Enviar opt-in** → `contact_event` outbound `opt_in` con `body` completo; actualizar `matches.current_step` y `match_participants.current_step`.
3. **Respuesta** → `contact_event` inbound `inbound_reply`; si sí → `opt_in_yes` en participante.
4. **Paso 2** → `match_align` outbound; ref `match-2026-00N` en notas/campo.
5. Los markdown `historial-contacto.md` **siguen actualizándose** en paralelo (fuente humana); PB es la vista ERP.

## Deploy / migración

En VPS (o local con PB + secrets):

```bash
set -a; source ~/.cursor/secrets.env; set +a
export SYNERGIUM_FORMS_PB_URL="${SYNERGIUM_FORMS_PB_URL:-https://forms.synergium.net}"

# 1. Crear/actualizar colecciones
python3 producto/forms/deploy/scripts/setup_collections.py

# 2. Backfill desde expedientes conocidos (idempotente)
python3 producto/forms/deploy/scripts/backfill_match_tracking.py

# Dry-run
python3 producto/forms/deploy/scripts/backfill_match_tracking.py --dry-run
```

Tras cambiar `setup_collections.py`, rsync + restart como en [COMO-HACERLO.md](COMO-HACERLO.md) (`apply_nexus_input.sh` o deploy manual).

## API (admin)

Solo superuser. Ejemplos:

```bash
# Match #7
curl -s "$SYNERGIUM_FORMS_PB_URL/api/collections/matches/records?filter=match_reference='match-2026-007'" \
  -H "Authorization: $TOKEN"

# Eventos de un match
curl -s "$SYNERGIUM_FORMS_PB_URL/api/collections/contact_events/records?filter=match_reference='match-2026-007'&sort=-sent_at" \
  -H "Authorization: $TOKEN"
```

## Relación con forms existentes

- `submissions` (nexus-input) = entrada al directorio.
- `match_participants.submission` = enlace opcional cuando se conozca el `submission.id` por email.
- `match-align` submissions **no** se enlazan aún en v0; el campo `match_reference` del form identifica el par.

## Backfill

`backfill_match_tracking.py` incluye seed de matches #1–#7 a partir de `clientes/*/historial-contacto.md` (estado 2026-08-22). No parsea markdown automáticamente; ampliar el array `MATCHES` al añadir contactos nuevos o re-ejecutar tras editar el seed.

## Manual steps

1. **Ejecutar `setup_collections.py` en producción** (colecciones no existen hasta deploy).
2. **Ejecutar backfill** una vez creadas las colecciones.
3. Opcional: enlazar `match_participants.submission` buscando por `respondent_email` en nexus-input.
