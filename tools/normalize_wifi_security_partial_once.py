# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

ALL_TOKENS = [
    "psk-mixed+ccmp",
    "sae-mixed",
    "sae",
    "psk2+ccmp",
    "psk+ccmp",
    "psk2+tkip+ccmp",
    "psk+tkip+ccmp",
    "psk-mixed+tkip+ccmp",
    "psk2+tkip",
    "psk+tkip",
    "psk-mixed+tkip",
    "wep-mixed",
    "none",
]
FIVE_G_ACCEPTED = ALL_TOKENS[:6]

methods = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods["methods"]}
contract_id = "wifi.security_matrix.partial_2026_08_31.v1"
contract = {
    "id": contract_id,
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "status": "PARTIAL_MATRIX_INTERRUPTED_BY_RESTORE_COMPARATOR_FALSE_POSITIVE",
    "wifi_if_24G": {
        "accepted_tokens": ALL_TOKENS,
        "key_behavior": {
            "none": "encryption token persisted as none; synthetic key was not retained",
            "all_other_tokens": "synthetic test key persisted exactly"
        }
    },
    "wifi_if_5G": {
        "accepted_tokens_before_resume_point": FIVE_G_ACCEPTED,
        "next_unclassified_token": "psk+tkip+ccmp"
    },
    "password_modified": {
        "observed_completed_cases": "0 -> 0 -> 0 for every completed write/restore case",
        "scope": "partial matrix only; do not infer universal semantics yet"
    },
    "restore_finding": {
        "section": "wifi_if_5G",
        "configured_channel": "restored independently from runtime operating channel",
        "only_mismatching_field": "cur_channel",
        "conclusion": "cur_channel is runtime state and must not be required to equal its pre-write value after configured auto-channel restore",
        "sdk_bug": "the first explorer version passed/restored the complete getter block and therefore falsely required cur_channel equality"
    }
}

for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    method = by_id[method_id]
    existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    method["semantic_contracts"] = existing + [contract]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        "2026-08-31 partial physical security matrix: all 13 source-known encryption tokens round-tripped on wifi_if_24G; none persisted as open mode while ignoring the synthetic key. The first six tokens also round-tripped on wifi_if_5G before the initial explorer aborted on a restore-comparison bug.",
        "A physical restore after 5-GHz security reconfiguration matched every configurable field while cur_channel alone differed. Treat cur_channel as runtime operating-channel state, not restorable configured state; configured channel remains the setter/read-back contract."
    ]))
METHODS.write_text(json.dumps(methods, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sem = json.loads(SEMANTICS.read_text(encoding="utf-8"))
sem.setdefault("mappings", {})["wireless/wifi_get_ap_config.wifi_if_5G.cur_channel"] = {
    "meaning": "current runtime operating channel",
    "evidence": "LIVE_SDK_RECONFIGURATION_2026_08_31",
    "configuration_field": "wifi_if_5G.channel",
    "restore_semantics": "Do not require cur_channel to return to its pre-write value after restoring configured channel, especially when configured channel is 0/auto.",
    "note": "The security-matrix restore returned all configurable fields to their original values while cur_channel alone differed."
}
sem.setdefault("mappings", {})["wireless/wifi_get_ap_config.wifi_if_24G.cur_channel"] = {
    "meaning": "current runtime operating channel",
    "evidence": "FIELD_ROLE_CONFIRMED_BY_5G_LIVE_BEHAVIOR_AND_SHARED_GETTER_SCHEMA",
    "configuration_field": "wifi_if_24G.channel",
    "restore_semantics": "Treat as runtime observation rather than setter target."
}
SEMANTICS.write_text(json.dumps(sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
block = """
## Partial physical encryption/key matrix — 2026-08-31

The first sanitized security-matrix run completed all 13 source-known encryption tokens on `wifi_if_24G` and the first six tokens on `wifi_if_5G` before the research runner stopped on a **restore-comparator false positive**.

Completed live results:

- `wifi_if_24G`: all 13 tokens were accepted and read back exactly;
- for `none`, the open-mode token persisted while the synthetic key was not retained;
- for the other 12 2.4-GHz tokens, the synthetic test key round-tripped exactly;
- `wifi_if_5G`: `psk-mixed+ccmp`, `sae-mixed`, `sae`, `psk2+ccmp`, `psk+ccmp` and `psk2+tkip+ccmp` were accepted with the synthetic key;
- `password_modified` remained `0 -> 0 -> 0` for every completed case in this partial run.

The interruption itself produced a separate contract finding. After restoring the 5-GHz configuration, every configurable field matched the original block and only `cur_channel` differed. `cur_channel` is therefore treated as **runtime operating-channel state**, not as a restorable configuration value. The configured `channel` field is the write/read-back contract; with `channel=0` (auto), a later `cur_channel` may legitimately differ after radio reconfiguration.

The remaining security matrix resumes at `wifi_if_5G / psk+tkip+ccmp`; the interrupted case is not classified from the failed runner because its result row had not yet been committed to the sanitized report.
"""
if "## Partial physical encryption/key matrix — 2026-08-31" not in wireless:
    wireless = wireless.rstrip() + "\n\n" + block.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- recorded the partial 2026-08-31 Wi-Fi security matrix: all 13 encryption tokens live-accepted on 24G, the first six live-accepted on 5G, open-mode key ignored as expected, password_modified stayed 0 through completed cases, and cur_channel was proven runtime/non-restorable after auto-channel reconfiguration\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized partial Wi-Fi security matrix and cur_channel restore semantics.")
