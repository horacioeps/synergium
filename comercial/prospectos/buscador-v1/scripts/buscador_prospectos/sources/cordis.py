"""CORDIS source: outreach lateral a coordinadores de proyectos recientes Horizon Europe.

Distinto de EEN/B2Match (partner search activo) — CORDIS lista proyectos ya
financiados. El angulo es identificar coordinadores europeos de proyectos
en tu dominio para ofrecerles colaboracion en futuras calls o spin-offs.

Bulk CSV oficial UE: ~34 MB ZIP, ~22k proyectos Horizon Europe.
Auto-descarga si falta o esta caducada (cache 7 dias).
"""
from __future__ import annotations

import csv
import logging
import re
import zipfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from time import time
from urllib.request import urlopen

from pydantic import BaseModel
from typing import Literal

from ..config import cache_dir, NcpHorizon, WebGenerica  # noqa: F401
from .base import Candidato, Source

log = logging.getLogger(__name__)

BULK_URL = "https://cordis.europa.eu/data/cordis-HORIZONprojects-csv.zip"
CACHE_TTL_DAYS = 7

# Filtros (configurables via config en el futuro; por ahora hardcoded sensible)
CLUSTER_RE = re.compile(r'^HORIZON-(CL4|CL5|CL6|HLTH|MISS)', re.IGNORECASE)
DOMAIN_RE = re.compile(
    r'\b(drug discovery|bioinformatic|structural biolog|virtual screening|'
    r'molecular dynamics|cheminformatic|chemoinformatic|drug design|'
    r'computational biolog|computational chemist|fragment.based|'
    r'high.performance computing|HPC simulation|'
    r'machine learning|deep learning|artificial intelligence|AI.driven|AI.based|'
    r'genomic|proteomic|metabolomic|microbiom|biomarker|'
    r'agri.food|agroecolog|food safety|food technolog|food chain|'
    r'green chemistry|nanomaterial|biomass|biorefiner|fermentation|biotech)\b',
    re.IGNORECASE)


class CordisConfig(BaseModel):
    """Config schema para fuente CORDIS en sources.yaml."""
    id: str
    tipo: Literal["cordis"]
    activa: bool
    meses_atras: int = 6   # cuanto miramos hacia atras
    max_resultados: int = 50   # tope por corrida


def _bulk_zip_path() -> Path:
    return cache_dir() / "cordis" / "cordis-HORIZONprojects-csv.zip"


def _extracted_dir() -> Path:
    return cache_dir() / "cordis" / "extracted"


def _is_cache_fresh(p: Path) -> bool:
    if not p.exists():
        return False
    age_days = (time() - p.stat().st_mtime) / 86400
    return age_days < CACHE_TTL_DAYS


def _ensure_bulk() -> Path:
    """Descarga el bulk si falta o tiene mas de CACHE_TTL_DAYS dias."""
    zp = _bulk_zip_path()
    if _is_cache_fresh(zp):
        log.info("CORDIS bulk fresco en cache (%s)", zp)
    else:
        zp.parent.mkdir(parents=True, exist_ok=True)
        log.info("Descargando CORDIS bulk (~34 MB) -> %s", zp)
        with urlopen(BULK_URL, timeout=180) as r, open(zp, "wb") as f:
            f.write(r.read())
        log.info("CORDIS bulk descargado: %d bytes", zp.stat().st_size)

    ed = _extracted_dir()
    if not ed.exists() or not _is_cache_fresh(ed):
        ed.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zp) as z:
            z.extractall(ed)
        log.info("CORDIS bulk extraido en %s", ed)
    return ed


def _coordinators_index(ed: Path) -> dict[str, dict]:
    """Mapea projectID -> dict del coordinador (role=coordinator)."""
    out: dict[str, dict] = {}
    csv.field_size_limit(10**7)
    with (ed / "organization.csv").open() as f:
        for r in csv.DictReader(f, delimiter=';'):
            if (r.get("role") or "").lower() == "coordinator":
                out[r["projectID"]] = r
    return out


def _topics_index(ed: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    csv.field_size_limit(10**7)
    with (ed / "topics.csv").open() as f:
        for r in csv.DictReader(f, delimiter=';'):
            out.setdefault(r["projectID"], []).append(r["topic"])
    return out


class CordisSource(Source):
    """Genera candidatos a partir del bulk CSV oficial CORDIS Horizon Europe."""

    def __init__(self, cfg: CordisConfig) -> None:
        self.cfg = cfg
        self.id = cfg.id
        self.tipo = cfg.tipo
        self.activa = cfg.activa

    def discover(self) -> list[Candidato]:
        ed = _ensure_bulk()
        coords = _coordinators_index(ed)
        topics = _topics_index(ed)

        cutoff = date.today() - timedelta(days=int(self.cfg.meses_atras * 30.5))
        out: list[Candidato] = []
        csv.field_size_limit(10**7)
        with (ed / "project.csv").open() as f:
            for r in csv.DictReader(f, delimiter=';'):
                try:
                    sd = date.fromisoformat((r.get("startDate") or "")[:10])
                except Exception:
                    continue
                if sd < cutoff:
                    continue
                pid_topics = topics.get(r["id"], [])
                if not any(CLUSTER_RE.search(t) for t in pid_topics):
                    continue
                text = (r.get("title", "") + " " + r.get("objective", "") + " " + r.get("keywords", ""))
                if not DOMAIN_RE.search(text):
                    continue
                coord = coords.get(r["id"])
                if not coord or not coord.get("name"):
                    continue

                # Resumen del objective para extracto
                obj = (r.get("objective") or "").strip().replace("\n", " ")
                if len(obj) > 700:
                    obj = obj[:700] + "..."
                topic_short = "; ".join(pid_topics[:2])
                extracto = (
                    f"CORDIS - OUTREACH LATERAL. Coordinador europeo {coord.get('name')} "
                    f"({coord.get('country','')}, {coord.get('city','')}) ha ganado el proyecto "
                    f"Horizon \"{r.get('acronym','')}\" ({topic_short}) iniciado {sd.isoformat()}. "
                    f"EC max contribution: {r.get('ecMaxContribution','-')}. "
                    f"Objective: {obj}"
                )

                out.append(Candidato(
                    url=f"https://cordis.europa.eu/project/id/{r['id']}",
                    titulo=f"[{r.get('acronym','')}] {r.get('title','')}",
                    extracto=extracto,
                    fuente_id=self.id,
                    plataforma="cordis",
                    autor=coord.get("name"),
                    pais=coord.get("country"),
                    idioma="en",
                    objetivo="cordis_outreach",
                    termino_origen=f"cluster/{topic_short[:30]}",
                    fecha_publicacion=sd.isoformat(),
                    metadata={
                        "acronym": r.get("acronym"),
                        "topic": topic_short,
                        "coord_url": coord.get("organizationURL", ""),
                        "contact_form": coord.get("contactForm", ""),
                        "ec_max_contribution": r.get("ecMaxContribution", ""),
                        "endDate": r.get("endDate", ""),
                        "tipo_outreach": "lateral_proyecto_ganado",
                    },
                ))

        out.sort(key=lambda c: c.fecha_publicacion or "", reverse=True)
        if len(out) > self.cfg.max_resultados:
            log.info("CORDIS: %d candidatos brutos, recortando a %d", len(out), self.cfg.max_resultados)
            out = out[:self.cfg.max_resultados]
        else:
            log.info("CORDIS: %d candidatos finales", len(out))
        return out
