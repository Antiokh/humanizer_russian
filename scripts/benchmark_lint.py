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

from check import (  # noqa: E402
    check_text,
    compact_rows,
    has_blocking_findings,
    select_normalized,
)
from library_runtime import normalize_review_v1  # noqa: E402

DEFAULT_CASES = ROOT / "tests" / "lint_cases.json"


def test_compact_deduplication() -> None:
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
        {**common,"rule_id":"GAL-X","library_id":"gal","source_namespace":"GAL","reviewer_id":"gal","verdict":"REVIEW"},
        {**common,"line":0,"rule_id":"CHUK-R17","library_id":"chukovsky","source_namespace":"CHUK","reviewer_id":"chukovsky","verdict":"REVIEW"},
    ]
    rows = compact_rows(compatible)
    assert len(rows) == 1, rows
    assert rows[0]["deduplicated_sources"] == 2, rows
    assert {item["library_id"] for item in rows[0]["provenance"]} == {"gal", "chukovsky"}, rows

    same_line = [compatible[0], dict(compatible[1], line=4)]
    rows = compact_rows(same_line)
    assert len(rows) == 1, rows
    assert rows[0]["deduplicated_sources"] == 2, rows

    conflict = [dict(compatible[0], verdict="CHANGE"), dict(compatible[1], verdict="KEEP")]
    rows = compact_rows(conflict)
    assert len(rows) == 2, rows
    assert not any("deduplicated_sources" in row for row in rows), rows

    unmapped = [
        dict(compatible[0], phenomenon_id=None, rule_id="TEST-A", library_id="a", source_namespace="A", reviewer_id="a"),
        dict(compatible[0], phenomenon_id=None, rule_id="TEST-B", library_id="b", source_namespace="B", reviewer_id="b"),
    ]
    rows = compact_rows(unmapped)
    assert len(rows) == 2, rows
    assert not any("deduplicated_sources" in row for row in rows), rows

    shared = {
        "phenomenon_id": "norm.synthetic_overlap",
        "line": 1,
        "excerpt": "Один и тот же фрагмент",
        "reason": "synthetic overlap",
        "operation": None,
        "confidence": None,
    }
    soft = {
        **shared,
        "rule_id": "SOFT-X",
        "library_id": "a_soft",
        "source_namespace": "SOFT",
        "reviewer_id": "soft",
        "project_class": "EDITING",
        "automation_level": "DEFAULT_MECHANICAL",
        "verdict": "REVIEW",
    }
    hard = {
        **shared,
        "rule_id": "RU-NORM-X",
        "library_id": "russian",
        "source_namespace": "RU",
        "reviewer_id": None,
        "project_class": "NORM",
        "automation_level": "HARD_GATE",
        "verdict": "CHANGE",
    }
    forward = compact_rows([soft, hard])
    reverse = compact_rows([hard, soft])
    assert forward == reverse, (forward, reverse)
    assert len(forward) == 1, forward
    assert forward[0]["kind"] == "LANGUAGE_ERROR", forward
    assert forward[0]["project_class"] == "NORM", forward
    assert forward[0]["automation_level"] == "HARD_GATE", forward
    assert forward[0]["verdict"] == "CHANGE", forward
    assert forward[0]["rule"] == "RU-NORM-X", forward
    assert forward[0]["deduplicated_sources"] == 2, forward
    assert has_blocking_findings(forward), forward
    assert {item["rule_id"] for item in forward[0]["provenance"]} == {"SOFT-X", "RU-NORM-X"}, forward


def test_normalized_finding_contract() -> None:
    manifest = {"id": "contract-test", "source_namespace": "TEST", "reviewer_id": "test"}
    valid = {
        "rule_id": "TEST-R1",
        "phenomenon_id": "editing.contract_test",
        "project_class": "EDITING",
        "automation_level": "EXTENDED_SOFT",
        "verdict": "REVIEW",
        "line": 1,
        "excerpt": "Тест",
        "reason": "synthetic",
        "operation": None,
    }
    row = normalize_review_v1(valid, manifest)
    assert row["library_id"] == "contract-test", row

    invalid = [
        ("project_class", "EDITNG"),
        ("automation_level", "DEFAULT_MECHANIC"),
        ("verdict", "MAYBE"),
        ("rule_id", ""),
        ("phenomenon_id", ""),
        ("line", -1),
    ]
    for field, value in invalid:
        candidate = dict(valid)
        candidate[field] = value
        try:
            normalize_review_v1(candidate, manifest)
        except ValueError as exc:
            assert field in str(exc), (field, value, exc)
        else:
            raise AssertionError(f"invalid {field} accepted: {value!r}")

    bad_hard_gate = dict(valid, automation_level="HARD_GATE")
    try:
        normalize_review_v1(bad_hard_gate, manifest)
    except ValueError as exc:
        assert "HARD_GATE" in str(exc), exc
    else:
        raise AssertionError("non-guardrail HARD_GATE accepted")

    metric = dict(valid, automation_level="METRIC_ONLY")
    assert select_normalized([metric], extended=True) == [], metric


def run_case(case: dict) -> dict:
    extended = case.get("mode", "mechanical") == "extended"
    register = case.get("register", "general")
    findings, metrics = check_text(case["text"], extended=extended, register=register)
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
        "register": register,
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
    parser.add_argument("cases", nargs="?", default=str(DEFAULT_CASES), help="path to deterministic JSON corpus")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    test_compact_deduplication()
    test_normalized_finding_contract()
    report = run_suite(Path(args.cases))

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"linter benchmark: {report['passed']}/{report['cases']} passed ({report['by_mode']}); compact dedupe + finding contract OK")
        for result in report["results"]:
            if result["ok"]:
                continue
            print(f"FAIL {result['id']} [{result['mode']}/{result['register']}]")
            for error in result["errors"]:
                print(f"  - {error}")
            print(f"  emitted: {result['rules']}")

    if report["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
