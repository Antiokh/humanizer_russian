#!/usr/bin/env python3
"""High-precision Russian lexical-calque and event-structure candidates.

These checks are deliberately narrow. They flag places where an English verb
can spread too broadly into Russian or where Russian event structure usually
prefers a more specific pre-failure process/result. A finding is REVIEW, not a
language error: colloquial technical usage and intentional metaphor can be valid.
"""
from __future__ import annotations

import re
from typing import Any

ABSTRACT_BREAK_SUBJECT = (
    r"(?:процесс(?:ы)?|логик(?:а|и)|сценари(?:й|и)|алгоритм(?:ы)?|"
    r"систем(?:а|ы)|интеграц(?:ия|ии)|автоматизац(?:ия|ии)|пайплайн(?:ы)?|"
    r"карьер(?:а|ы))"
)

# High-precision mechanical surface: present/infinitive imperfective forms.
# Past imperfective ломался/ломались is deliberately not included: in Russian
# it can narrate repeated or bounded episodes ("машина несколько раз ломалась")
# without presenting one failure as an English-style continuous process.
ABSTRACT_BREAK_PRESENT = r"(?:ломается|ломаются|ломаться)"
ABSTRACT_BREAK_PATTERNS = [
    re.compile(
        rf"\b(?P<subject>{ABSTRACT_BREAK_SUBJECT})\b"
        rf"(?P<middle>[^.!?\n]{{0,60}}?)\b(?P<verb>{ABSTRACT_BREAK_PRESENT})\b",
        re.I,
    ),
    re.compile(
        rf"\b(?P<verb>{ABSTRACT_BREAK_PRESENT})\b"
        rf"(?P<middle>[^.!?\n]{{0,40}}?)\b(?P<subject>{ABSTRACT_BREAK_SUBJECT})\b",
        re.I,
    ),
]

# A second, narrower signal captures an explicit progressive reading with
# ordinary physical/functioning objects. In neutral everyday Russian, a speaker
# usually names the pre-break process (трещит, гнётся, глохнет, барахлит) or the
# boundary/result (сейчас сломается, сломалось), rather than saying that the
# object is "ломается" right now. This is NATIVE_USAGE, not NORM.
PROGRESSIVE_BREAK_SUBJECT = (
    r"(?:ветк(?:а|и)|ветв(?:ь|и)|л[её]д|машин(?:а|ы)|механизм(?:ы)?|"
    r"устройств(?:о|а)|детал(?:ь|и))"
)
PROGRESSIVE_CUE = r"(?:прямо\s+сейчас|сейчас|на\s+глазах|постепенно|в\s+данный\s+момент)"
HABITUAL_CUE_RE = re.compile(
    r"\b(?:часто|постоянно|регулярно|иногда|обычно|всегда|снова|опять|"
    r"несколько\s+раз|второй\s+раз|кажд\w*)\b",
    re.I,
)
PROGRESSIVE_BREAK_PATTERNS = [
    re.compile(
        rf"\b(?P<subject>{PROGRESSIVE_BREAK_SUBJECT})\b"
        rf"(?P<middle1>[^.!?\n]{{0,30}}?)\b(?P<cue>{PROGRESSIVE_CUE})\b"
        rf"(?P<middle2>[^.!?\n]{{0,30}}?)\b(?P<verb>ломается|ломаются)\b",
        re.I,
    ),
    re.compile(
        rf"\b(?P<cue>{PROGRESSIVE_CUE})\b"
        rf"(?P<middle1>[^.!?\n]{{0,30}}?)\b(?P<subject>{PROGRESSIVE_BREAK_SUBJECT})\b"
        rf"(?P<middle2>[^.!?\n]{{0,30}}?)\b(?P<verb>ломается|ломаются)\b",
        re.I,
    ),
    re.compile(
        rf"\b(?P<subject>{PROGRESSIVE_BREAK_SUBJECT})\b"
        rf"(?P<middle1>[^.!?\n]{{0,30}}?)\b(?P<verb>ломается|ломаются)\b"
        rf"(?P<middle2>[^.!?\n]{{0,30}}?)\b(?P<cue>{PROGRESSIVE_CUE})\b",
        re.I,
    ),
]


def _line_no(text: str, start: int) -> int:
    return text.count("\n", 0, max(0, start)) + 1


def _finding(
    rule_id: str,
    phenomenon_id: str,
    project_class: str,
    excerpt: str,
    line: int,
    reason: str,
    operation: str,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "phenomenon_id": phenomenon_id,
        "project_class": project_class,
        "automation_level": "DEFAULT_MECHANICAL",
        "verdict": "REVIEW",
        "reviewer_id": "russian",
        "line": line,
        "excerpt": " ".join(excerpt.split())[:240],
        "reason": reason,
        "operation": operation,
        "confidence": None,
    }


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int]] = set()

    for pattern in ABSTRACT_BREAK_PATTERNS:
        for match in pattern.finditer(text):
            key = ("abstract", *match.span())
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                _finding(
                    "RU-CALQUE-ABSTRACT-BREAK",
                    "russian.abstract_break_calque",
                    "AI_CALQUE",
                    match.group(0),
                    _line_no(text, match.start()),
                    (
                        "`Ломается/ломаться` описывает абстрактный процесс, логику, сценарий или "
                        "другую операционную сущность как будто сам отказ идёт во времени. В русском "
                        "поломка обычно мыслится как переход состояния: до границы называют конкретный "
                        "процесс (сбивается, глохнет, даёт сбой, нарушается), после границы — результат "
                        "(`сломалось`, `не работает`). Проверьте кальку English break = fail/go wrong."
                    ),
                    "replace_abstract_break_with_specific_failure_verb",
                )
            )

    for pattern in PROGRESSIVE_BREAK_PATTERNS:
        for match in pattern.finditer(text):
            excerpt = match.group(0)
            if HABITUAL_CUE_RE.search(excerpt):
                continue
            key = ("progressive", *match.span())
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                _finding(
                    "RU-NATIVE-BREAK-STATE-TRANSITION",
                    "russian.break_state_transition",
                    "NATIVE_USAGE",
                    excerpt,
                    _line_no(text, match.start()),
                    (
                        "Фраза подаёт `ломается` как наблюдаемый процесс прямо сейчас. Для бытового "
                        "русского это нетипичная событийная модель: обычно называют предшествующий "
                        "процесс (`трещит`, `гнётся`, `барахлит`, `глохнет`) или границу/результат "
                        "(`сейчас сломается`, `сломалось`). Повторяемое `часто ломается` и устойчивое "
                        "`голос ломается` — другие значения и этим правилом не запрещаются."
                    ),
                    "name_prebreak_process_or_state_transition",
                )
            )

    return {
        "findings": findings,
        "metrics": {
            "abstract_break_candidates": sum(
                1 for item in findings if item["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK"
            ),
            "progressive_break_candidates": sum(
                1 for item in findings if item["rule_id"] == "RU-NATIVE-BREAK-STATE-TRANSITION"
            ),
        },
    }


def self_test() -> None:
    abstract_positives = [
        "На этом шаге процесс ломается.",
        "Если поле пустое, логика ломается.",
        "Под нагрузкой система ломается.",
        "Из-за этой реформы карьера постепенно ломается.",
        "После изменения процесс начинает ломаться.",
    ]
    for text in abstract_positives:
        rows = review(text)["findings"]
        assert any(x["rule_id"] == "RU-CALQUE-ABSTRACT-BREAK" for x in rows), (text, rows)

    progressive_positives = [
        "Ветка сейчас ломается.",
        "Лёд на глазах ломается.",
        "Механизм в данный момент ломается.",
    ]
    for text in progressive_positives:
        rows = review(text)["findings"]
        assert any(x["rule_id"] == "RU-NATIVE-BREAK-STATE-TRANSITION" for x in rows), (text, rows)

    negatives = [
        "Машина часто ломается.",
        "Чугун легко ломается от удара.",
        "У подростка сейчас ломается голос.",
        "Ветки ломались под тяжестью снега.",
        "Процесс ломался на одном и том же шаге.",
        "Ветка трещит и сейчас сломается.",
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
