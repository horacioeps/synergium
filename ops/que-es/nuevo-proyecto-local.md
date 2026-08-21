# Arrancar otro proyecto local (sin repetir instrucciones)

Las instrucciones de «bájate el repo + main + push siempre + sesiones + HISTORICO» viven en un **skill personal** de Cursor, no hay que volver a dictarlas.

Skill: `~/.cursor/skills/nuevo-proyecto-local/`  
Regla de usuario: `~/.cursor/rules/horacio-flujo-repos.mdc`

## Qué pegar en el chat del proyecto nuevo

Carpeta vacía (o solo `.vscode`) abierta en Cursor:

```
Nuevo proyecto local: https://github.com/USUARIO/REPO
```

El agente clona `main`, escribe las rules del proyecto, crea `sesiones/` e `HISTORICO.md`, enlaza el README y hace push.

Si más adelante el repo está desordenado: skill personal `orden-jerarquico-repo` (`~/.cursor/skills/orden-jerarquico-repo/`).
