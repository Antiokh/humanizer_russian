#!/usr/bin/env python3
"""Distributional Russian/RKI metrics.

These signals are intentionally METRIC_ONLY. They never produce findings and
have no normative threshold. Their purpose is to support later contextual
review of explicit-subject bias, agentive-passive density and bookish copulas.
"""
from __future__ import annotations

import re
from typing import Any

CYRILLIC_WORD_RE = re.compile(r"[А-Яа-яЁё-]+")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
NOMINATIVE_PERSONAL_PRONOUN_RE = re.compile(r"(?<![А-Яа-яЁё-])(?:я|ты|он|она|оно|мы|вы|они)(?![А-Яа-яЁё-])", re.I)
# Precision-first proxy: deliberately omit the productive short-participle -т
# family because a bare final т also matches ordinary words such as документ
# and finite verbs such as лежит. Missing some -т participles is preferable to
# inflating a METRIC_ONLY signal with systematic false positives.
SHORT_PASSIVE_RE = re.compile(r"(?<![А-Яа-яЁё-])[А-Яа-яЁё]{3,}(?:ан|ян|ен|ён)(?:а|о|ы)?(?![А-Яа-яЁё-])", re.I)
AGENT_PRONOUN_RE = re.compile(r"(?<![А-Яа-яЁё-])(?:мной|нами|тобой|вами|ею|ими|кем)(?![А-Яа-яЁё-])", re.I)
YAVLYATSYA_RE = re.compile(r"(?<![А-Яа-яЁё-])явля(?:юсь|ешься|ется|емся|етесь|ются|лся|лась|лось|лись|ться|ясь|вшись)(?![А-Яа-яЁё-])", re.I)
PREDSTAVLYAT_SOBOY_RE = re.compile(r"(?<![А-Яа-яЁё-])представля(?:ет|ют|л|ла|ло|ли|ть|я)\s+собой(?![А-Яа-яЁё-])", re.I)


def _visible_text(text: str) -> str:
    lines: list[str] = []
    fenced = False
    fence_char: str | None = None
    fence_len = 0
    for raw in text.splitlines():
        stripped = raw.lstrip()
        fence = FENCE_RE.match(stripped)
        if fence:
            marker = fence.group(1)
            if not fenced:
                fenced = True
                fence_char = marker[0]
                fence_len = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fenced = False
                fence_char = None
                fence_len = 0
            # A shorter same-character marker remains content of the open fence;
            # it must not expose following code as prose, and fence lines never
            # contribute to language metrics themselves.
            continue
        if fenced:
            continue
        clean = INLINE_CODE_RE.sub(" ", raw)
        clean = URL_RE.sub(" ", clean)
        lines.append(clean)
    return "\n".join(lines)


def _per_1000(count: int, words: int) -> float:
    return round((count * 1000.0 / words), 2) if words else 0.0


def _agentive_passive_pronoun_proxy(text: str) -> int:
    """Very conservative surface proxy; deliberately misses noun agents and -т participles."""
    count = 0
    for match in SHORT_PASSIVE_RE.finditer(text):
        left = text[max(0, match.start() - 90):match.start()]
        right = text[match.end():match.end() + 90]
        if AGENT_PRONOUN_RE.search(left) or AGENT_PRONOUN_RE.search(right):
            count += 1
    return count


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    visible = _visible_text(text)
    words = len(CYRILLIC_WORD_RE.findall(visible))
    pronouns = len(NOMINATIVE_PERSONAL_PRONOUN_RE.findall(visible))
    passive_proxy = _agentive_passive_pronoun_proxy(visible)
    yavlyatsya = len(YAVLYATSYA_RE.findall(visible))
    predstavlyat = len(PREDSTAVLYAT_SOBOY_RE.findall(visible))
    bookish_copulas = yavlyatsya + predstavlyat
    return {
        "findings": [],
        "metrics": {
            "word_tokens": words,
            "nominative_personal_pronoun_proxy_tokens": pronouns,
            "nominative_personal_pronoun_proxy_per_1000": _per_1000(pronouns, words),
            "agentive_passive_pronoun_proxy_hits": passive_proxy,
            "agentive_passive_pronoun_proxy_per_1000": _per_1000(passive_proxy, words),
            "bookish_copula_proxy_hits": bookish_copulas,
            "bookish_copula_proxy_per_1000": _per_1000(bookish_copulas, words),
            "yavlyatsya_forms": yavlyatsya,
            "predstavlyat_soboy_forms": predstavlyat,
            "policy": "METRIC_ONLY: no threshold and no verdict",
        },
    }


def self_test() -> None:
    text = (
        "Я проверил файл. Мы сверили журнал. Документ подписан мной. "
        "Метод является частью системы. Система представляет собой набор модулей."
    )
    report = review(text)
    assert report["findings"] == []
    metrics = report["metrics"]
    assert metrics["nominative_personal_pronoun_proxy_tokens"] == 2, metrics
    assert metrics["agentive_passive_pronoun_proxy_hits"] >= 1, metrics
    assert metrics["yavlyatsya_forms"] == 1, metrics
    assert metrics["predstavlyat_soboy_forms"] == 1, metrics

    active_t = review("Документ лежит перед нами.")
    assert active_t["metrics"]["agentive_passive_pronoun_proxy_hits"] == 0, active_t

    masked = review("`Я являюсь тестом` https://example.com/является")
    assert masked["metrics"]["nominative_personal_pronoun_proxy_tokens"] == 0, masked
    assert masked["metrics"]["bookish_copula_proxy_hits"] == 0, masked

    long_fence = review(
        "````text\n"
        "Я являюсь тестом.\n"
        "```\n"
        "Мы являемся тестом.\n"
        "````\n"
        "Я являюсь вне кода."
    )
    assert long_fence["metrics"]["nominative_personal_pronoun_proxy_tokens"] == 1, long_fence
    assert long_fence["metrics"]["yavlyatsya_forms"] == 1, long_fence


if __name__ == "__main__":
    self_test()
    print("Russian RKI metrics: OK")
