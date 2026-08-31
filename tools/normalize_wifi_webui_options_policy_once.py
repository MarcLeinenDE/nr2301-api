# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
WIRELESS = Path("api/wireless.md")
AGENTS = Path("AGENTS.md")
CHANGELOG = Path("CHANGELOG.md")

doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in doc["methods"]}

contracts = [
    {
        "id": "wifi.webui.net_mode_24g.v1",
        "evidence": "STATIC_FRONTEND_VERIFIED",
        "source": "/html/wireless.html control wifi_24g_80211_mode",
        "field": "wifi_if_24G.net_mode",
        "values": ["11b", "11bg", "11bgn", "11bgnax"],
    },
    {
        "id": "wifi.webui.net_mode_5g.v1",
        "evidence": "STATIC_FRONTEND_VERIFIED",
        "source": "/html/wireless.html control wifi_5g_80211_mode",
        "field": "wifi_if_5G.net_mode",
        "values": ["11a", "11an", "11anac", "11anacax"],
    },
    {
        "id": "wifi.webui.bandwidth_24g.v1",
        "evidence": "STATIC_FRONTEND_VERIFIED",
        "source": "/html/wireless.html control wifi_24g_channel_band",
        "field": "wifi_if_24G.bandwidth",
        "values": ["HT20/HT40", "HT20", "HT40"],
    },
    {
        "id": "wifi.webui.bandwidth_5g.v1",
        "evidence": "STATIC_FRONTEND_VERIFIED",
        "source": "/html/wireless.html control wifi_5g_channel_band",
        "field": "wifi_if_5G.bandwidth",
        "values": ["HT20/HT40/HT80", "HT20", "HT40", "HT80"],
    },
]
ids = {c["id"] for c in contracts}
for method_id in ("wireless/wifi_get_ap_config", "wireless/wifi_set_ap_config"):
    m = by_id[method_id]
    existing = [c for c in m.get("semantic_contracts", []) if not (isinstance(c, dict) and c.get("id") in ids)]
    m["semantic_contracts"] = existing + contracts
    m["implementation_notes"] = list(dict.fromkeys(m.get("implementation_notes", []) + [
        "The original NR2301 WebUI exposes exact per-band net_mode and bandwidth option tokens; these are protocol/UI capability evidence, not jurisdiction-specific legality rules.",
        "Do not impose Germany/EU-specific channel, band or transmit-power policy in the protocol contract. Record what firmware exposes/accepts and keep deployment legality separate.",
    ]))

METHODS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wireless = WIRELESS.read_text(encoding="utf-8")
needle = "Verified mode tokens on firmware `V1.00(ACIY.3)C0`:\n"
block = """Original WebUI option contracts additionally map exactly to the setter/getter fields:\n\n```text\nwifi_if_24G.net_mode: 11b | 11bg | 11bgn | 11bgnax\nwifi_if_5G.net_mode:  11a | 11an | 11anac | 11anacax\n\nwifi_if_24G.bandwidth: HT20/HT40 | HT20 | HT40\nwifi_if_5G.bandwidth:  HT20/HT40/HT80 | HT20 | HT40 | HT80\n```\n\nThese are firmware/WebUI capability tokens. They are not a statement that every option is lawful in every deployment jurisdiction. The API reference intentionally does not encode Germany/EU-specific radio-policy restrictions; firmware regulatory behavior and deployment policy are separate from the raw protocol contract.\n\n"""
if block not in wireless and needle in wireless:
    wireless = wireless.replace(needle, block + needle, 1)
WIRELESS.write_text(wireless, encoding="utf-8")

agents = AGENTS.read_text(encoding="utf-8")
marker = "## Core rule: evidence before convenience\n"
policy = """## Jurisdiction-neutral capability documentation\n\nThe API contract is global and must not hard-code Germany-, EU-, FCC-, or other jurisdiction-specific Wi-Fi channel, band or transmit-power policy merely because the maintainer or physical test router is located in one jurisdiction.\n\nDocument the raw capabilities, option tokens, firmware regulatory-domain behavior and acceptance/rejection results that are actually evidenced. A documented capability is **not** a claim that using it is lawful in every country or deployment.\n\nDo not invent unsupported radio values and do not bypass firmware/hardware enforcement. If firmware rejects or masks a value, record that behavior. Deployment-specific legal/regulatory policy belongs to the consumer/integrator/operator and/or the router firmware's regulatory domain, not to the protocol abstraction itself.\n\nPhysical lab testing on the dedicated non-production router may exercise evidenced or deliberately exploratory router-accepted radio settings to establish the technical contract. Clearly distinguish WebUI-proven enums, live-accepted values and unresolved exploratory values.\n\n"""
if policy not in agents and marker in agents:
    agents = agents.replace(marker, policy + marker, 1)
AGENTS.write_text(agents, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- normalized the original WebUI Wi-Fi net-mode and bandwidth option tokens for 2.4/5 GHz and clarified that the API is jurisdiction-neutral: radio capabilities are documented technically rather than filtered through Germany/EU-specific policy\n"
release_marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and release_marker in changelog:
    changelog = changelog.replace(release_marker, release_marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized Wi-Fi WebUI options and jurisdiction-neutral policy.")
