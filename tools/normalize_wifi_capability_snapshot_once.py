# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in doc["methods"]}

ap = by_id["wireless/wifi_get_ap_config"]
contracts = [
    c for c in ap.get("semantic_contracts", [])
    if not (isinstance(c, dict) and c.get("id") == "wifi.runtime_capability_snapshot.2026_08_31")
]
contracts.append({
    "id": "wifi.runtime_capability_snapshot.2026_08_31",
    "evidence": "LIVE_PHYSICAL_SDK_READ",
    "firmware": "V1.00(ACIY.3)C0",
    "management": "USB via http://zyxel.home",
    "observed": {
        "mode": "DUAL",
        "switch": "on",
        "maxassoc": "32",
        "power_level": "1",
        "wifi_if_24G": {
            "channel": "0",
            "cur_channel": "6",
            "first_channel": "1",
            "last_channel": "13",
            "bandwidth": "HT20/HT40",
            "net_mode": "11bgnax",
            "hidden": "0",
            "isolate": "0",
        },
        "wifi_if_5G": {
            "channel": "0",
            "cur_channel": "44",
            "channel_list": {
                "indoor": "36 40 44 48",
                "indoor_or_dfs": "52 56 60 64",
                "dfs": "100 104 108 112 116 120 124 128 132 136 140",
            },
            "bandwidth": "HT20/HT40/HT80",
            "net_mode": "11anacax",
            "hidden": "0",
            "isolate": "0",
        },
        "wifi_if_GUEST": {"band_mode": "2.4G", "maxassoc": "10", "hidden": "0"},
        "wifi_timed_off": {
            "enable": 0,
            "start_hour": 0,
            "start_minute": 0,
            "end_hour": 0,
            "end_minute": 0,
        },
    },
    "scope": "Observed runtime values, not universal allowed-value enums.",
})
ap["semantic_contracts"] = contracts
ap["implementation_notes"] = list(dict.fromkeys(ap.get("implementation_notes", []) + [
    "2026-08-31 physical SDK capability snapshot observed 2.4-GHz auto channel=0 with live channel 6 and first/last channel 1..13; 5-GHz auto channel=0 with live channel 44 and explicit indoor/DFS channel lists.",
    "Observed bandwidth/net_mode/power_level values are runtime observations only; do not infer complete allowed-value sets from the getter alone.",
]))

status = by_id["wireless/wifi_get_timed_off_status"]
status_contracts = [
    c for c in status.get("semantic_contracts", [])
    if not (isinstance(c, dict) and c.get("id") == "wifi.timed_off_status_not_enable.v1")
]
status_contracts.append({
    "id": "wifi.timed_off_status_not_enable.v1",
    "evidence": "LIVE_SIMULTANEOUS_READ_2026_08_31",
    "observation": {
        "wifi_get_ap_config.config.wifi_timed_off.enable": 0,
        "wifi_get_timed_off_status.status": "on",
        "wifi_get_timed_off_status.result": 0,
    },
    "constraint": "status='on' must not be documented as equivalent to timed-off schedule enable=1.",
    "meaning": "UNRESOLVED_BEYOND_NON_EQUIVALENCE",
})
status["semantic_contracts"] = status_contracts
status["implementation_notes"] = list(dict.fromkeys(status.get("implementation_notes", []) + [
    "2026-08-31: status='on' was returned while wifi_timed_off.enable=0 in the simultaneous AP-config read. Therefore status is not a direct schedule-enabled flag; its exact positive-state meaning remains unresolved.",
]))

METHODS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
needle = "### Notes\n\n- 2026-08-31 public-SDK physical test: Guest toggle"
insert = (
    "### Notes\n\n"
    "- 2026-08-31 sanitized physical SDK capability snapshot: 2.4 GHz reported configured channel `0` (auto), live channel `6`, first/last `1..13`, bandwidth `HT20/HT40`, net mode `11bgnax`; 5 GHz reported configured channel `0`, live channel `44`, explicit indoor/DFS channel lists, bandwidth `HT20/HT40/HT80`, net mode `11anacax`. These are observed runtime values, not complete allowed-value enums.\n"
    "- The same snapshot reported top-level `maxassoc=32`, `power_level=1`, `switch=on`, with 2.4/5 GHz `hidden=0` and `isolate=0`.\n"
    "- 2026-08-31 public-SDK physical test: Guest toggle"
)
if needle in wireless:
    wireless = wireless.replace(needle, insert, 1)

status_anchor = "## `wifi_get_timed_off_status`"
idx = wireless.find(status_anchor)
if idx >= 0:
    next_idx = wireless.find("\n<a id=", idx + len(status_anchor))
    block_end = next_idx if next_idx >= 0 else len(wireless)
    block = wireless[idx:block_end]
    note = "\n### Notes\n\n- 2026-08-31 simultaneous physical read returned `status=\"on\"` while `wifi_get_ap_config.config.wifi_timed_off.enable=0`. Therefore `status` is not equivalent to the schedule-enable flag; exact semantics remain unresolved.\n"
    if "not equivalent to the schedule-enable flag" not in block:
        wireless = wireless[:block_end].rstrip() + note + "\n" + wireless[block_end:].lstrip("\n")

WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- recorded the 2026-08-31 sanitized physical Wi-Fi capability snapshot, including runtime channel/range lists and the finding that `wifi_get_timed_off_status.status=on` can coexist with `wifi_timed_off.enable=0`; the status field is therefore not a direct schedule-enable flag\n"
if entry not in changelog:
    marker = "Development metadata: `0.1.1.dev0`.\n\n"
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical Wi-Fi capability snapshot evidence.")
