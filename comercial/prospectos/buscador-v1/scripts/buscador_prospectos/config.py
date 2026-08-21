from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

PKG_DIR = Path(__file__).resolve().parent
REPO_DIR = PKG_DIR.parent.parent
CONFIG_DIR = PKG_DIR / "config"
OUTPUT_DIR = REPO_DIR / "generado" / "buscador-prospectos"
CACHE_DIR = OUTPUT_DIR / "cache"
CASOS_DIR = OUTPUT_DIR / "casos"

load_dotenv(REPO_DIR / ".env")


class Terms(BaseModel):
    paises: list[str]
    objetivos: dict[str, dict[str, list[str]]]
    ajustes_pais: dict[str, dict[str, str]] = Field(default_factory=dict)


class WebGenerica(BaseModel):
    id: str
    tipo: Literal["web_generica"]
    activa: bool
    proveedor_busqueda: Literal["brave"]
    idioma: str
    objetivo: str
    max_resultados_por_termino: int = 10
    freshness: str | None = None   # Brave: 'pd' dia, 'pw' semana, 'pm' mes, 'py' ano


class NcpHorizon(BaseModel):
    id: str
    tipo: Literal["ncp_horizon"]
    activa: bool
    pais: str
    nombre: str
    lista_url: str


class Cordis(BaseModel):
    id: str
    tipo: Literal["cordis"]
    activa: bool
    meses_atras: int = 6
    max_resultados: int = 50


Fuente = WebGenerica | NcpHorizon | Cordis


class Limites(BaseModel):
    rate_limit_por_dominio_seg: float = 2.0
    timeout_http_seg: int = 20
    user_agent: str = "BuscadorProspectosSynergium/0.1"


class Modelos(BaseModel):
    clasificar: str = "gpt-5-nano"
    redactar: str = "gpt-5-mini"


class Sources(BaseModel):
    fuentes: list[Fuente]
    limites: Limites = Field(default_factory=Limites)
    modelos: Modelos = Field(default_factory=Modelos)


def load_terms() -> Terms:
    with (CONFIG_DIR / "terms.yaml").open("r", encoding="utf-8") as f:
        return Terms.model_validate(yaml.safe_load(f))


def load_sources() -> Sources:
    with (CONFIG_DIR / "sources.yaml").open("r", encoding="utf-8") as f:
        return Sources.model_validate(yaml.safe_load(f))


def caso_dir(nombre: str) -> Path:
    d = CASOS_DIR / nombre
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_dir() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Falta variable de entorno {name}. Definir en .env")
    return v
