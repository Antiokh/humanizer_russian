#!/usr/bin/env python3
"""Normalized Native/core adapter without source-library findings.

`scripts/lint.py` remains the standalone surface linter and compatibility CLI.
The knowledge-library runtime consumes this module through `review_v1`, so the
native layer owns its mapping from legacy surface names to the normalized
finding contract. Source-specific Chukovsky findings are filtered before they
can be attributed to the native reviewer.
"""

from __future__ import annotations

import re
from typing import Any

try:
    from lint import lint as aggregate_lint
except ImportError:  # package/import context
    from scripts.lint import lint as aggregate_lint

DEFAULT_MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
}

PHENOMENON_MAP = {
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

PROJECT_CLASS_BY_KIND = {
    "ARTIFACT": "ARTIFACT",
    "NATIVE_WARNING": "NATIVE_USAGE",
    "STYLE_WARNING": "EDITING",
    "EDITING_SUGGESTION": "EDITING",
    "AI_PATTERN": "AI_CALQUE",
}


def _slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-zа-яё0-9]+", "_", value, flags=re.I)
    return value.strip("_") or "unknown"


def _normalize_native_finding(finding: dict[str, Any]) -> dict[str, Any]:
    rule = str(finding["rule"])
    kind = str(finding["kind"])
    try:
        project_class = PROJECT_CLASS_BY_KIND[kind]
    except KeyError as exc:
        raise ValueError(f"unsupported native surface kind: {kind!r}") from exc

    automation_level = (
        "HARD_GATE"
        if kind == "ARTIFACT"
        else "DEFAULT_MECHANICAL"
        if rule in DEFAULT_MECHANICAL_RULES
        else "EXTENDED_SOFT"
    )
    phenomenon_id = PHENOMENON_MAP.get(rule)
    if not phenomenon_id and rule.startswith("calque: "):
        phenomenon_id = f"ai_calque.{_slug(rule[8:])}"
    if not phenomenon_id:
        # Preserve the historical identifier until an individual rule receives
        # a deliberate source-neutral phenomenon migration.
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
        # Compact mode has a stable human-facing surface predating rule IDs.
        # These are display hints, not normalization inputs.
        "display_rule": rule,
        "display_kind": kind,
    }


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    findings, metrics = aggregate_lint(text)
    native_findings = [
        _normalize_native_finding(item)
        for item in findings
        if item.get("source") != "chukovsky"
    ]
    native_metrics = {
        key: value
        for key, value in metrics.items()
        if not str(key).startswith("chukovsky_")
    }
    return {"findings": native_findings, "metrics": native_metrics}


def self_test() -> None:
    report = review("Следует отметить, что резервная копия завершилась в 03:10.")
    assert not [item for item in report["findings"] if item.get("source") == "chukovsky"]
    assert not [key for key in report["metrics"] if key.startswith("chukovsky_")]

    artifact = review("Служебный маркер turn1search2 нельзя публиковать.")["findings"]
    assert len(artifact) == 1, artifact
    assert artifact[0]["project_class"] == "ARTIFACT", artifact
    assert artifact[0]["automation_level"] == "HARD_GATE", artifact
    assert artifact[0]["verdict"] == "CHANGE", artifact
    assert artifact[0]["reviewer_id"] is None, artifact


if __name__ == "__main__":
    self_test()
    print("lint_native review_v1 self-test: OK")
