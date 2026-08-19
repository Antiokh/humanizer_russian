#!/usr/bin/env python3
"""Conservative mechanical surface checks for the Nora Gal knowledge library.

Only the audited rules whose surface part can be checked with tolerable
precision live here. Contextual Gal rules remain MODEL_ONLY. Metric-only
signals are descriptive and never create findings.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

try:
    from lint import URL_OR_CODE, strip_frontmatter
except ImportError:  # package/import context
    from scripts.lint import URL_OR_CODE, strip_frontmatter

SERVICE_NOMINALIZATION = re.compile(
    r"\b(?:осуществ(?:ить|ил(?:а|и)?|ляет|лять|ляют|ляется|ляются|лял(?:ся|ась|ось|ись)|ляться)|"
    r"произв(?:ести|ёл|ела|ели|одит|одить|одят))\s+"
    r"(?:проведени(?:е|я)|предоставлени(?:е|я)|выполнени(?:е|я)|"
    r"фиксаци(?:ю|и)|регистраци(?:ю|и))\b",
    re.I,
)
PSEUDOFORMAL_SHELL = re.compile(
    r"\b(?:прошу|просим)\s+(?:вас\s+)?осуществить\s+предоставление\b|"
    r"\bв\s+целях\s+осуществления\s+(?:проведения|выполнения|предоставления)\b",
    re.I,
)
REDUNDANT_POSSESSIVE_BODY = re.compile(
    r"\b(?:свою\s+руку\s+в\s+свой\s+карман|"
    r"своей\s+рукой\s+по\s+своей\s+голове|"
    r"свою\s+руку\s+к\s+своему\s+лицу)\b",
    re.I,
)
WORD = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")
PARTICIPLE_LIKE = re.compile(
    r"\b[А-Яа-яЁё]{3,}(?:вш(?:ий|ая|ее|ие|его|ему|им|их|ими)|"
    r"ющ(?:ий|ая|ее|ие|его|ему|им|их|ими)|"
    r"ащ(?:ий|ая|ее|ие|его|ему|им|их|ими)|"
    r"енн(?:ый|ая|ое|ые|ого|ому|ым|ых|ыми)|"
    r"анн(?:ый|ая|ое|ые|ого|ому|ым|ых|ыми))\b",
    re.I,
)
MARKDOWN_NON_PROSE_LINE = re.compile(r"^\s*(#|\||[-*+]\s|\d+\.\s|>)")


def _line(text: str, pos: int) -> int:
    """Convert a character offset in line-preserving prose to a 1-based line."""
    return text.count("\n", 0, pos) + 1


def _line_preserving_prose(text: str) -> str:
    """Mirror core prose normalization while retaining source line positions.

    The core linter intentionally removes Markdown-only lines from prose. Gal
    findings, however, expose source line numbers, so filtered headings, lists,
    tables, and blockquotes are represented by blank placeholders instead of
    being dropped. URL/code and frontmatter handling reuse the core primitives.
    """
    clean = URL_OR_CODE.sub(lambda match: "\n" * match.group(0).count("\n"), text)
    lines = strip_frontmatter(clean.splitlines())
    kept: list[str] = []
    for line in lines:
        if not line.strip() or MARKDOWN_NON_PROSE_LINE.match(line):
            kept.append("")
            continue
        kept.append(re.sub(r"\*\*|«|»", "", line))
    return "\n".join(kept)


def _finding(
    *,
    rule_id: str,
    phenomenon_id: str,
    excerpt: str,
    line: int,
    reason: str,
    operation: str,
) -> dict:
    """Build one normalized review_v1 Gal finding."""
    return {
        "rule_id": rule_id,
        "phenomenon_id": phenomenon_id,
        "project_class": "EDITING",
        "automation_level": "EXTENDED_SOFT",
        "verdict": "REVIEW",
        "line": line,
        "excerpt": excerpt[:180],
        "reason": reason,
        "operation": operation,
        "confidence": None,
    }


def _sentences(text: str) -> list[str]:
    """Split normalized prose into lightweight sentence candidates."""
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]


def _sound_echo_pairs(words: list[str]) -> int:
    """Count only a crude adjacent phonographic echo; this is a metric, not a verdict."""
    count = 0
    for left, right in zip(words, words[1:]):
        if left == right or len(left) < 5 or len(right) < 5:
            continue
        if left[:3] == right[:3] or left[-3:] == right[-3:]:
            count += 1
    return count


def review(text: str) -> dict:
    """Return normalized review_v1 findings plus non-normative metrics."""
    findings: list[dict] = []
    prose = _line_preserving_prose(text)

    for match in SERVICE_NOMINALIZATION.finditer(prose):
        findings.append(
            _finding(
                rule_id="GAL-KANZ-VERB",
                phenomenon_id="editing.action_hidden_in_nominalization",
                excerpt=match.group(0),
                line=_line(prose, match.start()),
                reason=(
                    "По системе Норы Галь это кандидат на проверку: действие может быть спрятано "
                    "в служебном глаголе и отглагольном существительном. Не менять механически "
                    "в юридическом/терминологическом контексте."
                ),
                operation="compare_direct_finite_verb",
            )
        )

    for match in PSEUDOFORMAL_SHELL.finditer(prose):
        findings.append(
            _finding(
                rule_id="GAL-KANZ-PSEUDOFORMAL",
                phenomenon_id="editing.register_pseudoformality",
                excerpt=match.group(0),
                line=_line(prose, match.start()),
                reason="Узкая многословная служебная оболочка: проверить, нужна ли такая степень официальности адресату и жанру.",
                operation="replace_service_shell_with_direct_action",
            )
        )

    for match in REDUNDANT_POSSESSIVE_BODY.finditer(prose):
        findings.append(
            _finding(
                rule_id="GAL-EXPLICITNESS",
                phenomenon_id="editing.excessive_explicitness",
                excerpt=match.group(0),
                line=_line(prose, match.start()),
                reason=(
                    "Surface-кандидат на лишнюю эксплицитность. Удалять только если владение и "
                    "референты однозначно восстанавливаются; функциональный повтор сохранять."
                ),
                operation="remove_only_recoverable_explicit_material",
            )
        )

    sentences = _sentences(prose)
    lengths = [len(WORD.findall(sentence)) for sentence in sentences]
    words = [word.lower() for word in WORD.findall(prose)]
    metrics = {
        "sentences": len(sentences),
        "sentence_word_counts": lengths,
        "sentence_word_max": max(lengths, default=0),
        "sentence_word_median": statistics.median(lengths) if lengths else 0,
        "participle_like_tokens": len(PARTICIPLE_LIKE.findall(prose)),
        "sound_echo_adjacent_pairs": _sound_echo_pairs(words),
        "metric_rule_ids": [
            "GAL-KANZ-PARTICIPLE",
            "GAL-SOUND-COLLISION",
            "GAL-LONG-SENTENCE-CLARITY",
        ],
        "metrics_are_descriptive": True,
    }
    return {"findings": findings, "metrics": metrics}


def self_test() -> None:
    """Run deterministic positive, negative, markup, metric, and line-map checks."""
    result = review("Команда осуществила проведение проверки доступности сервиса.")
    assert any(x["rule_id"] == "GAL-KANZ-VERB" for x in result["findings"]), result
    result = review("Осуществляется проведение проверки доступности сервиса.")
    assert any(x["rule_id"] == "GAL-KANZ-VERB" for x in result["findings"]), result
    result = review("Команда провела проверку доступности сервиса.")
    assert not any(x["rule_id"] == "GAL-KANZ-VERB" for x in result["findings"]), result

    result = review("Прошу осуществить предоставление информации о задаче.")
    assert "GAL-KANZ-PSEUDOFORMAL" in {x["rule_id"] for x in result["findings"]}, result
    result = review("Прошу предоставить информацию о задаче.")
    assert not any(x["rule_id"] == "GAL-KANZ-PSEUDOFORMAL" for x in result["findings"]), result

    result = review("Он положил свою руку в свой карман.")
    assert any(x["rule_id"] == "GAL-EXPLICITNESS" for x in result["findings"]), result
    result = review("Я положил свою книгу рядом с его книгой.")
    assert not any(x["rule_id"] == "GAL-EXPLICITNESS" for x in result["findings"]), result

    markup = """# Заголовок

```text
Команда осуществила проведение проверки доступности сервиса.
Прошу осуществить предоставление информации о задаче.
Он положил свою руку в свой карман.
```
"""
    result = review(markup)
    assert not result["findings"], result

    positioned = """# Заголовок

- служебный пункт
> цитата
Команда осуществила проведение проверки доступности сервиса.
"""
    result = review(positioned)
    verb = next(x for x in result["findings"] if x["rule_id"] == "GAL-KANZ-VERB")
    assert verb["line"] == 5, result

    result = review("Документ, подписанный директором, отправили утром.")
    assert result["metrics"]["participle_like_tokens"] >= 1, result
    assert not result["findings"], result
    result = review("Это решение, отражение прежней идеи, осталось в черновике.")
    assert result["metrics"]["sound_echo_adjacent_pairs"] >= 1, result
    print("gal linter self-test: OK")


def main() -> None:
    """Run the standalone Gal reviewer CLI."""
    parser = argparse.ArgumentParser(description="Nora Gal source-specific surface reviewer")
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    result = review(text)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["findings"]:
            print(f"{item['rule_id']}:{item['line']} {item['excerpt']} — {item['reason']}")
        print(json.dumps(result["metrics"], ensure_ascii=False))


if __name__ == "__main__":
    main()