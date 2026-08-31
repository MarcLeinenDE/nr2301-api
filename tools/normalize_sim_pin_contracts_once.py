# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
SIM_DOC = Path("api/sim.md")
CHANGELOG = Path("CHANGELOG.md")

REQUESTS = {
    "sim/provide_pin": {
        "http_method": "POST",
        "request_schema": {"pin_puk": {"pin": "string"}},
        "example": {"pin_puk": {"pin": "<secret>"}},
        "source": "/html/set_pin.html line 269",
        "frontend_expression": "{pin_puk:{pin:pin}}",
    },
    "sim/enable_pin": {
        "http_method": "POST",
        "request_schema": {"pin_puk": {"pin": "string"}},
        "example": {"pin_puk": {"pin": "<secret>"}},
        "source": "/html/set_pin.html line 273",
        "frontend_expression": "{pin_puk:{pin:pin}}",
    },
    "sim/disable_pin": {
        "http_method": "POST",
        "request_schema": {"pin_puk": {"pin": "string"}},
        "example": {"pin_puk": {"pin": "<secret>"}},
        "source": "/html/set_pin.html line 277",
        "frontend_expression": "{pin_puk:{pin:pin}}",
    },
    "sim/change_pin": {
        "http_method": "POST",
        "request_schema": {"pin_puk": {"pin": "string", "new_pin": "string"}},
        "example": {"pin_puk": {"pin": "<secret>", "new_pin": "<secret>"}},
        "source": "/html/set_pin.html line 281",
        "frontend_expression": "{pin_puk:{pin:pin,new_pin:new_pin}}",
    },
    "sim/reset_pin_using_puk": {
        "http_method": "POST",
        "request_schema": {"pin_puk": {"puk": "string", "new_pin": "string"}},
        "example": {"pin_puk": {"puk": "<secret>", "new_pin": "<secret>"}},
        "source": "/html/set_pin.html line 328",
        "frontend_expression": "{pin_puk:{puk:puk,new_pin:pin}}",
    },
}

methods_doc = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in methods_doc["methods"]}
contract_id = "sim.pin_puk.frontend_request_contracts.v1"

for method_id, request in REQUESTS.items():
    method = by_id[method_id]
    method["accepted_request"] = {
        "http_method": request["http_method"],
        "request_schema": request["request_schema"],
        "basis": "exact shipped-frontend request builder; physical acceptance pending",
    }
    contract = {
        "id": contract_id,
        "evidence": "STATIC_FRONTEND_VERIFIED",
        "source": request["source"],
        "http_method": request["http_method"],
        "request_schema": request["request_schema"],
        "frontend_expression": request["frontend_expression"],
        "secret_handling": "PIN/PUK/new_pin are secrets; redact and never publish real values",
        "validation": {
            "frontend_html_maxlength": 8,
            "scope": "maxlength=8 is source-verified; no stricter minimum length or character-set rule is asserted by this contract",
        },
        "testing_policy": "Do not consume SIM retries merely for coverage. Read pin_attempts/puk_attempts before any physical mutation and use only known-correct locally supplied credentials.",
    }
    existing = [
        c for c in method.get("semantic_contracts", [])
        if not (isinstance(c, dict) and c.get("id") == contract_id)
    ]
    method["semantic_contracts"] = existing + [contract]
    method["implementation_notes"] = list(dict.fromkeys(method.get("implementation_notes", []) + [
        f"Exact shipped-frontend POST payload reconstructed from {request['source']}: {request['frontend_expression']}.",
        "PIN/PUK values are secrets and must not be copied into fixtures, logs, public reports or documentation examples.",
        "The source-verified HTML fields use maxlength=8; do not invent stricter validation without separate evidence.",
    ]))

METHODS.write_text(json.dumps(methods_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sim = SIM_DOC.read_text(encoding="utf-8")
for method_id, request in REQUESTS.items():
    short = method_id.split("/", 1)[1]
    marker = f"## `{short}`"
    start = sim.find(marker)
    if start < 0:
        continue
    next_start = sim.find("\n<a id=", start + len(marker))
    if next_start < 0:
        next_start = len(sim)
    block = sim[start:next_start]
    request_pos = block.find("### Request")
    response_pos = block.find("### Response")
    if request_pos < 0 or response_pos < 0:
        continue
    request_text = f'''### Request\n\nHTTP method: `POST`\n\nExact shipped-frontend payload:\n\n```json\n{json.dumps(request["example"], indent=2)}\n```\n\nStatic source: `{request["source"]}`; frontend expression `{request["frontend_expression"]}`.\n\nThe PIN/PUK/new-PIN values are secrets and must be redacted. The corresponding WebUI password inputs are source-verified with `maxlength=8`; no stricter minimum length or character-set rule is asserted here.\n\n'''
    block = block[:request_pos] + request_text + block[response_pos:]
    sim = sim[:start] + block + sim[next_start:]

note = '''\n## PIN/PUK physical-testing policy — 2026-08-31\n\nThe public contract now contains the exact shipped-frontend request shapes for all five PIN/PUK mutation methods. This does **not** promote their physical verification status. Physical testing must be deliberate rather than coverage-driven:\n\n- obtain PIN/PUK only from local secret storage/environment; never publish them;\n- read `get_sim_status` before every mutation and refuse exploratory writes when retry counts are low or unavailable;\n- never send a deliberately incorrect PIN/PUK merely to discover error behavior;\n- prefer reversible enable/disable/change-PIN sequences with read-back and restoration;\n- `reset_pin_using_puk` remains a separate recovery-path capability and should not be exercised by intentionally exhausting PIN retries solely for coverage.\n'''
if "## PIN/PUK physical-testing policy — 2026-08-31" not in sim:
    sim = sim.rstrip() + "\n\n" + note.strip() + "\n"
SIM_DOC.write_text(sim, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
marker = "Development metadata: `0.1.1.dev0`.\n\n"
entry = "- reconstructed and normalized the exact shipped-frontend SIM PIN/PUK POST payloads for provide/enable/disable/change/reset, with explicit secret-redaction and retry-preservation policy; physical status remains unchanged pending deliberate known-credential testing\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Normalized exact static SIM PIN/PUK request contracts.")
