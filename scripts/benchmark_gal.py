#!/usr/bin/env python3
"""Deterministic regression suite for the mechanical part of the Gal library.

The suite also verifies that the same normalized Gal implementation is consumed
by compact and editorial-board runtimes. It does not run a language model and
must not be described as a model benchmark.
"""

from __future__ import annotations

import json
from pathlib import Path

from check import check_text
from lint_gal import review
from review import run_review

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "gal_cases.json"


def direct_source_failures() -> tuple[list[str], int]:
    """Run Gal source-specific deterministic cases and return failures plus count."""
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in payload["cases"]:
        result = review(case["text"])
        findings = result["findings"]
        ids = [item["rule_id"] for item in findings]
        by_id = {item["rule_id"]: item for item in findings}

        for rule_id in case.get("must_find", []):
            if rule_id not in ids:
                failures.append(f"{case['id']}: missing {rule_id}; got {ids}")
        for rule_id in case.get("must_not_find", []):
            if rule_id in ids:
                failures.append(f"{case['id']}: forbidden {rule_id}; got {ids}")
        if "verdict" in case:
            for rule_id in case.get("must_find", []):
                if rule_id in by_id and by_id[rule_id]["verdict"] != case["verdict"]:
                    failures.append(
                        f"{case['id']}: {rule_id} verdict {by_id[rule_id]['verdict']} "
                        f"!= {case['verdict']}"
                    )
        for key, minimum in case.get("metric_min", {}).items():
            actual = result["metrics"].get(key)
            if actual is None or actual < minimum:
                failures.append(f"{case['id']}: metric {key}={actual} < {minimum}")
        for key, maximum in case.get("metric_max", {}).items():
            actual = result["metrics"].get(key)
            if actual is None or actual > maximum:
                failures.append(f"{case['id']}: metric {key}={actual} > {maximum}")
    return failures, len(payload["cases"])


def runtime_failures() -> list[str]:
    """Validate shared compact/board routing, provenance, negatives, and guardrails."""
    failures: list[str] = []
    shared = "Осуществляется проведение проверки сервиса."

    # Ilyakhov now owns a DEFAULT_MECHANICAL route for this shared phenomenon.
    # Gal and Chukovsky remain EXTENDED_SOFT and therefore must not leak into
    # the default compact row merely because the phenomenon identifier matches.
    default_rows, _ = check_text(shared, extended=False)
    default_overlap = [
        row
        for row in default_rows
        if row.get("phenomenon_id") == "editing.action_hidden_in_nominalization"
    ]
    if len(default_overlap) != 1:
        failures.append(
            f"compact default expected one Ilyakhov shared-phenomenon row: {default_overlap}"
        )
    else:
        row = default_overlap[0]
        # compact_shape exposes canonical source rule_id as the public `rule`
        # field; provenance entries retain their own `rule_id` keys.
        if row.get("rule") != "ILY-M01" or row.get("library_id") != "ilyakhov":
            failures.append(f"compact default shared row is not ILY-M01: {row}")
        default_provenance = row.get("provenance", [])
        if any(item.get("library_id") in {"gal", "chukovsky"} for item in default_provenance):
            failures.append(
                f"EXTENDED_SOFT Gal/Chukovsky provenance leaked into default compact row: {row}"
            )

    extended_rows, _ = check_text(shared, extended=True)
    overlap = [
        row
        for row in extended_rows
        if row.get("phenomenon_id") == "editing.action_hidden_in_nominalization"
    ]
    if len(overlap) != 1:
        failures.append(f"compact shared phenomenon was not deduplicated to one row: {overlap}")
    else:
        row = overlap[0]
        provenance_ids = {
            item.get("rule_id") for item in row.get("provenance", []) if item.get("rule_id")
        }
        required = {"GAL-KANZ-VERB", "CHUK-R17", "ILY-M01"}
        if not required <= provenance_ids:
            failures.append(
                f"compact shared phenomenon lost provenance: required {sorted(required)}, "
                f"got {sorted(provenance_ids)}"
            )
        if row.get("deduplicated_sources") != 3:
            failures.append(
                f"compact shared phenomenon expected 3 sources, got {row.get('deduplicated_sources')}"
            )

    # Board scope is explicit here: this test is about Gal/Chukovsky grouping,
    # not about the separate Ilyakhov majority behavior covered by base tests.
    board = run_review(shared, style_id="neutral", library_ids=["gal", "chukovsky"])
    groups = [
        group
        for group in board["board"]["groups"]
        if group["phenomenon_id"] == "editing.action_hidden_in_nominalization"
    ]
    if len(groups) != 1:
        failures.append(f"board did not group Gal/Chukovsky shared phenomenon: {groups}")
    else:
        group = groups[0]
        if set(group["reviewer_verdicts"]) != {"gal", "chukovsky"}:
            failures.append(f"board lost reviewer provenance: {group['reviewer_verdicts']}")
        if group["status"] != "REVIEW":
            failures.append(
                f"non-directional mechanical findings must remain REVIEW, got {group['status']}"
            )
        rule_ids = {item["rule_id"] for item in group["findings"]}
        if not {"GAL-KANZ-VERB", "CHUK-R17"} <= rule_ids:
            failures.append(f"board lost source rule IDs: {sorted(rule_ids)}")

    negative = run_review(
        "Команда провела проверку сервиса и записала результат.",
        style_id="neutral",
        library_ids=["gal"],
    )
    if negative["findings"]:
        failures.append(f"Gal natural negative produced findings: {negative['findings']}")

    guarded = run_review(
        "Черновик с oaicite внутри.",
        style_id="neutral",
        library_ids=["native", "gal"],
    )
    if not guarded["board"]["guardrails"]:
        failures.append("native ARTIFACT did not remain a board guardrail")
    if any(item.get("reviewer_id") == "gal" for item in guarded["board"]["guardrails"]):
        failures.append("Gal editorial finding incorrectly entered hard guardrails")

    return failures


def main() -> None:
    """Run source and runtime regressions and exit nonzero on any failure."""
    failures, direct_count = direct_source_failures()
    failures.extend(runtime_failures())
    if failures:
        print("GAL BENCHMARK FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(
        f"gal benchmark: {direct_count} source cases OK; compact/board shared-runtime contracts OK"
    )


if __name__ == "__main__":
    main()