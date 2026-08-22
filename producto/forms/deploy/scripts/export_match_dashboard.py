#!/usr/bin/env python3
"""Export match pipeline data to static JSON for match-dashboard/index.html."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from backfill_match_tracking import BASE, MATCHES, auth, req  # noqa: E402

OUT_DIR = SCRIPT_DIR.parent / "pb_public" / "match-dashboard"
OUT_FILE = OUT_DIR / "data.json"
REPO_ROOT = SCRIPT_DIR.parent.parent.parent.parent
NEXUS_SCHEMA_PATH = REPO_ROOT / "comunidad" / "formulario" / "nexus-input" / "schema-en.json"
MATCH_ALIGN_SCHEMA_PATH = REPO_ROOT / "comunidad" / "formulario" / "match-align" / "schema-en.json"


def iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_date(val: str | None) -> str | None:
    if not val:
        return None
    return val.replace(" ", "T").replace("Z", "")[:10]


def last_sent_at(events: list[dict]) -> str | None:
    dates = [e.get("sent_at") for e in events if e.get("sent_at")]
    if not dates:
        return None
    return max(dates)


def opt_in_sent_for(events: list[dict], email: str) -> bool:
    email = email.lower()
    for ev in events:
        if ev.get("event_type") != "opt_in":
            continue
        if ev.get("direction") != "outbound":
            continue
        pe = (ev.get("person_email") or ev.get("to_email") or "").lower()
        if pe == email:
            return True
    return False


def build_from_seed() -> dict:
    match_rows = []
    participant_rows = []

    for seed in MATCHES:
        events = seed.get("events") or []
        pa = seed["participants"][0]
        pb = seed["participants"][1]
        opt_a = opt_in_sent_for(events, pa["person_email"])
        opt_b = opt_in_sent_for(events, pb["person_email"])

        match_rows.append(
            {
                "match_number": seed["match_number"],
                "match_reference": seed["match_reference"],
                "slug": seed["slug"],
                "axis": seed.get("axis", ""),
                "status": seed.get("status", "active"),
                "current_step": seed.get("current_step", "curated"),
                "pairing_status": seed.get("pairing_status", "proposed"),
                "pairing_method": seed.get("pairing_method", ""),
                "proposed_at": parse_date(seed.get("proposed_at")),
                "paired_at": parse_date(seed.get("paired_at")),
                "person_a_name": pa["person_name"],
                "person_a_email": pa["person_email"],
                "person_b_name": pb["person_name"],
                "person_b_email": pb["person_email"],
                "expediente_path": seed.get("expediente_path", ""),
                "opt_in_a_sent": opt_a,
                "opt_in_b_sent": opt_b,
                "last_contact_at": parse_date(last_sent_at(events)),
                "event_count": len(events),
            }
        )

        for p in seed["participants"]:
            participant_rows.append(
                {
                    "match_number": seed["match_number"],
                    "match_reference": seed["match_reference"],
                    "slug": seed["slug"],
                    "side": p["side"],
                    "person_name": p.get("person_name", ""),
                    "person_email": p["person_email"],
                    "whatsapp": p.get("whatsapp", ""),
                    "current_step": p.get("current_step", "directory"),
                    "is_paired": p.get("is_paired", True),
                    "paired_with_email": p.get(
                        "paired_with_email",
                        pb["person_email"] if p["side"] == "a" else pa["person_email"],
                    ),
                    "pairing_proposed_at": parse_date(
                        p.get("pairing_proposed_at") or seed.get("proposed_at")
                    ),
                    "opt_in_sent": opt_in_sent_for(events, p["person_email"]),
                    "last_contact_at": parse_date(
                        last_sent_at([e for e in events if e.get("person_email") == p["person_email"]])
                        or last_sent_at(events)
                    ),
                }
            )

    participant_rows.sort(key=lambda x: (x.get("match_number") or 0, x.get("side") or ""))

    # Seed directory: participants only (no PB submissions in --seed-only).
    directory_rows = []
    seen: set[str] = set()
    for p in participant_rows:
        email = (p.get("person_email") or "").lower()
        if not email or email in seen:
            continue
        seen.add(email)
        directory_rows.append(
            {
                "person_name": p.get("person_name", ""),
                "person_email": p.get("person_email", ""),
                "country": "",
                "whatsapp": p.get("whatsapp", ""),
                "match_me": "yes",
                "match_me_label": match_me_label("yes"),
                "source": "seed",
                "submitted_at": None,
                "is_paired": bool(p.get("is_paired")),
                "match_number": p.get("match_number"),
                "match_reference": p.get("match_reference", ""),
                "slug": p.get("slug", ""),
                "paired_with_email": p.get("paired_with_email", ""),
                "current_step": p.get("current_step") or "directory",
                "last_contact_at": p.get("last_contact_at"),
            }
        )

    seed_matches: list[dict] = []
    seed_participants: list[dict] = []
    seed_events: list[dict] = []
    for seed in MATCHES:
        ref = seed["match_reference"]
        seed_matches.append({k: v for k, v in seed.items() if k not in ("participants", "events")})
        pa = seed["participants"][0]
        pb = seed["participants"][1]
        for p in seed["participants"]:
            paired = pb if p["side"] == "a" else pa
            seed_participants.append(
                {
                    **p,
                    "match_reference": ref,
                    "is_paired": p.get("is_paired", True),
                    "paired_with_email": p.get("paired_with_email", paired["person_email"]),
                    "pairing_proposed_at": p.get("pairing_proposed_at") or seed.get("proposed_at"),
                }
            )
        for ev in seed.get("events") or []:
            seed_events.append({**ev, "match_reference": ev.get("match_reference") or ref})

    nexus_schema = load_schema(NEXUS_SCHEMA_PATH)
    match_align_schema = load_schema(MATCH_ALIGN_SCHEMA_PATH)
    profile_rows = build_profiles(
        nexus_submissions=[],
        match_align_submissions=[],
        participants=seed_participants,
        matches=seed_matches,
        events=seed_events,
        nexus_schema=nexus_schema,
        match_align_schema=match_align_schema,
        participant_rows=participant_rows,
    )

    return {
        "exported_at": iso_now(),
        "source": "seed",
        "pb_url": BASE,
        "matches": match_rows,
        "participants": participant_rows,
        "directory": directory_rows,
        "profiles": profile_rows,
        "stats": {
            "matches": len(match_rows),
            "participants": len(participant_rows),
            "directory": len(directory_rows),
            "profiles": len(profile_rows),
            "submissions_total": len(directory_rows),
            "events": sum(m["event_count"] for m in match_rows),
        },
    }


NEXUS_INPUT_PUBLIC_ID = "nexus-input"
MATCH_ALIGN_PUBLIC_ID = "match-align"
DIRECTORY_MATCH_ME = frozenset({"yes", "directory_only", "you_only_no_intro"})


def parse_answers(raw: dict | str | None) -> dict:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}


def submission_email(sub: dict, answers: dict) -> str:
    return (sub.get("respondent_email") or answers.get("email") or "").strip()


def is_test_submission(email: str, answers: dict) -> bool:
    name = (answers.get("full_name") or "").lower()
    return email.lower().startswith("publictest") or name.startswith("publictest")


def match_me_label(value: str | None) -> str:
    labels = {
        "yes": "Sí (matching)",
        "directory_only": "Solo directorio",
        "you_only_no_intro": "Equipo ve datos; sin intro",
        "no": "No",
    }
    return labels.get(value or "", value or "—")


def load_schema(path: Path) -> dict:
    if not path.is_file():
        return {"fields": []}
    return json.loads(path.read_text(encoding="utf-8"))


def format_field_value(field: dict, value: object) -> str:
    if value is None or value == "" or value == []:
        return ""
    ftype = field.get("type", "text")
    if ftype in ("text", "email", "phone", "textarea"):
        return str(value)
    if ftype == "url_list":
        if isinstance(value, list):
            return "\n".join(str(v) for v in value)
        return str(value)
    if ftype == "single_select":
        opt_map = {o["value"]: o["label"] for o in field.get("options", [])}
        if isinstance(value, dict):
            return value.get("label") or value.get("value") or json.dumps(value, ensure_ascii=False)
        if isinstance(value, str) and value in opt_map:
            return opt_map[value]
        return str(value)
    if ftype == "multi_select":
        opt_map = {o["value"]: o["label"] for o in field.get("options", [])}
        if isinstance(value, list):
            parts = []
            for v in value:
                if isinstance(v, dict):
                    parts.append(v.get("label") or v.get("value") or json.dumps(v, ensure_ascii=False))
                else:
                    parts.append(opt_map.get(v, str(v)))
            return "; ".join(parts)
        return str(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def answers_to_labeled_fields(schema: dict, answers: dict) -> list[dict]:
    field_defs = {f["id"]: f for f in schema.get("fields", [])}
    rows: list[dict] = []
    for fid, fdef in field_defs.items():
        if fid not in answers:
            continue
        val = answers[fid]
        if val is None or val == "" or val == []:
            continue
        rows.append(
            {
                "field_id": fid,
                "label": fdef.get("label", fid),
                "value": format_field_value(fdef, val),
            }
        )
    for fid, val in answers.items():
        if fid in field_defs or val in (None, "", []):
            continue
        rows.append({"field_id": fid, "label": fid, "value": str(val)})
    return rows


def serialize_event(ev: dict) -> dict:
    return {
        "event_type": ev.get("event_type", ""),
        "channel": ev.get("channel", ""),
        "direction": ev.get("direction", ""),
        "status": ev.get("status", ""),
        "sent_at": ev.get("sent_at") or "",
        "subject": ev.get("subject") or "",
        "body": ev.get("body") or "",
        "notes": ev.get("notes") or "",
        "match_reference": ev.get("match_reference") or "",
        "from_email": ev.get("from_email") or "",
        "to_email": ev.get("to_email") or "",
        "person_email": ev.get("person_email") or "",
    }


def events_for_email(events: list[dict], email: str) -> list[dict]:
    key = email.lower()
    matched: list[dict] = []
    for ev in events:
        candidates = (ev.get("person_email"), ev.get("to_email"), ev.get("from_email"))
        if any((c or "").lower() == key for c in candidates):
            matched.append(serialize_event(ev))
    matched.sort(key=lambda e: e.get("sent_at") or "", reverse=True)
    return matched


def fetch_form_submissions(token: str, public_id: str) -> list[dict]:
    forms = req(
        "GET",
        f"/api/collections/forms/records?filter=public_id='{public_id}'",
        token=token,
    ).get("items") or []
    if not forms:
        return []
    form_id = forms[0]["id"]
    items: list[dict] = []
    page = 1
    while True:
        params: dict[str, str | int] = {"page": page, "perPage": 200, "filter": f"form='{form_id}'"}
        q = urllib.parse.urlencode(params)
        out = req("GET", f"/api/collections/submissions/records?{q}", token=token)
        batch = out.get("items") or []
        items.extend(batch)
        if page >= out.get("totalPages", 1):
            break
        page += 1
    return items


def fetch_nexus_submissions(token: str) -> list[dict]:
    return fetch_form_submissions(token, NEXUS_INPUT_PUBLIC_ID)


def participant_pipeline_row(
    p: dict,
    match: dict,
    participants: list[dict],
) -> dict:
    paired_email = (p.get("paired_with_email") or "").lower()
    paired_name = ""
    for other in participants:
        if (other.get("person_email") or "").lower() == paired_email:
            paired_name = other.get("person_name") or ""
            break
    return {
        "match_number": match.get("match_number"),
        "match_reference": match.get("match_reference", ""),
        "slug": match.get("slug", ""),
        "axis": match.get("axis", ""),
        "side": p.get("side", ""),
        "current_step": p.get("current_step", ""),
        "is_paired": bool(p.get("is_paired")),
        "paired_with_name": paired_name,
        "paired_with_email": p.get("paired_with_email", ""),
        "pairing_proposed_at": parse_date(p.get("pairing_proposed_at")),
        "pairing_status": match.get("pairing_status", ""),
        "pairing_method": match.get("pairing_method", ""),
        "match_current_step": match.get("current_step", ""),
        "match_status": match.get("status", ""),
        "expediente_path": match.get("expediente_path", ""),
    }


def build_profiles(
    *,
    nexus_submissions: list[dict],
    match_align_submissions: list[dict],
    participants: list[dict],
    matches: list[dict],
    events: list[dict],
    nexus_schema: dict,
    match_align_schema: dict,
    participant_rows: list[dict] | None = None,
) -> list[dict]:
    match_by_id = {m["id"]: m for m in matches if m.get("id")}
    match_by_ref = {m.get("match_reference", ""): m for m in matches if m.get("match_reference")}

    # Latest nexus submission per email (non-test).
    nexus_by_email: dict[str, dict] = {}
    for sub in nexus_submissions:
        answers = parse_answers(sub.get("answers"))
        email = submission_email(sub, answers)
        if not email or is_test_submission(email, answers):
            continue
        key = email.lower()
        prev = nexus_by_email.get(key)
        if not prev or (sub.get("created") or "") > (prev.get("created") or ""):
            nexus_by_email[key] = sub

    # Match-align submissions grouped by email.
    align_by_email: dict[str, list[dict]] = {}
    for sub in match_align_submissions:
        answers = parse_answers(sub.get("answers"))
        email = submission_email(sub, answers)
        if not email or is_test_submission(email, answers):
            continue
        align_by_email.setdefault(email.lower(), []).append(sub)

    participants_by_email: dict[str, list[dict]] = {}
    for p in participants:
        email = (p.get("person_email") or "").strip()
        if email:
            participants_by_email.setdefault(email.lower(), []).append(p)

    # Collect every email from pipeline, directory, and contact history.
    all_emails: set[str] = set()
    all_emails.update(nexus_by_email.keys())
    all_emails.update(participants_by_email.keys())
    for ev in events:
        for key in ("person_email", "to_email", "from_email"):
            val = (ev.get(key) or "").strip().lower()
            if val and not val.startswith("publictest"):
                all_emails.add(val)

    profiles: list[dict] = []
    for email_key in sorted(all_emails):
        sub = nexus_by_email.get(email_key)
        answers = parse_answers(sub.get("answers")) if sub else {}

        # Identity from submission, then pipeline participant rows.
        part_list = participants_by_email.get(email_key, [])
        part_export = None
        if participant_rows:
            for row in participant_rows:
                if (row.get("person_email") or "").lower() == email_key:
                    part_export = row
                    break
        first_part = part_list[0] if part_list else {}

        name = (
            answers.get("full_name")
            or (part_export or {}).get("person_name")
            or first_part.get("person_name")
            or ""
        )
        if is_test_submission(email_key, {"full_name": name}):
            continue

        pipeline: list[dict] = []
        for p in part_list:
            mid = p.get("match")
            match = match_by_id.get(mid, {}) if mid else {}
            if not match:
                match = match_by_ref.get(p.get("match_reference", ""), {})
            if not match and part_export:
                ref = part_export.get("match_reference")
                if ref:
                    match = match_by_ref.get(ref, {})
            pipeline.append(participant_pipeline_row(p, match, participants))

        # Seed / export rows without raw PB participant objects.
        if not pipeline and part_export:
            pipeline.append(
                {
                    "match_number": part_export.get("match_number"),
                    "match_reference": part_export.get("match_reference", ""),
                    "slug": part_export.get("slug", ""),
                    "axis": "",
                    "side": part_export.get("side", ""),
                    "current_step": part_export.get("current_step", ""),
                    "is_paired": bool(part_export.get("is_paired")),
                    "paired_with_name": "",
                    "paired_with_email": part_export.get("paired_with_email", ""),
                    "pairing_proposed_at": part_export.get("pairing_proposed_at"),
                    "pairing_status": "",
                    "pairing_method": "",
                    "match_current_step": "",
                    "match_status": "",
                    "expediente_path": "",
                }
            )

        match_align: list[dict] = []
        for align_sub in align_by_email.get(email_key, []):
            align_answers = parse_answers(align_sub.get("answers"))
            match_align.append(
                {
                    "submitted_at": parse_date(align_sub.get("created")),
                    "match_reference": align_answers.get("match_reference") or "",
                    "fields": answers_to_labeled_fields(match_align_schema, align_answers),
                }
            )
        match_align.sort(key=lambda r: r.get("submitted_at") or "", reverse=True)

        display_email = (
            (sub.get("respondent_email") if sub else None)
            or answers.get("email")
            or first_part.get("person_email")
            or ((part_export or {}).get("person_email"))
            or email_key
        )

        profiles.append(
            {
                "person_name": name,
                "person_email": display_email,
                "whatsapp": answers.get("whatsapp") or first_part.get("whatsapp") or "",
                "country": answers.get("country") or "",
                "institution": answers.get("institution") or "",
                "city": answers.get("city") or "",
                "match_me": answers.get("match_me") or "",
                "match_me_label": match_me_label(answers.get("match_me")),
                "submitted_at": parse_date(sub.get("created")) if sub else None,
                "nexus_source": sub.get("source") if sub else "",
                "nexus_form": answers_to_labeled_fields(nexus_schema, answers) if answers else [],
                "pipeline": pipeline,
                "contact_events": events_for_email(events, email_key),
                "match_align": match_align,
            }
        )

    profiles.sort(key=lambda p: (p.get("person_name") or p.get("person_email") or "").lower())
    return profiles


def build_directory_rows(
    submissions: list[dict],
    participant_by_email: dict[str, dict],
    match_by_id: dict[str, dict],
    events_by_person: dict[str, list],
) -> list[dict]:
    rows: list[dict] = []
    seen_emails: set[str] = set()

    for sub in submissions:
        answers = parse_answers(sub.get("answers"))
        email = submission_email(sub, answers)
        if not email or is_test_submission(email, answers):
            continue

        match_me = answers.get("match_me") or ""
        if match_me not in DIRECTORY_MATCH_ME:
            continue

        key = email.lower()
        if key in seen_emails:
            continue
        seen_emails.add(key)

        part = participant_by_email.get(key, {})
        mid = part.get("match")
        match = match_by_id.get(mid, {}) if mid else {}
        pe_events = events_by_person.get(key, [])

        rows.append(
            {
                "person_name": answers.get("full_name") or part.get("person_name") or "",
                "person_email": email,
                "country": answers.get("country") or "",
                "whatsapp": answers.get("whatsapp") or part.get("whatsapp") or "",
                "match_me": match_me,
                "match_me_label": match_me_label(match_me),
                "source": sub.get("source") or "",
                "submitted_at": parse_date(sub.get("created")),
                "is_paired": bool(part.get("is_paired")),
                "match_number": match.get("match_number"),
                "match_reference": match.get("match_reference", ""),
                "slug": match.get("slug", ""),
                "paired_with_email": part.get("paired_with_email", ""),
                "current_step": part.get("current_step") or "directory",
                "last_contact_at": parse_date(last_sent_at(pe_events)),
            }
        )

    rows.sort(
        key=lambda r: (
            0 if r.get("is_paired") else 1,
            r.get("person_name") or r.get("person_email") or "",
        )
    )
    return rows


def fetch_all(token: str, collection: str, sort: str | None = None) -> list[dict]:
    items: list[dict] = []
    page = 1
    while True:
        params: dict[str, str | int] = {"page": page, "perPage": 200}
        if sort:
            params["sort"] = sort
        q = urllib.parse.urlencode(params)
        out = req("GET", f"/api/collections/{collection}/records?{q}", token=token)
        batch = out.get("items") or []
        items.extend(batch)
        if page >= out.get("totalPages", 1):
            break
        page += 1
    return items


def build_from_pb(token: str) -> dict:
    matches = fetch_all(token, "matches", sort="match_number")
    participants = fetch_all(token, "match_participants", sort="person_email")
    events = fetch_all(token, "contact_events", sort="-sent_at")
    submissions = fetch_nexus_submissions(token)
    match_align_submissions = fetch_form_submissions(token, MATCH_ALIGN_PUBLIC_ID)
    nexus_schema = load_schema(NEXUS_SCHEMA_PATH)
    match_align_schema = load_schema(MATCH_ALIGN_SCHEMA_PATH)

    events_by_match: dict[str, list] = {}
    events_by_person: dict[str, list] = {}
    for ev in events:
        ref = ev.get("match_reference") or ""
        events_by_match.setdefault(ref, []).append(ev)
        pe = (ev.get("person_email") or "").lower()
        if pe:
            events_by_person.setdefault(pe, []).append(ev)

    match_rows = []
    participant_rows = []

    for m in sorted(matches, key=lambda x: x.get("match_number", 0)):
        ref = m.get("match_reference", "")
        evs = events_by_match.get(ref, [])
        pa_email = (m.get("person_a_email") or "").lower()
        pb_email = (m.get("person_b_email") or "").lower()

        match_rows.append(
            {
                "match_number": m.get("match_number"),
                "match_reference": ref,
                "slug": m.get("slug", ""),
                "axis": m.get("axis", ""),
                "status": m.get("status", ""),
                "current_step": m.get("current_step", ""),
                "pairing_status": m.get("pairing_status", ""),
                "pairing_method": m.get("pairing_method", ""),
                "proposed_at": parse_date(m.get("proposed_at")),
                "paired_at": parse_date(m.get("paired_at")),
                "person_a_name": m.get("person_a_name", ""),
                "person_a_email": m.get("person_a_email", ""),
                "person_b_name": m.get("person_b_name", ""),
                "person_b_email": m.get("person_b_email", ""),
                "expediente_path": m.get("expediente_path", ""),
                "opt_in_a_sent": opt_in_sent_for(evs, pa_email) if pa_email else False,
                "opt_in_b_sent": opt_in_sent_for(evs, pb_email) if pb_email else False,
                "last_contact_at": parse_date(last_sent_at(evs)),
                "event_count": len(evs),
            }
        )

    match_by_id = {m["id"]: m for m in matches}
    for p in participants:
        mid = p.get("match")
        m = match_by_id.get(mid, {})
        ref = m.get("match_reference", "")
        email = p.get("person_email", "")
        pe_events = events_by_person.get(email.lower(), [])

        participant_rows.append(
            {
                "match_number": m.get("match_number"),
                "match_reference": ref,
                "slug": m.get("slug", ""),
                "side": p.get("side", ""),
                "person_name": p.get("person_name", ""),
                "person_email": email,
                "whatsapp": p.get("whatsapp", ""),
                "current_step": p.get("current_step", ""),
                "is_paired": bool(p.get("is_paired")),
                "paired_with_email": p.get("paired_with_email", ""),
                "pairing_proposed_at": parse_date(p.get("pairing_proposed_at")),
                "opt_in_sent": opt_in_sent_for(pe_events, email) or opt_in_sent_for(
                    events_by_match.get(ref, []), email
                ),
                "last_contact_at": parse_date(last_sent_at(pe_events)),
            }
        )

    participant_rows.sort(key=lambda x: (x.get("match_number") or 0, x.get("side") or ""))

    participant_by_email = {
        (p.get("person_email") or "").lower(): p for p in participants if p.get("person_email")
    }
    match_by_id = {m["id"]: m for m in matches}
    directory_rows = build_directory_rows(
        submissions, participant_by_email, match_by_id, events_by_person
    )

    profile_rows = build_profiles(
        nexus_submissions=submissions,
        match_align_submissions=match_align_submissions,
        participants=participants,
        matches=matches,
        events=events,
        nexus_schema=nexus_schema,
        match_align_schema=match_align_schema,
        participant_rows=participant_rows,
    )

    nexus_non_test = [
        s
        for s in submissions
        if not is_test_submission(
            submission_email(s, parse_answers(s.get("answers"))),
            parse_answers(s.get("answers")),
        )
    ]

    return {
        "exported_at": iso_now(),
        "source": "pocketbase",
        "pb_url": BASE,
        "matches": match_rows,
        "participants": participant_rows,
        "directory": directory_rows,
        "profiles": profile_rows,
        "stats": {
            "matches": len(match_rows),
            "participants": len(participant_rows),
            "directory": len(directory_rows),
            "profiles": len(profile_rows),
            "submissions_total": len(nexus_non_test),
            "events": len(events),
        },
    }


def main() -> None:
    seed_only = "--seed-only" in sys.argv
    data: dict

    if seed_only:
        print("Using seed data (no PocketBase)")
        data = build_from_seed()
    else:
        try:
            token = auth()
            data = build_from_pb(token)
            print(f"Exported from PocketBase ({BASE})")
        except Exception as exc:  # noqa: BLE001
            print(f"PocketBase unavailable ({exc}); falling back to seed")
            data = build_from_seed()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_FILE}")
    print(
        f"  {data['stats']['matches']} matches, "
        f"{data['stats']['participants']} participants, "
        f"{data['stats']['directory']} directory, "
        f"{data['stats'].get('profiles', 0)} profiles, "
        f"{data['stats']['events']} events ({data['source']})"
    )


if __name__ == "__main__":
    main()
