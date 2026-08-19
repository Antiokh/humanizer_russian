#!/usr/bin/env python3
"""Compact mechanical-first checker for humanizer_russian.

The compact product consumes all enabled knowledge libraries but only exposes
HARD_GATE / DEFAULT_MECHANICAL findings by default. Lower-confidence mechanical
heuristics are available through --extended.

The point is to keep quick checks cheap and unified while sharing the same
source libraries with editorial-board mode.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from library_runtime import compact_shape, run_libraries

# Retained as an explicit architectural marker and for compatibility with
# existing deterministic tests. New review_v1 libraries declare automation
# level directly in their normalized findings.
MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
}


def select_normalized(findings: list[dict], extended: bool = False) -> list[dict]:
    if extended:
        return [item for item in findings if item.get("automation_level") != "MODEL_ONLY"]
    return [
        item
        for item in findings
        if item.get("automation_level") in {"HARD_GATE", "DEFAULT_MECHANICAL"}
    ]


def check_text(text: str, extended: bool = False) -> tuple[list[dict], dict]:
    normalized, metrics = run_libraries(text)
    selected = select_normalized(normalized, extended=extended)
    return [compact_shape(item) for item in selected], metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Compact mechanical-first checker for humanizer_russian")
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "--extended",
        action="store_true",
        help="include lower-confidence mechanical/style/AI heuristics from enabled libraries",
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
            source = f" · {item['library_id']}" if item.get("library_id") else ""
            print(f"{item['kind']}{loc} [{item['rule']}]{source}: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))

    if any(item["kind"] in {"ARTIFACT", "LANGUAGE_ERROR"} for item in findings):
        raise SystemExit(1)
    if args.fail_on_findings and findings:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
