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

    return {
        "exported_at": iso_now(),
        "source": "seed",
        "pb_url": BASE,
        "matches": match_rows,
        "participants": participant_rows,
        "stats": {
            "matches": len(match_rows),
            "participants": len(participant_rows),
            "events": sum(m["event_count"] for m in match_rows),
        },
    }


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

    return {
        "exported_at": iso_now(),
        "source": "pocketbase",
        "pb_url": BASE,
        "matches": match_rows,
        "participants": participant_rows,
        "stats": {
            "matches": len(match_rows),
            "participants": len(participant_rows),
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
        f"{data['stats']['events']} events ({data['source']})"
    )


if __name__ == "__main__":
    main()
