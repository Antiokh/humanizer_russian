#!/usr/bin/env python3
"""Structural quality gate for studies created with docs/book-study-framework.md.

The validator intentionally checks only properties that can be proven
mechanically. Faithful interpretation, counterexample quality and
non-overgeneralization remain manual/model review tasks.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RULE_RE = re.compile(r"^##\s+(CHK-R\d{2})\s+—", re.M)
CONCEPT_RE = re.compile(r"^##\s+(C\d{2})\s+—", re.M)
INTERACTION_RE = re.compile(r"^##\s+(I\d{2})\s+—", re.M)
CLAIM_ROW_RE = re.compile(r"^\|\s*(CLM-\d{2})\s*\|", re.M)
COVERAGE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|.*?\|\s*(VERIFIED|NO_OPERATIONAL_CONTENT|READ|EXTRACTED|UNREAD)\s*\|",
    re.M,
)
LOCATOR_RE = re.compile(r"SRC:L(\d+)(?:-L(\d+))?")


def unique(items: list[str], label: str) -> set[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for item in items:
        if item in seen:
            dupes.add(item)
        seen.add(item)
    assert not dupes, f"duplicate {label}: {sorted(dupes)}"
    return seen


def validate(study_dir: Path) -> dict[str, int]:
    required = [
        "source.md",
        "coverage.md",
        "concepts.md",
        "rules.md",
        "counterexamples.md",
        "interactions.md",
        "claims.md",
        "claims-external.md",
        "evals.json",
        "eval-map.json",
        "audit.md",
        "integration.md",
    ]
    missing = [name for name in required if not (study_dir / name).is_file()]
    assert not missing, f"missing study artifacts: {missing}"

    rules_text = (study_dir / "rules.md").read_text(encoding="utf-8")
    concepts_text = (study_dir / "concepts.md").read_text(encoding="utf-8")
    interactions_text = (study_dir / "interactions.md").read_text(encoding="utf-8")
    claims_text = (study_dir / "claims.md").read_text(encoding="utf-8")
    coverage_text = (study_dir / "coverage.md").read_text(encoding="utf-8")
    audit_text = (study_dir / "audit.md").read_text(encoding="utf-8")

    rule_ids = unique(RULE_RE.findall(rules_text), "rule IDs")
    concept_ids = unique(CONCEPT_RE.findall(concepts_text), "concept IDs")
    interaction_ids = unique(INTERACTION_RE.findall(interactions_text), "interaction IDs")
    claim_ids = unique(CLAIM_ROW_RE.findall(claims_text), "claim IDs")

    assert len(rule_ids) == 38, f"expected 38 rules, got {len(rule_ids)}"
    assert len(concept_ids) == 22, f"expected 22 concepts, got {len(concept_ids)}"
    assert len(interaction_ids) == 20, f"expected 20 interactions, got {len(interaction_ids)}"
    assert len(claim_ids) == 30, f"expected 30 claims, got {len(claim_ids)}"

    # Every atomic rule card must have the framework sections and at least one locator.
    cards = re.split(r"(?=^##\s+CHK-R\d{2}\s+—)", rules_text, flags=re.M)
    cards = [card for card in cards if card.startswith("## CHK-R")]
    required_rule_sections = [
        "Source locator:",
        "Scope:",
        "Basis:",
        "Level:",
        "Confidence:",
        "### Что проверяет",
        "### Почему это важно",
        "### Семантический/функциональный инвариант",
        "### Trigger / признаки",
        "### Диагностика",
        "### Возможные исправления",
        "### Не применять автоматически",
        "### Do not infer",
        "### Взаимодействует с",
        "### Positive example",
        "### Counterexample",
        "### Verification",
    ]
    assert len(cards) == len(rule_ids)
    for card in cards:
        rule_id = RULE_RE.search(card).group(1)  # type: ignore[union-attr]
        for section in required_rule_sections:
            assert section in card, f"{rule_id}: missing section {section}"
        locators = LOCATOR_RE.findall(card)
        assert locators, f"{rule_id}: missing SRC locator"
        for start_s, end_s in locators:
            start = int(start_s)
            end = int(end_s or start_s)
            assert 1 <= start <= end <= 4530, f"{rule_id}: invalid locator {start}-{end}"

    evals = json.loads((study_dir / "evals.json").read_text(encoding="utf-8"))
    eval_map = json.loads((study_dir / "eval-map.json").read_text(encoding="utf-8"))
    eval_ids = unique([item["id"] for item in evals["evals"]], "eval IDs")

    direct_ids = {item_id for item_id in eval_ids if item_id.startswith("chk-e")}
    compound_ids = {item_id for item_id in eval_ids if item_id.startswith("chk-c")}
    assert len(direct_ids) == 38, f"expected 38 direct evals, got {len(direct_ids)}"
    assert len(compound_ids) == 20, f"expected 20 compound evals, got {len(compound_ids)}"
    assert len(eval_ids) == 58, f"expected 58 total evals, got {len(eval_ids)}"

    rule_source = eval_map["rule_source"]
    assert set(rule_source) == rule_ids, (
        f"rule index mismatch: missing={sorted(rule_ids - set(rule_source))}; "
        f"extra={sorted(set(rule_source) - rule_ids)}"
    )
    for rule_id, data in rule_source.items():
        for concept_id in data["concepts"]:
            assert concept_id in concept_ids, f"{rule_id}: unknown concept {concept_id}"
        assert data["source"], f"{rule_id}: empty source map"
        for locator in data["source"]:
            assert LOCATOR_RE.fullmatch(locator), f"{rule_id}: invalid source locator {locator}"

    eval_rule_map = eval_map["eval_rule_map"]
    assert set(eval_rule_map) == eval_ids, (
        f"eval map mismatch: missing={sorted(eval_ids - set(eval_rule_map))}; "
        f"extra={sorted(set(eval_rule_map) - eval_ids)}"
    )
    for eval_id, mapped_rules in eval_rule_map.items():
        assert mapped_rules, f"{eval_id}: no mapped rules"
        for rule_id in mapped_rules:
            assert rule_id in rule_ids, f"{eval_id}: unknown rule {rule_id}"

    # Direct coverage: each atomic rule has at least one chk-eXX scenario.
    directly_covered = {
        rule_id
        for eval_id, mapped_rules in eval_rule_map.items()
        if eval_id.startswith("chk-e")
        for rule_id in mapped_rules
    }
    assert directly_covered == rule_ids, (
        f"rules lacking direct eval: {sorted(rule_ids - directly_covered)}"
    )

    interaction_eval_map = eval_map["interaction_eval_map"]
    assert set(interaction_eval_map) == interaction_ids, (
        f"interaction map mismatch: missing={sorted(interaction_ids - set(interaction_eval_map))}; "
        f"extra={sorted(set(interaction_eval_map) - interaction_ids)}"
    )
    for interaction_id, mapped_evals in interaction_eval_map.items():
        assert mapped_evals, f"{interaction_id}: no compound eval"
        for eval_id in mapped_evals:
            assert eval_id in compound_ids, f"{interaction_id}: non-compound/unknown eval {eval_id}"

    coverage_rows = COVERAGE_ROW_RE.findall(coverage_text)
    assert len(coverage_rows) == 14, f"expected 14 coverage rows, got {len(coverage_rows)}"
    statuses = [status for _, status in coverage_rows]
    incomplete = [status for status in statuses if status not in {"VERIFIED", "NO_OPERATIONAL_CONTENT"}]
    assert not incomplete, f"incomplete coverage statuses: {incomplete}"
    assert "100% VERIFIED" in coverage_text
    assert "unlisted gaps: none" in coverage_text
    assert "unavailable chapters/appendices/dictionary/notes: none" in coverage_text

    assert "Independent deep-book-study status: `COMPLETE`" in audit_text
    assert "[x] 100% sequential reading complete" in audit_text
    assert "[x] overgeneralization audit complete" in audit_text
    assert "[x] unresolved claims explicit" in audit_text

    return {
        "concepts": len(concept_ids),
        "rules": len(rule_ids),
        "claims": len(claim_ids),
        "interactions": len(interaction_ids),
        "evals": len(eval_ids),
        "coverage_rows": len(coverage_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "study_dir",
        nargs="?",
        default="studies/chukovsky-zhivoy-kak-zhizn",
    )
    args = parser.parse_args()
    summary = validate(Path(args.study_dir))
    print("book-study structural validation: OK")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
