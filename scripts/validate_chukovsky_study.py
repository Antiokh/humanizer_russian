#!/usr/bin/env python3
"""Structural validator for the Chukovsky study/integration gate.

This proves traceability/completeness properties only. It cannot prove faithful
interpretation, good counterexamples, current linguistic norm or model behavior.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "chukovsky-zhivoy-kak-zhizn"

RULE_RE = re.compile(r"^##\s+(CHK-R\d{2})\s+—", re.M)
CONCEPT_RE = re.compile(r"^##\s+(C\d{2})\s+—", re.M)
INTERACTION_RE = re.compile(r"^##\s+(I\d{2})\s+—", re.M)
CLAIM_ROW_RE = re.compile(r"^\|\s*(CLM-\d{2})\s*\|", re.M)
LOCATOR_RE = re.compile(r"SRC:L(\d+)(?:-L(\d+))?")
COVERAGE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|.*?\|\s*(VERIFIED|NO_OPERATIONAL_CONTENT|READ|EXTRACTED|UNREAD)\s*\|",
    re.M,
)
MATRIX_ROW_RE = re.compile(r"^\|\s*(R\d{2})\s*\|", re.M)

ALLOWED_CLASSES = {"NORM", "NATIVE_USAGE", "EDITING", "AI_CALQUE", "AUTHOR", "ARTIFACT"}
ALLOWED_AUTOMATION = {
    "HARD_GATE",
    "DEFAULT_MECHANICAL",
    "EXTENDED_SOFT",
    "METRIC_ONLY",
    "MODEL_ONLY",
}
EXPECTED_AUTOMATION = Counter(
    {
        "HARD_GATE": 0,
        "DEFAULT_MECHANICAL": 0,
        "EXTENDED_SOFT": 7,
        "METRIC_ONLY": 2,
        "MODEL_ONLY": 29,
    }
)
EXPECTED_CLASSES = Counter(
    {
        "NORM": 4,
        "NATIVE_USAGE": 7,
        "EDITING": 23,
        "AI_CALQUE": 0,
        "AUTHOR": 4,
        "ARTIFACT": 0,
    }
)


def read(name: str) -> str:
    return (STUDY / name).read_text(encoding="utf-8")


def unique(items: list[str], label: str) -> set[str]:
    counts = Counter(items)
    dupes = sorted(item for item, count in counts.items() if count > 1)
    assert not dupes, f"duplicate {label}: {dupes}"
    return set(items)


def parse_markdown_table(text: str, prefix: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not re.match(rf"^\|\s*{re.escape(prefix)}\d{{2}}\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        row_id = cells[0]
        assert row_id not in rows, f"duplicate table row: {row_id}"
        rows[row_id] = cells
    return rows


def main() -> None:
    required = [
        "source.md",
        "coverage.md",
        "concepts.md",
        "rules.md",
        "counterexamples.md",
        "interactions.md",
        "claims.md",
        "claims-external.md",
        "evals.json",
        "eval-map.json",
        "audit.md",
        "integration.md",
        "re-audit-2026-08-19.md",
        "integration-matrix.md",
        "mechanical-feasibility.md",
    ]
    missing = [name for name in required if not (STUDY / name).is_file()]
    assert not missing, f"missing Chukovsky study artifacts: {missing}"

    source = read("source.md")
    coverage = read("coverage.md")
    concepts = read("concepts.md")
    rules = read("rules.md")
    interactions = read("interactions.md")
    claims = read("claims.md")
    audit = read("audit.md")
    re_audit = read("re-audit-2026-08-19.md")
    matrix = read("integration-matrix.md")
    feasibility = read("mechanical-feasibility.md")

    assert "Study status: `OPERATIONAL_FOR_INTEGRATION`" in source
    assert "e4db5cef1d6d3483b232020994953aada176f4cde5597d314a0a152428e41bf9" in source
    assert "SRC:L1-L4530" in source

    rule_ids = unique(RULE_RE.findall(rules), "rule IDs")
    concept_ids = unique(CONCEPT_RE.findall(concepts), "concept IDs")
    interaction_ids = unique(INTERACTION_RE.findall(interactions), "interaction IDs")
    claim_ids = unique(CLAIM_ROW_RE.findall(claims), "claim IDs")

    assert len(rule_ids) == 38, f"expected 38 rules, got {len(rule_ids)}"
    assert len(concept_ids) == 22, f"expected 22 concepts, got {len(concept_ids)}"
    assert len(interaction_ids) == 20, f"expected 20 interactions, got {len(interaction_ids)}"
    assert len(claim_ids) == 30, f"expected 30 claims, got {len(claim_ids)}"

    cards = re.split(r"(?=^##\s+CHK-R\d{2}\s+—)", rules, flags=re.M)
    cards = [card for card in cards if card.startswith("## CHK-R")]
    required_sections = [
        "Source locator:",
        "Scope:",
        "Basis:",
        "Level:",
        "Confidence:",
        "### Что проверяет",
        "### Почему это важно",
        "### Семантический/функциональный инвариант",
        "### Trigger / признаки",
        "### Диагностика",
        "### Возможные исправления",
        "### Не применять автоматически",
        "### Do not infer",
        "### Взаимодействует с",
        "### Positive example",
        "### Counterexample",
        "### Verification",
    ]
    assert len(cards) == 38
    for card in cards:
        match = RULE_RE.search(card)
        assert match
        rule_id = match.group(1)
        for section in required_sections:
            assert section in card, f"{rule_id}: missing {section}"
        locators = LOCATOR_RE.findall(card)
        assert locators, f"{rule_id}: missing source locator"
        for start_s, end_s in locators:
            start = int(start_s)
            end = int(end_s or start_s)
            assert 1 <= start <= end <= 4530, f"{rule_id}: invalid locator {start}-{end}"

    coverage_rows = COVERAGE_ROW_RE.findall(coverage)
    assert len(coverage_rows) == 14, f"expected 14 coverage rows, got {len(coverage_rows)}"
    incomplete = [status for _, status in coverage_rows if status not in {"VERIFIED", "NO_OPERATIONAL_CONTENT"}]
    assert not incomplete, f"incomplete coverage statuses: {incomplete}"
    for marker in [
        "Book-level source coverage: `100% VERIFIED`",
        "unlisted gaps: none",
        "unavailable chapters/appendices/dictionary/notes: none",
    ]:
        assert marker in coverage, f"coverage lost marker: {marker}"

    evals = json.loads(read("evals.json"))
    eval_map = json.loads(read("eval-map.json"))
    eval_ids = unique([item["id"] for item in evals["evals"]], "eval IDs")
    direct_ids = {item for item in eval_ids if item.startswith("chk-e")}
    compound_ids = {item for item in eval_ids if item.startswith("chk-c")}
    assert len(direct_ids) == 38
    assert len(compound_ids) == 20
    assert len(eval_ids) == 58

    rule_source = eval_map["rule_source"]
    assert set(rule_source) == rule_ids
    for rule_id, data in rule_source.items():
        assert data["source"], f"{rule_id}: no source mapping"
        for locator in data["source"]:
            assert LOCATOR_RE.fullmatch(locator), f"{rule_id}: bad map locator {locator}"
        for concept_id in data["concepts"]:
            assert concept_id in concept_ids, f"{rule_id}: unknown concept {concept_id}"

    eval_rule_map = eval_map["eval_rule_map"]
    assert set(eval_rule_map) == eval_ids
    directly_covered = {
        rule_id
        for eval_id, mapped_rules in eval_rule_map.items()
        if eval_id.startswith("chk-e")
        for rule_id in mapped_rules
    }
    assert directly_covered == rule_ids

    interaction_eval_map = eval_map["interaction_eval_map"]
    assert set(interaction_eval_map) == interaction_ids
    for interaction_id, mapped_evals in interaction_eval_map.items():
        assert mapped_evals, f"{interaction_id}: no compound eval"
        assert all(item in compound_ids for item in mapped_evals)

    assert "Independent deep-book-study status: `COMPLETE`" in audit
    assert "[x] 100% sequential reading complete" in audit
    assert "[x] overgeneralization audit complete" in audit
    assert "[x] unresolved claims explicit" in audit
    assert "Independent study status after re-audit: `OPERATIONAL_FOR_INTEGRATION`" in re_audit

    matrix_rows = parse_markdown_table(matrix, "R")
    feasibility_rows = parse_markdown_table(feasibility, "R")
    expected_short_ids = {f"R{i:02d}" for i in range(1, 39)}
    assert set(matrix_rows) == expected_short_ids, "integration matrix does not cover exactly R01-R38"
    assert set(feasibility_rows) == expected_short_ids, "mechanical feasibility does not cover exactly R01-R38"

    classes = Counter()
    automation = Counter()
    for rule_id, cells in matrix_rows.items():
        assert len(cells) >= 12, f"{rule_id}: incomplete integration-matrix row"
        project_class = cells[2].strip("`")
        level = cells[3].strip("`")
        assert project_class in ALLOWED_CLASSES, f"{rule_id}: bad class {project_class}"
        assert level in ALLOWED_AUTOMATION, f"{rule_id}: bad automation {level}"
        classes[project_class] += 1
        automation[level] += 1

        feasibility_level = feasibility_rows[rule_id][2].strip("`")
        assert feasibility_level == level, (
            f"{rule_id}: matrix={level}, feasibility={feasibility_level}"
        )

    for key in ALLOWED_CLASSES:
        classes.setdefault(key, 0)
    for key in ALLOWED_AUTOMATION:
        automation.setdefault(key, 0)

    assert classes == EXPECTED_CLASSES, f"project-class counts drifted: {classes}"
    assert automation == EXPECTED_AUTOMATION, f"automation counts drifted: {automation}"

    print("chukovsky study/integration validation: OK")
    print("  concepts: 22")
    print("  rules: 38")
    print("  claims: 30")
    print("  interactions: 20")
    print("  evals: 58")
    print("  coverage rows: 14")
    print("  automation: HARD_GATE=0 DEFAULT_MECHANICAL=0 EXTENDED_SOFT=7 METRIC_ONLY=2 MODEL_ONLY=29")


if __name__ == "__main__":
    main()
