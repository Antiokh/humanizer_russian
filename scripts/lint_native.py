#!/usr/bin/env python3
"""Native/core legacy adapter without source-library findings.

scripts/lint.py remains the standalone aggregate legacy linter for compatibility
and its own regression tests. The knowledge-library runtime must not relabel
source-specific Chukovsky findings as native-core opinions, so this adapter
filters them before legacy normalization. The Chukovsky library consumes the
same underlying mechanical implementation through scripts/lint_chukovsky.py.
"""

from __future__ import annotations

try:
    from lint import lint as aggregate_lint
except ImportError:  # package/import context
    from scripts.lint import lint as aggregate_lint


def lint(text: str) -> tuple[list[dict], dict]:
    findings, metrics = aggregate_lint(text)
    findings = [item for item in findings if item.get("source") != "chukovsky"]
    metrics = {
        key: value
        for key, value in metrics.items()
        if not str(key).startswith("chukovsky_")
    }
    return findings, metrics


def self_test() -> None:
    findings, metrics = lint("Следует отметить, что резервная копия завершилась в 03:10.")
    assert not [item for item in findings if item.get("source") == "chukovsky"]
    assert not [key for key in metrics if key.startswith("chukovsky_")]


if __name__ == "__main__":
    self_test()
    print("lint_native self-test: OK")
