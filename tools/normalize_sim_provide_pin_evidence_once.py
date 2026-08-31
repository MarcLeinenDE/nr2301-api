# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SIM_DOC = Path("api/sim.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}

contract_id = "sim.provide_pin.after_reboot.live_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_REBOOT_PIN_REQUIRED_PROVIDE_RESTORE_2026_08_31",
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
        {"method": "router/router_call_reboot", "management_outage": "CONFIRMED", "outage_probe": 16},
        {"event": "management_recovery", "login_attempt": 27},
        {"event": "sim_state_stable", "poll_attempt": 9, "pin_status": 2, "pin_enabled": 1},
        {"method": "sim/provide_pin", "setting_response": "OK", "pin_status_after": 5, "pin_enabled_after": 1},
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
    "retry_result": "No PIN or PUK retry was consumed by the known-correct provide_pin operation or surrounding enable/disable operations.",
    "reboot_timing": "The reboot action interrupted its request before shutdown; physical validation therefore required a confirmed management outage before accepting recovery login and a stable SIM state before provide_pin.",
    "secret_handling": "The real SIM PIN remained a local environment secret and was never logged, stored or published.",
}

method = by_id["sim/provide_pin"]
method["verification"] = "LIVE_VERIFIED"
method["auth_evidence"] = "ADMIN_OK"
existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
method["semantic_contracts"] = existing + [contract]
method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
    "2026-08-31 physical SDK lifecycle enabled PIN protection, confirmed a real reboot outage, waited for stable post-reboot pin_status=2, submitted the known-correct PIN once via provide_pin, read back pin_status=5, and restored pin_enabled=0.",
    "provide_pin returned response.setting_response='OK'; pin_attempts remained 3 and puk_attempts remained 10 throughout.",
    "A reboot-call transport interruption alone is not recovery evidence on ACIY.3; the tested router can remain reachable for several seconds before shutdown begins."
]))
METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sim = SIM_DOC.read_text(encoding="utf-8")
sim = sim.replace("| [`provide_pin`](#provide-pin) | `STATIC_CONFIRMED` | `UNTESTED` |", "| [`provide_pin`](#provide-pin) | `LIVE_VERIFIED` | `ADMIN_OK` |")
marker = "## `provide_pin`"
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
        "> [!CAUTION]\n> This remains a retry-sensitive SIM credential operation. Live verification used one known-correct local PIN only after a real reboot produced stable `pin_status=2`, with retry counters checked before/after and the original PIN-protection state restored. Never probe with guessed credentials.\n\n",
    )
    note = "\n### Physical evidence — 2026-08-31\n\nOn ACIY.3, a guarded SDK lifecycle enabled PIN protection, triggered `router_call_reboot`, confirmed an actual management outage, recovered administrator login, waited for the SIM subsystem to stabilize at `pin_status=2`, then submitted the known-correct local PIN exactly once. `provide_pin` returned `response.setting_response=\"OK\"`, read-back changed to `pin_status=5`, and the test restored `pin_enabled=0`. `pin_attempts` remained 3 and `puk_attempts` remained 10 throughout. The real PIN was never logged or published.\n\nThe reboot action can interrupt its HTTP request several seconds before physical shutdown begins, so an immediately successful login is not sufficient reboot-recovery evidence. Consumers performing lifecycle tests should require an actual management outage and stable post-reboot SIM state.\n"
    if "waited for the SIM subsystem to stabilize" not in block:
        block = block.rstrip() + "\n" + note
    sim = sim[:start] + block + sim[end:]
SIM_DOC.write_text(sim, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- live-verified `sim/provide_pin` in its real post-reboot PIN-required lifecycle: after enabling PIN protection and confirming a true management outage/recovery, the SIM stabilized at `pin_status=2`, one known-correct local PIN returned `response.setting_response=OK`, read-back changed to `pin_status=5`, retry counters stayed at 3/10, and PIN protection was restored to disabled\n"
changelog_marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and changelog_marker in changelog:
    changelog = changelog.replace(changelog_marker, changelog_marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical SIM provide-PIN evidence.")
