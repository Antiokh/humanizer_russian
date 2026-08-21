#!/usr/bin/env python3
"""Guard mechanical-first, dual-runtime architecture against regressions."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from finding_contract import AUTOMATION_LEVELS, PROJECT_CLASSES, VERDICTS  # noqa: E402

REQUIRED_FILES = [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SKILL.md",
    "BOARD_SKILL.md",
    "docs/editorial-board-architecture.md",
    "docs/evidence-provider-architecture.md",
    "libraries/README.md",
    "libraries/native/library.json",
    "libraries/russian/library.json",
    "libraries/russian/rules.json",
    "evidence/README.md",
    "evidence/_template/provider.json",
    "reviewers/native.json",
    "reviewers/russian.json",
    "styles/neutral.json",
    "schemas/evidence-provider.schema.json",
    "schemas/evidence-item.schema.json",
    "schemas/review-report.schema.json",
    "scripts/check.py",
    "scripts/finding_contract.py",
    "scripts/lint.py",
    "scripts/lint_native.py",
    "scripts/benchmark_native_adapter.py",
    "scripts/lint_russian.py",
    "scripts/library_runtime.py",
    "scripts/evidence_runtime.py",
    "scripts/editorial_board.py",
    "scripts/review.py",
    "scripts/validate_libraries.py",
    "scripts/benchmark_lint.py",
    "scripts/benchmark_board.py",
    "tests/lint_cases.json",
    "tests/editorial_board_cases.json",
    "tests/russian_cases.json",
    "tests/russian_board_cases.json",
    "references/russian-core-rules.md",
    ".github/workflows/quality.yml",
]
AGENT_MARKERS = [
    "USER_INTENT + SEMANTICS + NORM",
    "AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score",
    "Mechanical-first",
    "DEFAULT_MECHANICAL",
    "EXTENDED_SOFT",
    "MODEL_ONLY",
    "tests/lint_cases.json",
    "Два продуктовых режима",
    "Книги — подключаемые библиотеки знаний",
]
CHECK_MARKERS = [
    "MECHANICAL_RULES",
    "--extended",
    "--register",
    "from library_runtime import compact_shape, run_libraries",
]
BOARD_MARKERS = [
    "Editorial Board mode",
    "scripts/review.py",
    "CONSENSUS",
    "SOURCE_CONFLICT",
    "Evidence",
    "Russian language layer",
    "RU-SEM-CATEGORY-COLLECTION",
]
QUALITY_MARKERS = [
    "python -m compileall -q scripts",
    "python scripts/lint.py --self-test",
    "python scripts/lint_native.py",
    "python scripts/benchmark_native_adapter.py",
    "python scripts/lint_russian.py",
    "python scripts/benchmark_lint.py",
    "python scripts/benchmark_lint.py tests/russian_cases.json",
    "python scripts/validate_architecture.py",
    "python scripts/validate_libraries.py",
    "python scripts/benchmark_board.py",
    "python scripts/benchmark_board.py tests/russian_board_cases.json",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _finding_schema_failures() -> list[str]:
    schema = json.loads(read("schemas/review-report.schema.json"))
    props = schema["properties"]["findings"]["items"]["properties"]
    expected = {
        "project_class": set(PROJECT_CLASSES),
        "automation_level": set(AUTOMATION_LEVELS),
        "verdict": set(VERDICTS),
    }
    failures: list[str] = []
    for field, values in expected.items():
        actual = set(props.get(field, {}).get("enum", []))
        if actual != values:
            failures.append(
                f"review-report finding {field} enum drift: {sorted(actual)} != {sorted(values)}"
            )
    return failures


def _adapter_contract_failures() -> list[str]:
    failures: list[str] = []
    for path in sorted((ROOT / "libraries").glob("*/library.json")):
        if path.parent.name.startswith("_"):
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("source_type") == "project_core" and manifest.get("adapter") != "review_v1":
            failures.append(
                f"project core {manifest.get('id', path.parent.name)} must use review_v1, got {manifest.get('adapter')!r}"
            )
    runtime = read("scripts/library_runtime.py")
    if "legacy_lint_v1" in runtime or "normalize_legacy" in runtime:
        failures.append("shared library runtime reintroduced legacy adapter compatibility")
    return failures


def main() -> None:
    failures: list[str] = []
    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            failures.append(f"missing required architecture file: {path}")

    if not failures:
        agents = read("AGENTS.md")
        check = read("scripts/check.py")
        board = read("BOARD_SKILL.md")
        quality = read(".github/workflows/quality.yml")
        contributing = read("CONTRIBUTING.md")
        for marker in AGENT_MARKERS:
            if marker not in agents:
                failures.append(f"AGENTS.md lost required marker: {marker}")
        for marker in CHECK_MARKERS:
            if marker not in check:
                failures.append(f"scripts/check.py lost compact-library marker: {marker}")
        for marker in BOARD_MARKERS:
            if marker not in board:
                failures.append(f"BOARD_SKILL.md lost required marker: {marker}")
        for marker in QUALITY_MARKERS:
            if marker not in quality:
                failures.append(f"quality workflow lost required check: {marker}")
        if "evidence_runtime" in check or "run_evidence" in check:
            failures.append("scripts/check.py must not invoke evidence providers")
        if "humanizer+ru" in contributing:
            failures.append("CONTRIBUTING.md reintroduced deprecated project name humanizer+ru")
        failures.extend(_finding_schema_failures())
        failures.extend(_adapter_contract_failures())

    if failures:
        print("ARCHITECTURE CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Architecture contract: OK")


if __name__ == "__main__":
    main()
