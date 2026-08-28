#!/usr/bin/env python3
"""Early Serbian humanizer checks based on public-source hypotheses.

The checks in this module are deliberately conservative. They identify accumulated
style patterns; they do not attempt to prove AI authorship and they do not classify
ordinary Serbian constructions as errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


CYR_TO_LAT = str.maketrans(
    {
        "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ",
        "Е": "E", "Ж": "Ž", "З": "Z", "И": "I", "Ј": "J", "К": "K",
        "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O",
        "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "Ć", "У": "U",
        "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ",
        "е": "e", "ж": "ž", "з": "z", "и": "i", "ј": "j", "к": "k",
        "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
        "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "ć", "у": "u",
        "ф": "f", "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
    }
)

HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*$")

# These are normal Serbian constructions. A finding requires repeated use.
NEGATIVE_PARALLELISM_RE = re.compile(
    r"\b(?:nije|nisu|nisam|nisi|nismo|niste|ne)\s+"
    r"(?:samo\s+)?[^.!?;:\n]{1,120}?\s+"
    r"(?:već|nego)(?:\s+i)?\s+[^.!?;:\n]{1,120}",
    re.IGNORECASE,
)

# Deliberately narrow heuristic: three compact coordinated chunks.
TRIPLET_RE = re.compile(
    r"\b([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s*,\s*"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s+"
    r"(?:i|ili)\s+"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\b",
    re.IGNORECASE,
)

SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", re.MULTILINE)
WORD_RE = re.compile(r"\b[\wčćžšđ]+\b", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    category: str
    severity: str
    message: str
    count: int
    evidence: list[str]


def normalize_script(text: str) -> str:
    """Normalize Serbian Cyrillic to Latin for matching, preserving meaning."""
    return text.translate(CYR_TO_LAT)


def _compact_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()]


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def negative_parallelism_density(text: str) -> Finding | None:
    normalized = normalize_script(text)
    matches = [_compact_ws(m.group(0)) for m in NEGATIVE_PARALLELISM_RE.finditer(normalized)]
    sentences = _sentences(normalized)

    # One or two occurrences are intentionally ignored. We want accumulation.
    threshold = max(4, (len(sentences) + 5) // 6)
    if len(matches) < threshold:
        return None

    return Finding(
        rule_id="sr_ai_negative_parallelism_density",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "Kontrastni obrasci tipa ‘nije … već/nego …’ ponavljaju se veoma često. "
            "Konstrukcija je sama po sebi normalna; signal nastaje tek zbog gustine i ponavljanja."
        ),
        count=len(matches),
        evidence=matches[:5],
    )


def triplet_density(text: str) -> Finding | None:
    normalized = normalize_script(text)
    matches = [_compact_ws(m.group(0)) for m in TRIPLET_RE.finditer(normalized)]
    sentences = _sentences(normalized)

    threshold = max(4, (len(sentences) + 4) // 5)
    if len(matches) < threshold:
        return None

    return Finding(
        rule_id="sr_ai_triplet_density",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "U tekstu se nagomilavaju tročlana nabrajanja ili opisi. "
            "Pojedinačna trojka nije problem; ovde je signal njihova ponovljena struktura."
        ),
        count=len(matches),
        evidence=matches[:5],
    )


def repeated_section_scaffold(text: str) -> Finding | None:
    headings = [_compact_ws(h) for h in HEADING_RE.findall(text)]
    if len(headings) < 6:
        return None

    normalized = [normalize_script(h).casefold() for h in headings]
    counts = Counter(normalized)
    repeated = [(heading, count) for heading, count in counts.most_common() if count >= 3]
    if not repeated:
        return None

    repeated_instances = sum(count for _, count in repeated)
    if repeated_instances / len(headings) < 0.5:
        return None

    pretty = [f"{heading} × {count}" for heading, count in repeated[:5]]
    return Finding(
        rule_id="sr_ai_repeated_section_scaffold",
        category="AI_STYLE_SIGNAL",
        severity="medium",
        message=(
            "Isti naslovi ili sekcijski markeri ponavljaju se kroz veliki deo dokumenta. "
            "To može biti namerni obrazac, ali vredi proveriti da li je struktura mehanički generisana."
        ),
        count=repeated_instances,
        evidence=pretty,
    )


def heading_fragmentation(text: str) -> Finding | None:
    headings = HEADING_RE.findall(text)
    words = _words(normalize_script(text))
    if len(headings) < 6 or not words:
        return None

    words_per_heading = len(words) / len(headings)
    if words_per_heading >= 45:
        return None

    return Finding(
        rule_id="sr_ai_heading_fragmentation",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "Naslovi su veoma gusti u odnosu na količinu proze. "
            "To je legitimno u dokumentaciji i beleškama, ali u kontinuiranom tekstu može delovati šablonski."
        ),
        count=len(headings),
        evidence=[_compact_ws(h) for h in headings[:5]],
    )


def review(text: str) -> list[Finding]:
    checks = (
        negative_parallelism_density,
        triplet_density,
        repeated_section_scaffold,
        heading_fragmentation,
    )
    return [finding for check in checks if (finding := check(text)) is not None]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Conservative Serbian humanizer seed checks")
    parser.add_argument("path", nargs="?", help="UTF-8 text/Markdown file; stdin if omitted")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    if args.path:
        text = Path(args.path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    findings = review(text)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    elif not findings:
        print("Nema nalaza u prvom konzervativnom srpskom prolazu.")
    else:
        for finding in findings:
            print(f"[{finding.category}] {finding.rule_id}: {finding.message}")
            for item in finding.evidence:
                print(f"  - {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
