#!/usr/bin/env python3
"""Validate the derived Ilyakhov editing-layer registry and eval coverage.

This script validates project contracts, not the book itself. It deliberately
works only with derived metadata committed to the repository.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN_FILE = ROOT / "knowledge" / "ilyakhov-patterns.json"
EVAL_FILE = ROOT / "evals" / "ilyakhov.json"

ALLOWED_STATUS = {"core", "conditional", "optional"}
ALLOWED_AUTOMATION = {"model_only", "soft_lint", "review_gate"}
SOFT_LINT_CONTRACT = {"ILY-03", "ILY-05", "ILY-07", "ILY-10", "ILY-12", "ILY-28"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    registry = load(PATTERN_FILE)
    eval_suite = load(EVAL_FILE)

    patterns = registry["patterns"]
    evals = eval_suite["evals"]

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
        "Soft-lint contract changed. Review false-positive risk before changing it: "
        f"registry={sorted(soft_ids)}, expected={sorted(SOFT_LINT_CONTRACT)}"
    )

    eval_ids = [item["id"] for item in evals]
    assert len(eval_ids) == len(set(eval_ids)), "Duplicate eval IDs"

    known = set(pattern_ids)
    covered: set[str] = set()
    for item in evals:
        refs = set(item.get("patterns", []))
        unknown = refs - known
        assert not unknown, f"{item['id']} references unknown patterns: {sorted(unknown)}"
        covered.update(refs)
        assert item.get("prompt", "").strip(), item["id"]
        assert len(item.get("expectations", [])) >= 2, item["id"]

    missing = known - covered
    assert not missing, f"Patterns without eval coverage: {sorted(missing)}"

    status_counts = Counter(item["status"] for item in patterns)
    automation_counts = Counter(item["automation"] for item in patterns)

    print(f"patterns: {len(patterns)}")
    print(f"evals: {len(evals)}")
    print(f"covered: {len(covered)}/{len(known)}")
    print("status:", dict(sorted(status_counts.items())))
    print("automation:", dict(sorted(automation_counts.items())))
    print("Ilyakhov registry validation: OK")


if __name__ == "__main__":
    main()
