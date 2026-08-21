# Emails opt-in — Match #4 (borrador)

**De:** Horacio Pérez-Sánchez `<horacio@horacio-ps.com>`  
**Vía:** Emailer_X (`scripts/main/send_test_email.py --account 1`)  
**Estado:** **Borrador — no enviar hasta que Horacio confirme el texto.**  
**Fecha:** 2026-08-21 (rev. nombre completo + sin presentación + enlace form)

Principios del primer mensaje:

- Ya te conocen → **sin presentarte**.
- Viene de **Synergium** y del **formulario** (enlace `nexus-input`).
- Habla de la otra persona en **términos generales**.
- **Sin nombre, sin institución concreta, sin métodos detallados.**
- Primer paso: solo sí/no a una posible presentación.
- Línea en blanco entre párrafos.
- Nombre real Driselda: **Driselda Patricia Sánchez Aguirre** (UNAM / ORCID).

Formulario: https://forms.synergium.net/nexus-input

---

## A → Driselda Patricia Sánchez Aguirre

**Para:** dsanchez@encit.unam.mx  
**Asunto:** Synergium — posible colaboración (patrimonio / territorio)

```
Hola Driselda,

Te escribo desde Synergium a partir de lo que dejaste en el formulario de matching (https://forms.synergium.net/nexus-input).

Hay alguien en el directorio — investigadora en Colombia, en ciencias sociales y humanidades, con trabajo en torno a patrimonio, territorio e historia — con quien veo un encaje razonable a nivel general con lo que comentaste (patrimonio y temas afines, interés en paper / colaboración).

Esto es solo un primer paso: ¿te parecería bien que, si ella también quiere, os presente por email? Sin compromiso; si no encaja, lo dices y no paso ningún dato.

Un saludo,
Horacio
```

---

## B → Tatiana González L

**Para:** tatiana.gonzalezl@udea.edu.co  
**Asunto:** Synergium — posible colaboración (patrimonio / territorio)

```
Hola Tatiana,

Te escribo desde Synergium a partir de lo que dejaste en el formulario de matching (https://forms.synergium.net/nexus-input).

Hay alguien en el directorio — investigadora en México, también en el eje patrimonio / humanidades (turismo, patrimonio y temas cercanos) — con quien veo un encaje razonable a nivel general con lo que comentaste (territorio, patrimonio, historia; interés en movilidad y colaboración).

Esto es solo un primer paso: ¿te parecería bien que, si ella también quiere, os presente por email? Sin compromiso; si no encaja, lo dices y no paso ningún dato.

Un saludo,
Horacio
```

---

## Cómo enviar (cuando confirmes)

Desde el clone local de Emailer_X:

```bash
cd "/Users/horacio/Documents/Documents - horacio/Personal/Coding/Emailer X local"
./venv/bin/python scripts/main/send_test_email.py \
  --account 1 \
  --to "dsanchez@encit.unam.mx" \
  --subject "Synergium — posible colaboración (patrimonio / territorio)" \
  --body "$(cat <<'EOF'
…cuerpo A…
EOF
)"
```

Repetir para Tatiana con el cuerpo B. Cuenta `1` = `horacio@horacio-ps.com` (Ionos) vía `config/config.test.ini`.

---

## Tras el envío

1. Marcar enviados en [historial-contacto.md](historial-contacto.md).
2. Esperar sí/no de ambas.
3. Si doble sí → intro conjunta (nombres + emails; playbook matching).
