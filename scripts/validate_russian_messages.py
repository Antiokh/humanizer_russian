#!/usr/bin/env python3
"""Проверяет, что человекочитаемый слой humanizer_russian остаётся русским."""
from __future__ import annotations

import re

from library_runtime import run_libraries
from review import render_markdown, run_review

CYRILLIC = re.compile(r"[А-Яа-яЁё]")
FORBIDDEN_ENGLISH_FRAGMENTS = (
    "surface nominalization candidates",
    "reconstruct events/roles",
    "adjacent sentences repeat",
    "check whether",
    "compare a version",
    "review only",
    "technical trace",
    "heuristic only",
    "candidate only",
    "soft provenance signal",
)

CASES = {
    "chukovsky": (
        "В рамках данного документа осуществляется обеспечение повышения "
        "эффективности процесса."
    ),
    "native": (
        "Компания ежедневно проверяет данные проекта перед публикацией. "
        "Компания затем обновляет данные проекта после проверки редактором."
    ),
    "ilyakhov": "В данной статье мы рассмотрим три способа резервного копирования.",
    "gal": "Команда осуществила проведение проверки доступности сервиса.",
    "golub": "Согласно приказа директора встреча переносится.",
    "rosenthal": "Согласно приказа директора документ обновили.",
    "russian": "# Заголовок.\nОбычный текст продолжается здесь.",
    "visson": "Имейте хороший день!",
}


def _assert_russian_finding(library_id: str, finding: dict) -> None:
    reason = str(finding.get("reason") or "")
    label = str(finding.get("display_rule_ru") or "")
    assert CYRILLIC.search(reason), (library_id, finding)
    assert CYRILLIC.search(label), (library_id, finding)
    lowered = reason.lower()
    leaks = [fragment for fragment in FORBIDDEN_ENGLISH_FRAGMENTS if fragment in lowered]
    assert not leaks, (library_id, leaks, finding)


def validate_libraries() -> None:
    for library_id, text in CASES.items():
        findings, _ = run_libraries(text, library_ids=[library_id])
        assert findings, f"контрольный пример не вызвал находок: {library_id}"
        for finding in findings:
            _assert_russian_finding(library_id, finding)


def validate_markdown() -> None:
    report = run_review(
        CASES["chukovsky"],
        library_ids=["chukovsky"],
        register="general",
    )
    rendered = render_markdown(report)
    assert CYRILLIC.search(rendered), rendered
    for leak in (
        "### Guardrails",
        "Evidence status",
        "Evidence (не голос)",
        "SOURCE_CONFLICT",
        "SINGLE_REVIEW",
        "SHOW_ALTERNATIVES",
        " → REVIEW",
        ": REVIEW**",
    ):
        assert leak not in rendered, (leak, rendered)


def main() -> None:
    validate_libraries()
    validate_markdown()
    print("Человекочитаемые сообщения: русский слой проверен для 8 библиотек и редколлегии.")


if __name__ == "__main__":
    main()
