#!/usr/bin/env python3
"""Experimental surface linter for the Ilyakhov EDITING layer.

This module intentionally implements only patterns that can be surfaced with
reasonable lexical/syntactic heuristics. It is not a "stop-word deleter" and
never blocks publication.

All findings are STYLE_WARNING candidates. The model/editor must still check:
SEMANTICS -> NORM -> AUTHOR -> NATIVE_USAGE -> EDITING.

Source-derived pattern cards live in knowledge/ilyakhov-patterns.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


URL_OR_CODE = re.compile(r"```.*?```|`[^`\n]+`|https?://\S+", re.S)

COMMON_KNOWLEDGE = [
    re.compile(r"\bкак\s+известно\b", re.I),
    re.compile(r"\bне\s+секрет\b", re.I),
    re.compile(r"\bни\s+для\s+кого\s+не\s+секрет\b", re.I),
    re.compile(r"\bвсем\s+известно\b", re.I),
    re.compile(r"\bобщеизвестно\b", re.I),
]

VERBAL_NUMBERING = [
    re.compile(r"\bво-первых\b", re.I),
    re.compile(r"\bво-вторых\b", re.I),
    re.compile(r"\bв-третьих\b", re.I),
    re.compile(r"\bв-четв[её]ртых\b", re.I),
    re.compile(r"\bнаконец\b", re.I),
]

FORMAL_POLITENESS = [
    re.compile(r"\bбудьте\s+так\s+добры\b", re.I),
    re.compile(r"\bесли\s+не\s*сложно\b", re.I),
    re.compile(r"\bизвините\s+за\s+беспокойство\b", re.I),
    re.compile(r"\bзаранее\s+спасибо\b", re.I),
    re.compile(r"\bне\s+сочтите\s+за\s+труд\b", re.I),
]

INTENSIFIERS = [
    re.compile(r"\bабсолютно\b", re.I),
    re.compile(r"\bсовершенно\b", re.I),
    re.compile(r"\bмаксимально\b", re.I),
    re.compile(r"\bкрайне\b", re.I),
    re.compile(r"\bневероятно\b", re.I),
    re.compile(r"\bисключительно\b", re.I),
    re.compile(r"\bчрезвычайно\b", re.I),
    re.compile(r"\bфеноменально\b", re.I),
]

TIME_WRAPPERS = [
    re.compile(r"\bна\s+сегодняшний\s+день\b", re.I),
    re.compile(r"\bв\s+настоящее\s+время\b", re.I),
    re.compile(r"\bна\s+данный\s+момент\b", re.I),
    re.compile(r"\bсегодня\s+как\s+никогда\b", re.I),
    re.compile(r"\bв\s+современном\s+мире\b", re.I),
    re.compile(r"\bв\s+наши\s+дни\b", re.I),
]

# These thresholds are triage heuristics, not language norms.
LONG_CORRELATIVES = [
    (
        "не только … но и",
        "ILY-28",
        re.compile(r"\bне\s+только\b(?P<middle>.{70,}?)\bно\s+и\b", re.I | re.S),
    ),
    (
        "как … так и",
        "ILY-28",
        re.compile(r"\bкак\b(?P<middle>.{70,}?)\bтак\s+и\b", re.I | re.S),
    ),
    (
        "если … то",
        "ILY-28",
        re.compile(r"\bесли\b(?P<middle>.{100,}?)\bто\b", re.I | re.S),
    ),
]


def prose_text(text: str) -> str:
    """Remove code/URLs but keep prose and paragraph boundaries."""
    return URL_OR_CODE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def excerpt(text: str, start: int, end: int, limit: int = 180) -> str:
    left = max(0, start - 40)
    right = min(len(text), end + 70)
    value = re.sub(r"\s+", " ", text[left:right]).strip()
    if len(value) > limit:
        value = value[: limit - 1] + "…"
    return value


def add(findings: list[dict], rule: str, pattern_id: str, text: str, note: str) -> None:
    findings.append(
        {
            "kind": "STYLE_WARNING",
            "rule": rule,
            "pattern_id": pattern_id,
            "excerpt": text,
            "note": note,
        }
    )


def all_matches(text: str, regexes: list[re.Pattern]) -> list[re.Match]:
    hits: list[re.Match] = []
    for rx in regexes:
        hits.extend(rx.finditer(text))
    return sorted(hits, key=lambda m: m.start())


def lint(text: str) -> tuple[list[dict], dict]:
    prose = prose_text(text)
    findings: list[dict] = []

    common_hits = all_matches(prose, COMMON_KNOWLEDGE)
    for hit in common_hits:
        add(
            findings,
            "common-knowledge wrapper",
            "ILY-03",
            excerpt(prose, hit.start(), hit.end()),
            (
                "Check function. Remove only if the wrapper merely declares a claim "
                "obvious; do not turn an unsupported claim into fact."
            ),
        )

    numbering_hits = all_matches(prose, VERBAL_NUMBERING)
    if len(numbering_hits) >= 2:
        add(
            findings,
            "verbal-numbering cluster",
            "ILY-05",
            " | ".join(hit.group(0) for hit in numbering_hits[:6]),
            (
                "If this is not an instruction or a list whose items need references, "
                "compare paragraphs/a real list/natural transitions."
            ),
        )

    politeness_hits = all_matches(prose, FORMAL_POLITENESS)
    if len(politeness_hits) >= 2:
        add(
            findings,
            "formal-politeness cluster",
            "ILY-07",
            " | ".join(hit.group(0) for hit in politeness_hits[:6]),
            (
                "Keep normal politeness. Check whether reason, deadline, attachment "
                "or next step would help the reader more than repeated formulas."
            ),
        )

    # Intensifiers are flagged only when clustered. One emphatic word is not a problem.
    sentences = [
        s.strip()
        for s in re.split(r"(?<=[.!?])\s+|\n+", prose)
        if s.strip()
    ]
    intensifier_clusters = 0
    for sentence in sentences:
        hits = all_matches(sentence, INTENSIFIERS)
        if len(hits) >= 2:
            intensifier_clusters += 1
            add(
                findings,
                "intensifier cluster",
                "ILY-10",
                re.sub(r"\s+", " ", sentence)[:180],
                (
                    "Check whether modifiers carry measurable meaning or merely amplify "
                    "an evaluation. Do not invent evidence."
                ),
            )

    time_hits = all_matches(prose, TIME_WRAPPERS)
    for hit in time_hits:
        add(
            findings,
            "present-time wrapper",
            "ILY-12",
            excerpt(prose, hit.start(), hit.end()),
            (
                "Soft candidate only. Keep it when a real past/present/future contrast "
                "or dating function depends on the marker."
            ),
        )

    long_correlative_hits = 0
    for label, pattern_id, rx in LONG_CORRELATIVES:
        for hit in rx.finditer(prose):
            long_correlative_hits += 1
            add(
                findings,
                f"long correlative: {label}",
                pattern_id,
                excerpt(prose, hit.start(), hit.end()),
                (
                    "Distance is a cognitive-load heuristic, not a grammar rule. "
                    "Short transparent correlatives must remain untouched."
                ),
            )

    metrics = {
        "common_knowledge": len(common_hits),
        "verbal_numbering_markers": len(numbering_hits),
        "formal_politeness_markers": len(politeness_hits),
        "intensifier_clusters": intensifier_clusters,
        "time_wrappers": len(time_hits),
        "long_correlatives": long_correlative_hits,
    }
    return findings, metrics


def self_test() -> None:
    findings, _ = lint("Как известно, отчёт готов.")
    assert any(x["pattern_id"] == "ILY-03" for x in findings), findings

    findings, _ = lint(
        "Во-первых, проверим данные. Во-вторых, сравним версии. В-третьих, отправим."
    )
    assert any(x["pattern_id"] == "ILY-05" for x in findings), findings

    findings, _ = lint(
        "Пожалуйста, пришлите договор. Если несложно, сегодня. Заранее спасибо."
    )
    assert any(x["pattern_id"] == "ILY-07" for x in findings), findings

    findings, _ = lint("Это абсолютно невероятно удобный отчёт.")
    assert any(x["pattern_id"] == "ILY-10" for x in findings), findings

    findings, _ = lint("На сегодняшний день сервис работает в Сербии.")
    assert any(x["pattern_id"] == "ILY-12" for x in findings), findings

    long_middle = " данные," + " которые пришлось сверять вручную" * 4
    findings, _ = lint(
        "Мы не только проверили" + long_middle + ", но и исправили связи."
    )
    assert any(x["pattern_id"] == "ILY-28" for x in findings), findings

    # Negative tests: these are explicitly not automatic Ilyakhov findings.
    safe = (
        "Мне кажется, срок изменится. "
        "Он не только нашёл ошибку, но и исправил её. "
        "Мы переделали форму (наконец-то). "
        "Клиенты, оплатившие счёт до пятницы, получат доступ в понедельник. "
        "Воду отключат в десять."
    )
    findings, _ = lint(safe)
    assert not findings, findings

    print("self-test: OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    findings, metrics = lint(text)

    if args.as_json:
        print(
            json.dumps(
                {"findings": findings, "metrics": metrics},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if findings:
            for finding in findings:
                print(
                    f"{finding['kind']:14} {finding['pattern_id']:6} "
                    f"{finding['rule']}: {finding['excerpt']}"
                )
                print(f"  {finding['note']}")
        else:
            print("no conservative Ilyakhov surface candidates")

        print("\nmetrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")

        print("\nnon-gating: every finding requires contextual review")


if __name__ == "__main__":
    main()
