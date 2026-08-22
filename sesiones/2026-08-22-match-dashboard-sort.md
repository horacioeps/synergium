
## 2026-08-22 ~18:15 CEST — Columnas ordenables en match dashboard

**Pedido:** Cabeceras de columna ordenables (asc/desc) en las 3 pestañas del dashboard; indicador visual; compatible con búsqueda; deploy VPS.

**Implementación:**
- `index.html`: estado `sortState` por pestaña; clic en `<th>` alterna asc/desc; indicador ↑↓ en columna activa; orden tras filtro de búsqueda; cabecera sticky intacta
- `MATCH-TRACKING.md`: nota una línea sobre ordenación
- Deploy rsync `match-dashboard/` → VPS (`/var/www/forms.synergium.net/match-dashboard/`)
- Sin regenerar `data.json` (solo cambio de UI)

**Pestañas:** Por match · Por participante · Directorio — todas con sort en todas las columnas.
