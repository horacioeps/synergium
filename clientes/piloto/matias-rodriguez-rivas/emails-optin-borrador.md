# Emails opt-in — Match #1 Matías Rodríguez-Rivas ↔ Valentina Lucena (borrador)

**De:** `horacio@horacio-ps.com` · EmailerX cuenta 1  
**Estado:** **Enviado** 2026-08-22 ~17:00 CEST (EmailerX VPS + copia IMAP → Elementos enviados)  
**Match ref:** `matias-valentina`

Sin presentación, sin em dashes, enlace form directorio, línea en blanco entre párrafos.

Form directorio: https://forms.synergium.net/nexus-input  
Form fase 2 (tras opt-in de ambos): https://forms.synergium.net/match-align

---

## ¿Ya le escribimos sobre este match?

| Contacto previo | Canal | Tema |
|-----------------|-------|------|
| 2026-08-06 | Email `mrodriguezri@udla.cl` | Solicitud PDF artículo VR/esquizofrenia (podcast) |
| 2026-08-06 | Email respuesta | PDF enviado |
| 2026-08-14 | Google Form EN | Community directory (`match_me=yes`) |
| **Opt-in match Valentina** | Email EmailerX | **Enviado** 2026-08-22 ~17:00 CEST |

Valentina: sí por WhatsApp (2026-08-20). Falta opt-in de Matías antes de intro conjunta.

---

## A → Matías Rodríguez-Rivas (ES)

**Para:** matiaserodriguezrivas@gmail.com  
**CC opcional:** mrodriguezri@udla.cl (donde respondió el PDF)  
**Asunto:** Synergium: posible coautoría (salud mental / artículos empíricos)

```
Hola Matías,

Te escribo desde Synergium por lo que dejaste en el formulario de matching de la comunidad:
https://forms.synergium.net/nexus-input

En el directorio hay una investigadora en España en salud mental y bienestar psicológico, con un enfoque clínico o aplicado. Por lo que contaste (buscas coautores para artículos empíricos y aportas diseño cuantitativo, análisis avanzado y metodología), puede haber encaje por roles complementarios más que por el mismo subtema.

Ella estaría dispuesta a avanzar en algo en las próximas semanas, no en un horizonte abierto.

¿Te parece bien que, si ella también quiere, os presente por email? Sin compromiso: si no encaja, lo dices y no paso ningún dato.

Un saludo,
Horacio
Synergium
https://synergium.net
horacio@horacio-ps.com
```

---

## Después del sí de Matías

1. Confirmar que Valentina sigue en (ya dijo sí; pedir email UCO si hace falta).
2. Enviar a **cada uno** el brief fase 2: https://forms.synergium.net/match-align (referencia `matias-valentina`).
3. Cuando ambos completen → resumen 1 página → intro conjunta ([playbook](../../../comunidad/casos/formulario-agosto-2026/playbook-matching.md)).

### WhatsApp Valentina (ES) — enlace match-align

```
Hola Valentina,

Antes de la intro conjunta, cada uno rellena un brief corto (5–8 min) para dejar claras expectativas de autoría, tiempos y datos. No es orientación: es el paso estándar del directorio.

https://forms.synergium.net/match-align

En «referencia del match» pon: matias-valentina

Cuando Matías también lo haya hecho, os presento con un resumen en una página.
```

---

## Nota idioma

Matías: opt-in en **ES** (2026-08-22). Valentina: ES → mensajes WA en español.

---

## Envío (EmailerX + copia Outlook)

Los envíos anteriores vía SES no aparecían en Outlook porque `send_test_email.py` no copiaba a IMAP. Usar `sent_copy` → carpeta **Elementos enviados** (Ionos):

```bash
# En VPS ~/EmailerX — patrón send_manual_replies.py
sent_copy={
  "host": imap["host"], "port": imap["port"],
  "login": imap["login"], "password": imap["password"],
  "folder": "Elementos enviados",
}
```
