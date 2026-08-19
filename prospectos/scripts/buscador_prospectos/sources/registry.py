from __future__ import annotations

from ..config import Cordis, NcpHorizon, Sources, WebGenerica
from .base import Source
from .cordis import CordisConfig, CordisSource
from .ncp_horizon import NcpHorizonSource
from .web_generica import WebGenericaSource


def build_sources(cfg: Sources, *, solo_ids: list[str] | None = None) -> list[Source]:
    out: list[Source] = []
    for f in cfg.fuentes:
        if solo_ids and f.id not in solo_ids:
            continue
        if not f.activa and not solo_ids:
            continue
        if isinstance(f, WebGenerica):
            out.append(WebGenericaSource(f))
        elif isinstance(f, NcpHorizon):
            out.append(NcpHorizonSource(f))
        elif isinstance(f, Cordis):
            out.append(CordisSource(CordisConfig.model_validate(f.model_dump())))
    return out
