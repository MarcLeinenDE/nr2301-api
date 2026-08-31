# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in doc["methods"]}

contract_id = "wifi.sdk_physical_field_matrix_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "admin_session": True,
    "result": "15/15 physical integration cases passed; every changed value was read back and the original state restored",
    "verified_transitions": {
        "wifi_if_24G.channel": ["0", "1", "0"],
        "wifi_if_5G.channel": ["0", "36", "0"],
        "wifi_if_24G.hidden": ["0", "1", "0"],
        "wifi_if_5G.hidden": ["0", "1", "0"],
        "wifi_if_DUAL.hidden": ["0", "1", "0"],
        "wifi_if_GUEST.hidden": ["0", "1", "0"],
        "wifi_if_24G.isolate": ["0", "1", "0"],
        "wifi_if_5G.isolate": ["0", "1", "0"],
        "maxassoc": ["32", "31", "32"],
        "switch": ["on", "off", "on"],
        "wifi_if_24G.net_mode": ["11bgnax", "11bgn", "11bgnax"],
        "wifi_if_5G.net_mode": ["11anacax", "11anac", "11anacax"],
        "wifi_if_24G.bandwidth": ["HT20/HT40", "HT20", "HT20/HT40"],
        "wifi_if_5G.bandwidth": ["HT20/HT40/HT80", "HT20", "HT20/HT40/HT80"],
        "wifi_timed_off.enable": [0, 1, 0],
    },
    "timed_off_note": "The enabled test used a short future window and restored the complete original wifi_timed_off block.",
    "channel_scope_note": "Channel 1 and channel 36 are live-accepted examples; broader runtime-advertised channel ranges remain separate capability evidence until individually exercised.",
}

for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    method = by_id[method_id]
    existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    method["semantic_contracts"] = existing + [contract]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        "2026-08-31 public-SDK physical field matrix passed 15/15 cases with exact read-back and original-state restoration for channels, hidden/isolation flags, maxassoc, timed-off, master switch, net modes and bandwidths.",
        "Do not generalize the representative live channel transitions to every advertised channel without additional physical evidence; use runtime channel lists for capability discovery.",
    ]))

METHODS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
block = """
## Physical SDK field matrix — 2026-08-31

A USB-connected dedicated test router on firmware `V1.00(ACIY.3)C0` completed the public SDK Wi-Fi field suite with **15/15 passing cases in 178.96 s**. Every write used normal administrator authentication through `http://zyxel.home`, required read-back of the changed value, and restored the original state.

Live write/read-back/restore transitions included:

```text
2.4 GHz channel:          0 (auto) -> 1 -> 0
5 GHz channel:            0 (auto) -> 36 -> 0
24G/5G/DUAL/Guest hidden: 0 -> 1 -> 0
24G/5G isolate:           0 -> 1 -> 0
global maxassoc:          32 -> 31 -> 32
master switch:            on -> off -> on
24G net_mode:             11bgnax -> 11bgn -> 11bgnax
5G net_mode:              11anacax -> 11anac -> 11anacax
24G bandwidth:            HT20/HT40 -> HT20 -> HT20/HT40
5G bandwidth:             HT20/HT40/HT80 -> HT20 -> HT20/HT40/HT80
timed-off enable:         0 -> 1 -> 0 (complete block restored)
```

These live transitions establish setter/read-back behavior for the listed values. They do not imply that only those channel values are supported; the runtime-advertised channel/range fields remain the capability source for additional channel choices.
"""
if "## Physical SDK field matrix — 2026-08-31" not in wireless:
    wireless = wireless.rstrip() + "\n\n" + block.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- recorded the 2026-08-31 public-SDK Wi-Fi field matrix: 15/15 physical write/read-back/restore cases passed for representative 2.4/5-GHz channels, Hidden, AP isolation, global maxassoc, timed-off, Wi-Fi master switch, per-band net modes and bandwidths\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized 2026-08-31 Wi-Fi physical field matrix.")
