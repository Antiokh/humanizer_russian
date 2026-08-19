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

from check import check_text, compact_rows  # noqa: E402

DEFAULT_CASES = ROOT / "tests" / "lint_cases.json"


def test_compact_deduplication() -> None:
    """Exercise compatible, conflicting, and unmapped compact grouping cases."""
    common = {
        "phenomenon_id": "editing.action_hidden_in_nominalization",
        "project_class": "EDITING",
        "automation_level": "EXTENDED_SOFT",
        "line": 4,
        "excerpt": "Осуществляется проведение проверки",
        "reason": "candidate",
        "operation": "recover_actor_action_object",
        "confidence": None,
    }
    compatible = [
        {
            **common,
            "rule_id": "GAL-X",
            "library_id": "gal",
            "source_namespace": "GAL",
            "reviewer_id": "gal",
            "verdict": "REVIEW",
        },
        {
            **common,
            "line": 0,
            "rule_id": "CHUK-R17",
            "library_id": "chukovsky",
            "source_namespace": "CHUK",
            "reviewer_id": "chukovsky",
            "verdict": "REVIEW",
        },
    ]
    rows = compact_rows(compatible)
    assert len(rows) == 1, rows
    assert rows[0]["deduplicated_sources"] == 2, rows
    assert {item["library_id"] for item in rows[0]["provenance"]} == {"gal", "chukovsky"}, rows

    conflict = [dict(compatible[0], verdict="CHANGE"), dict(compatible[1], verdict="KEEP")]
    rows = compact_rows(conflict)
    assert len(rows) == 2, rows
    assert not any("deduplicated_sources" in row for row in rows), rows

    unmapped = [
        dict(
            compatible[0],
            phenomenon_id=None,
            rule_id="TEST-A",
            library_id="a",
            source_namespace="A",
            reviewer_id="a",
        ),
        dict(
            compatible[0],
            phenomenon_id=None,
            rule_id="TEST-B",
            library_id="b",
            source_namespace="B",
            reviewer_id="b",
        ),
    ]
    rows = compact_rows(unmapped)
    assert len(rows) == 2, rows
    assert not any("deduplicated_sources" in row for row in rows), rows


def run_case(case: dict) -> dict:
    """Run one deterministic corpus case and return a structured result."""
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
    """Run a JSON corpus and summarize pass/fail counts by mode."""
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
    """Run the requested benchmark corpus and print a human or JSON report."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cases",
        nargs="?",
        default=str(DEFAULT_CASES),
        help="path to deterministic JSON corpus",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    test_compact_deduplication()
    report = run_suite(Path(args.cases))

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"linter benchmark: {report['passed']}/{report['cases']} passed "
            f"({report['by_mode']}); compact dedupe OK"
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