# Arquitectura — Synergium Forms

## Cómo se hace (sin alternativas)

Ver **[COMO-HACERLO.md](COMO-HACERLO.md)**:

- Host: **VPS Explore Labs** (IP distinta del WordPress synergium.net)
- Tú das directrices en chat; el **agente publica por API** (sin que toques paneles)
- PocketBase + front mínimo + email SMTP

## Veredicto corto

**No uses la base de WordPress de synergium.net como almacén principal de respuestas.**  
Servicio en `forms.synergium.net` en el VPS Explore Labs + notificaciones por SMTP/Resend.

---

## Requisitos (lo que pediste)

1. Formularios tipo Google Form
2. URL con código: `forms.synergium.net/<codigo>`
3. Abiertos a quien tenga el enlace (sin login)
4. Respuestas en BD
5. Email cada vez que alguien complete una encuesta
6. Primer form: Community directory (muchas preguntas, multi-checkbox, textos largos, PII)

---

## Comparación de candidatos

| Opción | Encaje URL | BD propia | Email | Matching futuro | Esfuerzo | Veredicto |
|--------|------------|-----------|-------|-----------------|----------|-----------|
| **A. App propia + Postgres** | Ideal (`/<id>`) | Sí | Sí (SMTP/Resend) | Excelente (SQL/JSON, export, scripts) | Medio | **Recomendada** |
| **B. Plugin WP** (Fluent Forms / Gravity / Formidable) | Regular (slugs en synergium.net o rewrite raro) | Misma MySQL que WP | Sí nativo | Regular (tablas plugin, export CSV) | Bajo–medio | Solo si quieres cero infra nueva |
| **C. Tally / Fillout / Typeform** + custom domain | Bueno | En su cloud (export) | Sí | Débil (dependes de ellos) | Muy bajo | Puente temporal |
| **D. Google Forms** (estado actual EN) | `forms.gle/…` | Sheets | Sí | Malo para matching serio | Cero | Solo mientras migras |
| **E. Airtable / Notion forms** | No marca | En su cloud | Webhooks | Medio | Bajo | No recomendado (PII + marca) |

---

## Por qué no la BD de WordPress

Synergium.net ya es WP (Twenty Twenty-Five, REST, ES/EN). Meter ahí las respuestas del directorio mezcla:

- **PII sensible** (email, WhatsApp, consentimiento de intros) con el CMS de marketing
- Backups, plugins y actualizaciones WP = superficie de riesgo sobre datos de matching
- Consultas de matching (filtros por área, offer/need, geo, idioma) son incómodas en `wp_postmeta` / tablas de plugins
- La URL `forms.synergium.net/codigo` no es natural en WP: o creas un WP aparte solo para forms (doble mantenimiento) o rewrites frágiles

Un plugin WP **sí** puede servir si priorizas “mañana en producción” y aceptas export CSV + email. Para un directorio que vas a cruzar a mano (y luego semi-automático), conviene datos limpios fuera del CMS.

---

## Diseño recomendado (opción A)

```
                    ┌─────────────────────┐
  Usuario ─────────▶│ forms.synergium.net │  (app: Astro/Next o PHP mínimo)
  (solo enlace)     │  GET /:publicId      │
                    │  POST /:publicId     │
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         PostgreSQL      Email notify     Admin (tú)
         forms +         (SMTP / Resend)  /admin (auth)
         submissions     → info@ o personal
```

### Componentes

1. **DNS:** `forms.synergium.net` → VPS (Cloudflare/proxy o A record). Puede ser el mismo servidor que WP o uno pequeño aparte.
2. **App pública:** renderiza el form por `public_id` (nanoid ~12–16 chars). Sin listado público de formularios.
3. **BD:** PostgreSQL preferido (JSON nativo para respuestas). Alternativa: MariaDB en el mismo VPS, **base distinta** de `wordpress_*`.
4. **Email:** al insertar submission → enviar correo con resumen + enlace admin. Reutilizar SMTP que ya uses, o Resend/Postmark.
5. **Admin:** login solo para ti (crear forms, ver respuestas, export CSV, cerrar form). No hace falta panel fancy al inicio.

### Modelo mínimo

- `forms`: id, public_id, title, description, schema (JSON de campos), status (open/closed), notify_email, created_at
- `submissions`: id, form_id, answers (JSONB), ip_hash opcional, user_agent, created_at
- Opcional: `submission_events` si quieres auditar emails enviados

Detalle: [modelo-datos.md](modelo-datos.md).

### Seguridad (público con enlace)

- El `public_id` es el secreto: no indexar (`noindex`), no sitemap, no listado
- Rate limit por IP en POST (anti-spam)
- Honeypot + opcional Turnstile/hCaptcha
- HTTPS obligatorio
- No loguear cuerpos completos en access logs
- Derecho de borrado: borras la fila `submissions` (WhatsApp, como ya dices en el copy)

### Branding

Misma paleta/favicon que synergium.net; el form no necesita el resto del sitio. Footer corto + privacidad.

---

## Opción B (WP) — si eliges velocidad máxima

Plugin: **Fluent Forms** (bueno precio/calidad) o **Gravity Forms**.

- Crear el Community directory como un form
- Notificaciones nativas a tu email
- Entradas en tablas del plugin (misma MySQL WP)
- URL: `https://synergium.net/forms/<slug>` o página con slug opaco  
  Para `forms.synergium.net`: subdomain → mismo WP + plugin de domain mapping / rewrite, o un second site en multisite (más lío)

Úsala solo como **fase 0** si necesitas el form EN/ES esta semana y luego migrar CSV → Postgres.

---

## Opción C — puente sin código

**Tally** o **Fillout** con custom domain `forms.synergium.net`:

- URLs limpias, email, export
- Datos en su cloud (DPA/GDPR a revisar: WhatsApp + email de investigadores)
- Webhook → tu BD más adelante

Válido 2–4 semanas; no como casa definitiva del directorio.

---

## Email al completar

En opción A (recomendado):

1. Tras `INSERT` exitoso en `submissions`
2. Enviar a `notify_email` del form (p.ej. tu Gmail o `info@synergium.net`)
3. Asunto: `[Synergium Forms] Community directory — {nombre}`
4. Cuerpo: campos clave (nombre, email, WhatsApp, country, role, need, match me?) + link a admin
5. Cola simple (tabla `outbox` o envío síncrono primero; si falla SMTP, reintento)

No hace falta WordPress para el correo.

---

## Ruta de implementación sugerida

1. **Ahora:** este diseño + schema del Community directory (hecho en `casos/`).
2. **MVP:** un solo form hardcodeado o schema JSON + Postgres + email + URL pública.
3. **Después:** UI admin para crear más forms (otros pedidos Synergium: Snapshot intake, Consorcio, etc.).
4. **Matching:** scripts/SQL sobre `answers` (ya tienes `playbook-matching.md` del caso Google Forms).

### Stack concreto sugerido (MVP)

| Pieza | Elección práctica |
|-------|-------------------|
| Host | Mismo VPS Explore Labs o un contenedor pequeño |
| Runtime | Node (Astro SSR / Next) **o** PHP/Laravel ligero si prefieres alinear con hosting WP |
| BD | PostgreSQL 16 (Docker) o Supabase free si quieres managed |
| Auth admin | Magic link o usuario/clave única + session |
| Email | Resend API o SMTP existente |
| ID público | `nanoid(12)` URL-safe |

Si quieres cero Node: **Laravel + Filament** o incluso **PocketBase** (SQLite/Postgres + API + admin) detrás de Caddy en `forms.`.

**PocketBase** es candidato fuerte para MVP ultra-rápido: forms + submissions + admin + email hooks, URL `/_/` admin y app front mínima que lea el form por id.

---

## Qué no hacer

- Guardar respuestas solo en Google Sheets a largo plazo
- Meter PII del directorio en Contact Form 7 / HTML estático de la home
- Indexar formularios en Google
- Reutilizar Application Passwords de WP para esto

---

## Decisión para confirmar contigo

| Pregunta | Recomendación por defecto |
|----------|---------------------------|
| ¿Dónde la BD? | **Postgres aparte** (no tablas WP) |
| ¿Dónde la app? | `forms.synergium.net` |
| ¿WP? | Solo marketing; enlace opcional desde la web |
| ¿Primer form? | Community directory (schema en el caso) |
| ¿Mientras tanto? | Seguir con Google Forms EN si ya está vivo; migrar cuando el MVP esté listo |
