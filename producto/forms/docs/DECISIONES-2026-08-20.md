# Decisiones Forms — 2026-08-20 (respuestas Horacio)

| # | Tema | Decisión |
|---|------|----------|
| 1 | Google Form + Synergium | **Ambos**. Google sigue; sync a PocketBase |
| 2 | Lectura Sheet | **2b** CSV público (`gid=1537513728`) |
| 3 | URL idioma | **Una sola** (`nexus-input` + selector) |
| 4 | Secrets PB local | **OK** — en `~/.cursor/secrets.env` |
| 5 | WhatsApp enlace nuevo | *(sin respuesta aún)* |
| 6 | Dedupe email | **OK** |
| 7 | Import masivo luego cron | **OK** — 26 filas importadas; cron `*/15` en VPS |
| 8 | ES nativo en forms nuevos | **OK** |

## Enlaces

- Form Synergium: https://forms.synergium.net/nexus-input
- Google Form: ver `comunidad/casos/formulario-agosto-2026/enlaces-vivos.md`
- Sync: `ops/scripts/synergium_forms_sheet_sync.py` · log VPS `~/synergium-forms/logs/sheet-sync.log`
