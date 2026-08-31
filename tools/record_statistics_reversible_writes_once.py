# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from pathlib import Path

METHODS = Path('specification/methods.json')
DOC = Path('api/statistics.md')
CHANGELOG = Path('CHANGELOG.md')

root = json.loads(METHODS.read_text(encoding='utf-8'))
by_id = {m['method_id']: m for m in root['methods']}

alias = by_id['statistics/set_alias']
forbidden = by_id['statistics/set_forbidden']

alias_contract = {
    'id': 'statistics.set_alias.sdk_roundtrip.live_2026_08_31.v1',
    'evidence': 'LIVE_SDK_REVERSIBLE_WRITE_2026_08_31',
    'firmware': 'V1.00(ACIY.3)C0',
    'sequence': 'existing inactive row -> synthetic alias -> inactive-view readback -> original alias restore -> restore readback',
    'privacy': 'Real MAC and alias values were used only locally and never emitted.',
}
forbidden_contract = {
    'id': 'statistics.set_forbidden.synthetic_roundtrip.live_2026_08_31.v1',
    'evidence': 'LIVE_SDK_REVERSIBLE_WRITE_2026_08_31',
    'firmware': 'V1.00(ACIY.3)C0',
    'sequence': 'synthetic locally-administered MAC absent -> set_forbidden(enable=1) result=0 -> forbidden-view readback -> set_forbidden(enable=0) result=0 -> confirmed absent',
    'privacy': 'No real client identifier was printed or published.',
}
for method, contract in [(alias, alias_contract), (forbidden, forbidden_contract)]:
    existing = [c for c in method.get('semantic_contracts', []) if not (isinstance(c, dict) and c.get('id') == contract['id'])]
    method['semantic_contracts'] = existing + [contract]

alias['implementation_notes'] = list(dict.fromkeys(alias.get('implementation_notes', []) + [
    '2026-08-31 SDK integration test changed one existing inactive client alias to a synthetic value, verified read-back, restored the exact original alias, and verified restoration.'
]))
forbidden['implementation_notes'] = list(dict.fromkeys(forbidden.get('implementation_notes', []) + [
    '2026-08-31 SDK integration test added a previously absent locally-administered synthetic MAC in Black mode, verified forbidden-view presence, removed it, and verified final absence.'
]))
METHODS.write_text(json.dumps(root, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

doc = DOC.read_text(encoding='utf-8')
needle = '- Temporary alias change live-tested and restored.'
if needle in doc:
    addition = '- 2026-08-31 SDK round-trip: an existing inactive client alias was changed to a synthetic test value, read back successfully, then restored exactly; real MAC/alias values were not logged.\n'
    if addition not in doc:
        doc = doc.replace(needle + '\n', needle + '\n' + addition, 1)
needle2 = '- In black-list mode, an arbitrary previously unknown locally-administered unicast MAC can be added with enable=1, appears in get_forbidden_users with forbidden=1, and is removed from that list with enable=0.'
if needle2 in doc:
    addition2 = '- 2026-08-31 SDK round-trip repeated this with a synthetic locally-administered MAC: add `result=0`, read-back present, remove `result=0`, final read-back absent.\n'
    if addition2 not in doc:
        doc = doc.replace(needle2 + '\n', needle2 + '\n' + addition2, 1)
DOC.write_text(doc, encoding='utf-8')

changelog = CHANGELOG.read_text(encoding='utf-8')
entry = '- live-verified SDK reversible Statistics writes for `set_alias` (synthetic alias + exact restore) and `set_forbidden` (synthetic locally-administered MAC add/readback/remove), with no real identifiers logged\n'
marker = 'Development metadata: `0.1.1.dev0`.\n\n'
if entry not in changelog and marker in changelog:
    changelog = changelog.replace(marker, marker + entry, 1)
CHANGELOG.write_text(changelog, encoding='utf-8')

print('Recorded reversible Statistics write evidence.')
