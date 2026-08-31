# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path("specification/methods.json")
DOC = Path("api/sms.md")
CHANGELOG = Path("CHANGELOG.md")

root = json.loads(METHODS.read_text(encoding="utf-8"))
by_id = {m["method_id"]: m for m in root["methods"]}


def replace_contract(method: dict, contract: dict) -> None:
    cid = contract["id"]
    method["semantic_contracts"] = [
        c for c in method.get("semantic_contracts", [])
        if not (isinstance(c, dict) and c.get("id") == cid)
    ] + [contract]

save = by_id["sms/sms.save"]
replace_contract(save, {
    "id": "sms.save.existing_id.copy_on_save.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_PUBLIC_SDK_ACIY3",
    "request_intent": "shipped frontend sends id=<existing smsId> when saving an edited draft",
    "observed_firmware_behavior": "COPY_ON_SAVE",
    "observed_transition": {
        "original_id": "remained present with original body A",
        "new_id_count": 1,
        "new_id": "contained replacement body B",
    },
    "verified_success": {"resp": 0, "smsSaveSucc": 1, "smsSaveFail": 0},
    "scope": "observed on tested NR2301 ACIY.3 firmware; do not generalize to all firmware without evidence",
    "cleanup": "both synthetic Draft IDs deleted successfully; final synthetic absence verified",
    "privacy": "recipient/body/real identifiers not retained",
})
save["implementation_notes"] = list(dict.fromkeys(save.get("implementation_notes", []) + [
    "2026-08-31 ACIY.3 physical SDK test: saving with an existing Draft ID returned resp=0/smsSaveSucc=1/smsSaveFail=0 but did not modify that ID in place; the original remained unchanged and exactly one new Draft ID contained the replacement body (COPY_ON_SAVE).",
    "Keep the shipped-frontend existing-ID request variant documented as frontend intent, but do not describe its ACIY.3 effect as an in-place update.",
]))

listing = by_id["sms/sms.list_by_type"]
replace_contract(listing, {
    "id": "sms.list.draft.presentation.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_PUBLIC_SDK_SYNTHETIC_DRAFT",
    "list_type": 2,
    "observed": {
        "address_form": "BARE (no trailing comma)",
        "body_representation": "UTF-16BE hexadecimal",
        "type": 2,
    },
    "privacy": "synthetic address/body values not retained",
})
listing["implementation_notes"] = list(dict.fromkeys(listing.get("implementation_notes", []) + [
    "2026-08-31 synthetic Draft list readback on ACIY.3: address was returned without the save-wire trailing comma, body was UTF-16BE hex, and type=2.",
]))

get_by_id = by_id["sms/sms.get_by_id"]
replace_contract(get_by_id, {
    "id": "sms.get_by_id.draft.presentation.live_2026_08_31.v1",
    "evidence": "LIVE_VERIFIED_PUBLIC_SDK_SYNTHETIC_DRAFT",
    "observed": {
        "address_form": "BARE (no trailing comma)",
        "body_representation": "UTF-16BE hexadecimal",
        "type": 2,
    },
    "response_fields": [
        "address", "body", "contact_id", "date", "id", "location",
        "protocol", "read", "resp", "status", "type",
    ],
    "privacy": "synthetic address/body values not retained",
})
get_by_id["implementation_notes"] = list(dict.fromkeys(get_by_id.get("implementation_notes", []) + [
    "2026-08-31 synthetic Draft get_by_id readback on ACIY.3: address was bare (no trailing comma), body decoded from UTF-16BE hex, and type=2.",
]))

METHODS.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

doc = DOC.read_text(encoding="utf-8")
old = "Updating an existing draft uses the same object with `id=<existing smsId>`. `type=2` is the exact draft token. Historical live wire evidence using the stock frontend-compatible serializer showed `id`, `type` and `protocol` as JSON strings on the wire while `gsm7` remained a JSON boolean. `address` keeps the trailing comma and `body` uses the same frontend `UniEncode` representation as SMS send."
new = "The shipped frontend uses the same object with `id=<existing smsId>` when saving an edited draft. `type=2` is the exact draft token. Historical live wire evidence using the stock frontend-compatible serializer showed `id`, `type` and `protocol` as JSON strings on the wire while `gsm7` remained a JSON boolean. `address` keeps the trailing comma on the write wire and `body` uses the same frontend `UniEncode` representation as SMS send.\n\n**ACIY.3 physical behavior (2026-08-31):** an existing-ID save returned `resp=0`, `smsSaveSucc=1`, `smsSaveFail=0`, but did **not** modify the original Draft ID in place. The original ID remained with its old body and exactly one new Draft ID appeared with the replacement body. This is `COPY_ON_SAVE` behavior on the tested firmware. Treat the existing-ID value as shipped-frontend intent, not as proof of in-place update semantics on all firmware."
if old in doc:
    doc = doc.replace(old, new, 1)

response_note = "This success triple was live verified for a new draft. Recipient and message content are private data and should not be logged."
response_new = "This success triple was live verified for both a new Draft and the tested existing-ID save path. On ACIY.3, the existing-ID path exhibited `COPY_ON_SAVE` rather than in-place mutation. Recipient and message content are private data and should not be logged."
if response_note in doc:
    doc = doc.replace(response_note, response_new, 1)

list_anchor = "### 2026-08-31 SDK list representation evidence\n"
draft_list_note = """### 2026-08-31 Draft list presentation evidence\n\nA synthetic Draft (`list_type=2`) created through the public SDK read back with a **bare** address (the trailing comma used on the save wire was removed), a UTF-16BE-hex body and `type=2`. During the existing-ID save profiler, the original and copy Drafts remained distinguishable by decoded content classes without logging the actual address or body.\n\n"""
if "### 2026-08-31 Draft list presentation evidence" not in doc and list_anchor in doc:
    doc = doc.replace(list_anchor, draft_list_note + list_anchor, 1)

get_anchor = "### 2026-08-31 SDK inbound-reply evidence\n"
draft_get_note = """### 2026-08-31 Draft `get_by_id` presentation evidence\n\nSynthetic Draft reads through `sms.get_by_id` returned the documented field set with a bare address, UTF-16BE-hex body and `type=2`. The same representation was observed for both the original Draft and the new Draft produced by ACIY.3 `COPY_ON_SAVE` behavior.\n\n"""
if "### 2026-08-31 Draft `get_by_id` presentation evidence" not in doc and get_anchor in doc:
    doc = doc.replace(get_anchor, draft_get_note + get_anchor, 1)

DOC.write_text(doc, encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
entry = "- live-profiled `sms.save` existing-ID behavior on ACIY.3: despite the shipped frontend sending the current Draft ID and the router returning `resp=0/smsSaveSucc=1/smsSaveFail=0`, the original Draft remained unchanged and exactly one new Draft ID carried the replacement body (`COPY_ON_SAVE`); Draft list/get-by-ID also returned bare addresses and UTF-16BE-hex bodies\n"
marker = "Development metadata: `0.1.1.dev0`.\n\n"
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding="utf-8")

print("Recorded SMS Draft COPY_ON_SAVE evidence.")
