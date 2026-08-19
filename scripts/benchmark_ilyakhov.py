#!/usr/bin/env python3
"""Deterministic regression suite for the Ilyakhov/Sarycheva library."""
from __future__ import annotations

import json
from pathlib import Path

from lint_ilyakhov import review

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "tests" / "ilyakhov_cases.json").read_text(encoding="utf-8"))
    failures: list[str] = []

    for case in payload["cases"]:
        result = review(case["text"])
        rows = result["findings"]
        ids = {x["rule_id"] for x in rows}
        by_id = {x["rule_id"]: x for x in rows}

        for rid in case.get("must_find", []):
            if rid not in ids:
                failures.append(f"{case['id']}: missing {rid}; got {sorted(ids)}")
        for rid in case.get("must_not_find", []):
            if rid in ids:
                failures.append(f"{case['id']}: forbidden {rid}; row={by_id[rid]}")
        if case.get("clean") and rows:
            failures.append(f"{case['id']}: expected clean, got {rows}")
        for rid in case.get("expect_review", []):
            row = by_id.get(rid)
            if row is None:
                failures.append(f"{case['id']}: expected REVIEW row {rid} is absent")
            elif row.get("verdict") != "REVIEW" or row.get("automation_level") != "EXTENDED_SOFT":
                failures.append(f"{case['id']}: intentional-use {rid} must stay EXTENDED_SOFT/REVIEW; got {row}")

        metrics = result["metrics"]
        for key, expected in case.get("metric_exact", {}).items():
            if metrics.get(key) != expected:
                failures.append(f"{case['id']}: metric {key}={metrics.get(key)!r} != {expected!r}")
        for key, minimum in case.get("metric_min", {}).items():
            value = metrics.get(key)
            if value is None or value < minimum:
                failures.append(f"{case['id']}: metric {key}={value!r} < {minimum!r}")

        # Mechanical runtime must never emit the 89 MODEL_ONLY source rules.
        leaked = [x for x in rows if x.get("automation_level") == "MODEL_ONLY"]
        if leaked:
            failures.append(f"{case['id']}: MODEL_ONLY leaked into mechanics: {leaked}")

    if failures:
        print("ILYAKHOV BENCHMARK FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(f"Ilyakhov deterministic benchmark: {len(payload['cases'])} cases OK")


if __name__ == "__main__":
    main()
