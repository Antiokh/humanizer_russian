#!/usr/bin/env python3
"""Structural validator for the public deep study of «Пиши, сокращай».

This validates only repository contracts: ID continuity, declared counts,
coverage rows, eval/counterexample coverage and the absence of raw book files.
It does not validate the interpretation of the source.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "pishi-sokrashchay"


def ids(pattern: str, text: str) -> set[int]:
    return {int(x) for x in re.findall(pattern, text, flags=re.M)}


def expect_range(found: set[int], last: int, label: str) -> None:
    expected = set(range(1, last + 1))
    missing = sorted(expected - found)
    extra = sorted(found - expected)
    assert not missing and not extra, f"{label}: missing={missing}, extra={extra}"


def main() -> None:
    manifest = json.loads((STUDY / "manifest.json").read_text(encoding="utf-8"))
    counts = manifest["counts"]
    source = manifest["source"]

    assert source["toc_nodes"] == 211
    assert source["leaf_sections"] == 177
    assert source["unread_sections"] == 0
    assert counts == {
        "concepts": 26,
        "rules": 102,
        "counterexample_classes": 30,
        "claims": 32,
        "interactions": 17,
        "evals": 67,
    }

    coverage = (STUDY / "coverage.md").read_text(encoding="utf-8")
    coverage_rows = re.findall(r"^\|\s*(\d+)\s*\|", coverage, flags=re.M)
    assert [int(x) for x in coverage_rows] == list(range(1, 212)), (
        "coverage.md must contain exactly the 211 ordered NCX rows"
    )
    assert "unread/inaccessible sections: **0**" in coverage.lower()

    concepts = (STUDY / "concepts.md").read_text(encoding="utf-8")
    concept_ids = ids(r"^## PS-C(\d+)\b", concepts)
    expect_range(concept_ids, 26, "concepts")

    rule_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(STUDY.glob("rules-*.md"))
    )
    rule_ids = ids(r"^## PS-R(\d+)\b", rule_text)
    expect_range(rule_ids, 102, "rules")

    ce_claims = (STUDY / "counterexamples-claims.md").read_text(encoding="utf-8")
    ce_part, claims_part = ce_claims.split("# Claims audit", 1)
    ce_ids = ids(r"\*\*PS-CE(\d+)\*\*", ce_part)
    claim_ids = ids(r"\*\*PS-CL(\d+)\*\*", claims_part)
    expect_range(ce_ids, 30, "counterexamples")
    expect_range(claim_ids, 32, "claims")

    interactions = (STUDY / "interactions.md").read_text(encoding="utf-8")
    interaction_ids = ids(r"^## PS-I(\d+)\b", interactions)
    expect_range(interaction_ids, 17, "interactions")

    eval_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(STUDY.glob("evals-*.md"))
    )
    eval_ids = ids(r"^## ps-e(\d+)\b", eval_text)
    expect_range(eval_ids, 67, "evals")

    # Every source rule must have at least one original eval and one explicit
    # counterexample class. This prevents one-way "always fix" extraction.
    for n in range(1, 103):
        rid = f"PS-R{n:02d}"
        assert rid in eval_text, f"{rid}: missing eval coverage"
        assert rid in ce_part, f"{rid}: missing counterexample coverage"

    forbidden_ext = {".epub", ".pdf", ".fb2", ".mobi", ".azw", ".azw3"}
    forbidden = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in forbidden_ext
    ]
    assert not forbidden, f"raw book-like files committed: {forbidden}"

    print(
        "OK: 211 NCX nodes / 177 leaf sections; "
        "26 concepts; 102 rules; 30 counterexample classes; "
        "32 claims; 17 interactions; 67 evals; "
        "100% rule eval/counterexample coverage"
    )


if __name__ == "__main__":
    main()
