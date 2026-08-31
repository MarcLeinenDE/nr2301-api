# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
DOC = Path("api/statistics.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}
method = by_id["statistics/get_conn_clients_info"]

contract_id = "clients.request_type.tokens.live_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_SANITIZED_EXPLICIT_CLIENT_VIEWS_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "admin_session": True,
    "filter_mode": {"mode": "black", "result": 1},
    "views": {
        "get_active_users": {
            "count": 2,
            "fields": ["alias", "client_type", "cur_conn_time", "forbidden", "ip", "mac", "name", "type"],
        },
        "get_inactive_users": {
            "count": 1,
            "fields": ["alias", "client_type", "cur_conn_time", "forbidden", "ip", "mac", "name", "type"],
        },
        "get_allow_users": {"count": 0, "fields": []},
        "get_forbidden_users": {"count": 0, "fields": []},
    },
    "privacy": "Physical test emitted only view counts and field names; no MAC/IP/name/alias values were published.",
    "important": "get_black_white_mode returned mode='black' with result=1 in this read. Do not assume result=0 is a universal success value across statistics read endpoints.",
}
existing = [
    c for c in method.get("semantic_contracts", [])
    if not (isinstance(c, dict) and c.get("id") == contract_id)
]
method["semantic_contracts"] = existing + [contract]
method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
    "2026-08-31 sanitized SDK read confirmed all four explicit request_type tokens in one admin session: active, inactive, allow and forbidden views all returned successfully.",
    "Active/inactive rows exposed alias, client_type, cur_conn_time, forbidden, ip, mac, name and type on ACIY.3; empty allow/forbidden views returned zero rows.",
]))

filter_method = by_id["statistics/get_black_white_mode"]
filter_method["implementation_notes"] = list(dict.fromkeys(filter_method.get("implementation_notes", []) + [
    "2026-08-31 sanitized admin read returned mode='black' with result=1. Treat the result field as endpoint-specific; do not impose a generic result==0 read-success rule."
]))
METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

doc = DOC.read_text(encoding="utf-8")
needle = "- White-mode get_allow_users now live verified with a real Wi-Fi client: absent/allow=0 before set_allow, present/allow=1 after set_allow, active/allow=1 after actual WLAN reconnect, absent again after cleanup.\n"
addition = "- 2026-08-31 sanitized SDK explicit-view sweep confirmed all four exact POST tokens in one Black-mode admin session: active=2, inactive=1, allow=0, forbidden=0. Active/inactive rows exposed `alias`, `client_type`, `cur_conn_time`, `forbidden`, `ip`, `mac`, `name`, `type`; only counts/schema keys were logged.\n"
if addition not in doc and needle in doc:
    doc = doc.replace(needle, needle + addition, 1)
filter_note = "- 2026-08-31 sanitized read returned `mode='black'` with `result=1`; do not treat `result=0` as a universal success requirement for Statistics read endpoints.\n"
mode_note = "- Real transition read-back verified: black -> white -> black, HTTP200/result0 writes and immediate mode read-back.\n"
if filter_note not in doc and mode_note in doc:
    doc = doc.replace(mode_note, mode_note + filter_note, 1)
DOC.write_text(doc, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- live-confirmed all four normalized `statistics/get_conn_clients_info` explicit client-view tokens in one sanitized SDK read (`get_active_users`, `get_inactive_users`, `get_allow_users`, `get_forbidden_users`); also observed `get_black_white_mode` returning `mode=black` with `result=1`, so Statistics read `result` values remain endpoint-specific\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Recorded live statistics client-view evidence.")
