#!/usr/bin/env python3
"""Validate the bounded Velichko source study and Russian-core integration.

This validator proves traceability and architectural boundaries only. It does
not pretend that the unavailable chapters 14–44 were read or reconstructed.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "velichko-kniga-o-grammatike"

CARD_RE = re.compile(r"^##\s+(VEL-(?:R|M)\d{2})\s+—", re.M)
CONCEPT_RE = re.compile(r"^##\s+(VEL-C\d{2})\s+—", re.M)
INTERACTION_RE = re.compile(r"^##\s+(I\d{2})\s+—", re.M)
CLAIM_RE = re.compile(r"^\|\s*(VEL-CLM\d{2})\s*\|", re.M)
LOCATOR_RE = re.compile(r"DOCX2004:P(\d+)(?:-P(\d+))?")

EXPECTED_CLASSES = Counter({"NORM": 5, "NATIVE_USAGE": 22, "AI_CALQUE": 8})
EXPECTED_AUTOMATION = Counter({"MODEL_ONLY": 32, "METRIC_ONLY": 3})


def read(name: str) -> str:
    return (STUDY / name).read_text(encoding="utf-8")


def unique(items: list[str], label: str) -> set[str]:
    counts = Counter(items)
    dupes = sorted(item for item, count in counts.items() if count > 1)
    assert not dupes, f"duplicate {label}: {dupes}"
    return set(items)


def matrix_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("| VEL-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        assert len(cells) == 19, f"bad integration-matrix row width for {cells[:1]}: {len(cells)}"
        assert cells[0] not in rows, f"duplicate integration row {cells[0]}"
        rows[cells[0]] = cells
    return rows


def main() -> None:
    required = [
        "source.md", "coverage.md", "concepts.md", "claims.md", "counterexamples.md",
        "interactions.md", "rules-index.md", "rules-01-12.md", "rules-13-24.md",
        "rules-25-35.md", "integration-matrix.md", "mechanical-feasibility.md",
        "evals.json", "eval-map.json", "integration.md", "audit.md",
    ]
    missing = [name for name in required if not (STUDY / name).is_file()]
    assert not missing, f"missing Velichko study artifacts: {missing}"

    source = read("source.md")
    coverage = read("coverage.md")
    concepts = read("concepts.md")
    claims = read("claims.md")
    interactions = read("interactions.md")
    matrix = read("integration-matrix.md")
    feasibility = read("mechanical-feasibility.md")
    audit = read("audit.md")

    assert "Study status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`" in source
    assert "bed226342fc11ce67df63281a8581a37cf4e13f8d838225c962294ff3640c5d8" in source
    assert "chapters 14–44" in source
    assert "not" in source.lower() and "complete 816-page book" in source
    assert "100% of the **physically available fragment**" in coverage
    assert "13/44 advertised chapter bodies available" in coverage
    assert "31/44 advertised chapter bodies" in coverage
    assert "UNAVAILABLE" in coverage
    assert "no missing body is reconstructed" in coverage

    rule_text = "\n".join(read(name) for name in ["rules-01-12.md", "rules-13-24.md", "rules-25-35.md"])
    rule_ids = unique(CARD_RE.findall(rule_text), "study rule IDs")
    expected_rules = {f"VEL-R{i:02d}" for i in range(1, 33)} | {f"VEL-M{i:02d}" for i in range(1, 4)}
    assert rule_ids == expected_rules, f"study rule set drifted: {sorted(rule_ids ^ expected_rules)}"

    required_fields = [
        "- source_locator:", "- provenance:", "- claim:", "- project_class:",
        "- grammar_domain:", "- automation_level:", "- semantic/function invariant:",
        "- required context:", "- trigger:", "- diagnosis:", "- possible repair:",
        "- positive example:", "- natural negative control:", "- boundary case:",
        "- counterexample:", "- do_not_infer:", "- interactions with other rules:",
        "- confidence:", "- verification status:",
    ]
    cards = [part for part in re.split(r"(?=^##\s+VEL-(?:R|M)\d{2}\s+—)", rule_text, flags=re.M) if part.startswith("## VEL-")]
    assert len(cards) == 35
    for card in cards:
        rid = CARD_RE.search(card).group(1)
        for field in required_fields:
            assert field in card, f"{rid}: missing field {field}"
        locators = LOCATOR_RE.findall(card)
        assert locators, f"{rid}: missing DOCX locator"
        for start_s, end_s in locators:
            start, end = int(start_s), int(end_s or start_s)
            assert 0 <= start <= end <= 2256, f"{rid}: invalid locator {start}-{end}"

    concept_ids = unique(CONCEPT_RE.findall(concepts), "concept IDs")
    claim_ids = unique(CLAIM_RE.findall(claims), "claim IDs")
    interaction_ids = unique(INTERACTION_RE.findall(interactions), "interaction IDs")
    assert len(concept_ids) == 14, len(concept_ids)
    assert len(claim_ids) == 12, len(claim_ids)
    assert len(interaction_ids) == 12, len(interaction_ids)

    rows = matrix_rows(matrix)
    assert set(rows) == expected_rules, "integration matrix does not cover all 35 observations"
    classes = Counter()
    automation = Counter()
    for rid, cells in rows.items():
        classes[cells[4].strip("`")] += 1
        automation[cells[7].strip("`")] += 1
        expected_module = "RKI_METRIC" if rid.startswith("VEL-M") else "RKI_MODEL"
        assert cells[17].strip("`") == expected_module, f"{rid}: unexpected planned module {cells[17]}"
    assert classes == EXPECTED_CLASSES, f"class counts drifted: {classes}"
    assert automation == EXPECTED_AUTOMATION, f"automation counts drifted: {automation}"
    for rid in expected_rules:
        assert f"| {rid} |" in feasibility, f"missing mechanical-feasibility row {rid}"

    evals = json.loads(read("evals.json"))
    eval_map = json.loads(read("eval-map.json"))
    direct = [item for item in evals["evals"] if item["id"].startswith("vel-e")]
    compound = [item for item in evals["evals"] if item["id"].startswith("vel-c")]
    assert len(direct) == 35
    assert len(compound) == 12
    directly_covered = {rid for item in direct for rid in item["rules"]}
    assert directly_covered == expected_rules
    assert set(eval_map["rule_source"]) == expected_rules
    assert set(eval_map["eval_rule_map"]) == {item["id"] for item in evals["evals"]}

    runtime_rules_path = ROOT / "libraries" / "russian" / "rki-rules.json"
    runtime_reference = ROOT / "references" / "russian-rki-grammar.md"
    metric_module = ROOT / "scripts" / "lint_russian_rki_metrics.py"
    assert runtime_rules_path.is_file()
    assert runtime_reference.is_file()
    assert metric_module.is_file()
    runtime_rules = json.loads(runtime_rules_path.read_text(encoding="utf-8"))
    assert len(runtime_rules["rules"]) == 11
    assert all(item["rule_id"].startswith("RU-") for item in runtime_rules["rules"])
    assert all(not item["rule_id"].startswith("VEL-") for item in runtime_rules["rules"])
    assert all(item["automation_level"] == "MODEL_ONLY" for item in runtime_rules["rules"])

    library = json.loads((ROOT / "libraries" / "russian" / "library.json").read_text(encoding="utf-8"))
    assert "libraries/russian/rki-rules.json" in library["references"]
    assert "references/russian-rki-grammar.md" in library["references"]

    assert "OPERATIONAL_FOR_AVAILABLE_FRAGMENT" in audit
    assert "new hard/default warning checks: **0**" in audit
    assert "new metrics: **3**" in audit
    assert "chapters 14–44" in audit

    print("velichko bounded study/integration validation: OK")
    print("  available fragment: 100% verified; advertised book: 13/44 chapter bodies available")
    print("  concepts: 14; observations: 35; claims: 12; interactions: 12")
    print("  evals: 35 direct + 12 compound/preservation")
    print("  automation: HARD_GATE=0 DEFAULT_MECHANICAL=0 EXTENDED_SOFT=0 METRIC_ONLY=3 MODEL_ONLY=32")
    print("  runtime contextual cards: 11 source-neutral RU-* rules")


if __name__ == "__main__":
    main()
