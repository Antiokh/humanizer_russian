#!/usr/bin/env python3
"""Deterministic regression suite for the mechanical part of the Gal library."""

from __future__ import annotations

import json
from pathlib import Path

from lint_gal import review

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "gal_cases.json"


def main() -> None:
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
                        f"{case['id']}: {rule_id} verdict {by_id[rule_id]['verdict']} != {case['verdict']}"
                    )
        for key, minimum in case.get("metric_min", {}).items():
            actual = result["metrics"].get(key)
            if actual is None or actual < minimum:
                failures.append(f"{case['id']}: metric {key}={actual} < {minimum}")
        for key, maximum in case.get("metric_max", {}).items():
            actual = result["metrics"].get(key)
            if actual is None or actual > maximum:
                failures.append(f"{case['id']}: metric {key}={actual} > {maximum}")

    if failures:
        print("GAL BENCHMARK FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"gal benchmark: {len(payload['cases'])} cases OK")


if __name__ == "__main__":
    main()
