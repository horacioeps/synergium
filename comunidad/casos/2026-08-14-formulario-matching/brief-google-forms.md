# Brief para Gemini — dos Google Forms (ES y EN)

Haz **dos** llamadas separadas a Gemini (o monta a mano). Un solo form bilingüe con saltos se rompe.

## Llamada 1 — español

Pega `formulario-es.md` y `privacidad.md` (bloque ES) y pide:

> Crea un Google Form en español con esta estructura exacta. Tuteo. Marca como obligatorias solo las preguntas con (*). Respeta tipos: texto corto, texto largo, selección única, casillas. Donde diga «Otro», activa «Otro» con campo libre. No añadas preguntas. No menciones marcas, Synergium, consultoría ni precios. Barra de progreso activada. Mensaje de confirmación = el del documento. En P2, validación de email. En P3, texto de ayuda con el ejemplo de código de país.

## Llamada 2 — inglés

Igual con `formulario-en.md` + bloque EN de `privacidad.md`:

> Create a Google Form in English with this exact structure. Mark as required only questions marked (*). Keep question types. Enable “Other” with a text field where specified. Do not add questions. Do not mention brands, Synergium, consulting or prices. Progress bar on. Confirmation message = the one in the document. P2 = email validation. P3 = help text with country-code example.

## Ajustes que Gemini suele olvidar (hazlos tú en Forms)

| Ajuste | Valor | Por qué |
|--------|--------|---------|
| Recopilar emails de Google | **OFF** | Van a rellenar desde el móvil de WhatsApp; el campo P2 es el email real. |
| Limitar a 1 respuesta | **OFF** | Si actualizan, te quedas con la fila más reciente por email/WhatsApp. |
| Restricción de dominio | **OFF** | La comunidad no es un Workspace. |
| Barra de progreso | ON | 8 secciones; si no ven avance, abandonan. |
| Preguntas barajadas | OFF | El orden es el matching. |
| Destino | Hoja de cálculo (una por idioma) | Luego fusionas por P1–P35. |
| Quién puede responder | Cualquiera con el enlace | |
| Editar tras enviar | ON si puedes | Menos duplicados. |

## Tras crearlos

1. Copia los dos `forms.gle` en `mensaje-whatsapp-es.md` y `mensaje-whatsapp-en.md` (hay un placeholder `PEGA_AQUI_EL_ENLACE`).
2. Rellena **tú** ambos forms de punta a punta en el móvil (8–10 min). Si te cansas en la sección 6, el resto también.
3. Comprueba que P2 rechaza «hola» y que P3 admite `+34 600111222`.
4. No indexar en Google; el link solo sale por WhatsApp.
