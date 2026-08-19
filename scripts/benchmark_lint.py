#!/usr/bin/env python3
"""Run the deterministic humanizer_russian linter corpus.

No LLM, network call, judge prompt or reference document is used. A case passes
only when the mechanical checker emits the required findings and avoids the
forbidden ones. Cases marked clean must produce no selected findings.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from check import check_text  # noqa: E402

DEFAULT_CASES = ROOT / "tests" / "lint_cases.json"


def run_case(case: dict) -> dict:
    extended = case.get("mode", "mechanical") == "extended"
    findings, metrics = check_text(case["text"], extended=extended)
    rules = [item["rule"] for item in findings]

    errors: list[str] = []
    for rule in case.get("must_find", []):
        if rule not in rules:
            errors.append(f"missing required rule: {rule}")
    for rule in case.get("must_not_find", []):
        if rule in rules:
            errors.append(f"forbidden rule emitted: {rule}")
    if case.get("clean") and findings:
        errors.append(f"expected clean result, got: {rules}")

    return {
        "id": case["id"],
        "mode": case.get("mode", "mechanical"),
        "ok": not errors,
        "errors": errors,
        "rules": rules,
        "metrics": metrics,
    }


def run_suite(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload["cases"]

    ids = [case["id"] for case in cases]
    duplicates = sorted(k for k, v in Counter(ids).items() if v > 1)
    if duplicates:
        raise ValueError(f"duplicate case ids: {duplicates}")

    results = [run_case(case) for case in cases]
    failed = [result for result in results if not result["ok"]]
    by_mode = Counter(result["mode"] for result in results)

    return {
        "version": payload.get("version", 1),
        "cases": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "by_mode": dict(sorted(by_mode.items())),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cases",
        nargs="?",
        default=str(DEFAULT_CASES),
        help="path to deterministic JSON corpus",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    report = run_suite(Path(args.cases))

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"linter benchmark: {report['passed']}/{report['cases']} passed "
            f"({report['by_mode']})"
        )
        for result in report["results"]:
            if result["ok"]:
                continue
            print(f"FAIL {result['id']} [{result['mode']}]")
            for error in result["errors"]:
                print(f"  - {error}")
            print(f"  emitted: {result['rules']}")

    if report["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
