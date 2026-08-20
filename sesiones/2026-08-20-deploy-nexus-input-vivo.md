# Sesión 2026-08-20 — Deploy vivo nexus-input con secrets.env

## Usuario

> lo primero, he metido las varaibles en .cursor secrents.env mira a ve si con eso puedes [aplicar lo pendiente en vivo]

## Agente

1. Secrets en `~/.cursor/secrets.env`: SSH Horacio **SET**; `SYNERGIUM_FORMS_PB_*` no (se usó `.env` del VPS vía SSH).
2. Bug path en `apply_nexus_input.sh` (`REPO_ROOT` un nivel corto) → corregido.
3. Deploy OK:
   - rename `0mn7nfs5kqsi8g` → `nexus-input`
   - campo `source` añadido a submissions
   - front + Apache docroot
   - pm2 restart `synergium-forms`
4. Alias front invertido (legacy → nexus-input) y redesplegado.
5. Verificado: `GET /api/sf/form/nexus-input` → 200.

**URL viva:** https://forms.synergium.net/nexus-input
