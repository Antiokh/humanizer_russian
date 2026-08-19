#!/usr/bin/env python3
"""Validate Chukovsky library registration, rule identity and routing completeness."""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "libraries" / "chukovsky" / "rules.json"
ROUTING = ROOT / "studies" / "chukovsky-zhivoy-kak-zhizn" / "library-routing.md"
MANIFEST = ROOT / "libraries" / "chukovsky" / "library.json"
REVIEWER = ROOT / "reviewers" / "chukovsky.json"
ADAPTER = ROOT / "scripts" / "lint_chukovsky.py"

EXPECTED_SOFT = {"CHUK-R09", "CHUK-R15", "CHUK-R17", "CHUK-R18", "CHUK-R19", "CHUK-R24", "CHUK-R25"}
EXPECTED_METRIC = {"CHUK-R22", "CHUK-R31"}
EXPECTED_ALL = {f"CHUK-R{i:02d}" for i in range(1, 39)}
EXPECTED_MODEL = EXPECTED_ALL - EXPECTED_SOFT - EXPECTED_METRIC
EXPECTED_STUDY = {f"CHK-R{i:02d}" for i in range(1, 39)}


def main() -> None:
    for path in [REGISTRY, ROUTING, MANIFEST, REVIEWER, ADAPTER]:
        assert path.is_file(), f"missing Chukovsky library artifact: {path.relative_to(ROOT)}"

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    reviewer = json.loads(REVIEWER.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    adapter = ADAPTER.read_text(encoding="utf-8")

    assert manifest["id"] == "chukovsky"
    assert manifest["source_namespace"] == "CHUK"
    assert manifest["source_branch"] == "chukovsky"
    assert manifest["reviewer_id"] == "chukovsky"
    assert manifest["adapter"] == "review_v1"
    assert manifest["linter_path"] == "scripts/lint_chukovsky.py"
    assert manifest["enabled_by_default"] is True
    assert manifest["status"] == "OPERATIONAL"
    assert manifest["rules_path"] == "libraries/chukovsky/rules.json"
    assert "libraries/chukovsky/rules.json" in manifest["references"]

    assert reviewer["id"] == "chukovsky"
    assert reviewer["library_id"] == "chukovsky"
    assert reviewer["source_namespace"] == "CHUK"
    assert reviewer["avatar"] is None or isinstance(reviewer["avatar"], dict)
    assert "не реальная рецензия" in reviewer["disclaimer"]

    assert registry["library_id"] == "chukovsky"
    assert registry["source_namespace"] == "CHUK"
    assert registry["study_namespace"] == "CHK"
    rules = registry["rules"]
    assert len(rules) == 38, f"expected 38 registry rules, got {len(rules)}"

    runtime_ids = {row["rule_id"] for row in rules}
    study_ids = {row["study_rule_id"] for row in rules}
    assert runtime_ids == EXPECTED_ALL
    assert study_ids == EXPECTED_STUDY
    assert len(runtime_ids) == len(rules)
    assert all(row["rule_id"].startswith(manifest["source_namespace"] + "-") for row in rules)
    assert all("." in row["phenomenon_id"] for row in rules)
    assert all(row.get("source_locator", "").startswith("SRC:") for row in rules)

    by_level = {
        level: {row["rule_id"] for row in rules if row["automation_level"] == level}
        for level in {"HARD_GATE", "DEFAULT_MECHANICAL", "EXTENDED_SOFT", "METRIC_ONLY", "MODEL_ONLY"}
    }
    assert by_level["HARD_GATE"] == set()
    assert by_level["DEFAULT_MECHANICAL"] == set()
    assert by_level["EXTENDED_SOFT"] == EXPECTED_SOFT
    assert by_level["METRIC_ONLY"] == EXPECTED_METRIC
    assert by_level["MODEL_ONLY"] == EXPECTED_MODEL
    assert set(registry["model_only_rule_ids"]) == EXPECTED_MODEL

    by_id = {row["rule_id"]: row for row in rules}
    assert by_id["CHUK-R17"]["phenomenon_id"] == "editing.action_hidden_in_nominalization"
    assert by_id["CHUK-R24"]["phenomenon_id"] == "editing.metadiscourse_announcement"
    assert by_id["CHUK-R32"]["phenomenon_id"] == "native.idiom_as_lexical_unit"

    adapter_rule_ids = set(re.findall(r'"(CHUK-R\d{2})"', adapter))
    assert EXPECTED_SOFT <= adapter_rule_ids, adapter_rule_ids
    assert not re.search(r'"CHK-R\d{2}"', adapter), "legacy study ids leaked into runtime adapter"

    print("chukovsky library validation: OK")
    print("  canonical runtime rules: 38 (CHUK-Rxx)")
    print("  historical study aliases: 38 (CHK-Rxx)")
    print("  HARD_GATE: 0")
    print("  DEFAULT_MECHANICAL: 0")
    print("  EXTENDED_SOFT: 7")
    print("  METRIC_ONLY: 2")
    print("  MODEL_ONLY: 29")
    print("  review_v1 library: enabled")


if __name__ == "__main__":
    main()
