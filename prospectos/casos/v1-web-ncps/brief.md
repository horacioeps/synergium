# Brief para Claude Code: buscador de prospectos por "señal de dolor"

Versión inicial. Alcance v1: **web abierta + NCPs (National Contact Points) Horizon**. LinkedIn y Twitter quedan fuera de v1 (se valoran en v2 con flujo semi-manual).

---

## Contexto

Soy investigador y consultor. Mi proyecto **Synergium** es un broker de colaboraciones de investigación entre LATAM y Europa: conecto grupos/universidades de Latinoamérica con socios europeos para proyectos Horizon, convocatorias internacionales y publicaciones conjuntas. Mi diferenciación es la triada **investigación + transferencia tecnológica + comunicación** (tengo un podcast de investigación con 390+ episodios).

Clientes potenciales:
- Investigadores principales (IPs)
- OTRIs y oficinas de transferencia
- Vicerrectorados de investigación
- Agencias de ciencia
- Foco geográfico: Chile, México, Colombia, Uruguay

## Qué quiero construir

Código (Python) que **rastree la web abierta para encontrar gente que expresa públicamente un dolor que yo resuelvo** y los meta en una tabla de seguimiento. No busco competidores como prioridad; busco a quien **se queja o pide ayuda sin saber que existe una solución** — ahí está el cliente.

### Señales de dolor a detectar (ejemplos)

- "looking for partners" / "seeking partners" / "buscamos socios" / "nos falta un partner" Horizon
- "open call for partners" / "expression of interest" / "completing consortium"
- "looking for collaborators EU" / "seeking European collaborator"
- Universidades LATAM anunciando "estrategia de internacionalización" sin medios claros para ejecutarla
- Investigadores expresando frustración con internacionalización, financiación europea o búsqueda de socios

Hay una lista más larga de términos por idioma y país en la nota hermana [busqueda-competidores-prospectos-linkedin-twitter.md](../../../notas-derivadas/casos/analisis-ideas-negocio-synergium/busqueda-competidores-prospectos-linkedin-twitter.md). Cárgala como configuración externa, no la hardcodees.

## Alcance v1 (esta iteración)

**Fuentes a soportar de salida:**
1. **Web abierta** vía búsqueda + fetch de páginas (respetando robots.txt y rate limits).
2. **NCPs Horizon Europe** (National Contact Points): páginas oficiales por país (España, Chile, México, Colombia, Uruguay y otros LATAM) donde se publican convocatorias con necesidad de partners.
3. Subfuentes asociadas a NCPs si surgen de forma natural (portal oficial UE de partner search, páginas de oficinas regionales, etc.).

**Fuera de alcance en v1:**
- LinkedIn (no scrapeable, sin API útil) — irá en v2 como flujo semi-manual.
- Twitter/X (depende del coste de API) — irá en v2.
- Sales Navigator (manual siempre, no automatizar).

## Restricciones técnicas

- Respetar robots.txt y rate limits de cada dominio.
- Sin cabeceras falsificadas ni evasión activa.
- Cachear lo descargado para no re-pegar a las fuentes.
- Logs claros de qué URL se visitó, cuándo y con qué resultado.

## Diseño esperado

1. **Configuración externa** (YAML o JSON), editable sin tocar código:
   - Términos de búsqueda agrupados por objetivo (`dolor_prospectos`, `competidores_aprender`, `eventos`).
   - Términos por idioma (es, en) y por país.
   - Lista de fuentes a rastrear (URLs base, tipo de fuente, frecuencia).
2. **Módulos de fuente intercambiables** con interfaz común. v1 implementa al menos:
   - `web_generica`: búsqueda + fetch.
   - `ncp_horizon`: rastreo de páginas oficiales de NCPs.
3. **Tabla de seguimiento** en CSV + Markdown con columnas:
   `fecha_deteccion | plataforma | autor_o_cuenta | titulo_o_extracto | senal_de_dolor | URL | tema | pais | categoria | estado | proximo_paso | relevancia_1_5 | mensaje_sugerido`
   - `categoria` toma uno de dos valores: `personal` o `INV_AMP`.
4. **Deduplicación** por URL (y opcionalmente por hash de contenido) entre ejecuciones.
5. **Análisis con LLM** sobre lo recolectado:
   - Clasificar dolor real vs. ruido.
   - Puntuar relevancia 1-5 para Synergium.
   - Sugerir primer mensaje de contacto personalizado (no enviar nada — solo redactar).
6. **Ejecución incremental**: pensado para correrlo cada semana y que solo añada lo nuevo a la tabla.

## Convenciones del proyecto

- Solo escribir dentro de `cursor_obsidian/`. La vault de Obsidian es **solo lectura**.
- Código en `scripts/`; salidas (tablas, logs, resultados) en `generado/buscador-prospectos/casos/<pedido>/`.
- No usar los términos "trabajo" / "work" / "bio-hpc". Para la segunda categoría de seguimiento usar **INV_AMP**.
- Comunicación en español, sin emojis.

## Lo que quiero primero

Antes de programar, dame:
1. Un **plan de arquitectura**: módulos, fuentes concretas a soportar en v1, librerías Python propuestas, estructura de la config, esquema de la tabla.
2. Las **decisiones que necesitas que confirme** antes de empezar.

No empieces a programar hasta que valide el plan.

## Notas de versiones futuras

- **v2**: añadir flujo semi-manual de LinkedIn (yo pego URLs/textos en lote, el código analiza y clasifica) y, si la API de Twitter/X resulta viable en coste, automatizar Twitter/X.
- **v3**: monitoreo de eventos de matchmaking (B2Match, info days) detectando aperturas/cierres de convocatorias.
