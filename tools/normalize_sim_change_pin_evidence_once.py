# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SIM_DOC = Path("api/sim.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}

contract_id = "sim.change_pin.live_2026_08_31.v1"
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
        {"method": "sim/change_pin", "direction": "original_to_temporary", "setting_response": "OK", "pin_enabled_after": 1},
        {"method": "sim/change_pin", "direction": "temporary_to_original", "setting_response": "OK", "pin_enabled_after": 1},
        {"method": "sim/disable_pin", "setting_response": "OK", "pin_enabled_after": 0},
    ],
    "final_state": {
        "sim_status": 1,
        "pin_status": 5,
        "pin_enabled": 0,
        "pin_attempts": 3,
        "puk_attempts": 10,
    },
    "response_shape": "response.setting_response",
    "retry_result": "No PIN or PUK retry was consumed by either known-correct change_pin operation or the surrounding enable/disable operations.",
    "secret_handling": "Original and temporary SIM PIN values remained local environment secrets and were never logged, stored or published.",
}

method = by_id["sim/change_pin"]
method["verification"] = "LIVE_VERIFIED"
method["auth_evidence"] = "ADMIN_OK"
existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
method["semantic_contracts"] = existing + [contract]
method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
    "2026-08-31 known-correct physical SDK sequence changed the active PIN to a temporary local PIN and back to the original PIN; both writes returned response.setting_response='OK'.",
    "pin_attempts remained 3 and puk_attempts remained 10 throughout; the PIN-protection state was restored to disabled.",
    "Neither original nor temporary PIN was logged or published."
]))
METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sim = SIM_DOC.read_text(encoding="utf-8")
sim = sim.replace("| [`change_pin`](#change-pin) | `STATIC_CONFIRMED` | `UNTESTED` |", "| [`change_pin`](#change-pin) | `LIVE_VERIFIED` | `ADMIN_OK` |")
marker = "## `change_pin`"
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
        "> [!CAUTION]\n> This remains a retry-sensitive SIM mutation. Live verification used known-correct original and temporary PIN values, checked retry counters, and restored the original PIN plus PIN-protection state. Never probe with guessed credentials.\n\n",
    )
    note = "\n### Physical evidence — 2026-08-31\n\nOn ACIY.3, a guarded SDK sequence enabled PIN protection, changed the known-correct original PIN to a temporary local PIN, changed it back to the original PIN, and disabled PIN protection again. Both `change_pin` calls returned `response.setting_response=\"OK\"`; `pin_attempts` stayed at 3 and `puk_attempts` at 10 throughout. No real PIN value was logged or published.\n"
    if "Both `change_pin` calls returned" not in block:
        block = block.rstrip() + "\n" + note
    sim = sim[:start] + block + sim[end:]
SIM_DOC.write_text(sim, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- live-verified `sim/change_pin` with a known-correct original PIN and temporary local PIN: original -> temporary -> original returned `response.setting_response=OK` both times, PIN protection was restored to disabled, and retry counters remained unchanged at 3/10\n"
changelog_marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and changelog_marker in changelog:
    changelog = changelog.replace(changelog_marker, changelog_marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical SIM change-PIN evidence.")
