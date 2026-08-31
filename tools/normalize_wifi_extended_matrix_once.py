# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in doc["methods"]}

contract_id = "wifi.sdk_physical_extended_matrix_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "admin_session": True,
    "result": "18/18 extended physical integration cases passed; every changed configuration value was read back and restored",
    "verified_capabilities": {
        "power_level": {
            "live_roundtrip_values": ["0", "1", "2"],
            "original_value": "1",
            "exhaustive": False,
            "semantic_meaning": "unresolved raw values; do not label as percentages or regional power classes without separate evidence"
        },
        "maxassoc": {"verified_transitions": [["32", "1", "32"], ["32", "31", "32"]]},
        "wifi_if_GUEST.maxassoc": {"verified_values": ["1", "9", "10"], "frontend_range": "1..10"},
        "wifi_if_GUEST.band_mode": {"verified_values": ["2.4G", "5G"]},
        "ssid_write": {
            "verified_sections": ["wifi_if_24G", "wifi_if_5G", "wifi_if_DUAL", "wifi_if_GUEST"],
            "test_values": "synthetic only; original/live SSIDs not published"
        },
        "wifi_if_24G.channel": {"live_values": ["1", "13"], "auto_value": "0"},
        "wifi_if_5G.channel": {"live_values": ["36", "52", "100", "140"], "auto_value": "0"},
        "wifi_if_24G.net_mode": {"all_original_webui_values_live": ["11b", "11bg", "11bgn", "11bgnax"]},
        "wifi_if_5G.net_mode": {"all_original_webui_values_live": ["11a", "11an", "11anac", "11anacax"]},
        "wifi_if_24G.bandwidth": {"all_original_webui_values_live": ["HT20/HT40", "HT20", "HT40"]},
        "wifi_if_5G.bandwidth": {"all_original_webui_values_live": ["HT20/HT40/HT80", "HT20", "HT40", "HT80"]}
    },
    "dfs_note": "Configured-channel persistence was verified. DFS/CAC operating-channel timing was intentionally not conflated with setter persistence.",
    "jurisdiction_note": "These are technical firmware/API capabilities, not a claim of legal use in every jurisdiction."
}

for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    method = by_id[method_id]
    existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    method["semantic_contracts"] = existing + [contract]
    notes = method.get("implementation_notes", []) + [
        "2026-08-31 extended public-SDK Wi-Fi matrix passed 18/18 physical cases with read-back and restore, including power_level 0/1/2, Guest band_mode 2.4G/5G, synthetic SSID writes, additional channel categories and every original-WebUI net-mode/bandwidth token.",
        "power_level raw values 0, 1 and 2 are live round-trippable on ACIY.3, but their human meaning and whether the enum is exhaustive remain unresolved.",
        "Synthetic SSID writes were verified for 24G, 5G, DUAL and Guest; no live SSID values are published."
    ]
    method["implementation_notes"] = list(dict.fromkeys(notes))

scan = by_id["wireless/wifi_scan"]
scan["auth_evidence"] = "ADMIN_OK"
scan["implementation_notes"] = list(dict.fromkeys(scan.get("implementation_notes", []) + [
    "2026-08-31 public-SDK authenticated scan completed successfully with normal administrator authentication; scan-list contents were intentionally not logged because they can contain nearby SSIDs/BSSIDs."
]))

METHODS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
wireless = wireless.replace("| [`wifi_scan`](#wifi-scan) | `LIVE_VERIFIED` | `UNTESTED` |", "| [`wifi_scan`](#wifi-scan) | `LIVE_VERIFIED` | `ADMIN_OK` |")
wireless = wireless.replace("**Auth evidence:** `UNTESTED`", "**Auth evidence:** `ADMIN_OK`", 1 if "## `wifi_scan`" in wireless else 0)
block = """
## Extended physical SDK Wi-Fi matrix — 2026-08-31

The second dedicated-router matrix completed **18/18 cases in 226.96 s**, again using normal administrator authentication through `http://zyxel.home` and restoring every changed configuration value.

Additional live evidence:

```text
power_level:              1 -> 0 -> 1, then 1 -> 2 -> 1
Global maxassoc:          32 -> 1 -> 32
Guest maxassoc:           10 -> 1 -> 10
Guest band_mode:          2.4G -> 5G -> 2.4G
SSID writes:              synthetic values accepted/restored for 24G, 5G, DUAL, Guest
2.4 GHz channel:          0 -> 13 -> 0
5 GHz channels:           0 -> 52 -> 0; 0 -> 100 -> 0; 0 -> 140 -> 0
24G net_mode:             all 11b / 11bg / 11bgn / 11bgnax values accepted
5G net_mode:              all 11a / 11an / 11anac / 11anacax values accepted
24G bandwidth:            all HT20/HT40 / HT20 / HT40 values accepted
5G bandwidth:             all HT20/HT40/HT80 / HT20 / HT40 / HT80 values accepted
wifi_scan:                normal-admin authenticated call succeeded
```

`power_level` values `0`, `1` and `2` are therefore proven round-trippable raw values on ACIY.3. Their human meaning and whether additional values exist remain unresolved; do not label them as percentages or regulatory classes without separate evidence.

For DFS-class channel tests the configured `channel` read-back was the contract being verified. DFS/CAC timing and the eventual `cur_channel` were deliberately not treated as the same property.
"""
if "## Extended physical SDK Wi-Fi matrix — 2026-08-31" not in wireless:
    wireless = wireless.rstrip() + "\n\n" + block.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- recorded the second 2026-08-31 public-SDK Wi-Fi matrix: 18/18 cases passed, adding live power_level 0/1/2 round-trips, Guest 2.4G/5G band mode, synthetic SSID writes, channels 13/52/100/140, every known WebUI net-mode/bandwidth option and normal-admin wifi_scan authentication\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized 2026-08-31 extended Wi-Fi physical matrix.")
