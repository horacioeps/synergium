# Modelo de datos — Synergium Forms

## Principio

Cada formulario tiene un **schema JSON** (definición de campos). Cada respuesta guarda un **answers JSONB** (valores). Así no hace falta migrar columnas por cada form nuevo.

Para matching frecuente se pueden añadir columnas materializadas o vistas más adelante (`role`, `country`, `match_me`, etc.).

---

## Tablas

### `forms`

| Columna | Tipo | Notas |
|---------|------|--------|
| `id` | uuid PK | interno |
| `public_id` | text UNIQUE | lo que va en la URL (`jha76sd8a78sda`) |
| `slug` | text NULL | opcional legible solo en admin |
| `title` | text | |
| `description` | text | markdown/plain |
| `locale` | text | `en` / `es` |
| `schema` | jsonb | lista de campos (ver abajo) |
| `status` | text | `draft` \| `open` \| `closed` |
| `notify_email` | text | destino del aviso |
| `success_message` | text | post-submit |
| `created_at` | timestamptz | |
| `updated_at` | timestamptz | |
| `closed_at` | timestamptz NULL | |

Índice: `UNIQUE(public_id)`.

### `submissions`

| Columna | Tipo | Notas |
|---------|------|--------|
| `id` | uuid PK | |
| `form_id` | uuid FK → forms | |
| `answers` | jsonb | mapa `field_id → value` |
| `respondent_email` | text NULL | denormalizado si existe campo email |
| `source` | text | `web` \| `google` (origen del alta) |
| `ip_hash` | text NULL | hash, no IP en claro |
| `user_agent` | text NULL | |
| `created_at` | timestamptz | |

Índices: `(form_id, created_at DESC)`; GIN opcional sobre `answers`.

### `notification_log` (opcional MVP+)

| Columna | Tipo | Notas |
|---------|------|--------|
| `id` | uuid PK | |
| `submission_id` | uuid FK | |
| `channel` | text | `email` |
| `status` | text | `sent` \| `failed` |
| `error` | text NULL | |
| `sent_at` | timestamptz | |

---

## Schema de campo (dentro de `forms.schema`)

```json
{
  "version": 1,
  "fields": [
    {
      "id": "full_name",
      "type": "text",
      "label": "Full name",
      "required": true
    },
    {
      "id": "areas",
      "type": "multi_select",
      "label": "Areas (tick all that apply)",
      "required": true,
      "options": [
        { "value": "biomed", "label": "Biomed/health/pharma" }
      ],
      "allow_other": true
    }
  ]
}
```

### Tipos soportados (MVP)

| type | UI | Value en answers |
|------|-----|------------------|
| `text` | input | string |
| `email` | email | string |
| `phone` | tel | string |
| `textarea` | textarea | string |
| `single_select` | radio | string (value) |
| `multi_select` | checkboxes | string[] |
| `url_list` | textarea (1 URL/línea) | string[] |
| `section` | solo título/ayuda | — (no se guarda) |

`allow_other: true` → si eligen Other, guardar `{ "value": "other", "other_text": "…" }` o convención fija.

---

## Ejemplo mínimo SQL (Postgres)

```sql
CREATE TABLE forms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  public_id text NOT NULL UNIQUE,
  title text NOT NULL,
  description text NOT NULL DEFAULT '',
  locale text NOT NULL DEFAULT 'en',
  schema jsonb NOT NULL,
  status text NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'open', 'closed')),
  notify_email text NOT NULL,
  success_message text NOT NULL DEFAULT 'Thanks. Your answers were saved.',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  closed_at timestamptz
);

CREATE TABLE submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  form_id uuid NOT NULL REFERENCES forms(id) ON DELETE CASCADE,
  answers jsonb NOT NULL,
  respondent_email text,
  ip_hash text,
  user_agent text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX submissions_form_created_idx
  ON submissions (form_id, created_at DESC);
```

---

## Export y matching

- CSV: aplanar `answers` por `field_id`
- Matching: filtrar por JSON (`answers->>'country'`, `answers->'need_now'`, etc.) o materializar columnas en una vista `v_community_directory`
