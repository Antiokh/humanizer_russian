#!/usr/bin/env python3
"""Validate pluggable library/reviewer/style manifests and their referenced files."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_dir(pattern: str, schema_path: str, skip_prefix: str = "_") -> list[dict]:
    schema = load(ROOT / schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    out = []
    for path in sorted(ROOT.glob(pattern)):
        if path.name.startswith(skip_prefix) or path.parent.name.startswith(skip_prefix):
            continue
        data = load(path)
        validator.validate(data)
        data["_path"] = path
        out.append(data)
    return out


def main() -> None:
    libraries = validate_dir("libraries/*/library.json", "schemas/library.schema.json")
    reviewers = validate_dir("reviewers/*.json", "schemas/reviewer.schema.json")
    styles = validate_dir("styles/*.json", "schemas/style.schema.json")

    reviewer_ids = {x["id"] for x in reviewers}
    library_ids = {x["id"] for x in libraries}
    if len(library_ids) != len(libraries):
        raise SystemExit("duplicate library id")
    if len(reviewer_ids) != len(reviewers):
        raise SystemExit("duplicate reviewer id")

    for lib in libraries:
        if lib["reviewer_id"] not in reviewer_ids:
            raise SystemExit(f"{lib['id']}: unknown reviewer {lib['reviewer_id']}")
        if not (ROOT / lib["linter_path"]).is_file():
            raise SystemExit(f"{lib['id']}: missing linter {lib['linter_path']}")
        for reference in lib.get("references", []):
            if not (ROOT / reference).is_file():
                raise SystemExit(f"{lib['id']}: missing reference {reference}")

    style_ids = {x["id"] for x in styles}
    if "neutral" not in style_ids:
        raise SystemExit("neutral style is required")

    print(f"libraries: {len(libraries)}; reviewers: {len(reviewers)}; styles: {len(styles)}; OK")


if __name__ == "__main__":
    main()
