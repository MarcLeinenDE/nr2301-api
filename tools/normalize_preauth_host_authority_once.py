# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

PATH = Path("specification/methods.json")
doc = json.loads(PATH.read_text(encoding="utf-8"))
by_id = {method["method_id"]: method for method in doc["methods"]}

contract = {
    "id": "account.preauth_host_authority.v1",
    "evidence": "LIVE_AB_VERIFIED_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "canonical_management_url": "http://zyxel.home",
    "dns_observation": "zyxel.home resolved to 192.168.1.1 on the tested USB-connected router",
    "direct_ip_observation": "http://192.168.1.1 returned result=4 for administrator pre-auth",
    "canonical_host_observation": "http://zyxel.home returned result=0 for administrator pre-auth",
    "scope": "host/authority-dependent behavior; does not define result=4 as a universal error enum",
}

for method_id in ("account/get_retrytimes_and_time", "account/get_rand"):
    method = by_id[method_id]
    contracts = [
        item for item in method.get("semantic_contracts", [])
        if not (isinstance(item, dict) and item.get("id") == contract["id"])
    ]
    contracts.append(dict(contract, method_id=method_id))
    method["semantic_contracts"] = contracts

    notes = [
        note for note in method.get("implementation_notes", [])
        if "current result=4" not in note.lower()
        and "cause remains unresolved" not in note.lower()
        and "compare the exact historically working transport" not in note.lower()
    ]
    notes.extend([
        "On tested firmware V1.00(ACIY.3)C0, administrator pre-auth is host/authority sensitive.",
        "zyxel.home and 192.168.1.1 reached the same router address during the USB A/B test, but the direct-IP path returned result=4 while http://zyxel.home returned result=0.",
        "The behavior was unchanged by requests-vs-urllib transport, historical compact JSON/header reproduction, WebUI bootstrap, or explicit WebUI logout.",
        "Use http://zyxel.home as the canonical administrator management URL on the tested firmware.",
        "Do not assign a universal meaning to result=4 from this observation; the result-code table for account/login remains endpoint-specific.",
    ])
    method["implementation_notes"] = list(dict.fromkeys(notes))

get_rand = by_id["account/get_rand"]
contracts = []
for item in get_rand.get("semantic_contracts", []):
    if isinstance(item, dict) and item.get("id") == "account.get_rand_result4.usb_retest.v1":
        item = dict(item)
        item["meaning"] = "DIRECT_IP_HOST_AUTHORITY_OBSERVATION_ON_TESTED_FIRMWARE"
        item["resolved_by_ab_test"] = (
            "The same router and historical [a-z0-9]{8} user_id returned result=0 when addressed as http://zyxel.home."
        )
        item["constraint"] = (
            "Do not generalize result=4 as a universal host error or apply the account/login result table to get_rand."
        )
    contracts.append(item)
get_rand["semantic_contracts"] = contracts

login = by_id["account/login"]
login_notes = login.get("implementation_notes", []) + [
    "On tested firmware V1.00(ACIY.3)C0, use the canonical management host http://zyxel.home for the administrator challenge/login flow; direct-IP pre-auth returned result=4 before password submission.",
]
login["implementation_notes"] = list(dict.fromkeys(login_notes))

PATH.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Normalized administrator pre-auth host/authority A/B evidence.")
