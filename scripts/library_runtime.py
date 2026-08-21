#!/usr/bin/env python3
"""Load knowledge libraries and normalize their findings for both product modes."""

from __future__ import annotations

import importlib.util
import inspect
import json
import re
from pathlib import Path
from typing import Any

from finding_contract import validate_normalized_finding

ROOT = Path(__file__).resolve().parents[1]
LIBRARIES = ROOT / "libraries"
REVIEWERS = ROOT / "reviewers"
STYLES = ROOT / "styles"

COMPACT_KIND_BY_PROJECT_CLASS = {
    "ARTIFACT": "ARTIFACT",
    "NORM": "LANGUAGE_ERROR",
    "NATIVE_USAGE": "NATIVE_WARNING",
    "EDITING": "STYLE_WARNING",
    "AI_CALQUE": "AI_PATTERN",
    "AUTHOR": "STYLE_WARNING",
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


def normalize_review_v1(item: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    out = dict(item)
    out.setdefault("line", 0)
    out.setdefault("excerpt", "")
    out.setdefault("reason", "")
    out.setdefault("operation", None)
    out.setdefault("confidence", None)
    out["library_id"] = manifest["id"]
    out["source_namespace"] = manifest["source_namespace"]
    out.setdefault("reviewer_id", manifest.get("reviewer_id"))
    validate_normalized_finding(out, manifest["id"])
    return out


def _call_review(module: Any, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
    """Pass optional runtime context only to adapters that declare it."""
    params = inspect.signature(module.review).parameters
    if "context" in params:
        return module.review(text, context=context or {})
    return module.review(text)


def run_library(
    manifest: dict[str, Any],
    text: str,
    context: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    module = import_path(manifest["linter_path"])
    adapter = manifest["adapter"]
    if adapter != "review_v1":
        raise ValueError(f"unsupported adapter: {adapter}; operational libraries must use review_v1")
    result = _call_review(module, text, context)
    return [
        normalize_review_v1(item, manifest)
        for item in result.get("findings", [])
    ], result.get("metrics", {})


def run_libraries(
    text: str,
    library_ids: list[str] | None = None,
    context: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
        lib_findings, lib_metrics = run_library(manifest, text, context=context)
        findings.extend(lib_findings)
        metrics[manifest["id"]] = lib_metrics
    return findings, metrics


def compact_shape(item: dict[str, Any]) -> dict[str, Any]:
    """Stable compact shape compatible with the existing check/benchmark interface."""
    project_class = item.get("project_class")
    display_kind = item.get("display_kind")
    if display_kind:
        kind = display_kind
    else:
        try:
            kind = COMPACT_KIND_BY_PROJECT_CLASS[project_class]
        except KeyError as exc:
            raise ValueError(f"unsupported compact project_class: {project_class!r}") from exc
    return {
        "kind": kind,
        "line": item.get("line", 0),
        "rule": item.get("display_rule") or item["rule_id"],
        "excerpt": item.get("excerpt", ""),
        "note": item.get("reason", ""),
        "library_id": item.get("library_id"),
        "reviewer_id": item.get("reviewer_id"),
        "phenomenon_id": item.get("phenomenon_id"),
        "project_class": project_class,
        "automation_level": item.get("automation_level"),
        "verdict": item.get("verdict"),
    }
