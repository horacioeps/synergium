# Acceso a la vault (VPS) desde repo Synergium

La vault personal de Horacio vive en el VPS Explore Labs (Obsidian Sync / Headless). **No está en git.** Los agentes que trabajan en **este repo** pueden leerla por SSH cuando haga falta contexto Synergium.

## Helper

Script: **`scripts/vault_ssh_ro.sh`** (solo lectura).

```bash
# Comprobar conexión
scripts/vault_ssh_ro.sh count-md

# Listar carpeta
scripts/vault_ssh_ro.sh ls Inbox

# Leer nota
scripts/vault_ssh_ro.sh cat "Ideas de negocio para ayudar investigadores - Synergium - y otras.md"

# Copiar a local para procesar
scripts/vault_ssh_ro.sh get "ruta/nota.md" /tmp/nota.md

# Ruta remota canónica
scripts/vault_ssh_ro.sh root
```

## Secrets requeridos (Cloud Agents)

Inyectados en el entorno del agente (mismos que repo Obsidian legacy):

| Variable | Uso |
|----------|-----|
| `EXPLORE_LABS_SSH_HOST` | Host VPS |
| `EXPLORE_LABS_SSH_OBISIDIAN_USER` | Usuario cuenta vault |
| `EXPLORE_LABS_SSH_OBSIDIAN_PASSWORD` | Password SSH |
| `EXPLORE_LABS_OBSIDIAN_VAULT_PATH` | Home del usuario vault |

Regla Cursor: `.cursor/rules/vault-cloud-ssh.mdc`

## Notas Synergium útiles en vault (ejemplos)

| Tema | Buscar en vault |
|------|-----------------|
| Ideas de negocio | Nota «Ideas de negocio… Synergium…» |
| Conversaciones comerciales | Enlaces desde esa nota (Fabián, Alexander, etc.) |
| Comunidad | Nota maestra Synergium + conversaciones podcast |

Usar `scripts/vault_ssh_ro.sh find` con criterios acotados si no conoces la ruta exacta.

## Política

1. **Leer sí** cuando el pedido lo requiera.
2. **No escribir** en vault salvo petición explícita del usuario.
3. **No subir** contenido de vault a git salvo extractos derivados en `estrategia/` u otras carpetas de este repo (con criterio del usuario).

## Repo Obsidian legacy

El mismo script existe como copia archivada en el repo Obsidian (`scripts/vault_ssh_ro.sh`). **Usar el de este repo** cuando el workspace sea synergium.
