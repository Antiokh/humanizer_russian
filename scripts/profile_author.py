#!/usr/bin/env python3
"""Build a descriptive author-style profile from a Russian text corpus.

The profiler is deliberately descriptive:
- it does not diagnose personality;
- it does not decide what is "good" Russian;
- it preserves document boundaries for sentence and n-gram statistics;
- it does not emit source paths into the profile.

The output follows profiles/schema.json (v1).
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)?")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

DISCOURSE_MARKERS = [
    "ну", "вот", "то есть", "короче", "в общем", "кстати", "просто",
    "вообще", "значит", "слушай", "смотри", "в принципе", "при этом",
    "так что", "с другой стороны", "мне кажется", "похоже", "скорее всего",
    "возможно", "видимо", "наверное", "ладно", "хотя", "впрочем",
]

SELF_REPAIR_MARKERS = [
    "то есть", "точнее", "вернее", "нет,", "хотя нет", "или нет",
    "в смысле", "я имею в виду", "если точнее",
]

STANCE_HEDGES = [
    "мне кажется", "похоже", "скорее всего", "возможно", "видимо",
    "наверное", "предположительно", "я думаю", "я так понимаю",
]

CERTAINTY_MARKERS = [
    "точно", "очевидно", "безусловно", "однозначно", "реально", "точно не",
]

VERB_PROXY = re.compile(
    r"\b[а-яё]{3,}(?:ть|ться|ет|ёт|ют|ут|ит|ат|ят|ешь|ишь|ем|им|ете|ите|"
    r"ал|ала|али|ял|яла|яли|ил|ила|или|лся|лась|лись|ем|ен|ена|ены)\b",
    re.I,
)

FIRST_PERSON = re.compile(
    r"\b(?:я|мы|мне|нам|меня|нас|мой|моя|моё|мои|наш|наша|наше|наши)\b",
    re.I,
)


def load_paths(paths: list[str]) -> list[str]:
    """Read UTF-8 .txt/.md documents without exposing filesystem paths."""
    docs: list[str] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.suffix.lower() in {".txt", ".md"} and child.is_file():
                    docs.append(child.read_text(encoding="utf-8"))
        elif p.is_file():
            docs.append(p.read_text(encoding="utf-8"))
        else:
            raise FileNotFoundError(raw)
    return docs


def words(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s*\n+\s*", " ", text).strip()
    if not flat:
        return []
    return [s.strip() for s in SENT_SPLIT.split(flat) if s.strip()]


def percentile(values: list[int], q: float) -> float:
    if not values:
        return 0
    v = sorted(values)
    pos = (len(v) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(v) - 1)
    frac = pos - lo
    return round(v[lo] * (1 - frac) + v[hi] * frac, 2)


def count_phrases(text_low: str, phrases: list[str]) -> dict[str, int]:
    return {
        p: len(re.findall(r"(?<!\w)" + re.escape(p) + r"(?!\w)", text_low))
        for p in phrases
    }


def merge_phrase_counts(docs: list[str], phrases: list[str]) -> Counter[str]:
    total: Counter[str] = Counter()
    for text in docs:
        total.update(count_phrases(text.lower(), phrases))
    return total


def ngram_counts(tokens: list[str], n: int) -> Counter[tuple[str, ...]]:
    if len(tokens) < n:
        return Counter()
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def top_ngrams_by_document(docs: list[str], n: int, limit: int = 20) -> list[dict]:
    """Aggregate n-grams without creating cross-document token pairs."""
    grams: Counter[tuple[str, ...]] = Counter()
    for text in docs:
        grams.update(ngram_counts(words(text), n))
    return [
        {"text": " ".join(g), "count": c}
        for g, c in grams.most_common(limit)
        if c >= 2
    ]


def rate_item(text: str, count: int, total_words: int) -> dict:
    return {
        "text": text,
        "count": count,
        "per_10k_words": round(count * 10000 / total_words, 2) if total_words else 0,
    }


def analyse(docs: list[str]) -> dict:
    all_text = "\n\n".join(docs)
    all_tokens = [token for doc in docs for token in words(doc)]
    all_sentences = [sent for doc in docs for sent in sentences(doc)]
    sent_lengths = [len(words(s)) for s in all_sentences]
    total_words = len(all_tokens)

    markers = merge_phrase_counts(docs, DISCOURSE_MARKERS)
    repairs = merge_phrase_counts(docs, SELF_REPAIR_MARKERS)
    hedges = merge_phrase_counts(docs, STANCE_HEDGES)
    certainty = merge_phrase_counts(docs, CERTAINTY_MARKERS)

    no_verb_proxy = [
        s for s in all_sentences
        if words(s) and not VERB_PROXY.search(s)
    ]
    first_person_sents = [s for s in all_sentences if FIRST_PERSON.search(s)]

    latin_tokens = [
        token for token in all_tokens
        if re.fullmatch(r"[a-z]+(?:-[a-z]+)?", token)
    ]

    punctuation_counts = {
        "em_dash": all_text.count("—"),
        "en_dash": all_text.count("–"),
        "colon": all_text.count(":"),
        "semicolon": all_text.count(";"),
        "question": all_text.count("?"),
        "exclamation": all_text.count("!"),
        "ellipsis_unicode": all_text.count("…"),
        "ellipsis_three_dots": all_text.count("..."),
        "parentheses_open": all_text.count("("),
    }

    return {
        "version": 1,
        "corpus": {
            "documents": len(docs),
            "words": total_words,
            "sentences": len(all_sentences),
        },
        "lexicon": {
            "discourse_markers": [
                rate_item(k, v, total_words)
                for k, v in sorted(markers.items(), key=lambda x: (-x[1], x[0]))
                if v
            ],
            "self_repair_markers": [
                rate_item(k, v, total_words)
                for k, v in sorted(repairs.items(), key=lambda x: (-x[1], x[0]))
                if v
            ],
            "code_switching": {
                "latin_token_count": len(latin_tokens),
                "latin_token_rate": round(len(latin_tokens) / total_words, 4)
                if total_words else 0,
                "top_latin_tokens": [
                    {"text": token, "count": count}
                    for token, count in Counter(latin_tokens).most_common(30)
                ],
            },
            "ngrams": {
                "bigrams": top_ngrams_by_document(docs, 2),
                "trigrams": top_ngrams_by_document(docs, 3),
            },
        },
        "syntax": {
            "sentence_length": {
                "p25": percentile(sent_lengths, 0.25),
                "median": percentile(sent_lengths, 0.50),
                "p75": percentile(sent_lengths, 0.75),
                "p90": percentile(sent_lengths, 0.90),
            },
            "short_le_4_rate": round(
                sum(x <= 4 for x in sent_lengths) / len(all_sentences), 4
            ) if all_sentences else 0,
            "sentences_without_verb_proxy_rate": round(
                len(no_verb_proxy) / len(all_sentences), 4
            ) if all_sentences else 0,
            "first_person_sentence_rate": round(
                len(first_person_sents) / len(all_sentences), 4
            ) if all_sentences else 0,
            "proxy_warning": "Regex proxies are descriptive, not morphological analysis.",
        },
        "punctuation": {
            key: {
                "count": value,
                "per_10k_words": round(value * 10000 / total_words, 2)
                if total_words else 0,
            }
            for key, value in punctuation_counts.items()
        },
        "stance": {
            "hedges": [
                rate_item(k, v, total_words)
                for k, v in sorted(hedges.items(), key=lambda x: (-x[1], x[0]))
                if v
            ],
            "certainty": [
                rate_item(k, v, total_words)
                for k, v in sorted(certainty.items(), key=lambda x: (-x[1], x[0]))
                if v
            ],
        },
        "observed_errors": [],
        "settings": {
            "imitate_errors": False,
            "correct_norm_errors": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="UTF-8 .txt/.md files or directories")
    parser.add_argument("-o", "--output", help="write JSON to file; stdout otherwise")
    args = parser.parse_args()

    profile = analyse(load_paths(args.paths))
    rendered = json.dumps(profile, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
