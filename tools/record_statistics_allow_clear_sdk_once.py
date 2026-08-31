# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path('specification/methods.json')
DOC = Path('api/statistics.md')
CHANGELOG = Path('CHANGELOG.md')

root = json.loads(METHODS.read_text(encoding='utf-8'))
by_id = {m['method_id']: m for m in root['methods']}

allow = by_id['statistics/set_allow']
clear = by_id['statistics/clear_offline_user']

allow_contract = {
    'id': 'statistics.set_allow.sdk_blackmode_synthetic.live_2026_08_31.v1',
    'evidence': 'LIVE_SDK_SYNTHETIC_WRITE_2026_08_31',
    'firmware': 'V1.00(ACIY.3)C0',
    'sequence': 'synthetic locally-administered MAC absent -> set_allow(enable=1) result=0 -> inactive-view readback with forbidden=0 -> allow-view remains absent in Black mode',
    'privacy': 'Synthetic identifier only; no real client identifier was printed or published.',
}
clear_contract = {
    'id': 'statistics.clear_offline_user.sdk_synthetic.live_2026_08_31.v1',
    'evidence': 'LIVE_SDK_SYNTHETIC_WRITE_2026_08_31',
    'firmware': 'V1.00(ACIY.3)C0',
    'sequence': 'same synthetic inactive row -> clear_offline_user result=0 -> confirmed absent from all explicit client views',
    'privacy': 'No real inactive-history row was deleted.',
}

for method, contract in [(allow, allow_contract), (clear, clear_contract)]:
    existing = [c for c in method.get('semantic_contracts', []) if not (isinstance(c, dict) and c.get('id') == contract['id'])]
    method['semantic_contracts'] = existing + [contract]

allow['implementation_notes'] = list(dict.fromkeys(allow.get('implementation_notes', []) + [
    '2026-08-31 SDK Black-mode synthetic test returned result=0 for set_allow(enable=1); the row appeared in the inactive view with forbidden=0 and correctly remained absent from get_allow_users in Black mode.'
]))
clear['implementation_notes'] = list(dict.fromkeys(clear.get('implementation_notes', []) + [
    '2026-08-31 SDK synthetic test cleared only the synthetic inactive row with result=0 and verified final absence from active, inactive, allow and forbidden views.'
]))
METHODS.write_text(json.dumps(root, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

doc = DOC.read_text(encoding='utf-8')
allow_needle = '- 2026-08-25 White-mode real Wi-Fi test: set_allow(enable=1) returned result0, client appeared in get_allow_users with allow=1, and the same Wi-Fi client successfully reconnected and became active. enable=0 removed it from Allow and restored allow=0.\n'
allow_note = '- 2026-08-31 SDK Black-mode synthetic round-trip: `set_allow(enable=1)` returned `result=0`; the synthetic row appeared in the inactive view with `forbidden=0` and correctly remained absent from `get_allow_users`. No real client was modified.\n'
if allow_note not in doc and allow_needle in doc:
    doc = doc.replace(allow_needle, allow_needle + allow_note, 1)
clear_needle = '- Live verification used source-correct get_inactive_users. 3 inactive records before; clear_offline_user returned result=0; selected record disappeared and 2 remained.\n'
clear_note = '- 2026-08-31 SDK synthetic cleanup: `clear_offline_user` returned `result=0` for the synthetic row created by the preceding Black-mode allow test; final reads confirmed it absent from all four explicit client views, so no real history row was deleted.\n'
if clear_note not in doc and clear_needle in doc:
    doc = doc.replace(clear_needle, clear_needle + clear_note, 1)
DOC.write_text(doc, encoding='utf-8')

changelog = CHANGELOG.read_text(encoding='utf-8')
entry = '- live-verified SDK `set_allow` + `clear_offline_user` with a synthetic locally-administered MAC in Black mode: allow returned result=0 with expected inactive-view semantics, then synthetic history was cleared with result=0 and verified absent from all explicit views\n'
marker = 'Development metadata: `0.1.1.dev0`.\n\n'
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding='utf-8')

print('Recorded Statistics synthetic allow/clear SDK evidence.')
