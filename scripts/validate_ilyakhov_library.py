#!/usr/bin/env python3
"""Validate Ilyakhov/Sarycheva source-library routing and provenance."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "libraries" / "ilyakhov"
WEB_STUDY = ROOT / "studies" / "ilyakhov-web"


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


def validate_web_supplement(manifest: dict) -> None:
    web_rules = load(LIB / "web-rules.json")
    source_index = load(WEB_STUDY / "source-index.json")
    stopwords = load(WEB_STUDY / "stopword-corpus.json")

    required_refs = {
        "libraries/ilyakhov/web-rules.json",
        "references/ilyakhov-web.md",
        "studies/ilyakhov-web/source-index.json",
        "studies/ilyakhov-web/stopword-corpus.json",
        "studies/ilyakhov-web/integration-matrix.md",
    }
    require(required_refs <= set(manifest.get("references", [])), "web supplement files must be registered in library references")

    sources = source_index.get("sources", [])
    source_ids = [item.get("id") for item in sources]
    require(len(sources) >= 20, f"expected a substantial curated web source index, got {len(sources)}")
    require(len(source_ids) == len(set(source_ids)), "duplicate Ilyakhov web source ids")
    require(all(str(item.get("url", "")).startswith("https://") for item in sources), "all web sources must use explicit HTTPS URLs")
    require("IW-S21" in source_ids, "historical stop-word list provenance source is missing")
    historical = next(item for item in sources if item["id"] == "IW-S21")
    require(historical.get("kind") == "THIRD_PARTY_ACKNOWLEDGED", "historical stop list must not be presented as an author/official source")
    require("not represented as an official" in historical.get("provenance_note", ""), "historical stop-list caveat is missing")

    require(web_rules.get("source_namespace") == "IW", "web supplement must use a distinct IW namespace")
    cards = web_rules.get("rules", [])
    require([x.get("rule_id") for x in cards] == ["IW-R01", "IW-R02", "IW-R03"], "unexpected web-rule identity set")
    require(all(x.get("automation_level") == "MODEL_ONLY" for x in cards), "web-only rules must remain MODEL_ONLY")
    require(all(x.get("verdict") == "REVIEW" for x in cards), "web-only rules must remain REVIEW guidance")
    require(all(x.get("project_class") in {"EDITING", "NATIVE_USAGE"} for x in cards), "web-only rules cannot become NORM")
    for card in cards:
        refs = card.get("source_ids", [])
        require(refs and set(refs) <= set(source_ids), f"{card.get('rule_id')}: unknown or empty web source ids")

    require(stopwords.get("status") == "REFERENCE_ONLY", "historical stopword corpus must remain REFERENCE_ONLY")
    require(stopwords.get("official_current_glavred_export_found") is False, "do not claim a current official stop-list export")
    policy = str(stopwords.get("runtime_policy", "")).lower()
    require("never" in policy and "automatic" in policy, "stopword runtime policy must prohibit automatic rewrites")
    require(len(stopwords.get("curated_candidate_groups", {})) >= 6, "stopword candidate taxonomy is unexpectedly thin")


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

    validate_web_supplement(manifest)

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

    corporate = module.review("Предлагаем полный спектр услуг, комплексный подход и кратчайшие сроки.")
    row = first_rule(corporate, "ILY-R85")
    require(row["automation_level"] == "EXTENDED_SOFT", f"web-backed R85 automation mismatch: {row}")
    require(row["verdict"] == "REVIEW", f"web-backed R85 verdict mismatch: {row}")

    time_metric = module.review("В наши дни компания выпускает три модели.")
    require(time_metric["metrics"]["ilyakhov_present_time_wrappers"] == 1, f"web-backed R21 metric missing: {time_metric}")
    require(not any(x["rule_id"] == "ILY-R21" for x in time_metric["findings"]), "R21 must remain metric-only")

    print("Ilyakhov library: 102 book rules + ILY-M01 + 3 provenance-separated web MODEL_ONLY cards; routing/provenance OK")


if __name__ == "__main__":
    main()
