#!/usr/bin/env python3
"""Publica página EN, cabecera con selector ES/EN y toggle claro/oscuro en synergium.net."""
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
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()


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
            body = json.loads(resp.read().decode())
            return resp.status, body
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print("HTTP", e.code, url, err[:500])
        return e.code, err


def main():
    es_html = (HERE / "page-es.html").read_text()
    en_html = (HERE / "page-en.html").read_text()
    header = (HERE / "header.html").read_text()

    st, page_es = req("POST", f"{WP}/pages/35", {
        "content": es_html,
        "title": "Synergium",
    })
    print("update ES page 35:", st, page_es.get("modified") if isinstance(page_es, dict) else page_es)

    st, pages = req("GET", f"{WP}/pages?slug=en&per_page=5")
    en_id = None
    if isinstance(pages, list) and pages:
        en_id = pages[0]["id"]
        print("existing EN page", en_id)
        st, page_en = req("POST", f"{WP}/pages/{en_id}", {
            "title": "Synergium",
            "slug": "en",
            "status": "publish",
            "content": en_html,
        })
    else:
        st, page_en = req("POST", f"{WP}/pages", {
            "title": "Synergium",
            "slug": "en",
            "status": "publish",
            "content": en_html,
        })
    print("EN page:", st, page_en.get("id") if isinstance(page_en, dict) else page_en,
          page_en.get("link") if isinstance(page_en, dict) else "")

    st, hdr = req("POST", f"{WP}/template-parts/twentytwentyfive//header", {
        "slug": "header",
        "theme": "twentytwentyfive",
        "area": "header",
        "content": header,
        "status": "publish",
    })
    print("header template-part:", st, hdr.get("id") if isinstance(hdr, dict) else hdr,
          hdr.get("wp_id") if isinstance(hdr, dict) else "")

    st, nav = req("POST", f"{WP}/navigation/27", {
        "content": "<!-- wp:paragraph --><p></p><!-- /wp:paragraph -->",
    })
    print("nav 27 cleared (switcher is in header):", st)


if __name__ == "__main__":
    if not APP:
        raise SystemExit("Falta Application Password en /tmp/synergium-app-pass.txt")
    main()
