#!/usr/bin/env python3
"""Validate the source-first Ilyakhov integration contract.

This validator checks the completed source study, Gate-A classification,
post-implementation calibration decisions and the source-specific mechanical
module. It does not claim that source heuristics are language norms.
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
import validate_pishi_study  # noqa: E402

# Gate-A matrix is intentionally historical: it records classification before
# implementation/corpus testing. PS-R21 is demoted only after that gate.
EXPECTED_GATE_A_AUTOMATION = {
    "HARD_GATE": 0,
    "DEFAULT_MECHANICAL": 0,
    "EXTENDED_SOFT": 10,
    "METRIC_ONLY": 3,
    "MODEL_ONLY": 89,
}

EXPECTED_EFFECTIVE_AUTOMATION = {
    "HARD_GATE": 0,
    "DEFAULT_MECHANICAL": 0,
    "EXTENDED_SOFT": 9,
    "METRIC_ONLY": 4,
    "MODEL_ONLY": 89,
}

AUTO_CODE = {
    "M": "MODEL_ONLY",
    "X": "EXTENDED_SOFT",
    "T": "METRIC_ONLY",
}


def main() -> None:
    # Gate A must stay green before any runtime classification is accepted.
    validate_pishi_study.main()

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
    gate_a_actual = {
        "HARD_GATE": 0,
        "DEFAULT_MECHANICAL": 0,
        "EXTENDED_SOFT": automation["EXTENDED_SOFT"],
        "METRIC_ONLY": automation["METRIC_ONLY"],
        "MODEL_ONLY": automation["MODEL_ONLY"],
    }
    assert gate_a_actual == EXPECTED_GATE_A_AUTOMATION, (
        f"Gate-A automation counts drifted: {gate_a_actual}"
    )

    feasibility = (STUDY / "mechanical-feasibility.md").read_text(encoding="utf-8")
    calibration = (STUDY / "corpus-calibration.md").read_text(encoding="utf-8")
    external = (STUDY / "external-claims-evidence.md").read_text(encoding="utf-8")

    assert "ILY-M01" in feasibility
    assert "PROJECT_DERIVED" in feasibility
    assert "EXTENDED_SOFT`: **9**" in feasibility
    assert "METRIC_ONLY`: **4**" in feasibility
    assert "218,167" in calibration
    assert "51" in calibration and "PS-R21" in calibration
    assert "PS-CL01" in external and "PS-CL32" in external

    module_text = (SCRIPTS / "lint_ilyakhov.py").read_text(encoding="utf-8")
    assert "ilyakhov: bureaucratic tautology" in module_text
    assert "PS-R22+PS-R29" in module_text
    assert "ilyakhov_present_time_wrappers_without_local_contrast" in module_text
    assert "cognitive frame" not in module_text.lower(), (
        "do not reintroduce the old broad cognitive-frame detector"
    )

    # A bare present-time phrase must now be measured without becoming a finding.
    findings, metrics = lint_ilyakhov.lint(
        "В настоящее время компания выпускает три модели."
    )
    assert metrics["ilyakhov_present_time_wrappers"] == 1
    assert not [item for item in findings if item["rule"] == "ilyakhov: present-time wrapper"]

    lint_ilyakhov.self_test()

    print(
        "Ilyakhov integration: OK — 102 Gate-A rules classified; "
        "effective treatment 0 HARD_GATE / 0 source DEFAULT / "
        "9 EXTENDED / 4 METRIC / 89 MODEL_ONLY; "
        "ILY-M01 project-derived default retained; PS-R21 demoted after corpus calibration"
    )


if __name__ == "__main__":
    main()
