# Synergium

**Repo canónico** del proyecto Synergium: broker de colaboraciones de investigación entre LATAM y Europa, con infraestructura web, formularios, prospección comercial y comunidad.

A partir de **2026-08-19**, todo el trabajo Synergium se hace **aquí**. El repo Obsidian conserva copias antiguas solo como referencia — ver [REFERENCIAS-LEGACY-OBSIDIAN.md](REFERENCIAS-LEGACY-OBSIDIAN.md).

## Qué es Synergium

**Synergium** conecta investigadores y grupos de Latinoamérica con socios europeos para proyectos Horizon, convocatorias internacionales y publicaciones conjuntas. La diferenciación es la triada **investigación + transferencia tecnológica + comunicación** (podcast de investigación con 390+ episodios).

Clientes potenciales: IPs, OTRIs, vicerrectorados, agencias de ciencia. Foco geográfico: Chile, México, Colombia, Uruguay.

Detalle: [docs/QUE-ES-SYNERGIUM.md](docs/QUE-ES-SYNERGIUM.md)

## Estructura del repo

| Carpeta | Contenido |
|---------|-----------|
| [docs/](docs/) | Síntesis, historial, infraestructura |
| [estrategia/](estrategia/) | Ideas de negocio, plantillas email, búsqueda prospectos |
| [web/](web/) | synergium.net — WordPress REST, casos, backups |
| [forms/](forms/) | forms.synergium.net — PocketBase, deploy |
| [prospectos/](prospectos/) | Buscador de prospectos v1 (web + NCPs) |
| [comunidad/](comunidad/) | Directorio WhatsApp / matching |
| [clientes/](clientes/) | Expedientes por investigador (piloto, matching, contacto) |
| [web-direcciones/](web-direcciones/) | Mockups y propuestas web |
| [outreach/](outreach/) | Outreach (Tec Monterrey, etc.) |
| [scripts/](scripts/) | Publicación forms, **vault_ssh_ro.sh**, utilidades |
| [chats/](chats/) | Volcados sesiones Cursor |
| [sesiones/](sesiones/) | Volcados en bruto |

## Infraestructura

| Servicio | URL | Estado |
|----------|-----|--------|
| Web | [synergium.net](https://synergium.net) | WordPress, VPS Explore Labs |
| Forms | [forms.synergium.net](https://forms.synergium.net) | PocketBase — DNS A pendiente IONOS |

[docs/INFRAESTRUCTURA.md](docs/INFRAESTRUCTURA.md) · [forms/docs/ESTADO-DEPLOY.md](forms/docs/ESTADO-DEPLOY.md)

## Para agentes

Leer **[AGENTS.md](AGENTS.md)** antes de cualquier tarea Synergium.

Cronología compacta de pedidos y trabajo: **[HISTORICO.md](HISTORICO.md)**.

Embudos post-formulario: **[EMBUDOS.md](EMBUDOS.md)** · Ideas/tareas abiertas: **[TODO.md](TODO.md)**.

Otro repo desde cero (misma frase, sin repetir reglas): [docs/NUEVO-PROYECTO-LOCAL.md](docs/NUEVO-PROYECTO-LOCAL.md).

## Vault en el VPS (solo lectura)

Las notas fuente (ideas, conversaciones comerciales) están en la vault del VPS. Los agentes **leen por SSH** cuando hace falta:

```bash
scripts/vault_ssh_ro.sh cat "ruta/nota.md"
```

[docs/VAULT-ACCESO.md](docs/VAULT-ACCESO.md) · `.cursor/rules/vault-cloud-ssh.mdc`

## Referencias antiguas (repo Obsidian legacy)

Material duplicado previo al 2026-08-19 en el repo Obsidian: [REFERENCIAS-LEGACY-OBSIDIAN.md](REFERENCIAS-LEGACY-OBSIDIAN.md)

## Licencia

Material interno de Horacio Pérez Sánchez.
