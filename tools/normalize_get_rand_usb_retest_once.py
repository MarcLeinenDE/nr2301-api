# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

PATH = Path("specification/methods.json")
doc = json.loads(PATH.read_text(encoding="utf-8"))
by_id = {method["method_id"]: method for method in doc["methods"]}

get_rand = by_id["account/get_rand"]
get_rand["request"]["schema"]["user_id"] = (
    "historically live-working shape: 8 lowercase alphanumeric characters matching [a-z0-9]{8}; "
    "current 2026-08-31 USB retest still returns result=4 with this shape"
)
get_rand["request"]["basis"] = (
    "historical live-working application evidence + 2026-08-31 physical USB retest"
)

contracts = [
    c for c in get_rand.get("semantic_contracts", [])
    if not (isinstance(c, dict) and c.get("id") in {
        "account.login_user_id.compat.v1",
        "account.get_rand_result4.usb_retest.v1",
    })
]
contracts.append({
    "id": "account.login_user_id.compat.v1",
    "evidence": "HISTORICAL_LIVE_VERIFIED_CLIENT",
    "field": "user_id",
    "known_working_shape": "[a-z0-9]{8}",
    "reuse": "reuse the same user_id in the subsequent account/login request",
    "current_retest_note": (
        "The historical shape remains proven working evidence, but the 2026-08-31 USB retest "
        "also returned account/get_rand result=4 with this shape; user-id length is therefore "
        "not established as the cause of the current failure."
    ),
})
contracts.append({
    "id": "account.get_rand_result4.usb_retest.v1",
    "evidence": "LIVE_REPRODUCED_2026_08_31",
    "field": "result",
    "value": 4,
    "context": "physical USB SDK pre-auth smoke before password submission",
    "reproduced_with_user_id_shapes": ["32-character hexadecimal", "[a-z0-9]{8}"],
    "meaning": "UNRESOLVED_ENDPOINT_SPECIFIC",
    "constraint": "Do not apply the account/login result-code table to this get_rand result without separate evidence.",
})
get_rand["semantic_contracts"] = contracts

notes = [
    n for n in get_rand.get("implementation_notes", [])
    if "32-character hexadecimal" not in n and "Use [a-z0-9]{8}" not in n
]
notes.extend([
    "Historical live-working NR2301 clients used exactly eight lowercase alphanumeric characters for user_id.",
    "On 2026-08-31 the physical USB SDK smoke returned result=4 before password submission with both the initial 32-character hexadecimal user_id and the corrected historical [a-z0-9]{8} user_id.",
    "The current result=4 cannot be attributed to user-id length alone; its account/get_rand meaning/cause remains unresolved.",
    "Compare the exact historically working transport/request behavior before changing further authentication semantics.",
])
get_rand["implementation_notes"] = list(dict.fromkeys(notes))

login = by_id["account/login"]
login["request"]["schema"]["user_id"] = (
    "same user_id used for account/get_rand; historical live-working clients used [a-z0-9]{8}"
)
login_notes = login.get("implementation_notes", []) + [
    "The documented 0..6 result-code mapping applies to account/login; do not generalize it to account/get_rand.result.",
]
login["implementation_notes"] = list(dict.fromkeys(login_notes))

PATH.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Normalized 2026-08-31 get_rand physical USB retest evidence.")
