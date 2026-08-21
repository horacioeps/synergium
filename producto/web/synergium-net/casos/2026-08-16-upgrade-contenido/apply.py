#!/usr/bin/env python3
"""Publica el upgrade corto de synergium.net: EN en /, ES en /es/, SEO, GTranslate."""
from __future__ import annotations

import base64
import http.cookiejar
import json
import pathlib
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import zipfile

WP = "https://synergium.net/wp-json/wp/v2"
USER = "admin"
HERE = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path("/tmp/synergium-app-pass.txt").read_text().strip()
AUTH = "Basic " + base64.b64encode(f"{USER}:{APP}".encode()).decode()
VAULT_CREDS = pathlib.Path(
    "/Users/horacio/Library/Obsidian/Horacio/@/@Sistema/Credenciales/Enlaces repetitivos o típicos.md"
)
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


def vault_wp_password() -> str:
    text = VAULT_CREDS.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "Synergium.net" in line and "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                return parts[2]
    raise SystemExit("No se encontró la fila Synergium.net en la nota de credenciales")


def cookie_opener():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar),
        urllib.request.HTTPSHandler(context=CTX),
    )
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    opener.open("https://synergium.net/wp-login.php", timeout=45)
    payload = urllib.parse.urlencode({
        "log": USER,
        "pwd": vault_wp_password(),
        "wp-submit": "Log In",
        "redirect_to": "https://synergium.net/wp-admin/",
        "testcookie": "1",
    }).encode()
    req_login = urllib.request.Request(
        "https://synergium.net/wp-login.php",
        data=payload,
        method="POST",
    )
    try:
        opener.open(req_login, timeout=45)
    except urllib.error.HTTPError:
        pass
    return opener


def make_seo_zip() -> pathlib.Path:
    zpath = HERE / "synergium-seo.zip"
    php = HERE / "plugin" / "synergium-seo.php"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(php, "synergium-seo/synergium-seo.php")
    return zpath


def upload_seo_plugin(opener) -> None:
    html = opener.open(
        "https://synergium.net/wp-admin/plugin-install.php?tab=upload",
        timeout=45,
    ).read().decode("utf-8", errors="replace")
    nonce = re.search(r'name="_wpnonce"\s+value="([^"]+)"', html)
    if not nonce:
        print("SEO plugin: no nonce en plugin-install upload")
        return
    boundary = "----SynBoundary7"
    zip_bytes = make_seo_zip().read_bytes()
    body = b""
    fields = {
        "_wpnonce": nonce.group(1),
        "_wp_http_referer": "/wp-admin/plugin-install.php?tab=upload",
        "install-plugin-submit": "Install Now",
    }
    for k, v in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="pluginzip"; filename="synergium-seo.zip"\r\n'
    body += b"Content-Type: application/zip\r\n\r\n"
    body += zip_bytes + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    up = urllib.request.Request(
        "https://synergium.net/wp-admin/update.php?action=upload-plugin",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        resp = opener.open(up, timeout=90)
        print("SEO plugin upload", resp.status, resp.geturl())
    except urllib.error.HTTPError as e:
        print("SEO plugin upload HTTP", e.code, e.geturl())
    st, body = req("POST", f"{WP}/plugins/synergium-seo/synergium-seo", {"status": "active"})
    print("SEO plugin activate", st, body.get("status") if isinstance(body, dict) else str(body)[:200])


def main() -> None:
    if not APP:
        raise SystemExit("Falta Application Password en /tmp/synergium-app-pass.txt")

    en_html = (HERE / "page-en.html").read_text(encoding="utf-8")
    es_html = (HERE / "page-es.html").read_text(encoding="utf-8")
    header = (HERE / "header.html").read_text(encoding="utf-8")

    st, settings = req("POST", f"{WP.replace('/wp/v2', '/wp/v2')}/settings", {
        "title": "Synergium",
        "description": "International research collaborations",
        "url": "https://synergium.net",
    })
    print("settings", st, settings.get("url") if isinstance(settings, dict) else settings)

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

    st, hdr = req("POST", f"{WP}/template-parts/twentytwentyfive//header", {
        "slug": "header",
        "theme": "twentytwentyfive",
        "area": "header",
        "content": header,
        "status": "publish",
    })
    print("header", st, hdr.get("wp_id") if isinstance(hdr, dict) else hdr)

    st, media = req("POST", f"{WP}/media/63", {
        "alt_text": "Synergium icon",
        "title": "Synergium icon",
    })
    print("media 63 alt", st, media.get("alt_text") if isinstance(media, dict) else media)
    st, media = req("POST", f"{WP}/media/59", {
        "alt_text": "Synergium",
        "title": "Synergium Open Graph",
    })
    print("media 59 alt", st, media.get("alt_text") if isinstance(media, dict) else media)

    st, plug = req("POST", f"{WP}/plugins", {"slug": "gtranslate", "status": "active"})
    print("gtranslate", st, plug.get("plugin") if isinstance(plug, dict) else str(plug)[:240])

    try:
        opener = cookie_opener()
        upload_seo_plugin(opener)
    except Exception as e:
        print("SEO plugin cookie path failed:", type(e).__name__)


if __name__ == "__main__":
    main()
