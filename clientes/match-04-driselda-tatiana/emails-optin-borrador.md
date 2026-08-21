# Emails opt-in — Match #4 (borrador)

**De:** Horacio Pérez-Sánchez `<horacio@horacio-ps.com>`  
**Vía:** Emailer_X (`scripts/main/send_test_email.py --account 1`)  
**Estado:** **Borrador — no enviar hasta que Horacio confirme el texto.**  
**Fecha:** 2026-08-21 (rev. unslop, sin em dashes, firma visible)

Reglas de texto:

- Sin em dashes (`—`).
- Sin presentación (ya te conocen).
- Enlace form: https://forms.synergium.net/nexus-input
- Línea en blanco entre párrafos.
- Nombre Driselda: **Driselda Patricia Sánchez Aguirre**.

Firma (igual en ambos):

```
Un saludo,
Horacio
Synergium
https://synergium.net
horacio@horacio-ps.com
```

---

## A → Driselda Patricia Sánchez Aguirre

**Para:** dsanchez@encit.unam.mx  
**Asunto:** Synergium: posible colaboración (patrimonio / territorio)

```
Hola Driselda,

Te escribo desde Synergium por lo que dejaste en el formulario de matching:
https://forms.synergium.net/nexus-input

En el directorio hay una investigadora en Colombia, en ciencias sociales y humanidades, con trabajo sobre patrimonio, territorio e historia. Por lo que contaste (patrimonio y temas cercanos, interés en paper o colaboración), me parece que puede haber encaje.

¿Te parece bien que, si ella también quiere, os presente por email? Sin compromiso: si no encaja, lo dices y no paso ningún dato.

Un saludo,
Horacio
Synergium
https://synergium.net
horacio@horacio-ps.com
```

---

## B → Tatiana González L

**Para:** tatiana.gonzalezl@udea.edu.co  
**Asunto:** Synergium: posible colaboración (patrimonio / territorio)

```
Hola Tatiana,

Te escribo desde Synergium por lo que dejaste en el formulario de matching:
https://forms.synergium.net/nexus-input

En el directorio hay una investigadora en México, también en patrimonio y humanidades (turismo, patrimonio y temas cercanos). Por lo que contaste (territorio, patrimonio, historia, e interés en movilidad y colaboración), me parece que puede haber encaje.

¿Te parece bien que, si ella también quiere, os presente por email? Sin compromiso: si no encaja, lo dices y no paso ningún dato.

Un saludo,
Horacio
Synergium
https://synergium.net
horacio@horacio-ps.com
```

---

## Cómo enviar (cuando confirmes)

```bash
cd "/Users/horacio/Documents/Documents - horacio/Personal/Coding/Emailer X local"
./venv/bin/python scripts/main/send_test_email.py \
  --account 1 \
  --to "EMAIL" \
  --subject "Synergium: posible colaboración (patrimonio / territorio)" \
  --body "$(cat <<'EOF'
…cuerpo…
EOF
)"
```

Cuenta `1` = `horacio@horacio-ps.com` (Ionos). Hace falta `config/config.test.ini` local.
