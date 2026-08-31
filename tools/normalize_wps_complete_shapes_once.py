# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}

old_id = "wps.action_response_envelopes.2026_08_31.v1"
contract_id = "wps.action_response_envelopes.complete_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "physical_test_result": "1 passed in 1.44s",
    "observed": {
        "wireless/wifi_call_wps_pbc": {
            "request": "GET",
            "response_envelope": "wireless",
            "result_field": "wps_call_pbc_result",
            "result_value": "OK"
        },
        "wireless/wifi_call_wps_cancel": {
            "request": "GET",
            "response_envelope": "top_level",
            "result_field": "wps_call_cancel_result",
            "result_value": "OK",
            "observed_after": ["PBC", "PIN"]
        },
        "wireless/wifi_call_wps_pin": {
            "request": "POST",
            "request_payload": {"wps_enable": "1", "wps_pin": "12345670"},
            "response_envelope": "wireless",
            "result_field": "wps_call_pin_result",
            "result_value": "OK"
        }
    },
    "sequence": [
        "PBC -> nested wireless OK",
        "Cancel -> top-level OK",
        "PIN 12345670 -> nested wireless OK",
        "Cancel -> top-level OK"
    ],
    "restore": "The physical integration test restored the original WPS enable state in finally; the run completed without a restore exception.",
    "scope": "Action-specific response envelopes are physically qualified for ACIY.3; do not assume a uniform wrapper across WPS actions."
}

for method_id in (
    "wireless/wifi_call_wps_pbc",
    "wireless/wifi_call_wps_pin",
    "wireless/wifi_call_wps_cancel",
):
    method = by_id[method_id]
    contracts = [
        c for c in method.get("semantic_contracts", [])
        if not (isinstance(c, dict) and c.get("id") in {old_id, contract_id})
    ]
    contracts.append(contract)
    method["semantic_contracts"] = contracts

notes = {
    "wireless/wifi_call_wps_pbc": "2026-08-31 completed physical SDK test: PBC returned nested wireless.wps_call_pbc_result='OK', followed immediately by successful flat Cancel.",
    "wireless/wifi_call_wps_pin": "2026-08-31 completed physical SDK test: POST {wps_enable:'1', wps_pin:'12345670'} returned nested wireless.wps_call_pin_result='OK', followed immediately by successful flat Cancel.",
    "wireless/wifi_call_wps_cancel": "2026-08-31 completed physical SDK test: Cancel returned top-level wps_call_cancel_result='OK' after both PBC and PIN actions."
}
for method_id, note in notes.items():
    method = by_id[method_id]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [note]))

METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sem = json.loads(SEMANTICS.read_text(encoding="utf-8"))
sem.setdefault("mappings", {})["wireless/wps_action_response_envelopes"] = contract
SEMANTICS.write_text(json.dumps(sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
old_pin = """### Response\n\nKnown/observed response fields: `wireless`.\n\n### Notes\n\n- POST wps_enable='1', wps_pin='12345670' returned wireless.wps_call_pin_result='OK'; immediately cancelled.\n"""
new_pin = """### Response\n\nPhysical ACIY.3 SDK evidence on 2026-08-31 returned the PIN action result nested under `wireless`:\n\n```json\n{\n  \"wireless\": {\n    \"wps_call_pin_result\": \"OK\"\n  }\n}\n```\n\n### Notes\n\n- POST `wps_enable='1'`, `wps_pin='12345670'` returned `wireless.wps_call_pin_result='OK'`; the same physical test immediately called Cancel, which returned flat top-level `wps_call_cancel_result='OK'`.\n"""
if old_pin in wireless:
    wireless = wireless.replace(old_pin, new_pin, 1)

summary = """
### Complete physical WPS action sequence — 2026-08-31

The public SDK physical integration test completed successfully in **1.44 s** with the original WPS-enable state restored:

```text
PBC              -> wireless.wps_call_pbc_result = OK
Cancel after PBC -> top-level wps_call_cancel_result = OK
PIN 12345670     -> wireless.wps_call_pin_result = OK
Cancel after PIN -> top-level wps_call_cancel_result = OK
```

This confirms that ACIY.3 uses **action-specific response envelopes**: PBC and PIN are nested under `wireless`, while Cancel is flat at the top level. Consumers must not impose one uniform WPS response wrapper.
"""
if "### Complete physical WPS action sequence — 2026-08-31" not in wireless:
    insert_at = wireless.find("<a id=\"wifi-get-ap-config\"></a>")
    if insert_at >= 0:
        wireless = wireless[:insert_at] + summary.strip() + "\n\n" + wireless[insert_at:]
    else:
        wireless = wireless.rstrip() + "\n\n" + summary.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
marker = "Development metadata: `0.1.1.dev0`.\n\n"
entry = "- completed the physical WPS action contract on 2026-08-31: PBC and PIN return nested `wireless.*_result=OK`, while Cancel returns flat top-level `wps_call_cancel_result=OK` after both actions; the public SDK integration test passed in 1.44 s and restored the original WPS-enable state\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized complete physical WPS action response envelopes.")
