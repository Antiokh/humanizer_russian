#!/usr/bin/env python3
"""Deterministic regression suite for the editorial-board runtime."""

from __future__ import annotations

import json
from pathlib import Path

from review import run_review

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cases = json.loads((ROOT / "tests/editorial_board_cases.json").read_text(encoding="utf-8"))
    failures = []
    for case in cases:
        report = run_review(case["text"], style_id="neutral")
        phenomena = {g["phenomenon_id"] for g in report["board"]["groups"]}
        guardrails = len(report["board"]["guardrails"])
        for expected in case.get("expect_phenomena", []):
            if expected not in phenomena:
                failures.append(f"{case['id']}: missing phenomenon {expected}")
        for forbidden in case.get("must_not_have_phenomena", []):
            if forbidden in phenomena:
                failures.append(f"{case['id']}: forbidden phenomenon {forbidden}")
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
