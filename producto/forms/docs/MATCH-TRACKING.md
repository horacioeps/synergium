# Pipeline de matching — PocketBase

**Nombre canónico:** **Pipeline de matching** (ES) · **Match Pipeline** (EN).

Evitar «ERP» en UI y comunicación con la comunidad: sugiere contabilidad/empresa, no curación de intros. En código y colecciones PB se mantienen nombres técnicos (`matches`, `match_participants`, `contact_events`). En docs internas «match pipeline» o «tracking PB» son alias aceptables.

**Estado:** colecciones en producción PocketBase (2026-08-22); `setup_collections.py` con merge de campos pairing v2. Datos iniciales vía `backfill_match_tracking.py`.

## Vista tabular (dashboard)

| Recurso | Ruta |
|---------|------|
| HTML | [deploy/pb_public/match-dashboard/index.html](../deploy/pb_public/match-dashboard/index.html) |
| Datos | `deploy/pb_public/match-dashboard/data.json` (generado) |
| Export | `python3 producto/forms/deploy/scripts/export_match_dashboard.py` |
| Producción | `https://forms.synergium.net/match-dashboard/` (tras rsync `pb_public/`) |
| Auth | HTTP Basic (usuario en VPS htpasswd); ver sección Seguridad abajo |
| Local | Abrir el HTML en navegador o servir la carpeta con `python3 -m http.server` |

### Pestañas

| Pestaña | Contenido |
|---------|-----------|
| **Por match** | Pares curados (`matches`) |
| **Por participante** | Pipeline por persona (`match_participants`) |
| **Directorio** | Submissions nexus-input con `match_me` ∈ `yes`, `directory_only`, `you_only_no_intro` (sin pruebas), con emparejamiento si existe |

Cabeceras de columna ordenables (asc/desc por clic); compatible con búsqueda.

Regenerar JSON tras cambios en PB o en el seed del backfill. Con credenciales admin usa PocketBase; si falla, cae al seed (`--seed-only` fuerza seed).

### Seguridad

`data.json` contiene **PII** (emails, WhatsApp). En producción el path `/match-dashboard/` exige **HTTP Basic Auth** (Apache `<Location>`). El formulario público y la API PB no se tocan.

**Configuración (VPS):**

```bash
# En ~/.cursor/secrets.env (local) o export en el VPS:
SYNERGIUM_MATCH_DASHBOARD_USER=synergium          # o horacio
SYNERGIUM_MATCH_DASHBOARD_PASSWORD='…'            # pragma: allowlist secret — no commitear

bash producto/forms/deploy/scripts/setup_match_dashboard_auth.sh
sudo a2enmod auth_basic authn_file
# Vhost: deploy/apache/forms.synergium.net.conf (+ bloque en :443 si certbot)
sudo apache2ctl configtest && sudo systemctl reload apache2
```

Sin contraseña configurada, Apache devuelve **401** hasta crear `~/synergium-forms/.htpasswd-match-dashboard` en el VPS.

**Histórico:** antes de 2026-08-22 el dashboard era estático público; cualquiera con la URL podía leer PII.

Roadmap de campos futuros: [MATCH-ERP-ROADMAP.md](MATCH-ERP-ROADMAP.md).

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

## Emparejamiento (v2)

Campos que responden: **¿ya emparejado?**, **cómo** y **cuándo se propuso** (curación, no opt-in).

### `matches` (nivel par)

| Campo | Tipo | Valores / uso |
|-------|------|----------------|
| `pairing_status` | select | `proposed` · `active` · `rejected` · `completed` · `discarded` |
| `pairing_method` | select | `curated_manual` · `auto_score` · `plan_b` · `user_requested` |
| `proposed_at` | date | Fecha de curación / propuesta del match |
| `paired_at` | date | Opcional: cuando el emparejamiento se confirma (doble sí, intro, etc.) |

`pairing_status` ≠ `current_step`: el primero es **relación propuesta/activa**; el segundo es **pipeline de contacto** (opt-in → match-align → intro).

### `match_participants` (nivel persona)

| Campo | Tipo | Uso |
|-------|------|-----|
| `is_paired` | bool | Sí si esta persona está en un match curado (aunque opt-in pendiente) |
| `paired_with_email` | email | Email de la contraparte en este match |
| `pairing_proposed_at` | date | Cuándo se les propuso este emparejamiento |

### Ejemplo match #7 (`match-2026-007`)

| Campo | Valor |
|-------|-------|
| `pairing_status` | `proposed` |
| `pairing_method` | `curated_manual` |
| `proposed_at` | `2026-08-21` (curado en MATCHES.md; expediente creado 2026-08-22) |
| `paired_at` | — |
| Michelle `is_paired` | `true` |
| Michelle `paired_with_email` | `kblanco@una.cr` |
| Kinndle `paired_with_email` | `michelle.vierarom@ug.edu.ec` |

## Flujo operativo (agente)

1. **Curar match** → crear expediente en `clientes/matches/<slug>/` (como siempre) **y** registro en PB (`matches` + 2 `match_participants`).
2. **Enviar opt-in** → `contact_event` outbound `opt_in` con `body` completo; actualizar `matches.current_step` y `match_participants.current_step`.
3. **Respuesta** → `contact_event` inbound `inbound_reply`; si sí → `opt_in_yes` en participante.
4. **Paso 2** → `match_align` outbound; ref `match-2026-00N` en notas/campo.
5. Los markdown `historial-contacto.md` **siguen actualizándose** en paralelo (fuente humana); PB es la vista operativa del pipeline.

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

1. **Ejecutar `setup_collections.py` en producción** si faltan campos v2 (pairing merge).
2. **Re-ejecutar backfill** tras añadir pairing fields o editar seed.
3. **Export dashboard:** `export_match_dashboard.py` → commit `data.json` o regenerar en deploy.
4. Opcional: enlazar `match_participants.submission` buscando por `respondent_email` en nexus-input.
5. Match #7: opt-in **pendiente de envío** (borradores ES en expediente; PB sin `contact_events` opt-in).
