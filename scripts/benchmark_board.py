#!/usr/bin/env python3
"""Deterministic regression suite for editorial-board and evidence separation."""
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from editorial_board import build_board
from evidence_runtime import run_provider
from library_runtime import load_style
from review import run_review
ROOT=Path(__file__).resolve().parents[1]
def main():
    cases=json.loads((ROOT/"tests/editorial_board_cases.json").read_text(encoding="utf-8")); schema=json.loads((ROOT/"schemas/review-report.schema.json").read_text(encoding="utf-8")); Draft202012Validator.check_schema(schema); validator=Draft202012Validator(schema); style=load_style("neutral"); failures=[]
    slow={"id":"slow_fixture","status":"OPERATIONAL","evidence_type":"CORPUS_USAGE","failure_policy":"SKIP","timeout_ms":30,"module_path":"tests/fixtures/evidence_slow.py"}; items,status=run_provider(slow,"текст")
    if items or status["status"]!="TIMEOUT": failures.append(f"evidence hard-timeout contract failed: {status}")
    vote_board=build_board([{"rule_id":"TEST-EDIT","phenomenon_id":"editing.test_phenomenon","library_id":"test","source_namespace":"TEST","reviewer_id":"test","project_class":"EDITING","automation_level":"MODEL_ONLY","verdict":"CHANGE","excerpt":"тестовая формулировка","reason":"synthetic reviewer fixture"}],style,evidence=[{"provider_id":"test_corpus","phenomenon_id":"editing.test_phenomenon","evidence_type":"CORPUS_USAGE","direction":"SUPPORTS_KEEP","target_scope":"PHENOMENON","reason":"synthetic evidence fixture","strength":"LOW","scope":"test","line":0,"excerpt":"","provenance":[{"source":"synthetic fixture"}]}]); g=vote_board["groups"][0]
    if g["recommendation"]!="CHANGE" or g["reviewer_verdicts"].get("test")!="CHANGE" or len(g.get("evidence",[]))!=1: failures.append(f"evidence-vs-vote separation failed: {g}")
    unavailable=run_review("Обычный текст.",evidence_ids=["current_usage"]); us={x["provider_id"]:x["status"] for x in unavailable["evidence_status"]}
    if us.get("current_usage")!="UNAVAILABLE": failures.append(f"planned evidence fail-open contract failed: {us}")
    for case in cases:
        if case.get("type","runtime")=="board_unit":
            board=build_board(case["findings"],style,evidence=case.get("evidence"))
            if len(board["groups"])!=1: failures.append(f"{case['id']}: expected one board group, got {len(board['groups'])}"); continue
            group=board["groups"][0]
            if group["status"]!=case["expect_status"]: failures.append(f"{case['id']}: status {group['status']} != {case['expect_status']}")
            if group["recommendation"]!=case["expect_recommendation"]: failures.append(f"{case['id']}: recommendation {group['recommendation']} != {case['expect_recommendation']}")
            continue
        report=run_review(case["text"],style_id=case.get("style","neutral"),library_ids=case.get("libraries"),evidence_ids=case.get("evidence"))
        try: validator.validate(report)
        except Exception as exc: failures.append(f"{case['id']}: report schema failed: {exc}"); continue
        if case.get("evidence") is None and report["evidence_status"]: failures.append(f"{case['id']}: default board unexpectedly ran evidence providers")
        groups=report["board"]["groups"]; phenomena={g["phenomenon_id"] for g in groups}; statuses={g["phenomenon_id"]:g["status"] for g in groups}; guardrails=len(report["board"]["guardrails"]); rule_ids={x["rule_id"] for x in report["findings"]}; reviewers={x.get("reviewer_id") for x in report["findings"] if x.get("reviewer_id")}
        for x in case.get("expect_phenomena",[]):
            if x not in phenomena: failures.append(f"{case['id']}: missing phenomenon {x}")
        for x in case.get("must_not_have_phenomena",[]):
            if x in phenomena: failures.append(f"{case['id']}: forbidden phenomenon {x}")
        for x in case.get("expect_rule_ids",[]):
            if x not in rule_ids: failures.append(f"{case['id']}: missing rule_id {x}")
        for x in case.get("must_not_have_rule_ids",[]):
            if x in rule_ids: failures.append(f"{case['id']}: forbidden rule_id {x}")
        for x in case.get("expect_reviewers",[]):
            if x not in reviewers: failures.append(f"{case['id']}: missing reviewer {x}")
        for pid,expected in case.get("expect_status_by_phenomenon",{}).items():
            if statuses.get(pid)!=expected: failures.append(f"{case['id']}: status for {pid} {statuses.get(pid)} != {expected}")
        if "expect_guardrails" in case and guardrails!=case["expect_guardrails"]: failures.append(f"{case['id']}: guardrails {guardrails} != {case['expect_guardrails']}")
        if "expect_guardrails_min" in case and guardrails<case["expect_guardrails_min"]: failures.append(f"{case['id']}: guardrails {guardrails} < {case['expect_guardrails_min']}")
    if failures:
        print("EDITORIAL BOARD BENCHMARK FAILED"); [print(f"- {x}") for x in failures]; raise SystemExit(1)
    print(f"editorial-board benchmark: {len(cases)} cases + evidence contracts OK")
if __name__=="__main__": main()
