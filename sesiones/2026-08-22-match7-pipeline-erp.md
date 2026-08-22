# Sesión 2026-08-22 — Match #7 Michelle ↔ Kinndle + Pipeline de matching (ERP)

Volcado consolidado de la conversación (detalle por turnos también en `2026-08-22-match-erp-tracking.md` y `2026-08-22-optin-match-7-michelle-kinndle.md`).

## Temas

1. **Matches pendientes de contacto** — Solo Match #7 Michelle ↔ Kinndle (#2 Ferran–Elena descartado; #1–#6 ya escritos/contactados).
2. **Tracking tipo ERP en PocketBase** — Pasos, emails, cuerpo de conversación; expediente Match #7.
3. **Trabajo en background (agentes)**:
   - Expediente `clientes/matches/michelle-kinndle/` (fichas, opt-in borradores).
   - Colecciones PB: `matches`, `match_participants`, `contact_events`.
   - Campos emparejamiento: `pairing_status`, `pairing_method`, `proposed_at`, `paired_at`, `is_paired`, `paired_with_email`, `pairing_proposed_at`.
   - Dashboard HTML: `producto/forms/deploy/pb_public/match-dashboard/index.html` + `export_match_dashboard.py`.
   - Docs: `MATCH-TRACKING.md`, `MATCH-ERP-ROADMAP.md`.
   - Naming canónico: **Pipeline de matching** / **Match Pipeline** (evitar «ERP» en UI).
4. **Opt-in ES** Michelle + Kinndle — escritos y enviados.
5. **«dale y envia»** — Opt-in vía EmailerX VPS ~17:44–17:45 CEST a `michelle.vierarom@ug.edu.ec` y `kblanco@una.cr`.
6. **Sugerencias ERP + dashboard HTML** — Roadmap campos; dashboard desplegado en `https://forms.synergium.net/match-dashboard/`.
7. **Schema/backfill pairing** — Producción PB actualizada.
8. **Deploy manual** — rsync `pb_public` al VPS para dashboard en vivo.

## Commits relevantes (main)

- `70f53cb` — pairing fields schema/backfill/docs
- `0a25cf4` — match pipeline dashboard, naming, roadmap
- `628ab1a` — match #7 opt-in sent + PB sync
- `0745be8` — MATCHES tablero #7 opt-in sent
- `352af64` — fix duplicate match #7 row in MATCHES

## Turno — /guarda-sesion-y-demas (~17:53 CEST)

Pedido: ejecutar skill guarda-sesion; consolidar volcado; HISTORICO; commit + push main (sin `.vscode`).

Hecho: este fichero consolidado; fila HISTORICO; push si hay cambios.
