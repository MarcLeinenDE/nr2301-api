# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

methods = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods["methods"]}

contract_id = "wps.action_response_envelopes.2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "observed": {
        "wireless/wifi_call_wps_pbc": {
            "response_envelope": "wireless",
            "result_field": "wps_call_pbc_result",
            "result_value": "OK",
        },
        "wireless/wifi_call_wps_cancel": {
            "response_envelope": "top_level",
            "result_field": "wps_call_cancel_result",
            "result_value": "OK",
        },
    },
    "scope": "Physical SDK run on 2026-08-31. PIN response envelope was not reached in this run because the pre-fix SDK rejected the successful flat Cancel response before the PIN step.",
}

for method_id in ("wireless/wifi_call_wps_pbc", "wireless/wifi_call_wps_cancel"):
    method = by_id[method_id]
    contracts = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    contracts.append(contract)
    method["semantic_contracts"] = contracts

pbc = by_id["wireless/wifi_call_wps_pbc"]
pbc["implementation_notes"] = list(dict.fromkeys(pbc.get("implementation_notes", []) + [
    "2026-08-31 physical SDK run: PBC returned wireless.wps_call_pbc_result='OK' in a nested wireless response envelope."
]))

cancel = by_id["wireless/wifi_call_wps_cancel"]
cancel["implementation_notes"] = list(dict.fromkeys(cancel.get("implementation_notes", []) + [
    "2026-08-31 physical SDK run: Cancel returned top-level wps_call_cancel_result='OK' as {\"wps_call_cancel_result\":\"OK\"}; do not require a wireless wrapper for this action on ACIY.3."
]))

METHODS.write_text(json.dumps(methods, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sem = json.loads(SEMANTICS.read_text(encoding="utf-8"))
sem.setdefault("mappings", {})["wireless/wps_action_response_envelopes"] = contract
SEMANTICS.write_text(json.dumps(sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
pbc_old = """### Response\n\nKnown/observed response fields: `wireless`.\n\n### Notes\n\n- GET returned wireless.wps_call_pbc_result='OK'; immediately cancelled in test.\n"""
pbc_new = """### Response\n\nPhysical ACIY.3 SDK evidence on 2026-08-31 returned the action result nested under `wireless`:\n\n```json\n{\n  \"wireless\": {\n    \"wps_call_pbc_result\": \"OK\"\n  }\n}\n```\n\n### Notes\n\n- GET returned `wireless.wps_call_pbc_result='OK'`; the same physical run then called Cancel immediately.\n"""
if pbc_old in wireless:
    wireless = wireless.replace(pbc_old, pbc_new, 1)

cancel_old = """### Response\n\nKnown/observed response fields: `wireless`.\n\n### Notes\n\n- GET returned wps_call_cancel_result='OK' after both PBC and PIN tests.\n"""
cancel_new = """### Response\n\nPhysical ACIY.3 SDK evidence on 2026-08-31 returned the Cancel result directly at the top level:\n\n```json\n{\n  \"wps_call_cancel_result\": \"OK\"\n}\n```\n\nDo not require a `wireless` wrapper for this action on the tested firmware.\n\n### Notes\n\n- The earlier live observation that Cancel returned `wps_call_cancel_result='OK'` is now shape-qualified by the 2026-08-31 SDK run: the field is top-level.\n"""
if cancel_old in wireless:
    wireless = wireless.replace(cancel_old, cancel_new, 1)
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
marker = "Development metadata: `0.1.1.dev0`.\n\n"
entry = "- recorded action-specific WPS response envelopes from the 2026-08-31 physical SDK run: PBC returned `wireless.wps_call_pbc_result=OK`, while Cancel returned flat top-level `wps_call_cancel_result=OK`; PIN envelope remains to be observed in the resumed run\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Recorded physical WPS PBC/Cancel response envelopes.")
