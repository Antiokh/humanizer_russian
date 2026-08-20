#!/usr/bin/env python3
"""Validate the machine-readable Ilyakhov/Sarycheva external-evidence layer.

The validator proves coverage and provenance contracts only. It does not decide
whether an empirical paper is methodologically strong enough for a new runtime
rule and never promotes book authority into current NORM/HARD_GATE.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "pishi-sokrashchay"
DATA_PATH = STUDY / "external-evidence-2026.json"
NARRATIVE_PATH = STUDY / "external-claims-evidence.md"
SOURCE_CLAIMS_PATH = STUDY / "counterexamples-claims.md"
CORPUS_PATH = STUDY / "corpus-calibration.md"
MANIFEST_PATH = ROOT / "libraries" / "ilyakhov" / "library.json"

SOURCE_CLAIMS_REL = "studies/pishi-sokrashchay/counterexamples-claims.md"
NARRATIVE_REL = "studies/pishi-sokrashchay/external-claims-evidence.md"
CORPUS_REL = "studies/pishi-sokrashchay/corpus-calibration.md"

EXPECTED_CLAIMS = [f"PS-CL{i:02d}" for i in range(1, 33)]
EXPECTED_SOURCES = [f"ILY-EXT-{i:02d}" for i in range(1, 26)]
ALLOWED_DISPOSITIONS = {
    "SUPPORTED_BOUNDED",
    "PARTIAL_CONDITIONAL",
    "CONTESTED",
    "UNVERIFIED",
    "COUNTEREVIDENCE",
    "MODEL_OR_VALUE",
    "SOURCE_INTERNAL",
    "TOOL_SPECIFIC_STALE",
}
EVIDENCE_BEARING = {
    "SUPPORTED_BOUNDED",
    "PARTIAL_CONDITIONAL",
    "CONTESTED",
    "COUNTEREVIDENCE",
}
TRUSTED_PREFIXES = ("https://doi.org/", "https://pubmed.ncbi.nlm.nih.gov/")
STABLE_ID_RE = re.compile(r"^(?:DOI:10\.\d{4,9}/\S+|PMID:\d+)$")
NARRATIVE_ROW_RE = re.compile(
    r"^\|\s*(PS-CL\d{2})\s*\|\s*([A-Z_]+)\s*\|",
    re.M,
)


def load_json(path: Path) -> dict:
    """Load a UTF-8 JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def validate() -> None:
    """Validate evidence coverage, declared artifact paths and runtime boundaries."""
    data = load_json(DATA_PATH)
    manifest = load_json(MANIFEST_PATH)
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    # The registry declares which public artifacts its evidence contract refers to.
    # Validate those declarations before reading the fixed trusted repository paths,
    # so a typo or silent redirect cannot pass while the validator reads another file.
    declared_paths = {
        "source_claim_document": SOURCE_CLAIMS_REL,
        "narrative_evidence_document": NARRATIVE_REL,
        "corpus_calibration_document": CORPUS_REL,
    }
    for field, expected in declared_paths.items():
        check(data.get(field) == expected, f"{field} must equal {expected!r}")

    narrative = NARRATIVE_PATH.read_text(encoding="utf-8")
    source_claims = SOURCE_CLAIMS_PATH.read_text(encoding="utf-8")
    corpus = CORPUS_PATH.read_text(encoding="utf-8")

    check(data.get("schema_version") == 1, "schema_version must be 1")
    check(data.get("audit_date") == "2026-08-20", "unexpected audit_date")
    policy = str(data.get("policy", ""))
    check("never promotes" in policy.lower(), "policy must preserve no-promotion boundary")

    bibliography = data.get("bibliography")
    check(isinstance(bibliography, list), "bibliography must be an array")
    bibliography = bibliography if isinstance(bibliography, list) else []
    source_ids = [str(item.get("source_id", "")) for item in bibliography if isinstance(item, dict)]
    check(source_ids == EXPECTED_SOURCES, f"source IDs/order mismatch: {source_ids}")
    check(len(source_ids) == len(set(source_ids)), "duplicate source IDs")
    known_sources = set(source_ids)

    for row in bibliography:
        if not isinstance(row, dict):
            failures.append("bibliography row must be object")
            continue
        source_id = str(row.get("source_id", ""))
        for field in ("kind", "title", "responsible", "url", "stable_id"):
            check(bool(str(row.get(field, "")).strip()), f"{source_id}: missing {field}")
        url = row.get("url")
        check(
            isinstance(url, str) and url.startswith(TRUSTED_PREFIXES),
            f"{source_id}: unapproved evidence URL {url!r}",
        )
        stable_id = str(row.get("stable_id", ""))
        check(
            bool(STABLE_ID_RE.fullmatch(stable_id)),
            f"{source_id}: stable_id must be exactly one canonical DOI or PMID",
        )

    claims = data.get("claims")
    check(isinstance(claims, list), "claims must be an array")
    claims = claims if isinstance(claims, list) else []
    claim_ids = [str(item.get("claim_id", "")) for item in claims if isinstance(item, dict)]
    check(claim_ids == EXPECTED_CLAIMS, f"claim IDs/order mismatch: {claim_ids}")
    check(len(claim_ids) == len(set(claim_ids)), "duplicate claim IDs")

    narrative_status = dict(NARRATIVE_ROW_RE.findall(narrative))
    check(set(narrative_status) == set(EXPECTED_CLAIMS), "narrative audit must cover PS-CL01..PS-CL32 exactly")

    for row in claims:
        if not isinstance(row, dict):
            failures.append("claim row must be object")
            continue
        claim_id = str(row.get("claim_id", ""))
        disposition = str(row.get("disposition", ""))
        check(disposition in ALLOWED_DISPOSITIONS, f"{claim_id}: invalid disposition {disposition!r}")
        check(narrative_status.get(claim_id) == disposition, f"{claim_id}: JSON/narrative disposition drift")
        refs = row.get("source_ids")
        check(isinstance(refs, list), f"{claim_id}: source_ids must be an array")
        refs = refs if isinstance(refs, list) else []
        if disposition in EVIDENCE_BEARING:
            check(bool(refs), f"{claim_id}: {disposition} requires at least one source_id")
        for source_id in refs:
            check(source_id in known_sources, f"{claim_id}: unknown source_id {source_id}")
        check(bool(str(row.get("runtime_boundary", "")).strip()), f"{claim_id}: missing runtime_boundary")
        check(
            row.get("may_promote_norm_or_hard_gate") is False,
            f"{claim_id}: external evidence must not authorize NORM/HARD_GATE promotion",
        )
        check(f"**{claim_id}**" in source_claims, f"{claim_id}: missing from primary source claims audit")

    calibration = data.get("corpus_calibration")
    check(isinstance(calibration, dict), "corpus_calibration must be an object")
    calibration = calibration if isinstance(calibration, dict) else {}
    check(calibration.get("articles") == 30, "corpus calibration article count drifted")
    check(calibration.get("words") == 218167, "corpus calibration word count drifted")
    check(
        "PS-R21 present-time wrapper demoted" in str(calibration.get("key_disposition", "")),
        "corpus calibration must retain PS-R21 demotion",
    )
    check(
        "No additional source rule promoted" in str(calibration.get("promotion_result", "")),
        "corpus calibration must retain no-promotion result",
    )
    check("218,167 words" in corpus, "corpus-calibration.md snapshot drifted")
    check("METRIC_ONLY" in corpus and "PS-R21" in corpus, "corpus calibration lost PS-R21 METRIC_ONLY boundary")

    references = manifest.get("references", [])
    for required in (NARRATIVE_REL, "studies/pishi-sokrashchay/external-evidence-2026.json", CORPUS_REL):
        check(required in references, f"Ilyakhov manifest missing evidence reference: {required}")

    if failures:
        print("Ilyakhov external-evidence validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Ilyakhov external-evidence validation: OK "
        f"({len(bibliography)} sources; {len(claims)} claim dispositions; "
        f"{calibration.get('words', 0)} calibration words)"
    )


if __name__ == "__main__":
    validate()
