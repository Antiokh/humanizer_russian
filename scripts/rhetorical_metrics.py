#!/usr/bin/env python3
"""Optional document-level rhetoric metrics; no editorial findings or rewrite advice.

The same measured pattern can be a defect, a genre convention or an author's
intentional rhythm. This module therefore emits METRIC_ONLY statistics.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?", re.UNICODE)
ANSWER_RE = re.compile(
    r"^(?:потому что|дело в том(?:,)? что|ответ(?:\s+прост)?|причина в том(?:,)? что)\b",
    re.IGNORECASE,
)


def prose_paragraphs(text: str) -> list[str]:
    """Exclude common Markdown non-prose areas, without editing the input."""
    result: list[str] = []
    current: list[str] = []
    fence: str | None = None

    def flush() -> None:
        if current:
            result.append(" ".join(current))
            current.clear()

    for line in text.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"^(\x60{3,}|~{3,})", stripped)
        if fence_match:
            flush()
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        if not stripped or re.match(r"^(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", stripped):
            flush()
            continue
        cleaned = re.sub(r"\x60[^\x60]*\x60", "", line)
        cleaned = re.sub(r"https?://\S+", "", cleaned)
        if cleaned.strip():
            current.append(" ".join(cleaned.split()))
        else:
            flush()
    flush()
    return result


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text.casefold())


def _sentences(paragraph: str) -> list[str]:
    return [part.strip() for part in SENTENCE_RE.findall(paragraph) if _words(part)]


def _repeated(counter: Counter[str], minimum: int = 3) -> list[dict[str, str | int]]:
    return [
        {"text": phrase, "count": count}
        for phrase, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
        if count >= minimum
    ]


def audit(text: str) -> dict:
    paragraphs = prose_paragraphs(text)
    groups = [_sentences(p) for p in paragraphs]
    sentences = [sentence for group in groups for sentence in group]
    openers: Counter[str] = Counter()
    endings: Counter[str] = Counter()
    bins: list[str] = []
    pairs = 0

    for sentence in sentences:
        words = _words(sentence)
        if len(words) >= 2:
            openers[" ".join(words[:2])] += 1
        bins.append("short" if len(words) <= 7 else "medium" if len(words) <= 18 else "long")

    for paragraph in paragraphs:
        words = _words(paragraph)
        if len(words) >= 2:
            endings[" ".join(words[-2:])] += 1

    for group in groups:
        for previous, current in zip(group, group[1:]):
            if previous.rstrip().endswith("?") and ANSWER_RE.search(current.strip()):
                pairs += 1

    same_length_windows = sum(
        bins[i] == bins[i - 1] == bins[i - 2]
        for i in range(2, len(bins))
    )

    return {
        "schema_version": 1,
        "classification": "METRIC_ONLY",
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "length_bins": dict(sorted(Counter(bins).items())),
        "same_length_three_sentence_windows": same_length_windows,
        "immediate_question_answer_pairs": pairs,
        "repeated_two_word_sentence_openers": _repeated(openers),
        "repeated_two_word_paragraph_endings": _repeated(endings),
        "interpretation": "Descriptive statistics only; not evidence of AI authorship or a rewrite instruction.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Optional Russian rhetoric metrics (no verdict)")
    parser.add_argument("path", nargs="?", help="UTF-8 prose or Markdown; stdin if omitted")
    args = parser.parse_args(argv)
    raw = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    print(json.dumps(audit(raw), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
