#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from lint_rosenthal import review
ROOT=Path(__file__).resolve().parents[1]
def main():
    cases=json.loads((ROOT/'studies/rosenthal-prakticheskaya-stilistika-2001/evals.json').read_text(encoding='utf-8'))['cases']
    rules=json.loads((ROOT/'libraries/rosenthal/rules-cycle6.json').read_text(encoding='utf-8'))['rules']
    assert [r['rule_id'] for r in rules]==['ROS-R79'], rules
    failures=[]
    for c in cases:
        findings=review(c['text'])['findings']
        leaked=[x['rule_id'] for x in findings if x['rule_id']=='ROS-R79']
        if leaked: failures.append(f"{c['id']}: R79 MODEL_ONLY leaked into mechanical runtime: {leaked}")
        if c['expected']=='KEEP' and findings: failures.append(f"{c['id']}: preservation case produced mechanical findings: {[x['rule_id'] for x in findings]}")
    if failures:
        print('ROSENTHAL CYCLE 6 PRESERVATION BENCHMARK FAILED')
        for x in failures: print('-',x)
        raise SystemExit(1)
    print(f"rosenthal cycle6 preservation: {len(cases)}/{len(cases)} cases; R79 absent from mechanical runtime; OK")
if __name__=='__main__': main()
