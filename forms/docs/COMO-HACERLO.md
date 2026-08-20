# Cómo hacerlo (decisión única)

Sin menú de opciones: **esto** es lo que hay que montar.

## Qué quieres (flujo operativo)

Tú **no tocas ningún panel**. El flujo es:

1. Me das directrices en el chat (texto del form, campos, idioma, a quién notificar).
2. Yo genero el schema en el repo (`generado/synergium-forms/casos/…`).
3. Yo lo **publico por API** (script + token de admin).
4. Te devuelvo el enlace `https://forms.synergium.net/<codigo>`.
5. Tú solo compartes ese enlace (WhatsApp, email, etc.).
6. Cuando alguien responde → te llega un email; yo puedo listar/exportar respuestas también por API si lo pides.

El panel de PocketBase existe solo como backend técnico; **tú no lo usas**. Las credenciales viven en secrets del entorno del agente.

---

## ¿Qué VPS?

Hay **dos máquinas distintas** en IONOS:

| Qué | IP (ago 2026) | Rol |
|-----|----------------|-----|
| **synergium.net** (WordPress) | `217.160.0.160` | Web marketing Synergium |
| **VPS Explore Labs** (`EXPLORE_LABS_SSH_HOST`) | `217.154.191.98` | SaaS Explore Labs, vault Sync headless, EmailerX, etc. |

Cuando dije “VPS”, me refería al **VPS de Explore Labs** (`217.154.191.98`), **no** al hosting donde está el WordPress de synergium.net.

Ahí montamos PocketBase (Docker). El DNS de `forms.synergium.net` debe apuntar a **ese** VPS (A/AAAA o CNAME), no al IP del WP.

WordPress de synergium.net **no se toca** para almacenar encuestas.

---

## Qué es el sistema

La URL que ve la gente (y la que tú compartes) es siempre bajo **`forms.synergium.net`**:

`https://forms.synergium.net/<codigo>`

Ejemplo: `https://forms.synergium.net/jha76sd8a78sda`

Eso es un **subdominio de Synergium**, aunque el servidor detrás sea el VPS Explore Labs. Quien abre el enlace no ve Explore Labs ni WordPress: solo `forms.synergium.net`.

Quien tenga el enlace rellena. Respuestas en BD (PocketBase). Email a ti al enviar.

## Stack fijo

| Pieza | Elección |
|-------|----------|
| Host | **VPS Explore Labs** (pm2 + Apache; sin Docker) |
| Backend | **PocketBase** |
| Front público | SPA en `/var/www/forms.synergium.net` (Apache FallbackResource) |
| Publicación | **API + script** desde el agente (no UI) |
| Email | Hook PocketBase → SES SMTP (mismo que EmailerX) |
| DNS | `forms.synergium.net` → IP del VPS Explore Labs |

## Flujo agente (crear una encuesta)

```
Tú (chat)  →  schema JSON en repo  →  scripts/synergium_forms_publish.py
                                         │
                                         ▼
                                   PocketBase Admin API
                                         │
                                         ▼
                              public_id + status=open
                                         │
                                         ▼
                         https://forms.synergium.net/{public_id}
```

Comandos típicos (los ejecuto yo):

- `publish` — crea/actualiza form y lo deja abierto  
- `close` — cierra un `public_id`  
- `list` — lista forms  
- `export` — CSV de respuestas de un form  

Secrets necesarios (nombres, no valores en el repo):

- `SYNERGIUM_FORMS_PB_URL` — p.ej. `https://forms.synergium.net`  
- `SYNERGIUM_FORMS_PB_ADMIN_EMAIL` / `SYNERGIUM_FORMS_PB_ADMIN_PASSWORD` (o token)  
- SMTP para notificaciones  

Acceso VPS: reutilizar `EXPLORE_LABS_SSH_*` para el deploy inicial.

## Colecciones PocketBase

**`forms`:** `public_id`, `title`, `description`, `locale`, `schema` (json), `status`, `notify_email`, `success_message`  

**`submissions`:** `form`, `answers` (json), `respondent_email`  

Reglas: público solo puede **crear** submissions si el form está `open`. Listar/editar = solo admin (el agente).

## Orden de puesta en marcha (una vez)

1. DNS: `forms.synergium.net` → IP VPS Explore Labs (tú o yo si hay API DNS IONOS).  
2. En el VPS: PocketBase (pm2) + Apache.  
3. Colecciones + reglas + secret del agente.  
4. Front público + hook email.  
5. Script `publish` en el repo.  
6. Primera encuesta: Community directory EN (schema ya listo).

**Estado 2026-08-20:** DNS + HTTPS OK. Form EN vivo:
`https://forms.synergium.net/nexus-input`
Google Sheet y PocketBase **aún no se fusionan solos** — ver [ESTADO-DEPLOY.md](ESTADO-DEPLOY.md) y [GOOGLE-SHEET-SYNC.md](GOOGLE-SHEET-SYNC.md).

Después de eso, cada encuesta nueva = solo chat (“crea esta encuesta…”) → enlace.

## Qué no hacemos

- Tú no entras al admin de PocketBase  
- No usamos el MySQL/WordPress de synergium.net para respuestas  
- No dejamos Google Forms como sistema definitivo  

## Mientras no esté desplegado

Sigue el Google Form EN si hace falta; al tener MVP, publico el mismo schema aquí y cambias el link.

## Docs

- Este archivo = ruta canónica  
- [arquitectura.md](arquitectura.md) · [modelo-datos.md](modelo-datos.md)  
- Schema ejemplo: `../casos/community-directory-matching/`
