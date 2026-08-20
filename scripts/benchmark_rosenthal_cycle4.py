#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from lint_rosenthal import review
ROOT=Path(__file__).resolve().parents[1]

def main():
    cases=json.loads((ROOT/'studies/rosenthal-pravopisanie-stilistika/evals.json').read_text(encoding='utf-8'))['cases']
    failures=[]
    allowed={'ROS-R30','ROS-R44','ROS-R53'}
    for c in cases:
        findings=review(c['text'])['findings']
        ids={x['rule_id'] for x in findings}
        unexpected=ids-allowed
        if unexpected:
            failures.append(f"{c['id']}: unexpected Rosenthal mechanical findings: {sorted(unexpected)}")
        if c['expected']=='KEEP' and findings:
            failures.append(f"{c['id']}: preservation case produced mechanical findings: {sorted(ids)}")
        if c['expected']=='CHANGE' and c['rule_id'] in allowed and c['rule_id'] not in ids:
            failures.append(f"{c['id']}: expected existing mechanical {c['rule_id']}, got {sorted(ids)}")
    if failures:
        print('ROSENTHAL CYCLE 4 PROVENANCE/PRESERVATION BENCHMARK FAILED')
        for x in failures: print('-',x)
        raise SystemExit(1)
    print(f"rosenthal cycle4 provenance/preservation: {len(cases)}/{len(cases)} cases; no new mechanical surface; OK")
if __name__=='__main__': main()
