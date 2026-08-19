"""Conservative surface candidates derived from the independent Chukovsky study.

These checks never decide that a construction is wrong, AI-generated, insincere,
or outside current norm. They only point to places where a human/model editor can
run an explicit comparison test from references/chukovsky.md.

Exit status and publication gating remain the responsibility of scripts/lint.py;
these findings are always EDITING_SUGGESTION.
"""

from __future__ import annotations

from collections import Counter
import re
from typing import Iterable


WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)?")

METADISCOURSE = [
    "важно отметить",
    "стоит отметить",
    "следует отметить",
    "необходимо отметить",
    "нужно отметить",
    "нельзя не отметить",
    "приходится отметить",
    "следует подчеркнуть",
    "необходимо подчеркнуть",
    "следует указать",
    "необходимо указать",
    "нельзя не признать",
]

BUREAUCRATIC_FAMILIES = {
    "paper-deictic": re.compile(
        r"\b(?:данн(?:ый|ая|ое|ые|ого|ому|ым|ой|ых)|"
        r"вышеизложенн\w*|нижеследующ\w*|вышеуказанн\w*)\b",
        re.I,
    ),
    "procedural-frame": re.compile(
        r"\b(?:в\s+части|в\s+плане|в\s+отношении|при\s+наличии|"
        r"по\s+линии|в\s+рамках|в\s+целях)\b",
        re.I,
    ),
    "existence-wrapper": re.compile(
        r"\b(?:имеет\s+место|имел[аио]?\s+место|имеются?)\b",
        re.I,
    ),
    "official-action": re.compile(
        r"\b(?:осуществл\w*|обеспеч\w*|производ\w*|проведен\w*|"
        r"проводит(?:ся|ь|е|еся|ся)?|реализ\w*)\b",
        re.I,
    ),
}

# Require a verbal/light-verb form followed by a deverbal noun. Bare
# "осуществление проекта" must not match this rule.
LIGHT_VERB_NOMINAL = re.compile(
    r"\b(?:осуществля(?:ется|ются|л(?:ся|ась|ись)?|ть)|"
    r"обеспечива(?:ется|ются|л(?:ся|ась|ись)?|ть)|"
    r"производи(?:тся|ятся|л(?:ся|ась|ись)?|ть)|"
    r"проводи(?:тся|ятся|л(?:ся|ась|ись)?|ть))\s+"
    r"(?:[а-яё-]+\s+){0,2}"
    r"[а-яё-]+(?:ание|ания|анию|анием|аний|"
    r"ение|ения|ению|ением|ений|"
    r"ация|ации|ацию|ацией|аций|"
    r"изация|изации|изацию|изацией|изаций)\b",
    re.I,
)

# These are deliberately candidates, not a dictionary of pleonasms.
MODIFIER_CANDIDATES = [
    re.compile(r"\bимеющ\w*\s+ошиб\w*\b", re.I),
    re.compile(r"\bдостигнут\w*\s+успех\w*\b", re.I),
    re.compile(r"\bприглаш[её]нн\w*\s+гост\w*\b", re.I),
    re.compile(r"\bглавн\w*\s+суть\b", re.I),
    re.compile(r"\bконечн\w*\s+итог\w*\b", re.I),
]

STAMP_COLLOCATIONS = [
    re.compile(r"\bярк\w*\s+(?:показ\w*|раскры\w*|отраж\w*|образ\w*)\b", re.I),
    re.compile(r"\bволнующ\w*\s+(?:образ\w*|показ\w*|произведен\w*)\b", re.I),
    re.compile(r"\bнеизгладим\w*\s+впечатлен\w*\b", re.I),
    re.compile(r"\bсложн\w*\s+и\s+противоречив\w*\b", re.I),
    re.compile(r"\bважн\w*\s+роль\b", re.I),
]

ABSTRACT_COLLISIONS = [
    re.compile(r"\bналичи\w*\s+отсутстви\w*\b", re.I),
    re.compile(r"\bвозникновени\w*\s+исчезновени\w*\b", re.I),
    re.compile(r"\bсил\w*\s+слабост\w*\b", re.I),
]

QUESTION_PACKAGING = re.compile(
    r"\b(?:освет\w*|увяз\w*|проработ\w*|продвин\w*|поднять\w*|"
    r"постав\w*)\s+вопрос\w*\b",
    re.I,
)

NOMINAL_ENDING = re.compile(
    r"(?:ание|ания|анию|анием|аний|"
    r"ение|ения|ению|ением|ений|"
    r"ация|ации|ацию|ацией|аций|"
    r"изация|изации|изацию|изацией|изаций)$",
    re.I,
)

ACRONYM = re.compile(
    r"(?<![A-Za-zА-Яа-яЁё])(?:[A-ZА-ЯЁ]{4,})(?![A-Za-zА-Яа-яЁё])"
)


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _nominalizations(sentence: str) -> list[str]:
    return [word for word in _words(sentence) if NOMINAL_ENDING.search(word)]


def _add(findings: list[dict], rule: str, excerpt: str, note: str) -> None:
    findings.append({
        "kind": "EDITING_SUGGESTION",
        "line": 0,
        "rule": rule,
        "excerpt": excerpt[:180],
        "note": note,
    })


def _suffix_echo(sentence: str) -> tuple[str, list[str]] | None:
    """Return a dense repeated ending candidate, never a euphony verdict."""
    words = [word.lower() for word in _words(sentence) if len(word) >= 7]
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(word[-4:], []).append(word)
    for suffix, items in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(items) >= 4:
            return suffix, items
    return None


def check_chukovsky(
    prose: str,
    sentences: Iterable[str],
) -> tuple[list[dict], dict]:
    findings: list[dict] = []
    sents = list(sentences)
    low = prose.lower()

    # A/B deletion test, not an AI attribution.
    meta_occurrences: list[str] = []
    for phrase in METADISCOURSE:
        count = low.count(phrase)
        meta_occurrences.extend([phrase] * count)
    if meta_occurrences:
        _add(
            findings,
            "chukovsky: metadiscourse deletion test",
            "; ".join(meta_occurrences[:8]),
            (
                "compare a version without the announcing frame; keep it when it "
                "adds real modality, warning hierarchy, navigation or contrast"
            ),
        )

    # Surface register markers need a cluster across at least two families.
    bureau_hits: dict[str, list[str]] = {}
    for family, rx in BUREAUCRATIC_FAMILIES.items():
        matches = [m.group(0) for m in rx.finditer(prose)]
        if matches:
            bureau_hits[family] = matches
    bureau_total = sum(len(items) for items in bureau_hits.values())
    if bureau_total >= 3 and len(bureau_hits) >= 2:
        excerpt = "; ".join(
            f"{family}: {', '.join(items[:3])}"
            for family, items in bureau_hits.items()
        )
        _add(
            findings,
            "chukovsky: bureaucratic-register cluster",
            excerpt,
            (
                "run register-fit and direct-language tests; preserve the wording "
                "when the genre is genuinely official/legal/technical"
            ),
        )

    light_hits = [m.group(0) for m in LIGHT_VERB_NOMINAL.finditer(prose)]
    if light_hits:
        _add(
            findings,
            "chukovsky: light verb + nominalization",
            "; ".join(light_hits[:6]),
            (
                "try recovering actor → action → object/result; do not invent an "
                "unknown actor and do not ban nominalization as a class"
            ),
        )

    nominal_total = 0
    nominal_sentences = 0
    for sentence in sents:
        noms = _nominalizations(sentence)
        nominal_total += len(noms)
        if len(noms) >= 3 and len(_words(sentence)) >= 10:
            nominal_sentences += 1
            _add(
                findings,
                "chukovsky: nominalization cluster",
                sentence,
                (
                    f"{len(noms)} surface nominalization candidates; reconstruct "
                    "events/roles before deciding whether the sentence is actually heavy"
                ),
            )

    modifier_hits: list[str] = []
    for rx in MODIFIER_CANDIDATES:
        modifier_hits.extend(m.group(0) for m in rx.finditer(prose))
    if modifier_hits:
        _add(
            findings,
            "chukovsky: modifier subtraction candidate",
            "; ".join(modifier_hits[:6]),
            (
                "compare with the modifier removed; keep it if scope, contrast, "
                "degree, chronology, stance, terminology or prosody changes"
            ),
        )

    stamp_hits: list[str] = []
    for rx in STAMP_COLLOCATIONS:
        stamp_hits.extend(m.group(0) for m in rx.finditer(prose))
    if len(stamp_hits) >= 2:
        _add(
            findings,
            "chukovsky: evaluative-template cluster",
            "; ".join(stamp_hits[:8]),
            (
                "inspect repeated discourse function; prefer a source-supported "
                "proposition/observation where available, never invented specificity"
            ),
        )

    collision_hits: list[str] = []
    for rx in ABSTRACT_COLLISIONS:
        collision_hits.extend(m.group(0) for m in rx.finditer(prose))
    if collision_hits:
        _add(
            findings,
            "chukovsky: fresh abstract collision candidate",
            "; ".join(collision_hits[:6]),
            (
                "unpack the event in plain language and verify polarity/roles; an "
                "established lexicalized expression would need separate treatment"
            ),
        )

    question_hits = [m.group(0) for m in QUESTION_PACKAGING.finditer(prose)]
    if len(question_hits) >= 2:
        _add(
            findings,
            "chukovsky: repeated 'question' packaging",
            "; ".join(question_hits[:8]),
            (
                "check whether the actual speech acts can be named directly; keep "
                "вопрос where the referent genuinely is an issue/topic/question"
            ),
        )

    unique_acronyms = sorted(set(ACRONYM.findall(prose)))
    if len(unique_acronyms) >= 3:
        _add(
            findings,
            "chukovsky: abbreviation-density candidate",
            "; ".join(unique_acronyms[:10]),
            (
                "for a new/non-specialist audience, test first-use expansion and "
                "reader effort; established domain abbreviations may be optimal"
            ),
        )

    echo_sentences = 0
    for sentence in sents:
        echo = _suffix_echo(sentence)
        if not echo:
            continue
        echo_sentences += 1
        suffix, items = echo
        _add(
            findings,
            "chukovsky: ending-echo read-aloud test",
            "; ".join(items[:8]),
            (
                f"four or more long words share final «{suffix}»; read aloud and "
                "revise only if the echo is accidental rather than technical or expressive"
            ),
        )

    words_total = max(1, len(_words(prose)))
    metrics = {
        "chukovsky_metadiscourse_occurrences": len(meta_occurrences),
        "chukovsky_bureaucratic_marker_hits": bureau_total,
        "chukovsky_nominalizations": nominal_total,
        "chukovsky_nominalization_sentences": nominal_sentences,
        "chukovsky_nominalizations_per_100_words": round(
            nominal_total * 100 / words_total, 2
        ),
        "chukovsky_unique_acronyms_4plus": len(unique_acronyms),
        "chukovsky_ending_echo_sentences": echo_sentences,
    }
    return findings, metrics


def self_test() -> None:
    text = (
        "Важно отметить, что в рамках данного проекта осуществляется "
        "обеспечение повышения эффективности реализации процесса. "
        "Автор ярко показывает конфликт, затем автор ярко раскрывает тему. "
        "Мы исправим имеющиеся ошибки."
    )
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    findings, metrics = check_chukovsky(text, sents)
    rules = {item["rule"] for item in findings}
    assert "chukovsky: metadiscourse deletion test" in rules, findings
    assert "chukovsky: bureaucratic-register cluster" in rules, findings
    assert "chukovsky: light verb + nominalization" in rules, findings
    assert "chukovsky: evaluative-template cluster" in rules, findings
    assert "chukovsky: modifier subtraction candidate" in rules, findings
    assert metrics["chukovsky_metadiscourse_occurrences"] == 1, metrics

    # A bare process noun must not satisfy the light-verb check.
    findings, _ = check_chukovsky("Осуществление проекта началось.", ["Осуществление проекта началось."])
    assert not [
        item for item in findings
        if item["rule"] == "chukovsky: light verb + nominalization"
    ], findings

    # One formal marker is insufficient for a register-cluster verdict.
    findings, _ = check_chukovsky("В рамках проекта всё готово.", ["В рамках проекта всё готово."])
    assert not [
        item for item in findings
        if item["rule"] == "chukovsky: bureaucratic-register cluster"
    ], findings


if __name__ == "__main__":
    self_test()
    print("chukovsky self-test: OK")
