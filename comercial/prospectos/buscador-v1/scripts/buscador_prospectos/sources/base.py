from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Candidato:
    """URL candidata descubierta por una fuente, antes de analisis."""
    url: str
    titulo: str | None = None
    extracto: str | None = None
    fuente_id: str = ""
    plataforma: str = ""           # 'web' / 'ncp'
    autor: str | None = None
    pais: str | None = None
    idioma: str | None = None
    objetivo: str | None = None    # 'dolor_prospectos' / 'competidores_aprender' / 'eventos'
    termino_origen: str | None = None
    fecha_deteccion: date = field(default_factory=date.today)
    fecha_publicacion: str | None = None   # ISO si se conoce; "YYYY" si solo se infiere ano de la URL
    metadata: dict = field(default_factory=dict)


class Source(ABC):
    """Interfaz comun para fuentes. discover() es lo unico requerido en v1."""

    id: str
    tipo: str
    activa: bool

    @abstractmethod
    def discover(self) -> list[Candidato]:
        ...
