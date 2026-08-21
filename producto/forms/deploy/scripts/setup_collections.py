#!/usr/bin/env python3
"""Create PocketBase collections + SMTP settings for Synergium Forms."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("SYNERGIUM_FORMS_PB_URL", "http://127.0.0.1:8090").rstrip("/")
EMAIL = os.environ["SYNERGIUM_FORMS_PB_ADMIN_EMAIL"]
PASSWORD = os.environ["SYNERGIUM_FORMS_PB_ADMIN_PASSWORD"]


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
    # PocketBase >=0.23 superuser auth
    out = req(
        "POST",
        "/api/collections/_superusers/auth-with-password",
        {"identity": EMAIL, "password": PASSWORD},
    )
    return out["token"]


def ensure_collections(token: str) -> None:
    existing = req("GET", "/api/collections?perPage=200", token=token)
    names = {c["name"] for c in existing.get("items", [])}

    forms_schema = {
        "name": "forms",
        "type": "base",
        "fields": [
            {"name": "public_id", "type": "text", "required": True, "presentable": True},
            {"name": "title", "type": "text", "required": True},
            {"name": "description", "type": "text", "required": False},
            {"name": "locale", "type": "text", "required": False},
            {"name": "schema", "type": "json", "required": True},
            {
                "name": "status",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["draft", "open", "closed"],
            },
            {"name": "notify_email", "type": "email", "required": True},
            {"name": "success_message", "type": "text", "required": False},
        ],
        "indexes": [
            "CREATE UNIQUE INDEX idx_forms_public_id ON forms (public_id)",
        ],
        # Admin-only collection access; public reads go through /api/sf/form/{id}
        "listRule": None,
        "viewRule": None,
        "createRule": None,
        "updateRule": None,
        "deleteRule": None,
    }

    if "forms" not in names:
        forms = req("POST", "/api/collections", forms_schema, token=token)
        print("created forms", forms["id"])
        forms_id = forms["id"]
    else:
        forms = next(c for c in existing["items"] if c["name"] == "forms")
        forms_id = forms["id"]
        req(
            "PATCH",
            f"/api/collections/{forms_id}",
            {
                "listRule": None,
                "viewRule": None,
                "createRule": None,
                "updateRule": None,
                "deleteRule": None,
            },
            token=token,
        )
        print("forms exists", forms_id)

    submissions_schema = {
        "name": "submissions",
        "type": "base",
        "fields": [
            {
                "name": "form",
                "type": "relation",
                "required": True,
                "collectionId": forms_id,
                "maxSelect": 1,
                "cascadeDelete": True,
            },
            {"name": "answers", "type": "json", "required": True},
            {"name": "respondent_email", "type": "email", "required": False},
            {
                "name": "source",
                "type": "select",
                "required": False,
                "maxSelect": 1,
                "values": ["web", "google"],
            },
            {"name": "ip_hash", "type": "text", "required": False},
            {"name": "user_agent", "type": "text", "required": False},
        ],
        "listRule": None,
        "viewRule": None,
        "createRule": '@request.data.form.status = "open" || @request.data.form.status ?= "open"',
        "updateRule": None,
        "deleteRule": None,
    }

    # PocketBase relation createRule: allow create if related form is open.
    # Simpler reliable rule: anyone can create (spam mitigated by honeypot + obscure id).
    # We'll use: createRule = ""  meaning public create, and validate form id exists via hook optionally.
    submissions_schema["createRule"] = ""  # public create

    if "submissions" not in names:
        sub = req("POST", "/api/collections", submissions_schema, token=token)
        print("created submissions", sub["id"])
    else:
        sub = next(c for c in existing["items"] if c["name"] == "submissions")
        field_names = {f.get("name") for f in (sub.get("fields") or [])}
        patch = {
            "createRule": "",
            "listRule": None,
            "viewRule": None,
            "updateRule": None,
            "deleteRule": None,
        }
        if "source" not in field_names:
            # PocketBase expects full fields list when adding; merge existing + source.
            fields = list(sub.get("fields") or [])
            fields.append(
                {
                    "name": "source",
                    "type": "select",
                    "required": False,
                    "maxSelect": 1,
                    "values": ["web", "google"],
                }
            )
            patch["fields"] = fields
            print("adding source field to submissions")
        req("PATCH", f"/api/collections/{sub['id']}", patch, token=token)
        print("submissions exists", sub["id"])


def configure_smtp(token: str) -> None:
    host = os.environ.get("SYNERGIUM_FORMS_SMTP_HOST", "")
    if not host:
        print("skip SMTP (no SYNERGIUM_FORMS_SMTP_HOST)")
        return
    settings = req("GET", "/api/settings", token=token)
    settings["smtp"] = {
        "enabled": True,
        "host": host,
        "port": int(os.environ.get("SYNERGIUM_FORMS_SMTP_PORT", "587")),
        "username": os.environ.get("SYNERGIUM_FORMS_SMTP_USER", ""),
        "password": os.environ.get("SYNERGIUM_FORMS_SMTP_PASS", ""),
        "authMethod": "PLAIN",
        # Port 587 = STARTTLS (tls false). Port 465 = implicit TLS (tls true).
        "tls": os.environ.get("SYNERGIUM_FORMS_SMTP_TLS", "false").lower() in ("1", "true", "yes"),
        "localName": os.environ.get("SYNERGIUM_FORMS_SMTP_LOCALNAME", "forms.synergium.net"),
    }
    meta = settings.get("meta") or {}
    meta["senderName"] = os.environ.get("SYNERGIUM_FORMS_SENDER_NAME", "Synergium Forms")
    meta["senderAddress"] = os.environ.get(
        "SYNERGIUM_FORMS_SENDER_ADDRESS", "horacio@horacio-ps.com"
    )
    settings["meta"] = meta
    req("PATCH", "/api/settings", settings, token=token)
    print("smtp configured")


def main() -> None:
    token = auth()
    ensure_collections(token)
    configure_smtp(token)
    print("OK setup")


if __name__ == "__main__":
    main()
