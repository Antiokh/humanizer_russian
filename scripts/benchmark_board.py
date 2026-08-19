#!/usr/bin/env python3
"""Deterministic regression suite for the editorial-board runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from editorial_board import build_board
from library_runtime import load_style
from review import run_review

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests/editorial_board_cases.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", nargs="?", default=str(DEFAULT_CASES))
    args = parser.parse_args()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/review-report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    failures = []
    for case in cases:
        style_id = case.get("style", "neutral")
        style = load_style(style_id)
        if case.get("type", "runtime") == "board_unit":
            board = build_board(case["findings"], style)
            if len(board["groups"]) != 1:
                failures.append(f"{case['id']}: expected one board group, got {len(board['groups'])}")
                continue
            group = board["groups"][0]
            if group["status"] != case["expect_status"]:
                failures.append(f"{case['id']}: status {group['status']} != {case['expect_status']}")
            if group["recommendation"] != case["expect_recommendation"]:
                failures.append(f"{case['id']}: recommendation {group['recommendation']} != {case['expect_recommendation']}")
            continue

        report = run_review(case["text"], style_id=style_id, library_ids=case.get("libraries"))
        try:
            validator.validate(report)
        except Exception as exc:
            failures.append(f"{case['id']}: report schema failed: {exc}")
            continue
        groups = report["board"]["groups"]
        phenomena = {g["phenomenon_id"] for g in groups}
        guardrails = len(report["board"]["guardrails"])
        for expected in case.get("expect_phenomena", []):
            if expected not in phenomena:
                failures.append(f"{case['id']}: missing phenomenon {expected}")
        for forbidden in case.get("must_not_have_phenomena", []):
            if forbidden in phenomena:
                failures.append(f"{case['id']}: forbidden phenomenon {forbidden}")
        if "expect_status_by_phenomenon" in case:
            by_phenomenon = {g["phenomenon_id"]: g for g in groups}
            for phenomenon, expected_status in case["expect_status_by_phenomenon"].items():
                actual = by_phenomenon.get(phenomenon, {}).get("status")
                if actual != expected_status:
                    failures.append(f"{case['id']}: {phenomenon} status {actual} != {expected_status}")
        if "expect_reviewer" in case:
            reviewers = {f.get("reviewer_id") for f in report["findings"]}
            if case["expect_reviewer"] not in reviewers:
                failures.append(f"{case['id']}: missing reviewer {case['expect_reviewer']}; got {reviewers}")
        if "expect_guardrails" in case and guardrails != case["expect_guardrails"]:
            failures.append(f"{case['id']}: guardrails {guardrails} != {case['expect_guardrails']}")
        if "expect_guardrails_min" in case and guardrails < case["expect_guardrails_min"]:
            failures.append(f"{case['id']}: guardrails {guardrails} < {case['expect_guardrails_min']}")

    if failures:
        print("EDITORIAL BOARD BENCHMARK FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"editorial-board benchmark: {len(cases)} cases OK")


if __name__ == "__main__":
    main()
