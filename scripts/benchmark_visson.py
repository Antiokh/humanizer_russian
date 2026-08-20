#!/usr/bin/env python3
"""Deterministic source and dual-runtime benchmark for the Visson library."""
from __future__ import annotations
import json
from pathlib import Path

from check import check_text
from lint_visson import review
from review import run_review

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/visson_cases.json"

def main() -> None:
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    failures=[]
    for case in payload["cases"]:
        findings=review(case["text"])["findings"]
        ids={x["rule_id"] for x in findings}
        for rule_id in case.get("must_find",[]):
            if rule_id not in ids: failures.append(f"{case['id']}: missing {rule_id}; got {sorted(ids)}")
        for rule_id in case.get("must_not_find",[]):
            if rule_id in ids: failures.append(f"{case['id']}: forbidden {rule_id}; got {sorted(ids)}")

    default,_=check_text("Я хочу спросить у вас вопрос. Он претендует, что это нормально.",extended=False)
    default_ids={x["rule"] for x in default}
    for required in {"VISSON-NORM-ASK-QUESTION","VISSON-CALQUE-PRETEND-CLAUSE"}:
        if required not in default_ids: failures.append(f"compact default missing {required}: {default_ids}")
    if "VISSON-CALQUE-HAVE-NICE-DAY" in {x["rule"] for x in check_text("Имейте хороший день!",extended=False)[0]}:
        failures.append("extended formula leaked into compact default")
    extended,_=check_text("Имейте хороший день!",extended=True)
    if "VISSON-CALQUE-HAVE-NICE-DAY" not in {x["rule"] for x in extended}:
        failures.append("extended formula missing from compact --extended")

    board=run_review("Он претендует, что всё знает.",style_id="neutral",library_ids=["visson"])
    rows=[x for x in board["findings"] if x["rule_id"]=="VISSON-CALQUE-PRETEND-CLAUSE"]
    if len(rows)!=1 or rows[0].get("reviewer_id")!="visson": failures.append(f"board provenance failed: {rows}")
    groups=[g for g in board["board"]["groups"] if g["phenomenon_id"]=="russian.false_friend_pretend_claim"]
    if len(groups)!=1 or groups[0]["status"]!="SINGLE_REVIEW": failures.append(f"board grouping failed: {groups}")

    norm=run_review("Я хочу спросить у вас вопрос.",style_id="neutral",library_ids=["visson"])
    if not any(x["rule_id"]=="VISSON-NORM-ASK-QUESTION" for x in norm["board"]["guardrails"]):
        failures.append(f"Visson NORM finding did not enter board guardrails: {norm['board']['guardrails']}")

    if failures:
        print("VISSON BENCHMARK FAILED")
        for x in failures: print(f"- {x}")
        raise SystemExit(1)
    print(f"visson benchmark: {len(payload['cases'])} source cases + compact/board routing OK")

if __name__=="__main__": main()
