#!/usr/bin/env python3
"""Opt-in descriptive Russian rhetoric metrics: no findings and no rewrite advice.

The same rhetorical pattern can be ordinary grammar, a genre convention or a
deliberate authorial choice. These experimental values are METRIC_ONLY.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

if __package__:
    from .russian_prose import mask_nonprose
else:
    from russian_prose import mask_nonprose

WORD_RE = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)
WORD_BEFORE_DOT = re.compile(r"([^\W\d_]+)$", re.UNICODE)
ANSWER_RE = re.compile(
    r"^(?:потому\s+что\b|дело\s+в\s+том,?\s+что\b|"
    r"причина\s+в\s+том,?\s+что\b|ответ(?:\s+прост)?\s*:)",
    re.IGNORECASE,
)
ABBREVIATIONS = frozenset({
    "г", "гг", "ул", "стр", "рис", "табл", "им", "др", "т", "д", "п", "н", "см",
})
CLOSING_QUOTES = "»”\"')]}’"
OPENING_QUOTES = "«„“\"'([{’"
SENTENCE_END = ".?!…"
SHORT_LE = 7
MEDIUM_LE = 18
MIN_REPETITIONS = 3
MIN_RUN_SENTENCES = 3


def prose_paragraphs(text: str) -> list[str]:
    """Reuse the repository's Markdown/code/URL masker; discard non-prose blocks."""
    masked = mask_nonprose(text)
    result: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            result.append(" ".join(current))
            current.clear()

    for line in masked.splitlines():
        stripped = line.lstrip()
        if not stripped or re.match(r"^(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", stripped):
            flush()
            continue
        if stripped:
            current.append(" ".join(stripped.split()))
    flush()
    return result


def _words(value: str) -> list[str]:
    return WORD_RE.findall(value.casefold())


def _nonterminal_dot(value: str, i: int) -> bool:
    if i and i + 1 < len(value) and value[i - 1].isdigit() and value[i + 1].isdigit():
        return True
    match = WORD_BEFORE_DOT.search(value[:i])
    if not match:
        return False
    token = match.group(1)
    if token.casefold() in ABBREVIATIONS:
        return True
    # Personal-name initials such as А. П. Чехов, but not arbitrary one-letter
    # sentence endings followed by lower-case prose.
    if len(token) == 1 and token.isupper():
        following = value[i + 1:].lstrip()
        if following and following[0].isupper():
            return True
    return False


def _sentences(paragraph: str) -> list[str]:
    """Conservative segmentation with common abbreviation, decimal and quote guards."""
    result: list[str] = []
    start = 0
    i = 0
    while i < len(paragraph):
        mark = paragraph[i]
        if mark not in SENTENCE_END:
            i += 1
            continue
        if mark == ".":
            if i + 1 < len(paragraph) and paragraph[i + 1] == ".":
                i += 1
                continue
            if _nonterminal_dot(paragraph, i):
                i += 1
                continue
        j = i + 1
        while j < len(paragraph) and paragraph[j] in SENTENCE_END:
            j += 1
        while j < len(paragraph) and paragraph[j] in CLOSING_QUOTES:
            j += 1
        if j < len(paragraph) and not paragraph[j].isspace():
            i = j
            continue
        candidate = paragraph[start:j].strip()
        if _words(candidate):
            result.append(candidate)
        start = j
        i = j
    tail = paragraph[start:].strip()
    if _words(tail):
        result.append(tail)
    return result


def _repeated(counter: Counter[str]) -> list[dict[str, str | int]]:
    """Show repeated surface n-grams; threshold is a display filter, not a verdict."""
    return [
        {"text": phrase, "count": count}
        for phrase, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
        if count >= MIN_REPETITIONS
    ]


def _bin(words: int) -> str:
    return "short" if words <= SHORT_LE else "medium" if words <= MEDIUM_LE else "long"


def _length_runs(groups: list[list[str]]) -> list[dict[str, int | str]]:
    """Maximal within-paragraph runs, never cross-paragraph overlapping windows."""
    runs: list[dict[str, int | str]] = []
    for paragraph_index, sentences in enumerate(groups, start=1):
        lengths = [_bin(len(_words(sentence))) for sentence in sentences]
        if not lengths:
            continue
        start = 0
        for i in range(1, len(lengths) + 1):
            if i == len(lengths) or lengths[i] != lengths[start]:
                count = i - start
                if count >= MIN_RUN_SENTENCES:
                    runs.append({
                        "paragraph_index": paragraph_index,
                        "bin": lengths[start],
                        "sentences": count,
                    })
                start = i
    return runs


def audit(text: str) -> dict:
    paragraphs = prose_paragraphs(text)
    groups = [_sentences(paragraph) for paragraph in paragraphs]
    sentences = [sentence for group in groups for sentence in group]
    sentence_lengths = [len(_words(sentence)) for sentence in sentences]
    openers: Counter[str] = Counter()
    endings: Counter[str] = Counter()
    marker_pairs = 0

    for sentence in sentences:
        words = _words(sentence)
        if len(words) >= 2:
            openers[" ".join(words[:2])] += 1

    for paragraph in paragraphs:
        words = _words(paragraph)
        if len(words) >= 2:
            endings[" ".join(words[-2:])] += 1

    for group in groups:
        for previous, current in zip(group, group[1:]):
            question = previous.rstrip().rstrip(CLOSING_QUOTES).rstrip()
            answer = current.lstrip().lstrip(OPENING_QUOTES).lstrip()
            if question.endswith("?") and ANSWER_RE.search(answer):
                marker_pairs += 1

    runs = _length_runs(groups)
    return {
        "schema_version": 2,
        "classification": "METRIC_ONLY",
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "word_count": sum(sentence_lengths),
        "length_bins": dict(sorted(Counter(_bin(length) for length in sentence_lengths).items())),
        "same_length_sentence_run_count": len(runs),
        "same_length_sentence_runs": runs,
        "explicit_question_answer_marker_pairs": marker_pairs,
        "repeated_two_word_sentence_openers": _repeated(openers),
        "repeated_two_word_paragraph_endings": _repeated(endings),
        "parameters": {
            "short_le_words": SHORT_LE,
            "medium_le_words": MEDIUM_LE,
            "minimum_repeat_to_display": MIN_REPETITIONS,
            "minimum_run_sentences": MIN_RUN_SENTENCES,
            "status": "provisional_not_corpus_calibrated",
        },
        "interpretation": (
            "Descriptive surface proxies only; not validated as genre-adjusted "
            "rhetorical analysis, AI attribution or a rewrite instruction."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Opt-in Russian rhetoric metrics (no verdict)")
    parser.add_argument("path", nargs="?", help="UTF-8 prose or Markdown; stdin if omitted")
    args = parser.parse_args(argv)
    raw = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    print(json.dumps(audit(raw), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
