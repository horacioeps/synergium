# Sesión 2026-08-19 — Copia local del repo y push siempre

## Usuario

> en este proyecto, creamos una copia local del repo: https://github.com/horacioeps/synergium , y cada vez que te pida algo y lo hagas, subes siemore los cambios al repo. o cuando yo modifique ficheros desde las copias locales, queda claro? puedes ademas ver esto en los "rules"?

## Contexto del workspace

La carpeta `Synergium local` estaba vacía (solo `.vscode`). No había clone.

## Agente

1. `git init` + `origin` → `https://github.com/horacioeps/synergium.git` + checkout de `origin/main` (el `git clone .` falló porque el directorio no estaba vacío).
2. Lectura de rules y docs ya existentes:
   - `.cursor/rules/synergium-canonical.mdc` — este repo es canónico vs Obsidian; **no** decía push siempre ni copia local.
   - `.cursor/rules/vault-cloud-ssh.mdc` — vault VPS solo lectura.
   - `AGENTS.md` **sí** decía: trabajar en `main`; commit + push tras cada avance material; volcado en `chats/` y `sesiones/`.
   - `HISTORICO.md` existía pero **no** estaba enlazado desde `README.md`.
3. Nueva regla siempre activa: `.cursor/rules/local-clone-siempre-push.mdc`
   - Este workspace = copia local de `horacioeps/synergium`.
   - Tras cada interacción: estar en `main`, commitear cambios del agente **y** ediciones manuales de Horacio, push a `origin/main`.
   - Sesiones + `HISTORICO.md`.
4. Apuntes cruzados en `synergium-canonical.mdc`, `AGENTS.md`, `README.md` (enlace a HISTORICO), `docs/HISTORIAL-TRABAJO.md`.
5. Volcado de sesión + fila en `HISTORICO.md` + commit + push.

## Respuesta al usuario (acuerdo)

Sí, queda claro:

- Esta carpeta es el clone local de [horacioeps/synergium](https://github.com/horacioeps/synergium).
- Tras cada pedido hecho: commit + push a `main`.
- Si Horacio edita ficheros a mano en esta copia, esos cambios también se suben (al cerrar la interacción o cuando haya cambios pendientes).
- En las rules: parte ya estaba en `AGENTS.md`; ahora está explícito en `.cursor/rules/local-clone-siempre-push.mdc` (`alwaysApply: true`).

---

## Usuario (continuación)

> actualiza con github

## Agente

1. `git fetch` + `git pull --ff-only origin main` (estábamos 1 commit detrás).
2. Bajó `2d945d5` — match Valentina enviada, email UCO, expediente Matías, sesión `sesiones/2026-08-19-match-valentina-envio-datos-uco.md`.
3. `HISTORICO.md` en ese commit traía marcadores de conflicto sin resolver (`<<<<<<< HEAD` / filas 15:50 vs 18:40–18:45). Se dejaron **todas** las filas y se quitaron los marcadores.
4. Volcado de esta continuación + push.
