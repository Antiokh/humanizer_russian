#!/usr/bin/env python3
"""Validate philologist review fixtures and completed review files.

The repository keeps an intentionally blank template. A completed review is
validated against JSON Schema plus project-specific semantic constraints, such
as requiring a cited normative source when a case is called LANGUAGE_ERROR.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "reviews/philologist-cases.json"
TEMPLATE_PATH = ROOT / "reviews/philologist-review-template.json"
SCHEMA_PATH = ROOT / "schemas/philologist-review.schema.json"
EXPECTED_IDS = [f"PHIL-{i:02d}" for i in range(1, 29)]


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from a UTF-8 repository/local file."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def schema_validator() -> Draft202012Validator:
    """Compile and return the canonical review schema validator."""
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_repository_contract() -> None:
    """Validate cases, option vocabularies, blank template, and schema alignment."""
    cases = load_json(CASES_PATH)
    template = load_json(TEMPLATE_PATH)
    schema = load_json(SCHEMA_PATH)
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    rows = cases.get("cases")
    check(isinstance(rows, list), "philologist cases must be an array")
    rows = rows if isinstance(rows, list) else []
    ids = [str(row.get("case_id", "")) for row in rows if isinstance(row, dict)]
    check(ids == EXPECTED_IDS, f"case IDs/order mismatch: {ids}")
    check(len(ids) == len(set(ids)), "duplicate philologist case IDs")

    for row in rows:
        case_id = str(row.get("case_id", "<missing>"))
        for field in ["topic", "prompt", "project_position"]:
            check(bool(str(row.get(field, "")).strip()), f"{case_id}: empty {field}")
        questions = row.get("review_questions")
        check(isinstance(questions, list) and bool(questions), f"{case_id}: missing review_questions")
        check(isinstance(row.get("rule_ids"), list), f"{case_id}: rule_ids must be an array")
        check(isinstance(row.get("phenomena"), list) and bool(row.get("phenomena")), f"{case_id}: phenomena must be non-empty")

    primary_enum = schema["properties"]["case_reviews"]["items"]["properties"]["primary_class"]["enum"]
    verdict_enum = schema["properties"]["case_reviews"]["items"]["properties"]["verdict"]["enum"]
    check(cases.get("classification_options") == primary_enum, "classification options drifted from schema")
    check(cases.get("verdict_options") == verdict_enum, "verdict options drifted from schema")

    template_rows = template.get("case_reviews")
    check(isinstance(template_rows, list), "template case_reviews must be an array")
    template_rows = template_rows if isinstance(template_rows, list) else []
    template_ids = [str(row.get("case_id", "")) for row in template_rows if isinstance(row, dict)]
    check(template_ids == EXPECTED_IDS, "template IDs/order drifted from cases")
    check(template.get("reviewer", {}).get("name") == "", "template reviewer name must remain blank")
    for row in template_rows:
        for field in ["primary_class", "verdict", "confidence", "reason"]:
            check(row.get(field) == "", f"template {row.get('case_id')} must leave {field} blank")

    if failures:
        print("Philologist review repository contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"philologist review repository contract: OK ({len(rows)} blind-review cases)")


def validate_completed_review(review: dict[str, Any]) -> None:
    """Validate one completed expert review structurally and semantically."""
    validator = schema_validator()
    errors = sorted(validator.iter_errors(review), key=lambda error: list(error.path))
    failures = [error.message for error in errors]

    rows = review.get("case_reviews") if isinstance(review, dict) else None
    rows = rows if isinstance(rows, list) else []
    ids = [str(row.get("case_id", "")) for row in rows if isinstance(row, dict)]
    if ids != EXPECTED_IDS:
        failures.append(f"completed review must contain PHIL-01..PHIL-28 exactly once in order; got {ids}")

    for row in rows:
        if not isinstance(row, dict):
            continue
        case_id = str(row.get("case_id", "<missing>"))
        primary = row.get("primary_class")
        verdict = row.get("verdict")
        source = str(row.get("normative_source", "")).strip()
        counterexample = str(row.get("counterexample", "")).strip()
        if primary == "LANGUAGE_ERROR" and not source:
            failures.append(f"{case_id}: LANGUAGE_ERROR requires a normative_source")
        if primary == "NEEDS_NORM_SOURCE" and verdict != "NEEDS_VERIFICATION":
            failures.append(f"{case_id}: NEEDS_NORM_SOURCE should use NEEDS_VERIFICATION verdict")
        if primary == "NEEDS_CORPUS" and verdict not in {"REVIEW", "NEEDS_VERIFICATION"}:
            failures.append(f"{case_id}: NEEDS_CORPUS cannot be an unconditional KEEP/CHANGE verdict")
        if primary in {
            "MARKED_BUT_ACCEPTABLE",
            "NATIVE_PREFERENCE",
            "EDITING_PREFERENCE",
            "AUTHOR_DEPENDENT",
            "NEEDS_CONTEXT",
        } and not counterexample:
            failures.append(f"{case_id}: context-sensitive classification requires a counterexample/boundary")

    if failures:
        print("Completed philologist review FAILED validation")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"completed philologist review: OK ({len(rows)} cases)")


def synthetic_review() -> dict[str, Any]:
    """Create a valid artificial review only for offline validator self-testing."""
    rows = []
    for case_id in EXPECTED_IDS:
        rows.append(
            {
                "case_id": case_id,
                "primary_class": "NORMATIVE_VARIANT",
                "verdict": "KEEP",
                "confidence": "MEDIUM",
                "reason": "synthetic validator fixture",
                "preferred_variant": "",
                "normative_source": "",
                "counterexample": "context can change markedness",
                "notes": "synthetic only; not expert evidence"
            }
        )
    return {
        "schema_version": 1,
        "reviewer": {
            "name": "Synthetic Validator Fixture",
            "qualification": "not a real reviewer",
            "affiliation_or_independent": "test fixture",
            "conflict_of_interest": "synthetic"
        },
        "review_date": "2026-08-19",
        "case_reviews": rows,
        "overall_notes": "Synthetic object used only to test schema plumbing."
    }


def self_test() -> None:
    """Run repository-contract and completed-review validation without expert evidence."""
    validate_repository_contract()
    review = synthetic_review()
    validate_completed_review(review)

    broken = json.loads(json.dumps(review, ensure_ascii=False))
    broken["case_reviews"][0]["primary_class"] = "LANGUAGE_ERROR"
    broken["case_reviews"][0]["normative_source"] = ""
    try:
        validate_completed_review(broken)
    except SystemExit:
        pass
    else:
        raise AssertionError("LANGUAGE_ERROR without normative source was accepted")
    print("philologist review validator self-test: OK")


def parse_args() -> argparse.Namespace:
    """Parse validation mode and optional completed-review path."""
    parser = argparse.ArgumentParser(description="Validate humanizer_russian philologist review data")
    parser.add_argument("review", nargs="?", type=Path, help="completed review JSON to validate")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Validate repository fixtures, self-test, or one completed expert review."""
    args = parse_args()
    if args.self_test:
        self_test()
        return
    validate_repository_contract()
    if args.review is not None:
        validate_completed_review(load_json(args.review))


if __name__ == "__main__":
    main()
