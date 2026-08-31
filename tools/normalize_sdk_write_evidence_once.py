# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
CM = Path("api/cm.md")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")


def add_unique_note(method: dict, note: str) -> None:
    notes = method.setdefault("implementation_notes", [])
    if note not in notes:
        notes.append(note)


def add_unique_contract(method: dict, contract: dict) -> None:
    contracts = method.setdefault("semantic_contracts", [])
    cid = contract.get("id")
    contracts[:] = [
        item for item in contracts
        if not (isinstance(item, dict) and item.get("id") == cid)
    ]
    contracts.append(contract)


doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in doc["methods"]}

mobile = by_id["cm/set_network_settings"]
mobile["auth_evidence"] = "ADMIN_OK"
add_unique_contract(
    mobile,
    {
        "id": "cm.set_network_settings.sdk_restore.v1",
        "evidence": "LIVE_SDK_PHYSICAL_2026_08_31",
        "firmware": "V1.00(ACIY.3)C0",
        "host": "http://zyxel.home",
        "verified_fields": ["data_roaming", "network_mode"],
        "lifecycle": "read current -> write alternate value -> exact read-back -> restore original -> exact read-back",
        "auth": "normal administrator session",
    },
)
add_unique_note(
    mobile,
    "2026-08-31 public-SDK physical test: normal admin changed data_roaming and one router-reported alternative network_mode, exact-read-back verified both writes, then restored both original values successfully via http://zyxel.home.",
)

for method_id, summary in (
    (
        "wireless/wifi_set_wps_disable",
        "2026-08-31 public-SDK physical test: normal admin toggled WPS, exact-read-back verified the change, then restored and verified the original state via http://zyxel.home.",
    ),
    (
        "wireless/wifi_set_ap_config",
        "2026-08-31 public-SDK physical test: normal admin toggled Guest state and combined/separate main-SSID mode, verified preservation of the other mode dimension after each write, then restored and verified the original state via http://zyxel.home.",
    ),
):
    method = by_id[method_id]
    add_unique_contract(
        method,
        {
            "id": method_id.replace("/", ".") + ".sdk_restore.v1",
            "evidence": "LIVE_SDK_PHYSICAL_2026_08_31",
            "firmware": "V1.00(ACIY.3)C0",
            "host": "http://zyxel.home",
            "lifecycle": "write -> exact read-back -> restore original -> exact read-back",
            "auth": "normal administrator session",
        },
    )
    add_unique_note(method, summary)

METHODS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

cm = CM.read_text(encoding="utf-8")
cm = cm.replace(
    "| [`set_network_settings`](#set-network-settings) | `LIVE_VERIFIED` | `UNTESTED` | `WRITE_OR_SIDE_EFFECT` |",
    "| [`set_network_settings`](#set-network-settings) | `LIVE_VERIFIED` | `ADMIN_OK` | `WRITE_OR_SIDE_EFFECT` |",
)
anchor = "**Method ID:** `cm/set_network_settings`"
pos = cm.index(anchor)
section_end = cm.find("\n<a id=", pos)
if section_end == -1:
    section_end = len(cm)
section = cm[pos:section_end]
section = section.replace("**Auth evidence:** `UNTESTED`", "**Auth evidence:** `ADMIN_OK`")
note = "- 2026-08-31 public-SDK physical test: normal admin changed data_roaming and one router-reported alternative network_mode, exact-read-back verified both writes, then restored both original values successfully via `http://zyxel.home`.\n"
if note not in section:
    notes_marker = "### Notes\n\n"
    if notes_marker in section:
        section = section.replace(notes_marker, notes_marker + note, 1)
    else:
        section = section.rstrip() + "\n\n### Notes\n\n" + note
cm = cm[:pos] + section + cm[section_end:]
CM.write_text(cm, encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
for anchor, note in (
    (
        "**Method ID:** `wireless/wifi_set_ap_config`",
        "- 2026-08-31 public-SDK physical test: Guest toggle and combined/separate mode transition both passed exact read-back and full original-state restore through normal admin via `http://zyxel.home`.\n",
    ),
    (
        "**Method ID:** `wireless/wifi_set_wps_disable`",
        "- 2026-08-31 public-SDK physical test: WPS toggle passed exact read-back and original-state restore through normal admin via `http://zyxel.home`.\n",
    ),
):
    pos = wireless.index(anchor)
    section_end = wireless.find("\n<a id=", pos)
    if section_end == -1:
        section_end = len(wireless)
    section = wireless[pos:section_end]
    if note not in section:
        notes_marker = "### Notes\n\n"
        if notes_marker in section:
            section = section.replace(notes_marker, notes_marker + note, 1)
        else:
            section = section.rstrip() + "\n\n### Notes\n\n" + note
    wireless = wireless[:pos] + section + wireless[section_end:]
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
bullet = "- recorded the 2026-08-31 public-SDK physical reversible-write pass: normal-admin data-roaming/network-mode, WPS and Wi-Fi Guest/combined-separate transitions all succeeded with exact read-back and original-state restore; `cm/set_network_settings` auth evidence is now `ADMIN_OK`\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if bullet not in changelog:
    changelog = changelog.replace(marker, marker + bullet, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical SDK reversible-write evidence.")
