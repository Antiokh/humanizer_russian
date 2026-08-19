#!/usr/bin/env python3
"""Normalized Chukovsky knowledge-library adapter.

Mechanical detection stays in chukovsky_checks.py. This module only maps the
seven accepted EXTENDED_SOFT candidates into the shared review_v1 contract so
compact and editorial-board modes consume exactly the same source output.
"""

from __future__ import annotations

import re

try:
    from chukovsky_checks import check_chukovsky
except ImportError:  # package/import context
    from scripts.chukovsky_checks import check_chukovsky


RULE_MAP = {
    "chukovsky: metadiscourse deletion test": (
        "CHK-R24",
        "editing.metadiscourse_announcement",
        "compare_without_announcing_frame",
    ),
    "chukovsky: bureaucratic-register cluster": (
        "CHK-R15",
        "editing.register_leakage_bureaucratic",
        "check_register_fit",
    ),
    "chukovsky: light verb + nominalization": (
        "CHK-R17",
        "editing.action_hidden_in_nominalization",
        "recover_actor_action_object",
    ),
    "chukovsky: nominalization cluster": (
        "CHK-R17",
        "editing.action_hidden_in_nominalization",
        "reconstruct_events_and_roles",
    ),
    "chukovsky: modifier subtraction candidate": (
        "CHK-R18",
        "editing.modifier_semantic_subtraction",
        "compare_without_modifier",
    ),
    "chukovsky: evaluative-template cluster": (
        "CHK-R19",
        "editing.template_without_semantic_gain",
        "replace_template_function_with_supported_content",
    ),
    "chukovsky: repeated 'question' packaging": (
        "CHK-R25",
        "editing.procedural_question_packaging",
        "name_actual_speech_act",
    ),
    "chukovsky: abbreviation-density candidate": (
        "CHK-R09",
        "editing.abbreviation_reader_effort",
        "check_first_use_and_audience_effort",
    ),
}


def _sentences(text: str) -> list[str]:
    prose = re.sub(r"\s*\n+\s*", " ", text).strip()
    if not prose:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip()]


def review(text: str) -> dict:
    findings, metrics = check_chukovsky(text, _sentences(text))
    normalized = []
    for item in findings:
        rule_id, phenomenon_id, operation = RULE_MAP[item["rule"]]
        normalized.append(
            {
                "rule_id": rule_id,
                "phenomenon_id": phenomenon_id,
                "project_class": "EDITING",
                "automation_level": "EXTENDED_SOFT",
                "verdict": "REVIEW",
                "line": item.get("line", 0),
                "excerpt": item.get("excerpt", ""),
                "reason": item.get("note", ""),
                "operation": operation,
                "confidence": None,
            }
        )
    return {"findings": normalized, "metrics": metrics}


def self_test() -> None:
    result = review(
        "Следует отметить, что в рамках данного документа осуществляется "
        "обеспечение повышения качества обслуживания."
    )
    ids = {item["rule_id"] for item in result["findings"]}
    assert "CHK-R24" in ids, result
    assert "CHK-R15" in ids, result
    assert "CHK-R17" in ids, result
    assert all(item["automation_level"] == "EXTENDED_SOFT" for item in result["findings"])
    assert all(item["project_class"] == "EDITING" for item in result["findings"])


if __name__ == "__main__":
    self_test()
    print("lint_chukovsky review_v1 self-test: OK")
