#!/usr/bin/env python3
# Copyright (C) 2026 Marc Leinen
# SPDX-License-Identifier: GPL-3.0-or-later
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=json.loads((ROOT/'specification/methods.json').read_text(encoding='utf-8'))
errors=[]
methods=spec.get('methods',[])
if len(methods)!=157: errors.append(f'expected 157 methods, got {len(methods)}')
ids=[m.get('method_id') for m in methods]
if len(ids)!=len(set(ids)): errors.append('duplicate method_id detected')
if len({m.get('namespace') for m in methods})!=16: errors.append('expected 16 namespaces')
valid=set(spec.get('verification_statuses',{}))
for m in methods:
    if m.get('verification') not in valid: errors.append(f"unknown verification status: {m.get('method_id')}")

# Publication policy files must be present before a public release.
required_files=[
    ROOT/'LICENSE.md', ROOT/'ATTRIBUTION.md',
    ROOT/'LICENSES/CC-BY-SA-4.0.txt', ROOT/'LICENSES/GPL-3.0.txt'
]
for path in required_files:
    if not path.is_file(): errors.append(f'missing required publication file: {path.relative_to(ROOT)}')
if 'CC BY-SA 4.0' not in (ROOT/'LICENSE.md').read_text(encoding='utf-8'):
    errors.append('documentation license marker missing')
if 'GPL-3.0-or-later' not in (ROOT/'LICENSE.md').read_text(encoding='utf-8'):
    errors.append('software license marker missing')

# Private-baseline live identifiers are stored only as hashes, never as literals.
import hashlib
text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts)
forbidden_hashes={
    'd3928833425e79637fd08a9e18bf98e8182e74aa715aa75919e4585229108590',
    '4800e8b5d2c8698e2ef00582d531bba10316506896e81a10ecd8643d12957e5c',
}
candidates=set(re.findall(r'(?i)\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b',text))
candidates.update(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',text))
for token in candidates:
    if hashlib.sha256(token.lower().encode()).hexdigest() in forbidden_hashes:
        errors.append('known private-baseline identifier leaked')
# Broad MAC scan: public docs should not contain captured MAC literals.
macs=set(re.findall(r'(?i)\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b',text))
if macs: errors.append('MAC-like literal(s) present; replace with placeholders')
if errors:
    print('PUBLIC REPO VALIDATION FAILED')
    for e in errors: print('-',e)
    sys.exit(1)
print(f'OK: {len(methods)} methods, {len(set(m["namespace"] for m in methods))} namespaces, no known live identifier leakage')
