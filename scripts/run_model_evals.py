#!/usr/bin/env python3
"""Run contextual humanizer_russian evals through the OpenAI Responses API.

The harness is manifest-driven: each participating knowledge library declares
its runtime eval suite, traceability map and rules path in
``libraries/<id>/library.json``. Candidate models receive only the user prompt
and mapped rule cards; expected answers and counterexample labels are reserved
for the independent judge call.

Live calls are opt-in and never run in CI. Authentication comes only from
``OPENAI_API_KEY`` and is never written to reports. ``store`` is always false.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import json
import os
from pathlib import Path
import time
from typing import Any
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LIBRARIES_ROOT = ROOT / "libraries"
DEFAULT_LIBRARY = "gal"
DEFAULT_ENDPOINT = "https://api.openai.com/v1/responses"
RETRYABLE_HTTP = {408, 409, 429, 500, 502, 503, 504}

JUDGMENT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "overall",
        "expectations",
        "semantic_violation",
        "norm_violation",
        "notes",
    ],
    "properties": {
        "overall": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
        "expectations": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["expectation", "verdict", "reason"],
                "properties": {
                    "expectation": {"type": "string"},
                    "verdict": {
                        "type": "string",
                        "enum": ["PASS", "FAIL", "UNCERTAIN"],
                    },
                    "reason": {"type": "string"},
                },
            },
        },
        "semantic_violation": {"type": "boolean"},
        "norm_violation": {"type": "boolean"},
        "notes": {"type": "string"},
    },
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object from disk."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def repo_path(relative: str, *, label: str, must_exist: bool = True) -> Path:
    """Resolve a repository-relative manifest path without allowing traversal."""
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError(f"{label} must be a non-empty repository-relative path")
    rel = Path(relative)
    if rel.is_absolute():
        raise ValueError(f"{label} must be repository-relative: {relative!r}")
    root = ROOT.resolve()
    resolved = (ROOT / rel).resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"{label} escapes repository root: {relative!r}")
    if must_exist and not resolved.is_file():
        raise ValueError(f"{label} does not exist: {relative!r}")
    return resolved


def relative_display(path: Path) -> str:
    """Return a stable repository-relative path when possible."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def discover_model_eval_libraries() -> list[str]:
    """Return library IDs with a complete manifest-declared model-eval contract."""
    found: list[str] = []
    for manifest_path in sorted(LIBRARIES_ROOT.glob("*/library.json")):
        manifest = load_json(manifest_path)
        library_id = manifest.get("id")
        if manifest.get("model_eval_path") and manifest.get("model_eval_map_path"):
            if not isinstance(library_id, str) or library_id != manifest_path.parent.name:
                raise ValueError(f"manifest id/path mismatch: {manifest_path}")
            if library_id in found:
                raise ValueError(f"duplicate library id: {library_id!r}")
            found.append(library_id)
    return found

def load_library_config(
    library_id: str,
    *,
    suite_override: Path | None = None,
    map_override: Path | None = None,
) -> dict[str, Any]:
    """Load one library manifest and resolve its eval/rule resources."""
    manifest_path = LIBRARIES_ROOT / library_id / "library.json"
    if not manifest_path.is_file():
        raise ValueError(f"unknown library {library_id!r}: {manifest_path} not found")
    manifest = load_json(manifest_path)
    if manifest.get("id") != library_id:
        raise ValueError(f"library manifest id mismatch: requested={library_id!r}, got={manifest.get('id')!r}")

    rules_path = repo_path(str(manifest.get("rules_path", "")), label="rules_path")
    if suite_override is None:
        suite_path = repo_path(str(manifest.get("model_eval_path", "")), label="model_eval_path")
    else:
        suite_path = suite_override.expanduser().resolve()
        if not suite_path.is_file():
            raise ValueError(f"suite override does not exist: {suite_path}")
    if map_override is None:
        map_path = repo_path(str(manifest.get("model_eval_map_path", "")), label="model_eval_map_path")
    else:
        map_path = map_override.expanduser().resolve()
        if not map_path.is_file():
            raise ValueError(f"map override does not exist: {map_path}")

    return {
        "id": library_id,
        "display_name": str(manifest.get("display_name") or library_id),
        "source_namespace": str(manifest.get("source_namespace") or library_id.upper()),
        "manifest_path": manifest_path,
        "manifest": manifest,
        "rules_path": rules_path,
        "suite_path": suite_path,
        "map_path": map_path,
    }


def parse_markdown_matrix(path: Path) -> dict[str, dict[str, str]]:
    """Parse the first Markdown integration table keyed by its Rule column."""
    text = path.read_text(encoding="utf-8")
    headers: list[str] | None = None
    rows: dict[str, dict[str, str]] = {}
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not in_table:
            if line.startswith("| Rule |"):
                headers = [cell.strip() for cell in line.strip("|").split("|")]
                in_table = True
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if headers is None or len(cells) != len(headers):
            if rows:
                break
            continue
        rule_key = cells[0].strip("`")
        if not rule_key or rule_key == "Rule":
            continue
        if rule_key in rows:
            raise ValueError(f"duplicate integration-matrix rule {rule_key!r} in {path}")
        rows[rule_key] = dict(zip(headers, cells))
    return rows


def matrix_row_for_rule(
    rule: dict[str, Any],
    matrix: dict[str, dict[str, str]],
) -> dict[str, str]:
    """Join runtime rules to source-study matrix rows without relying on one namespace."""
    candidates: list[str] = []
    for raw in (rule.get("study_rule_id"), rule.get("rule_id")):
        if not raw:
            continue
        value = str(raw)
        candidates.append(value)
        if "-" in value:
            candidates.append(value.split("-", 1)[1])
    for candidate in candidates:
        if candidate in matrix:
            return matrix[candidate]
    return {}


def load_rules(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Load flat or grouped canonical rules and enrich sparse rules from their matrix."""
    index = load_json(config["rules_path"])
    raw_rules: list[dict[str, Any]] = []

    direct = index.get("rules")
    if isinstance(direct, list):
        raw_rules.extend(item for item in direct if isinstance(item, dict))
    groups = index.get("groups")
    if isinstance(groups, list):
        for relative in groups:
            group_path = repo_path(str(relative), label="rule group path")
            payload = load_json(group_path)
            group_rules = payload.get("rules")
            if not isinstance(group_rules, list):
                raise ValueError(f"rule group has no rules array: {group_path}")
            raw_rules.extend(item for item in group_rules if isinstance(item, dict))

    project_derived = index.get("project_derived_rules")
    if isinstance(project_derived, list):
        raw_rules.extend(item for item in project_derived if isinstance(item, dict))
    if not raw_rules:
        raise ValueError(f"no rules found in {config['rules_path']}")

    matrix: dict[str, dict[str, str]] = {}
    detail_sources = index.get("detail_sources")
    if isinstance(detail_sources, dict) and detail_sources.get("integration_matrix"):
        matrix_path = repo_path(str(detail_sources["integration_matrix"]), label="integration_matrix")
        matrix = parse_markdown_matrix(matrix_path)

    rules: dict[str, dict[str, Any]] = {}
    for original in raw_rules:
        rule = dict(original)
        rule_id = str(rule.get("rule_id", ""))
        if not rule_id:
            raise ValueError(f"rule without rule_id in {config['rules_path']}")
        if rule_id in rules:
            raise ValueError(f"duplicate rule_id {rule_id!r} in library {config['id']}")
        matrix_row = matrix_row_for_rule(rule, matrix)
        if matrix_row:
            rule["_integration_matrix"] = matrix_row
        rules[rule_id] = rule
    return rules


def matrix_value(row: dict[str, str], *needles: str) -> str:
    """Find a matrix cell by tolerant header fragments."""
    lowered = [(key.lower(), value) for key, value in row.items()]
    for needle in needles:
        target = needle.lower()
        for key, value in lowered:
            if target == key or target in key:
                return value
    return ""


def compact_rule_card(rule: dict[str, Any]) -> str:
    """Render source-derived guidance without any eval expectation text."""
    rows = [f"[{rule['rule_id']}] {rule.get('phenomenon_id', '')}".rstrip()]
    for label, key in (
        ("project class", "project_class"),
        ("automation", "automation_level"),
        ("operation", "operation"),
        ("semantic invariant", "semantic_invariant"),
        ("required context", "required_context"),
        ("native/author guard", "conflict_with_native_usage"),
        ("positive case", "positive_case"),
        ("natural negative", "natural_negative"),
        ("boundary", "boundary_case"),
        ("intentional counterexample", "intentional_counterexample"),
        ("source locator", "source_locator"),
    ):
        value = rule.get(key)
        if value not in (None, "", [], {}):
            if isinstance(value, list):
                value = "; ".join(str(item) for item in value)
            rows.append(f"{label}: {value}")

    matrix = rule.get("_integration_matrix")
    if isinstance(matrix, dict):
        supplements = [
            ("surface trigger", matrix_value(matrix, "surface trigger")),
            ("required context", matrix_value(matrix, "required context")),
            ("false-positive risk", matrix_value(matrix, "fp risk", "fp")),
            ("positive case", matrix_value(matrix, "positive case", "+")),
            ("natural negative", matrix_value(matrix, "natural negative", "natural control")),
            ("boundary/counterexample", matrix_value(matrix, "b / counterexample", "boundary")),
            ("native-usage conflict", matrix_value(matrix, "native_usage conflict", "native_usage conflict risk")),
            ("integration plan", matrix_value(matrix, "integration", "runtime plan")),
        ]
        existing_labels = {line.split(":", 1)[0] for line in rows if ":" in line}
        for label, value in supplements:
            if value and label not in existing_labels:
                rows.append(f"{label}: {value}")
    return "\n".join(rows)


def candidate_instructions(config: dict[str, Any], mapped_rules: list[dict[str, Any]]) -> str:
    """Build project-constrained candidate instructions for one library/case."""
    cards = "\n\n".join(compact_rule_card(rule) for rule in mapped_rules)
    return (
        "Ты выполняешь контекстный редакторский проход humanizer_russian. "
        "Ответь на задачу пользователя напрямую.\n\n"
        "Жёсткие ограничения: сохрани USER_INTENT, SEMANTICS и NORM. Не меняй "
        "факты, тезис, референты, причинность, полярность и степень уверенности. "
        "Не создавай ошибок русского языка ради стилизации. Среди нормативных "
        "вариантов AUTHOR и NATIVE_USAGE выше EDITING, а detector score не цель.\n\n"
        f"Активная библиотека: {config['display_name']} ({config['source_namespace']}). "
        "Ниже даны только релевантные source-derived rule cards. Они не являются "
        "автоматическими запретами и сами по себе не доказывают современную норму. "
        "Применяй операцию только после проверки required context, negative control, "
        "boundary/counterexample и конфликта с живым русским. Если безопасной "
        "однозначной правки нет, сохрани корректный вариант или обозначь, чего не "
        "хватает. Не цитируй книгу и не выдумывай отсутствующие данные.\n\n"
        f"RELEVANT RULE CARDS:\n{cards}"
    )


def judge_instructions() -> str:
    """Return strict, expectation-based instructions for the independent judge."""
    return (
        "Ты независимый судья eval-набора humanizer_russian. Оцени только то, "
        "что следует из исходного задания, ответа кандидата и перечисленных "
        "ожиданий. Не награждай ответ за красивую формулировку и не штрафуй за "
        "стилистическое отличие, если ожидание выполнено. PASS ставь только если "
        "выполнение ожидания явно видно или однозначно следует из ответа; FAIL — "
        "если ответ ему противоречит или пропускает обязательное действие; "
        "UNCERTAIN — если данных недостаточно. semantic_violation=true только при "
        "реальной подмене факта, референта, причинности, тезиса или степени "
        "уверенности. norm_violation=true только при ясной ошибке русского языка. "
        "overall=PASS только если все expectations имеют PASS и нет semantic/norm "
        "violation; overall=FAIL при любом FAIL или violation; иначе UNCERTAIN."
    )


def validate_suite_map(
    config: dict[str, Any],
    suite: dict[str, Any],
    mapping: dict[str, Any],
    rules: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Validate complete traceability and return map rows keyed by eval ID."""
    evals = suite.get("evals")
    rows = mapping.get("cases")
    if not isinstance(evals, list) or not evals:
        raise ValueError(f"{config['id']}: suite must contain a non-empty evals array")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{config['id']}: map must contain a non-empty cases array")
    if mapping.get("library_id") not in (None, config["id"]):
        raise ValueError(f"{config['id']}: map library_id mismatch")
    if mapping.get("suite") not in (None, suite.get("suite")):
        raise ValueError(f"{config['id']}: map suite mismatch")

    eval_ids: list[str] = []
    for case in evals:
        if not isinstance(case, dict):
            raise ValueError(f"{config['id']}: eval row must be an object")
        case_id = str(case.get("id", ""))
        if not case_id or not isinstance(case.get("prompt"), str):
            raise ValueError(f"{config['id']}: malformed eval case {case!r}")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or not expectations or not all(isinstance(item, str) and item for item in expectations):
            raise ValueError(f"{config['id']}:{case_id}: expectations must be non-empty strings")
        eval_ids.append(case_id)
    if len(eval_ids) != len(set(eval_ids)):
        raise ValueError(f"{config['id']}: duplicate eval IDs")

    map_by_id: dict[str, dict[str, Any]] = {}
    for meta in rows:
        if not isinstance(meta, dict):
            raise ValueError(f"{config['id']}: map row must be an object")
        if "expectations" in meta or "expected" in meta:
            raise ValueError(f"{config['id']}: map must not contain expected answers")
        case_id = str(meta.get("id", ""))
        if not case_id or case_id in map_by_id:
            raise ValueError(f"{config['id']}: missing/duplicate map id {case_id!r}")
        mapped = meta.get("rules")
        if not isinstance(mapped, list) or not mapped:
            raise ValueError(f"{config['id']}:{case_id}: map requires at least one rule")
        unknown = [rule_id for rule_id in mapped if rule_id not in rules]
        if unknown:
            raise ValueError(f"{config['id']}:{case_id}: unknown mapped rules {unknown}")
        map_by_id[case_id] = meta

    if set(eval_ids) != set(map_by_id):
        missing = sorted(set(eval_ids) - set(map_by_id))
        extra = sorted(set(map_by_id) - set(eval_ids))
        raise ValueError(f"{config['id']}: suite/map drift; missing={missing}, extra={extra}")
    return map_by_id


def select_cases(
    suite: dict[str, Any],
    map_by_id: dict[str, dict[str, Any]],
    rules: dict[str, dict[str, Any]],
    *,
    scope: str,
    case_ids: set[str],
    limit: int | None,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Join eval cases to traceability metadata and apply CLI selection."""
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for case in suite["evals"]:
        case_id = str(case["id"])
        meta = map_by_id[case_id]
        if case_ids and case_id not in case_ids:
            continue
        mapped_rules = [rules[str(rule_id)] for rule_id in meta["rules"]]
        if scope == "model-only" and not any(
            rule.get("automation_level") == "MODEL_ONLY" for rule in mapped_rules
        ):
            continue
        selected.append((case, meta))
        if limit is not None and len(selected) >= limit:
            break
    return selected


def judgment_input(
    config: dict[str, Any],
    case: dict[str, Any],
    meta: dict[str, Any],
    candidate_text: str,
) -> str:
    """Build a self-contained judge input; expectations never reach the candidate."""
    payload = {
        "library_id": config["id"],
        "source_namespace": config["source_namespace"],
        "eval_id": case["id"],
        "prompt": case["prompt"],
        "candidate_response": candidate_text,
        "expectations": case["expectations"],
        "mapped_rules": meta["rules"],
        "counterexample": bool(meta.get("counterexample")),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def response_payload(
    *,
    model: str,
    instructions: str,
    input_text: str,
    max_output_tokens: int,
    structured: bool,
) -> dict[str, Any]:
    """Build one Responses API request body."""
    payload: dict[str, Any] = {
        "model": model,
        "store": False,
        "instructions": instructions,
        "input": input_text,
        "max_output_tokens": max_output_tokens,
    }
    if structured:
        payload["text"] = {
            "format": {
                "type": "json_schema",
                "name": "humanizer_russian_eval_judgment",
                "description": "Expectation-level judgment for one humanizer_russian eval case.",
                "strict": True,
                "schema": JUDGMENT_SCHEMA,
            }
        }
    return payload


def post_json(
    endpoint: str,
    api_key: str,
    payload: dict[str, Any],
    *,
    timeout: float,
    retries: int,
) -> dict[str, Any]:
    """POST JSON with bounded retries for transient API failures."""
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "humanizer_russian-model-evals/2",
    }
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(endpoint, data=raw, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
            value = json.loads(body)
            if not isinstance(value, dict):
                raise RuntimeError("Responses API returned a non-object JSON value")
            return value
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1200]
            last_error = RuntimeError(f"OpenAI API HTTP {exc.code}: {body}")
            if exc.code not in RETRYABLE_HTTP or attempt >= retries:
                raise last_error from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = RuntimeError(f"OpenAI API transport error: {exc}")
            if attempt >= retries:
                raise last_error from exc
        time.sleep(min(2**attempt, 8))
    raise RuntimeError(f"OpenAI API request failed: {last_error}")


def extract_output_text(response: dict[str, Any]) -> str:
    """Extract concatenated output_text content from a raw Responses response."""
    chunks: list[str] = []
    for item in response.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                chunks.append(str(content.get("text", "")))
    text = "".join(chunks).strip()
    if not text:
        raise RuntimeError(
            f"Responses API returned no output_text (status={response.get('status')!r}, "
            f"error={response.get('error')!r})"
        )
    return text


def usage_shape(response: dict[str, Any]) -> dict[str, Any]:
    """Keep only non-sensitive token accounting from a response."""
    usage = response.get("usage")
    return usage if isinstance(usage, dict) else {}


def validate_judgment(judgment: dict[str, Any], expectations: list[str]) -> None:
    """Apply structural and internal-consistency checks to judge JSON."""
    required = {
        "overall",
        "expectations",
        "semantic_violation",
        "norm_violation",
        "notes",
    }
    if set(judgment) != required:
        raise ValueError(f"judge keys differ from schema: {sorted(judgment)}")
    rows = judgment["expectations"]
    if not isinstance(rows, list) or len(rows) != len(expectations):
        raise ValueError("judge returned the wrong number of expectation rows")
    returned = [row.get("expectation") for row in rows]
    if returned != expectations:
        raise ValueError("judge changed or reordered expectation text")
    verdicts = [row.get("verdict") for row in rows]
    if any(verdict not in {"PASS", "FAIL", "UNCERTAIN"} for verdict in verdicts):
        raise ValueError(f"invalid expectation verdicts: {verdicts}")
    expected_overall = (
        "FAIL"
        if "FAIL" in verdicts or judgment["semantic_violation"] or judgment["norm_violation"]
        else "UNCERTAIN"
        if "UNCERTAIN" in verdicts
        else "PASS"
    )
    if judgment["overall"] != expected_overall:
        raise ValueError(
            f"judge overall {judgment['overall']} conflicts with expectation rows; "
            f"expected {expected_overall}"
        )


def rule_provenance(rule: dict[str, Any]) -> dict[str, Any]:
    """Return stable source/routing metadata for report consumers."""
    return {
        "rule_id": rule.get("rule_id"),
        "study_rule_id": rule.get("study_rule_id"),
        "phenomenon_id": rule.get("phenomenon_id"),
        "project_class": rule.get("project_class"),
        "automation_level": rule.get("automation_level"),
        "source_locator": rule.get("source_locator"),
    }


def run_case(
    config: dict[str, Any],
    case: dict[str, Any],
    meta: dict[str, Any],
    rules: dict[str, dict[str, Any]],
    *,
    api_key: str,
    endpoint: str,
    candidate_model: str,
    judge_model: str,
    max_output_tokens: int,
    judge_max_output_tokens: int,
    timeout: float,
    retries: int,
) -> dict[str, Any]:
    """Run candidate and judge calls for one eval case."""
    mapped_rules = [rules[str(rule_id)] for rule_id in meta["rules"]]
    candidate_response = post_json(
        endpoint,
        api_key,
        response_payload(
            model=candidate_model,
            instructions=candidate_instructions(config, mapped_rules),
            input_text=case["prompt"],
            max_output_tokens=max_output_tokens,
            structured=False,
        ),
        timeout=timeout,
        retries=retries,
    )
    candidate_text = extract_output_text(candidate_response)

    judge_response = post_json(
        endpoint,
        api_key,
        response_payload(
            model=judge_model,
            instructions=judge_instructions(),
            input_text=judgment_input(config, case, meta, candidate_text),
            max_output_tokens=judge_max_output_tokens,
            structured=True,
        ),
        timeout=timeout,
        retries=retries,
    )
    judgment = json.loads(extract_output_text(judge_response))
    if not isinstance(judgment, dict):
        raise ValueError("judge output is not a JSON object")
    validate_judgment(judgment, list(case["expectations"]))

    return {
        "id": case["id"],
        "name": case.get("name", case["id"]),
        "rules": list(meta["rules"]),
        "rule_provenance": [rule_provenance(rule) for rule in mapped_rules],
        "counterexample": bool(meta.get("counterexample")),
        "prompt": case["prompt"],
        "expectations": list(case["expectations"]),
        "candidate": {
            "model": candidate_response.get("model", candidate_model),
            "response_id": candidate_response.get("id"),
            "text": candidate_text,
            "usage": usage_shape(candidate_response),
        },
        "judgment": {
            "model": judge_response.get("model", judge_model),
            "response_id": judge_response.get("id"),
            "result": judgment,
            "usage": usage_shape(judge_response),
        },
    }


def report_summary(cases: list[dict[str, Any]], failures: list[dict[str, str]]) -> dict[str, int]:
    """Summarize judgment outcomes and transport/parser failures."""
    counts = Counter(
        case["judgment"]["result"]["overall"]
        for case in cases
        if "judgment" in case
    )
    return {
        "completed_cases": len(cases),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "uncertain": counts["UNCERTAIN"],
        "api_or_parse_failures": len(failures),
    }


def library_report(config: dict[str, Any]) -> dict[str, str]:
    """Describe the exact manifest/rules/suite/map inputs used by a run."""
    return {
        "id": config["id"],
        "display_name": config["display_name"],
        "source_namespace": config["source_namespace"],
        "manifest_path": relative_display(config["manifest_path"]),
        "rules_path": relative_display(config["rules_path"]),
        "suite_path": relative_display(config["suite_path"]),
        "map_path": relative_display(config["map_path"]),
    }


def dry_run_report(
    config: dict[str, Any],
    selected: list[tuple[dict[str, Any], dict[str, Any]]],
    rules: dict[str, dict[str, Any]],
    *,
    candidate_model: str,
    judge_model: str,
    scope: str,
) -> dict[str, Any]:
    """Return a no-network plan showing exactly what the harness would run."""
    return {
        "schema_version": 2,
        "dry_run": True,
        "library": library_report(config),
        "candidate_model": candidate_model,
        "judge_model": judge_model,
        "self_judged": candidate_model == judge_model,
        "scope": scope,
        "selected_cases": [
            {
                "id": case["id"],
                "name": case.get("name", case["id"]),
                "rules": meta["rules"],
                "rule_provenance": [rule_provenance(rules[str(rule_id)]) for rule_id in meta["rules"]],
                "counterexample": bool(meta.get("counterexample")),
            }
            for case, meta in selected
        ],
    }


def load_runtime(
    library_id: str,
    *,
    suite_override: Path | None = None,
    map_override: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Load and validate one library's complete model-eval runtime contract."""
    config = load_library_config(library_id, suite_override=suite_override, map_override=map_override)
    suite = load_json(config["suite_path"])
    mapping = load_json(config["map_path"])
    rules = load_rules(config)
    map_by_id = validate_suite_map(config, suite, mapping, rules)
    return config, suite, mapping, rules, map_by_id


def self_test() -> None:
    """Validate all registered library eval contracts and leakage guards offline."""
    library_ids = discover_model_eval_libraries()
    required = {"gal", "chukovsky", "ilyakhov"}
    if not required.issubset(library_ids):
        raise AssertionError(f"missing required model-eval libraries: {sorted(required - set(library_ids))}")

    selected_counts: dict[str, int] = {}
    first_case_bundle: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]] | None = None
    for library_id in library_ids:
        config, suite, _mapping, rules, map_by_id = load_runtime(library_id)
        selected = select_cases(
            suite,
            map_by_id,
            rules,
            scope="model-only",
            case_ids=set(),
            limit=None,
        )
        if not selected:
            raise AssertionError(f"{library_id}: model-only selection is empty")
        selected_counts[library_id] = len(selected)
        for case, meta in selected:
            if not any(rules[str(rule_id)].get("automation_level") == "MODEL_ONLY" for rule_id in meta["rules"]):
                raise AssertionError(f"{library_id}:{case['id']}: model-only filter admitted no MODEL_ONLY rule")
            instructions = candidate_instructions(config, [rules[str(rule_id)] for rule_id in meta["rules"]])
            if "USER_INTENT" not in instructions or "SEMANTICS" not in instructions or "NORM" not in instructions:
                raise AssertionError(f"{library_id}:{case['id']}: candidate hard constraints are missing")
            if any(expectation in instructions for expectation in case["expectations"]):
                raise AssertionError(f"{library_id}:{case['id']}: candidate instructions leaked eval expectations")
        dry = dry_run_report(
            config,
            selected[:2],
            rules,
            candidate_model="test-candidate",
            judge_model="test-judge",
            scope="model-only",
        )
        if dry["library"]["id"] != library_id or not dry["selected_cases"][0]["rule_provenance"]:
            raise AssertionError(f"{library_id}: dry-run provenance contract failed")
        if first_case_bundle is None:
            case, meta = selected[0]
            first_case_bundle = (config, case, meta, rules)

    if first_case_bundle is None:
        raise AssertionError("no model-eval cases available")
    config, case, meta, rules = first_case_bundle
    instructions = candidate_instructions(config, [rules[str(rule_id)] for rule_id in meta["rules"]])
    candidate_payload = response_payload(
        model="test-candidate",
        instructions=instructions,
        input_text=case["prompt"],
        max_output_tokens=700,
        structured=False,
    )
    if candidate_payload.get("store") is not False or "text" in candidate_payload:
        raise AssertionError(candidate_payload)

    judge_payload = response_payload(
        model="test-judge",
        instructions=judge_instructions(),
        input_text=judgment_input(config, case, meta, "Тестовый ответ."),
        max_output_tokens=900,
        structured=True,
    )
    fmt = judge_payload["text"]["format"]
    if fmt.get("type") != "json_schema" or fmt.get("strict") is not True:
        raise AssertionError(fmt)

    fake_response = {
        "id": "resp_test",
        "model": "test-model",
        "output": [
            {
                "type": "message",
                "content": [
                    {"type": "output_text", "text": "часть 1"},
                    {"type": "output_text", "text": " + часть 2"},
                ],
            }
        ],
    }
    if extract_output_text(fake_response) != "часть 1 + часть 2":
        raise AssertionError(fake_response)

    expectations = ["A", "B"]
    judgment = {
        "overall": "PASS",
        "expectations": [
            {"expectation": "A", "verdict": "PASS", "reason": "ok"},
            {"expectation": "B", "verdict": "PASS", "reason": "ok"},
        ],
        "semantic_violation": False,
        "norm_violation": False,
        "notes": "",
    }
    validate_judgment(judgment, expectations)
    broken = dict(judgment, overall="FAIL")
    try:
        validate_judgment(broken, expectations)
    except ValueError:
        pass
    else:
        raise AssertionError("inconsistent judge overall was accepted")

    counts = ", ".join(f"{key}={selected_counts[key]}" for key in sorted(selected_counts))
    print(f"model eval harness self-test: OK; model-only selections: {counts}")


def parse_args() -> argparse.Namespace:
    """Parse command-line options without requiring an API key for dry/self tests."""
    libraries = discover_model_eval_libraries()
    parser = argparse.ArgumentParser(description="Run contextual humanizer_russian evals via OpenAI Responses API")
    parser.add_argument("--library", choices=libraries, default=DEFAULT_LIBRARY)
    parser.add_argument("--suite", type=Path, help="optional suite override; library still supplies the rule source")
    parser.add_argument("--map", dest="map_path", type=Path, help="optional traceability-map override")
    parser.add_argument("--model", help="candidate API model ID; required for live runs")
    parser.add_argument("--judge-model", help="judge API model ID; defaults to --model")
    parser.add_argument("--scope", choices=["model-only", "all"], default="model-only")
    parser.add_argument("--case", action="append", default=[], dest="case_ids")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--max-output-tokens", type=int, default=900)
    parser.add_argument("--judge-max-output-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Run offline validation, a dry plan, or selected live eval cases."""
    args = parse_args()
    if args.self_test:
        self_test()
        return
    if args.limit is not None and args.limit <= 0:
        raise SystemExit("--limit must be positive")
    if args.retries < 0:
        raise SystemExit("--retries must be >= 0")

    config, suite, _mapping, rules, map_by_id = load_runtime(
        args.library,
        suite_override=args.suite,
        map_override=args.map_path,
    )
    selected = select_cases(
        suite,
        map_by_id,
        rules,
        scope=args.scope,
        case_ids=set(args.case_ids),
        limit=args.limit,
    )
    if args.case_ids:
        found = {case["id"] for case, _ in selected}
        missing = sorted(set(args.case_ids) - found)
        if missing:
            raise SystemExit(f"requested cases were not selected: {', '.join(missing)}")
    if not selected:
        raise SystemExit("no eval cases selected")

    candidate_model = args.model or "<required-for-live-run>"
    judge_model = args.judge_model or candidate_model
    if args.dry_run:
        report = dry_run_report(
            config,
            selected,
            rules,
            candidate_model=candidate_model,
            judge_model=judge_model,
            scope=args.scope,
        )
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return

    if not args.model:
        raise SystemExit("--model is required for a live run")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required for a live run")
    judge_model = args.judge_model or args.model

    completed: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for case, meta in selected:
        try:
            completed.append(
                run_case(
                    config,
                    case,
                    meta,
                    rules,
                    api_key=api_key,
                    endpoint=args.endpoint,
                    candidate_model=args.model,
                    judge_model=judge_model,
                    max_output_tokens=args.max_output_tokens,
                    judge_max_output_tokens=args.judge_max_output_tokens,
                    timeout=args.timeout,
                    retries=args.retries,
                )
            )
        except Exception as exc:  # keep a partial report; no API key is included
            failures.append({"id": str(case["id"]), "error": str(exc)})
            if not args.continue_on_error:
                break

    report = {
        "schema_version": 2,
        "suite": suite.get("suite"),
        "suite_version": suite.get("version"),
        "library": library_report(config),
        "run": {
            "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "candidate_model": args.model,
            "judge_model": judge_model,
            "self_judged": args.model == judge_model,
            "scope": args.scope,
            "selected_cases": len(selected),
            "endpoint": args.endpoint,
            "store": False,
        },
        "summary": report_summary(completed, failures),
        "cases": completed,
        "failures": failures,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    if failures:
        raise SystemExit(2)
    if any(case["judgment"]["result"]["overall"] != "PASS" for case in completed):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
