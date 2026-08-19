#!/usr/bin/env python3
"""Validate the audited Nora Gal source study and its pluggable library contract.

This is structural/traceability validation, not a semantic model benchmark.
"""

from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_RX = re.compile(r"GAL-[A-Z0-9-]+")
SOURCE_LABEL_RX = re.compile(r"^\d+\.\s+`([^`]+)`\s*$", re.MULTILINE)
EXPECTED_EVAL_IDS = [f"gal-{i:02d}" for i in range(1, 46)]
EXPECTED_RULE_COUNT = 42
EXPECTED_AUTOMATION = {
    "HARD_GATE": 0,
    "DEFAULT_MECHANICAL": 0,
    "EXTENDED_SOFT": 3,
    "METRIC_ONLY": 3,
    "MODEL_ONLY": 36,
}
SOURCE_SHA256 = "38bdce9dfaf93ea820aae3fd0c7da74e9c2a908f5a3c77da2764793535bf4aa9"
REQUIRED_RULE_FIELDS = {
    "rule_id", "source_locator", "project_class", "scope", "automation_level",
    "semantic_invariant", "surface_trigger", "required_context", "false_positive_risk",
    "positive_case", "natural_negative", "boundary_case", "intentional_counterexample",
    "existing_overlap", "conflict_with_native_usage", "phenomenon_id", "operation",
}
REQUIRED_EXACT_SOURCE_LABELS = {
    "Откуда что берется?", "Куда же идет язык?", "Мертвый хватает живого",
    "Веревка — вервие простое", "«Свинки замяукали»", "… Или Дух?",
    "Пять чувств — и еще шестое",
}


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def normalize_chapter_label(label: str) -> str:
    value = label.casefold().replace("ё", "е").replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"…\s+", "…", value)


def load_operational_rules() -> list[dict]:
    index = load_json("libraries/gal/rules.json")
    assert index["rule_count"] == EXPECTED_RULE_COUNT
    assert index["source_fingerprint_sha256"] == SOURCE_SHA256
    rules: list[dict] = []
    for relative in index["groups"]:
        payload = load_json(relative)
        assert payload["library_id"] == "gal", relative
        rules.extend(payload["rules"])
    return rules


def import_gal_linter():
    path = ROOT / "scripts/lint_gal.py"
    spec = importlib.util.spec_from_file_location("lint_gal_validate", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate() -> None:
    # Source inventory / 100% sequential coverage.
    source = (ROOT / "studies/nora-gal/source.md").read_text(encoding="utf-8")
    coverage = (ROOT / "studies/nora-gal/coverage.md").read_text(encoding="utf-8")
    audit = (ROOT / "studies/nora-gal/audit.md").read_text(encoding="utf-8")
    for marker in [SOURCE_SHA256, "35 XHTML", "34 navigation", "ch1-7.xhtml", "ch1-29.xhtml"]:
        assert marker in source, f"source inventory lost marker: {marker}"
    for marker in ["35/35", "30/30", "5/5", "34/34", "Inaccessible or unread parts: **none**"]:
        assert marker in coverage, f"coverage lost marker: {marker}"
    assert "no inaccessible or unread source parts" in audit.casefold()

    # Operational classification.
    rules = load_operational_rules()
    assert len(rules) == EXPECTED_RULE_COUNT, len(rules)
    ids = [r["rule_id"] for r in rules]
    assert len(ids) == len(set(ids)), "duplicate GAL rule IDs"
    for rule in rules:
        missing = REQUIRED_RULE_FIELDS - set(rule)
        assert not missing, f"{rule.get('rule_id')}: missing {sorted(missing)}"
        assert RULE_RX.fullmatch(rule["rule_id"]), rule["rule_id"]
        assert rule["project_class"] == "EDITING", f"book rule promoted outside EDITING: {rule['rule_id']}"
        assert rule["automation_level"] in EXPECTED_AUTOMATION, rule["rule_id"]
        assert isinstance(rule["scope"], list) and rule["scope"], rule["rule_id"]
        assert rule["intentional_counterexample"].strip(), rule["rule_id"]
        assert rule["phenomenon_id"].strip(), rule["rule_id"]
    actual_automation = dict(Counter(r["automation_level"] for r in rules))
    for key in EXPECTED_AUTOMATION:
        actual_automation.setdefault(key, 0)
    assert actual_automation == EXPECTED_AUTOMATION, actual_automation

    residue = (ROOT / "libraries/gal/model-only.md").read_text(encoding="utf-8")
    model_ids = {r["rule_id"] for r in rules if r["automation_level"] == "MODEL_ONLY"}
    missing_residue = sorted(rid for rid in model_ids if f"`{rid}`" not in residue)
    assert not missing_residue, f"MODEL_ONLY rules missing from residue: {missing_residue}"

    # Manifest and reviewer: source system, not impersonation.
    manifest = load_json("libraries/gal/library.json")
    reviewer = load_json("reviewers/gal.json")
    assert manifest["adapter"] == "review_v1"
    assert manifest["linter_path"] == "scripts/lint_gal.py"
    assert manifest["reviewer_id"] == "gal"
    assert manifest["source_branch"] == "gal"
    assert manifest["status"] in {"AUDITED", "OPERATIONAL"}
    assert reviewer.get("library_id") == "gal"
    assert reviewer["review_label"] == "По системе Норы Галь"
    assert reviewer["avatar"] is None
    assert "не реальная рецензия" in reviewer["disclaimer"].casefold()

    # Source-specific linter emits normalized review_v1 and only audited mechanical rules.
    linter = import_gal_linter()
    linter.self_test()
    sample = linter.review("Команда осуществила проведение проверки.")
    assert sample["findings"]
    for finding in sample["findings"]:
        assert {"rule_id", "phenomenon_id", "project_class", "automation_level", "verdict"} <= set(finding)
        assert finding["automation_level"] == "EXTENDED_SOFT"
        assert finding["verdict"] == "REVIEW"

    # Canonical 45 original project evals and source traceability map.
    suite = load_json("evals/nora-gal.json")
    mapping = load_json("evals/nora-gal-map.json")
    assert suite.get("version") == 2 and mapping.get("version") == 2
    evals = suite["evals"]
    cases = mapping["cases"]
    eval_ids = [item["id"] for item in evals]
    assert eval_ids == EXPECTED_EVAL_IDS
    assert [item["id"] for item in cases] == eval_ids

    rule_index = (ROOT / "references/nora-gal-rule-index.md").read_text(encoding="utf-8")
    declared = set(RULE_RX.findall(rule_index))
    assert declared == set(ids), f"rule-index/library mismatch: {sorted(declared ^ set(ids))}"

    source_labels = (ROOT / "references/nora-gal-source-labels.md").read_text(encoding="utf-8")
    exact_labels = SOURCE_LABEL_RX.findall(source_labels)
    assert len(exact_labels) == 34, len(exact_labels)
    for required in REQUIRED_EXACT_SOURCE_LABELS:
        assert required in exact_labels, required
    normalized = {normalize_chapter_label(x) for x in exact_labels}

    mapped_rules: set[str] = set()
    counterexamples = 0
    for item in cases:
        counterexamples += int(bool(item["counterexample"]))
        for rid in item["rules"]:
            assert rid in declared, rid
            mapped_rules.add(rid)
        for chapter in item["chapters"]:
            assert normalize_chapter_label(chapter) in normalized, (item["id"], chapter)
    assert mapped_rules == declared, f"eval coverage missing {sorted(declared - mapped_rules)}"
    assert counterexamples >= 10, counterexamples

    print(
        "Nora Gal validation: OK "
        f"(35/35 spine docs, {len(rules)} rules, automation={actual_automation}, "
        f"{len(evals)} evals, {counterexamples} counterexamples)"
    )


if __name__ == "__main__":
    validate()
