# Flujo matching v0 — lineal en 2 pasos

**Estado:** v0 lineal, **mejorable**. Fecha: 2026-08-22.

Este documento es la fuente canónica del flujo operativo actual. Los embudos amplios (A2/A3, intro conjunta, follow-up) siguen en [hoy/tableros/EMBUDOS.md](../../../hoy/tableros/EMBUDOS.md); aquí solo el **camino mínimo** que estamos ejecutando hoy.

---

## Resumen

```text
[nexus-input] → curación match
       |
  Paso 1: opt-in bilateral (email, sin nombre del otro)
       |  sí (email o WhatsApp)
  Paso 2: brief match-align (form fase 2)
       |  ambos completan (objetivo)
  Intro conjunta + follow-up 10–14 d (playbook)
```

| Paso | Nombre | Canal | Formulario | Cuándo |
|------|--------|-------|------------|--------|
| **1** | Opt-in bilateral | Email (`horacio@horacio-ps.com`, EmailerX VPS) o WA | Contexto: [nexus-input](https://forms.synergium.net/nexus-input) | Tras curar el par; **sin** nombre de la otra parte |
| **2** | Brief `match-align` | Email o WA con enlace | [match-align](https://forms.synergium.net/match-align) | Tras **sí** al paso 1 (por parte); ideal cuando ambos han dicho sí |
| **3** | Intro conjunta | Email/WA según P30 | — | Tras ambos completan `match-align` (o excepción documentada) |

**v0 = lineal:** no ramas A3 automáticas, sin pre-relleno por URL, sin resumen automático. Mejoras previstas en [README.md](README.md) (pre-relleno `?ref=`, versión corta, export resumen).

---

## Paso 1 — Opt-in bilateral

- Plantillas: `clientes/piloto/…/emails-optin-borrador.md` o `clientes/matches/…/emails-optin-borrador.md`.
- Asunto tipo: `Synergium: posible colaboración (eje temático)`.
- Enlace al directorio: `https://forms.synergium.net/nexus-input`.
- Pregunta: ¿ok presentaros por email si la otra parte también quiere? **Sin** revelar nombre ni institución del match.
- Envío: EmailerX cuenta 1; copia IMAP → carpeta **Elementos enviados** (`sent_copy` en scripts VPS).

**Sí válido:** respuesta email explícita, o WhatsApp (ej. Valentina Lucena antes del email opt-in a Matías).

---

## Paso 2 — Brief `match-align`

- URL: `https://forms.synergium.net/match-align`.
- Cada parte rellena **por separado**; campo `match_reference` con referencia abstracta (ej. `match-2026-001`, no nombres).
- Email tipo: asunto `Synergium: brief corto antes de la intro (eje)`.
- Piloto enviado: Valentina Lucena (match #1), 2026-08-22 — ver [clientes/piloto/matias-rodriguez-rivas/emails-optin-borrador.md](../../../clientes/piloto/matias-rodriguez-rivas/emails-optin-borrador.md).

**Regla v0:** enviar paso 2 a quien ya dijo **sí** al paso 1. No esperar al doble sí para el primero que confirma (caso Valentina). La intro conjunta sigue bloqueada hasta opt-in bilateral completo + ambos briefs (o decisión manual).

---

## Referencias de match (v0)

| Match # | Par | `match_reference` sugerida |
|---------|-----|---------------------------|
| 1 | Matías Rodríguez-Rivas ↔ Valentina Lucena | `match-2026-001` (piloto usó `matias-valentina`) |
| 2 | Ferran ↔ Elena | — (opt-in descartado) |
| 3 | Causa ↔ Yen Na | `match-2026-003` |
| 4 | Driselda ↔ Tatiana | `match-2026-004` |
| 5 | Erdoğan ↔ Antonio | `match-2026-005` |
| 6 | Karen ↔ Verónica | `match-2026-006` |
| 7 | Michelle ↔ Kinndle | `match-2026-007` |

Tablero vivo + auditoría: [hoy/tableros/MATCHES.md](../../../hoy/tableros/MATCHES.md), [AUDITORIA-match-align-2026-08-22.md](../../../hoy/tableros/AUDITORIA-match-align-2026-08-22.md).

---

## Relacionado

- Playbook intros y follow-up: [comunidad/casos/formulario-agosto-2026/playbook-matching.md](../../casos/formulario-agosto-2026/playbook-matching.md)
- Schema e campos: [README.md](README.md)
- Embudos amplios: [hoy/tableros/EMBUDOS.md](../../../hoy/tableros/EMBUDOS.md)
