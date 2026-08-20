#!/usr/bin/env python3
"""Import Google Sheet responses → PocketBase submissions (source=google).

Usage:
  set -a; source ~/.cursor/secrets.env; set +a
  python3 scripts/synergium_forms_sheet_sync.py --public-id nexus-input
  python3 scripts/synergium_forms_sheet_sync.py --public-id nexus-input --dry-run
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = os.environ.get("SYNERGIUM_FORMS_PB_URL", "https://forms.synergium.net").rstrip("/")
EMAIL = os.environ.get("SYNERGIUM_FORMS_PB_ADMIN_EMAIL", "")
PASSWORD = os.environ.get("SYNERGIUM_FORMS_PB_ADMIN_PASSWORD", "")

DEFAULT_SHEET_ID = "19XjibPTR6LFRLM3fJXffLbFDebOT1kXWMhKvh7-nJ5w"
DEFAULT_GID = "1537513728"
REPO = Path(__file__).resolve().parents[1]
SCHEMA_EN = REPO / "forms/casos/community-directory-matching/schema-en-google-sync.json"
# Frozen labels/options matching the Google Form / Sheet headers.
# Live web form schema (professional copy) is schema-en.json — do not point sync there
# or column mapping breaks. Heterogeneous answers in PB are expected.

# Google Form label variants → field_id
HEADER_ALIASES = {
    "Share with a match (if Q28=Yes, tick name + email or WhatsApp)": "share_with_match",
    "Timestamp": None,  # skip
}


def req(method: str, path: str, body=None, token: str | None = None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = token
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=90) as res:
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


def find_form(token: str, public_id: str) -> dict:
    filt = urllib.parse.quote(f'public_id="{public_id}"')
    out = req("GET", f"/api/collections/forms/records?filter={filt}&perPage=1", token=token)
    items = out.get("items") or []
    if not items:
        raise SystemExit(f"form not found: {public_id}")
    return items[0]


def load_schema() -> dict:
    return json.loads(SCHEMA_EN.read_text(encoding="utf-8"))


def build_maps(schema: dict):
    label_to_field = {}
    value_maps = {}  # field_id -> {option_label_lower: value}
    for f in schema.get("fields") or []:
        label_to_field[f["label"]] = f["id"]
        if f.get("options"):
            value_maps[f["id"]] = {o["label"].strip().lower(): o["value"] for o in f["options"]}
    for alias, fid in HEADER_ALIASES.items():
        if fid:
            label_to_field[alias] = fid
    return label_to_field, value_maps


def fetch_csv(sheet_id: str, gid: str) -> str:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    req_http = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 SynergiumFormsSync/1.0"})
    with urllib.request.urlopen(req_http, timeout=90) as res:
        return res.read().decode("utf-8")


def split_multi(raw: str) -> list[str]:
    if not raw or not str(raw).strip():
        return []
    # Google multi-select joins with ", "
    parts = [p.strip() for p in str(raw).split(",")]
    return [p for p in parts if p]


def map_cell(field: dict, raw: str, value_maps: dict):
    fid = field["id"]
    t = field["type"]
    if raw is None:
        raw = ""
    raw = str(raw).strip()
    if t in ("text", "email", "phone", "textarea"):
        return raw
    if t == "url_list":
        return [u.strip() for u in raw.replace(",", "\n").splitlines() if u.strip()]
    if t == "single_select":
        if not raw:
            return ""
        vm = value_maps.get(fid, {})
        v = vm.get(raw.lower())
        if v:
            return v
        # Other free text
        if field.get("allow_other"):
            return {"value": "other", "other_text": raw}
        return raw
    if t == "multi_select":
        labels = split_multi(raw)
        vm = value_maps.get(fid, {})
        out = []
        other_bits = []
        for lab in labels:
            v = vm.get(lab.lower())
            if v:
                out.append(v)
            else:
                other_bits.append(lab)
        if other_bits and field.get("allow_other"):
            out.append({"value": "other", "other_text": ", ".join(other_bits)})
        elif other_bits:
            out.extend(other_bits)
        return out
    return raw


def row_to_answers(row: dict, schema: dict, label_to_field: dict, value_maps: dict) -> dict:
    fields_by_id = {f["id"]: f for f in schema["fields"]}
    answers = {}
    for header, raw in row.items():
        if header in HEADER_ALIASES and HEADER_ALIASES[header] is None:
            continue
        fid = label_to_field.get(header)
        if not fid:
            continue
        field = fields_by_id[fid]
        answers[fid] = map_cell(field, raw, value_maps)
    return answers


def existing_emails(token: str, form_id: str) -> set[str]:
    emails: set[str] = set()
    page = 1
    while True:
        filt = urllib.parse.quote(f'form="{form_id}"')
        out = req(
            "GET",
            f"/api/collections/submissions/records?filter={filt}&perPage=200&page={page}&fields=respondent_email,answers",
            token=token,
        )
        items = out.get("items") or []
        for it in items:
            em = (it.get("respondent_email") or "").strip().lower()
            if not em:
                ans = it.get("answers") or {}
                em = str(ans.get("email") or "").strip().lower()
            if em:
                emails.add(em)
        total_pages = int(out.get("totalPages") or 1)
        if page >= total_pages:
            break
        page += 1
    return emails


def main() -> None:
    p = argparse.ArgumentParser(description="Sync Google Sheet → Synergium Forms")
    p.add_argument("--public-id", default="nexus-input")
    p.add_argument("--sheet-id", default=DEFAULT_SHEET_ID)
    p.add_argument("--gid", default=DEFAULT_GID)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--csv", default=None, help="Optional local CSV path instead of download")
    args = p.parse_args()

    schema = load_schema()
    label_to_field, value_maps = build_maps(schema)
    raw_csv = Path(args.csv).read_text(encoding="utf-8") if args.csv else fetch_csv(args.sheet_id, args.gid)
    rows = list(csv.DictReader(io.StringIO(raw_csv)))

    token = auth()
    form = find_form(token, args.public_id)
    form_id = form["id"]
    have = existing_emails(token, form_id)

    created = skipped = errors = 0
    for row in rows:
        answers = row_to_answers(row, schema, label_to_field, value_maps)
        email = str(answers.get("email") or "").strip().lower()
        if not email:
            errors += 1
            print("skip_no_email", row.get("Full name"), file=sys.stderr)
            continue
        if email in have:
            skipped += 1
            continue
        payload = {
            "form": form_id,
            "answers": answers,
            "respondent_email": email,
            "source": "google",
        }
        if args.dry_run:
            print("would_create", email, answers.get("full_name"))
            created += 1
            have.add(email)
            continue
        try:
            req("POST", "/api/collections/submissions/records", payload, token=token)
            created += 1
            have.add(email)
            print("created", email)
        except SystemExit as e:
            errors += 1
            print("error", email, e, file=sys.stderr)

    print(
        json.dumps(
            {
                "sheet_rows": len(rows),
                "created": created,
                "skipped_existing": skipped,
                "errors": errors,
                "dry_run": args.dry_run,
                "public_id": args.public_id,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
