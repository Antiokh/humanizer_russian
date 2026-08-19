#!/usr/bin/env python3
"""Conservative surface linter for humanizer_russian.

The linter does not decide what is grammatical, human, or author-written by
regex. It finds surface candidates for contextual review.

Kinds:
  ARTIFACT       technical chatbot/citation traces; the only automatic gate
  AI_PATTERN     repeated formulae or calque-like patterns
  NATIVE_WARNING formally possible but potentially synthetic/native-unfriendly
  STYLE_WARNING  rhythm/format patterns that may be intentional

Descriptive metrics are returned separately. Exit status is non-zero only when
ARTIFACT findings remain.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ARTIFACT_PATTERNS = [
    ("openai citation marker", re.compile(r"\boaicite\b", re.I)),
    (
        "tool turn marker",
        re.compile(
            r"\bturn\d+(?:search|news|fetch|view|file|image|product|business)\d+\b",
            re.I,
        ),
    ),
    (
        "bracket citation placeholder",
        re.compile(r"\[(?:cite|citation)\s*:\s*\d+[^\]]*\]", re.I),
    ),
    (
        "chatgpt/openai utm",
        re.compile(r"utm_source=(?:chatgpt(?:\.com)?|openai)", re.I),
    ),
]

AI_PHRASE_FAMILIES = {
    "assistant-wrapper": [
        "надеюсь, это поможет",
        "надеюсь, было полезно",
        "дайте знать, если",
        "буду рад помочь",
        "вот краткий обзор",
    ],
    "importance-announcement": [
        "важно отметить",
        "следует подчеркнуть",
        "стоит обратить внимание",
        "нельзя не упомянуть",
        "необходимо учитывать",
    ],
    "pseudo-depth": [
        "если копнуть глубже",
        "глубинная проблема",
        "настоящий вопрос в том",
        "в конечном счёте",
        "вот в чём штука",
    ],
    "video-script": [
        "давайте разберёмся",
        "погрузимся в",
        "вот что нужно знать",
        "перейдём к главному",
        "без лишних слов",
    ],
    "generic-conclusion": [
        "подводя итог",
        "в заключение",
        "резюмируя",
        "будущее выглядит ярким",
        "впереди захватывающие времена",
    ],
    "stack-connector": [
        "кроме того",
        "более того",
        "также стоит",
        "ещё один аспект",
        "ещё одним аспектом",
    ],
}

CALQUE_PATTERNS = [
    (
        "literal possessives",
        re.compile(
            r"\b(?:свою\s+руку\s+в\s+свой\s+карман|мой\s+ответ|мою\s+встречу|свою\s+руку)\b",
            re.I,
        ),
    ),
    (
        "address a problem",
        re.compile(r"\bадрес(?:овать|ует|уем|уют|ация)\s+(?:проблем|вопрос)", re.I),
    ),
    (
        "deliver value",
        re.compile(r"\bдостав(?:лять|ить|ляет|ляем|ляют)\s+ценност", re.I),
    ),
    ("have influence", re.compile(r"\bиме(?:ть|ет|ют|ем)\s+влияни", re.I)),
    (
        "be ready by",
        re.compile(r"\bмогу\s+быть\s+готов(?:ым|ой|ы)?\s+к\b", re.I),
    ),
]

SLOGAN_PATTERNS = [
    re.compile(r"\bхорошая новость\?", re.I),
    re.compile(r"\bглавное\?", re.I),
    re.compile(r"\bпочему это важно\?", re.I),
    re.compile(r"\bвот почему это важно\b", re.I),
    re.compile(r"\bодин вопрос\.?\s+один ответ\b", re.I),
    re.compile(r"\bне теория\.?\s+практика\b", re.I),
    re.compile(r"\bвот (?:тут|здесь) становится интересно\b", re.I),
]

CONTRAST_PATTERNS = [
    re.compile(r"\bне\s+просто\b", re.I),
    re.compile(r"\bне\s+только\b", re.I),
    re.compile(r"\bэто\s+не\b[^.!?\n]{0,100}?\bа\b", re.I),
]

# Candidates for factoring repeated common material out of a contrast.
# These regexes only raise NATIVE_WARNING; the model still checks meaning.
REPEATED_COMMON_PATTERNS = [
    re.compile(
        r"\bне\s+(?P<head>[а-яё]{4,})\b(?P<left>[^.!?\n]{0,90}?),\s*а\s+(?P=head)\b",
        re.I,
    ),
    re.compile(
        r"\b(?P<head>[а-яё]{4,})\b(?P<left>[^.!?\n]{1,90}?),\s*но\s+(?P=head)\b",
        re.I,
    ),
]
REPEATED_CONTRAST_STOP = {"только", "просто", "очень", "столько", "сколько"}

PARCELLATED_ENUM_PATTERNS = [
    re.compile(
        r"\b(?:две|три|четыре|пять)\s+[а-яё-]{2,}\s*[.!]\s*(?:либо|или)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:нужн[аоы]?|есть|выделю|назову)\s+"
        r"(?:две|три|четыре|пять)\s+[а-яё-]{2,}\s*[.!]\s*"
        r"(?:перв(?:ое|ая|ый)|во-первых)\b",
        re.I,
    ),
]

POSSESSIVE_RE = re.compile(
    r"\b(?:мой|моя|моё|мои|моего|моей|мою|моим|моими|"
    r"твой|твоя|твоё|твои|твоего|твоей|твою|"
    r"свой|своя|своё|свои|своего|своей|свою|своим|своими|"
    r"наш|наша|наше|наши|ваш|ваша|ваше|ваши)\b",
    re.I,
)

ASCII_DASH_IN_PROSE = re.compile(r"(?<=[А-Яа-яЁё0-9»)])\s-\s(?=[А-Яа-яЁё0-9«(])")
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
BOLD_SPAN = re.compile(r"\*\*[^*\n]+\*\*")
URL_OR_CODE = re.compile(r"```.*?```|`[^`\n]+`|https?://\S+", re.S)
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")

COMMON_SENTENCE_STARTS = {
    "и",
    "а",
    "но",
    "или",
    "если",
    "когда",
    "что",
    "это",
    "так",
    "тут",
    "здесь",
    "вот",
}


def strip_frontmatter(lines: list[str]) -> list[str]:
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 50)):
            if lines[i].strip() == "---":
                return [""] * (i + 1) + lines[i + 1 :]
    return lines


def prose_text(text: str) -> str:
    clean = URL_OR_CODE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    lines = strip_frontmatter(clean.splitlines())
    kept = []
    for line in lines:
        if not line.strip():
            kept.append("")
            continue
        if re.match(r"^\s*(#|\||[-*+]\s|\d+\.\s|>)", line):
            continue
        kept.append(re.sub(r"\*\*|«|»", "", line))
    return "\n".join(kept)


def sentences(text: str) -> list[str]:
    prose = re.sub(r"\s*\n+\s*", " ", prose_text(text)).strip()
    if not prose:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip()]


def word_count(s: str) -> int:
    return len(WORD_RE.findall(s))


def words(s: str) -> list[str]:
    return [x.lower() for x in re.findall(r"[A-Za-zА-Яа-яЁё]+", s)]


def first_words(s: str, n: int = 2) -> tuple[str, ...]:
    return tuple(words(s)[:n])


def first_content_word(s: str) -> str:
    for token in words(s):
        if token not in COMMON_SENTENCE_STARTS:
            return token
    toks = words(s)
    return toks[0] if toks else ""


def add(
    findings: list[dict],
    kind: str,
    rule: str,
    excerpt: str,
    line: int = 0,
    note: str = "",
) -> None:
    findings.append(
        {
            "kind": kind,
            "line": line,
            "rule": rule,
            "excerpt": excerpt[:180],
            "note": note,
        }
    )


def repeated_subject_candidates(sents: list[str]) -> list[tuple[str, list[str]]]:
    """Find 3+ consecutive sentences with the same first content token.

    This is only a proxy for repeated explicit context / SVO-lock. It does not
    claim that the token is morphologically the subject.
    """
    out: list[tuple[str, list[str]]] = []
    i = 0
    while i < len(sents):
        token = first_content_word(sents[i])
        if not token or len(token) < 3:
            i += 1
            continue
        run = [sents[i]]
        j = i + 1
        while j < len(sents) and first_content_word(sents[j]) == token:
            run.append(sents[j])
            j += 1
        if len(run) >= 3:
            out.append((token, run))
        i = max(j, i + 1)
    return out


def question_answer_cluster(sents: list[str]) -> int:
    count = 0
    for i in range(len(sents) - 1):
        if (
            sents[i].endswith("?")
            and word_count(sents[i]) <= 8
            and word_count(sents[i + 1]) <= 6
        ):
            count += 1
    return count


def lint(text: str) -> tuple[list[dict], dict]:
    findings: list[dict] = []

    for rule, rx in ARTIFACT_PATTERNS:
        for match in rx.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            add(
                findings,
                "ARTIFACT",
                rule,
                match.group(0),
                line,
                "technical trace; remove before publication",
            )

    prose = prose_text(text)
    sents = sentences(text)
    lengths = [word_count(s) for s in sents]
    low = prose.lower()

    for family, phrases in AI_PHRASE_FAMILIES.items():
        hits = [phrase for phrase in phrases if phrase in low]
        if hits:
            add(
                findings,
                "AI_PATTERN",
                family,
                "; ".join(hits),
                note="soft signal; judge by function and clustering",
            )

    for rule, rx in CALQUE_PATTERNS:
        for match in rx.finditer(prose):
            add(
                findings,
                "AI_PATTERN",
                f"calque: {rule}",
                match.group(0),
                note="candidate only; verify idiom, audience and context",
            )

    possessive_dense = 0
    for sent in sents:
        hits = POSSESSIVE_RE.findall(sent)
        if len(hits) >= 2:
            possessive_dense += 1
            add(
                findings,
                "NATIVE_WARNING",
                "possessive overexplication candidate",
                sent,
                note=(
                    "Russian often leaves obvious ownership implicit; check whether "
                    "one or more possessives can disappear without ambiguity"
                ),
            )

    seen_spans: set[tuple[int, int]] = set()
    for rx in REPEATED_COMMON_PATTERNS:
        for match in rx.finditer(prose):
            if match.span() in seen_spans:
                continue
            seen_spans.add(match.span())
            head = match.group("head").lower()
            if head in REPEATED_CONTRAST_STOP:
                continue
            add(
                findings,
                "NATIVE_WARNING",
                "repeated common element in contrast",
                match.group(0),
                note=(
                    f"common «{head}» may be factorable: say it once, then re-check "
                    "word order, contrast and information focus"
                ),
            )

    contrast_hits = sum(len(rx.findall(prose)) for rx in CONTRAST_PATTERNS)
    if contrast_hits >= 3:
        add(
            findings,
            "STYLE_WARNING",
            "repeated contrast formula",
            f"{contrast_hits} contrast formulae",
            note="`не X, а Y` is normative; review only repetitive rhetorical use",
        )

    slogan_hits = sum(len(rx.findall(prose)) for rx in SLOGAN_PATTERNS)
    qa_hits = question_answer_cluster(sents)
    if slogan_hits >= 2 or qa_hits >= 3:
        add(
            findings,
            "AI_PATTERN",
            "anglo-rhetorical question/answer cluster",
            f"{slogan_hits} slogan markers; {qa_hits} short question-answer pairs",
            note=(
                "short Q/A is normal in real dialogue; review only serial punchline "
                "use in expository/marketing prose"
            ),
        )

    parcellated_enum_hits = 0
    for rx in PARCELLATED_ENUM_PATTERNS:
        for match in rx.finditer(prose):
            parcellated_enum_hits += 1
            add(
                findings,
                "NATIVE_WARNING",
                "parcellated enumeration",
                match.group(0),
                note=(
                    "check whether the first clause introduces a list that is more "
                    "natural as one construction with a colon"
                ),
            )

    short_fragment_clusters = 0
    run: list[str] = []
    for sent in sents + ["SENTINEL LONG ENOUGH TO FLUSH"]:
        if word_count(sent) <= 4:
            run.append(sent)
        else:
            if len(run) >= 3:
                short_fragment_clusters += 1
                add(
                    findings,
                    "STYLE_WARNING",
                    "short-fragment cluster",
                    " | ".join(run[:5]),
                    note=(
                        "parcellation may be intentional; verify that each break adds "
                        "an accent instead of hiding one syntactic construction"
                    ),
                )
            run = []

    starts = [first_words(sent, 2) for sent in sents]
    repeated_start_flag = 0
    for i in range(len(starts) - 2):
        tri = starts[i : i + 3]
        if tri[0] and tri[0] == tri[1] == tri[2]:
            repeated_start_flag = 1
            add(
                findings,
                "NATIVE_WARNING",
                "repeated sentence start",
                " / ".join(" ".join(item) for item in tri),
                note=(
                    "candidate for repeated explicit context/SVO-lock; compress or "
                    "reorder only if the context stays unambiguous"
                ),
            )
            break

    repeated_subject_runs = repeated_subject_candidates(sents)
    for token, run_sents in repeated_subject_runs[:2]:
        add(
            findings,
            "NATIVE_WARNING",
            "repeated explicit context candidate",
            " | ".join(run_sents[:4]),
            note=(
                f"«{token}» opens {len(run_sents)} consecutive sentences; check "
                "pronoun, zero subject, ellipsis or a different theme-rheme order"
            ),
        )

    undercompression_pairs = 0
    for left, right in zip(sents, sents[1:]):
        lw = [w for w in words(left) if len(w) >= 5]
        rw = [w for w in words(right) if len(w) >= 5]
        shared = sorted(set(lw) & set(rw))
        if len(shared) >= 3 and word_count(left) >= 7 and word_count(right) >= 7:
            undercompression_pairs += 1
            add(
                findings,
                "NATIVE_WARNING",
                "context undercompression candidate",
                f"{left} | {right}",
                note=(
                    "adjacent sentences repeat several content words; check whether "
                    "the second can trust the first sentence's context instead of "
                    "renaming the same material"
                ),
            )

    if ASCII_DASH_IN_PROSE.search(prose):
        add(
            findings,
            "STYLE_WARNING",
            "ascii hyphen used as dash",
            " - ",
            note="check typography; do not replace normative dash for anti-detection",
        )

    dash_count = len(re.findall(r"[—–]", prose))
    words_total = sum(lengths)
    metrics = {
        "sentences": len(sents),
        "words": words_total,
        "sentence_length_median": sorted(lengths)[len(lengths) // 2] if lengths else 0,
        "short_sentences_le_4": sum(1 for x in lengths if x <= 4),
        "dashes": dash_count,
        "colons": prose.count(":"),
        "questions": prose.count("?"),
        "emoji": len(EMOJI.findall(prose)),
        "bold_spans": len(BOLD_SPAN.findall(text)),
        "contrast_formulae": contrast_hits,
        "slogan_markers": slogan_hits,
        "short_question_answer_pairs": qa_hits,
        "possessive_dense_sentences": possessive_dense,
        "parcellated_enumerations": parcellated_enum_hits,
        "short_fragment_clusters": short_fragment_clusters,
        "repeated_sentence_start_flag": repeated_start_flag,
        "repeated_explicit_context_runs": len(repeated_subject_runs),
        "undercompression_pairs": undercompression_pairs,
    }

    if len(sents) >= 6 and dash_count >= 5 and dash_count > len(sents) / 2:
        add(
            findings,
            "STYLE_WARNING",
            "high dash density",
            f"{dash_count} dashes / {len(sents)} sentences",
            note="heuristic only: inspect whether the same dash construction repeats",
        )

    return findings, metrics


def self_test() -> None:
    synthetic = "Это не ошибка в расчёте, а ошибка в исходных данных."
    findings, _ = lint(synthetic)
    assert any(
        item["kind"] == "NATIVE_WARNING"
        and item["rule"] == "repeated common element in contrast"
        for item in findings
    ), findings

    compressed = (
        "Это ошибка не в расчёте, а в исходных данных. "
        "Первый вариант дорогой. Второй — быстрее."
    )
    findings, _ = lint(compressed)
    assert not [
        item for item in findings if item["rule"] == "repeated common element in contrast"
    ], findings

    verb_repeat = "Мы не меняем цену, а меняем условия."
    findings, _ = lint(verb_repeat)
    assert any(
        item["rule"] == "repeated common element in contrast" for item in findings
    ), findings

    intentional_repeat = "Никогда. Никогда больше."
    findings, _ = lint(intentional_repeat)
    assert not [
        item for item in findings if item["rule"] == "repeated common element in contrast"
    ], findings

    enum = (
        "С такими курсами обычно две беды. "
        "Либо чистая теория. Либо пересказ пересказа."
    )
    findings, _ = lint(enum)
    assert any(item["rule"] == "parcellated enumeration" for item in findings), findings

    contrasts = (
        "Это не просто курс, а опыт. "
        "Это не просто опыт, а путь. "
        "Это не просто путь, а философия."
    )
    findings, _ = lint(contrasts)
    assert any(item["rule"] == "repeated contrast formula" for item in findings), findings

    artifact = "Текст с oaicite и ?utm_source=chatgpt.com"
    findings, _ = lint(artifact)
    assert len([item for item in findings if item["kind"] == "ARTIFACT"]) >= 2, findings

    calque = (
        "Он положил свою руку в свой карман. "
        "Я дал ему мой ответ после того, как закончил мою встречу."
    )
    findings, metrics = lint(calque)
    assert any(item["rule"].startswith("calque:") for item in findings), findings
    assert metrics["possessive_dense_sentences"] >= 1, metrics

    subject_lock = (
        "Компания выпустила новую версию продукта. "
        "Компания добавила новые фильтры для поиска. "
        "Компания изменила старую страницу настроек."
    )
    findings, _ = lint(subject_lock)
    assert any(
        item["rule"] in {"repeated sentence start", "repeated explicit context candidate"}
        for item in findings
    ), findings

    qa = (
        "Главное? Начать. Хорошая новость? Это решаемо. "
        "Почему это важно? Потому что рынок изменился."
    )
    findings, metrics = lint(qa)
    assert any(
        item["rule"] == "anglo-rhetorical question/answer cluster" for item in findings
    ), findings
    assert metrics["short_question_answer_pairs"] >= 2, metrics

    dialogue = "Кого любит Паша? Машу."
    findings, _ = lint(dialogue)
    assert not [
        item
        for item in findings
        if item["rule"] == "anglo-rhetorical question/answer cluster"
    ], findings

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
        for item in findings:
            loc = f":{item['line']}" if item["line"] else ""
            note = f" — {item['note']}" if item["note"] else ""
            print(f"{item['kind']}{loc} [{item['rule']}]: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))

    if any(item["kind"] == "ARTIFACT" for item in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
