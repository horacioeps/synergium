# Opciones de URL legible

**Elegido (2026-08-20):** **P** → `nexus-input`

| | |
|--|--|
| **URL canónica** | https://forms.synergium.net/nexus-input |
| **También aceptado** | `/nexus/input` (el front lo normaliza a `nexus-input`) |
| **Id legacy** | `0mn7nfs5kqsi8g` (redirigir / alias hasta rename en PocketBase) |

`public_id` es un solo segmento (`nexus-input`) porque la API `/api/sf/form/{id}` no admite `/` en el path. El patrón top/sub queda como **hyphen**: `nexus` + `input`.

## Aplicar en producción

```bash
# Con secrets SSH Horacio en el entorno:
bash producto/forms/deploy/scripts/apply_nexus_input.sh

# O solo rename vía API admin:
export SYNERGIUM_FORMS_PB_URL=https://forms.synergium.net
export SYNERGIUM_FORMS_PB_ADMIN_EMAIL=…
export SYNERGIUM_FORMS_PB_ADMIN_PASSWORD=…
python3 ops/scripts/synergium_forms_publish.py rename --from 0mn7nfs5kqsi8g --to nexus-input
```

---

## Histórico de propuestas (no aplicadas)

### Ronda 1 A–H

| # | URL | Notas |
|---|-----|--------|
| A–H | ver commits previos | Descartadas |

### Ronda 2 I–P

| # | URL | Top |
|---|-----|-----|
| I | `/win/input` | win |
| J | `/gain/input` | gain |
| K | `/collab/input` | collab |
| L | `/bridge/input` | bridge |
| M | `/rise/input` | rise |
| N | `/forge/input` | forge |
| O | `/leap/input` | leap |
| **P** | **`/nexus/input` → `nexus-input`** | **nexus** ✓ |
