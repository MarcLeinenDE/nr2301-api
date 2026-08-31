# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SIM_DOC = Path("api/sim.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}

contract_id = "sim.pin_protection_toggle.live_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "admin_session": True,
    "initial_state": {
        "sim_status": 1,
        "pin_status": 5,
        "pin_enabled": 0,
        "pin_attempts": 3,
        "puk_attempts": 10,
    },
    "sequence": [
        {"method": "sim/enable_pin", "setting_response": "OK", "pin_enabled_after": 1},
        {"method": "sim/disable_pin", "setting_response": "OK", "pin_enabled_after": 0},
    ],
    "final_state": {
        "sim_status": 1,
        "pin_status": 5,
        "pin_enabled": 0,
        "pin_attempts": 3,
        "puk_attempts": 10,
    },
    "retry_result": "No PIN or PUK retry was consumed by either known-correct credential operation.",
    "secret_handling": "The real SIM PIN remained local and was not logged, stored or published.",
}

for method_id in ("sim/enable_pin", "sim/disable_pin"):
    method = by_id[method_id]
    method["verification"] = "LIVE_VERIFIED"
    method["auth_evidence"] = "ADMIN_OK"
    existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    method["semantic_contracts"] = existing + [contract]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        "2026-08-31 known-correct physical SDK sequence verified PIN protection 0->1->0 with response.setting_response='OK' for both enable_pin and disable_pin.",
        "pin_attempts remained 3 and puk_attempts remained 10 across the complete enable/read-back/disable/read-back sequence.",
        "The real SIM PIN was supplied only from the local test environment and was not published."
    ]))

METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sim = SIM_DOC.read_text(encoding="utf-8")
for short in ("enable_pin", "disable_pin"):
    sim = sim.replace(f"| [`{short}`](#{short.replace('_','-')}) | `STATIC_CONFIRMED` | `UNTESTED` |", f"| [`{short}`](#{short.replace('_','-')}) | `LIVE_VERIFIED` | `ADMIN_OK` |")

for short in ("enable_pin", "disable_pin"):
    marker = f"## `{short}`"
    start = sim.find(marker)
    if start >= 0:
        end = sim.find("\n<a id=", start + len(marker))
        if end < 0:
            end = len(sim)
        block = sim[start:end]
        block = block.replace("**Verification:** `STATIC_CONFIRMED`", "**Verification:** `LIVE_VERIFIED`")
        block = block.replace("**Auth evidence:** `UNTESTED`", "**Auth evidence:** `ADMIN_OK`")
        block = block.replace(
            "> [!CAUTION]\n> This method was deliberately not exercised merely to improve coverage because its potential impact outweighed the documentation value. Treat the contract as static evidence only.\n\n",
            "> [!CAUTION]\n> This remains a retry-sensitive SIM mutation. Live verification used a known-correct local PIN, checked retry counters before the write, and restored the original PIN-protection state. Never probe with guessed credentials.\n\n",
        )
        note = "\n### Physical evidence — 2026-08-31\n\nOn ACIY.3, a guarded SDK sequence started from `pin_enabled=0`, returned `response.setting_response=\"OK\"`, read back `pin_enabled=1`, then restored with the complementary action to `pin_enabled=0`. `pin_attempts` remained 3 and `puk_attempts` remained 10 throughout. The actual PIN was never logged or published.\n"
        if "### Physical evidence — 2026-08-31" not in block:
            block = block.rstrip() + "\n" + note
        sim = sim[:start] + block + sim[end:]

SIM_DOC.write_text(sim, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- live-verified `sim/enable_pin` and `sim/disable_pin` with a known-correct locally supplied PIN: `pin_enabled` round-tripped 0 -> 1 -> 0, both writes returned `response.setting_response=OK`, and PIN/PUK retry counters remained unchanged at 3/10\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical SIM PIN protection toggle evidence.")
