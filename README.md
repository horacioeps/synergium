# Synergium

**Repo canónico** del proyecto Synergium: broker de colaboraciones de investigación entre LATAM y Europa, con infraestructura web, formularios, prospección comercial y comunidad.

A partir de **2026-08-19**, todo el trabajo Synergium se hace **aquí**. El repo Obsidian conserva copias antiguas solo como referencia — ver [archivo/legacy-obsidian.md](archivo/legacy-obsidian.md).

Índice de carpetas: **[MAPA.md](MAPA.md)**.

## Qué es Synergium

**Synergium** conecta investigadores y grupos de Latinoamérica con socios europeos para proyectos Horizon, convocatorias internacionales y publicaciones conjuntas. La diferenciación es la triada **investigación + transferencia tecnológica + comunicación** (podcast de investigación con 390+ episodios).

Clientes potenciales: IPs, OTRIs, vicerrectorados, agencias de ciencia. Foco geográfico: Chile, México, Colombia, Uruguay.

Detalle: [ops/que-es/synergium.md](ops/que-es/synergium.md)

## Estructura del repo

Área → categoría → ítem. Detalle en [MAPA.md](MAPA.md).

| Área | Contenido |
|------|-----------|
| [hoy/tableros/](hoy/tableros/) | Embudos, matches, TODO |
| [comunidad/](comunidad/) | Formulario nexus-input, matching, casos WhatsApp |
| [clientes/](clientes/) | Expedientes (piloto y matches) |
| [comercial/](comercial/) | Estrategia, prospectos, outreach |
| [producto/](producto/) | synergium.net, forms.synergium.net, mockups |
| [ops/](ops/) | Scripts, infra, vault, procedimientos |
| [archivo/](archivo/) | Chats, historial, legacy Obsidian, registro de reorg |
| [sesiones/](sesiones/) | Volcados en bruto (raíz; contrato de agentes) |

## Infraestructura

| Servicio | URL | Estado |
|----------|-----|--------|
| Web | [synergium.net](https://synergium.net) | WordPress, VPS Explore Labs |
| Forms | [forms.synergium.net](https://forms.synergium.net) | PocketBase — DNS A pendiente IONOS |

[ops/infra/infraestructura.md](ops/infra/infraestructura.md) · [producto/forms/docs/ESTADO-DEPLOY.md](producto/forms/docs/ESTADO-DEPLOY.md)

## Para agentes

Leer **[AGENTS.md](AGENTS.md)** antes de cualquier tarea Synergium.

Cronología compacta de pedidos y trabajo: **[HISTORICO.md](HISTORICO.md)**.

Embudos: **[hoy/tableros/EMBUDOS.md](hoy/tableros/EMBUDOS.md)** · Matches: **[hoy/tableros/MATCHES.md](hoy/tableros/MATCHES.md)** · Tareas: **[hoy/tableros/TODO.md](hoy/tableros/TODO.md)**.

Otro repo desde cero (misma frase, sin repetir reglas): [ops/que-es/nuevo-proyecto-local.md](ops/que-es/nuevo-proyecto-local.md).

## Vault en el VPS (solo lectura)

Las notas fuente (ideas, conversaciones comerciales) están en la vault del VPS. Los agentes **leen por SSH** cuando hace falta:

```bash
ops/scripts/vault_ssh_ro.sh cat "ruta/nota.md"
```

[ops/infra/vault-acceso.md](ops/infra/vault-acceso.md) · `.cursor/rules/vault-cloud-ssh.mdc`

## Referencias antiguas (repo Obsidian legacy)

Material duplicado previo al 2026-08-19: [archivo/legacy-obsidian.md](archivo/legacy-obsidian.md)

Si hay que deshacer el árbol de carpetas: [archivo/REORGANIZACION-2026-08-21.md](archivo/REORGANIZACION-2026-08-21.md) (tag `pre-orden-arbol-2026-08-21`).

## Licencia

Material interno de Horacio Pérez Sánchez.
