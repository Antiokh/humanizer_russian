#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from lint_rosenthal import review
ROOT=Path(__file__).resolve().parents[1]

def main():
    cases=json.loads((ROOT/'studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/evals.json').read_text(encoding='utf-8'))['cases']
    failures=[]
    cycle3={f'ROS-R{i}' for i in range(60,75)}
    for c in cases:
        findings=review(c['text'])['findings']
        leaked=[x['rule_id'] for x in findings if x['rule_id'] in cycle3]
        if leaked:
            failures.append(f"{c['id']}: cycle3 MODEL_ONLY leaked into mechanical runtime: {leaked}")
        if c['expected']=='KEEP' and findings:
            failures.append(f"{c['id']}: preservation case produced mechanical findings: {[x['rule_id'] for x in findings]}")
    if failures:
        print('ROSENTHAL CYCLE 3 PRESERVATION BENCHMARK FAILED')
        for x in failures: print('-',x)
        raise SystemExit(1)
    print(f"rosenthal cycle3 preservation: {len(cases)}/{len(cases)} cases; no cycle3 mechanical leakage; OK")
if __name__=='__main__': main()
