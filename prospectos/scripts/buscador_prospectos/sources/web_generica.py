from __future__ import annotations

import logging
import time
from urllib.parse import urlencode

import httpx

from ..config import WebGenerica, load_terms, require_env
from .base import Candidato, Source

log = logging.getLogger(__name__)

BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"


class WebGenericaSource(Source):
    def __init__(self, cfg: WebGenerica) -> None:
        self.cfg = cfg
        self.id = cfg.id
        self.tipo = cfg.tipo
        self.activa = cfg.activa

    def _brave_search(self, query: str, count: int) -> list[dict]:
        api_key = require_env("BRAVE_API_KEY")
        params = {
            "q": query,
            "count": min(count, 20),
            "search_lang": self.cfg.idioma,
            "country": "ES" if self.cfg.idioma == "es" else "US",
            "safesearch": "moderate",
        }
        if self.cfg.freshness:
            params["freshness"] = self.cfg.freshness
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        }
        try:
            with httpx.Client(timeout=20) as c:
                r = c.get(BRAVE_ENDPOINT, params=params, headers=headers)
                if r.status_code != 200:
                    log.warning("Brave %s para '%s': %s", r.status_code, query, r.text[:200])
                    return []
                data = r.json()
                return (data.get("web") or {}).get("results") or []
        except Exception as e:
            log.exception("Error en Brave para '%s': %s", query, e)
            return []

    def discover(self) -> list[Candidato]:
        terms = load_terms()
        try:
            queries = terms.objetivos[self.cfg.objetivo][self.cfg.idioma]
        except KeyError:
            log.warning("Sin terminos para %s/%s", self.cfg.objetivo, self.cfg.idioma)
            return []

        candidatos: list[Candidato] = []
        for q in queries:
            results = self._brave_search(q, self.cfg.max_resultados_por_termino)
            for r in results:
                candidatos.append(Candidato(
                    url=r.get("url", ""),
                    titulo=r.get("title"),
                    extracto=r.get("description"),
                    fuente_id=self.id,
                    plataforma="web",
                    idioma=self.cfg.idioma,
                    objetivo=self.cfg.objetivo,
                    termino_origen=q,
                    fecha_publicacion=(r.get("page_age") or r.get("age") or None),
                    metadata={"snippet_source": "brave",
                              "age_raw": r.get("age")},
                ))
            time.sleep(1.0)   # cortesia con la API
        return [c for c in candidatos if c.url]
