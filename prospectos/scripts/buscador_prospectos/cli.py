from __future__ import annotations

import json
import logging
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer

from .analyze import clasificar, redactar_mensaje
from .config import caso_dir, load_sources
from .extract import extract
from .fetch import fetch
from .sources._filtros import aplicar_prefiltros
from .sources.base import Candidato
from .sources.registry import build_sources
from .tracking import (cargar_csv, guardar, merge_incremental, registro_de)

app = typer.Typer(add_completion=False, no_args_is_help=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("buscador_prospectos")


def _candidatos_path(caso: str) -> Path:
    return caso_dir(caso) / "candidatos.jsonl"


def _csv_path(caso: str) -> Path:
    return caso_dir(caso) / "tracking.csv"


def _md_path(caso: str) -> Path:
    return caso_dir(caso) / "tracking.md"


def _xlsx_path(caso: str) -> Path:
    return caso_dir(caso) / "tracking.xlsx"


def _log_path(caso: str) -> Path:
    d = caso_dir(caso) / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"run-{date.today().isoformat()}.log"


def _save_candidatos(caso: str, candidatos: list[Candidato]) -> None:
    p = _candidatos_path(caso)
    with p.open("w", encoding="utf-8") as f:
        for c in candidatos:
            d = {
                "url": c.url, "titulo": c.titulo, "extracto": c.extracto,
                "fuente_id": c.fuente_id, "plataforma": c.plataforma,
                "autor": c.autor, "pais": c.pais, "idioma": c.idioma,
                "objetivo": c.objetivo, "termino_origen": c.termino_origen,
                "fecha_deteccion": c.fecha_deteccion.isoformat(),
                "fecha_publicacion": c.fecha_publicacion,
                "metadata": c.metadata,
            }
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    log.info("Guardados %d candidatos en %s", len(candidatos), p)


def _load_candidatos(caso: str) -> list[Candidato]:
    p = _candidatos_path(caso)
    if not p.exists():
        return []
    out: list[Candidato] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        out.append(Candidato(
            url=d["url"], titulo=d.get("titulo"), extracto=d.get("extracto"),
            fuente_id=d.get("fuente_id", ""), plataforma=d.get("plataforma", ""),
            autor=d.get("autor"), pais=d.get("pais"), idioma=d.get("idioma"),
            objetivo=d.get("objetivo"), termino_origen=d.get("termino_origen"),
            fecha_deteccion=date.fromisoformat(d["fecha_deteccion"]),
            fecha_publicacion=d.get("fecha_publicacion"),
            metadata=d.get("metadata", {}) or {},
        ))
    return out


@app.command()
def discover(
    caso: str = typer.Option("v1-web-ncps", help="nombre del caso bajo generado/buscador-prospectos/casos/"),
    solo: Optional[str] = typer.Option(None, help="ids de fuentes separados por coma; si no, todas las activas"),
    limite: Optional[int] = typer.Option(None, help="cortar a N candidatos por fuente (debug)"),
) -> None:
    """Descubrir URLs candidatas vias todas las fuentes activas."""
    cfg = load_sources()
    ids = [s.strip() for s in solo.split(",")] if solo else None
    fuentes = build_sources(cfg, solo_ids=ids)
    if not fuentes:
        typer.echo("No hay fuentes que ejecutar.")
        raise typer.Exit(code=1)
    todos: list[Candidato] = []
    for s in fuentes:
        log.info("Discover %s (%s)", s.id, s.tipo)
        cands = s.discover()
        if limite:
            cands = cands[:limite]
        todos.extend(cands)
        log.info("  -> %d candidatos", len(cands))
    filtrados, stats = aplicar_prefiltros(todos)
    log.info("Prefiltros: descartados off_domain=%d, antiguos=%d. Supervivientes=%d/%d",
             stats["off_domain"], stats["antiguo"], stats["supervivientes"], len(todos))
    _save_candidatos(caso, filtrados)
    typer.echo(f"OK. {len(filtrados)} candidatos tras prefiltros "
               f"(off_domain={stats['off_domain']}, antiguos={stats['antiguo']}, "
               f"de {len(todos)} brutos). {_candidatos_path(caso)}")


@app.command()
def analyze(
    caso: str = typer.Option("v1-web-ncps"),
    enriquecer: bool = typer.Option(False, help="si true, hace fetch+extract de cada candidato antes de clasificar"),
    limite: Optional[int] = typer.Option(None, help="analizar solo los primeros N (debug)"),
) -> None:
    """Clasificar candidatos con LLM y producir tracking.csv/md."""
    cands = _load_candidatos(caso)
    if not cands:
        typer.echo("No hay candidatos. Ejecuta discover primero.")
        raise typer.Exit(code=1)
    if limite:
        cands = cands[:limite]

    registros = []
    for i, c in enumerate(cands, 1):
        texto = None
        if enriquecer:
            res = fetch(c.url)
            if res.html:
                texto = extract(res.html, c.url).text
        clf = clasificar(c, texto)
        if clf is None:
            log.warning("Sin clasificacion para %s; salto", c.url)
            continue
        msg = redactar_mensaje(c, clf, texto)
        registros.append(registro_de(c, clf, msg))
        if i % 10 == 0:
            log.info("  procesados %d/%d", i, len(cands))

    df, anadidos = merge_incremental(_csv_path(caso), registros)
    guardar(df, _csv_path(caso), _md_path(caso), _xlsx_path(caso))
    typer.echo(f"OK. {anadidos} nuevos / {len(df)} totales. {_csv_path(caso)}")


@app.command()
def run(
    caso: str = typer.Option("v1-web-ncps"),
    solo: Optional[str] = typer.Option(None),
    enriquecer: bool = typer.Option(False),
    limite: Optional[int] = typer.Option(None),
) -> None:
    """discover + analyze en una sola orden."""
    discover(caso=caso, solo=solo, limite=limite)
    analyze(caso=caso, enriquecer=enriquecer, limite=limite)


@app.command()
def report(caso: str = typer.Option("v1-web-ncps")) -> None:
    """Regenerar tracking.md y tracking.xlsx desde tracking.csv (sin tocar LLM)."""
    df = cargar_csv(_csv_path(caso))
    guardar(df, _csv_path(caso), _md_path(caso), _xlsx_path(caso))
    typer.echo(f"OK. {_md_path(caso)} + {_xlsx_path(caso)}")


if __name__ == "__main__":
    app()
