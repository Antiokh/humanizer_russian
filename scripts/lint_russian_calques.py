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
    r"систем(?:а|ы)|интеграц(?:ия|ии)|автоматизац(?:ия|ии)|пайплайн(?:ы)?)"
)
ABSTRACT_BREAK_VERB = (
    r"(?:ломается|ломаются|сломался|сломалась|сломалось|сломались|сломается|сломаются)"
)
ABSTRACT_BREAK_PATTERNS = [
    re.compile(
        rf"\b(?P<subject>{ABSTRACT_BREAK_SUBJECT})\b"
        rf"(?P<middle>[^.!?\n]{{0,60}}?)\b(?P<verb>{ABSTRACT_BREAK_VERB})\b",
        re.I,
    ),
    re.compile(
        rf"\b(?P<verb>{ABSTRACT_BREAK_VERB})\b"
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
                        "`Ломаться` здесь относится к абстрактному процессу/логике/сценарию. "
                        "В русском это часто слишком широкая калька с English break: уточните, "
                        "что именно происходит — процесс останавливается, сбивается, нарушается, "
                        "перестаёт работать или даёт сбой. Разговорное техническое употребление "
                        "может быть намеренным, поэтому это REVIEW, а не запрет."
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
        "После обновления сломался сценарий обработки.",
        "Под нагрузкой система ломается.",
    ]
    for text in positives:
        rows = review(text)["findings"]
        assert any(x["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK" for x in rows), (text, rows)

    negatives = [
        "Велосипед часто ломается.",
        "Весной лёд ломается на реке.",
        "У подростка ломается голос.",
        "Карандаш сломался пополам.",
    ]
    for text in negatives:
        rows = review(text)["findings"]
        assert not rows, (text, rows)


if __name__ == "__main__":
    self_test()
    print("Russian calque layer: OK")
