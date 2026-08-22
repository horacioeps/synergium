#!/usr/bin/env python3
"""Backfill match pipeline tracking from known expedientes in clientes/."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("SYNERGIUM_FORMS_PB_URL", "https://forms.synergium.net").rstrip("/")
EMAIL = os.environ["SYNERGIUM_FORMS_PB_ADMIN_EMAIL"]
PASSWORD = os.environ["SYNERGIUM_FORMS_PB_ADMIN_PASSWORD"]
FROM_EMAIL = "horacio@horacio-ps.com"

# Canonical seed from clientes/matches/* and clientes/piloto/* (2026-08-22).
MATCHES = [
    {
        "match_number": 1,
        "match_reference": "match-2026-001",
        "slug": "matias-valentina",
        "axis": "Salud mental / bienestar",
        "status": "active",
        "current_step": "match_align_partial",
        "expediente_path": "clientes/piloto/matias-rodriguez-rivas/",
        "participants": [
            {
                "side": "a",
                "person_name": "Matías E. Rodríguez-Rivas",
                "person_email": "matiaserodriguezrivas@gmail.com",
                "whatsapp": "+56930322072",
                "current_step": "opt_in_pending",
            },
            {
                "side": "b",
                "person_name": "Valentina Lucena Jurado",
                "person_email": "valentina.lucena@gmail.com",
                "whatsapp": "+34661347478",
                "current_step": "match_align_done",
            },
        ],
        "events": [
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:00:00Z",
                "person_email": "matiaserodriguezrivas@gmail.com",
                "to_email": "matiaserodriguezrivas@gmail.com",
                "from_email": FROM_EMAIL,
                "subject": "Synergium: posible colaboración (salud mental)",
                "notes": "Opt-in ES; sin respuesta 22/08",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:06:00Z",
                "person_email": "valentina.lucena@gmail.com",
                "to_email": "valentina.lucena@gmail.com",
                "from_email": FROM_EMAIL,
                "subject": "Synergium: brief corto antes de la intro",
                "notes": "Paso 2 match-align ES",
            },
            {
                "event_type": "inbound_reply",
                "channel": "whatsapp",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-20 12:00:00Z",
                "person_email": "valentina.lucena@gmail.com",
                "notes": "WA sí: «claro encantada»",
            },
        ],
    },
    {
        "match_number": 2,
        "match_reference": "match-2026-002",
        "slug": "ferran-elena",
        "axis": "CADD / drug discovery obesidad",
        "status": "discarded",
        "current_step": "curated",
        "discarded_reason": "Horacio pidió no enviar opt-in (2026-08-21)",
        "expediente_path": "clientes/matches/ferran-elena/",
        "participants": [
            {
                "side": "a",
                "person_name": "Ferran Acuña Parés",
                "person_email": "ferran.acuna@unir.net",
                "current_step": "directory",
            },
            {
                "side": "b",
                "person_name": "Elena Murcia García",
                "person_email": "emurcia@ucam.edu",
                "current_step": "directory",
            },
        ],
        "events": [
            {
                "event_type": "note",
                "channel": "other",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 12:00:00Z",
                "notes": "Opt-in descartado; no enviar",
            },
        ],
    },
    {
        "match_number": 3,
        "match_reference": "match-2026-003",
        "slug": "causa-yen-na",
        "axis": "Educación superior / jóvenes",
        "status": "active",
        "current_step": "match_align_partial",
        "expediente_path": "clientes/matches/causa-yen-na/",
        "participants": [
            {
                "side": "a",
                "person_name": "Matías Causa",
                "person_email": "causamd@gmail.com",
                "whatsapp": "+542213541572",
                "current_step": "match_align_done",
            },
            {
                "side": "b",
                "person_name": "Yen Na Yum",
                "person_email": "yyum2024@gmail.com",
                "whatsapp": "+85266091707",
                "current_step": "opt_in_pending",
            },
        ],
        "events": [
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 10:24:00Z",
                "person_email": "causamd@gmail.com",
                "to_email": "causamd@gmail.com",
                "from_email": FROM_EMAIL,
                "subject": "Synergium: posible colaboración (educación)",
            },
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 10:24:00Z",
                "person_email": "yyum2024@gmail.com",
                "to_email": "yyum2024@gmail.com",
                "from_email": FROM_EMAIL,
                "subject": "Synergium: possible collaboration (education)",
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-21 20:32:00Z",
                "person_email": "causamd@gmail.com",
                "notes": "Sí: «Absolutamente de acuerdo. Adelante.»",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:22:00Z",
                "person_email": "causamd@gmail.com",
                "to_email": "causamd@gmail.com",
                "from_email": FROM_EMAIL,
                "notes": "Paso 2 match-align ES; ref match-2026-003",
            },
        ],
    },
    {
        "match_number": 4,
        "match_reference": "match-2026-004",
        "slug": "driselda-tatiana",
        "axis": "Patrimonio / territorio / humanidades",
        "status": "active",
        "current_step": "match_align_complete",
        "expediente_path": "clientes/matches/driselda-tatiana/",
        "participants": [
            {
                "side": "a",
                "person_name": "Driselda Patricia Sánchez Aguirre",
                "person_email": "dsanchez@encit.unam.mx",
                "whatsapp": "+527771294657",
                "current_step": "match_align_done",
            },
            {
                "side": "b",
                "person_name": "Tatiana González L",
                "person_email": "tatiana.gonzalezl@udea.edu.co",
                "whatsapp": "+573002469789",
                "current_step": "match_align_done",
            },
        ],
        "events": [
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 10:16:00Z",
                "person_email": "dsanchez@encit.unam.mx",
                "to_email": "dsanchez@encit.unam.mx",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 10:16:00Z",
                "person_email": "tatiana.gonzalezl@udea.edu.co",
                "to_email": "tatiana.gonzalezl@udea.edu.co",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-21 11:44:00Z",
                "person_email": "dsanchez@encit.unam.mx",
                "notes": "Sí opt-in",
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-21 14:57:00Z",
                "person_email": "tatiana.gonzalezl@udea.edu.co",
                "notes": "Sí opt-in",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:22:00Z",
                "person_email": "dsanchez@encit.unam.mx",
                "notes": "Paso 2 ambos",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:24:00Z",
                "person_email": "tatiana.gonzalezl@udea.edu.co",
                "notes": "Paso 2 ambos",
            },
        ],
    },
    {
        "match_number": 5,
        "match_reference": "match-2026-005",
        "slug": "erdogan-antonio",
        "axis": "Medical imaging / deep learning",
        "status": "active",
        "current_step": "match_align_partial",
        "expediente_path": "clientes/matches/erdogan-antonio/",
        "participants": [
            {
                "side": "a",
                "person_name": "Erdoğan Aldemir",
                "person_email": "erdogan.aldemir@batman.edu.tr",
                "whatsapp": "+905379397879",
                "current_step": "opt_in_pending",
            },
            {
                "side": "b",
                "person_name": "Antonio Jesús Fernández García",
                "person_email": "ajfernandez@ual.es",
                "whatsapp": "+34622217502",
                "current_step": "match_align_done",
            },
        ],
        "events": [
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 15:11:00Z",
                "person_email": "erdogan.aldemir@batman.edu.tr",
                "to_email": "erdogan.aldemir@batman.edu.tr",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 15:11:00Z",
                "person_email": "ajfernandez@ual.es",
                "to_email": "ajfernandez@ual.es",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-22 13:14:00Z",
                "person_email": "ajfernandez@ual.es",
                "notes": "Sí desde fga870@ual.es",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:23:00Z",
                "person_email": "ajfernandez@ual.es",
                "to_email": "fga870@ual.es",
                "from_email": FROM_EMAIL,
                "notes": "Paso 2 match-align ES",
            },
        ],
    },
    {
        "match_number": 6,
        "match_reference": "match-2026-006",
        "slug": "karen-veronica",
        "axis": "Educación / inclusión / arte-educación",
        "status": "active",
        "current_step": "match_align_complete",
        "expediente_path": "clientes/matches/karen-veronica/",
        "participants": [
            {
                "side": "a",
                "person_name": "Karen Villalba",
                "person_email": "karen.villalba.ramos@gmail.com",
                "whatsapp": "+573152033635",
                "current_step": "match_align_done",
            },
            {
                "side": "b",
                "person_name": "E. Verónica Romo López",
                "person_email": "everonicaromo@gmail.com",
                "whatsapp": "+5695397675",
                "current_step": "match_align_done",
            },
        ],
        "events": [
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 15:11:00Z",
                "person_email": "karen.villalba.ramos@gmail.com",
                "to_email": "karen.villalba.ramos@gmail.com",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "opt_in",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-21 15:11:00Z",
                "person_email": "everonicaromo@gmail.com",
                "to_email": "everonicaromo@gmail.com",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-21 21:26:00Z",
                "person_email": "karen.villalba.ramos@gmail.com",
                "notes": "Sí opt-in",
            },
            {
                "event_type": "inbound_reply",
                "channel": "email",
                "direction": "inbound",
                "status": "received",
                "sent_at": "2026-08-21 15:50:00Z",
                "person_email": "everonicaromo@gmail.com",
                "notes": "Sí opt-in",
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:23:00Z",
                "person_email": "karen.villalba.ramos@gmail.com",
                "from_email": FROM_EMAIL,
            },
            {
                "event_type": "match_align",
                "channel": "email",
                "direction": "outbound",
                "status": "sent",
                "sent_at": "2026-08-22 15:24:00Z",
                "person_email": "everonicaromo@gmail.com",
                "from_email": FROM_EMAIL,
            },
        ],
    },
    {
        "match_number": 7,
        "match_reference": "match-2026-007",
        "slug": "michelle-kinndle",
        "axis": "Sostenibilidad / ambiente / One Health",
        "status": "active",
        "current_step": "curated",
        "expediente_path": "clientes/matches/michelle-kinndle/",
        "participants": [
            {
                "side": "a",
                "person_name": "Michelle Viera Romero",
                "person_email": "michelle.vierarom@ug.edu.ec",
                "whatsapp": "+593986815603",
                "current_step": "directory",
            },
            {
                "side": "b",
                "person_name": "Kinndle Blanco Peña",
                "person_email": "kblanco@una.cr",
                "whatsapp": "+50683970508",
                "current_step": "directory",
            },
        ],
        "events": [],
    },
]


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
    out = req(
        "POST",
        "/api/collections/_superusers/auth-with-password",
        {"identity": EMAIL, "password": PASSWORD},
    )
    return out["token"]


def find_one(token: str, collection: str, filter_expr: str) -> dict | None:
    q = urllib.parse.urlencode({"filter": filter_expr, "perPage": 1})
    out = req("GET", f"/api/collections/{collection}/records?{q}", token=token)
    items = out.get("items") or []
    return items[0] if items else None


def upsert_match(token: str, seed: dict) -> str:
    ref = seed["match_reference"]
    existing = find_one(token, "matches", f'match_reference="{ref}"')
    pa = seed["participants"][0]
    pb = seed["participants"][1]
    payload = {
        "match_number": seed["match_number"],
        "match_reference": ref,
        "slug": seed["slug"],
        "axis": seed.get("axis", ""),
        "status": seed.get("status", "active"),
        "current_step": seed.get("current_step", "curated"),
        "person_a_name": pa["person_name"],
        "person_a_email": pa["person_email"],
        "person_b_name": pb["person_name"],
        "person_b_email": pb["person_email"],
        "expediente_path": seed.get("expediente_path", ""),
        "notes": seed.get("notes", ""),
        "discarded_reason": seed.get("discarded_reason", ""),
    }
    if existing:
        req("PATCH", f"/api/collections/matches/records/{existing['id']}", payload, token=token)
        print(f"updated match {ref}")
        return existing["id"]
    out = req("POST", "/api/collections/matches/records", payload, token=token)
    print(f"created match {ref}")
    return out["id"]


def upsert_participant(token: str, match_id: str, seed: dict) -> str:
    email = seed["person_email"]
    existing = find_one(
        token,
        "match_participants",
        f'match="{match_id}" && person_email="{email}"',
    )
    payload = {
        "match": match_id,
        "person_name": seed.get("person_name", ""),
        "person_email": email,
        "side": seed["side"],
        "whatsapp": seed.get("whatsapp", ""),
        "match_language": seed.get("match_language", ""),
        "current_step": seed.get("current_step", "directory"),
    }
    if existing:
        req(
            "PATCH",
            f"/api/collections/match_participants/records/{existing['id']}",
            payload,
            token=token,
        )
        return existing["id"]
    out = req("POST", "/api/collections/match_participants/records", payload, token=token)
    return out["id"]


def event_fingerprint(ev: dict, match_ref: str) -> str:
    parts = [
        match_ref,
        ev.get("event_type", ""),
        ev.get("direction", ""),
        ev.get("person_email", ""),
        ev.get("sent_at", ""),
        ev.get("notes", "")[:80],
    ]
    return "|".join(parts)


def upsert_event(token: str, match_id: str, match_ref: str, ev: dict, participant_id: str | None):
    fp = event_fingerprint(ev, match_ref)
    existing = find_one(token, "contact_events", f'notes="{fp}"')
    if existing:
        return
    payload = {
        "match": match_id,
        "participant": participant_id,
        "event_type": ev["event_type"],
        "channel": ev["channel"],
        "direction": ev["direction"],
        "status": ev.get("status", "sent"),
        "sent_at": ev.get("sent_at"),
        "from_email": ev.get("from_email", ""),
        "to_email": ev.get("to_email", ""),
        "person_email": ev.get("person_email", ""),
        "match_reference": match_ref,
        "subject": ev.get("subject", ""),
        "body": ev.get("body", ""),
        "notes": fp if not ev.get("notes") else f"{ev['notes']} [{fp}]",
    }
    req("POST", "/api/collections/contact_events/records", payload, token=token)


def main() -> None:
    dry = "--dry-run" in os.sys.argv
    if dry:
        print(f"DRY RUN — would backfill {len(MATCHES)} matches")
        for m in MATCHES:
            print(f"  {m['match_reference']} ({m['slug']}) — {len(m.get('events', []))} events")
        return

    token = auth()
    for seed in MATCHES:
        match_id = upsert_match(token, seed)
        part_ids: dict[str, str] = {}
        for p in seed["participants"]:
            pid = upsert_participant(token, match_id, p)
            part_ids[p["person_email"]] = pid
        for ev in seed.get("events", []):
            pe = ev.get("person_email", "")
            upsert_event(token, match_id, seed["match_reference"], ev, part_ids.get(pe))
        print(
            f"  {seed['match_reference']}: {len(seed['participants'])} participants, "
            f"{len(seed.get('events', []))} events"
        )
    print("OK backfill")


if __name__ == "__main__":
    main()
