#!/usr/bin/env python3
"""Validate Ilyakhov/Sarycheva source-library routing and provenance."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "libraries" / "ilyakhov"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def import_linter():
    path = ROOT / "scripts" / "lint_ilyakhov.py"
    spec = importlib.util.spec_from_file_location("validate_ilyakhov_linter", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    manifest = load(LIB / "library.json")
    registry = load(LIB / "rules.json")
    reviewer = load(ROOT / "reviewers" / "ilyakhov.json")

    assert manifest["id"] == "ilyakhov"
    assert manifest["adapter"] == "review_v1"
    assert manifest["linter_path"] == "scripts/lint_ilyakhov.py"
    assert manifest["enabled_by_default"] is True
    assert manifest["status"] == "OPERATIONAL"
    assert manifest["reviewer_id"] == reviewer["id"] == "ilyakhov"
    assert reviewer["library_id"] == "ilyakhov"
    assert reviewer["source_namespace"] == manifest["source_namespace"] == "ILY"
    assert "реальная рецензия" in reviewer["disclaimer"]

    rules = registry["rules"]
    assert len(rules) == 102
    assert [x["rule_id"] for x in rules] == [f"ILY-R{i:02d}" for i in range(1, 103)]
    assert [x["study_rule_id"] for x in rules] == [f"PS-R{i:02d}" for i in range(1, 103)]
    assert all(x["source_locator"].startswith("studies/pishi-sokrashchay/") for x in rules)
    assert not [x for x in rules if x["automation_level"] in {"HARD_GATE", "DEFAULT_MECHANICAL"}]

    by_auto = {}
    for item in rules:
        by_auto[item["automation_level"]] = by_auto.get(item["automation_level"], 0) + 1
    assert by_auto == {"MODEL_ONLY": 89, "EXTENDED_SOFT": 9, "METRIC_ONLY": 4}, by_auto
    assert len(registry["model_only_rule_ids"]) == 89
    assert len(registry["extended_soft_rule_ids"]) == 9
    assert len(registry["metric_only_rule_ids"]) == 4

    derived = registry["project_derived_rules"]
    assert len(derived) == 1
    op = derived[0]
    assert op["rule_id"] == "ILY-M01"
    assert op["automation_level"] == "DEFAULT_MECHANICAL"
    assert op["derived_from"] == ["PS-R22", "PS-R29"]
    assert op["phenomenon_id"] == "editing.action_hidden_in_nominalization"

    # Existing phenomena are reused only where the mechanism is genuinely the
    # same; reviewer/source provenance remains separate.
    chuk = load(ROOT / "libraries" / "chukovsky" / "rules.json")
    chuk_by_id = {x["rule_id"]: x for x in chuk["rules"]}
    ily_by_id = {x["rule_id"]: x for x in rules}
    shared = {
        "ILY-R08": "CHUK-R22",
        "ILY-R16": "CHUK-R21",
        "ILY-R19": "CHUK-R19",
        "ILY-R23": "CHUK-R08",
        "ILY-R26": "CHUK-R07",
        "ILY-R29": "CHUK-R17",
        "ILY-R62": "CHUK-R24",
    }
    for ily_id, chuk_id in shared.items():
        assert ily_by_id[ily_id]["phenomenon_id"] == chuk_by_id[chuk_id]["phenomenon_id"], (ily_id, chuk_id)

    module = import_linter()
    module.self_test()
    default = module.review("Было осуществлено проведение проверки.")
    row = next(x for x in default["findings"] if x["rule_id"] == "ILY-M01")
    assert row["automation_level"] == "DEFAULT_MECHANICAL"
    assert row["verdict"] == "CHANGE"
    assert row["phenomenon_id"] == "editing.action_hidden_in_nominalization"

    soft = module.review("В данной статье мы рассмотрим три варианта.")
    row = next(x for x in soft["findings"] if x["rule_id"] == "ILY-R62")
    assert row["automation_level"] == "EXTENDED_SOFT"
    assert row["verdict"] == "REVIEW"

    print("Ilyakhov library: 102 source rules + ILY-M01; routing/provenance OK")


if __name__ == "__main__":
    main()
