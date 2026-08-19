#!/usr/bin/env python3
"""Mechanical-first checker for humanizer_russian.

Default mode intentionally exposes only deterministic/high-precision surface
checks. The full heuristic linter remains available through --extended.

The point is to make the normal workflow a cheap check, not a model-vs-context
prompt battle. Contextual interpretation is reserved for cases the mechanical
layer cannot settle.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lint import lint

# Findings from lint.py that are useful enough to show in the default,
# mechanical-first pass. ARTIFACT is always included by kind.
MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
    "ilyakhov: bureaucratic tautology",
}


def select_findings(findings: list[dict], extended: bool = False) -> list[dict]:
    if extended:
        return findings
    return [
        item
        for item in findings
        if item["kind"] == "ARTIFACT" or item["rule"] in MECHANICAL_RULES
    ]


def check_text(text: str, extended: bool = False) -> tuple[list[dict], dict]:
    findings, metrics = lint(text)
    selected = select_findings(findings, extended=extended)
    return selected, metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mechanical-first checker for humanizer_russian"
    )
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "--extended",
        action="store_true",
        help="include lower-confidence contextual/AI/style heuristics",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="return exit 2 if any selected finding exists (useful in tests/CI)",
    )
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    findings, metrics = check_text(text, extended=args.extended)

    if args.as_json:
        print(
            json.dumps(
                {
                    "mode": "extended" if args.extended else "mechanical",
                    "findings": findings,
                    "metrics": metrics,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        mode = "extended" if args.extended else "mechanical"
        print(f"mode: {mode}")
        for item in findings:
            loc = f":{item['line']}" if item["line"] else ""
            note = f" — {item['note']}" if item["note"] else ""
            print(f"{item['kind']}{loc} [{item['rule']}]: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))

    if any(item["kind"] == "ARTIFACT" for item in findings):
        raise SystemExit(1)
    if args.fail_on_findings and findings:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
