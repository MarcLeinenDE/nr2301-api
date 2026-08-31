# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
ROUTER_MD = Path("api/router.md")
CHANGELOG = Path("CHANGELOG.md")

method_doc = json.loads(METHODS.read_text(encoding="utf-8"))
method = next(m for m in method_doc["methods"] if m["method_id"] == "router/router_set_dhcp_settings_comb")
method["auth_evidence"] = "ADMIN_OK"
method["live_note"] = (
    "2026-08-31 public-SDK physical test via normal admin and http://zyxel.home: "
    "combined DHCP/DNS write succeeded, all seven non-DNS fields remained unchanged, "
    "and the complete original 12-field object was restored exactly."
)
notes = method.get("implementation_notes", []) + [
    "Public SDK physical verification on 2026-08-31 confirmed normal-admin write/read-back/restore through the combined DHCP/DNS setter.",
    "The test changed only DNS fields, asserted all seven non-DNS fields stayed unchanged, then required the complete restored object to equal the original object.",
]
method["implementation_notes"] = list(dict.fromkeys(notes))
METHODS.write_text(json.dumps(method_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

router = ROUTER_MD.read_text(encoding="utf-8")
router = router.replace(
    "| [`router_set_dhcp_settings_comb`](#router-set-dhcp-settings-comb) | `LIVE_VERIFIED` | `UNKNOWN` | `DISRUPTIVE_RECOVERY_REQUIRED` |",
    "| [`router_set_dhcp_settings_comb`](#router-set-dhcp-settings-comb) | `LIVE_VERIFIED` | `ADMIN_OK` | `DISRUPTIVE_RECOVERY_REQUIRED` |",
)
start = router.index("## `router_set_dhcp_settings_comb`")
end = router.index("\n<a id=\"router-set-dhcp-static-ip\"></a>", start)
section = router[start:end]
section = section.replace("**Auth evidence:** `UNKNOWN`", "**Auth evidence:** `ADMIN_OK`")
new_note = (
    "- 2026-08-31 public-SDK physical test through normal admin: DNS-only mutation preserved all seven non-DNS fields; "
    "the original complete 12-field DHCP/DNS object was restored and matched exactly on final read-back.\n"
)
if new_note.strip() not in section:
    if "### Notes\n\n" in section:
        section = section.replace("### Notes\n\n", "### Notes\n\n" + new_note, 1)
    else:
        section = section.rstrip() + "\n\n### Notes\n\n" + new_note
router = router[:start] + section + router[end:]
ROUTER_MD.write_text(router, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = (
    "- recorded the 2026-08-31 public-SDK physical combined DHCP/DNS write pass: normal-admin write succeeded, "
    "all seven non-DNS fields were preserved, and the complete original 12-field object was restored exactly; "
    "`router/router_set_dhcp_settings_comb` auth evidence is now `ADMIN_OK`\n"
)
needle = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog:
    changelog = changelog.replace(needle, needle + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized physical SDK DNS write evidence.")
