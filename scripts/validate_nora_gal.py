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
EXPECTED_SHARED_PHENOMENA = {
    "GAL-KANZ-VERB": "editing.action_hidden_in_nominalization",
    "GAL-KANZ-STAMP": "editing.template_without_semantic_gain",
    "GAL-TERM-AUDIENCE": "editing.terminology_audience_fit",
    "GAL-IDIOM-CONTAMINATION": "editing.idiom_play_vs_contamination",
}
SOURCE_SHA256 = "38bdce9dfaf93ea820aae3fd0c7da74e9c2a908f5a3c77da2764793535bf4aa9"
REQUIRED_RULE_FIELDS = {
    "rule_id",
    "source_locator",
    "project_class",
    "scope",
    "automation_level",
    "semantic_invariant",
    "surface_trigger",
    "required_context",
    "false_positive_risk",
    "positive_case",
    "natural_negative",
    "boundary_case",
    "intentional_counterexample",
    "existing_overlap",
    "conflict_with_native_usage",
    "phenomenon_id",
    "operation",
}
REQUIRED_EXACT_SOURCE_LABELS = {
    "Откуда что берется?",
    "Куда же идет язык?",
    "Мертвый хватает живого",
    "Веревка — вервие простое",
    "«Свинки замяукали»",
    "… Или Дух?",
    "Пять чувств — и еще шестое",
}


def load_json(relative: str) -> dict:
    """Load one repository-relative UTF-8 JSON document."""
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def normalize_chapter_label(label: str) -> str:
    """Normalize source labels only enough for stable locator comparison."""
    value = label.casefold().replace("ё", "е").replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"…\s+", "…", value)


def load_operational_rules() -> list[dict]:
    """Load all canonical Gal rule groups and enforce manifest invariants."""
    index = load_json("libraries/gal/rules.json")
    if index.get("rule_count") != EXPECTED_RULE_COUNT:
        raise ValueError(f"rule index count {index.get('rule_count')} != {EXPECTED_RULE_COUNT}")
    if index.get("source_fingerprint_sha256") != SOURCE_SHA256:
        raise ValueError("Gal rule index source fingerprint changed")
    rules: list[dict] = []
    for relative in index["groups"]:
        payload = load_json(relative)
        if payload.get("library_id") != "gal":
            raise ValueError(f"unexpected library_id in {relative}: {payload.get('library_id')!r}")
        rules.extend(payload["rules"])
    return rules


def import_gal_linter():
    """Import the standalone Gal linter from its repository path."""
    path = ROOT / "scripts/lint_gal.py"
    spec = importlib.util.spec_from_file_location("lint_gal_validate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import Gal linter from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate() -> None:
    """Collect structural/source/runtime validation failures and fail CI explicitly."""
    failures: list[str] = []

    def check(condition: bool, message: object) -> None:
        """Record one failed invariant without relying on Python assert semantics."""
        if not condition:
            failures.append(str(message))

    # Source inventory / 100% sequential coverage.
    source = (ROOT / "studies/nora-gal/source.md").read_text(encoding="utf-8")
    coverage = (ROOT / "studies/nora-gal/coverage.md").read_text(encoding="utf-8")
    audit = (ROOT / "studies/nora-gal/audit.md").read_text(encoding="utf-8")
    integration = (ROOT / "studies/nora-gal/integration-matrix.md").read_text(encoding="utf-8")
    for marker in [SOURCE_SHA256, "35 XHTML", "34 navigation", "ch1-7.xhtml", "ch1-29.xhtml"]:
        check(marker in source, f"source inventory lost marker: {marker}")
    for marker in ["35/35", "30/30", "5/5", "34/34", "Inaccessible or unread parts: **none**"]:
        check(marker in coverage, f"coverage lost marker: {marker}")
    check("no inaccessible or unread source parts" in audit.casefold(), "audit lost no-inaccessible-parts conclusion")
    for marker in ["42", "HARD_GATE", "DEFAULT_MECHANICAL", "EXTENDED_SOFT", "MODEL_ONLY"]:
        check(marker in integration, f"integration matrix lost marker: {marker}")

    # Operational classification.
    rules = load_operational_rules()
    check(len(rules) == EXPECTED_RULE_COUNT, f"loaded rule count {len(rules)}")
    ids = [rule["rule_id"] for rule in rules]
    check(len(ids) == len(set(ids)), "duplicate GAL rule IDs")
    by_id = {rule["rule_id"]: rule for rule in rules}
    for rule in rules:
        rule_id = rule.get("rule_id", "<missing-rule-id>")
        missing = REQUIRED_RULE_FIELDS - set(rule)
        check(not missing, f"{rule_id}: missing {sorted(missing)}")
        check(bool(RULE_RX.fullmatch(str(rule_id))), rule_id)
        check(rule.get("project_class") == "EDITING", f"book rule promoted outside EDITING: {rule_id}")
        check(rule.get("automation_level") in EXPECTED_AUTOMATION, rule_id)
        check(isinstance(rule.get("scope"), list) and bool(rule.get("scope")), rule_id)
        check(bool(str(rule.get("intentional_counterexample", "")).strip()), rule_id)
        check(bool(str(rule.get("phenomenon_id", "")).strip()), rule_id)
    actual_automation = dict(Counter(rule["automation_level"] for rule in rules))
    for key in EXPECTED_AUTOMATION:
        actual_automation.setdefault(key, 0)
    check(actual_automation == EXPECTED_AUTOMATION, actual_automation)
    for rule_id, phenomenon_id in EXPECTED_SHARED_PHENOMENA.items():
        rule = by_id.get(rule_id, {})
        check(rule.get("phenomenon_id") == phenomenon_id, (rule_id, rule))
        check(phenomenon_id in rule.get("existing_overlap", []), rule_id)

    residue = (ROOT / "libraries/gal/model-only.md").read_text(encoding="utf-8")
    model_ids = {rule["rule_id"] for rule in rules if rule["automation_level"] == "MODEL_ONLY"}
    missing_residue = sorted(rule_id for rule_id in model_ids if f"`{rule_id}`" not in residue)
    check(not missing_residue, f"MODEL_ONLY rules missing from residue: {missing_residue}")
    for rule_id, phenomenon_id in EXPECTED_SHARED_PHENOMENA.items():
        if rule_id in model_ids:
            check(phenomenon_id in residue, (rule_id, phenomenon_id))

    # Manifest and reviewer: source system, not impersonation.
    manifest = load_json("libraries/gal/library.json")
    reviewer = load_json("reviewers/gal.json")
    check(manifest.get("adapter") == "review_v1", "manifest adapter")
    check(manifest.get("linter_path") == "scripts/lint_gal.py", "manifest linter_path")
    check(manifest.get("reviewer_id") == "gal", "manifest reviewer_id")
    check(manifest.get("source_branch") == "gal", "manifest source_branch")
    check(manifest.get("status") in {"AUDITED", "OPERATIONAL"}, "manifest status")
    check(manifest.get("rules_path") == "libraries/gal/rules.json", "manifest rules_path")
    check(manifest.get("model_only_reference") == "libraries/gal/model-only.md", "manifest model_only_reference")
    check("studies/nora-gal/integration-matrix.md" in manifest.get("references", []), "manifest integration reference")
    check(reviewer.get("library_id") == "gal", "reviewer library_id")
    check(reviewer.get("review_label") == "По системе Норы Галь", "reviewer label")
    check(reviewer.get("avatar") is None, "reviewer avatar must remain null")
    check("не реальная рецензия" in str(reviewer.get("disclaimer", "")).casefold(), "reviewer disclaimer")

    # Source-specific linter emits normalized review_v1 and only audited mechanical rules.
    linter = import_gal_linter()
    linter.self_test()
    sample = linter.review("Команда осуществила проведение проверки.")
    check(bool(sample["findings"]), "Gal linter sample emitted no findings")
    for finding in sample["findings"]:
        check(
            {"rule_id", "phenomenon_id", "project_class", "automation_level", "verdict"} <= set(finding),
            f"incomplete normalized finding: {finding}",
        )
        check(finding.get("automation_level") == "EXTENDED_SOFT", finding)
        check(finding.get("verdict") == "REVIEW", finding)
    shared = linter.review("Осуществляется проведение проверки.")
    check(
        any(
            item["rule_id"] == "GAL-KANZ-VERB"
            and item["phenomenon_id"] == "editing.action_hidden_in_nominalization"
            for item in shared["findings"]
        ),
        shared,
    )
    markup = linter.review("```text\nКоманда осуществила проведение проверки.\n```")
    check(not markup["findings"], markup)
    check(
        set(linter.METRIC_RULE_IDS)
        == {rule["rule_id"] for rule in rules if rule["automation_level"] == "METRIC_ONLY"},
        "Gal linter metric_rule_ids drifted from registry",
    )

    # Canonical 45 original project evals and source traceability map.
    suite = load_json("evals/nora-gal.json")
    mapping = load_json("evals/nora-gal-map.json")
    check(suite.get("version") == 2 and mapping.get("version") == 2, "eval/map version")
    evals = suite["evals"]
    cases = mapping["cases"]
    eval_ids = [item["id"] for item in evals]
    check(eval_ids == EXPECTED_EVAL_IDS, "canonical eval IDs changed")
    check([item["id"] for item in cases] == eval_ids, "eval-map IDs differ from eval suite")

    rule_index = (ROOT / "references/nora-gal-rule-index.md").read_text(encoding="utf-8")
    declared = set(RULE_RX.findall(rule_index))
    check(declared == set(ids), f"rule-index/library mismatch: {sorted(declared ^ set(ids))}")

    source_labels = (ROOT / "references/nora-gal-source-labels.md").read_text(encoding="utf-8")
    exact_labels = SOURCE_LABEL_RX.findall(source_labels)
    check(len(exact_labels) == 34, f"source labels: {len(exact_labels)}")
    for required in REQUIRED_EXACT_SOURCE_LABELS:
        check(required in exact_labels, required)
    normalized = {normalize_chapter_label(label) for label in exact_labels}

    mapped_rules: set[str] = set()
    counterexamples = 0
    for item in cases:
        counterexamples += int(bool(item["counterexample"]))
        for rule_id in item["rules"]:
            check(rule_id in declared, rule_id)
            mapped_rules.add(rule_id)
        for chapter in item["chapters"]:
            check(normalize_chapter_label(chapter) in normalized, (item["id"], chapter))
    check(mapped_rules == declared, f"eval coverage missing {sorted(declared - mapped_rules)}")
    check(counterexamples >= 10, f"counterexamples: {counterexamples}")

    if failures:
        print("Nora Gal validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Nora Gal validation: OK "
        f"(35/35 spine docs, {len(rules)} rules, automation={actual_automation}, "
        f"{len(evals)} evals, {counterexamples} counterexamples, "
        f"shared phenomena={len(EXPECTED_SHARED_PHENOMENA)})"
    )


if __name__ == "__main__":
    validate()