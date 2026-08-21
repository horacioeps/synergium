#!/usr/bin/env python3
"""Sube icono + OG, fija site_icon y republica cabecera/páginas."""
from __future__ import annotations

import base64
import json
import mimetypes
import pathlib
import urllib.error
import urllib.request

WP = "https://synergium.net/wp-json/wp/v2"
USER = "admin"
APP = pathlib.Path("/tmp/synergium-app-pass.txt").read_text().strip()
HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()


def request(method: str, url: str, data: bytes | None = None, headers: dict | None = None):
    h = {
        "Authorization": AUTH,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print("HTTP", e.code, url, err[:400])
        return e.code, err


def upload(path: pathlib.Path, title: str) -> dict:
    raw = path.read_bytes()
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    st, body = request(
        "POST",
        f"{WP}/media",
        data=raw,
        headers={
            "Content-Type": mime,
            "Content-Disposition": f'attachment; filename="{path.name}"',
        },
    )
    if st not in (200, 201) or not isinstance(body, dict):
        raise SystemExit(f"upload failed {path.name}: {st} {body}")
    # set title
    request("POST", f"{WP}/media/{body['id']}", data=json.dumps({"title": title, "alt_text": title}).encode(), headers={"Content-Type": "application/json"})
    print("uploaded", path.name, "id", body["id"], body.get("source_url"))
    return body


def main():
    icon = upload(ASSETS / "synergium-icon-512.png", "Synergium icon")
    og = upload(ASSETS / "synergium-og-1200x630.png", "Synergium Open Graph")
    og_url = og["source_url"]

    st, settings = request("POST", f"{WP}/settings", data=json.dumps({"site_icon": icon["id"]}).encode(), headers={"Content-Type": "application/json"})
    print("site_icon", st, settings.get("site_icon") if isinstance(settings, dict) else settings)

    header = (HERE / "header.html").read_text()
    st, hdr = request("POST", f"{WP}/template-parts/twentytwentyfive//header", data=json.dumps({
        "slug": "header",
        "theme": "twentytwentyfive",
        "area": "header",
        "content": header,
        "status": "publish",
    }).encode(), headers={"Content-Type": "application/json"})
    print("header", st, hdr.get("modified") if isinstance(hdr, dict) else hdr)

    for page_id, fname in ((35, "page-es.html"), (53, "page-en.html")):
        html = (HERE / fname).read_text().replace("OG_IMAGE_URL", og_url)
        st, page = request("POST", f"{WP}/pages/{page_id}", data=json.dumps({"content": html}).encode(), headers={"Content-Type": "application/json"})
        print("page", page_id, st, page.get("link") if isinstance(page, dict) else page)

    (HERE / "published-urls.json").write_text(json.dumps({
        "icon_id": icon["id"],
        "icon_url": icon.get("source_url"),
        "og_id": og["id"],
        "og_url": og_url,
    }, indent=2) + "\n")


if __name__ == "__main__":
    if not APP:
        raise SystemExit("Falta /tmp/synergium-app-pass.txt")
    main()
