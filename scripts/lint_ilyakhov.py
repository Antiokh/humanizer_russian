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

GENERIC_PRAISE = [
    re.compile(r"\bвысок(?:ое|ого)\s+качеств[оа]\b", re.I),
    re.compile(r"\bиндивидуальн(?:ый|ого)\s+подход\b", re.I),
    re.compile(r"\bбогат(?:ый|ого)\s+опыт\b", re.I),
    re.compile(r"\bширок(?:ий|ого)\s+спектр\s+(?:услуг|решений|возможностей)\b", re.I),
    re.compile(r"\bпрофессиональн(?:ая|ой)\s+команд[аы]\b", re.I),
    re.compile(r"\bэффективн(?:ое|ые|ых)\s+решени[еяй]\b", re.I),
    re.compile(r"\bпередов(?:ые|ых)\s+технологи[ияй]\b", re.I),
    re.compile(r"\bнад[её]жн(?:ый|ого)\s+партн[её]р\b", re.I),
]

SUSPICIOUS_GENERIC_STATS = [
    re.compile(
        r"\b(?:99|100)\s*%\s+(?:всех\s+)?(?:людей|пользователей|клиентов|"
        r"сотрудников|покупателей|россиян|компаний)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:каждый|все)\s+(?:пользователь|клиент|покупатель|сотрудник)"
        r"(?:и|ы|а|ов)?\b[^.!?\n]{0,80}\b(?:экономит|получает|выбирает|доволен|"
        r"рекомендует|увеличивает|снижает)\b",
        re.I,
    ),
]

GENERIC_CONCLUSIONS = [
    re.compile(r"^\s*подводя\s+итог\b", re.I),
    re.compile(r"^\s*в\s+заключение\b", re.I),
    re.compile(r"^\s*резюмируя\b", re.I),
]

SELF_PRESENTATION_SHELLS = [
    re.compile(r"\bмы\s+(?:являемся\s+)?команд(?:а|ой)\s+(?:опытных|профессиональных|высококлассных)\b", re.I),
    re.compile(r"\bмы\s+(?:успешно\s+)?работаем\s+на\s+рынке\s+(?:более\s+)?\d+\s+лет\b", re.I),
    re.compile(r"\bнаша\s+компания\s+(?:успешно\s+)?(?:работает|существует)\s+(?:более\s+)?\d+\s+лет\b", re.I),
]

STATE_PREDICATES = [
    re.compile(r"\bявля(?:ется|ются)\b", re.I),
    re.compile(r"\bпредставля(?:ет|ют)\s+собой\b", re.I),
    re.compile(r"\bхарактеризу(?:ется|ются)\b", re.I),
    re.compile(r"\bоблада(?:ет|ют)\b", re.I),
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
            recommendation_id="ILY-R21",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="The time phrase may be an empty shell rather than real temporal information.",
            recommendation="Compare a direct opening with the actual current fact or reader task.",
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

    generic_praise_hits = all_matches(prose, GENERIC_PRAISE)
    for hit in generic_praise_hits:
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="generic-praise",
            pattern_id="ILY-09",
            recommendation_id="ILY-R18",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="A generic positive evaluation may be weaker than an available use case or detail.",
            recommendation=(
                "If the source already contains a real scenario, result, working detail or limitation, "
                "move that evidence next to or ahead of the praise."
            ),
            guard="Do not invent a scenario or erase an intentional subjective voice.",
        )

    suspicious_stat_hits = all_matches(prose, SUSPICIOUS_GENERIC_STATS)
    for hit in suspicious_stat_hits:
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="generic-precision-claim",
            pattern_id="ILY-20",
            recommendation_id="ILY-R20",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="A broad claim uses unusually strong precision without visible source context.",
            recommendation=(
                "Verify source, sample, period and measurement. Keep the number if it is sourced; "
                "otherwise narrow or attribute the claim."
            ),
            guard="This is a verification prompt, not an accusation that the number is false.",
        )

    self_presentation_hits = all_matches(prose, SELF_PRESENTATION_SHELLS)
    for hit in self_presentation_hits:
        add(
            findings,
            kind="EDITING_OPPORTUNITY",
            rule="self-presentation-shell",
            pattern_id="ILY-35",
            recommendation_id="ILY-R24",
            text=excerpt(prose, hit.start(), hit.end()),
            diagnostic="The self-description may lead with status instead of reader-relevant usefulness.",
            recommendation=(
                "Compare a lead that says plainly who you are/what you do, then surfaces useful details, "
                "scenarios, evidence and relevant limitations already present in the source."
            ),
            guard="Do not erase real credentials when they are relevant evidence.",
        )

    state_clusters = 0
    for paragraph in paragraphs(prose):
        state_hits = all_matches(paragraph, STATE_PREDICATES)
        if len(state_hits) >= 3:
            state_clusters += 1
            add(
                findings,
                kind="EDITING_OPPORTUNITY",
                rule="state-predicate-cluster",
                pattern_id="ILY-22",
                recommendation_id="ILY-R03",
                text=re.sub(r"\s+", " ", paragraph)[:180],
                diagnostic="Several state predicates may make an informational paragraph static.",
                recommendation=(
                    "Check whether any sentence hides an action, change, decision or consequence that "
                    "can be stated directly."
                ),
                guard="Definitions and stable properties legitimately use state predicates; do not force action.",
            )

    meta_lead_hits = 0
    paragraph_list = paragraphs(prose)
    for paragraph in paragraph_list:
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

    generic_conclusion_hits = 0
    if paragraph_list:
        last_paragraph = paragraph_list[-1]
        first_sentence = re.split(r"(?<=[.!?])\s+", last_paragraph, maxsplit=1)[0]
        hits = all_matches(first_sentence, GENERIC_CONCLUSIONS)
        for hit in hits:
            generic_conclusion_hits += 1
            add(
                findings,
                kind="EDITING_OPPORTUNITY",
                rule="generic-conclusion-lead",
                pattern_id="ILY-30",
                recommendation_id="ILY-R22",
                text=re.sub(r"\s+", " ", first_sentence)[:180],
                diagnostic="The conclusion announces summarizing instead of helping the reader retain or act.",
                recommendation=(
                    "Compare a useful ending: a compact system, checklist, rule, limitation or next step "
                    "already supported by the text."
                ),
                guard="Do not manufacture a conclusion when the text already ends naturally.",
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
        "generic_praise": len(generic_praise_hits),
        "generic_precision_claims": len(suspicious_stat_hits),
        "self_presentation_shells": len(self_presentation_hits),
        "state_predicate_clusters": state_clusters,
        "meta_paragraph_leads": meta_lead_hits,
        "generic_conclusion_leads": generic_conclusion_hits,
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

    findings, _ = lint("Мы предлагаем высокий уровень качества и индивидуальный подход.")
    assert any(x["recommendation_id"] == "ILY-R18" for x in findings), findings

    findings, _ = lint("99% пользователей экономят два часа каждый день.")
    assert any(x["recommendation_id"] == "ILY-R20" for x in findings), findings

    findings, _ = lint("Мы команда профессиональных инженеров. Настраиваем PostgreSQL.")
    assert any(x["recommendation_id"] == "ILY-R24" for x in findings), findings

    findings, _ = lint(
        "Система является облачной. Решение представляет собой платформу. "
        "Архитектура характеризуется модульностью."
    )
    assert any(x["rule"] == "state-predicate-cluster" for x in findings), findings

    findings, _ = lint(
        "Основные правила перечислены выше.\n\n"
        "Подводя итог, резервное копирование является важной частью работы."
    )
    assert any(x["recommendation_id"] == "ILY-R22" for x in findings), findings

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
