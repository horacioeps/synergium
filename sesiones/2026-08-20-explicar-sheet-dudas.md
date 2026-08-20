# Sesión 2026-08-20 — Explicar Sheet sync + dudas numeradas

## Usuario

> "El Sheet ya lo tenemos identificado, pero el export público no abre…" esto no lo entiendo. y las dudas y sugerencias explicalas un poco mejor y a cada una dale un numero para que yo responda luego

## Respuesta al usuario (para contestar por número)

### Qué significaba lo del Sheet

Google Form y Synergium Forms son **dos tuberías**. Las respuestas del Form van al Spreadsheet; las de la web van a PocketBase. Para sync cada 15 min el VPS debe **leer** la hoja. Conocemos el ID, pero Google no deja bajar el CSV sin login → hace falta service account, hoja pública-visor, o CSV manual. Detalle en `forms/docs/GOOGLE-SHEET-SYNC.md`.

---

### Dudas (responde 1…N)

**1. Google Form abierto o cerrado**  
¿Seguimos aceptando respuestas en el Google Form (y las sync a nuestra BD), o lo cerramos / dejamos de compartirlo y solo usamos https://forms.synergium.net/nexus-input?

**2. Cómo leer el Spreadsheet**  
Elige una:  
- **2a** Service account (robot Google + JSON en el VPS; tú compartes la hoja con ese email).  
- **2b** Hoja “cualquiera con el enlace → Visor” (más fácil, menos privada).  
- **2c** De momento CSV manual (sin cron 15 min).

---

## Continuación — Horacio (hoja compartida)

> la hoja la tengo compartida… no puedes ????? + URL con gid=1537513728

**Agente:** Sí se puede. Fallo mío: exporté con `gid=0` (incorrecto). Con `gid=1537513728` el CSV responde **200** (~26 respuestas). Actualizado `GOOGLE-SHEET-SYNC.md`. La duda **2** queda resuelta en la práctica como **2b** (enlace público de lectura).
**3. Idioma en la URL**  
El selector ya está. ¿Te basta **una sola URL** (`nexus-input`) con el globo EN/ES/…, o quieres también una URL ES aparte (p. ej. `nexus-input-es`)?

**4. Secrets PocketBase en `~/.cursor/secrets.env`**  
Hoy el deploy usa SSH y el `.env` del VPS. ¿Quieres que añadamos también `SYNERGIUM_FORMS_PB_ADMIN_EMAIL` / `PASSWORD` al secrets.env local para publicar/renombrar sin SSH?

---

### Sugerencias (también numeradas; di sí/no o alternativa)

**5. WhatsApp con el enlace nuevo**  
Actualizar los mensajes de la comunidad a `https://forms.synergium.net/nexus-input` y, si hace falta, dejar el id viejo solo como redirección un tiempo.

**6. Deduplicar por email**  
Al importar del Sheet, si ese email ya está en PocketBase para ese form, no crear otra fila.

**7. Primero import masivo, luego cron**  
Traer de una vez las ~20 (o las que haya) filas actuales del Sheet; después montar el “cada 15 minutos” solo para lo nuevo.

**8. ES nativo en más forms**  
Cuando publiques otro form, conviene dejar `/i18n/{public_id}.es.json` (como nexus-input) para que ES no dependa de Google Translate.

---

## Usuario

> dime otras vez dudas y sugerencias

## Agente

Lista actualizada: **2** ya resuelta (2b). El resto igual, para que Horacio responda por número.
