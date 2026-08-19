#!/usr/bin/env python3
"""Normalized Chukovsky knowledge-library adapter.

Mechanical detection stays in chukovsky_checks.py. This module normalizes the
seven accepted EXTENDED_SOFT candidates through the canonical CHUK rule
registry so compact and editorial-board modes consume one source output.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from chukovsky_checks import check_chukovsky
    from lint import prose_text, sentences
except ImportError:  # package/import context
    from scripts.chukovsky_checks import check_chukovsky
    from scripts.lint import prose_text, sentences


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "libraries" / "chukovsky" / "rules.json"

# R17 has two surface routes to the same underlying phenomenon. The registry
# stores the general operation; the dense-cluster route benefits from a narrower
# follow-up hint. Rule identity itself comes from chukovsky_checks.py.
OPERATION_OVERRIDES = {
    "chukovsky: nominalization cluster": "reconstruct_events_and_roles",
}


def _load_registry() -> dict[str, dict]:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {item["rule_id"]: item for item in payload["rules"]}


RULES = _load_registry()


def review(text: str) -> dict:
    # Use exactly the same Markdown/code/URL normalization as the core surface
    # linter so compact and board cannot disagree merely because one inspected
    # prose and the other inspected raw markup.
    prose = prose_text(text)
    findings, metrics = check_chukovsky(prose, sentences(text))
    normalized = []
    for item in findings:
        if item.get("source") != "chukovsky":
            raise ValueError(f"unexpected source in Chukovsky adapter: {item.get('source')!r}")
        rule_id = item.get("rule_id")
        if not rule_id:
            raise ValueError(f"Chukovsky detector omitted structured rule_id: {item}")
        rule = RULES.get(rule_id)
        if rule is None:
            raise ValueError(f"Chukovsky detector references missing registry rule: {rule_id}")
        detector_label = item.get("rule", "")
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

    # Code fences/headings/URLs are not prose candidates in either runtime.
    markup = """# Заголовок

```text
Следует отметить, что в рамках данного документа осуществляется обеспечение качества.
```

Ссылка: https://example.test/Следует-отметить
"""
    result = review(markup)
    assert not result["findings"], result


if __name__ == "__main__":
    self_test()
    print("lint_chukovsky review_v1 self-test: OK")
