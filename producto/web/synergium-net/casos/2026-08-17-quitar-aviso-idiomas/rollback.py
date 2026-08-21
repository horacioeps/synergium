#!/usr/bin/env python3
"""Restaura footer y header previos a quitar el aviso de idiomas."""
from __future__ import annotations

import base64
import json
import pathlib
import ssl
import urllib.error
import urllib.request

WP = "https://synergium.net/wp-json/wp/v2"
USER = "admin"
APP = pathlib.Path("/tmp/synergium-app-pass.txt").read_text().strip()
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()
BAK = pathlib.Path(__file__).resolve().parents[3] / "backups" / "pre-footer-langs-2026-08-17"
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


def raw_of(name: str) -> str:
    data = json.loads((BAK / name).read_text(encoding="utf-8"))
    content = data["content"]
    return content["raw"] if isinstance(content, dict) else content


def main() -> None:
    if not APP:
        raise SystemExit("Falta Application Password en /tmp/synergium-app-pass.txt")

    st, ftr = req("POST", f"{WP}/template-parts/twentytwentyfive//footer", {
        "slug": "footer",
        "theme": "twentytwentyfive",
        "area": "footer",
        "content": raw_of("footer.json"),
        "status": "publish",
    })
    print("footer rollback", st, ftr.get("wp_id") if isinstance(ftr, dict) else ftr)

    st, hdr = req("POST", f"{WP}/template-parts/twentytwentyfive//header", {
        "slug": "header",
        "theme": "twentytwentyfive",
        "area": "header",
        "content": raw_of("header.json"),
        "status": "publish",
    })
    print("header rollback", st, hdr.get("wp_id") if isinstance(hdr, dict) else hdr)


if __name__ == "__main__":
    main()
