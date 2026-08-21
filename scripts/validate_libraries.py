#!/usr/bin/env python3
"""Validate libraries, reviewers, styles and optional evidence providers."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MODEL_EVAL_LIBRARIES = {
    "gal",
    "chukovsky",
    "ilyakhov",
    "golub",
    "visson",
    "rosenthal",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_dir(pattern: str, schema_path: str, skip_prefix: str = "_") -> list[dict]:
    schema = load(ROOT / schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    out: list[dict] = []
    for path in sorted(ROOT.glob(pattern)):
        if path.name.startswith(skip_prefix) or path.parent.name.startswith(skip_prefix):
            continue
        data = load(path)
        validator.validate(data)
        data["_path"] = path
        out.append(data)
    return out


def validate_one(path: str, schema_path: str) -> dict:
    schema = load(ROOT / schema_path)
    Draft202012Validator.check_schema(schema)
    data = load(ROOT / path)
    Draft202012Validator(schema).validate(data)
    return data


def _validate_model_eval_contract(lib: dict) -> bool:
    suite = lib.get("model_eval_path")
    mapping = lib.get("model_eval_map_path")
    if bool(suite) != bool(mapping):
        raise SystemExit(
            f"{lib['id']}: model eval registration must declare both model_eval_path and model_eval_map_path"
        )
    if not suite:
        return False
    for field, value in (("model_eval_path", suite), ("model_eval_map_path", mapping)):
        if not isinstance(value, str) or not (ROOT / value).is_file():
            raise SystemExit(f"{lib['id']}: missing {field} {value!r}")
    if not lib.get("rules_path"):
        raise SystemExit(f"{lib['id']}: model eval registration requires rules_path")
    return True


def main() -> None:
    libraries = validate_dir("libraries/*/library.json", "schemas/library.schema.json")
    reviewers = validate_dir("reviewers/*.json", "schemas/reviewer.schema.json")
    styles = validate_dir("styles/*.json", "schemas/style.schema.json")
    providers = validate_dir("evidence/*/provider.json", "schemas/evidence-provider.schema.json")
    validate_one("evidence/_template/provider.json", "schemas/evidence-provider.schema.json")

    reviewer_ids = {x["id"] for x in reviewers}
    library_ids = {x["id"] for x in libraries}
    provider_ids = {x["id"] for x in providers}
    if len(library_ids) != len(libraries):
        raise SystemExit("duplicate library id")
    if len(reviewer_ids) != len(reviewers):
        raise SystemExit("duplicate reviewer id")
    if len(provider_ids) != len(providers):
        raise SystemExit("duplicate evidence provider id")

    registered_model_eval: set[str] = set()
    for lib in libraries:
        if lib["reviewer_id"] not in reviewer_ids:
            raise SystemExit(f"{lib['id']}: unknown reviewer {lib['reviewer_id']}")
        if not (ROOT / lib["linter_path"]).is_file():
            raise SystemExit(f"{lib['id']}: missing linter {lib['linter_path']}")
        for ref in lib.get("references", []):
            if not (ROOT / ref).is_file():
                raise SystemExit(f"{lib['id']}: missing reference {ref}")
        if _validate_model_eval_contract(lib):
            registered_model_eval.add(lib["id"])

    missing_model_eval = REQUIRED_MODEL_EVAL_LIBRARIES - registered_model_eval
    if missing_model_eval:
        raise SystemExit(
            "missing required model-eval registrations: "
            + ", ".join(sorted(missing_model_eval))
        )

    for provider in providers:
        if provider["network_required"] and provider["enabled_by_default"]:
            raise SystemExit(
                f"{provider['id']}: network evidence providers must have enabled_by_default=false"
            )
        if provider["status"] == "OPERATIONAL":
            module = provider.get("module_path")
            if not module or not (ROOT / module).is_file():
                raise SystemExit(f"{provider['id']}: missing operational module {module}")
        for ref in provider.get("references", []):
            if not (ROOT / ref).is_file():
                raise SystemExit(f"{provider['id']}: missing reference {ref}")

    if "neutral" not in {x["id"] for x in styles}:
        raise SystemExit("neutral style is required")
    print(
        f"libraries: {len(libraries)}; reviewers: {len(reviewers)}; styles: {len(styles)}; "
        f"evidence providers: {len(providers)}; model-eval libraries: {len(registered_model_eval)}; OK"
    )


if __name__ == "__main__":
    main()
