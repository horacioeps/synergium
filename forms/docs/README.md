# Synergium Forms — `forms.synergium.net`

Sistema de formularios tipo Google Forms con URL opaca, acceso abierto por enlace, almacenamiento propio y email al completar.

## Objetivo

- URLs del estilo `https://forms.synergium.net/jha76sd8a78sda`
- Cualquiera con el enlace puede responder (sin cuenta)
- Respuestas en base de datos propia
- Email a Horacio (y opcionalmente copia) en cada envío
- Primer caso: **Community directory — matching researchers**

## Documentos

| Doc | Contenido |
|-----|-----------|
| **[COMO-HACERLO.md](COMO-HACERLO.md)** | Decisión única: tú das directrices → agente publica por API; VPS = Explore Labs |
| **[ESTADO-DEPLOY.md](ESTADO-DEPLOY.md)** | **Estado real del deploy (URL, DNS pendiente, SSL)** |
| [arquitectura.md](arquitectura.md) | Comparativas y por qué no WordPress |
| [modelo-datos.md](modelo-datos.md) | Tablas y campos |
| [../casos/community-directory-matching/](../casos/community-directory-matching/) | Spec del primer formulario |

## Relación con trabajo previo

El 2026-08-14 se generó el mismo directorio para **Google Forms** en `generado/comunidad-whatsapp/casos/2026-08-14-formulario-matching/`. Este módulo es la evolución: dejar Google y hospedar bajo marca Synergium, con BD consultable para matching.
