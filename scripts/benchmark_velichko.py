#!/usr/bin/env python3
"""Deterministic preservation benchmark for the bounded Velichko integration.

The source contributed model-only Russian-core cards and metric-only proxies,
not new surface warnings. This benchmark guards that architectural decision.
"""
from __future__ import annotations

import json
from pathlib import Path

from lint_russian_all import review as review_russian
from lint_russian_rki_metrics import review as review_metrics

ROOT = Path(__file__).resolve().parents[1]


def rule_ids(text: str) -> set[str]:
    return {item["rule_id"] for item in review_russian(text)["findings"]}


def main() -> None:
    model_rules = json.loads((ROOT / "libraries/russian/rki-rules.json").read_text(encoding="utf-8"))["rules"]
    assert len(model_rules) == 11
    assert all(item["automation_level"] == "MODEL_ONLY" for item in model_rules)
    assert all(item["rule_id"].startswith("RU-") for item in model_rules)

    # Natural controls drawn from the operational distinctions, not copied from
    # the book. The bounded study must not turn them into new surface findings.
    controls = [
        "Инженеры пришли. Они проверяют серверы.",
        "В городе есть театр.",
        "Пять экспертов выступили по очереди.",
        "Отчёт подготовлен аудитором.",
        "Исходя из условий задачи, получаем два решения.",
        "Показатель является одним из критериев.",
        "Нам пришлось ждать, сидя в коридоре.",
    ]
    for text in controls:
        ids = rule_ids(text)
        assert not any(item.startswith("VEL-") for item in ids), (text, ids)

    # Existing narrow Russian-core mechanics must still be routed normally.
    assert "RU-CALQUE-ABSTRACT-BREAK" in rule_ids("На этом шаге процесс ломается.")

    metric_report = review_metrics(
        "Я проверил файл. Мы сверили журнал. Документ подписан мной. "
        "Метод является частью системы. Система представляет собой набор модулей."
    )
    assert metric_report["findings"] == []
    metrics = metric_report["metrics"]
    assert metrics["nominative_personal_pronoun_proxy_tokens"] == 2, metrics
    assert metrics["agentive_passive_pronoun_proxy_hits"] >= 1, metrics
    assert metrics["bookish_copula_proxy_hits"] == 2, metrics
    assert metrics["policy"].startswith("METRIC_ONLY"), metrics

    print("velichko bounded integration benchmark: OK")
    print("  new deterministic findings: 0")
    print("  model-only Russian-core cards: 11")
    print("  metric-only proxies: 3")
    print(f"  preservation controls: {len(controls)}")


if __name__ == "__main__":
    main()
