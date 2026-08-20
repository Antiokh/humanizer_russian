#!/usr/bin/env python3
"""Aggregate the project-core Russian language checks."""
from __future__ import annotations

from typing import Any

from lint_russian import review as review_core
from lint_russian_calques import review as review_calques
from lint_russian_rki_metrics import review as review_rki_metrics


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    core = review_core(text, context)
    calques = review_calques(text, context)
    rki_metrics = review_rki_metrics(text, context)
    metrics = dict(core.get("metrics", {}))
    metrics["calques"] = calques.get("metrics", {})
    metrics["rki_distribution"] = rki_metrics.get("metrics", {})
    return {
        "findings": [
            *core.get("findings", []),
            *calques.get("findings", []),
            *rki_metrics.get("findings", []),
        ],
        "metrics": metrics,
    }


if __name__ == "__main__":
    sample = "На этом шаге процесс ломается."
    report = review(sample)
    assert any(x["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK" for x in report["findings"])
    assert report["metrics"]["rki_distribution"]["policy"].startswith("METRIC_ONLY")
    print("Russian aggregate layer: OK")
