# Selector de idioma — todos los Synergium Forms

Aplica a **cualquier** formulario en `forms.synergium.net/{public_id}` (SPA compartida).

## UI

Mismo botón que synergium.net: globo + código (`EN`…) + lista desplegable, junto al claro/oscuro.

## Idiomas (igual que la web)

English, Español, 简体中文, العربية, 日本語, Português, Italiano, Deutsch.

**Por defecto: inglés.** Preferencia en `localStorage` clave `syn-lang` (compartida con la web).

## Cómo se traduce

| Lang | Mecanismo |
|------|-----------|
| `en` | Texto canónico del form en PocketBase |
| `es` | Archivo nativo `/i18n/{public_id}.es.json` si existe; si no, Google Translate |
| `zh-CN`, `ar`, `ja`, `pt`, `it`, `de` | Google Translate (como synergium.net) |

Los `value` de opciones y los `field id` **no** cambian con el idioma (matching estable). Solo cambian labels/UI.

## Añadir ES nativo a un form

1. Copiar schema EN → ES (mismos `id` / `value`).
2. Guardar en `comunidad/formulario/nexus-input/schema-es.json` (u otro caso) y desplegar a `producto/forms/deploy/pb_public/i18n/{public_id}.es.json`.
3. Redeploy `pb_public/` al VPS.

Ejemplo vivo: `nexus-input` → `i18n/nexus-input.es.json`.

## Regla Cursor

`.cursor/rules/forms-idioma-selector.mdc` (`alwaysApply: true`).
