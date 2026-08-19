#!/usr/bin/env python3
"""Export a blind philologist-review packet from canonical internal cases.

The canonical case registry stores project positions and rule/phenomenon IDs for
traceability. An independent reviewer should not see those before making the
first classification, so this exporter deliberately strips them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "reviews/philologist-cases.json"


def load_cases() -> dict[str, Any]:
    """Load the canonical internal case registry."""
    value = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("cases"), list):
        raise ValueError("invalid philologist case registry")
    return value


def blind_case(case: dict[str, Any]) -> dict[str, Any]:
    """Return only reviewer-facing fields, stripping project answer hints."""
    return {
        "case_id": case["case_id"],
        "topic": case["topic"],
        "prompt": case["prompt"],
        "review_questions": list(case["review_questions"]),
    }


def blind_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Build the JSON reviewer packet without internal project positions."""
    return {
        "schema_version": payload["schema_version"],
        "purpose": (
            "Independent first-pass review of Russian norm, markedness, native usage, "
            "editing preference and context dependence. Do not judge AI authorship or detector behavior."
        ),
        "classification_options": list(payload["classification_options"]),
        "verdict_options": list(payload["verdict_options"]),
        "cases": [blind_case(case) for case in payload["cases"]],
    }


def markdown(payload: dict[str, Any]) -> str:
    """Render the blind packet in a compact human-readable Markdown form."""
    blind = blind_payload(payload)
    lines = [
        "# Independent philologist review — blind first pass",
        "",
        "Classify the Russian-language phenomenon in each case. Do not assess whether text is AI-generated and do not optimize for detector behavior.",
        "",
        "Primary classes: " + ", ".join(f"`{x}`" for x in blind["classification_options"]) + ".",
        "",
        "Verdicts: " + ", ".join(f"`{x}`" for x in blind["verdict_options"]) + ".",
        "",
        "For every case give a short reason, confidence (`LOW`/`MEDIUM`/`HIGH`), a normative source if you classify it as `LANGUAGE_ERROR`, a preferred variant when useful, and at least one counterexample/boundary when the rule is context-sensitive.",
        "",
    ]
    for case in blind["cases"]:
        lines.extend(
            [
                f"## {case['case_id']} — {case['topic']}",
                "",
                case["prompt"],
                "",
                "Questions:",
            ]
        )
        lines.extend(f"- {question}" for question in case["review_questions"])
        lines.extend(
            [
                "",
                "Decision fields:",
                "- primary_class:",
                "- verdict:",
                "- confidence:",
                "- reason:",
                "- preferred_variant:",
                "- normative_source:",
                "- counterexample:",
                "- notes:",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def self_test() -> None:
    """Ensure blind export cannot leak project positions or internal rule IDs."""
    payload = load_cases()
    blind = blind_payload(payload)
    serialized = json.dumps(blind, ensure_ascii=False)
    forbidden = ["project_position", "rule_ids", "phenomena", "GAL-", "CHUK-", "ILY-"]
    leaked = [marker for marker in forbidden if marker in serialized]
    if leaked:
        raise AssertionError(f"blind packet leaked internal hints: {leaked}")
    if len(blind["cases"]) != 28:
        raise AssertionError(f"expected 28 cases, got {len(blind['cases'])}")
    if [case["case_id"] for case in blind["cases"]] != [f"PHIL-{i:02d}" for i in range(1, 29)]:
        raise AssertionError("blind case order/IDs changed")
    rendered = markdown(payload)
    if "project_position" in rendered or "GAL-" in rendered or "CHUK-" in rendered or "ILY-" in rendered:
        raise AssertionError("Markdown blind packet leaked internal hints")
    print("philologist blind packet export self-test: OK")


def parse_args() -> argparse.Namespace:
    """Parse packet export options."""
    parser = argparse.ArgumentParser(description="Export a blind independent-philologist review packet")
    parser.add_argument("--format", choices=["json", "md"], default="md")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Export the blind packet or run its leakage self-test."""
    args = parse_args()
    if args.self_test:
        self_test()
        return
    payload = load_cases()
    text = (
        json.dumps(blind_payload(payload), ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(payload)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
