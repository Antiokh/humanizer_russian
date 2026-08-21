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

from finding_contract import (
    AUTOMATION_PRIORITY,
    DEFAULT_VISIBLE_AUTOMATION_LEVELS,
    EXTENDED_VISIBLE_AUTOMATION_LEVELS,
    GUARDRAIL_CLASSES,
    VERDICT_PRIORITY,
)
from library_runtime import compact_shape, run_libraries

MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
}


def select_normalized(findings: list[dict], extended: bool = False) -> list[dict]:
    allowed = (
        EXTENDED_VISIBLE_AUTOMATION_LEVELS
        if extended
        else DEFAULT_VISIBLE_AUTOMATION_LEVELS
    )
    return [item for item in findings if item.get("automation_level") in allowed]


def _normalized_excerpt(item: dict) -> str:
    return re.sub(r"\s+", " ", str(item.get("excerpt", "")).strip().lower())[:180]


def _line_no(item: dict) -> int:
    return int(item.get("line", 0) or 0)


def _provenance(item: dict) -> dict:
    return {
        "rule_id": item.get("rule_id"),
        "library_id": item.get("library_id"),
        "source_namespace": item.get("source_namespace"),
        "reviewer_id": item.get("reviewer_id"),
        "project_class": item.get("project_class"),
        "automation_level": item.get("automation_level"),
        "verdict": item.get("verdict"),
        "operation": item.get("operation"),
    }


def _provenance_key(item: dict) -> tuple[str, str, str]:
    return (
        str(item.get("library_id") or ""),
        str(item.get("rule_id") or ""),
        str(item.get("reviewer_id") or ""),
    )


def _group_compatible_surface(findings: list[dict]) -> list[list[dict]]:
    groups: list[dict] = []
    for index, item in enumerate(findings):
        phenomenon = str(item.get("phenomenon_id") or "") or f"__unmapped__:{index}"
        excerpt = _normalized_excerpt(item)
        line = _line_no(item)
        candidates = [
            group
            for group in groups
            if group["phenomenon_id"] == phenomenon and group["excerpt"] == excerpt
        ]

        target = None
        if line > 0:
            exact = [group for group in candidates if line in group["known_lines"]]
            if len(exact) == 1:
                target = exact[0]
            elif not exact:
                unknown_only = [group for group in candidates if not group["known_lines"]]
                if len(unknown_only) == 1:
                    target = unknown_only[0]
        elif len(candidates) == 1:
            target = candidates[0]

        if target is None:
            target = {
                "phenomenon_id": phenomenon,
                "excerpt": excerpt,
                "known_lines": set(),
                "items": [],
            }
            groups.append(target)
        if line > 0:
            target["known_lines"].add(line)
        target["items"].append(item)

    return [group["items"] for group in groups]


def _compact_winner_key(item: dict) -> tuple[int, int, int, str, str, str]:
    project_class = item.get("project_class")
    guardrail_rank = 2 if project_class == "ARTIFACT" else 1 if project_class == "NORM" else 0
    return (
        guardrail_rank,
        AUTOMATION_PRIORITY[item["automation_level"]],
        VERDICT_PRIORITY[item["verdict"]],
        str(project_class),
        str(item.get("library_id") or ""),
        str(item.get("rule_id") or ""),
    )


def compact_rows(findings: list[dict]) -> list[dict]:
    out: list[dict] = []
    for items in _group_compatible_surface(findings):
        directional = {
            item.get("verdict")
            for item in items
            if item.get("verdict") in {"CHANGE", "KEEP"}
        }
        if len(directional) > 1:
            out.extend(compact_shape(item) for item in items)
            continue

        winner = max(items, key=_compact_winner_key)
        row = compact_shape(winner)
        if len(items) > 1:
            row["provenance"] = [
                _provenance(item) for item in sorted(items, key=_provenance_key)
            ]
            row["deduplicated_sources"] = len(items)
        out.append(row)
    return out


def has_blocking_findings(findings: list[dict]) -> bool:
    """Guard CLI exit behavior with normalized project classes, not lossy display kinds."""
    return any(item.get("project_class") in GUARDRAIL_CLASSES for item in findings)


def check_text(
    text: str,
    extended: bool = False,
    register: str = "general",
) -> tuple[list[dict], dict]:
    """Run enabled libraries and return compact findings plus metrics."""
    normalized, metrics = run_libraries(
        text,
        context={"mode": "compact", "register": register},
    )
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
    parser.add_argument(
        "--register",
        choices=["general", "everyday", "professional", "technical"],
        default="general",
        help="text register; everyday promotes jargon/term candidates into the compact default surface",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="return exit 2 if any selected finding exists (useful in tests/CI)",
    )
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    findings, metrics = check_text(text, extended=args.extended, register=args.register)

    if args.as_json:
        print(
            json.dumps(
                {
                    "mode": "extended" if args.extended else "mechanical",
                    "register": args.register,
                    "findings": findings,
                    "metrics": metrics,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        mode = "extended" if args.extended else "mechanical"
        print(f"mode: {mode}; register: {args.register}")
        for item in findings:
            loc = f":{item['line']}" if item["line"] else ""
            note = f" — {item['note']}" if item["note"] else ""
            source = f" · {item['library_id']}" if item.get("library_id") else ""
            print(f"{item['kind']}{loc} [{item['rule']}]{source}: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))

    if has_blocking_findings(findings):
        raise SystemExit(1)
    if args.fail_on_findings and findings:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
