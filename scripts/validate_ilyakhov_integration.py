#!/usr/bin/env python3
"""Validate the source-first Ilyakhov integration contract.

This validator checks classification completeness and the source-specific
mechanical module. It does not claim that source heuristics are language norms.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "pishi-sokrashchay"
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import lint_ilyakhov  # noqa: E402

EXPECTED_AUTOMATION = {
    "HARD_GATE": 0,
    "DEFAULT_MECHANICAL": 0,
    "EXTENDED_SOFT": 10,
    "METRIC_ONLY": 3,
    "MODEL_ONLY": 89,
}

AUTO_CODE = {
    "M": "MODEL_ONLY",
    "X": "EXTENDED_SOFT",
    "T": "METRIC_ONLY",
}


def main() -> None:
    manifest = json.loads((STUDY / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["rules"] == 102
    assert manifest["source"]["leaf_sections"] == 177
    assert manifest["source"]["unread_sections"] == 0

    matrix = (STUDY / "integration-matrix.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"^\|\s*(PS-R\d{2,3})\s*\|[^\n]*?\|\s*([EMN])\s*\|\s*([MXT])\s*\|",
        matrix,
        flags=re.M,
    )
    assert len(rows) == 102, f"expected 102 matrix rows, got {len(rows)}"

    ids = [rid for rid, _cls, _auto in rows]
    expected_ids = [f"PS-R{i:02d}" for i in range(1, 103)]
    assert ids == expected_ids, "matrix PS-R sequence is incomplete or out of order"

    project_classes = Counter(cls for _rid, cls, _auto in rows)
    assert project_classes["E"] + project_classes["N"] == 102

    automation = Counter(AUTO_CODE[auto] for _rid, _cls, auto in rows)
    actual = {
        "HARD_GATE": 0,
        "DEFAULT_MECHANICAL": 0,
        "EXTENDED_SOFT": automation["EXTENDED_SOFT"],
        "METRIC_ONLY": automation["METRIC_ONLY"],
        "MODEL_ONLY": automation["MODEL_ONLY"],
    }
    assert actual == EXPECTED_AUTOMATION, f"automation counts drifted: {actual}"

    feasibility = (STUDY / "mechanical-feasibility.md").read_text(encoding="utf-8")
    assert "ILY-M01" in feasibility
    assert "PROJECT_DERIVED" in feasibility

    module_text = (SCRIPTS / "lint_ilyakhov.py").read_text(encoding="utf-8")
    assert "ilyakhov: bureaucratic tautology" in module_text
    assert "PS-R22+PS-R29" in module_text
    assert "cognitive frame" not in module_text.lower(), (
        "do not reintroduce the old broad cognitive-frame detector"
    )

    lint_ilyakhov.self_test()

    print(
        "Ilyakhov integration: OK — 102 rules classified; "
        "0 HARD_GATE / 0 source DEFAULT / 10 EXTENDED / 3 METRIC / 89 MODEL_ONLY; "
        "ILY-M01 project-derived default subset calibrated"
    )


if __name__ == "__main__":
    main()
