#!/usr/bin/env python3
"""Restaura synergium.net al estado previo a SKUs + Partner Snapshot.

Uso:
  python3 generado/web-synergium/casos/2026-08-17-skus-restantes/rollback.py

Requiere Application Password en /tmp/synergium-app-pass.txt
y los JSON en generado/web-synergium/wp-backups/pre-skus-2026-08-17/

DRY_RUN=1 python3 .../rollback.py  # solo muestra qué restauraría
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import urllib.error
import urllib.request

WP = "https://synergium.net/wp-json/wp/v2"
USER = "admin"
APP = pathlib.Path("/tmp/synergium-app-pass.txt").read_text().strip()
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()
BACK = pathlib.Path(__file__).resolve().parents[3] / "backups" / "pre-skus-2026-08-17"
DRY = os.environ.get("DRY_RUN", "0") not in ("", "0", "false", "False")


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
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print("HTTP", e.code, url, err[:500])
        return e.code, err


def load(name: str) -> dict:
    return json.loads((BACK / name).read_text(encoding="utf-8"))


def main() -> None:
    if not APP:
        raise SystemExit("Falta Application Password en /tmp/synergium-app-pass.txt")
    if not (BACK / "page-35.json").exists():
        raise SystemExit(f"No hay backups en {BACK}")

    page35 = load("page-35.json")
    page53 = load("page-53.json")

    jobs = [
        (f"{WP}/pages/35", {
            "title": page35["title"]["raw"],
            "content": page35["content"]["raw"],
            "excerpt": page35.get("excerpt", {}).get("raw", ""),
            "template": page35.get("template", "page-no-title"),
            "status": page35.get("status", "publish"),
        }),
        (f"{WP}/pages/53", {
            "title": page53["title"]["raw"],
            "content": page53["content"]["raw"],
            "excerpt": page53.get("excerpt", {}).get("raw", ""),
            "template": page53.get("template", "page-no-title"),
            "status": page53.get("status", "publish"),
        }),
    ]

    for url, payload in jobs:
        print(("DRY " if DRY else "POST ") + url)
        if DRY:
            continue
        st, body = req("POST", url, payload)
        extra = body.get("modified") if isinstance(body, dict) else str(body)[:160]
        print(" ", st, extra)


if __name__ == "__main__":
    main()
