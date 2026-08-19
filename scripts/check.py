#!/usr/bin/env python3
"""Compact mechanical-first checker for humanizer_russian.

The compact product consumes all enabled knowledge libraries but only exposes
HARD_GATE / DEFAULT_MECHANICAL findings by default. Lower-confidence mechanical
heuristics are available through --extended.

The point is to keep quick checks cheap and unified while sharing the same
source libraries with editorial-board mode. When several libraries emit the
same phenomenon for the same local surface, compact mode may collapse the
compatible signals into one row while preserving full provenance in JSON.
"""

from __future__ import annotations

import argparse
import json
import re
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


def _compact_key(item: dict) -> tuple[str, int, str]:
    excerpt = re.sub(r"\s+", " ", str(item.get("excerpt", "")).strip().lower())[:180]
    return (str(item.get("phenomenon_id", "")), int(item.get("line", 0) or 0), excerpt)


def _provenance(item: dict) -> dict:
    return {
        "rule_id": item.get("rule_id"),
        "library_id": item.get("library_id"),
        "source_namespace": item.get("source_namespace"),
        "reviewer_id": item.get("reviewer_id"),
        "verdict": item.get("verdict"),
        "operation": item.get("operation"),
    }


def compact_rows(findings: list[dict]) -> list[dict]:
    """Deduplicate compatible findings without erasing source provenance.

    Grouping is deliberately local: same phenomenon, line and normalized
    excerpt. Directional CHANGE/KEEP conflicts are *not* collapsed; those rows
    stay separate so compact mode never manufactures consensus. Editorial board
    remains the place where reviewer disagreement is interpreted explicitly.
    """
    grouped: dict[tuple[str, int, str], list[dict]] = {}
    order: list[tuple[str, int, str]] = []
    for index, item in enumerate(findings):
        key = _compact_key(item)
        if not key[0]:
            key = (f"__unmapped__:{index}", key[1], key[2])
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(item)

    out: list[dict] = []
    for key in order:
        items = grouped[key]
        directional = {item.get("verdict") for item in items if item.get("verdict") in {"CHANGE", "KEEP"}}
        if len(directional) > 1:
            out.extend(compact_shape(item) for item in items)
            continue

        row = compact_shape(items[0])
        if len(items) > 1:
            row["provenance"] = [_provenance(item) for item in items]
            row["deduplicated_sources"] = len(items)
        out.append(row)
    return out


def check_text(text: str, extended: bool = False) -> tuple[list[dict], dict]:
    normalized, metrics = run_libraries(text)
    selected = select_normalized(normalized, extended=extended)
    return compact_rows(selected), metrics


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
