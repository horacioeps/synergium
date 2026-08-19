# Sesión 2026-08-17 — synergium.net: acceso, ES/EN, 8 idiomas, SKUs, SEO, repo

Session ID: 5b23269c-8924-43e4-bc13-233e5bbe9fcb
Continuación de [2026-08-16-synergium-net-selectores.md](2026-08-16-synergium-net-selectores.md), [2026-08-16-synergium-upgrade-contenido.md](2026-08-16-synergium-upgrade-contenido.md) y [2026-08-17-synergium-skus-restantes.md](2026-08-17-synergium-skus-restantes.md).
Hoy 2026-08-17: Horacio pide «sube al repo y demas» + web más profesional + equipo internacional. Este volcado cubre el arco completo. El texto de equipo queda pendiente de otro agente.

## Interacciones (volcado bruto)

### Horacio
busca si alguna vez nos hemos metido en mi web de synergium.net

### Cursor
Nunca se había entrado al WordPress de synergium.net. Sí se usó la URL en campañas y se dejó como fase posterior (diagnóstico 25-jul-2026). El trabajo WP previo fue en horacio-ps.com y bio-hpc.eu (REST + Application Password).

### Horacio
te paso los datos de acceso al wordpress si lo ncesitas

### Cursor
No hacía falta pegarlas: están en la vault (nota Synergium.net / usuario admin).

### Horacio
peor es que necesito hacer cambios y que pongas un selector de idioma español ingles

### Cursor
Inspección en vivo: WP 6.8.3, tema Twenty Twenty-Five, una sola página ES (id 35), sin Polylang. El login por navegador se atascó; REST no aceptaba la clave de admin, solo Application Password.

### Horacio
no joder. antes te metiste en el wordpressd e bio-hpc.eu sin problemas, como lo hiciste?? pues hazlo igual

### Cursor
Mismo método que bio-hpc.eu: login por cookies (sin cargar el escritorio), REST nonce, Application Password llamada `cursor`, y a partir de ahí REST. Clave en `/tmp/synergium-app-pass.txt` (no va al repo).

### Horacio
bueno tu diras pero si no te paso los datos no creo puedas hacer nada, no?

### Cursor
Ya había acceso. No hace falta pegar claves.

### Horacio
y un selector modo claro y oscuro

### Cursor
Cabecera con ES | EN + toggle claro/oscuro (paleta Crepúsculo). Página EN publicada en `/en/` (id 53). `mailto:info@synergium.net` corregido. Salida: `generado/web-synergium/casos/2026-08-16-selectores/`.

### Horacio
y ponle icono logo del bookmark, card, y todas las cosas como tambien tiene bio-hpc.eu

### Cursor
`site_icon` + apple-touch + msapplication. OG/Twitter en ambas páginas. Icono https://synergium.net/wp-content/uploads/2026/08/synergium-icon-1024.png · OG https://synergium.net/wp-content/uploads/2026/08/synergium-og-1200x630-1.png.

### Horacio
y otra cosa, al lado del ES/EN n odeberia salir una bandera de lo que salga por defecto, para que quede mas claro que se puede cambir el idioma?

### Cursor
Bandera SVG del idioma actual (ES/UK) junto al selector.

### Horacio
y luego, mira en mi vault en profunidad para ver si hay ideas que se podrian añadir a la web para aumentar su contenido y las opcines que podemos ofrecer y que tenga ademas mas enganche. mira a ve rtambien si en su dia hice un estudio, creo que si, de comparacion con otras empresas similares, y si es asi, dime que ideas podemos copiar de ellas, de las que encajen con nosotros, para meterlas en la web, y que quede hiper profesional y super serio

### Cursor
El estudio existe (mayo 2026): chats/2026-05-05-benchmark-8-webs-horacio-ps.md + generado/web-direcciones/2026-05-05/. Extraídos 12 patrones copiables. Entrega: generado/web-synergium/casos/2026-08-16-contenido-enganche/README.md. WordPress no tocado en ese paso.

### Horacio
y de la pagina ppal, creo que el syneregium sibrayado sobra,no? por estar ya reeptido

### Cursor
H1 «Synergium» redundante con la cabecera. Plantilla `page-no-title` en páginas 35 y 53. En vivo 0 H1 en `<main>`; site-title de cabecera se mantiene. Copy no tocado.

### Horacio
sugieres meter todo esto? ok excepto demasiado detalle en el quienes somos. si lo haces, mete mecanismo para poder volver atras en cas oque no me guste. Brochure Synergium Colaboraciones Internacionales.pdf y baste tambien en este doc, pero nunca pongas numero en euros ni de costes

### Horacio
y recuerda, es menor menos que mas para no saturar. si algo no lo ves claro, no lo pongas, o me preguntas

### Horacio
y de paso le metes todo lo necesario para SEO

### Horacio
y como esto va de internacionalizamos , mte tambien que etodo el contenido salga automaticamente no solo en ES y EN si no tambien en Chino estandar, arabe y japones. y portugues brasil, italinao y aleman

### Horacio
pero que haya un icono claro para indicar selecciona de idiomas

### Horacio
y por defecto que salga siempre la version ingles

### Cursor
Upgrade publicado:
- Portada `/` en inglés (página 35). Español en `/es/` (página 53, antes `/en/`). `/en/` redirige a `/`.
- Copy corto del brochure (proceso, 3 pasos, un bloque para quién, quiénes somos de un párrafo). Sin precios. Logros existentes sin ampliar.
- Cabecera: globo + código de idioma (es/en/zh-CN/ar/ja/pt/it/de) + claro/oscuro. Árabe `dir=rtl`. GTranslate desde EN.
- SEO: plugin Synergium SEO (title, description, canonical, hreflang en/es/x-default→EN, OG, Twitter, JSON-LD). Sitemap `/wp-sitemap.xml`.
- Backups: `generado/web-synergium/wp-backups/pre-upgrade-2026-08-16/`
- Rollback: `python3 generado/web-synergium/casos/2026-08-16-upgrade-contenido/rollback.py`
Omitido a propósito: sitio de 8 páginas, landings «para quién», casos inventados, equipo largo, blog, brochure PDF (lleva precio), Rank Math, Search Console, precios, nombre de Horacio.

### Horacio
queda guayp oer todas las otras cosas que ibanos a implementar seguno lo que habiamos visato en el vault y en webs de competidores ?

### Cursor
Faltaban SKUs del plan vault/competidores. Publicados en las mismas homes (no segunda página):
- EN https://synergium.net/ y ES https://synergium.net/es/
- Tres SKUs: Partner search / Coordinator search / Call fit (ES: Búsqueda de socios / Búsqueda de coordinador / Encaje a convocatoria). Sin precios.
- Partner Snapshot: 3 fichas + 1 intro en 7–10 días.
- Método: Snapshot 7–10 días vs búsqueda completa ~12 semanas. No se redacta la parte científica ni se garantiza el grant.
- Para quién: instituciones / grupos / consultoras EU. CTA 10–12 min + mailto.
- Rollback: `python3 generado/web-synergium/casos/2026-08-17-skus-restantes/rollback.py`
Omitido: quiz (haría falta SaaS), IDs CORDIS inventados, brochure PDF con 3.450 €.

### Horacio (2026-08-17 ~11:39 CEST)
sube al repo y demas. por otra parte, creo que la web queda un poco simple, no se puede hacer mas completa par que quede mas profesional? creo que es necesario. y en cuanto a la descripcion del equipo poner que tambien hay mientbros otros, distruubios internacionalmente en todos los continentes

### Cursor
Pedido partido en dos:
1. Este agente: volcado de sesión, HISTORICO.md, índice chats, commit en main y push. Sin `git status -sb` del repo entero (iCloud cuelga). Rutas concretas: sesiones/, HISTORICO.md, README.md, PROJECT_PLAN.md, chats/2026-08-16*, chats/README.md, generado/web-synergium/.
2. Otro agente: ampliar la web para que quede más profesional y actualizar la descripción del equipo (miembros en todos los continentes). **Ese cambio de copy/equipo sigue pendiente.**

Había un `git rebase origin/main` colgado desde las 11:01 con `.git/index.lock` (el commit local de favicon/OG/banderas `5bff53b` ya estaba hecho; el rebase no avanzaba). Se mató solo ese rebase; no se tocó el git de Cursor IDE (`git status -z`, diffs).

## Estado vivo (antes del cambio de equipo)

- https://synergium.net/ — EN por defecto
- https://synergium.net/es/ — ES
- `/en/` redirige a `/`
- Globo + 8 idiomas (zh-CN, ar RTL, ja, pt-BR, it, de vía traducción automática desde EN)
- SKUs + Partner Snapshot + método + SEO en head
- Equipo: párrafo corto anónimo; ampliación internacional **pendiente de otro agente**

## Archivos de esta funcionalidad

- `generado/web-synergium/casos/2026-08-16-selectores/`
- `generado/web-synergium/casos/2026-08-16-contenido-enganche/`
- `generado/web-synergium/casos/2026-08-16-upgrade-contenido/`
- `generado/web-synergium/casos/2026-08-17-skus-restantes/`
- `generado/web-synergium/wp-backups/`
