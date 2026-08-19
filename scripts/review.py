#!/usr/bin/env python3
"""Editorial-board mode for humanizer_russian.

Compact mode remains scripts/check.py. This CLI preserves source/reviewer provenance,
keeps disagreements visible and applies a style policy without re-reading whole books.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from editorial_board import build_board
from library_runtime import library_manifests, load_style, reviewer_profiles, run_libraries


def default_libraries_for_style(style: dict[str, Any]) -> list[str]:
    """Select existing enabled libraries whose reviewer is enabled by the style."""
    allowed_reviewers = set(style.get("default_reviewers", []))
    selected: list[str] = []
    for manifest in library_manifests():
        reviewer_id = manifest.get("reviewer_id")
        if reviewer_id is None or reviewer_id in allowed_reviewers:
            selected.append(manifest["id"])
    return selected


def run_review(text: str, style_id: str = "neutral", library_ids: list[str] | None = None) -> dict[str, Any]:
    style = load_style(style_id)
    selected_libraries = library_ids if library_ids is not None else default_libraries_for_style(style)
    findings, metrics = run_libraries(text, library_ids=selected_libraries)
    board = build_board(findings, style)
    profiles = reviewer_profiles()
    used = sorted({f["reviewer_id"] for f in findings if f.get("reviewer_id")})
    return {
        "schema_version": 1,
        "mode": "editorial_board",
        "style": style,
        "libraries": selected_libraries,
        "reviewers": {key: profiles.get(key, {"id": key, "display_name": key}) for key in used},
        "findings": findings,
        "metrics": metrics,
        "board": board,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "## Редколлегия humanizer_russian",
        "",
        f"Стиль: **{report['style']['display_name']}**.",
        "",
    ]
    guardrails = report["board"]["guardrails"]
    if guardrails:
        lines += ["### Guardrails", ""]
        for item in guardrails:
            lines.append(f"- **{item['project_class']}** `{item['rule_id']}`: {item.get('excerpt','')}")
        lines.append("")

    for group in report["board"]["groups"]:
        lines += [
            f"### {group['phenomenon_id']}",
            "",
            f"Фрагмент: `{group.get('excerpt','')}`",
            f"Итог коллегии: **{group['status']} → {group['recommendation']}**",
            "",
        ]
        by_reviewer: dict[str, list[dict[str, Any]]] = {}
        for finding in group["findings"]:
            by_reviewer.setdefault(finding["reviewer_id"], []).append(finding)
        for reviewer_id, findings in by_reviewer.items():
            profile = report["reviewers"].get(reviewer_id, {})
            label = profile.get("review_label") or profile.get("display_name", reviewer_id)
            verdict = group["reviewer_verdicts"][reviewer_id]
            lines.append(f"- **{label}: {verdict}**")
            for finding in findings:
                reason = finding.get("reason") or finding["rule_id"]
                lines.append(f"  - `{finding['rule_id']}` — {reason}")
        lines.append("")

    if not guardrails and not report["board"]["groups"]:
        lines.append("Механические библиотеки не нашли замечаний.")
    lines += [
        "",
        "_Имена авторов обозначают оценку по формализованным правилам источника, а не реальную рецензию или цитату автора._",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Editorial-board review for humanizer_russian")
    parser.add_argument("file", nargs="?")
    parser.add_argument("--style", default="neutral")
    parser.add_argument("--libraries", help="comma-separated library ids; default = libraries enabled by the selected style")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    ids = [x.strip() for x in args.libraries.split(",") if x.strip()] if args.libraries else None
    report = run_review(text, style_id=args.style, library_ids=ids)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")


if __name__ == "__main__":
    main()
