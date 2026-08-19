#!/usr/bin/env python3
"""Guard mechanical-first, dual-runtime architecture against regressions."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SKILL.md",
    "BOARD_SKILL.md",
    "docs/editorial-board-architecture.md",
    "libraries/README.md",
    "libraries/native/library.json",
    "reviewers/native.json",
    "styles/neutral.json",
    "scripts/check.py",
    "scripts/lint.py",
    "scripts/library_runtime.py",
    "scripts/editorial_board.py",
    "scripts/review.py",
    "scripts/validate_libraries.py",
    "scripts/benchmark_lint.py",
    "scripts/benchmark_board.py",
    "tests/lint_cases.json",
    "tests/editorial_board_cases.json",
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
    "from library_runtime import compact_shape, run_libraries",
]

BOARD_MARKERS = [
    "Editorial Board mode",
    "scripts/review.py",
    "CONSENSUS",
    "SOURCE_CONFLICT",
]

QUALITY_MARKERS = [
    "python -m compileall -q scripts",
    "python scripts/lint.py --self-test",
    "python scripts/benchmark_lint.py",
    "python scripts/validate_architecture.py",
    "python scripts/validate_libraries.py",
    "python scripts/benchmark_board.py",
]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        require((ROOT / relative).is_file(), f"missing required architecture file: {relative}", failures)

    if not failures:
        agents = read("AGENTS.md")
        check = read("scripts/check.py")
        board = read("BOARD_SKILL.md")
        quality = read(".github/workflows/quality.yml")
        contributing = read("CONTRIBUTING.md")

        for marker in AGENT_MARKERS:
            require(marker in agents, f"AGENTS.md lost required marker: {marker}", failures)
        for marker in CHECK_MARKERS:
            require(marker in check, f"scripts/check.py lost compact-library marker: {marker}", failures)
        for marker in BOARD_MARKERS:
            require(marker in board, f"BOARD_SKILL.md lost required marker: {marker}", failures)
        for marker in QUALITY_MARKERS:
            require(marker in quality, f"quality workflow lost required check: {marker}", failures)

        require(
            "humanizer+ru" not in contributing,
            "CONTRIBUTING.md reintroduced deprecated project name humanizer+ru",
            failures,
        )

    if failures:
        print("ARCHITECTURE CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Architecture contract: OK")


if __name__ == "__main__":
    main()
