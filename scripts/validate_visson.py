#!/usr/bin/env python3
"""Validate complete Lynn Visson study, integration matrix and runtime adapter."""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = "45cd09d0101caa90effa2f7943d4ddf45659536857ae548910fccad144c806ca"
EXPECTED_CLASSES = {"NORM": 2, "NATIVE_USAGE": 22, "EDITING": 2, "AI_CALQUE": 13}
EXPECTED_AUTO = {
    "HARD_GATE": 0,
    "DEFAULT_MECHANICAL": 2,
    "EXTENDED_SOFT": 3,
    "METRIC_ONLY": 2,
    "MODEL_ONLY": 32,
}
REQUIRED = {
    "rule_id",
    "phenomenon_id",
    "source_locator",
    "provenance",
    "project_class",
    "semantic_invariant",
    "scope",
    "automation_level",
    "surface_trigger",
    "required_context",
    "false_positive_risk",
    "positive_case",
    "natural_negative_control",
    "boundary_case",
    "intentional_counterexample",
    "existing_overlap",
    "planned_module",
    "runtime_visibility",
    "english_pattern",
    "russian_native_pattern",
    "likely_interference",
    "diagnosis",
    "possible_russian_repairs",
    "operation",
    "do_not_infer",
}


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> None:
    failures = []

    def check(condition: bool, message: object) -> None:
        if not condition:
            failures.append(str(message))

    source = (ROOT / "studies/lynn-visson/source.md").read_text(encoding="utf-8")
    coverage = (ROOT / "studies/lynn-visson/coverage.md").read_text(encoding="utf-8")
    audit = (ROOT / "studies/lynn-visson/audit.md").read_text(encoding="utf-8")
    obs = (ROOT / "studies/lynn-visson/observations.md").read_text(encoding="utf-8")
    matrix = (ROOT / "studies/lynn-visson/integration-matrix.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        SHA,
        "55/55 content XHTML documents",
        "117/117 endnotes",
        "index_split_002.xhtml",
        "index_split_056.xhtml",
    ):
        check(marker in source, f"source missing {marker}")
    for marker in ("55/55", "117/117", "Inaccessible or unread parts: **none**"):
        check(marker in coverage, f"coverage missing {marker}")

    check(len(re.findall(r"`V-OBS-\d{2}`", obs)) == 72, "atomic observation count != 72")
    check("OPERATIONAL" in audit, "audit status")
    for marker in (
        "39",
        "DEFAULT_MECHANICAL",
        "MODEL_ONLY",
        "VISSON-NORM-ASK-QUESTION",
        "VISSON-CALQUE-PRETEND-CLAUSE",
    ):
        check(marker in matrix, f"matrix missing {marker}")

    index = load("libraries/visson/rules.json")
    rules = []
    for rel in index["groups"]:
        rules.extend(load(rel)["rules"])

    check(index.get("source_fingerprint_sha256") == SHA, "rules source fingerprint")
    check(index.get("rule_count") == 39 and len(rules) == 39, "rule count")

    ids = [rule["rule_id"] for rule in rules]
    check(len(ids) == len(set(ids)), "duplicate rule ids")
    for rule in rules:
        missing = REQUIRED - set(rule)
        check(not missing, f"{rule.get('rule_id')}: missing {sorted(missing)}")
        check(rule.get("rule_id", "").startswith("VISSON-"), rule.get("rule_id"))
        if rule.get("project_class") == "NORM":
            check(
                "EXTERNAL_CONFIRMED" in rule.get("provenance", ""),
                f"{rule.get('rule_id')}: NORM requires EXTERNAL_CONFIRMED provenance",
            )

    classes = dict(Counter(rule["project_class"] for rule in rules))
    automation = dict(Counter(rule["automation_level"] for rule in rules))
    for key in EXPECTED_AUTO:
        automation.setdefault(key, 0)
    check(classes == EXPECTED_CLASSES, classes)
    check(automation == EXPECTED_AUTO, automation)

    model_ids = {
        rule["rule_id"]
        for rule in rules
        if rule["automation_level"] == "MODEL_ONLY"
    }
    residue = (ROOT / "libraries/visson/model-only.md").read_text(encoding="utf-8")
    check(
        not [rule_id for rule_id in model_ids if f"`{rule_id}`" not in residue],
        "model-only residue incomplete",
    )

    manifest = load("libraries/visson/library.json")
    reviewer = load("reviewers/visson.json")
    check(manifest.get("adapter") == "review_v1", "adapter")
    check(manifest.get("source_branch") == "visson", "branch")
    check(manifest.get("status") == "OPERATIONAL", "manifest status")
    check(manifest.get("enabled_by_default") is True, "enabled")
    check(reviewer.get("library_id") == "visson", "reviewer library")
    check(reviewer.get("avatar") is None, "reviewer avatar")
    check(
        "не реальная рецензия" in reviewer.get("disclaimer", "").casefold(),
        "reviewer disclaimer",
    )
    for ref in manifest.get("references", []):
        check((ROOT / ref).is_file(), f"missing ref {ref}")

    suite = load("evals/lynn-visson.json")
    eval_map = load("evals/lynn-visson-map.json")
    check(len(suite["evals"]) == 39 and len(eval_map["cases"]) == 39, "eval count")
    check(
        [item["id"] for item in suite["evals"]]
        == [item["id"] for item in eval_map["cases"]],
        "eval map ids",
    )
    check(
        {item["rule_id"] for item in suite["evals"]} == set(ids),
        "eval rule coverage",
    )

    path = ROOT / "scripts/lint_visson.py"
    spec = importlib.util.spec_from_file_location("lint_visson_validate", path)
    if spec is None or spec.loader is None:
        failures.append("cannot load scripts/lint_visson.py")
    else:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.self_test()

        sample = mod.review(
            "Я хочу спросить у вас вопрос. Он претендует, что ничего не знает."
        )
        got = {item["rule_id"] for item in sample["findings"]}
        check(
            {"VISSON-NORM-ASK-QUESTION", "VISSON-CALQUE-PRETEND-CLAUSE"} <= got,
            got,
        )
        check(
            set(mod.METRIC_RULE_IDS)
            == {
                rule["rule_id"]
                for rule in rules
                if rule["automation_level"] == "METRIC_ONLY"
            },
            "metric ids drift",
        )

    claims = (ROOT / "studies/lynn-visson/claims.md").read_text(encoding="utf-8")
    check(
        "амбициозный проект" in claims and "STRONGLY_NARROWED_2026" in claims,
        "ambitious narrowing missing",
    )
    check("break → ломаться" in audit, "break provenance guard missing")

    if failures:
        print("Lynn Visson validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Lynn Visson validation: OK "
        "(55/55 content docs + 117/117 notes; 72 observations; 39 rules; "
        f"classes={classes}; automation={automation})"
    )


if __name__ == "__main__":
    main()
