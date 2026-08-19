#!/usr/bin/env python3
"""Validate libraries, reviewers, styles and optional evidence providers."""
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def validate_dir(pattern,schema_path,skip_prefix="_"):
    schema=load(ROOT/schema_path); Draft202012Validator.check_schema(schema); validator=Draft202012Validator(schema); out=[]
    for path in sorted(ROOT.glob(pattern)):
        if path.name.startswith(skip_prefix) or path.parent.name.startswith(skip_prefix): continue
        data=load(path); validator.validate(data); data["_path"]=path; out.append(data)
    return out
def validate_one(path,schema_path):
    schema=load(ROOT/schema_path); Draft202012Validator.check_schema(schema); data=load(ROOT/path); Draft202012Validator(schema).validate(data); return data
def main():
    libraries=validate_dir("libraries/*/library.json","schemas/library.schema.json"); reviewers=validate_dir("reviewers/*.json","schemas/reviewer.schema.json"); styles=validate_dir("styles/*.json","schemas/style.schema.json"); providers=validate_dir("evidence/*/provider.json","schemas/evidence-provider.schema.json"); validate_one("evidence/_template/provider.json","schemas/evidence-provider.schema.json")
    reviewer_ids={x["id"] for x in reviewers}; library_ids={x["id"] for x in libraries}; provider_ids={x["id"] for x in providers}
    if len(library_ids)!=len(libraries): raise SystemExit("duplicate library id")
    if len(reviewer_ids)!=len(reviewers): raise SystemExit("duplicate reviewer id")
    if len(provider_ids)!=len(providers): raise SystemExit("duplicate evidence provider id")
    for lib in libraries:
        if lib["reviewer_id"] not in reviewer_ids: raise SystemExit(f"{lib['id']}: unknown reviewer {lib['reviewer_id']}")
        if not (ROOT/lib["linter_path"]).is_file(): raise SystemExit(f"{lib['id']}: missing linter {lib['linter_path']}")
        for ref in lib.get("references",[]):
            if not (ROOT/ref).is_file(): raise SystemExit(f"{lib['id']}: missing reference {ref}")
    for provider in providers:
        if provider["network_required"] and provider["enabled_by_default"]: raise SystemExit(f"{provider['id']}: network evidence providers must have enabled_by_default=false")
        if provider["status"]=="OPERATIONAL":
            module=provider.get("module_path")
            if not module or not (ROOT/module).is_file(): raise SystemExit(f"{provider['id']}: missing operational module {module}")
        for ref in provider.get("references",[]):
            if not (ROOT/ref).is_file(): raise SystemExit(f"{provider['id']}: missing reference {ref}")
    if "neutral" not in {x["id"] for x in styles}: raise SystemExit("neutral style is required")
    print(f"libraries: {len(libraries)}; reviewers: {len(reviewers)}; styles: {len(styles)}; evidence providers: {len(providers)}; OK")
if __name__=="__main__": main()
