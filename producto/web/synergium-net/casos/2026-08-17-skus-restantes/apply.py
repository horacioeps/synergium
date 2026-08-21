#!/usr/bin/env python3
"""Publica SKUs + Partner Snapshot en synergium.net (EN / y ES /es/).

Solo toca páginas 35 y 53. No toca cabecera, plugins ni settings.
Hace backup REST antes de escribir.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import pathlib
import ssl
import urllib.error
import urllib.request

WP = "https://synergium.net/wp-json/wp/v2"
USER = "admin"
HERE = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path("/tmp/synergium-app-pass.txt").read_text().strip()
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()
BACK = HERE.parents[2] / "backups" / "pre-skus-2026-08-17"
CTX = ssl.create_default_context()


def req(method: str, url: str, payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": AUTH,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=90, context=CTX) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print("HTTP", e.code, url, err[:500])
        return e.code, err


def backup_page(pid: int) -> None:
    BACK.mkdir(parents=True, exist_ok=True)
    st, body = req("GET", f"{WP}/pages/{pid}?context=edit")
    if st != 200 or not isinstance(body, dict):
        raise SystemExit(f"No se pudo respaldar página {pid}: {st}")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (BACK / f"page-{pid}.json").write_text(
        json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (BACK / f"{stamp}-page-{pid}.json").write_text(
        json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("backup", pid, body.get("link"), "content_len", len(body.get("content", {}).get("raw", "")))


def main() -> None:
    if not APP:
        raise SystemExit("Falta Application Password en /tmp/synergium-app-pass.txt")

    backup_page(35)
    backup_page(53)

    en_html = (HERE / "page-en.html").read_text(encoding="utf-8")
    es_html = (HERE / "page-es.html").read_text(encoding="utf-8")

    st, page_en = req("POST", f"{WP}/pages/35", {
        "title": "Synergium",
        "content": en_html,
        "excerpt": "We identify international collaborators, contact them and arrange first meetings.",
        "template": "page-no-title",
        "status": "publish",
    })
    print("page 35 EN /", st, page_en.get("link") if isinstance(page_en, dict) else page_en)

    st, page_es = req("POST", f"{WP}/pages/53", {
        "title": "Synergium",
        "slug": "es",
        "content": es_html,
        "excerpt": "Identificamos colaboradores internacionales, los contactamos y organizamos las primeras reuniones.",
        "template": "page-no-title",
        "status": "publish",
    })
    print("page 53 ES /es/", st, page_es.get("link") if isinstance(page_es, dict) else page_es)


if __name__ == "__main__":
    main()
