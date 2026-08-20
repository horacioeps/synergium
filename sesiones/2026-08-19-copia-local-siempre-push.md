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

---

## Usuario (2026-08-20)

> todas estas intrucciones que te he dado iniciales, como las peudes empaquetar para que cuando yo cree otro proyecto local desde cero se las pueda pasar todas de golpe y el rpoyecto las enteidna y asi no tengo que reeptirals cada vez, es decir, bajate tal repo y luego todo los demas

## Agente

Empaquetado en skill personal + regla de usuario + doc en este repo:

- `~/.cursor/skills/nuevo-proyecto-local/` — clone, rules alwaysApply, sesiones, HISTORICO, push
- `~/.cursor/skills/guarda-sesion-y-demas/` — descripción arreglada para que se dispare al cierre de turno
- `~/.cursor/rules/horacio-flujo-repos.mdc` — flujo en cualquier proyecto
- Este repo: `.cursor/rules/horacio-sesiones-historico.mdc`, [docs/NUEVO-PROYECTO-LOCAL.md](../docs/NUEVO-PROYECTO-LOCAL.md)

Frase de arranque: `Nuevo proyecto local: https://github.com/USUARIO/REPO`

---

## Usuario (2026-08-20 20:42)

> haz sync

## Agente

`fetch` + comparación `HEAD...origin/main` = **0 / 0**. Local y GitHub en el mismo commit `9846a79`. Nada que bajar ni cambios locales de trabajo. Volcado + HISTORICO de este sync.

El push de ese volcado falló por disco lleno.

---

## Usuario (2026-08-20 20:46)

> vuelve a ver, he liberado disco

## Agente

~18 GB libres, git OK, sync sigue 0/0. Commit + push del volcado pendiente.
