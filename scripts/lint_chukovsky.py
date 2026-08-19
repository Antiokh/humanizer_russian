#!/usr/bin/env python3
"""Normalized Chukovsky knowledge-library adapter.

Mechanical detection stays in chukovsky_checks.py. This module maps the seven
accepted EXTENDED_SOFT candidates through the canonical CHUK rule registry so
compact and editorial-board modes consume the same source output without
copying phenomenon/class/automation metadata into two runtimes.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

try:
    from chukovsky_checks import check_chukovsky
except ImportError:  # package/import context
    from scripts.chukovsky_checks import check_chukovsky


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "libraries" / "chukovsky" / "rules.json"

# Detector labels are implementation details. Canonical public/runtime identity
# is CHUK-Rxx and is defined in libraries/chukovsky/rules.json.
DETECTOR_RULE_IDS = {
    "chukovsky: metadiscourse deletion test": "CHUK-R24",
    "chukovsky: bureaucratic-register cluster": "CHUK-R15",
    "chukovsky: light verb + nominalization": "CHUK-R17",
    "chukovsky: nominalization cluster": "CHUK-R17",
    "chukovsky: modifier subtraction candidate": "CHUK-R18",
    "chukovsky: evaluative-template cluster": "CHUK-R19",
    "chukovsky: repeated 'question' packaging": "CHUK-R25",
    "chukovsky: abbreviation-density candidate": "CHUK-R09",
}

# R17 has two surface routes to the same underlying phenomenon. The registry
# stores the general operation; the cluster route benefits from a narrower hint.
OPERATION_OVERRIDES = {
    "chukovsky: nominalization cluster": "reconstruct_events_and_roles",
}


def _load_registry() -> dict[str, dict]:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {item["rule_id"]: item for item in payload["rules"]}


RULES = _load_registry()


def _sentences(text: str) -> list[str]:
    prose = re.sub(r"\s*\n+\s*", " ", text).strip()
    if not prose:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip()]


def review(text: str) -> dict:
    findings, metrics = check_chukovsky(text, _sentences(text))
    normalized = []
    for item in findings:
        detector_label = item["rule"]
        rule_id = DETECTOR_RULE_IDS[detector_label]
        rule = RULES[rule_id]
        operation = OPERATION_OVERRIDES.get(detector_label, rule.get("operation"))
        normalized.append(
            {
                "rule_id": rule_id,
                "phenomenon_id": rule["phenomenon_id"],
                "project_class": rule["project_class"],
                "automation_level": rule["automation_level"],
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
    assert "CHUK-R24" in ids, result
    assert "CHUK-R15" in ids, result
    assert "CHUK-R17" in ids, result
    assert all(item["rule_id"].startswith("CHUK-") for item in result["findings"])
    assert all(item["automation_level"] == "EXTENDED_SOFT" for item in result["findings"])
    assert all(item["project_class"] == "EDITING" for item in result["findings"])
    assert all(
        item["phenomenon_id"] == RULES[item["rule_id"]]["phenomenon_id"]
        for item in result["findings"]
    )


if __name__ == "__main__":
    self_test()
    print("lint_chukovsky review_v1 self-test: OK")
