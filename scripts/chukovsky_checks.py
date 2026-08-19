"""Chukovsky-inspired positive editing checks for humanizer+ru.

These are deliberately soft. They do not decide whether a construction is
"wrong"; they surface places where a more direct, precise, audience-fit or
better-sounding Russian variant may exist.

The source model is Korney Chukovsky's "Живой как жизнь": register fit,
anti-purism, cancelearite, lexical economy, rhythm/phonetics, and idiom
integrity. Current norm still belongs to the NORM layer.
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
        r"\b(?:имеет\s+место|имел[аио]?\s+место|имеются?|наличи[еяю])\b",
        re.I,
    ),
    "official-action": re.compile(
        r"\b(?:осуществл\w*|обеспеч\w*|произвед\w*|производ\w*)\b",
        re.I,
    ),
}

LIGHT_VERB_NOMINAL = re.compile(
    r"\b(?:осуществл\w*|обеспеч\w*|производ\w*)\s+"
    r"(?:[а-яё-]+\s+){0,2}"
    r"[а-яё-]+(?:ание|ания|анию|анием|аний|"
    r"ение|ения|ению|ением|ений|"
    r"ция|ции|цию|цией|ций)\b",
    re.I,
)

REDUNDANT_QUALIFIERS = [
    ("достигнутые успехи", re.compile(r"\bдостигнут\w*\s+успех\w*\b", re.I)),
    ("имеющиеся ошибки", re.compile(r"\bимеющ\w*\s+ошиб\w*\b", re.I)),
    ("приглашённые гости", re.compile(r"\bприглаш[её]нн\w*\s+гост\w*\b", re.I)),
    ("важнейшая основа", re.compile(r"\bважнейш\w*\s+основ\w*\b", re.I)),
    ("главная суть", re.compile(r"\bглавн\w*\s+суть\b", re.I)),
    ("конечный итог", re.compile(r"\bконечн\w*\s+итог\w*\b", re.I)),
]

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
    ("возникновение исчезновения", re.compile(
        r"\bвозникновени\w*\s+исчезновени\w*\b", re.I
    )),
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
ACRONYM = re.compile(r"(?<![A-Za-zА-Яа-яЁё])(?:[A-ZА-ЯЁ]{4,})(?![A-Za-zА-Яа-яЁё])")


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
    return [w for w in _words(sentence) if NOMINAL_ENDING.search(w)]


def _suffix_echo(sentence: str) -> tuple[str, list[str]] | None:
    """Return a dense repeated 4-letter ending, if any.

    This is intentionally conservative: at least four long words in one
    sentence must share the same four final letters.
    """
    words = [w.lower() for w in _words(sentence) if len(w) >= 7]
    groups: dict[str, list[str]] = {}
    for word in words:
        suffix = word[-4:]
        groups.setdefault(suffix, []).append(word)
    for suffix, items in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):
        if len(items) >= 4:
            return suffix, items
    return None


def check_chukovsky(prose: str, sentences: Iterable[str]) -> tuple[list[dict], dict]:
    findings: list[dict] = []
    sents = list(sentences)
    low = prose.lower()

    meta_hits = [phrase for phrase in METADISCOURSE if phrase in low]
    if meta_hits:
        _add(
            findings,
            "chukovsky: metadiscourse deletion test",
            "; ".join(meta_hits),
            (
                "test a version without the announcing phrase; keep it only if it "
                "adds real modality, navigation or contrast rather than merely "
                "announcing that the next sentence is important"
            ),
        )

    bureau_hits: dict[str, list[str]] = {}
    for family, rx in BUREAUCRATIC_FAMILIES.items():
        matches = [m.group(0) for m in rx.finditer(prose)]
        if matches:
            bureau_hits[family] = matches

    bureau_total = sum(len(v) for v in bureau_hits.values())
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

    light_hits = [m.group(0) for m in LIGHT_VERB_NOMINAL.finditer(prose)]
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

    redundant_hits = []
    for _, rx in REDUNDANT_QUALIFIERS:
        for m in rx.finditer(prose):
            redundant_hits.append(m.group(0))
    if redundant_hits:
        _add(
            findings,
            "chukovsky: redundant qualifier candidate",
            "; ".join(redundant_hits[:6]),
            (
                "delete the qualifier in a comparison copy; keep it only if it "
                "changes scope, contrast, chronology or another real meaning"
            ),
        )

    stamp_hits: list[str] = []
    for _, rx in STAMP_COLLOCATIONS.items():
        matches = [m.group(0) for m in rx.finditer(prose)]
        if matches:
            stamp_hits.extend(matches)
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

    collision_hits = []
    for _, rx in ABSTRACT_COLLISIONS:
        collision_hits.extend(m.group(0) for m in rx.finditer(prose))
    if collision_hits:
        _add(
            findings,
            "chukovsky: abstract semantic collision",
            "; ".join(collision_hits[:5]),
            (
                "unpack the abstractions and state the event directly; verify the "
                "result against SEMANTICS because the original may be ironic"
            ),
        )

    qpack = [m.group(0) for m in QUESTION_PACKAGING.finditer(prose)]
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
                "actually saves effort; a technical term may still be fully justified"
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
                    "rhythmic/technical"
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
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    findings, metrics = check_chukovsky(text, sents)
    rules = {item["rule"] for item in findings}
    assert "chukovsky: metadiscourse deletion test" in rules, findings
    assert "chukovsky: bureaucratic-register cluster" in rules, findings
    assert "chukovsky: nominalization cluster" in rules, findings
    assert "chukovsky: evaluative stamp cluster" in rules, findings
    assert "chukovsky: redundant qualifier candidate" in rules, findings
    assert metrics["chukovsky_nominalizations"] >= 3, metrics

    clean = "Вышел релиз. Исправили поиск и добавили фильтры."
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean) if s.strip()]
    findings, _ = check_chukovsky(clean, sents)
    assert not findings, findings


if __name__ == "__main__":
    self_test()
    print("chukovsky self-test: OK")
