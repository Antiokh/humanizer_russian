#!/usr/bin/env python3
"""High-precision Russian lexical-calque candidates.

These checks are deliberately narrow. They flag places where an English verb
can spread too broadly into Russian and erase a more specific native relation.
A finding is REVIEW, not a language error: colloquial technical usage and
intentional metaphor can be valid.
"""
from __future__ import annotations

import re
from typing import Any

ABSTRACT_BREAK_SUBJECT = (
    r"(?:процесс(?:ы)?|логик(?:а|и)|сценари(?:й|и)|алгоритм(?:ы)?|"
    r"систем(?:а|ы)|интеграц(?:ия|ии)|автоматизац(?:ия|ии)|пайплайн(?:ы)?|"
    r"карьер(?:а|ы))"
)

# This rule targets the over-broad imperfective/ongoing use that often mirrors
# English break = fail/go wrong. Perfective result forms such as "сломалась" or
# resultative "сломана" are not this mechanical rule's target: with some nouns
# they are ordinary Russian metaphors and need lexical/contextual judgement.
ABSTRACT_BREAK_IMPERFECTIVE = (
    r"(?:ломается|ломаются|ломался|ломалась|ломалось|ломались|ломаться)"
)
ABSTRACT_BREAK_PATTERNS = [
    re.compile(
        rf"\b(?P<subject>{ABSTRACT_BREAK_SUBJECT})\b"
        rf"(?P<middle>[^.!?\n]{{0,60}}?)\b(?P<verb>{ABSTRACT_BREAK_IMPERFECTIVE})\b",
        re.I,
    ),
    re.compile(
        rf"\b(?P<verb>{ABSTRACT_BREAK_IMPERFECTIVE})\b"
        rf"(?P<middle>[^.!?\n]{{0,40}}?)\b(?P<subject>{ABSTRACT_BREAK_SUBJECT})\b",
        re.I,
    ),
]


def _line_no(text: str, start: int) -> int:
    return text.count("\n", 0, max(0, start)) + 1


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for pattern in ABSTRACT_BREAK_PATTERNS:
        for match in pattern.finditer(text):
            key = match.span()
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                {
                    "rule_id": "RU-CALQUE-ABSTRACT-BREAK",
                    "phenomenon_id": "russian.abstract_break_calque",
                    "project_class": "AI_CALQUE",
                    "automation_level": "DEFAULT_MECHANICAL",
                    "verdict": "REVIEW",
                    "reviewer_id": "russian",
                    "line": _line_no(text, match.start()),
                    "excerpt": " ".join(match.group(0).split())[:240],
                    "reason": (
                        "Несовершенное `ломаться` относится к абстрактному процессу, логике, "
                        "сценарию или другой нефизической сущности. Здесь возможен слишком широкий "
                        "перенос English break = fail/go wrong. Уточните реальное событие: процесс "
                        "останавливается/сбивается, логика нарушается, сценарий перестаёт работать, "
                        "система даёт сбой и т. п. Лексикализованные значения вроде `голос ломается` "
                        "и намеренный технический жаргон не исправляются автоматически."
                    ),
                    "operation": "replace_abstract_break_with_specific_failure_verb",
                    "confidence": None,
                }
            )
    return {
        "findings": findings,
        "metrics": {"abstract_break_candidates": len(findings)},
    }


def self_test() -> None:
    positives = [
        "На этом шаге процесс ломается.",
        "Если поле пустое, логика ломается.",
        "Под нагрузкой система ломается.",
        "Из-за этой реформы карьера постепенно ломается.",
    ]
    for text in positives:
        rows = review(text)["findings"]
        assert any(x["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK" for x in rows), (text, rows)

    negatives = [
        "Велосипед часто ломается.",
        "Весной лёд ломается на реке.",
        "У подростка ломается голос.",
        "Карандаш сломался пополам.",
        "После обновления сломался сценарий обработки.",
        "Его карьера сломалась после скандала.",
        "Его карьера была сломана этим решением.",
    ]
    for text in negatives:
        rows = review(text)["findings"]
        assert not rows, (text, rows)


if __name__ == "__main__":
    self_test()
    print("Russian calque layer: OK")
