# Sesión 2026-08-21 — Decisiones + import Sheet + ¿form usable?

## Usuario

> 1- usamos ambos. queda claro? 3. una sola. 4- ok 6- ok 7- 7 ok, 8- ok. y luego me dices si ya podemos usar nuestro form

## Decisiones

| # | Decisión |
|---|----------|
| 1 | Ambos (Google + Synergium) |
| 2 | Ya 2b |
| 3 | Una sola URL |
| 4 | PB secrets en secrets.env |
| 6 | Dedupe email |
| 7 | Import masivo + cron |
| 8 | ES nativo en forms nuevos |
| 5 | Sin respuesta (WhatsApp) |

## Hecho

- PB admin añadido a `~/.cursor/secrets.env` (no en git).
- `scripts/synergium_forms_sheet_sync.py` + import **26/26**.
- Cron `*/15` en VPS; re-run → skipped 26.
- Docs: DECISIONES, GOOGLE-SHEET-SYNC, enlaces-vivos, ESTADO-DEPLOY.

## ¿Ya se puede usar el form?

**Sí.** https://forms.synergium.net/nexus-input está vivo (API/página 200), idiomas, y las 26 del Sheet ya están en la BD.
