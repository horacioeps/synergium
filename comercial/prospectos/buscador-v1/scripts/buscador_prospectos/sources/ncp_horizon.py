from __future__ import annotations

import logging
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from ..config import NcpHorizon
from ..fetch import fetch
from .base import Candidato, Source

log = logging.getLogger(__name__)

# Palabras-pista que indican que el enlace probablemente es una convocatoria,
# noticia o partner search relevante (no menu/footer/sesion).
PISTAS_RELEVANTES = (
    "convocatoria", "concurso", "call", "noticia", "noticias",
    "anuncio", "partner", "consortium", "consorcio", "horizon",
    "internacional", "cooperacion", "cooperación",
    # EURAXESS jobs/funding/hosting partner offers
    "msca", "marie-sklodowska", "marie-curie", "fellowship", "postdoctoral",
    "expression-interest", "expression of interest", "/jobs/funding",
    "/jobs/hosting",
)

# Patrones a EXCLUIR aunque haya escapado al filtro de pistas.
# Cosas que no son contenido (login, cookies, redes, pdfs de plantilla, etc.)
PISTAS_EXCLUIR = (
    "cookie", "privacidad", "aviso-legal", "aviso legal", "legal-notice",
    "login", "iniciar-sesion", "registro", "registrate",
    "telegram", "whatsapp", "twitter.com", "facebook.com", "instagram.com",
    "linkedin.com/sharing", "youtube.com/channel",
    "/feed", "rss", "sitemap",
)


class NcpHorizonSource(Source):
    def __init__(self, cfg: NcpHorizon) -> None:
        self.cfg = cfg
        self.id = cfg.id
        self.tipo = cfg.tipo
        self.activa = cfg.activa

    def discover(self) -> list[Candidato]:
        log.info("Discover NCP %s -> %s", self.id, self.cfg.lista_url)
        res = fetch(self.cfg.lista_url)
        if not res.html:
            log.warning("NCP %s sin html (%s)", self.id, res.error)
            return []

        base_netloc = urlparse(self.cfg.lista_url).netloc
        soup = BeautifulSoup(res.html, "html.parser")

        # Eliminar nav/header/footer/aside/menu/breadcrumb antes de extraer enlaces.
        # Tambien tags semanticos por rol (role="navigation" / "banner" / "contentinfo")
        # y patrones de clase frecuentes en Wordpress/Drupal/temas comunes.
        for tag in soup.find_all(["nav", "header", "footer", "aside"]):
            tag.decompose()
        for sel in [
            '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]',
            '.menu', '.nav', '.navbar', '.sidebar', '.breadcrumb', '.breadcrumbs',
            '.cookie', '.cookies', '.cookie-banner', '#cookie', '#cookies',
            '.social', '.social-links', '.skip-link',
        ]:
            for tag in soup.select(sel):
                tag.decompose()

        candidatos: list[Candidato] = []
        vistos: set[str] = set()

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            url = urljoin(self.cfg.lista_url, href)
            if urlparse(url).netloc != base_netloc:
                continue   # solo enlaces internos del propio NCP
            titulo = (a.get_text() or "").strip()
            if not titulo or len(titulo) < 8:
                continue
            corpus = (url + " " + titulo).lower()
            if any(p in corpus for p in PISTAS_EXCLUIR):
                continue
            if not any(p in corpus for p in PISTAS_RELEVANTES):
                continue
            if url in vistos:
                continue
            vistos.add(url)
            candidatos.append(Candidato(
                url=url,
                titulo=titulo,
                fuente_id=self.id,
                plataforma="ncp",
                pais=self.cfg.pais,
                objetivo="dolor_prospectos",
                metadata={"ncp_nombre": self.cfg.nombre, "ncp_lista": self.cfg.lista_url},
            ))

        log.info("NCP %s: %d candidatos", self.id, len(candidatos))
        return candidatos
