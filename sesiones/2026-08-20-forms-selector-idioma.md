# Sesión 2026-08-20 — Selector idioma = web en todos los forms

## Usuario

> el selector de idioma que por defecto salgan los forms en ingles pero que se puedan cambiar de iioma y que salga el mismo boton de selector que siempre.
> y que salga en los mismos idiomas que la web ppal
> y que eso se cumpla para todos los formularios, que quede registrado

## Agente

1. SPA `forms/deploy/pb_public/index.html`: botón globo+código como synergium.net; idiomas EN/ES/zh-CN/ar/ja/pt/it/de; default **EN**.
2. ES nativo vía `/i18n/{public_id}.es.json` (nexus-input listo); si no hay archivo → Google Translate. Resto de idiomas → Google Translate (como la web). Clave `syn-lang` compartida.
3. Schema ES: `forms/casos/community-directory-matching/schema-es.json` + `pb_public/i18n/nexus-input.es.json`.
4. Regla registrada: `.cursor/rules/forms-idioma-selector.mdc` + `forms/docs/IDIOMA-SELECTOR.md` + mención en `AGENTS.md`.
5. Desplegado al VPS; smoke OK (`i18n/nexus-input.es.json` 200).
