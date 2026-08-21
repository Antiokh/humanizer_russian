#!/usr/bin/env python3
"""Canonical normalized-finding contract shared by runtime and validators."""
from __future__ import annotations

from typing import Any

PROJECT_CLASSES = (
    "ARTIFACT",
    "NORM",
    "NATIVE_USAGE",
    "EDITING",
    "AI_CALQUE",
    "AUTHOR",
)
AUTOMATION_LEVELS = (
    "HARD_GATE",
    "DEFAULT_MECHANICAL",
    "EXTENDED_SOFT",
    "METRIC_ONLY",
    "MODEL_ONLY",
)
VERDICTS = ("CHANGE", "KEEP", "REVIEW")

GUARDRAIL_CLASSES = frozenset({"ARTIFACT", "NORM"})
DEFAULT_VISIBLE_AUTOMATION_LEVELS = frozenset({"HARD_GATE", "DEFAULT_MECHANICAL"})
EXTENDED_VISIBLE_AUTOMATION_LEVELS = frozenset(
    {"HARD_GATE", "DEFAULT_MECHANICAL", "EXTENDED_SOFT"}
)
AUTOMATION_PRIORITY = {
    "HARD_GATE": 4,
    "DEFAULT_MECHANICAL": 3,
    "EXTENDED_SOFT": 2,
    "METRIC_ONLY": 1,
    "MODEL_ONLY": 0,
}
VERDICT_PRIORITY = {"CHANGE": 2, "REVIEW": 1, "KEEP": 0}

_REQUIRED = ("rule_id", "phenomenon_id", "project_class", "automation_level", "verdict")


def _source_prefix(source: str | None) -> str:
    return f"{source} finding" if source else "finding"


def validate_normalized_finding(item: dict[str, Any], source: str | None = None) -> None:
    """Fail fast when a library emits a malformed or unsupported normalized finding."""
    prefix = _source_prefix(source)
    missing = [field for field in _REQUIRED if field not in item]
    if missing:
        raise ValueError(f"{prefix} missing fields: {', '.join(missing)}")

    for field in ("rule_id", "phenomenon_id"):
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{prefix} has invalid {field}: {value!r}")

    project_class = item.get("project_class")
    if project_class not in PROJECT_CLASSES:
        raise ValueError(f"{prefix} has unknown project_class: {project_class!r}")

    automation_level = item.get("automation_level")
    if automation_level not in AUTOMATION_LEVELS:
        raise ValueError(f"{prefix} has unknown automation_level: {automation_level!r}")

    verdict = item.get("verdict")
    if verdict not in VERDICTS:
        raise ValueError(f"{prefix} has unknown verdict: {verdict!r}")

    if automation_level == "HARD_GATE" and project_class not in GUARDRAIL_CLASSES:
        raise ValueError(
            f"{prefix} uses HARD_GATE for non-guardrail project_class {project_class!r}"
        )

    line = item.get("line", 0)
    if isinstance(line, bool) or not isinstance(line, int) or line < 0:
        raise ValueError(f"{prefix} has invalid line: {line!r}")

    for field in ("excerpt", "reason"):
        value = item.get(field, "")
        if not isinstance(value, str):
            raise ValueError(f"{prefix} has invalid {field}: {value!r}")

    for field in ("operation", "reviewer_id"):
        value = item.get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{prefix} has invalid {field}: {value!r}")
