#!/usr/bin/env python3
"""Aggregate the project-core Russian language checks."""
from __future__ import annotations

from typing import Any

from lint_russian import review as review_core
from lint_russian_calques import review as review_calques


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    core = review_core(text, context)
    calques = review_calques(text, context)
    metrics = dict(core.get("metrics", {}))
    metrics["calques"] = calques.get("metrics", {})
    return {
        "findings": [*core.get("findings", []), *calques.get("findings", [])],
        "metrics": metrics,
    }


if __name__ == "__main__":
    sample = "На этом шаге процесс ломается."
    assert any(x["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK" for x in review(sample)["findings"])
    print("Russian aggregate layer: OK")
