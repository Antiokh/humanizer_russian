#!/usr/bin/env python3
"""Validate source-grounded Nora Gal rules and eval traceability.

This validator checks repository contracts only. It does not judge whether a
Russian sentence is good, grammatical, or faithful to Nora Gal by regex.
Semantic/editorial behavior is covered by the eval suite and human/model review.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "evals" / "nora-gal.json"
MAP_PATH = ROOT / "evals" / "nora-gal-map.json"
REFERENCE_PATH = ROOT / "references" / "nora-gal.md"
RULE_INDEX_PATH = ROOT / "references" / "nora-gal-rule-index.md"
SOURCE_LABELS_PATH = ROOT / "references" / "nora-gal-source-labels.md"

RULE_RX = re.compile(r"GAL-[A-Z0-9-]+")
SOURCE_LABEL_RX = re.compile(r"^\d+\.\s+`([^`]+)`\s*$", re.MULTILINE)
EXPECTED_EVAL_IDS = [f"gal-{i:02d}" for i in range(1, 46)]
EXPECTED_RULE_COUNT = 42
MIN_COUNTEREXAMPLES = 10

# Exact labels that are especially easy to accidentally normalize away in docs.
REQUIRED_EXACT_SOURCE_LABELS = {
    "Откуда что берется?",
    "Куда же идет язык?",
    "Мертвый хватает живого",
    "Веревка — вервие простое",
    "«Свинки замяукали»",
    "… Или Дух?",
    "Пять чувств — и еще шестое",
}


def load_json(path: Path) -> dict:
    """Read one repository JSON object as UTF-8."""
    return json.loads(path.read_text(encoding="utf-8"))


def declared_rules(rule_index: str) -> set[str]:
    """Extract unique atomic GAL rule IDs from the rule-index table."""
    return set(RULE_RX.findall(rule_index))


def normalize_chapter_label(label: str) -> str:
    """Normalize only documented ebook/display typography differences."""
    value = label.casefold().replace("ё", "е").replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"…\s+", "…", value)
    return value


def validate() -> None:
    """Validate eval IDs, rule coverage, counterexamples, and source locators."""
    suite = load_json(SUITE_PATH)
    mapping = load_json(MAP_PATH)
    reference = REFERENCE_PATH.read_text(encoding="utf-8")
    rule_index = RULE_INDEX_PATH.read_text(encoding="utf-8")
    source_labels = SOURCE_LABELS_PATH.read_text(encoding="utf-8")

    assert suite.get("version") == 2, suite.get("version")
    assert mapping.get("version") == 2, mapping.get("version")

    evals = suite.get("evals")
    cases = mapping.get("cases")
    assert isinstance(evals, list) and evals, "nora-gal.json must contain evals"
    assert isinstance(cases, list) and cases, "nora-gal-map.json must contain cases"

    eval_ids = [item.get("id") for item in evals]
    map_ids = [item.get("id") for item in cases]

    assert eval_ids == EXPECTED_EVAL_IDS, (
        f"expected ordered IDs {EXPECTED_EVAL_IDS[0]}..{EXPECTED_EVAL_IDS[-1]}, "
        f"got {eval_ids}"
    )
    assert len(eval_ids) == len(set(eval_ids)), "duplicate Nora Gal eval IDs"
    assert map_ids == eval_ids, "traceability map must cover evals in the same order"

    for item in evals:
        assert isinstance(item.get("name"), str) and item["name"].strip(), item
        assert isinstance(item.get("prompt"), str) and item["prompt"].strip(), item
        expectations = item.get("expectations")
        assert isinstance(expectations, list) and len(expectations) >= 3, item["id"]
        assert all(isinstance(x, str) and x.strip() for x in expectations), item["id"]

    index_rules = declared_rules(rule_index)
    assert len(index_rules) == EXPECTED_RULE_COUNT, (
        f"expected {EXPECTED_RULE_COUNT} atomic GAL rules, found {len(index_rules)}"
    )

    exact_source_labels = SOURCE_LABEL_RX.findall(source_labels)
    assert len(exact_source_labels) == 34, (
        f"expected 34 ordered ebook labels, found {len(exact_source_labels)}"
    )
    normalized_source_labels = {
        normalize_chapter_label(label) for label in exact_source_labels
    }

    mapped_rules: set[str] = set()
    mapped_chapters: set[str] = set()
    counterexamples = 0

    for item in cases:
        rules = item.get("rules")
        chapters = item.get("chapters")
        assert isinstance(rules, list) and rules, item["id"]
        assert isinstance(chapters, list) and chapters, item["id"]
        assert isinstance(item.get("counterexample"), bool), item["id"]

        if item["counterexample"]:
            counterexamples += 1

        for rule in rules:
            assert isinstance(rule, str) and RULE_RX.fullmatch(rule), rule
            assert rule in index_rules, f"{rule} missing from rule index"
            assert f"`{rule}`" in reference, f"{rule} missing from nora-gal.md"
            mapped_rules.add(rule)

        for chapter in chapters:
            assert isinstance(chapter, str) and chapter.strip(), item["id"]
            normalized = normalize_chapter_label(chapter)
            assert normalized in normalized_source_labels, (
                f"{item['id']}: unknown source chapter {chapter!r}; "
                "add/correct it in nora-gal-source-labels.md first"
            )
            mapped_chapters.add(normalized)

    assert mapped_rules == index_rules, (
        "every atomic GAL rule must have eval coverage; "
        f"missing={sorted(index_rules - mapped_rules)}, "
        f"unknown={sorted(mapped_rules - index_rules)}"
    )
    assert counterexamples >= MIN_COUNTEREXAMPLES, counterexamples

    for label in REQUIRED_EXACT_SOURCE_LABELS:
        assert label in exact_source_labels, f"exact ebook label missing: {label}"

    # The active suite should use the new namespace, not the legacy six SEM IDs.
    suite_text = SUITE_PATH.read_text(encoding="utf-8")
    assert '"id": "sem-' not in suite_text, "legacy sem-* eval IDs remain active"

    print(
        "Nora Gal validation: OK "
        f"({len(eval_ids)} evals, {len(index_rules)} rules, "
        f"{counterexamples} counterexamples, {len(mapped_chapters)} mapped chapters)"
    )


if __name__ == "__main__":
    validate()
