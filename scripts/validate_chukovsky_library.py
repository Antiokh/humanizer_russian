#!/usr/bin/env python3
"""Validate Chukovsky library registration and routing completeness."""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "studies" / "chukovsky-zhivoy-kak-zhizn" / "library-routing.md"
MANIFEST = ROOT / "libraries" / "chukovsky" / "library.json"
REVIEWER = ROOT / "reviewers" / "chukovsky.json"
ADAPTER = ROOT / "scripts" / "lint_chukovsky.py"

ROW_RE = re.compile(
    r"^\|\s*(R\d{2})\s*\|\s*`([^`]+)`\s*\|.*?\|\s*`"
    r"(EXTENDED_SOFT|METRIC_ONLY|MODEL_ONLY)(?:[^`]*)`\s*\|",
    re.M,
)

EXPECTED_SOFT = {"R09", "R15", "R17", "R18", "R19", "R24", "R25"}
EXPECTED_METRIC = {"R22", "R31"}
EXPECTED_MODEL = {f"R{i:02d}" for i in range(1, 39)} - EXPECTED_SOFT - EXPECTED_METRIC
EXPECTED_RULE_IDS = {f"CHK-R{i:02d}" for i in range(1, 39)}


def main() -> None:
    for path in [ROUTING, MANIFEST, REVIEWER, ADAPTER]:
        assert path.is_file(), f"missing Chukovsky library artifact: {path.relative_to(ROOT)}"

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    reviewer = json.loads(REVIEWER.read_text(encoding="utf-8"))
    routing = ROUTING.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")

    assert manifest["id"] == "chukovsky"
    assert manifest["source_namespace"] == "CHUK"
    assert manifest["source_branch"] == "chukovsky"
    assert manifest["reviewer_id"] == "chukovsky"
    assert manifest["adapter"] == "review_v1"
    assert manifest["linter_path"] == "scripts/lint_chukovsky.py"
    assert manifest["enabled_by_default"] is True
    assert manifest["status"] == "OPERATIONAL"
    assert reviewer["id"] == "chukovsky"

    rows = ROW_RE.findall(routing)
    assert len(rows) == 38, f"expected 38 routing rows, got {len(rows)}"
    ids = [row[0] for row in rows]
    assert len(set(ids)) == 38, "duplicate routing rule id"
    assert set(ids) == {f"R{i:02d}" for i in range(1, 39)}

    levels = {rule_id: level for rule_id, _, level in rows}
    assert {r for r, level in levels.items() if level == "EXTENDED_SOFT"} == EXPECTED_SOFT
    assert {r for r, level in levels.items() if level == "METRIC_ONLY"} == EXPECTED_METRIC
    assert {r for r, level in levels.items() if level == "MODEL_ONLY"} == EXPECTED_MODEL

    phenomena = {rule_id: phenomenon for rule_id, phenomenon, _ in rows}
    assert all("." in phenomenon for phenomenon in phenomena.values())
    assert phenomena["R17"] == "editing.action_hidden_in_nominalization"
    assert phenomena["R24"] == "editing.metadiscourse_announcement"
    assert phenomena["R32"] == "native.idiom_as_lexical_unit"

    mechanical_rule_ids = set(re.findall(r'"(CHK-R\d{2})"', adapter))
    assert mechanical_rule_ids == {f"CHK-{r}" for r in EXPECTED_SOFT}, mechanical_rule_ids
    assert mechanical_rule_ids <= EXPECTED_RULE_IDS

    print("chukovsky library validation: OK")
    print("  routing rows: 38")
    print("  EXTENDED_SOFT: 7")
    print("  METRIC_ONLY: 2")
    print("  MODEL_ONLY: 29")
    print("  review_v1 library: enabled")


if __name__ == "__main__":
    main()
