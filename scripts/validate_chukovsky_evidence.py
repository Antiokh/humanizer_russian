#!/usr/bin/env python3
"""Validate Chukovsky external-evidence provenance and claim dispositions.

This validator is deliberately offline. It checks reproducibility metadata,
coverage, cross-document registration and evidence boundaries. It does not
re-fetch external sources or convert editorial authority into current NORM.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "studies/chukovsky-zhivoy-kak-zhizn/external-evidence-2026.json"
CLAIMS_PATH = ROOT / "studies/chukovsky-zhivoy-kak-zhizn/claims-external.md"
GAP_PATH = ROOT / "studies/chukovsky-zhivoy-kak-zhizn/external-provenance-gap.md"
MANIFEST_PATH = ROOT / "libraries/chukovsky/library.json"

EXPECTED_SOURCE_IDS = [f"EXT-{i:02d}" for i in range(1, 15)]
EXPECTED_CLAIM_IDS = [f"CLM-{i:02d}" for i in range(1, 31)]
ALLOWED_DISPOSITIONS = {
    "EXTERNAL_CONFIRMED",
    "EXTERNAL_PARTIAL",
    "EXTERNAL_CONTESTED",
    "EXTERNAL_UNRESOLVED",
    "VALUE_ONLY",
    "HISTORICAL_ONLY",
    "CURRENT_SAMPLE_VERIFIED",
}
TRUSTED_PREFIXES = (
    "https://gramota.ru/",
    "https://rusgram.ru/",
    "https://iling-ran.ru/",
    "https://doi.org/",
    "https://pmc.ncbi.nlm.nih.gov/",
)


def load_json(path: Path) -> dict:
    """Load a UTF-8 JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def validate() -> None:
    """Validate exact source/claim coverage and no-promotion evidence boundaries."""
    payload = load_json(DATA_PATH)
    claims_doc = CLAIMS_PATH.read_text(encoding="utf-8")
    gap_doc = GAP_PATH.read_text(encoding="utf-8")
    manifest = load_json(MANIFEST_PATH)
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(payload.get("schema_version") == 1, "schema_version must be 1")
    check(payload.get("audit_date") == "2026-08-20", "unexpected audit_date")

    sources = payload.get("sources")
    check(isinstance(sources, list), "sources must be an array")
    sources = sources if isinstance(sources, list) else []
    source_ids = [str(row.get("source_id", "")) for row in sources if isinstance(row, dict)]
    check(source_ids == EXPECTED_SOURCE_IDS, f"source IDs/order mismatch: {source_ids}")
    check(len(source_ids) == len(set(source_ids)), "duplicate source IDs")
    known_sources = set(source_ids)

    for row in sources:
        if not isinstance(row, dict):
            failures.append("source row must be object")
            continue
        source_id = str(row.get("source_id", ""))
        for field in ("kind", "title", "responsible", "url", "locator", "accessed_on"):
            check(bool(str(row.get(field, "")).strip()), f"{source_id}: missing {field}")
        url = row.get("url")
        check(
            isinstance(url, str) and url.startswith(TRUSTED_PREFIXES),
            f"{source_id}: unapproved primary URL {url!r}",
        )
        secondary = row.get("secondary_url")
        if secondary is not None:
            check(
                isinstance(secondary, str) and secondary.startswith(TRUSTED_PREFIXES),
                f"{source_id}: unapproved secondary URL {secondary!r}",
            )
        check(
            bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(row.get("accessed_on", "")))),
            f"{source_id}: accessed_on must be YYYY-MM-DD",
        )

    for source_id in ("EXT-01", "EXT-02", "EXT-03"):
        row = next((item for item in sources if item.get("source_id") == source_id), {})
        check(bool(str(row.get("dictionary_layer", "")).strip()), f"{source_id}: missing dictionary_layer")

    for source_id in ("EXT-08", "EXT-12", "EXT-13"):
        row = next((item for item in sources if item.get("source_id") == source_id), {})
        stable_id = str(row.get("stable_id", ""))
        check("DOI:" in stable_id, f"{source_id}: DOI required in stable_id")
    for source_id in ("EXT-12", "EXT-13"):
        row = next((item for item in sources if item.get("source_id") == source_id), {})
        stable_id = str(row.get("stable_id", ""))
        check("PMCID:" in stable_id, f"{source_id}: PMCID required in stable_id")

    claims = payload.get("claims")
    check(isinstance(claims, list), "claims must be an array")
    claims = claims if isinstance(claims, list) else []
    claim_ids = [str(row.get("claim_id", "")) for row in claims if isinstance(row, dict)]
    check(claim_ids == EXPECTED_CLAIM_IDS, f"claim IDs/order mismatch: {claim_ids}")
    check(len(claim_ids) == len(set(claim_ids)), "duplicate claim IDs")

    for row in claims:
        if not isinstance(row, dict):
            failures.append("claim row must be object")
            continue
        claim_id = str(row.get("claim_id", ""))
        disposition = row.get("disposition")
        check(disposition in ALLOWED_DISPOSITIONS, f"{claim_id}: invalid disposition {disposition!r}")
        source_refs = row.get("source_ids")
        check(isinstance(source_refs, list), f"{claim_id}: source_ids must be an array")
        for source_id in source_refs if isinstance(source_refs, list) else []:
            check(source_id in known_sources, f"{claim_id}: unknown source_id {source_id}")
        check(bool(str(row.get("runtime_boundary", "")).strip()), f"{claim_id}: missing runtime_boundary")
        check(
            row.get("may_promote_norm_or_hard_gate") is False,
            f"{claim_id}: external audit must not authorize NORM/HARD_GATE promotion",
        )
        check(f"{claim_id} " in claims_doc, f"{claim_id}: missing from narrative claims audit")

    references = manifest.get("references", [])
    for required in (
        "studies/chukovsky-zhivoy-kak-zhizn/claims-external.md",
        "studies/chukovsky-zhivoy-kak-zhizn/external-evidence-2026.json",
        "studies/chukovsky-zhivoy-kak-zhizn/external-provenance-gap.md",
    ):
        check(required in references, f"Chukovsky manifest missing evidence reference: {required}")

    check("Status: `CLOSED`" in gap_doc, "external provenance gap must be marked CLOSED")
    check(
        "does not promote" in gap_doc.lower(),
        "gap closure must preserve explicit no-promotion boundary",
    )

    raw_source_ids = set(re.findall(r"EXT-\d{2}", DATA_PATH.read_text(encoding="utf-8")))
    check(raw_source_ids == set(EXPECTED_SOURCE_IDS), "unexpected/missing EXT IDs in evidence JSON")
    raw_claim_ids = set(re.findall(r"CLM-\d{2}", DATA_PATH.read_text(encoding="utf-8")))
    check(raw_claim_ids == set(EXPECTED_CLAIM_IDS), "unexpected/missing CLM IDs in evidence JSON")

    if failures:
        print("Chukovsky external-evidence validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Chukovsky external-evidence validation: OK "
        f"({len(sources)} sources; {len(claims)} claim dispositions)"
    )


if __name__ == "__main__":
    validate()
