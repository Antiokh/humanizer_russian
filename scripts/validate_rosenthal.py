#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RULES=ROOT/'libraries/rosenthal/rules.json'
MANIFEST=ROOT/'libraries/rosenthal/library.json'
CASES=ROOT/'tests/rosenthal_cases.json'
REQ_STUDY=[
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/source.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/coverage.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/rules.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/interactions.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/current-norm.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/audit.md',
 'studies/rosenthal-pravopisanie-literaturnaya-pravka/integration-matrix.md',
]

def main():
    rules=json.loads(RULES.read_text(encoding='utf-8'))
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    items=rules['rules']
    ids=[x['rule_id'] for x in items]
    if len(ids)!=len(set(ids)): raise SystemExit('duplicate Rosenthal rule_id')
    if ids != [f'ROS-R{i:02d}' for i in range(1,len(items)+1)]: raise SystemExit('Rosenthal IDs must be contiguous ROS-Rxx')
    if rules['rule_count']!=len(items): raise SystemExit('rule_count mismatch')
    counts={k:sum(x['automation_level']==k for x in items) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    if counts!=rules['automation_counts']: raise SystemExit(f'automation count mismatch: {counts}')
    if counts!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':2,'METRIC_ONLY':1,'MODEL_ONLY':43}: raise SystemExit(f'unexpected automation split: {counts}')
    if manifest['source_branch']!='rosenthal' or manifest['adapter']!='review_v1': raise SystemExit('manifest routing mismatch')
    if manifest['source_version'].find(rules['source_fingerprint_sha256'])<0: raise SystemExit('manifest fingerprint mismatch')
    for p in REQ_STUDY:
        if not (ROOT/p).is_file(): raise SystemExit(f'missing study artifact: {p}')
    cases=json.loads(CASES.read_text(encoding='utf-8'))['cases']
    if len(cases)<8: raise SystemExit('too few Rosenthal mechanical controls')
    print(f"rosenthal study/library: {len(items)} rules; automation {counts}; {len(cases)} controls; OK")
if __name__=='__main__': main()
