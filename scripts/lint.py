#!/usr/bin/env python3
"""Aggregate linter for humanizer_russian.

`lint_core.py` contains the stable main/native/AI surface linter.
Source-specific modules contribute separately calibrated findings and metrics.
The aggregate keeps the same public `lint(text)` and CLI contract.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lint_core import lint as lint_core
from lint_core import self_test as core_self_test
from lint_ilyakhov import lint as lint_ilyakhov
from lint_ilyakhov import self_test as ilyakhov_self_test


def lint(text: str) -> tuple[list[dict], dict]:
    findings, metrics = lint_core(text)
    source_findings, source_metrics = lint_ilyakhov(text)
    return findings + source_findings, {**metrics, **source_metrics}


def self_test() -> None:
    core_self_test()
    ilyakhov_self_test()

    findings, metrics = lint("Подрядчик должен произвести выполнение работ до пятницы.")
    assert any(
        item["rule"] == "ilyakhov: bureaucratic tautology" for item in findings
    ), findings
    assert "ilyakhov_comma_count" in metrics, metrics

    clean, _ = lint("Мы провели исследование и отправили отчёт.")
    assert not [
        item for item in clean if item["rule"] == "ilyakhov: bureaucratic tautology"
    ], clean

    print("aggregate self-test: OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    findings, metrics = lint(text)

    if args.as_json:
        print(
            json.dumps(
                {"findings": findings, "metrics": metrics},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in findings:
            loc = f":{item['line']}" if item["line"] else ""
            note = f" — {item['note']}" if item["note"] else ""
            print(f"{item['kind']}{loc} [{item['rule']}]: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))

    if any(item["kind"] == "ARTIFACT" for item in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
