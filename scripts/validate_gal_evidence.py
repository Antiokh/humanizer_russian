#!/usr/bin/env python3
"""Validate Nora Gal's modern external-evidence calibration.

This validator is deliberately offline. It checks traceability and evidence
boundaries, not the truth of the linked external sources and not live corpus
measurements.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "studies/nora-gal/external-evidence-2026.json"
DOC_PATH = ROOT / "studies/nora-gal/external-evidence-2026.md"
CLAIMS_PATH = ROOT / "studies/nora-gal/claims.md"
PLAN_PATH = ROOT / "studies/nora-gal/corpus-calibration-plan.md"
MANIFEST_PATH = ROOT / "libraries/gal/library.json"

EXPECTED_IDS = [f"GAL-CLAIM-{i:02d}" for i in range(1, 16)]
UNMEASURED_CORPUS_IDS = {"GAL-CLAIM-01", "GAL-CLAIM-03", "GAL-CLAIM-14"}
ALLOWED_DISPOSITIONS = {
    "SUPPORTED_NARROWLY",
    "REFINED_BY_CURRENT_LINGUISTICS",
    "REFINED_BY_CURRENT_LINGUISTICS+TESTABLE_NOT_YET_MEASURED",
    "REFINED_BY_CURRENT_USAGE/NORM",
    "TESTABLE_NOT_YET_MEASURED",
    "OBSOLETE_AS_ABSOLUTE",
    "NOT_ESTABLISHED_CAUSALLY",
    "SOURCE_METHOD",
    "VALUE_JUDGMENT",
}
PRIMARY_URL_PREFIXES = (
    "https://ruscorpora.ru/",
    "https://ruscorpora.github.io/",
    "https://rusgram.ru/",
    "https://gramota.ru/",
    "https://aclanthology.org/",
    "https://pubmed.ncbi.nlm.nih.gov/",
)


def load_json(path: Path) -> dict:
    """Load a UTF-8 JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object in {path}")
    return value


def validate() -> None:
    """Validate exact claim dispositions and unmeasured corpus boundaries."""
    payload = load_json(DATA_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")
    source_claims = CLAIMS_PATH.read_text(encoding="utf-8")
    plan = PLAN_PATH.read_text(encoding="utf-8")
    manifest = load_json(MANIFEST_PATH)
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(payload.get("schema_version") == 1, "evidence schema_version must be 1")
    check(payload.get("audit_date") == "2026-08-19", "unexpected evidence audit_date")
    rows = payload.get("claims")
    check(isinstance(rows, list), "claims must be an array")
    rows = rows if isinstance(rows, list) else []

    ids = [str(row.get("claim_id", "")) for row in rows if isinstance(row, dict)]
    check(ids == EXPECTED_IDS, f"claim IDs/order mismatch: {ids}")
    check(len(ids) == len(set(ids)), "duplicate claim IDs")

    by_id = {str(row.get("claim_id")): row for row in rows if isinstance(row, dict)}
    for claim_id in EXPECTED_IDS:
        row = by_id.get(claim_id)
        if row is None:
            continue
        disposition = row.get("disposition")
        check(disposition in ALLOWED_DISPOSITIONS, f"{claim_id}: invalid disposition {disposition!r}")
        check(isinstance(row.get("measured_by_project"), bool), f"{claim_id}: measured_by_project must be bool")
        check(bool(str(row.get("runtime_boundary", "")).strip()), f"{claim_id}: missing runtime_boundary")
        urls = row.get("evidence_urls")
        check(isinstance(urls, list), f"{claim_id}: evidence_urls must be an array")
        for url in urls if isinstance(urls, list) else []:
            check(
                isinstance(url, str) and url.startswith(PRIMARY_URL_PREFIXES),
                f"{claim_id}: non-primary/unapproved evidence URL {url!r}",
            )
            check(url in doc, f"{claim_id}: evidence URL missing from narrative audit: {url}")

        check(f"`{claim_id}`" in source_claims, f"{claim_id}: missing from source claims audit")
        check(f"`{claim_id}`" in doc, f"{claim_id}: missing from narrative evidence audit")
        check(str(disposition) in doc, f"{claim_id}: disposition not represented in narrative audit")

    for claim_id in UNMEASURED_CORPUS_IDS:
        row = by_id.get(claim_id, {})
        check(row.get("measured_by_project") is False, f"{claim_id}: must remain explicitly unmeasured")
        check(
            "TESTABLE_NOT_YET_MEASURED" in str(row.get("disposition", "")),
            f"{claim_id}: disposition must retain NOT_YET_MEASURED",
        )
        check(f"`{claim_id}`" in plan, f"{claim_id}: missing from corpus calibration plan")

    # No claim has been measured by this project in this evidence revision.
    measured = [claim_id for claim_id, row in by_id.items() if row.get("measured_by_project") is True]
    check(not measured, f"unexpected measured claims without committed result artifacts: {measured}")

    references = manifest.get("references", [])
    for required in [
        "studies/nora-gal/external-evidence-2026.md",
        "studies/nora-gal/external-evidence-2026.json",
        "studies/nora-gal/corpus-calibration-plan.md",
    ]:
        check(required in references, f"Gal manifest missing evidence reference: {required}")

    # Guard against accidentally replacing the evidence boundary with result language.
    for phrase in [
        "measurement plan, not a result",
        "TESTABLE_NOT_YET_MEASURED",
        "No corpus result for `GAL-CLAIM-01`",
        "No corpus result for `GAL-CLAIM-03`",
        "No “vocabulary decline” result for `GAL-CLAIM-14`",
    ]:
        corpus_text = f"{doc}\n{plan}"
        check(phrase in corpus_text, f"evidence boundary marker missing: {phrase}")

    # The JSON must not silently contain source-claim IDs outside the canonical 15.
    raw_ids = set(re.findall(r"GAL-CLAIM-\d+", DATA_PATH.read_text(encoding="utf-8")))
    check(raw_ids == set(EXPECTED_IDS), f"unexpected claim IDs in evidence JSON: {sorted(raw_ids ^ set(EXPECTED_IDS))}")

    if failures:
        print("Nora Gal external-evidence validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Nora Gal external-evidence validation: OK "
        f"({len(rows)} claims; {len(UNMEASURED_CORPUS_IDS)} corpus claims explicitly unmeasured)"
    )


if __name__ == "__main__":
    validate()
