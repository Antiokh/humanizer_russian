#!/usr/bin/env python3
"""Conservative mechanical surface checks for the Nora Gal knowledge library.

This module implements only the part of the audited Gal rule set that can be
checked with tolerable precision without pretending to understand voice,
semantics, POV, idiom or information structure. Contextual Gal rules remain
MODEL_ONLY and are described in libraries/gal/rules.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SERVICE_NOMINALIZATION = re.compile(
    r"\b(?:осуществ(?:ить|ил(?:а|и)?|ляет|лять|ляют)|"
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


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _finding(
    *,
    rule_id: str,
    phenomenon_id: str,
    excerpt: str,
    line: int,
    reason: str,
    operation: str,
) -> dict:
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
    clean = re.sub(r"```.*?```|`[^`\n]+`|https?://\S+", " ", text, flags=re.S)
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", clean) if x.strip()]


def review(text: str) -> dict:
    """Return normalized review_v1 findings plus non-normative metrics."""
    findings: list[dict] = []

    for match in SERVICE_NOMINALIZATION.finditer(text):
        findings.append(
            _finding(
                rule_id="GAL-KANZ-VERB",
                phenomenon_id="editing.action_hidden_in_nominalization",
                excerpt=match.group(0),
                line=_line(text, match.start()),
                reason=(
                    "По системе Норы Галь это кандидат на проверку: действие может быть "
                    "спрятано в служебном глаголе и отглагольном существительном. "
                    "Не менять механически в юридическом/терминологическом контексте."
                ),
                operation="compare_direct_finite_verb",
            )
        )

    for match in PSEUDOFORMAL_SHELL.finditer(text):
        findings.append(
            _finding(
                rule_id="GAL-KANZ-PSEUDOFORMAL",
                phenomenon_id="editing.register_pseudoformality",
                excerpt=match.group(0),
                line=_line(text, match.start()),
                reason=(
                    "Узкая многословная служебная оболочка: проверить, нужна ли такая степень "
                    "официальности адресату и жанру."
                ),
                operation="replace_service_shell_with_direct_action",
            )
        )

    for match in REDUNDANT_POSSESSIVE_BODY.finditer(text):
        findings.append(
            _finding(
                rule_id="GAL-EXPLICITNESS",
                phenomenon_id="editing.excessive_explicitness",
                excerpt=match.group(0),
                line=_line(text, match.start()),
                reason=(
                    "Surface-кандидат на лишнюю эксплицитность. Удалять только если владение и "
                    "референты однозначно восстанавливаются; функциональный повтор сохранять."
                ),
                operation="remove_only_recoverable_explicit_material",
            )
        )

    sentences = _sentences(text)
    lengths = [len(WORD.findall(s)) for s in sentences]
    participle_like = PARTICIPLE_LIKE.findall(text)
    words = [w.lower() for w in WORD.findall(text)]
    repeated_adjacent = sum(1 for a, b in zip(words, words[1:]) if a == b)

    metrics = {
        "sentences": len(sentences),
        "sentence_word_max": max(lengths, default=0),
        "long_sentence_candidates_ge_35": sum(1 for x in lengths if x >= 35),
        "participle_like_tokens": len(participle_like),
        "adjacent_exact_word_repeats": repeated_adjacent,
        "metric_rule_ids": [
            "GAL-KANZ-PARTICIPLE",
            "GAL-SOUND-COLLISION",
            "GAL-LONG-SENTENCE-CLARITY",
        ],
        "metrics_are_descriptive": True,
    }
    return {"findings": findings, "metrics": metrics}


def self_test() -> None:
    result = review("Команда осуществила проведение проверки доступности сервиса.")
    assert any(x["rule_id"] == "GAL-KANZ-VERB" for x in result["findings"]), result

    result = review("Команда провела проверку доступности сервиса.")
    assert not any(x["rule_id"] == "GAL-KANZ-VERB" for x in result["findings"]), result

    result = review("Прошу осуществить предоставление информации о задаче.")
    ids = {x["rule_id"] for x in result["findings"]}
    assert "GAL-KANZ-PSEUDOFORMAL" in ids, result

    result = review("Прошу предоставить информацию о задаче.")
    assert not any(x["rule_id"] == "GAL-KANZ-PSEUDOFORMAL" for x in result["findings"]), result

    result = review("Он положил свою руку в свой карман.")
    assert any(x["rule_id"] == "GAL-EXPLICITNESS" for x in result["findings"]), result

    result = review("Я положил свою книгу рядом с его книгой.")
    assert not any(x["rule_id"] == "GAL-EXPLICITNESS" for x in result["findings"]), result

    result = review("Документ, подписанный директором, отправили утром.")
    assert result["metrics"]["participle_like_tokens"] >= 1, result
    assert not result["findings"], result
    print("gal linter self-test: OK")


def main() -> None:
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
