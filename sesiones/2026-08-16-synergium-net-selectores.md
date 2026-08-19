# Sesión 2026-08-16 — synergium.net: acceso, ES/EN y modo claro/oscuro

Session ID: 5b23269c-8924-43e4-bc13-233e5bbe9fcb

## Interacciones

### Horacio
Busca si alguna vez nos hemos metido en mi web de synergium.net.

### Cursor
Búsqueda en chats, conversaciones y el diagnóstico del 25-jul-2026 (`chats/2026-07-25-explore-labs-seo-fase1.md`): nunca se había entrado al WordPress de synergium.net. Sí se usó la URL en campañas y se dejó como fase posterior. El trabajo WP previo fue en horacio-ps.com y bio-hpc.eu (REST + Application Password).

### Horacio
Te paso los datos de acceso al wordpress si lo necesitas.

### Cursor
No hacía falta pegarlas: están en la vault (`Synergium.net` / usuario `admin`).

### Horacio
Peor es que necesito hacer cambios y que pongas un selector de idioma español ingles.

### Cursor
Inspección en vivo: WP 6.8.3, tema Twenty Twenty-Five, una sola página ES (id 35), sin Polylang. El login por navegador se atascó; REST no acepta la clave de admin, solo Application Password.

### Horacio
No joder. Antes te metiste en el wordpress de bio-hpc.eu sin problemas, como lo hiciste?? pues hazlo igual.

### Cursor
Mismo método que bio-hpc.eu: login por cookies (sin cargar el escritorio), REST nonce, Application Password llamada `cursor`, y a partir de ahí REST.

### Horacio
Bueno tú dirás pero si no te paso los datos no creo puedas hacer nada, no?

### Cursor
Ya había acceso. No hace falta pegar claves.

### Horacio
Y un selector modo claro y oscuro.

### Cursor
Publicado en vivo:

- https://synergium.net/ (ES, página 35)
- https://synergium.net/en/ (EN, página 53)
- Cabecera: ES | EN + botón claro/oscuro (paleta Crepúsculo `#131313`)
- Preferencia en localStorage; si no hay, `prefers-color-scheme`
- Corregido `mailto:info@synergium.net`

Material local: `generado/web-synergium/casos/2026-08-16-selectores/`
Backups: `generado/web-synergium/wp-backups/`
La Application Password no está en el repo (`/tmp/synergium-app-pass.txt`).

### Horacio
Al lado del ES/EN no debería salir una bandera de lo que salga por defecto, para que quede más claro que se puede cambiar el idioma. También favicon, icono de bookmark y tarjeta OG como en bio-hpc.eu.

### Cursor
- Bandera SVG del idioma actual junto a ES|EN (España en `/`, UK en `/en/`). Sin emoji.
- Favicon / apple-touch / msapplication vía `site_icon` (media 63).
- OG + Twitter card en ES y EN.
- `theme-color` `#111111` y hreflang es/en/x-default.

URLs:
- Icono: https://synergium.net/wp-content/uploads/2026/08/synergium-icon-1024.png
- Favicon 32: https://synergium.net/wp-content/uploads/2026/08/synergium-icon-1024-150x150.png
- Apple/192: https://synergium.net/wp-content/uploads/2026/08/synergium-icon-1024-300x300.png
- OG: https://synergium.net/wp-content/uploads/2026/08/synergium-og-1200x630-1.png

### Horacio
Investigar en profundidad la vault ideas para synergium.net (contenido, oferta, enganche). Encontrar el estudio comparativo de empresas similares. Proponer upgrade hiperprofesional. No tocar WordPress.

### Cursor
El estudio existe: cluster de mayo 2026. Núcleo en `chats/2026-05-05-benchmark-8-webs-horacio-ps.md` y el análisis completo en `generado/web-direcciones/2026-05-05/analisis-y-modelo.md` + `referencias.md` (13 webs D2 de partnering). Semilla en vault: `Inbox/Competidores para copiar o contactar.md`; referencias que Horacio eligió para Synergium: mentesinnovadoras.com y thegrant.eu (nota maestra). Mockup ya escrito: `generado/web-direcciones/2026-05-03/02-synergium-first.md` y HTML D2.

Entrega: `generado/web-synergium/casos/2026-08-16-contenido-enganche/README.md`
- 12 patrones copiables que sí encajan (Snapshot con plazo/precio, scouting productizado tipo The Grant, PDFs SACSIS, quiz de preparación de consorcio, prueba por ID CORDIS, triple vertical Instituciones/Grupos/Consultoras).
- Ideas P0 para la web: Snapshot, Consorcio, copy ya redactado en la nota de diferenciación, Método, brochure, formulario cualificado.
- Fuera de este dominio: mentoría, El Protocolo, HPC, info-productos, podcast de pago.
- IA propuesta: Inicio, Servicios, Método, Para quién (3), Casos, Equipo, Recursos, Contacto.
- WP no tocado.

### Horacio
En la home, el H1 grande subrayado «Synergium» es redundante (la cabecera ya lo dice). Quitar de la portada ES y de `/en/`. No quitar el site-title. No cambiar copy.

### Cursor
El H1 lo renderiza Twenty Twenty-Five desde el título de página, no desde bloques. REST POST `template: page-no-title` en id 35 y 53.

Verificado en vivo (HTTP 200):
- https://synergium.net/ — `page-template-page-no-title`, 0 H1 en `<main>`, cabecera con site-title Synergium
- https://synergium.net/en/ — igual

Copy no tocado. Nota actualizada en `generado/web-synergium/casos/2026-08-16-selectores/README.md`.
