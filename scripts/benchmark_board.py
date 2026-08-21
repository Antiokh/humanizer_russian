#!/usr/bin/env python3
"""Deterministic regression suite for editorial-board and evidence separation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from editorial_board import build_board
from evidence_runtime import run_provider
from library_runtime import load_style
from review import run_review

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests/editorial_board_cases.json"


def evidence_contract_failures() -> list[str]:
    failures: list[str] = []
    style = load_style("neutral")
    slow = {
        "id": "slow_fixture",
        "status": "OPERATIONAL",
        "evidence_type": "CORPUS_USAGE",
        "failure_policy": "SKIP",
        "timeout_ms": 30,
        "module_path": "tests/fixtures/evidence_slow.py",
    }
    items, status = run_provider(slow, "текст")
    if items or status["status"] != "TIMEOUT":
        failures.append(f"evidence hard-timeout contract failed: {status}")

    vote_board = build_board(
        [
            {
                "rule_id": "TEST-EDIT",
                "phenomenon_id": "editing.test_phenomenon",
                "library_id": "test",
                "source_namespace": "TEST",
                "reviewer_id": "test",
                "project_class": "EDITING",
                "automation_level": "MODEL_ONLY",
                "verdict": "CHANGE",
                "excerpt": "тестовая формулировка",
                "reason": "synthetic reviewer fixture",
            }
        ],
        style,
        evidence=[
            {
                "provider_id": "test_corpus",
                "phenomenon_id": "editing.test_phenomenon",
                "evidence_type": "CORPUS_USAGE",
                "direction": "SUPPORTS_KEEP",
                "target_scope": "PHENOMENON",
                "reason": "synthetic evidence fixture",
                "strength": "LOW",
                "scope": "test",
                "line": 0,
                "excerpt": "",
                "provenance": [{"source": "synthetic fixture"}],
            }
        ],
    )
    group = vote_board["groups"][0]
    if (
        group["recommendation"] != "CHANGE"
        or group["reviewer_verdicts"].get("test") != "CHANGE"
        or len(group.get("evidence", [])) != 1
    ):
        failures.append(f"evidence-vs-vote separation failed: {group}")

    try:
        run_review("Обычный текст.", evidence_ids=["current_usage"])
    except ValueError as exc:
        if "project-only" not in str(exc) or "current_usage" not in str(exc):
            failures.append(f"project-only evidence rejection is unclear: {exc}")
    else:
        failures.append("project-only evidence provider current_usage was selectable")
    return failures


def run_cases(cases: list[dict], validator: Draft202012Validator) -> list[str]:
    failures: list[str] = []
    for case in cases:
        style = load_style(case.get("style", "neutral"))
        if case.get("type", "runtime") == "board_unit":
            board = build_board(case["findings"], style, evidence=case.get("evidence"))
            if len(board["groups"]) != 1:
                failures.append(f"{case['id']}: expected one board group, got {len(board['groups'])}")
                continue
            group = board["groups"][0]
            if group["status"] != case["expect_status"]:
                failures.append(f"{case['id']}: status {group['status']} != {case['expect_status']}")
            if group["recommendation"] != case["expect_recommendation"]:
                failures.append(f"{case['id']}: recommendation {group['recommendation']} != {case['expect_recommendation']}")
            continue

        report = run_review(
            case["text"],
            style_id=case.get("style", "neutral"),
            library_ids=case.get("libraries"),
            evidence_ids=case.get("evidence"),
            register=case.get("register", "general"),
        )
        try:
            validator.validate(report)
        except Exception as exc:
            failures.append(f"{case['id']}: report schema failed: {exc}")
            continue
        if case.get("evidence") is None and report["evidence_status"]:
            failures.append(f"{case['id']}: default board unexpectedly ran evidence providers")

        groups = report["board"]["groups"]
        phenomena = {g["phenomenon_id"] for g in groups}
        statuses = {g["phenomenon_id"]: g["status"] for g in groups}
        guardrails = len(report["board"]["guardrails"])
        rule_ids = {x["rule_id"] for x in report["findings"]}
        reviewers = {x.get("reviewer_id") for x in report["findings"] if x.get("reviewer_id")}

        for expected in case.get("expect_phenomena", []):
            if expected not in phenomena:
                failures.append(f"{case['id']}: missing phenomenon {expected}")
        for forbidden in case.get("must_not_have_phenomena", []):
            if forbidden in phenomena:
                failures.append(f"{case['id']}: forbidden phenomenon {forbidden}")
        for expected in case.get("expect_rule_ids", []):
            if expected not in rule_ids:
                failures.append(f"{case['id']}: missing rule_id {expected}")
        for forbidden in case.get("must_not_have_rule_ids", []):
            if forbidden in rule_ids:
                failures.append(f"{case['id']}: forbidden rule_id {forbidden}")
        for expected in case.get("expect_reviewers", []):
            if expected not in reviewers:
                failures.append(f"{case['id']}: missing reviewer {expected}")
        for phenomenon, expected_status in case.get("expect_status_by_phenomenon", {}).items():
            if statuses.get(phenomenon) != expected_status:
                failures.append(f"{case['id']}: status for {phenomenon} {statuses.get(phenomenon)} != {expected_status}")
        if "expect_guardrails" in case and guardrails != case["expect_guardrails"]:
            failures.append(f"{case['id']}: guardrails {guardrails} != {case['expect_guardrails']}")
        if "expect_guardrails_min" in case and guardrails < case["expect_guardrails_min"]:
            failures.append(f"{case['id']}: guardrails {guardrails} < {case['expect_guardrails_min']}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", nargs="?", default=str(DEFAULT_CASES))
    args = parser.parse_args()

    cases_path = Path(args.cases)
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/review-report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    failures = evidence_contract_failures()
    failures.extend(run_cases(cases, validator))
    if failures:
        print("EDITORIAL BOARD BENCHMARK FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"editorial-board benchmark: {len(cases)} cases + evidence contracts OK")


if __name__ == "__main__":
    main()
