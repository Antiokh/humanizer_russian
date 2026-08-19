#!/usr/bin/env python3
"""Deterministic benchmark for scripts/chukovsky_checks.py.

This benchmark validates only the surface/metric layer. It does not claim to
validate the 29 MODEL_ONLY rules from the book study.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

try:
    from chukovsky_checks import check_chukovsky
except ImportError:  # package/import context
    from scripts.chukovsky_checks import check_chukovsky


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "chukovsky_cases.json"


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def run_case(case: dict) -> list[str]:
    findings, metrics = check_chukovsky(case["text"], split_sentences(case["text"]))
    rules = [item["rule"] for item in findings]
    errors: list[str] = []

    for expected in case.get("must_find", []):
        if expected not in rules:
            errors.append(f"missing finding: {expected}; got={rules}")

    for forbidden in case.get("must_not_find", []):
        if forbidden in rules:
            errors.append(f"unexpected finding: {forbidden}; got={rules}")

    if case.get("clean") and findings:
        errors.append(f"expected no findings; got={rules}")

    for key, minimum in case.get("metric_min", {}).items():
        actual = metrics.get(key)
        if actual is None or actual < minimum:
            errors.append(f"metric {key}: expected >= {minimum}, got {actual}")

    for key, maximum in case.get("metric_max", {}).items():
        actual = metrics.get(key)
        if actual is None or actual > maximum:
            errors.append(f"metric {key}: expected <= {maximum}, got {actual}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    payload = json.loads(args.cases.read_text(encoding="utf-8"))
    failures: list[dict] = []

    for case in payload["cases"]:
        errors = run_case(case)
        if errors:
            failures.append({"id": case["id"], "errors": errors})

    summary = {
        "cases": len(payload["cases"]),
        "passed": len(payload["cases"]) - len(failures),
        "failed": len(failures),
        "failures": failures,
    }

    if args.as_json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            f"chukovsky benchmark: {summary['passed']}/{summary['cases']} passed"
        )
        for failure in failures:
            print(f"FAIL {failure['id']}")
            for error in failure["errors"]:
                print(f"  - {error}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
