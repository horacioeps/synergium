# Auditoría copy + campos — nexus-input (2026-08-21)

Contexto: el intro ya es profesional; el cuerpo del formulario aún arrastra tono de grupo WhatsApp. Campo nuevo: `how_found_form` (al final, antes de `anything_else`).

## Veredicto

El **núcleo de matching** (quién eres, qué haces, qué ofreces, qué necesitas, geo, horizonte, consentimiento de intro) está bien. Sobran **preguntas de investigación de mercado** al final del bloque medio, y faltan pocos campos duros. Varias etiquetas suenan de chat, no de servicio profesional.

## Lenguaje poco profesional (prioridad alta)

| id | Ahora | Propuesta |
|----|--------|-----------|
| `email` | Email (uno que revises de verdad) | Correo electrónico (el que consulta con regularidad) |
| `what_you_do` | …Lo concreto gana a lo impresionante. | …Priorice hechos concretos frente a formulaciones genéricas. |
| `need_now` | Necesitas AHORA | Necesidad actual |
| `what_you_seek` | Un vago «alguien en Europa»… | Evite descripciones genéricas (p. ej. «alguien en Europa»); indiquen tema, perfil y plazo. |
| `offer_next_months` | Estudiantes/manos de lab | Estudiantes / apoyo de laboratorio |
| `english_for_collab` | Me apaño | Nivel suficiente para trabajar |
| `match_me` | ¿Emparejarme? / Solo tú ves… | ¿Desea que le propongamos emparejamientos? / Solo el equipo ve los datos, sin introducción aún |
| `intro_channel` | Cualquiera | Indiferente |
| `later_write` | …match en la comunidad (fuera de intro, episodio)… | Más adelante, si Synergium puede ayudarle más allá de un emparejamiento, ¿podemos contactarle? |
| `also_spanish_community` | ¿También en la comunidad en español? | ¿Participa también en el canal en español? (o retirar; ver abajo) |
| `three_words` | 3 palabras para que te encuentren | Tres términos identificativos (además de palabras clave) |
| `anything_else` | Algo más para emparejarte | Información adicional útil para el emparejamiento |
| `how_found_form` | ¿Cómo te llegó…? (tú) | ¿Cómo obtuvo este formulario? (usted) — coherente con el resto formal |

EN: mismos ajustes (cut “one you actually check”, “Get by”, “Whatever”, “Need NOW”, scolding tone in seek).

## Sobran o sobran peso (candidatas a cortar / hacer opcionales)

Bloque **señal Synergium / mercado** (útiles para producto, poco para el match del día 1):

1. `last_unknown_collab_via`
2. `last_email_paper_author`
3. `follow_up_problem`
4. `recent_pubs_same_circle`
5. `institution_funds_intl`

**Recomendación:** pasarlas a opcionales, o a un segundo formulario corto post-submit, o dejar solo `blockers` + `institution_funds_intl`.

Otras:

| id | Motivo |
|----|--------|
| `three_words` | Solapa con `keywords`; elegir una |
| `also_spanish_community` | Asume dos grupos WhatsApp; confunde si llega por Discord / universidad / email |
| `years_in_research` | Útil pero no crítico; puede ser opcional |

## Faltan (pocas, de alto valor)

| Prioridad | Campo | Por qué |
|-----------|--------|---------|
| Alta | Ya: `how_found_form` | Atribución de canal |
| Media | Consentimiento explícito de tratamiento de datos (sí/no) | Alinea el tono legal del intro |
| Media | ORCID en campo propio (además de `profile_urls`) | Matching y dedupe |
| Baja | Modalidad preferida (remoto / híbrido / presencial) | Filtra estancias vs paper remoto |
| Baja | Disponibilidad semanal aproximada | Solo si se vende follow-up guiado |

No hace falta inflar el form: con etiqueta profesional + recortar el bloque 23-27 ya baja mucho la fricción.

## Estructura sugerida (sin reescribir todo aún)

1. Identidad y contacto  
2. Perfil científico  
3. Oferta / necesidad / búsqueda (núcleo)  
4. Preferencias (geo, tiempo, convocatoria)  
5. Consentimiento de intro + canal  
6. Atribución (`how_found_form`) + texto libre  
7. (Opcional) bloque mercado Synergium

## Hecho ya (2026-08-21)

- `how_found_form` al final (antes de `anything_else`), required, con Other.
- Opciones: WhatsApp, Discord, Email, colega, universidad/institución, LinkedIn, Podcast, Web Synergium.
- Notify email incluye `How found form`.
