#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from lint_rosenthal import review
ROOT=Path(__file__).resolve().parents[1]
CASES=ROOT/'tests/rosenthal_cases.json'

def main():
    payload=json.loads(CASES.read_text(encoding='utf-8'))
    failures=[]
    for c in payload['cases']:
        ids={x['rule_id'] for x in review(c['text'])['findings']}
        for rid in c.get('must_find',[]):
            if rid not in ids: failures.append(f"{c['id']}: missing {rid}; got {sorted(ids)}")
        for rid in c.get('must_not_find',[]):
            if rid in ids: failures.append(f"{c['id']}: forbidden {rid}")
        if c.get('clean') and ids: failures.append(f"{c['id']}: expected clean, got {sorted(ids)}")
    if failures:
        print('ROSENTHAL BENCHMARK FAILED')
        for x in failures: print('-',x)
        raise SystemExit(1)
    print(f"rosenthal benchmark: {len(payload['cases'])}/{len(payload['cases'])} passed")
if __name__=='__main__': main()
