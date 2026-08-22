
## 2026-08-22 ~18:10 CEST — Dashboard directorio + cobertura PB

**Pedido:** Mostrar TODAS las personas del directorio nexus-input (no solo 14 en matches); confirmar exposición pública; basic auth si hace falta.

**Investigación:**
- PB nexus-input: **30** submissions (28 sin pruebas PublicTest)
- `match_me`: 23 yes, 2 directory_only, 3 you_only_no_intro
- Dashboard antes: 7 matches, 14 participants (solo `match_participants`)
- **Seguridad:** ya protegido con HTTP Basic Auth (401 sin credenciales); `data.json` contiene emails y WhatsApp
- 15 emails en submissions no estaban en match_participants

**Implementación:**
- `export_match_dashboard.py`: nueva sección `directory` desde submissions nexus-input + cruce con participants/events
- `index.html`: pestaña **Directorio** (28 filas)
- Apache templates alineados con VPS (`~/synergium-forms/.htpasswd-match-dashboard`)
- `setup_match_dashboard_auth.sh`; docs `MATCH-TRACKING.md`
- Deploy rsync `match-dashboard/` a producción

**Resultado export:** 7 matches · 14 participants · **28 directory** · 68 events

**URL:** https://forms.synergium.net/match-dashboard/ (requiere Basic Auth)
