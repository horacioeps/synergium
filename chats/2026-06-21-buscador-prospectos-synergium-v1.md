# 2026-06-21 — Buscador de prospectos Synergium v1 (web abierta + NCPs)

## Contexto inicial

Usuario aporta captura de tarea de la vault: "Implementar en cursor-claude: A los que postean en RRSS o la web accesible sobre los temas de los cuales quiero hacer consultoría, hacer tabla y seguirlos para: #personal y #work". Plan inicial ya esbozado por Claude (otro hilo) con búsquedas para Synergium en una nota generada previa.

## Lo que se hizo

1. **Resumen global** integrando la idea con notas relacionadas del vault (Synergium maestra, conversaciones validadas con Fabián León Vargas y Alexander García Dávalos, optimización LinkedIn 360Brew, etc.).
2. **Brief de spec** para Claude Code en `generado/buscador-prospectos/casos/v1-web-ncps/brief.md`. Alcance v1: web abierta + NCPs Horizon. LinkedIn/Twitter → v2.
3. **Plan de arquitectura** validado por el usuario:
   - Brave Search API (free 2k/mes)
   - OpenAI gpt-5-nano para clasificar + gpt-5-mini para redactar mensaje (split coste/calidad)
   - NCPs iniciales: ES, CL, MX, CO, UY (más EU Funding & Tenders)
   - Trigger manual
4. **Implementación completa** en `scripts/buscador_prospectos/`:
   - `cli.py` (typer): comandos `discover`, `analyze`, `run`, `report`
   - `config.py` (pydantic + dotenv): loaders de YAML
   - `fetch.py`: httpx + robots.txt + cache por sha256 + rate limit por dominio
   - `extract.py`: trafilatura
   - `analyze.py`: OpenAI con response_format json_object, cache LLM por hash de input
   - `tracking.py`: pandas, merge incremental por URL, salida CSV + Markdown
   - `sources/`: base ABC + web_generica (Brave) + ncp_horizon (BeautifulSoup con pistas semánticas) + registry
   - `prompts/clasificar.md` y `prompts/redactar.md` (criterios Synergium-específicos: relevancia 1-5, marca competidor, NO_REDACTAR para irrelevantes)
   - `config/terms.yaml` (objetivos × idioma × país, semilla extraída de la nota de búsqueda previa)
   - `config/sources.yaml` (fuentes activas + límites + nombres de modelo OpenAI editables)
5. **Decisiones marcadas en código**:
   - `_categoria_por_defecto()` devuelve siempre `INV_AMP` (regla CLAUDE.md). Pendiente reglas reales para distinguir personal vs INV_AMP.
   - Cache HTML y LLM en `generado/buscador-prospectos/cache/` (gitignored).
6. **Venv `.venv/` en raíz** con requirements instalados (httpx, trafilatura, pyyaml, pydantic, pandas, typer, python-dotenv, openai, beautifulsoup4).
7. **Smoke test** end-to-end:
   - NCP España `horizonteeuropa.es/noticias`: 200 OK, 104 candidatos extraídos.
   - NCP Uruguay `anii.org.uy/apoyos/`: redirige y termina en 404 (URL adivinada, hay que corregir).
   - Brave Search `"buscamos socios" Horizon`: devuelve 3 resultados en es con un post de LinkedIn real entre ellos.
   - OpenAI `gpt-5-nano` clasificando 3 candidatos del menú de España: los marca como ruido relevancia 1 — clasificación correcta.
8. **Seguridad**: las API keys se pegaron en chat → advertido al usuario que las rote (asumir comprometidas).

## Archivos tocados

- Creados:
  - `.gitignore`, `.env`
  - `generado/buscador-prospectos/casos/v1-web-ncps/brief.md`
  - `scripts/buscador_prospectos/` (paquete completo: cli, config, fetch, extract, analyze, tracking, sources/*, prompts/*, config/*, requirements.txt)
- Generados por smoke: `generado/buscador-prospectos/casos/smoke/{candidatos.jsonl,tracking.csv,tracking.md}` y `generado/buscador-prospectos/cache/{html,llm}/`.

## Pendientes explícitos para próxima sesión

1. **Verificar y corregir URLs de NCPs LATAM** (UY confirmado roto; CL/MX/CO sin verificar).
2. **Filtro previo en `ncp_horizon.py`**: excluir enlaces dentro de `<nav>`, `<header>`, `<footer>` antes de pasar al LLM (ahorrar tokens).
3. Primera corrida real `run --caso v1-web-ncps --limite 30` cuando el usuario lo apruebe.
4. Definir regla de asignación `personal` vs `INV_AMP` cuando haya datos reales.
5. Diseñar v2 con flujo semi-manual de LinkedIn (pegar lote de URLs/textos).

## Decisión de tono / preferencias

- Usuario rotando keys voluntariamente tras advertencia (sin pushback).
- Aceptó split nano+mini sin objetar (validación tácita de la propuesta de coste/calidad).

## Continuación misma sesión - primera corrida + iteraciones

### Corrida 1 (77 candidatos, prompt v1)
- NCP Chile (ANID) desactivado: 403 con Cloudflare incluso con UA del proyecto (regla: no spoofear).
- NCP Uruguay (ANII): subpaginas /apoyos/ redirigian a /error/ 404; cambiado lista_url a home anii.org.uy.
- Discover: 77 candidatos (36 Brave + 20 ES + 0 EU SPA + 0 CONAHCYT SPA + 20 CO + 1 UY).
- Analyze: 77 clasificados. Distribucion 0/2/5/18/52. 7 accionables (9%). Top: LinkedIn Diego Aburto "Lex Play" (FP), B2Match NEB matchmaking (real), URJC Búsquedas de socios, UVT Timișoara EOI.

### Mejora 1 - filtro nav/header/footer en ncp_horizon.py
- Eliminacion previa de nav/header/footer/aside/role=navigation/.menu/.cookie/etc antes de extraer enlaces.
- Lista de exclusion de patrones (cookie, login, telegram, sitemap, /feed, etc).

### Mejora 2 - prompt clasificar.md v2
- Anadidos ejemplos explicitos de falsos positivos vistos en run 1 (DJ Napo, "interesados en colaborar" genericos, concursos movilidad, ofertas empleo, paginas explicativas).
- Regla: "si dudas, elige la menor".
- Cache bumped a clasificar-v2 para invalidar.

### Corrida 2 (56 candidatos, prompt v2)
- Discover: 77 -> 56 (-27%) por filtro nav.
- Analyze: distribucion 1/2/8/8/37. 11 accionables (20%). x2 senal con la mitad de ruido.
- Top: S-Cultural UPO Sevilla (5), Sequoia Pro (4), Microfluidics IC (4), Agroecology AEI, Europa Direct Canarias, EURAXESS LAC, B2Match NEB, Chipre EOI, UVT Timișoara, DevelopmentAid HORIZON-CL5.

### Excel enriquecido (tracking.py: _escribir_excel + _hoja_tabla)
- openpyxl 3.1.5 anadido a requirements.
- 5 hojas: Prospectos accionables (>=3 no comp), Todo, Competidores, Ruido (1-2), Leyenda.
- Color por relevancia (verde 5 -> rojo 1, gris para competidores), URLs hyperlink, autofiltro, panel fijo B2, dropdown estado (nuevo/revisar/contactar/contactado/respondio/agendado/descartado/competidor), wrap text.
- Altura adaptativa por fila estimada de contenido envuelto (min 30 pt, max 420 pt) tras feedback de Horacio: la altura fija 80 cortaba mensajes largos. Estima lineas dividiendo texto por ancho_columna * 1.1 (factor empirico Calibri 11) + saltos \n explicitos.

### Mejora 3 - filtro de dominio en prompt clasificar.md v3
- Triggered por revision de #1 (S-Cultural): nano detecta dolor pero NO sabe si el tema encaja con Synergium.
- Anadidos al prompt: dominios ENCAJE (drug discovery, bioinformatica, HPC, IA en ciencia, salud, agro-food, energia/ambiente, quimica/materiales/sensores, deep-tech) vs NO ENCAJE (arte/musica/cultura, educacion no cientifica, humanidades, inclusion social, turismo/gastronomia, periodismo).
- Si NO encaje: max relevancia 2 + motivo "fuera de dominio Synergium".
- Cache bumped a clasificar-v3-dominio.

### Corrida 3 (56 candidatos, prompt v3 con filtro de dominio)
- Distribucion 1/3/12/22/18 (mas conservador en rel 1, mas generoso en 2-3).
- S-Cultural bajo de 5 a 4 (no a 2, filtro insuficiente para overrides fuertes).
- Top 5: B2Match NEB (5 NO encaje arte/inclusion), S-Cultural (4 NO encaje musica/STEAM), SBEP Blue Economy (4 encaje lateral blue biotech), Murcia Region Europea (4 encaje como aliado regional), Agroecology Partnership AEI (3 encaje fuerte agro-genomica).
- Verificacion manual con WebFetch de cada uno: tasa real de encaje 2.5/5 (50%). Murcia (Radware blocked) inferido por contexto.

## Aprendizajes operativos

1. **Cache LLM clave por (modelo+version+payload)**: bump version invalida solo lo necesario, mantiene candidatos identicos sin re-discover.
2. **Filtros precapa baratos > tokens caros**: 27% menos candidatos con un dom-stripping vale por miles de tokens.
3. **gpt-5-nano detecta dolor pero no encaje de dominio**. Para v1.2 conviene segunda pasada con mini sobre rel >=3, o reglas duras de keyword anti-arte/cultura, o anti-ejemplos en el prompt nano.
4. **Excel autofit no existe en openpyxl** para wrap_text - hay que estimar altura manualmente. Aceptable con factor 1.1 chars por unidad de ancho de columna en Calibri 11.
5. **Bot protection (Cloudflare, Radware) bloquea con cualquier UA legitimo**. Murcia y ANID Chile fuera de alcance sin spoofing (no se hace).

## Pendientes acumulados

1. Segunda pasada gpt-5-mini sobre rel>=3 para verificar encaje de dominio (mejora #4).
2. Anadir fuentes recurrentes detectadas: EURAXESS LAC, Europa Direct Canarias, B2Match (RSS si lo tiene), horizonteeuropa.es seccion matchmaking.
3. Resolver SPA: Playwright para EU Funding & Tenders + CONAHCYT (ahi vive el oro real).
4. Reglas personal vs INV_AMP en tracking.py (ahora todo INV_AMP).
5. v2 LinkedIn semi-manual.
6. Murcia: contacto fisico, no automatizable - aliado regional con distancia cero.

## Resultados que SI accionar esta semana

- **Agroecology Partnership AEI** (#5 del top 5): pre-propuestas feb 2026. Identificar grupos espanoles candidatos y ofrecer partner LATAM (agro-genomica).
- **Murcia Region Europea** (#4): visita en persona, ofrecer red LATAM como cobertura recurrente.
- **SBEP Blue Economy** (#3): watchlist, valorar si tienes acceso a grupos marinos LATAM (no es core pero abierto).

## Sesiones subsecuentes 2026-06-22 y 2026-06-23

### Iteracion v5 - Fecha de cierre de call (prompt v5)

Feedback usuario tras top 5 v4: Aisophical caducado. Anadida regla al prompt v5: si extracto/titulo contiene fecha_cierre_call anterior a fecha_hoy, max relevancia 1 con motivo "CALL CADUCADA". Anadido fecha_hoy al payload LLM. Bump cache key v5. Corrida enriquecida (--enriquecer, fetch+extract completo) sobre 180 candidatos.

Resultado v5: 30 accionables (rel>=3), 13 calls caducadas detectadas. Top 5 con WebFetch: BETA Tech UVic Anna Rovira (BIODIV-04, dic-2025), CNTA Daniel de la Puente (COMMUNITIES-01 + CIRCBIO-10, nov-2025), Baltic Tech Vitalija (11 calls HLTH), IRIS Technology Solutions Oonagh Mc Nerney (CIRCBIO-04 textiles), INEGI Porto Jaime Correia (STAYHLTH-02). Emails encontrados: **anna.rovira.andujar@uvic.cat** (Cloudflare decoded), **elisabet.perona@uvic.cat**, **vitalija.brazauskiene@kcci.lt**, resto no publicos.

### Iteracion v6 - Filtro 3 meses (mucho mas estricto)

Feedback usuario: todos los top 5 v5 tenian 4-7 meses de antiguedad; regla debe ser "no mas de 3 meses". Cambiado ANTIGUEDAD_MAX_MESES=3 en _filtros.py + prompt v6 con regla "publicacion >3 meses => rel 1 motivo PUBLICACION ANTIGUA". Anti-ejemplos anadidos (CNTA nov-2025, Gradiant feb-2026).

Resultado v6 (180 candidatos): distribucion 1/2/1/46/7 (0 rel5, 2 rel4, 1 rel3). 47 filtrados por PUBLICACION ANTIGUA, 10 por CALL CADUCADA. **Solo 1 accionable, y ni ese valia**. Diagnostico honesto: Brave indexa B2Match con retraso >3 meses; el pozo publico esta agotado con este filtro.

### Exploracion B - alternativas de fuente

Descartadas: B2Match GraphQL requiere auth (500 a anonimos, ToS), EEN 403 con UA descriptivo, EU F&T API blindada. **Pivote a Brave site:een.ec.europa.eu con freshness=pm** funciona: 21 candidatos ultimo mes -> 2 reales: RTO espanol BATT4EU CL5-2026-09-D2-01 (grafito + gigafactoria bio-based, 31-may-2026) y empresa griega plataforma IA biomedica (12-jun-2026).

### Canal SEIMED Murcia

EEN no expone emails directos. Encontrado nodo SEIMED (Comunitat Valenciana + Region de Murcia) en INFO: **seimed@info.carm.es** + Victoria Diaz. Borrador correo redactado desde UCAM (sin mencionar Synergium por explicito del usuario) para canalizar los 2 EEN.

### CORDIS integrado como fuente

Descargado bulk CSV oficial UE (34 MB, 22529 proyectos Horizon Europe). Filtro piloto: 6 meses + cluster CL4/CL5/CL6/HLTH/MISS + keywords dominio + rol=coordinator => **116 proyectos**. Excel enriquecido con top 5 mas recientes (verbatim del objective via WebFetch: NextBON, DigiWaves, ALT-PROACT, UNCOVER, COMBO) + los 116 ordenados por fit_score con color por encaje. Salida: `generado/buscador-prospectos/casos/cordis-piloto/cordis-coordinadores.xlsx`.

Nueva fuente `cordis_recent_coordinators` (sources/cordis.py + config.py Cordis + registry.py) con auto-download del bulk cacheado 7 dias. Prompt v7 con caso especial "OUTREACH LATERAL" (no aplica filtro >3 meses porque los proyectos duran anos; escala adaptada por dominio).

### Deepening EEN

15 queries EEN por dominio Synergium + doble freshness (`web_brave_een_partners_semana` pw + `web_brave_een_partners_mes` pm).

### Corrida final v7 (todas las fuentes)

283 candidatos brutos, 6 off_domain descartados, 282 clasificados. **61 accionables (rel>=3)**: 5 rel5 (4 CORDIS: COMBO/AIMARIA/COMEDI/PROTEUS + 1 B2Match: INEGI Porto STAYHLTH-02), 22 rel4 (21 CORDIS incluido UNCOVER-Zaragoza-CO2, AIR2FOOD-Imperial-fermentacion, PREPAIR-VAC-vacunas-IA, GENeCITY-Murcia-DT, BIOCORE-biorefineria; +1 EEN battery-graphite), 34 rel3 (CORDIS + EEN + B2Match + EURAXESS-MSCA + NCP-ES). 43 marcados PUBLICACION ANTIGUA, 11 CALL CADUCADA, 47 CORDIS outreach.

Excel resumen: **`tracking-accionables-61.xlsx`** con canal de contacto recomendado por fuente (CORDIS=contact form UE F&T, B2Match=in-platform, EEN=via SEIMED Murcia, EURAXESS=direct al PI, NCP=oficina nacional).

Volcado en chat de los 61 con verbatim/titulo + URL + canal + mensaje sugerido redactado por gpt-5-mini.

### Duplicados detectados

Los mismos partner-searches EEN aparecen doble (semana + mes freshness). Ejemplos: battery-graphite CL5 (#27=#52=#55), AI software (#53=#59), CRO biometrics (#54=#60), Greek cold-chain (#58=#61). **57 unicos reales**. Mejora pendiente: normalizar URL antes de dedup.

### Descartes durante la sesion

- **EURAXESS LAC** como fuente: recon dio 2 hits/mes en pozo generico; no compensa. Descartado.
- **B2Match scraping directo** (GraphQL + Playwright): requeriria cuenta + bordear ToS. Descartado.
- **Bing/spoof UA**: cruza regla del proyecto "sin cabeceras falsificadas".

### Incidente disco

99% lleno (12 GB libres de 926 GB), bloqueo I/O masivo (pandas import tardo 4 min). Usuario libero espacio a 19 GB antes de generar Excel final.

## Aprendizajes clave anadidos

1. **Filtro 3 meses es correcto pero incompatible con Brave** para fuentes lentas de indexacion (B2Match). Brave freshness=pm sirve para portales bien indexados (EEN, F&T).
2. **CORDIS bulk oficial UE es mejor que scraping**: 22k proyectos Horizon con coordinadores + contact forms en 34 MB descarga oficial. No requiere spoofing.
3. **CORDIS es OUTREACH LATERAL**, no partner-search. Los proyectos ya estan financiados; el angulo es futuras calls / spin-offs / papers con red LATAM.
4. **Canal EEN unico es via oficina SEIMED local** (Murcia: seimed@info.carm.es). No hay email directo publicado.
5. **Deduplicacion por URL necesita normalizar** (www vs no-www, con/sin trailing slash, doble freshness genera duplicados).
6. **Nano LLM se equivoca inferiendo pais** (INEGI Porto Portugal marcado como MX Mexico por acronimo). Confiar en el pais de la fuente, no solo en el codigo devuelto.

## Pendientes prioritarios

1. Deduplicacion URL robusta (normalizar www/scheme/trailing).
2. Cron semanal o cuando el usuario decida.
3. **Enviar los 5 rel5 esta semana** (4 CORDIS contact forms + 1 B2Match INEGI Porto).
4. Segunda pasada mini para filtrar encaje de dominio en CORDIS outreach.
5. Anadir queries EEN mas amplias por dominios secundarios (energia, sensores).

## Archivos finales de la sesion

- `scripts/buscador_prospectos/` (paquete completo: sources incluye ahora cordis.py + _filtros.py; prompt v7)
- `generado/buscador-prospectos/casos/v1-web-ncps/`: brief.md, candidatos.jsonl (283 candidatos), tracking.csv (282 clasificados), tracking.md, tracking.xlsx (todos), **tracking-accionables-61.xlsx (los 61)**
- `generado/buscador-prospectos/casos/cordis-piloto/`: cordis_coordinadores_6meses_synergium.csv (116), cordis-coordinadores.xlsx
- `generado/buscador-prospectos/cache/`: html/ (fetches), llm/ (~1000 entries), cordis/ (bulk + extracted)

## Ask vs Done (28 asks del usuario)

Hecho:
1. Entender captura de tarea + notas relacionadas vault (Explore agent + resumen global)
2. Brief para Claude Code (guardado, arranque con web abierta + NCP)
3. Implementar en este chat (opcion B); arquitectura Brave + OpenAI nano/mini
4. Guardar keys .env + aviso rotacion (usuario las pego en chat)
5. Explicar el proyecto + arreglar URLs NCPs + primera corrida (77 candidatos)
6. Excel enriquecido tras Markdown; altura adaptativa tras feedback de filas cortadas
7. WebFetch S-Cultural UPO Sevilla → verdicto SKIP + diagnostico dominio
8. Filtro dominio + WebFetch top 5 → tasa real encaje 2.5/5
9. Filtros fecha + off-domain + prompt v4 tras 'nada vale nada, ten en cuenta las fechas'
10. 3 fuentes nuevas (EURAXESS+B2Match+F&T) → 12 accionables
11. Top con verbatim + mensaje + email (Anna Rovira anna.rovira.andujar@uvic.cat, Elisabet Perona elisabet.perona@uvic.cat, Vitalija Brazauskiene vitalija.brazauskiene@kcci.lt)
12. Umbral 3 meses + prompt v6 (feedback 'no mas de 3 meses')
13. Deepening EEN (15 queries + doble freshness) tras confirmar que pozo Brave estaba agotado
14. SEIMED Murcia (seimed@info.carm.es) + correo redactado desde UCAM sin Synergium
15. CORDIS piloto (bulk 34MB, 116 proyectos, Excel fit_score)
16. CORDIS integrado como fuente en pipeline con OUTREACH LATERAL en prompt v7
17. Corrida final 282 candidatos → **61 accionables**
18. Excel resumen focalizado tracking-accionables-61.xlsx
19. Volcado en chat de los 61 con verbatim + URL + canal + mensaje-sugerido
20. Sesion guardada (chat + README + build_mapa_sesiones + MAPA regenerado)

NO hecho (con motivo):
- EURAXESS LAC como fuente: descartado tras recon (2 hits/mes)
- Top 5 CORDIS por fit_score en el Excel del piloto: ofrecido como iteracion, no cambiado sin confirmacion
- WebFetch de 61 emails uno a uno: ineficiente cuando ya teniamos mensajes redactados
- B2Match scraping GraphQL directo: requiere auth + bordea ToS
- Dedup URL robusta: pendiente (57 unicos reales de 61 nominales)
- Cron semanal: pendiente (manual por ahora)

Contactos con email confirmado:
- Anna Rovira Andujar (BETA Tech UVic, BIODIV-04): **anna.rovira.andujar@uvic.cat**
- Elisabet Perona-Vico (BETA Tech UVic, SOIL-02/03): **elisabet.perona@uvic.cat**
- Vitalija Brazauskiene (Baltic Tech Park KCCI, HLTH-2026): **vitalija.brazauskiene@kcci.lt**
- SEIMED Murcia (canal EEN para toda la region): **seimed@info.carm.es**

Contactos via formulario oficial UE F&T (los 42 CORDIS + Cluster Health B2Match)
