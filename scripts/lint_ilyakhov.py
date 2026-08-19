#!/usr/bin/env python3
"""Non-gating surface linter for the Ilyakhov/Sarycheva EDITING layer.

The linter has two outputs:

- STYLE_WARNING: a surface pattern worth checking;
- EDITING_OPPORTUNITY: a conservative trigger for a positive editing operation.

It never edits automatically and never blocks publication. Full recommendations
live in knowledge/ilyakhov-recommendations.json. Source-derived diagnostic cards
live in knowledge/ilyakhov-patterns.json.

Priority remains:
SEMANTICS -> NORM -> AUTHOR -> NATIVE_USAGE -> EDITING.
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

# High-precision-ish surface hints for positive operations. These do not mean
# the full ILY pattern is automatable; they merely expose places worth comparing.
BUREAUCRATIC_ACTION_SHELLS = [
    re.compile(
        r"\bв\s+рамках\s+(?:проведения|осуществления|реализации|выполнения|мероприятий|работ)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:было|была|были|будет|будут)\s+(?:осуществлен[оаы]?|произведен[оаы]?|выполнен[оаы]?|проведен[оаы]?)\b",
        re.I,
    ),
    re.compile(r"\bосуществля(?:ется|ются|лось|лись)\s+(?:работ|мероприяти|деятельност)", re.I),
]

NOMINALIZATION_SHELLS = [
    re.compile(
        r"\b(?:осуществить|осуществлять|произвести|производить|выполнить|выполнять|провести|проводить)\s+"
        r"(?:[а-яё-]+\s+){0,2}[а-яё-]+(?:ние|ния|цию|ции|ку|ки)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:осуществление|проведение|выполнение|производство)\s+"
        r"(?:[а-яё-]+\s+){0,2}[а-яё-]+(?:ния|ции|ки)\b",
        re.I,
    ),
]

COGNITIVE_FRAMES = [
    re.compile(r"\b(?:я|мы)\s+(?:считаю|считаем|полагаю|полагаем|думаю|думаем),?\s+что\b", re.I),
    re.compile(r"\bследует\s+отметить,?\s+что\b", re.I),
    re.compile(r"\bважно\s+(?:отметить|понимать),?\s+что\b", re.I),
    re.compile(r"\bможно\s+сказать,?\s+что\b", re.I),
]

META_LEADS = [
    re.compile(r"^\s*в\s+(?:этой|данной)\s+(?:статье|главе|части|разделе)\b", re.I),
    re.compile(r"^\s*далее\s+(?:мы\s+)?(?:рассмотрим|разбер[её]м|обсудим)\b", re.I),
    re.compile(r"^\s*теперь\s+(?:мы\s+)?(?:рассмотрим|разбер[её]м|перейд[её]м)\b", re.I),
    re.compile(r"^\s*перейд[её]м\s+к\b", re.I),
    re.compile(r"^\s*(?:для\s+начала|прежде\s+всего)\s+(?:рассмотрим|отметим|разбер[её]м)\b", re.I),
]

# These thresholds are implementation triage heuristics, not claims from the book
# and not Russian-language norms.
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
    """Remove code/URLs while retaining prose and paragraph boundaries."""
    return URL_OR_CODE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def excerpt(text: str, start: int, end: int, limit: int = 180) -> str:
    left = max(0, start - 40)
    right = min(len(text), end + 70)
    value = re.sub(r"\s+", " ", text[left:right]).strip()
    if len(value) > limit:
        value = value[: limit - 1] + "…"
    return value


def add(
    findings: list[dict],
    *,
    kind: str,
    rule: str,
    pattern_id: str,
    text: str,
    diagnostic: str,
    recommendation: str,
    guard: str,
    recommendation_id: str | None = None,
) -> None:
    findings.append(
        {
            "kind": kind,
            "rule": rule,
            "pattern_id": pattern_id,
            "recommendation_id": recommendation_id,
            "excerpt": text,
            "diagnostic": diagnostic,
            "recommendation": recommendation,
            "guard": guard,
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
            kind="STYLE_WARNING",
            rule="common-knowledge wrapper",
            pattern_id="ILY-03",
            recommendation_id="ILY-R02",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="The phrase may announce obviousness instead of supporting the claim.",
            recommendation=(
                "Compare a version without the wrapper. If the claim needs persuasion, "
                "surface an existing fact/source/observation or explicitly attribute the opinion."
            ),
            guard="Do not turn an unsupported claim into fact.",
        )

    numbering_hits = all_matches(prose, VERBAL_NUMBERING)
    if len(numbering_hits) >= 2:
        add(
            findings,
            kind="STYLE_WARNING",
            rule="verbal-numbering cluster",
            pattern_id="ILY-05",
            text=" | ".join(hit.group(0) for hit in numbering_hits[:6]),
            diagnostic="The prose may be using spoken navigation where written structure can carry it.",
            recommendation=(
                "If items do not need stable references, compare paragraphs, a real list, "
                "or direct transitions. Keep numbering for algorithms and referenced steps."
            ),
            guard="Do not erase an actual sequence or cross-reference structure.",
        )

    politeness_hits = all_matches(prose, FORMAL_POLITENESS)
    if len(politeness_hits) >= 2:
        add(
            findings,
            kind="STYLE_WARNING",
            rule="formal-politeness cluster",
            pattern_id="ILY-07",
            text=" | ".join(hit.group(0) for hit in politeness_hits[:6]),
            diagnostic="Several politeness formulas may be crowding out practical help.",
            recommendation=(
                "Keep one natural politeness signal and move the reason, deadline, attachment "
                "or next step forward when those facts already exist."
            ),
            guard="Brevity must not make the message rude.",
        )

    sentence_list = [
        s.strip()
        for s in re.split(r"(?<=[.!?])\s+|\n+", prose)
        if s.strip()
    ]
    intensifier_clusters = 0
    for sentence in sentence_list:
        hits = all_matches(sentence, INTENSIFIERS)
        if len(hits) >= 2:
            intensifier_clusters += 1
            add(
                findings,
                kind="STYLE_WARNING",
                rule="intensifier cluster",
                pattern_id="ILY-10",
                recommendation_id="ILY-R02",
                text=re.sub(r"\s+", " ", sentence)[:180],
                diagnostic="Several modifiers may be amplifying an evaluation rather than supporting it.",
                recommendation=(
                    "If the source already contains a result, fact, example or observation, "
                    "let that carry the evaluation. Otherwise keep the claim appropriately subjective."
                ),
                guard="Do not invent evidence; one intentional intensifier is not a defect.",
            )

    time_hits = all_matches(prose, TIME_WRAPPERS)
    for hit in time_hits:
        add(
            findings,
            kind="STYLE_WARNING",
            rule="present-time wrapper",
            pattern_id="ILY-12",
            recommendation_id="ILY-R04",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="The time phrase may be an empty shell rather than real temporal information.",
            recommendation="Compare a direct version that begins with the actual current fact.",
            guard="Keep the marker when past/present/future contrast or dating depends on it.",
        )

    long_correlative_hits = 0
    for label, pattern_id, rx in LONG_CORRELATIVES:
        for hit in rx.finditer(prose):
            long_correlative_hits += 1
            add(
                findings,
                kind="STYLE_WARNING",
                rule=f"long correlative: {label}",
                pattern_id=pattern_id,
                recommendation_id="ILY-R04",
                text=excerpt(prose, hit.start(), hit.end()),
                diagnostic="The reader may have to retain the first half of the construction for too long.",
                recommendation=(
                    "Compare a shorter dependency, two transparent clauses, or a reordered sentence "
                    "that closes the relation earlier."
                ),
                guard="Distance is a triage heuristic; short transparent correlatives stay untouched.",
            )

    bureaucracy_hits = all_matches(prose, BUREAUCRATIC_ACTION_SHELLS)
    for hit in bureaucracy_hits:
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="bureaucratic-action-shell",
            pattern_id="ILY-13",
            recommendation_id="ILY-R03",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="A bureaucratic shell may be hiding the event itself.",
            recommendation=(
                "Extract the actual action and try a direct verb. Name the actor only if responsibility "
                "or causality requires it."
            ),
            guard="Legal/procedural wording and exact responsibility can outrank simplification.",
        )

    nominalization_hits = all_matches(prose, NOMINALIZATION_SHELLS)
    bureaucracy_spans = [(m.start(), m.end()) for m in bureaucracy_hits]
    for hit in nominalization_hits:
        if any(not (hit.end() <= a or hit.start() >= b) for a, b in bureaucracy_spans):
            continue
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="nominalization-shell",
            pattern_id="ILY-16",
            recommendation_id="ILY-R03",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="A shell verb + action noun may make a simple action harder to see.",
            recommendation="Compare a direct verb that expresses the same action.",
            guard="Keep terminology where the noun names a real domain concept; do not invent an actor.",
        )

    frame_hits = all_matches(prose, COGNITIVE_FRAMES)
    for hit in frame_hits:
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="cognitive-frame-wrapper",
            pattern_id="ILY-27",
            recommendation_id="ILY-R04",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="A cognitive frame may delay the proposition that carries the useful information.",
            recommendation=(
                "Compare a version that brings the proposition forward. Preserve the frame when it "
                "marks attribution, uncertainty, responsibility or the author's stance."
            ),
            guard="Do not strip real uncertainty; 'мне кажется' and self-correction are not automatic findings.",
        )

    meta_lead_hits = 0
    for paragraph in paragraphs(prose):
        first_sentence = re.split(r"(?<=[.!?])\s+", paragraph, maxsplit=1)[0]
        hits = all_matches(first_sentence, META_LEADS)
        for hit in hits:
            meta_lead_hits += 1
            add(
                findings,
                kind="EDITING_OPPORTUNITY",
                rule="meta-paragraph-lead",
                pattern_id="ILY-30",
                recommendation_id="ILY-R08",
                text=re.sub(r"\s+", " ", first_sentence)[:180],
                diagnostic="The paragraph starts by announcing the topic instead of delivering it.",
                recommendation=(
                    "For informational prose, compare a lead with the thesis, decision, action, benefit "
                    "or concrete fact that makes the paragraph worth reading."
                ),
                guard="Do not force a business lead onto narrative, dialogue or an intentional hook.",
            )

    metrics = {
        "style_warnings": sum(x["kind"] == "STYLE_WARNING" for x in findings),
        "editing_opportunities": sum(x["kind"] == "EDITING_OPPORTUNITY" for x in findings),
        "common_knowledge": len(common_hits),
        "verbal_numbering_markers": len(numbering_hits),
        "formal_politeness_markers": len(politeness_hits),
        "intensifier_clusters": intensifier_clusters,
        "time_wrappers": len(time_hits),
        "long_correlatives": long_correlative_hits,
        "bureaucratic_action_shells": len(bureaucracy_hits),
        "nominalization_shells": len(nominalization_hits),
        "cognitive_frames": len(frame_hits),
        "meta_paragraph_leads": meta_lead_hits,
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

    findings, _ = lint("В рамках проведения проверки было осуществлено выявление трёх ошибок.")
    assert any(x["kind"] == "EDITING_OPPORTUNITY" and x["recommendation_id"] == "ILY-R03" for x in findings), findings

    findings, _ = lint("Мы провели осуществление оптимизации процесса согласования.")
    assert any(x["pattern_id"] == "ILY-16" for x in findings), findings

    findings, _ = lint("Я считаю, что перенос нужно сделать ночью.")
    assert any(x["pattern_id"] == "ILY-27" for x in findings), findings

    findings, _ = lint(
        "В данной статье мы рассмотрим резервное копирование. Бэкап запускается каждую ночь."
    )
    assert any(x["recommendation_id"] == "ILY-R08" for x in findings), findings

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
        print(json.dumps({"findings": findings, "metrics": metrics}, ensure_ascii=False, indent=2))
    else:
        if findings:
            for finding in findings:
                rec = f" -> {finding['recommendation_id']}" if finding["recommendation_id"] else ""
                print(
                    f"{finding['kind']:20} {finding['pattern_id']:6}{rec:12} "
                    f"{finding['rule']}: {finding['excerpt']}"
                )
                print(f"  why: {finding['diagnostic']}")
                print(f"  try: {finding['recommendation']}")
                print(f"  guard: {finding['guard']}")
        else:
            print("no conservative Ilyakhov surface candidates")

        print("\nmetrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")

        print("\nnon-gating: every finding requires contextual review")


if __name__ == "__main__":
    main()
