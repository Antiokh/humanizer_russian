#!/usr/bin/env python3
"""Validate derived Ilyakhov/Sarycheva registries and eval coverage.

The script validates project contracts, not the book itself. It operates only
on derived metadata committed to the repository.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN_FILE = ROOT / "knowledge" / "ilyakhov-patterns.json"
RECOMMENDATION_FILE = ROOT / "knowledge" / "ilyakhov-recommendations.json"
EVAL_FILE = ROOT / "evals" / "ilyakhov.json"
POSITIVE_EVAL_FILE = ROOT / "evals" / "ilyakhov-positive.json"

ALLOWED_STATUS = {"core", "conditional", "optional"}
ALLOWED_AUTOMATION = {"model_only", "soft_lint", "review_gate"}
SOFT_LINT_CONTRACT = {"ILY-03", "ILY-05", "ILY-07", "ILY-10", "ILY-12", "ILY-28"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    registry = load(PATTERN_FILE)
    rec_registry = load(RECOMMENDATION_FILE)
    eval_suite = load(EVAL_FILE)
    positive_suite = load(POSITIVE_EVAL_FILE)

    patterns = registry["patterns"]
    recommendations = rec_registry["recommendations"]
    evals = eval_suite["evals"]
    positive_evals = positive_suite["evals"]

    pattern_ids = [item["id"] for item in patterns]
    expected_ids = [f"ILY-{i:02d}" for i in range(1, 37)]
    assert pattern_ids == expected_ids, (
        "Pattern registry must remain ordered and contiguous ILY-01..ILY-36; "
        f"got {pattern_ids}"
    )
    assert len(pattern_ids) == len(set(pattern_ids)), "Duplicate pattern IDs"

    for item in patterns:
        assert item["status"] in ALLOWED_STATUS, item
        assert item["automation"] in ALLOWED_AUTOMATION, item
        assert item.get("rule", "").strip(), item
        assert item.get("guard", "").strip(), item

    soft_ids = {item["id"] for item in patterns if item["automation"] == "soft_lint"}
    assert soft_ids == SOFT_LINT_CONTRACT, (
        "Source-like soft-lint contract changed. Review false-positive risk before changing it: "
        f"registry={sorted(soft_ids)}, expected={sorted(SOFT_LINT_CONTRACT)}"
    )

    eval_ids = [item["id"] for item in evals]
    assert len(eval_ids) == len(set(eval_ids)), "Duplicate diagnostic eval IDs"

    known_patterns = set(pattern_ids)
    covered_patterns: set[str] = set()
    for item in evals:
        refs = set(item.get("patterns", []))
        unknown = refs - known_patterns
        assert not unknown, f"{item['id']} references unknown patterns: {sorted(unknown)}"
        covered_patterns.update(refs)
        assert item.get("prompt", "").strip(), item["id"]
        assert len(item.get("expectations", [])) >= 2, item["id"]

    missing_patterns = known_patterns - covered_patterns
    assert not missing_patterns, f"Patterns without eval coverage: {sorted(missing_patterns)}"

    recommendation_ids = [item["id"] for item in recommendations]
    expected_recommendations = [f"ILY-R{i:02d}" for i in range(1, 25)]
    assert recommendation_ids == expected_recommendations, (
        "Recommendation registry must remain ordered and contiguous ILY-R01..ILY-R24; "
        f"got {recommendation_ids}"
    )
    assert len(recommendation_ids) == len(set(recommendation_ids)), "Duplicate recommendation IDs"

    for item in recommendations:
        assert item.get("when", "").strip(), item
        assert item.get("operation", "").strip(), item
        assert item.get("success_test", "").strip(), item
        assert item.get("guard", "").strip(), item
        source_patterns = set(item.get("source_patterns", []))
        assert source_patterns, item
        unknown = source_patterns - known_patterns
        assert not unknown, f"{item['id']} references unknown source patterns: {sorted(unknown)}"

    pos_eval_ids = [item["id"] for item in positive_evals]
    assert len(pos_eval_ids) == len(set(pos_eval_ids)), "Duplicate positive eval IDs"

    known_recommendations = set(recommendation_ids)
    covered_recommendations: set[str] = set()
    for item in positive_evals:
        refs = set(item.get("recommendations", []))
        assert refs, f"{item['id']} has no recommendation references"
        unknown = refs - known_recommendations
        assert not unknown, f"{item['id']} references unknown recommendations: {sorted(unknown)}"
        covered_recommendations.update(refs)
        assert item.get("prompt", "").strip(), item["id"]
        assert len(item.get("expectations", [])) >= 2, item["id"]

    missing_recommendations = known_recommendations - covered_recommendations
    assert not missing_recommendations, (
        "Recommendations without positive eval coverage: "
        f"{sorted(missing_recommendations)}"
    )

    status_counts = Counter(item["status"] for item in patterns)
    automation_counts = Counter(item["automation"] for item in patterns)

    print(f"patterns: {len(patterns)}")
    print(f"diagnostic evals: {len(evals)}")
    print(f"pattern coverage: {len(covered_patterns)}/{len(known_patterns)}")
    print(f"recommendations: {len(recommendations)}")
    print(f"positive evals: {len(positive_evals)}")
    print(f"recommendation coverage: {len(covered_recommendations)}/{len(known_recommendations)}")
    print("status:", dict(sorted(status_counts.items())))
    print("automation:", dict(sorted(automation_counts.items())))
    print("Ilyakhov registries validation: OK")


if __name__ == "__main__":
    main()
