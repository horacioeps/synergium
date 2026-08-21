from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from .config import cache_dir, load_sources

log = logging.getLogger(__name__)

_robots_cache: dict[str, RobotFileParser | None] = {}
_last_hit: dict[str, float] = {}


@dataclass
class FetchResult:
    url: str
    status: int
    html: str | None
    from_cache: bool
    error: str | None = None


def _url_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _cache_path(url: str) -> Path:
    return cache_dir() / "html" / f"{_url_key(url)}.json"


def _load_cached(url: str) -> FetchResult | None:
    p = _cache_path(url)
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return FetchResult(url=d["url"], status=d["status"], html=d.get("html"),
                           from_cache=True, error=d.get("error"))
    except Exception:
        return None


def _save_cache(res: FetchResult) -> None:
    p = _cache_path(res.url)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({
        "url": res.url, "status": res.status, "html": res.html, "error": res.error,
    }, ensure_ascii=False), encoding="utf-8")


def _robots_ok(url: str, user_agent: str) -> bool:
    parts = urlparse(url)
    base = f"{parts.scheme}://{parts.netloc}"
    rp = _robots_cache.get(base)
    if rp is None and base not in _robots_cache:
        rp = RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None
        _robots_cache[base] = rp
    if rp is None:
        return True
    try:
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def _rate_limit(url: str, min_delay: float) -> None:
    host = urlparse(url).netloc
    now = time.monotonic()
    last = _last_hit.get(host, 0.0)
    wait = (last + min_delay) - now
    if wait > 0:
        time.sleep(wait)
    _last_hit[host] = time.monotonic()


def fetch(url: str, *, use_cache: bool = True) -> FetchResult:
    if use_cache:
        cached = _load_cached(url)
        if cached is not None:
            return cached

    cfg = load_sources()
    ua = cfg.limites.user_agent
    timeout = cfg.limites.timeout_http_seg
    min_delay = cfg.limites.rate_limit_por_dominio_seg

    if not _robots_ok(url, ua):
        res = FetchResult(url=url, status=0, html=None, from_cache=False,
                          error="bloqueado por robots.txt")
        _save_cache(res)
        return res

    _rate_limit(url, min_delay)
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True,
                          headers={"User-Agent": ua}) as client:
            r = client.get(url)
            res = FetchResult(url=str(r.url), status=r.status_code,
                              html=r.text if r.status_code == 200 else None,
                              from_cache=False,
                              error=None if r.status_code == 200 else f"http {r.status_code}")
    except Exception as e:
        res = FetchResult(url=url, status=0, html=None, from_cache=False, error=str(e))

    _save_cache(res)
    return res
