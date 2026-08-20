#!/usr/bin/env python3
"""Deterministic Compact + Editorial Board preservation benchmark for Velichko.

The source contributes source-neutral model-only Russian-core cards and three
metric-only proxies, not new surface warnings. This benchmark guards both
product routes and the no-op controls that justify that architecture.
"""
from __future__ import annotations

import json
from pathlib import Path

from check import check_text
from review import run_review

ROOT = Path(__file__).resolve().parents[1]


def russian_compact_findings(text: str) -> tuple[list[dict], dict]:
    findings, metrics = check_text(text)
    return [item for item in findings if item.get("library_id") == "russian"], metrics


def main() -> None:
    model_rules = json.loads((ROOT / "libraries/russian/rki-rules.json").read_text(encoding="utf-8"))["rules"]
    assert len(model_rules) == 13
    assert all(item["automation_level"] == "MODEL_ONLY" for item in model_rules)
    assert all(item["rule_id"].startswith("RU-") for item in model_rules)

    # Natural controls are original to the study. They exercise distinctions
    # that must remain context/model-only and must not become surface warnings.
    controls = [
        "Инженеры пришли. Они проверяют серверы.",
        "В городе есть театр.",
        "Пять экспертов выступили по очереди.",
        "Много людей пишут нам после публикации.",
        "Отчёт подготовлен аудитором.",
        "Исходя из условий задачи, получаем два решения.",
        "Показатель является одним из критериев.",
        "Нам пришлось ждать, сидя в коридоре.",
    ]
    for text in controls:
        compact_findings, _ = russian_compact_findings(text)
        assert compact_findings == [], ("compact", text, compact_findings)

        board = run_review(text, library_ids=["russian"])
        assert board["findings"] == [], ("board", text, board["findings"])
        assert board["board"]["groups"] == [], ("board-groups", text, board["board"])

    # Existing narrow Russian-core mechanics must still be routed in both modes.
    break_text = "На этом шаге процесс ломается."
    compact_break, _ = russian_compact_findings(break_text)
    assert any(item.get("rule") == "RU-CALQUE-ABSTRACT-BREAK" for item in compact_break), compact_break
    board_break = run_review(break_text, library_ids=["russian"])
    assert any(item.get("rule_id") == "RU-CALQUE-ABSTRACT-BREAK" for item in board_break["findings"]), board_break

    metric_text = (
        "Я проверил файл. Мы сверили журнал. Документ подписан мной. "
        "Метод является частью системы. Система представляет собой набор модулей."
    )
    compact_metric_findings, compact_metrics = russian_compact_findings(metric_text)
    assert compact_metric_findings == [], compact_metric_findings
    compact_rki = compact_metrics["russian"]["rki_distribution"]

    board_metric = run_review(metric_text, library_ids=["russian"])
    assert board_metric["findings"] == [], board_metric["findings"]
    board_rki = board_metric["metrics"]["russian"]["rki_distribution"]

    for metrics in (compact_rki, board_rki):
        assert metrics["nominative_personal_pronoun_proxy_tokens"] == 2, metrics
        assert metrics["agentive_passive_pronoun_proxy_hits"] >= 1, metrics
        assert metrics["bookish_copula_proxy_hits"] == 2, metrics
        assert metrics["policy"].startswith("METRIC_ONLY"), metrics
    assert compact_rki == board_rki, (compact_rki, board_rki)

    print("velichko bounded integration benchmark: OK")
    print("  product routes: Compact + Editorial Board")
    print("  new deterministic findings on preservation controls: 0")
    print("  new source-neutral RKI model-only cards: 13")
    print("  enriched existing Russian-core cards: gerund subject, participle head, participial compression")
    print("  metric-only proxies: 3")
    print(f"  preservation controls: {len(controls)}")


if __name__ == "__main__":
    main()
