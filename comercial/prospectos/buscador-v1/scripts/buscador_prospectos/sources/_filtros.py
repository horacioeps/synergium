"""Pre-filtros comunes aplicados antes de pasar candidatos al LLM."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from .base import Candidato

# Antiguedad maxima aceptable para considerar un candidato accionable.
# Las convocatorias suelen tener ventana corta; un "looking for partners"
# de hace mas de 3 meses suele estar ya cerrado o el consorcio ya formado.
ANTIGUEDAD_MAX_MESES = 3


# Tokens en URL o titulo que descalifican el candidato (fuera de dominio Synergium).
# Casos vistos: NEB Bauhaus, S-Cultural, partner search para arte/musica/cultura.
TOKENS_OFF_DOMAIN = (
    " bauhaus", " neb-", "/neb-", " neb ", "new-european-bauhaus",
    " s-cultural", "s-cultural ", "/s-cultural",
    " cultural inclusion", "social-inclusion", " inclusion social",
    " music ", " musica", " música", " musical",
    " arte ", " artes ", " artistic ", "artistic-intelligence",
    " heritage", "patrimonio-cultural", "heritage-01",
    "creative-industries", "industrias-creativas",
    " gastronomia ", " gastronomy ", " turismo ", " tourism ",
    "periodismo", "journalism",
    "humanidades", "humanities ",
    "filosofia ", "filosofía ", "philosophy ",
)


def _ano_de_url(url: str) -> int | None:
    """Detecta /YYYY/ en la URL como pista de fecha. Solo si esta en rango razonable."""
    m = re.search(r"/(20\d{2})/", url)
    if not m:
        return None
    a = int(m.group(1))
    if 2010 <= a <= 2100:
        return a
    return None


def _parsear_fecha(s: str | None) -> date | None:
    if not s:
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d", "%d/%m/%Y", "%Y"):
        try:
            d = datetime.strptime(s, fmt)
            return d.date()
        except Exception:
            continue
    return None


def es_off_domain(c: Candidato) -> bool:
    """True si el candidato cae claramente en un dominio fuera de Synergium
    (arte, cultura, musica, inclusion social, patrimonio, turismo, humanidades)."""
    corpus = ((c.url or "") + " " + (c.titulo or "") + " " +
              (c.extracto or "")).lower()
    return any(t in corpus for t in TOKENS_OFF_DOMAIN)


def es_demasiado_viejo(c: Candidato, ref: date | None = None,
                       max_meses: int = ANTIGUEDAD_MAX_MESES) -> bool:
    """True si tiene fecha conocida y es mas vieja que `max_meses`. Si no hay
    fecha, devuelve False (no filtramos por defecto a falta de evidencia)."""
    ref = ref or date.today()
    cutoff = ref - timedelta(days=int(max_meses * 30.5))

    f = _parsear_fecha(c.fecha_publicacion)
    if f is None:
        a = _ano_de_url(c.url)
        if a is not None:
            f = date(a, 6, 30)   # asumir mitad de ano si solo se sabe el ano
    if f is None:
        return False
    return f < cutoff


def aplicar_prefiltros(cands: list[Candidato]) -> tuple[list[Candidato], dict]:
    """Devuelve (candidatos_supervivientes, contadores_descartados).

    Los items de CORDIS (objetivo='cordis_outreach') NO pasan por filtro de
    antiguedad: un proyecto Horizon dura 3-4 anos, sigue siendo valido para
    outreach lateral aunque arrancara hace 6+ meses. Si pasan por off_domain.
    """
    out: list[Candidato] = []
    stats = {"off_domain": 0, "antiguo": 0, "supervivientes": 0}
    for c in cands:
        if es_off_domain(c):
            stats["off_domain"] += 1
            continue
        if c.objetivo != "cordis_outreach" and es_demasiado_viejo(c):
            stats["antiguo"] += 1
            continue
        out.append(c)
    stats["supervivientes"] = len(out)
    return out, stats
