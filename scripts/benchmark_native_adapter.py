#!/usr/bin/env python3
"""Freeze legacy native-adapter behavior while the runtime uses review_v1.

This benchmark intentionally duplicates the pre-migration normalization mapping.
It is a regression oracle, not production code: changes to native rule identity,
phenomenon, automation, verdict, display surface or metrics must be deliberate.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from lint import lint as aggregate_lint
from lint_native import review as native_review

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "lint_cases.json"

OLD_DEFAULT_MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
}

OLD_PHENOMENON_MAP = {
    "repeated common element in contrast": "native.redundant_shared_material",
    "parcellated enumeration": "native.parcellated_enumeration",
    "ascii hyphen used as dash": "typography.ascii_hyphen_as_dash",
    "possessive overexplication candidate": "native.possessive_overexplication",
    "repeated sentence start": "native.repeated_sentence_start",
    "repeated explicit context candidate": "native.repeated_explicit_context",
    "context undercompression candidate": "native.context_undercompression",
    "repeated contrast formula": "style.repeated_contrast_formula",
    "anglo-rhetorical question/answer cluster": "ai_calque.qa_cluster",
    "short-fragment cluster": "style.short_fragment_cluster",
    "high dash density": "style.high_dash_density",
}

OLD_PROJECT_CLASS_BY_KIND = {
    "ARTIFACT": "ARTIFACT",
    "NATIVE_WARNING": "NATIVE_USAGE",
    "STYLE_WARNING": "EDITING",
    "EDITING_SUGGESTION": "EDITING",
    "AI_PATTERN": "AI_CALQUE",
}

SEMANTIC_FIELDS = (
    "rule_id",
    "phenomenon_id",
    "reviewer_id",
    "project_class",
    "automation_level",
    "verdict",
    "line",
    "excerpt",
    "reason",
    "operation",
    "confidence",
)


def _slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-zа-яё0-9]+", "_", value, flags=re.I)
    return value.strip("_") or "unknown"


def _old_semantics(finding: dict[str, Any]) -> dict[str, Any]:
    rule = str(finding["rule"])
    kind = str(finding["kind"])
    project_class = OLD_PROJECT_CLASS_BY_KIND[kind]
    automation_level = (
        "HARD_GATE"
        if kind == "ARTIFACT"
        else "DEFAULT_MECHANICAL"
        if rule in OLD_DEFAULT_MECHANICAL_RULES
        else "EXTENDED_SOFT"
    )
    phenomenon_id = OLD_PHENOMENON_MAP.get(rule)
    if not phenomenon_id and rule.startswith("calque: "):
        phenomenon_id = f"ai_calque.{_slug(rule[8:])}"
    if not phenomenon_id:
        phenomenon_id = f"legacy.{_slug(rule)}"
    return {
        "rule_id": f"NATIVE-{_slug(rule)}",
        "phenomenon_id": phenomenon_id,
        "reviewer_id": None if project_class == "ARTIFACT" else "native",
        "project_class": project_class,
        "automation_level": automation_level,
        "verdict": "CHANGE" if automation_level == "HARD_GATE" else "REVIEW",
        "line": int(finding.get("line", 0) or 0),
        "excerpt": str(finding.get("excerpt", "")),
        "reason": str(finding.get("note", "")),
        "operation": None,
        "confidence": None,
        "display_rule": rule,
        "display_kind": kind,
    }


def _project(item: dict[str, Any]) -> dict[str, Any]:
    out = {field: item.get(field) for field in SEMANTIC_FIELDS}
    out["display_rule"] = item.get("display_rule")
    out["display_kind"] = item.get("display_kind")
    return out


def main() -> None:
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []

    for case in payload["cases"]:
        raw_findings, raw_metrics = aggregate_lint(case["text"])
        raw_findings = [item for item in raw_findings if item.get("source") != "chukovsky"]
        old_metrics = {
            key: value
            for key, value in raw_metrics.items()
            if not str(key).startswith("chukovsky_")
        }
        expected = [_old_semantics(item) for item in raw_findings]

        report = native_review(case["text"])
        actual = report["findings"]

        if [_project(item) for item in actual] != [_project(item) for item in expected]:
            failures.append(
                f"{case['id']}: finding parity drift\n"
                f"  expected={[_project(item) for item in expected]!r}\n"
                f"  actual={[_project(item) for item in actual]!r}"
            )
        if report["metrics"] != old_metrics:
            failures.append(
                f"{case['id']}: metrics parity drift\n"
                f"  expected={old_metrics!r}\n"
                f"  actual={report['metrics']!r}"
            )

    if failures:
        print("NATIVE ADAPTER PARITY FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(f"native review_v1 parity: {len(payload['cases'])} legacy corpus cases OK")


if __name__ == "__main__":
    main()
