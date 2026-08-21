#!/usr/bin/env python3
"""Document-level preservation and default-noise regression benchmark.

Atomic rule tests answer whether known local cases still behave as expected.
This suite answers a different question: what does the complete enabled runtime
emit on realistic multi-paragraph documents, by library and in aggregate?

Only DEFAULT Compact behavior is frozen in the checked-in baseline. Extended
signals are reported for diagnosis but are not treated as a universal quality
threshold. A baseline change must therefore be deliberate and reviewable.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from check import compact_rows, select_normalized  # noqa: E402
from library_runtime import run_libraries  # noqa: E402

DEFAULT_CASES = ROOT / "tests" / "document_preservation_cases.json"
DEFAULT_BASELINE = ROOT / "tests" / "document_preservation_baseline.json"


def _sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def _selected_report(findings: list[dict[str, Any]], *, extended: bool) -> dict[str, Any]:
    selected = select_normalized(findings, extended=extended)
    rows = compact_rows(selected)
    by_library = Counter(str(item.get("library_id") or "unknown") for item in selected)
    by_class = Counter(str(item.get("project_class") or "unknown") for item in selected)
    by_automation = Counter(str(item.get("automation_level") or "unknown") for item in selected)
    by_rule = Counter(str(item.get("rule_id") or "unknown") for item in selected)
    return {
        "finding_count": len(selected),
        "compact_row_count": len(rows),
        "by_library": _sorted_counter(by_library),
        "by_class": _sorted_counter(by_class),
        "by_automation": _sorted_counter(by_automation),
        "by_rule": _sorted_counter(by_rule),
        "compact_rules": [row["rule"] for row in rows],
    }


def _case_report(case: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / case["path"]
    text = path.read_text(encoding="utf-8")
    register = case.get("register", "general")
    findings, metrics = run_libraries(
        text,
        context={"mode": "document_benchmark", "register": register},
    )
    default = _selected_report(findings, extended=False)
    extended = _selected_report(findings, extended=True)
    return {
        "id": case["id"],
        "genre": case["genre"],
        "path": case["path"],
        "register": register,
        "expectation": case["expectation"],
        "default": default,
        "extended": extended,
        "metrics": metrics,
    }


def _expectation_failures(case: dict[str, Any], report: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    default_rules = Counter(report["default"]["by_rule"])
    if case["expectation"] == "clean_default" and report["default"]["finding_count"]:
        failures.append(
            f"{case['id']}: expected zero default findings, got {report['default']['by_rule']}"
        )
    for rule_id in case.get("must_find_default", []):
        if default_rules[rule_id] <= 0:
            failures.append(f"{case['id']}: missing required default rule {rule_id}")
    for rule_id in case.get("must_not_find_default", []):
        if default_rules[rule_id] > 0:
            failures.append(f"{case['id']}: forbidden default rule {rule_id}")
    return failures


def _pair_failures(
    pairs: list[dict[str, Any]], reports_by_id: dict[str, dict[str, Any]]
) -> list[str]:
    failures: list[str] = []
    for pair in pairs:
        clean = Counter(reports_by_id[pair["clean_id"]]["default"]["by_rule"])
        defect = Counter(reports_by_id[pair["defect_id"]]["default"]["by_rule"])
        added = defect - clean
        removed = clean - defect
        expected = Counter({rule_id: 1 for rule_id in pair["expected_added_rules"]})
        missing = expected - added
        unexpected = added - expected
        if missing:
            failures.append(
                f"pair {pair['id']}: injected defect did not add {dict(missing)}; observed added={dict(added)}"
            )
        if unexpected:
            failures.append(
                f"pair {pair['id']}: injected edit added unexpected default rules {dict(unexpected)}"
            )
        if removed:
            failures.append(
                f"pair {pair['id']}: injected edit removed unrelated default rules {dict(removed)}"
            )
    return failures


def _aggregate(reports: list[dict[str, Any]], key: str) -> dict[str, Any]:
    by_library: Counter[str] = Counter()
    by_class: Counter[str] = Counter()
    by_automation: Counter[str] = Counter()
    by_rule: Counter[str] = Counter()
    finding_count = 0
    compact_row_count = 0
    for report in reports:
        selected = report[key]
        finding_count += selected["finding_count"]
        compact_row_count += selected["compact_row_count"]
        by_library.update(selected["by_library"])
        by_class.update(selected["by_class"])
        by_automation.update(selected["by_automation"])
        by_rule.update(selected["by_rule"])
    return {
        "finding_count": finding_count,
        "compact_row_count": compact_row_count,
        "by_library": _sorted_counter(by_library),
        "by_class": _sorted_counter(by_class),
        "by_automation": _sorted_counter(by_automation),
        "by_rule": _sorted_counter(by_rule),
    }


def build_report(cases_path: Path) -> tuple[dict[str, Any], list[str]]:
    payload = json.loads(cases_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    ids = [case["id"] for case in cases]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"duplicate document case ids: {duplicates}")

    reports = [_case_report(case) for case in cases]
    reports_by_id = {report["id"]: report for report in reports}
    failures: list[str] = []
    for case, report in zip(cases, reports):
        failures.extend(_expectation_failures(case, report))
    failures.extend(_pair_failures(payload.get("pairs", []), reports_by_id))

    return {
        "schema_version": 1,
        "suite": payload.get("suite", "humanizer_russian-document-preservation-v1"),
        "documents": len(reports),
        "genres": sorted({report["genre"] for report in reports}),
        "default": _aggregate(reports, "default"),
        "extended": _aggregate(reports, "extended"),
        "cases": reports,
    }, failures


def baseline_projection(report: dict[str, Any]) -> dict[str, Any]:
    """Freeze only deterministic default behavior, not the exploratory extended layer."""
    return {
        "schema_version": 1,
        "suite": report["suite"],
        "policy": (
            "Observed/audited DEFAULT Compact baseline. Update only after reviewing changed "
            "document findings; this is a regression snapshot, not a universal quality score."
        ),
        "aggregate": report["default"],
        "cases": [
            {
                "id": case["id"],
                "default": case["default"],
            }
            for case in report["cases"]
        ],
    }


def _baseline_diff(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    left = json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    right = json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    return list(
        difflib.unified_diff(
            left,
            right,
            fromfile="checked-in document baseline",
            tofile="current document baseline",
            lineterm="",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    parser.add_argument(
        "--print-baseline",
        action="store_true",
        help="print the current default baseline projection for explicit review/calibration",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    report, failures = build_report(Path(args.cases))
    current_baseline = baseline_projection(report)

    if args.print_baseline:
        print(json.dumps(current_baseline, ensure_ascii=False, indent=2))
        if failures:
            print("Expectation failures:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
        return

    baseline_path = Path(args.baseline)
    if not baseline_path.is_file():
        print("DOCUMENT BASELINE MISSING")
        print(json.dumps(current_baseline, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    expected_baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    diff = _baseline_diff(expected_baseline, current_baseline)
    if diff:
        failures.append("document-level DEFAULT Compact baseline changed")
        print("\n".join(diff))

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            "document preservation: "
            f"{report['documents']} docs; "
            f"default findings={report['default']['finding_count']} "
            f"rows={report['default']['compact_row_count']}; "
            f"extended findings={report['extended']['finding_count']} "
            f"rows={report['extended']['compact_row_count']}"
        )
        print(f"default by library: {report['default']['by_library']}")
        print(f"default by class: {report['default']['by_class']}")
        print(f"extended by library: {report['extended']['by_library']}")

    if failures:
        print("DOCUMENT PRESERVATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("document-level DEFAULT Compact baseline: OK")


if __name__ == "__main__":
    main()
