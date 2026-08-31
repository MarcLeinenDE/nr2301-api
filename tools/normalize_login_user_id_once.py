# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

PATH = Path("specification/methods.json")
doc = json.loads(PATH.read_text(encoding="utf-8"))
by_id = {method["method_id"]: method for method in doc["methods"]}

shape = "8 lowercase alphanumeric characters matching [a-z0-9]{8}; known live-working compatibility shape"

get_rand = by_id["account/get_rand"]
get_rand["request"]["schema"]["user_id"] = shape
get_rand["request"]["basis"] = "live-working application evidence + 2026-08-31 physical USB compatibility observation"
get_rand.setdefault("semantic_contracts", [])
contract_id = "account.login_user_id.compat.v1"
if not any(c.get("id") == contract_id for c in get_rand["semantic_contracts"] if isinstance(c, dict)):
    get_rand["semantic_contracts"].append({
        "id": contract_id,
        "evidence": "LIVE_WORKING_CLIENT_PLUS_PHYSICAL_COMPATIBILITY_OBSERVATION",
        "field": "user_id",
        "known_working_shape": "[a-z0-9]{8}",
        "reuse": "reuse the same user_id in the subsequent account/login request",
    })
notes = get_rand.get("implementation_notes", []) + [
    "Historical live-working NR2301 clients used exactly eight lowercase alphanumeric characters for user_id.",
    "During the 2026-08-31 physical USB SDK smoke, a 32-character hexadecimal user_id reproducibly received result=4 before password submission; do not map that result through the account/login result table.",
    "Use [a-z0-9]{8} for compatibility until broader firmware acceptance is separately verified.",
]
get_rand["implementation_notes"] = list(dict.fromkeys(notes))

login = by_id["account/login"]
login["request"]["schema"]["user_id"] = "same 8-character [a-z0-9]{8} value used for account/get_rand"
login_notes = login.get("implementation_notes", []) + [
    "Reuse the exact user_id from the successful account/get_rand challenge request.",
    "The documented 0..6 result-code mapping applies to account/login; do not generalize it to account/get_rand.result.",
]
login["implementation_notes"] = list(dict.fromkeys(login_notes))

retry = by_id["account/get_retrytimes_and_time"]
retry_notes = retry.get("implementation_notes", []) + [
    "Recommended pre-login lockout guard: if remain_time > 0, wait; if retry_times <= 1, abort rather than consume the final password attempt.",
]
retry["implementation_notes"] = list(dict.fromkeys(retry_notes))

PATH.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Normalized administrator login compatibility fields.")
