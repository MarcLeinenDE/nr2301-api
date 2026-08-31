# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
DOC = Path("api/statistics.md")
CHANGELOG = Path("CHANGELOG.md")

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}
method = by_id["statistics/get_conn_clients_info"]

contract_id = "clients.request_type.tokens.v1"
contract = {
    "id": contract_id,
    "evidence": "STATIC_FRONTEND_VERIFIED_PLUS_PRIOR_LIVE_VIEW_READBACK",
    "field": "request_type",
    "raw_tokens": {
        "get_active_users": "active clients view",
        "get_inactive_users": "inactive/offline clients view",
        "get_allow_users": "allow-list view; semantics depend on current MAC-filter mode",
        "get_forbidden_users": "forbidden/block-list view; semantics depend on current MAC-filter mode",
    },
    "important": "The inactive token is exactly get_inactive_users; get_offline_users is not a source-backed token.",
    "transport": "POST with top-level request_type for explicit views; a body-less GET variant also exists and remains separately documented.",
}
existing = [
    c for c in method.get("semantic_contracts", [])
    if not (isinstance(c, dict) and c.get("id") == contract_id)
]
method["semantic_contracts"] = existing + [contract]
method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
    "Exact shipped-frontend request_type tokens are get_active_users, get_inactive_users, get_allow_users and get_forbidden_users.",
    "Do not substitute get_offline_users for the source-correct inactive token get_inactive_users.",
    "Allow/forbidden views are mode-sensitive; callers should read statistics/get_black_white_mode before presenting policy semantics.",
]))
METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

doc = DOC.read_text(encoding="utf-8")
anchor = "### Semantics\n\n- **`clients.active`**"
section = """### Exact `request_type` tokens\n\nThe shipped frontend uses these four raw values when requesting explicit client views:\n\n| Raw token | View |\n|---|---|\n| `get_active_users` | active clients |\n| `get_inactive_users` | inactive/offline clients |\n| `get_allow_users` | allow-list view |\n| `get_forbidden_users` | forbidden/block-list view |\n\n`get_inactive_users` is the exact source-backed token. Do **not** replace it with the previously guessed `get_offline_users`. Explicit views are sent as a top-level POST field, for example `{\"request_type\":\"get_inactive_users\"}`. The separately observed body-less GET variant remains valid and is not redefined here as one of these four explicit tokens.\n\nAllow/forbidden semantics depend on the current Black/White MAC-filter mode; read `get_black_white_mode` before presenting them as policy state.\n\n"""
if "### Exact `request_type` tokens" not in doc and anchor in doc:
    doc = doc.replace(anchor, section + anchor, 1)
DOC.write_text(doc, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- normalized the exact `statistics/get_conn_clients_info.request_type` tokens from shipped-frontend evidence: `get_active_users`, `get_inactive_users`, `get_allow_users`, and `get_forbidden_users`; explicitly rejected the earlier guessed `get_offline_users` spelling\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized statistics client request_type tokens.")
