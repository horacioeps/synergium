from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from openai import OpenAI

from .config import PKG_DIR, cache_dir, load_sources, require_env
from .sources.base import Candidato

log = logging.getLogger(__name__)

PROMPT_CLASIFICAR = (PKG_DIR / "prompts" / "clasificar.md").read_text(encoding="utf-8")
PROMPT_REDACTAR   = (PKG_DIR / "prompts" / "redactar.md").read_text(encoding="utf-8")

_client: OpenAI | None = None


def _client_or_init() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
    return _client


@dataclass
class Clasificacion:
    es_dolor_real: bool
    tipo_actor: str
    tema: str
    pais_inferido: str
    relevancia: int
    motivo: str
    es_competidor: bool

    @classmethod
    def from_json(cls, data: dict) -> "Clasificacion":
        return cls(
            es_dolor_real=bool(data.get("es_dolor_real", False)),
            tipo_actor=str(data.get("tipo_actor", "otro")),
            tema=str(data.get("tema", "")),
            pais_inferido=str(data.get("pais_inferido", "desconocido")),
            relevancia=int(data.get("relevancia", 1) or 1),
            motivo=str(data.get("motivo", "")),
            es_competidor=bool(data.get("es_competidor", False)),
        )


def _cache_path(prefix: str, key: str) -> Path:
    d = cache_dir() / "llm"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{prefix}-{key}.json"


def _hash(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:24]


def _input_payload(c: Candidato, texto_extraido: str | None) -> str:
    extracto = (texto_extraido or c.extracto or "").strip()[:2000]
    return json.dumps({
        "url": c.url,
        "titulo": c.titulo,
        "extracto": extracto,
        "pais_fuente": c.pais,
        "idioma_fuente": c.idioma,
        "fecha_publicacion": c.fecha_publicacion,
        "fecha_hoy": date.today().isoformat(),
    }, ensure_ascii=False)


def clasificar(c: Candidato, texto_extraido: str | None = None) -> Clasificacion | None:
    cfg = load_sources()
    modelo = cfg.modelos.clasificar
    payload = _input_payload(c, texto_extraido)
    key = _hash(modelo, "clasificar-v7-cordis-outreach", payload)
    cp = _cache_path("clasificar", key)
    if cp.exists():
        try:
            return Clasificacion.from_json(json.loads(cp.read_text(encoding="utf-8")))
        except Exception:
            pass

    try:
        resp = _client_or_init().chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": PROMPT_CLASIFICAR},
                {"role": "user", "content": payload},
            ],
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        data = json.loads(raw)
        cp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return Clasificacion.from_json(data)
    except Exception as e:
        log.warning("Error clasificando %s con %s: %s", c.url, modelo, e)
        return None


def redactar_mensaje(c: Candidato, clf: Clasificacion, texto_extraido: str | None = None) -> str | None:
    if clf.relevancia < 3 or clf.es_competidor:
        return None
    cfg = load_sources()
    modelo = cfg.modelos.redactar
    payload = json.dumps({
        "url": c.url,
        "titulo": c.titulo,
        "extracto": (texto_extraido or c.extracto or "")[:1500],
        "pais": clf.pais_inferido,
        "tipo_actor": clf.tipo_actor,
        "tema": clf.tema,
        "idioma_fuente": c.idioma,
    }, ensure_ascii=False)
    key = _hash(modelo, "redactar-v1", payload)
    cp = _cache_path("redactar", key)
    if cp.exists():
        return cp.read_text(encoding="utf-8") or None
    try:
        resp = _client_or_init().chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": PROMPT_REDACTAR},
                {"role": "user", "content": payload},
            ],
        )
        msg = (resp.choices[0].message.content or "").strip()
        if msg == "NO_REDACTAR":
            return None
        cp.write_text(msg, encoding="utf-8")
        return msg or None
    except Exception as e:
        log.warning("Error redactando para %s: %s", c.url, e)
        return None
