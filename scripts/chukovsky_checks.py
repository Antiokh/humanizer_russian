"""Chukovsky-inspired positive editing checks for humanizer+ru.

These checks are deliberately soft. They do not decide whether a construction
is "wrong" and never block publication. They surface places where the editor
can build a more direct, precise, audience-fit or better-sounding alternative
and compare it with the original.

Source model: Korney Chukovsky, "Живой как жизнь" — register fit, anti-purism,
cancelearite, lexical economy, rhythm/phonetics, and idiom integrity.
Current norm remains the responsibility of the NORM layer.
"""

from __future__ import annotations

import re
from typing import Iterable


WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)?")

# These are not stop words. A hit means: compare a version without the
# announcing phrase and keep it when it performs real discourse work.
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

# A bureaucratic register warning requires a CLUSTER across at least two
# families. A single official-looking word is deliberately insufficient.
BUREAUCRATIC_FAMILIES = {
    "deictic-paper": re.compile(
        r"\b(?:данн(?:ый|ая|ое|ые|ого|ому|ым|ой|ых)|"
        r"вышеизложенн\w*|нижеследующ\w*|вышеуказанн\w*)\b",
        re.I,
    ),
    "prepositional-frame": re.compile(
        r"\b(?:в\s+части|в\s+плане|в\s+отношении|при\s+наличии|"
        r"в\s+силу|по\s+линии|в\s+рамках|в\s+целях)\b",
        re.I,
    ),
    "existence-wrapper": re.compile(
        r"\b(?:имеет\s+место|имел[аио]?\s+место|"
        r"име(?:ется|ются)|наличи(?:е|я|ю|ем|и))\b",
        re.I,
    ),
    "official-action-family": re.compile(
        r"\b(?:осуществл\w*|обеспеч\w*|произвед\w*|производ\w*)\b",
        re.I,
    ),
}

# Unlike the broad family marker above, this check deliberately requires a
# VERBAL form followed by a nominalization. It must not flag bare noun phrases
# such as "осуществление проекта".
LIGHT_VERB_NOMINAL = re.compile(
    r"\b(?:"
    r"осуществ(?:лять|ляет|ляют|ляем|ляете|лял|ляла|ляли|ляется|ляются|лялось|лялись)|"
    r"обеспеч(?:ивать|ивает|ивают|иваем|иваете|ивал|ивала|ивали|ивается|иваются|ивалось|ивались)|"
    r"производ(?:ить|ит|ят|им|ите|ил|ила|или|ится|ятся|ился|илась|ились)"
    r")\s+"
    r"(?:[а-яё-]+\s+){0,2}"
    r"[а-яё-]+(?:ание|ания|анию|анием|аний|"
    r"ение|ения|ению|ением|ений|"
    r"ция|ции|цию|цией|ций)\b",
    re.I,
)

# Small, conservative set for a *subtraction test*. Even here the linter only
# suggests A/B comparison: context can make an apparently redundant modifier
# contrastive or restrictive.
REDUNDANT_QUALIFIERS = [
    ("достигнутые успехи", re.compile(r"\bдостигнут\w*\s+успех\w*\b", re.I)),
    ("имеющиеся ошибки", re.compile(r"\bимеющ\w*\s+ошиб\w*\b", re.I)),
    ("приглашённые гости", re.compile(r"\bприглаш[её]нн\w*\s+гост\w*\b", re.I)),
    ("главная суть", re.compile(r"\bглавн\w*\s+суть\b", re.I)),
    ("конечный итог", re.compile(r"\bконечн\w*\s+итог\w*\b", re.I)),
]

# Chukovsky's point is serial, automatic use. One occurrence is not flagged;
# the finding appears only when two or more candidate collocations occur.
STAMP_COLLOCATIONS = {
    "bright-show": re.compile(
        r"\bярк\w*\s+(?:показ\w*|раскры\w*|отраж\w*|образ\w*)\b", re.I
    ),
    "moving-image": re.compile(
        r"\bволнующ\w*\s+(?:образ\w*|гимн\w*|показ\w*)\b", re.I
    ),
    "juicy-style": re.compile(r"\bсочн\w*\s+(?:язык\w*|образ\w*)\b", re.I),
    "indelible-impression": re.compile(
        r"\bнеизгладим\w*\s+впечатлен\w*\b", re.I
    ),
    "complex-contradictory": re.compile(
        r"\bсложн\w*\s+и\s+противоречив\w*\b", re.I
    ),
    "important-role": re.compile(r"\bважн\w*\s+роль\b", re.I),
}

ABSTRACT_COLLISIONS = [
    ("наличие отсутствия", re.compile(r"\bналичи\w*\s+отсутстви\w*\b", re.I)),
    (
        "возникновение исчезновения",
        re.compile(r"\bвозникновени\w*\s+исчезновени\w*\b", re.I),
    ),
    ("сила слабости", re.compile(r"\bсил\w*\s+слабост\w*\b", re.I)),
]

QUESTION_PACKAGING = re.compile(
    r"\b(?:освет\w*|увяз\w*|проработ\w*|продвин\w*|поднять\w*|"
    r"постав\w*)\s+вопрос\w*\b",
    re.I,
)

NOMINAL_ENDING = re.compile(
    r"(?:ание|ания|анию|анием|аний|"
    r"ение|ения|ению|ением|ений|"
    r"ция|ции|цию|цией|ций)$",
    re.I,
)

LONG_CYRILLIC = re.compile(r"\b[А-Яа-яЁё-]{25,}\b")
ACRONYM = re.compile(
    r"(?<![A-Za-zА-Яа-яЁё])(?:[A-ZА-ЯЁ]{4,})(?![A-Za-zА-Яа-яЁё])"
)


def _add(findings: list[dict], rule: str, excerpt: str, note: str) -> None:
    findings.append({
        "kind": "EDITING_SUGGESTION",
        "line": 0,
        "rule": rule,
        "excerpt": excerpt[:180],
        "note": note,
    })


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _nominalizations(sentence: str) -> list[str]:
    return [word for word in _words(sentence) if NOMINAL_ENDING.search(word)]


def _phrase_hits(text_low: str, phrase: str) -> list[str]:
    """Count phrase occurrences, not merely distinct phrase types."""
    rx = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.I)
    return [match.group(0) for match in rx.finditer(text_low)]


def _suffix_echo(sentence: str) -> tuple[str, list[str]] | None:
    """Return a dense repeated 4-letter ending, if any.

    Four long words in one sentence must share the same four final letters.
    This is intentionally only a read-aloud candidate, not a quality score.
    """
    words = [word.lower() for word in _words(sentence) if len(word) >= 7]
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(word[-4:], []).append(word)
    for suffix, items in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(items) >= 4:
            return suffix, items
    return None


def check_chukovsky(prose: str, sentences: Iterable[str]) -> tuple[list[dict], dict]:
    findings: list[dict] = []
    sents = list(sentences)
    low = prose.lower()

    meta_hits: list[str] = []
    for phrase in METADISCOURSE:
        meta_hits.extend(_phrase_hits(low, phrase))
    if meta_hits:
        _add(
            findings,
            "chukovsky: metadiscourse deletion test",
            "; ".join(meta_hits[:8]),
            (
                "test a version without the announcing phrase; keep it only if it "
                "adds real modality, navigation or contrast rather than merely "
                "announcing that the next sentence is important"
            ),
        )

    bureau_hits: dict[str, list[str]] = {}
    for family, rx in BUREAUCRATIC_FAMILIES.items():
        matches = [match.group(0) for match in rx.finditer(prose)]
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
                "compare with a direct, concrete version. Keep the formal wording "
                "when the genre is genuinely official/legal or when it adds "
                "technical precision; otherwise prefer ordinary names and actions"
            ),
        )

    light_hits = [match.group(0) for match in LIGHT_VERB_NOMINAL.finditer(prose)]
    if light_hits:
        _add(
            findings,
            "chukovsky: light verb + nominalization",
            "; ".join(light_hits[:5]),
            (
                "try restoring a lexical verb (actor → action → object/result) if "
                "that preserves meaning and domain terminology; do not invent an "
                "unknown actor"
            ),
        )

    nominal_sentences = 0
    nominal_total = 0
    for sent in sents:
        noms = _nominalizations(sent)
        nominal_total += len(noms)
        if len(noms) >= 3 and len(_words(sent)) >= 10:
            nominal_sentences += 1
            _add(
                findings,
                "chukovsky: nominalization cluster",
                sent,
                (
                    f"{len(noms)} nominalizations in one sentence; test a version "
                    "with explicit actions/clauses, then compare precision and rhythm"
                ),
            )

    redundant_hits: list[str] = []
    for _, rx in REDUNDANT_QUALIFIERS:
        redundant_hits.extend(match.group(0) for match in rx.finditer(prose))
    if redundant_hits:
        _add(
            findings,
            "chukovsky: modifier subtraction candidate",
            "; ".join(redundant_hits[:6]),
            (
                "delete the modifier in a comparison copy; keep it if it changes "
                "scope, contrast, chronology, terminology, rhythm or another real "
                "meaning/function"
            ),
        )

    stamp_hits: list[str] = []
    for rx in STAMP_COLLOCATIONS.values():
        stamp_hits.extend(match.group(0) for match in rx.finditer(prose))
    if len(stamp_hits) >= 2:
        _add(
            findings,
            "chukovsky: evaluative stamp cluster",
            "; ".join(stamp_hits[:6]),
            (
                "replace generic evaluation with the text-specific proposition or "
                "observation when the source provides one; never invent missing "
                "evidence merely to escape a cliché"
            ),
        )

    collision_hits: list[str] = []
    for _, rx in ABSTRACT_COLLISIONS:
        collision_hits.extend(match.group(0) for match in rx.finditer(prose))
    if collision_hits:
        _add(
            findings,
            "chukovsky: abstract semantic collision",
            "; ".join(collision_hits[:5]),
            (
                "unpack the abstractions and state the event directly; verify the "
                "result against SEMANTICS because the original may be ironic, quoted "
                "or deliberately paradoxical"
            ),
        )

    qpack = [match.group(0) for match in QUESTION_PACKAGING.finditer(prose)]
    if len(qpack) >= 2:
        _add(
            findings,
            "chukovsky: 'question' packaging cluster",
            "; ".join(qpack[:6]),
            (
                "check whether each phrase can name the actual action directly "
                "(explain, compare, propose, decide, etc.); keep 'вопрос' where the "
                "object really is an issue/question under discussion"
            ),
        )

    long_tokens = LONG_CYRILLIC.findall(prose)
    if long_tokens:
        _add(
            findings,
            "chukovsky: opaque long compound",
            "; ".join(long_tokens[:5]),
            (
                "check pronunciation, audience recognition and whether the form "
                "actually saves reader effort; a technical term may still be fully "
                "justified"
            ),
        )

    acronyms = ACRONYM.findall(prose)
    unique_acronyms = sorted(set(acronyms))
    if len(unique_acronyms) >= 3:
        _add(
            findings,
            "chukovsky: abbreviation opacity cluster",
            "; ".join(unique_acronyms[:8]),
            (
                "for a non-specialist or new audience, consider expanding unfamiliar "
                "abbreviations on first use; do not expand established forms blindly"
            ),
        )

    echo_count = 0
    for sent in sents:
        echo = _suffix_echo(sent)
        if echo:
            echo_count += 1
            suffix, items = echo
            _add(
                findings,
                "chukovsky: suffix/ending echo",
                "; ".join(items[:8]),
                (
                    f"four or more long words end in «{suffix}»; read the sentence "
                    "aloud and revise only if the echo is accidental rather than "
                    "rhythmic, terminological or authorial"
                ),
            )

    words_total = max(1, len(_words(prose)))
    metrics = {
        "chukovsky_metadiscourse_hits": len(meta_hits),
        "chukovsky_bureaucratic_marker_hits": bureau_total,
        "chukovsky_nominalizations": nominal_total,
        "chukovsky_nominalization_sentences": nominal_sentences,
        "chukovsky_long_compounds": len(long_tokens),
        "chukovsky_unique_acronyms_4plus": len(unique_acronyms),
        "chukovsky_suffix_echo_sentences": echo_count,
        "chukovsky_nominalizations_per_100_words": round(
            nominal_total * 100 / words_total, 2
        ),
    }
    return findings, metrics


def self_test() -> None:
    text = (
        "Важно отметить, что в рамках данного проекта осуществляется "
        "обеспечение повышения эффективности реализации процесса. "
        "Автор ярко показывает конфликт, а затем ярко раскрывает тему. "
        "Мы получили достигнутые успехи."
    )
    sents = [sent.strip() for sent in re.split(r"(?<=[.!?])\s+", text) if sent.strip()]
    findings, metrics = check_chukovsky(text, sents)
    rules = {item["rule"] for item in findings}
    assert "chukovsky: metadiscourse deletion test" in rules, findings
    assert "chukovsky: bureaucratic-register cluster" in rules, findings
    assert "chukovsky: light verb + nominalization" in rules, findings
    assert "chukovsky: nominalization cluster" in rules, findings
    assert "chukovsky: evaluative stamp cluster" in rules, findings
    assert "chukovsky: modifier subtraction candidate" in rules, findings
    assert metrics["chukovsky_nominalizations"] >= 3, metrics

    # Do not confuse a nominalization noun with the light-verb construction.
    noun_phrase = "Осуществление проекта завершено. Обеспечение проекта профинансировано."
    sents = [sent.strip() for sent in re.split(r"(?<=[.!?])\s+", noun_phrase) if sent.strip()]
    findings, _ = check_chukovsky(noun_phrase, sents)
    assert not [
        item for item in findings
        if item["rule"] == "chukovsky: light verb + nominalization"
    ], findings

    # A single formal marker must not be enough to claim register leakage.
    official_single = "В рамках проекта исправили ошибку."
    findings, _ = check_chukovsky(official_single, [official_single])
    assert not [
        item for item in findings
        if item["rule"] == "chukovsky: bureaucratic-register cluster"
    ], findings

    # Count repeated metadiscourse occurrences, not only unique phrase types.
    repeated_meta = "Важно отметить одно. Важно отметить и второе."
    sents = [sent.strip() for sent in re.split(r"(?<=[.!?])\s+", repeated_meta) if sent.strip()]
    _, metrics = check_chukovsky(repeated_meta, sents)
    assert metrics["chukovsky_metadiscourse_hits"] == 2, metrics

    clean = "Вышел релиз. Исправили поиск и добавили фильтры."
    sents = [sent.strip() for sent in re.split(r"(?<=[.!?])\s+", clean) if sent.strip()]
    findings, _ = check_chukovsky(clean, sents)
    assert not findings, findings


if __name__ == "__main__":
    self_test()
    print("chukovsky self-test: OK")
