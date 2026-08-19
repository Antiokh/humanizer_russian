#!/usr/bin/env python3
"""Validate Ilyakhov/Sarycheva source-library routing and provenance."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "libraries" / "ilyakhov"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def import_linter():
    path = ROOT / "scripts" / "lint_ilyakhov.py"
    spec = importlib.util.spec_from_file_location("validate_ilyakhov_linter", path)
    require(spec is not None and spec.loader is not None, f"cannot import {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_rule(result: dict, rule_id: str) -> dict:
    rows = [x for x in result.get("findings", []) if x.get("rule_id") == rule_id]
    require(len(rows) == 1, f"expected exactly one {rule_id} finding, got {rows}")
    return rows[0]


def main() -> None:
    manifest = load(LIB / "library.json")
    registry = load(LIB / "rules.json")
    reviewer = load(ROOT / "reviewers" / "ilyakhov.json")

    require(manifest["id"] == "ilyakhov", f"unexpected library id: {manifest['id']!r}")
    require(manifest["adapter"] == "review_v1", f"unexpected adapter: {manifest['adapter']!r}")
    require(manifest["linter_path"] == "scripts/lint_ilyakhov.py", f"unexpected linter path: {manifest['linter_path']!r}")
    require(manifest["enabled_by_default"] is True, "Ilyakhov library must be enabled by default")
    require(manifest["status"] == "OPERATIONAL", f"unexpected library status: {manifest['status']!r}")
    require(manifest["reviewer_id"] == reviewer["id"] == "ilyakhov", "manifest/reviewer id mismatch")
    require(reviewer["library_id"] == "ilyakhov", f"reviewer library mismatch: {reviewer['library_id']!r}")
    require(reviewer["source_namespace"] == manifest["source_namespace"] == "ILY", "source namespace mismatch")
    require("реальная рецензия" in reviewer["disclaimer"], "reviewer disclaimer must reject real-author-review framing")

    rules = registry["rules"]
    require(len(rules) == 102, f"expected 102 source rules, got {len(rules)}")
    require(
        [x["rule_id"] for x in rules] == [f"ILY-R{i:02d}" for i in range(1, 103)],
        "runtime rule ids must be the exact ILY-R01..ILY-R102 sequence",
    )
    require(
        [x["study_rule_id"] for x in rules] == [f"PS-R{i:02d}" for i in range(1, 103)],
        "study rule aliases must be the exact PS-R01..PS-R102 sequence",
    )
    require(
        all(x["source_locator"].startswith("studies/pishi-sokrashchay/") for x in rules),
        "every source rule needs a pishi-sokrashchay provenance locator",
    )
    forbidden_source_automation = [
        x["rule_id"] for x in rules
        if x["automation_level"] in {"HARD_GATE", "DEFAULT_MECHANICAL"}
    ]
    require(
        not forbidden_source_automation,
        f"book source rules must not be HARD_GATE/DEFAULT_MECHANICAL: {forbidden_source_automation}",
    )

    by_auto: dict[str, int] = {}
    for item in rules:
        by_auto[item["automation_level"]] = by_auto.get(item["automation_level"], 0) + 1
    expected_automation = {"MODEL_ONLY": 89, "EXTENDED_SOFT": 9, "METRIC_ONLY": 4}
    require(by_auto == expected_automation, f"automation distribution mismatch: expected {expected_automation}, got {by_auto}")
    require(len(registry["model_only_rule_ids"]) == 89, "model_only_rule_ids must contain exactly 89 ids")
    require(len(registry["extended_soft_rule_ids"]) == 9, "extended_soft_rule_ids must contain exactly 9 ids")
    require(len(registry["metric_only_rule_ids"]) == 4, "metric_only_rule_ids must contain exactly 4 ids")
    require(
        set(registry["model_only_rule_ids"]) == {x["rule_id"] for x in rules if x["automation_level"] == "MODEL_ONLY"},
        "model_only_rule_ids does not match source rule metadata",
    )
    require(
        set(registry["extended_soft_rule_ids"]) == {x["rule_id"] for x in rules if x["automation_level"] == "EXTENDED_SOFT"},
        "extended_soft_rule_ids does not match source rule metadata",
    )
    require(
        set(registry["metric_only_rule_ids"]) == {x["rule_id"] for x in rules if x["automation_level"] == "METRIC_ONLY"},
        "metric_only_rule_ids does not match source rule metadata",
    )

    derived = registry["project_derived_rules"]
    require(len(derived) == 1, f"expected exactly one project-derived operator, got {len(derived)}")
    op = derived[0]
    require(op["rule_id"] == "ILY-M01", f"unexpected project-derived rule id: {op['rule_id']!r}")
    require(op["automation_level"] == "DEFAULT_MECHANICAL", f"ILY-M01 must be DEFAULT_MECHANICAL, got {op['automation_level']!r}")
    require(op["derived_from"] == ["PS-R22", "PS-R29"], f"ILY-M01 provenance mismatch: {op['derived_from']!r}")
    require(op["phenomenon_id"] == "editing.action_hidden_in_nominalization", f"ILY-M01 phenomenon mismatch: {op['phenomenon_id']!r}")

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
        require(
            ily_by_id[ily_id]["phenomenon_id"] == chuk_by_id[chuk_id]["phenomenon_id"],
            f"shared phenomenon mismatch: {ily_id} / {chuk_id}",
        )

    module = import_linter()
    module.self_test()
    default = module.review("Было осуществлено проведение проверки.")
    row = first_rule(default, "ILY-M01")
    require(row["automation_level"] == "DEFAULT_MECHANICAL", f"ILY-M01 automation mismatch: {row}")
    require(row["verdict"] == "CHANGE", f"ILY-M01 verdict mismatch: {row}")
    require(row["phenomenon_id"] == "editing.action_hidden_in_nominalization", f"ILY-M01 finding phenomenon mismatch: {row}")

    soft = module.review("В данной статье мы рассмотрим три варианта.")
    row = first_rule(soft, "ILY-R62")
    require(row["automation_level"] == "EXTENDED_SOFT", f"ILY-R62 automation mismatch: {row}")
    require(row["verdict"] == "REVIEW", f"ILY-R62 verdict mismatch: {row}")

    print("Ilyakhov library: 102 source rules + ILY-M01; routing/provenance OK")


if __name__ == "__main__":
    main()
