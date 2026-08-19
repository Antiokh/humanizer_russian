#!/usr/bin/env python3
"""Load knowledge libraries and normalize their findings for both product modes."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIBRARIES = ROOT / "libraries"
REVIEWERS = ROOT / "reviewers"
STYLES = ROOT / "styles"

DEFAULT_MECHANICAL_RULES = {
    "repeated common element in contrast",
    "parcellated enumeration",
    "ascii hyphen used as dash",
}

PHENOMENON_MAP = {
    "repeated common element in contrast": "native.redundant_shared_material",
    "parcellated enumeration": "native.parcellated_enumeration",
    "ascii hyphen used as dash": "typography.ascii_hyphen_as_dash",
    "possessive overexplication candidate": "native.possessive_overexplication",
    "repeated sentence start": "native.repeated_sentence_start",
    "repeated explicit context candidate": "native.repeated_explicit_context",
    "context undercompression candidate": "native.context_undercompression",
    "repeated contrast formula": "style.repeated_contrast_formula",
    "anglo-rhetorical question/answer cluster": "ai_calque.qa_cluster",
    "short-fragment cluster": "style.short_fragment_cluster",
    "high dash density": "style.high_dash_density",
}


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-zа-яё0-9]+", "_", value, flags=re.I)
    return value.strip("_") or "unknown"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def library_manifests(include_disabled: bool = False) -> list[dict[str, Any]]:
    manifests = []
    for path in sorted(LIBRARIES.glob("*/library.json")):
        if path.parent.name.startswith("_"):
            continue
        manifest = load_json(path)
        manifest["_manifest_path"] = str(path.relative_to(ROOT))
        if include_disabled or manifest.get("enabled_by_default", False):
            manifests.append(manifest)
    return manifests


def reviewer_profiles() -> dict[str, dict[str, Any]]:
    out = {}
    for path in sorted(REVIEWERS.glob("*.json")):
        if path.name.startswith("_"):
            continue
        item = load_json(path)
        out[item["id"]] = item
    return out


def load_style(style_id: str) -> dict[str, Any]:
    path = STYLES / f"{style_id}.json"
    if not path.is_file():
        raise ValueError(f"unknown style: {style_id}")
    return load_json(path)


def import_path(relative: str):
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(f"library linter missing: {relative}")
    name = f"humanizer_library_{slug(relative)}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import library module: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def legacy_project_class(kind: str) -> str:
    return {
        "ARTIFACT": "ARTIFACT",
        "NATIVE_WARNING": "NATIVE_USAGE",
        "STYLE_WARNING": "EDITING",
        "AI_PATTERN": "AI_CALQUE",
    }.get(kind, "EDITING")


def normalize_legacy(finding: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    rule = finding["rule"]
    kind = finding["kind"]
    automation = "HARD_GATE" if kind == "ARTIFACT" else (
        "DEFAULT_MECHANICAL" if rule in DEFAULT_MECHANICAL_RULES else "EXTENDED_SOFT"
    )
    phenomenon = PHENOMENON_MAP.get(rule)
    if not phenomenon and rule.startswith("calque: "):
        phenomenon = f"ai_calque.{slug(rule[8:])}"
    if not phenomenon:
        phenomenon = f"legacy.{slug(rule)}"
    project_class = legacy_project_class(kind)
    reviewer_id = None if project_class == "ARTIFACT" else manifest.get("reviewer_id")
    return {
        "rule_id": f"{manifest['source_namespace']}-{slug(rule)}",
        "phenomenon_id": phenomenon,
        "library_id": manifest["id"],
        "source_namespace": manifest["source_namespace"],
        "reviewer_id": reviewer_id,
        "project_class": project_class,
        "automation_level": automation,
        "verdict": "CHANGE" if automation == "HARD_GATE" else "REVIEW",
        "line": finding.get("line", 0),
        "excerpt": finding.get("excerpt", ""),
        "reason": finding.get("note", ""),
        "operation": None,
        "confidence": None,
    }


def normalize_review_v1(item: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    required = {"rule_id", "phenomenon_id", "project_class", "automation_level", "verdict"}
    missing = sorted(required - set(item))
    if missing:
        raise ValueError(f"{manifest['id']} finding missing fields: {', '.join(missing)}")
    out = dict(item)
    out.setdefault("line", 0)
    out.setdefault("excerpt", "")
    out.setdefault("reason", "")
    out.setdefault("operation", None)
    out.setdefault("confidence", None)
    out["library_id"] = manifest["id"]
    out["source_namespace"] = manifest["source_namespace"]
    out.setdefault("reviewer_id", manifest.get("reviewer_id"))
    return out


def run_library(manifest: dict[str, Any], text: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    module = import_path(manifest["linter_path"])
    adapter = manifest["adapter"]
    if adapter == "legacy_lint_v1":
        findings, metrics = module.lint(text)
        return [normalize_legacy(item, manifest) for item in findings], metrics
    if adapter == "review_v1":
        result = module.review(text)
        return [normalize_review_v1(item, manifest) for item in result.get("findings", [])], result.get("metrics", {})
    raise ValueError(f"unsupported adapter: {adapter}")


def run_libraries(text: str, library_ids: list[str] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifests = library_manifests(include_disabled=bool(library_ids))
    if library_ids:
        wanted = set(library_ids)
        manifests = [m for m in manifests if m["id"] in wanted]
        missing = wanted - {m["id"] for m in manifests}
        if missing:
            raise ValueError(f"unknown libraries: {', '.join(sorted(missing))}")
    findings: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}
    for manifest in manifests:
        lib_findings, lib_metrics = run_library(manifest, text)
        findings.extend(lib_findings)
        metrics[manifest["id"]] = lib_metrics
    return findings, metrics
