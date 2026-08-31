# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

TOKENS = [
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
SECTIONS = ["wifi_if_24G", "wifi_if_5G", "wifi_if_DUAL", "wifi_if_GUEST"]
PROTECTED = [token for token in TOKENS if token != "none"]

methods = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods["methods"]}

final_id = "wifi.security_matrix.complete_2026_08_31.v1"
final_contract = {
    "id": final_id,
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "management_url": "http://zyxel.home",
    "matrix_size": 52,
    "coverage": {
        section: {
            "accepted_encryption_tokens": TOKENS,
            "protected_mode_key_roundtrip": PROTECTED,
        }
        for section in SECTIONS
    },
    "open_mode_key_behavior": {
        "wifi_if_24G": "encryption='none' persisted; requested empty key did not become the read-back key",
        "wifi_if_5G": "encryption='none' persisted; requested empty key did not become the read-back key",
        "wifi_if_DUAL": "encryption='none' persisted; requested empty key did not become the read-back key",
        "wifi_if_GUEST": "encryption='none' persisted and empty key read back exactly",
    },
    "password_modified": {
        "observed": "0 before write, 0 after write and 0 after restore for every completed case in the full 52-case campaign",
        "conclusion": "the field is not a generic indicator that a Wi-Fi key/security setting was changed during this admin API session",
        "exact_semantics": "unresolved",
    },
    "sdk_verification_note": "For open mode, verify encryption='none' as the contract. Do not require key='' on 24G/5G/DUAL because ACIY.3 accepts open mode while leaving the key field non-empty/unmodified.",
    "restore_policy": "Only mutable configuration is a restore target; runtime/capability metadata such as cur_channel, first_channel, last_channel and channel_list is excluded.",
}

for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    method = by_id[method_id]
    contracts = []
    for c in method.get("semantic_contracts", []):
        if isinstance(c, dict) and c.get("id") in {
            "wifi.security_matrix.partial_2026_08_31.v1",
            final_id,
        }:
            continue
        contracts.append(c)
    contracts.append(final_contract)
    method["semantic_contracts"] = contracts
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        "2026-08-31 complete physical Wi-Fi security matrix: all 13 source-known encryption tokens were accepted and read back on each of wifi_if_24G, wifi_if_5G, wifi_if_DUAL and wifi_if_GUEST.",
        "All 12 protected-mode tokens round-tripped the synthetic test key exactly on all four AP sections.",
        "For encryption='none', 24G/5G/DUAL accepted open mode but did not read back the requested empty key; Guest did read back an empty key. High-level clients must therefore verify the encryption token rather than force key='' as a universal open-mode invariant.",
        "password_modified remained 0 before/after writes and restores across the full 52-case security campaign; exact semantics remain unresolved."
    ]))
METHODS.write_text(json.dumps(methods, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sem = json.loads(SEMANTICS.read_text(encoding="utf-8"))
sem.setdefault("mappings", {})["wireless/wifi_get_ap_config.encryption.live_acceptance"] = {
    "evidence": "LIVE_SDK_WRITE_READBACK_RESTORE_2026_08_31",
    "firmware": "V1.00(ACIY.3)C0",
    "sections": {
        section: {"accepted_tokens": TOKENS}
        for section in SECTIONS
    },
    "protected_key_roundtrip": "All non-'none' tokens round-tripped the synthetic test key on all four sections.",
    "open_mode_key_behavior": final_contract["open_mode_key_behavior"],
}
sem.setdefault("mappings", {})["wireless/wifi_get_ap_config.password_modified"] = {
    "evidence": "LIVE_SDK_SECURITY_MATRIX_2026_08_31",
    "observed_value": 0,
    "observation": "remained 0 across all 52 encryption/key write/read-back/restore cases",
    "negative_semantic_finding": "not a generic latch for 'Wi-Fi password/security was changed by this admin API campaign'",
    "exact_meaning": "unresolved",
}
SEMANTICS.write_text(json.dumps(sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
partial_header = "## Partial physical encryption/key matrix — 2026-08-31"
if partial_header in wireless:
    wireless = wireless.split(partial_header)[0].rstrip() + "\n"
block = """
## Complete physical encryption/key matrix — 2026-08-31

The sanitized SDK campaign completed the full **13 encryption tokens × 4 AP sections = 52 cases** on ACIY.3, using only synthetic test keys and restoring each section after every case.

Live result: **all 13 source-known encryption tokens were accepted and read back on every tested AP section** (`wifi_if_24G`, `wifi_if_5G`, `wifi_if_DUAL`, `wifi_if_GUEST`). All 12 protected-mode tokens also round-tripped the synthetic test key exactly on every section.

Open mode has section-specific key-field behavior:

```text
wifi_if_24G   encryption=none accepted; requested empty key not read back
wifi_if_5G    encryption=none accepted; requested empty key not read back
wifi_if_DUAL  encryption=none accepted; requested empty key not read back
wifi_if_GUEST encryption=none accepted; empty key read back exactly
```

Therefore, `encryption="none"` is the open-mode write/read-back contract. A high-level client must **not** require `key=""` as a universal invariant for 24G/5G/DUAL; ACIY.3 can keep an internal/non-empty key field while the network is configured open.

`password_modified` remained `0` before the write, after the write and after the restore for every completed case across the full 52-case campaign. This disproves the simple interpretation "this field becomes 1 whenever Wi-Fi credentials/security are changed through the admin API"; its exact meaning remains unresolved.

Restore verification compares mutable configuration only. Runtime/capability metadata such as `cur_channel`, `first_channel`, `last_channel` and `channel_list` is not treated as restorable state.
"""
if "## Complete physical encryption/key matrix — 2026-08-31" not in wireless:
    wireless = wireless.rstrip() + "\n\n" + block.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- completed the 2026-08-31 Wi-Fi security matrix: all 13 source-known encryption tokens were live accepted on all four AP sections (52/52 cases), all protected modes round-tripped synthetic keys, open mode exposed section-specific key-field behavior, and password_modified remained 0 throughout the campaign\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized complete 52-case Wi-Fi security matrix.")
