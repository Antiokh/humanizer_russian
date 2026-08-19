#!/usr/bin/env python3
"""Guard the repository's mechanical-first architecture against accidental regressions.

This validator is intentionally small. It does not freeze implementation details;
it protects only the invariants that future source-layer integrations must retain.
When a source integration validator is installed, the architecture gate runs it
as an additional contract rather than silently trusting the source branch.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SKILL.md",
    "scripts/check.py",
    "scripts/lint.py",
    "scripts/benchmark_lint.py",
    "tests/lint_cases.json",
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
]

CHECK_MARKERS = [
    "MECHANICAL_RULES",
    "--extended",
    "from lint import lint",
]

QUALITY_MARKERS = [
    "python -m compileall -q scripts",
    "python scripts/lint.py --self-test",
    "python scripts/benchmark_lint.py",
    "python scripts/validate_architecture.py",
]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def run_source_integration_validators(failures: list[str]) -> None:
    """Run installed source validators without hard-coding a particular author."""
    scripts = ROOT / "scripts"
    validators = sorted(scripts.glob("validate_*_integration.py"))
    for path in validators:
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode:
            detail = (proc.stdout + "\n" + proc.stderr).strip()
            failures.append(f"source integration validator failed: {path.name}: {detail}")
        else:
            output = proc.stdout.strip()
            if output:
                print(output)


def main() -> None:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        require((ROOT / relative).is_file(), f"missing required architecture file: {relative}", failures)

    if not failures:
        agents = read("AGENTS.md")
        check = read("scripts/check.py")
        quality = read(".github/workflows/quality.yml")
        contributing = read("CONTRIBUTING.md")

        for marker in AGENT_MARKERS:
            require(marker in agents, f"AGENTS.md lost required marker: {marker}", failures)

        for marker in CHECK_MARKERS:
            require(marker in check, f"scripts/check.py lost mechanical-first marker: {marker}", failures)

        for marker in QUALITY_MARKERS:
            require(marker in quality, f"quality workflow lost required check: {marker}", failures)

        require(
            "humanizer+ru" not in contributing,
            "CONTRIBUTING.md reintroduced deprecated project name humanizer+ru",
            failures,
        )

        run_source_integration_validators(failures)

    if failures:
        print("ARCHITECTURE CONTRACT FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Architecture contract: OK")


if __name__ == "__main__":
    main()
