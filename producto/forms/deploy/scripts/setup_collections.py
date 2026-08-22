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


ADMIN_ONLY = {
    "listRule": None,
    "viewRule": None,
    "createRule": None,
    "updateRule": None,
    "deleteRule": None,
}


def _collection_id(existing: dict, name: str) -> str:
    return next(c["id"] for c in existing["items"] if c["name"] == name)


def _collection_record(existing: dict, name: str) -> dict:
    return next(c for c in existing["items"] if c["name"] == name)


def merge_missing_fields(existing_fields: list, new_defs: list) -> list | None:
    names = {f.get("name") for f in existing_fields}
    to_add = [f for f in new_defs if f["name"] not in names]
    if not to_add:
        return None
    return list(existing_fields) + to_add


def patch_collection_fields(
    token: str, existing: dict, name: str, field_defs: list, extra_patch: dict | None = None
) -> None:
    coll = _collection_record(existing, name)
    coll_id = coll["id"]
    patch: dict = {**(extra_patch or ADMIN_ONLY)}
    merged = merge_missing_fields(coll.get("fields") or [], field_defs)
    if merged:
        patch["fields"] = merged
        print(f"adding fields to {name}: {[f['name'] for f in merged if f['name'] not in {x.get('name') for x in (coll.get('fields') or [])}]}")
    req("PATCH", f"/api/collections/{coll_id}", patch, token=token)
    print(f"{name} exists", coll_id)
    """Create ERP-like match pipeline collections. Returns name -> collection id."""
    existing = req("GET", "/api/collections?perPage=200", token=token)
    names = {c["name"] for c in existing.get("items", [])}
    ids: dict[str, str] = {}

    matches_schema = {
        "name": "matches",
        "type": "base",
        "fields": [
            {"name": "match_number", "type": "number", "required": True},
            {"name": "match_reference", "type": "text", "required": True, "presentable": True},
            {"name": "slug", "type": "text", "required": True},
            {"name": "axis", "type": "text", "required": False},
            {
                "name": "status",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["active", "discarded", "completed"],
            },
            {
                "name": "current_step",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": [
                    "curated",
                    "opt_in_sent",
                    "opt_in_partial",
                    "opt_in_complete",
                    "match_align_partial",
                    "match_align_complete",
                    "intro_done",
                    "closed",
                ],
            },
            {"name": "person_a_name", "type": "text", "required": False},
            {"name": "person_a_email", "type": "email", "required": False},
            {"name": "person_b_name", "type": "text", "required": False},
            {"name": "person_b_email", "type": "email", "required": False},
            {"name": "expediente_path", "type": "text", "required": False},
            {"name": "notes", "type": "text", "required": False},
            {"name": "discarded_reason", "type": "text", "required": False},
        ],
        "indexes": [
            "CREATE UNIQUE INDEX idx_matches_reference ON matches (match_reference)",
            "CREATE UNIQUE INDEX idx_matches_number ON matches (match_number)",
        ],
        **ADMIN_ONLY,
    }

    if "matches" not in names:
        out = req("POST", "/api/collections", matches_schema, token=token)
        print("created matches", out["id"])
        ids["matches"] = out["id"]
    else:
        mid = _collection_id(existing, "matches")
        req("PATCH", f"/api/collections/{mid}", {**ADMIN_ONLY}, token=token)
        print("matches exists", mid)
        ids["matches"] = mid

    participants_schema = {
        "name": "match_participants",
        "type": "base",
        "fields": [
            {
                "name": "match",
                "type": "relation",
                "required": True,
                "collectionId": ids["matches"],
                "maxSelect": 1,
                "cascadeDelete": True,
            },
            {
                "name": "submission",
                "type": "relation",
                "required": False,
                "collectionId": submissions_id,
                "maxSelect": 1,
            },
            {"name": "person_name", "type": "text", "required": False},
            {"name": "person_email", "type": "email", "required": True},
            {
                "name": "side",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["a", "b"],
            },
            {"name": "whatsapp", "type": "text", "required": False},
            {"name": "match_language", "type": "text", "required": False},
            {
                "name": "current_step",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": [
                    "directory",
                    "opt_in_pending",
                    "opt_in_yes",
                    "opt_in_no",
                    "match_align_pending",
                    "match_align_done",
                    "intro_done",
                ],
            },
        ],
        "indexes": [
            "CREATE UNIQUE INDEX idx_match_participants_email ON match_participants (match, person_email)",
        ],
        **ADMIN_ONLY,
    }

    if "match_participants" not in names:
        out = req("POST", "/api/collections", participants_schema, token=token)
        print("created match_participants", out["id"])
        ids["match_participants"] = out["id"]
    else:
        pid = _collection_id(existing, "match_participants")
        req("PATCH", f"/api/collections/{pid}", {**ADMIN_ONLY}, token=token)
        print("match_participants exists", pid)
        ids["match_participants"] = pid

    events_schema = {
        "name": "contact_events",
        "type": "base",
        "fields": [
            {
                "name": "match",
                "type": "relation",
                "required": False,
                "collectionId": ids["matches"],
                "maxSelect": 1,
                "cascadeDelete": True,
            },
            {
                "name": "participant",
                "type": "relation",
                "required": False,
                "collectionId": ids["match_participants"],
                "maxSelect": 1,
                "cascadeDelete": False,
            },
            {
                "name": "event_type",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["opt_in", "match_align", "intro", "follow_up", "inbound_reply", "note"],
            },
            {
                "name": "channel",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["email", "whatsapp", "other"],
            },
            {
                "name": "direction",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["outbound", "inbound"],
            },
            {
                "name": "status",
                "type": "select",
                "required": True,
                "maxSelect": 1,
                "values": ["draft", "sent", "failed", "received"],
            },
            {"name": "sent_at", "type": "date", "required": False},
            {"name": "from_email", "type": "email", "required": False},
            {"name": "to_email", "type": "email", "required": False},
            {"name": "person_email", "type": "email", "required": False},
            {"name": "match_reference", "type": "text", "required": False},
            {"name": "subject", "type": "text", "required": False},
            {"name": "body", "type": "text", "required": False},
            {"name": "notes", "type": "text", "required": False},
        ],
        "indexes": [
            "CREATE INDEX idx_contact_events_match_ref ON contact_events (match_reference)",
            "CREATE INDEX idx_contact_events_person ON contact_events (person_email)",
        ],
        **ADMIN_ONLY,
    }

    if "contact_events" not in names:
        out = req("POST", "/api/collections", events_schema, token=token)
        print("created contact_events", out["id"])
        ids["contact_events"] = out["id"]
    else:
        eid = _collection_id(existing, "contact_events")
        req("PATCH", f"/api/collections/{eid}", {**ADMIN_ONLY}, token=token)
        print("contact_events exists", eid)
        ids["contact_events"] = eid

    return ids


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
        submissions_id = sub["id"]
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
        submissions_id = sub["id"]

    ensure_match_tracking(token, submissions_id)


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
