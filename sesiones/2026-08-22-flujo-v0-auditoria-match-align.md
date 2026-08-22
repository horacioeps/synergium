# Sesión 2026-08-22 — Flujo v0 lineal + auditoría match-align

## Usuario

> Registrar flujo lineal 2 pasos (opt-in bilateral → brief match-align). Auditar todos opt-ins #1–#6 y respuestas inbox horacio@horacio-ps.com. Tabla quién puede recibir paso 2. Documentar en lugar canónico. Sesiones + HISTORICO + commit push.

## Contexto conocido

- Match #1: opt-in Matías 22/08; match-align Valentina 22/08; Valentina sí WA.
- Opt-ins 21/08: #3, #4, #5, #6. #2 descartado.

## Agente

### Documentación

- Creado [comunidad/formulario/match-align/FLUJO-v0.md](../comunidad/formulario/match-align/FLUJO-v0.md) — fuente canónica flujo v0 lineal (paso 1 opt-in, paso 2 match-align, paso 3 intro).
- Creado [hoy/tableros/AUDITORIA-match-align-2026-08-22.md](../hoy/tableros/AUDITORIA-match-align-2026-08-22.md) — tabla matches + quién recibe paso 2.
- Actualizados: `match-align/README.md`, `EMBUDOS.md`, `playbook-matching.md`, `MATCHES.md`.
- Historiales expedientes #1, #3–#6 con respuestas inbox.

### Auditoría IMAP (VPS EmailerX)

INBOX desde 20-Aug-2026: respuestas sí de Driselda, Tatiana, Verónica, Matías Causa, Karen, Antonio (22/08). Sin respuesta: Yen Na, Erdoğan, Matías Rivas, Valentina (email; sí WA).

Elementos enviados (solo `sent_copy`): opt-in Matías + match-align Valentina 22/08.

### Listo paso 2 ahora (6 personas)

Matías Causa, Driselda, Tatiana, Antonio (fga870@ual.es), Karen, Verónica. Valentina ya recibió. Pendiente paso 1: Matías Rivas, Yen Na, Erdoğan.

## Usuario (implícito)

Commit + push main.

## Re-verificación urgente ~17:17 CEST

- VPS EmailerX: `imap_box.Buzon` + `config/config.test.ini`, INBOX últimos 7 días — **confirma** respuestas ya en auditoría (Driselda, Tatiana, Verónica, Causa, Karen, Antonio `fga870@ual.es`; sin mail de Yen Na, Erdoğan, Matías Rivas).
- `read_recent_emails.py` devolvió `authentication failed` en esta pasada; `check_replies.py` parcial por EOF en carpetas; **fuente fiable:** `imap_box` INBOX.
- Repo ya en `d8cc72e` (FLUJO-v0 + AUDITORIA); sin cambios de tabla.
