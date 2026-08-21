#!/usr/bin/env python3
"""Publish / update / close Synergium Forms via PocketBase API (agent-operated)."""
from __future__ import annotations

import argparse
import json
import os
import secrets
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = os.environ.get("SYNERGIUM_FORMS_PB_URL", "https://forms.synergium.net").rstrip("/")
EMAIL = os.environ.get("SYNERGIUM_FORMS_PB_ADMIN_EMAIL", "")
PASSWORD = os.environ.get("SYNERGIUM_FORMS_PB_ADMIN_PASSWORD", "")
DEFAULT_NOTIFY = os.environ.get("SYNERGIUM_FORMS_NOTIFY_EMAIL", "horacio@horacio-ps.com")


def req(method: str, path: str, body=None, token: str | None = None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = token
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as res:
            raw = res.read().decode() or "{}"
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise SystemExit(f"{method} {path} -> {e.code}: {err}") from e


def auth() -> str:
    if not EMAIL or not PASSWORD:
        raise SystemExit("Set SYNERGIUM_FORMS_PB_ADMIN_EMAIL and SYNERGIUM_FORMS_PB_ADMIN_PASSWORD")
    out = req(
        "POST",
        "/api/collections/_superusers/auth-with-password",
        {"identity": EMAIL, "password": PASSWORD},
    )
    return out["token"]


def nanoid(n: int = 14) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_by_public_id(token: str, public_id: str) -> dict | None:
    filt = urllib.parse.quote(f'public_id="{public_id}"')
    out = req("GET", f"/api/collections/forms/records?filter={filt}&perPage=1", token=token)
    items = out.get("items") or []
    return items[0] if items else None


def cmd_publish(args: argparse.Namespace) -> None:
    token = auth()
    schema = load_schema(Path(args.schema))
    public_id = args.public_id or nanoid()
    title = args.title or schema.get("title") or "Untitled form"
    description = args.description if args.description is not None else schema.get("description", "")
    locale = args.locale or schema.get("locale") or "en"
    notify = args.notify_email or DEFAULT_NOTIFY
    success = args.success_message or schema.get("success_message") or "Thanks. Your answers were saved."
    status = args.status or "open"

    existing = find_by_public_id(token, public_id) if args.public_id else None
    payload = {
        "public_id": public_id if not existing else existing["public_id"],
        "title": title,
        "description": description,
        "locale": locale,
        "schema": schema,
        "status": status,
        "notify_email": notify,
        "success_message": success,
    }
    if existing:
        rec = req("PATCH", f"/api/collections/forms/records/{existing['id']}", payload, token=token)
        action = "updated"
    else:
        if not args.public_id:
            payload["public_id"] = public_id
        rec = req("POST", "/api/collections/forms/records", payload, token=token)
        action = "created"

    url = f"{BASE}/{rec['public_id']}"
    print(json.dumps({"action": action, "id": rec["id"], "public_id": rec["public_id"], "url": url, "status": rec["status"]}, indent=2))


def cmd_close(args: argparse.Namespace) -> None:
    token = auth()
    rec = find_by_public_id(token, args.public_id)
    if not rec:
        raise SystemExit(f"form not found: {args.public_id}")
    out = req(
        "PATCH",
        f"/api/collections/forms/records/{rec['id']}",
        {"status": "closed"},
        token=token,
    )
    print(json.dumps({"action": "closed", "public_id": out["public_id"], "status": out["status"]}, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    token = auth()
    out = req("GET", "/api/collections/forms/records?perPage=100&sort=-created", token=token)
    rows = [
        {
            "public_id": i["public_id"],
            "title": i["title"],
            "status": i["status"],
            "locale": i.get("locale"),
            "url": f"{BASE}/{i['public_id']}",
        }
        for i in out.get("items") or []
    ]
    print(json.dumps(rows, indent=2))


def cmd_export(args: argparse.Namespace) -> None:
    import csv

    token = auth()
    form = find_by_public_id(token, args.public_id)
    if not form:
        raise SystemExit(f"form not found: {args.public_id}")
    filt = urllib.parse.quote(f'form="{form["id"]}"')
    out = req(
        "GET",
        f"/api/collections/submissions/records?filter={filt}&perPage=500&sort=created",
        token=token,
    )
    items = out.get("items") or []
    field_ids = []
    schema = form.get("schema") or {}
    if isinstance(schema, str):
        schema = json.loads(schema)
    for f in schema.get("fields") or []:
        if f.get("type") != "section":
            field_ids.append(f["id"])

    path = Path(args.out)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["submission_id", "created"] + field_ids)
        for it in items:
            answers = it.get("answers") or {}
            row = [it["id"], it.get("created", "")]
            for fid in field_ids:
                v = answers.get(fid, "")
                if isinstance(v, (dict, list)):
                    v = json.dumps(v, ensure_ascii=False)
                row.append(v)
            w.writerow(row)
    print(json.dumps({"exported": len(items), "out": str(path)}, indent=2))


def cmd_rename(args: argparse.Namespace) -> None:
    """Rename forms.public_id (URL slug). Keeps same record + submissions."""
    token = auth()
    rec = find_by_public_id(token, args.from_id)
    if not rec:
        raise SystemExit(f"form not found: {args.from_id}")
    clash = find_by_public_id(token, args.to_id)
    if clash and clash["id"] != rec["id"]:
        raise SystemExit(f"target public_id already in use: {args.to_id}")
    out = req(
        "PATCH",
        f"/api/collections/forms/records/{rec['id']}",
        {"public_id": args.to_id},
        token=token,
    )
    url = f"{BASE}/{out['public_id']}"
    print(
        json.dumps(
            {
                "action": "renamed",
                "id": out["id"],
                "from": args.from_id,
                "public_id": out["public_id"],
                "url": url,
                "status": out["status"],
            },
            indent=2,
        )
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Synergium Forms agent CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    pub = sub.add_parser("publish", help="Create or update a form and open it")
    pub.add_argument("--schema", required=True, help="Path to schema JSON")
    pub.add_argument("--public-id", default=None)
    pub.add_argument("--title", default=None)
    pub.add_argument("--description", default=None)
    pub.add_argument("--locale", default=None)
    pub.add_argument("--notify-email", default=None)
    pub.add_argument("--success-message", default=None)
    pub.add_argument("--status", default="open", choices=["draft", "open", "closed"])
    pub.set_defaults(func=cmd_publish)

    cl = sub.add_parser("close", help="Close a form by public_id")
    cl.add_argument("--public-id", required=True)
    cl.set_defaults(func=cmd_close)

    ls = sub.add_parser("list", help="List forms")
    ls.set_defaults(func=cmd_list)

    ex = sub.add_parser("export", help="Export submissions CSV")
    ex.add_argument("--public-id", required=True)
    ex.add_argument("--out", required=True)
    ex.set_defaults(func=cmd_export)

    rn = sub.add_parser("rename", help="Change public_id (URL slug) of an existing form")
    rn.add_argument("--from", dest="from_id", required=True)
    rn.add_argument("--to", dest="to_id", required=True)
    rn.set_defaults(func=cmd_rename)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
