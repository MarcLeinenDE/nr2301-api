# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SEMANTICS = Path("specification/semantics.json")
WIRELESS = Path("api/wireless.md")
CHANGELOG = Path("CHANGELOG.md")

TOKENS = {
    "psk+ccmp": "WPA-PSK / AES-CCMP",
    "psk+tkip": "WPA-PSK / TKIP",
    "psk+tkip+ccmp": "WPA-PSK / TKIP+AES-CCMP",
    "psk2+ccmp": "WPA2-PSK / AES-CCMP",
    "psk2+tkip": "WPA2-PSK / TKIP",
    "psk2+tkip+ccmp": "WPA2-PSK / TKIP+AES-CCMP",
    "psk-mixed+ccmp": "WPA/WPA2-PSK / AES-CCMP",
    "psk-mixed+tkip": "WPA/WPA2-PSK / TKIP",
    "psk-mixed+tkip+ccmp": "WPA/WPA2-PSK / TKIP+AES-CCMP",
    "sae": "WPA3-SAE",
    "sae-mixed": "WPA2-PSK/WPA3-SAE",
    "wep-mixed": "WEP",
    "none": "Open / no encryption",
}

methods = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods["methods"]}
contract_id = "wifi.encryption.presentation_tokens.v1"
contract = {
    "id": contract_id,
    "evidence": "STATIC_FRONTEND_VERIFIED",
    "source": "/html/wireless.html get_encryption_tag() lines 658-689 + security controls",
    "field": "encryption",
    "values": TOKENS,
    "scope": "frontend presentation/backend raw tokens; physical setter acceptance is not yet established for every token",
    "setter_evidence": {
        "sae-mixed": "shipped frontend explicitly constructs wifi_if_5G, wifi_if_24G and wifi_if_DUAL writes with encryption='sae-mixed' when updating the key"
    }
}
for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    method = by_id[method_id]
    existing = [c for c in method.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") == contract_id)]
    method["semantic_contracts"] = existing + [contract]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        "The shipped WebUI defines 13 exact encryption display/raw tokens. Treat these as frontend-proven tokens until physical write acceptance is established per token/section.",
        "The shipped frontend separately provides exact setter evidence for encryption='sae-mixed' on wifi_if_24G, wifi_if_5G and wifi_if_DUAL when changing the Wi-Fi key."
    ]))
METHODS.write_text(json.dumps(methods, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sem = json.loads(SEMANTICS.read_text(encoding="utf-8"))
sem.setdefault("mappings", {})["wireless/wifi_get_ap_config.encryption"] = {
    "source": "/html/wireless.html get_encryption_tag() lines 658-689 + security controls",
    "layer": "PRESENTATION_TOKEN",
    "evidence": "STATIC_FRONTEND_VERIFIED",
    "values": {token: {"meaning": meaning, "evidence": "STATIC_FRONTEND_VERIFIED"} for token, meaning in TOKENS.items()},
    "setter_scope_note": "Do not infer universal write acceptance from the display mapping. Physical testing must establish accepted/coerced/rejected behavior by section.",
    "explicit_setter_evidence": "sae-mixed appears in exact shipped-frontend wifi_set_ap_config writes for 24G, 5G and DUAL key updates."
}
SEMANTICS.write_text(json.dumps(sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
block = """
### Frontend encryption tokens

The shipped `wireless.html` frontend contains an exact display/raw-token mapping for the `encryption` field:

```text
psk+ccmp              WPA-PSK / AES-CCMP
psk+tkip              WPA-PSK / TKIP
psk+tkip+ccmp         WPA-PSK / TKIP+AES-CCMP
psk2+ccmp             WPA2-PSK / AES-CCMP
psk2+tkip             WPA2-PSK / TKIP
psk2+tkip+ccmp        WPA2-PSK / TKIP+AES-CCMP
psk-mixed+ccmp        WPA/WPA2-PSK / AES-CCMP
psk-mixed+tkip        WPA/WPA2-PSK / TKIP
psk-mixed+tkip+ccmp   WPA/WPA2-PSK / TKIP+AES-CCMP
sae                    WPA3-SAE
sae-mixed              WPA2-PSK/WPA3-SAE
wep-mixed              WEP
none                   Open / no encryption
```

This mapping is **frontend-source verified**, not yet a claim that every token is accepted by every AP block on ACIY.3. The shipped frontend separately constructs `wifi_set_ap_config` writes using `encryption="sae-mixed"` for `wifi_if_24G`, `wifi_if_5G` and `wifi_if_DUAL` when changing the key. Physical matrix testing should classify each remaining token/section as accepted, coerced or rejected before a high-level SDK enum is treated as fully live verified.
"""
anchor = "### Response\n"
if "### Frontend encryption tokens" not in wireless:
    pos = wireless.find(anchor, wireless.find("## `wifi_set_ap_config`"))
    if pos >= 0:
        wireless = wireless[:pos] + block.strip() + "\n\n" + wireless[pos:]
    else:
        wireless = wireless.rstrip() + "\n\n" + block.strip() + "\n"
WIRELESS.write_text(wireless, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- restored the source-verified 13-token Wi-Fi encryption presentation mapping from the shipped wireless.html frontend into the current public contract; physical per-section setter acceptance remains a dedicated matrix task, while sae-mixed has exact frontend setter evidence for 24G/5G/DUAL key updates\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized Wi-Fi encryption presentation tokens.")
