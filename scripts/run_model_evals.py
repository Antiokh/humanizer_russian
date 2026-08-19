#!/usr/bin/env python3
"""Run Nora Gal contextual evals through the OpenAI Responses API.

This harness is intentionally opt-in and never runs in CI against a live model.
It reads the public project eval fixtures, gives the candidate model only the
mapped Gal rule cards (not the expected answers), then asks a judge model to
score the candidate against the explicit expectations.

Authentication comes only from OPENAI_API_KEY. The key is never written to the
report. Callers must choose the model explicitly because API model availability
changes over time.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = ROOT / "evals/nora-gal.json"
DEFAULT_MAP = ROOT / "evals/nora-gal-map.json"
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


def load_gal_rules() -> dict[str, dict[str, Any]]:
    """Load all canonical Gal rule records keyed by rule_id."""
    index = load_json(ROOT / "libraries/gal/rules.json")
    rules: dict[str, dict[str, Any]] = {}
    for relative in index["groups"]:
        payload = load_json(ROOT / relative)
        for rule in payload["rules"]:
            rule_id = str(rule["rule_id"])
            if rule_id in rules:
                raise ValueError(f"duplicate Gal rule_id: {rule_id}")
            rules[rule_id] = rule
    return rules


def select_cases(
    suite: dict[str, Any],
    mapping: dict[str, Any],
    rules: dict[str, dict[str, Any]],
    *,
    scope: str,
    case_ids: set[str],
    limit: int | None,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Join eval cases to traceability metadata and apply CLI selection."""
    map_by_id = {item["id"]: item for item in mapping["cases"]}
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for case in suite["evals"]:
        case_id = str(case["id"])
        meta = map_by_id.get(case_id)
        if meta is None:
            raise ValueError(f"eval {case_id} is missing from the Gal traceability map")
        if case_ids and case_id not in case_ids:
            continue
        mapped_rules = [rules[rule_id] for rule_id in meta["rules"]]
        if scope == "model-only" and not any(
            rule["automation_level"] == "MODEL_ONLY" for rule in mapped_rules
        ):
            continue
        selected.append((case, meta))
        if limit is not None and len(selected) >= limit:
            break
    return selected


def compact_rule_card(rule: dict[str, Any]) -> str:
    """Render only the rule information needed by the candidate model."""
    return "\n".join(
        [
            f"[{rule['rule_id']}] {rule['phenomenon_id']}",
            f"operation: {rule['operation']}",
            f"semantic invariant: {rule['semantic_invariant']}",
            f"required context: {rule['required_context']}",
            f"native/author guard: {rule['conflict_with_native_usage']}",
            f"natural negative: {rule['natural_negative']}",
            f"boundary: {rule['boundary_case']}",
            f"intentional counterexample: {rule['intentional_counterexample']}",
        ]
    )


def candidate_instructions(mapped_rules: list[dict[str, Any]]) -> str:
    """Build the project-constrained candidate instructions for one case."""
    cards = "\n\n".join(compact_rule_card(rule) for rule in mapped_rules)
    return (
        "Ты выполняешь контекстный редакторский проход humanizer_russian. "
        "Ответь на задачу пользователя напрямую.\n\n"
        "Жёсткие ограничения: сохрани USER_INTENT, SEMANTICS и NORM. Не меняй "
        "факты, тезис, референты, причинность и степень уверенности. Не создавай "
        "ошибок русского языка ради стилизации. Среди нормативных вариантов "
        "AUTHOR и NATIVE_USAGE выше EDITING.\n\n"
        "Ниже даны только релевантные правила системы Норы Галь. Это "
        "редакторские эвристики, а не автоматические запреты и не доказательство "
        "современной языковой нормы. Применяй правило только после проверки его "
        "guard/boundary/counterexample. Если безопасной однозначной правки нет, "
        "не выдумывай недостающие сведения. Не цитируй и не пересказывай книгу; "
        "выдай только полезный пользователю результат.\n\n"
        f"RELEVANT RULE CARDS:\n{cards}"
    )


def judge_instructions() -> str:
    """Return strict, expectation-based instructions for the judge model."""
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


def judgment_input(
    case: dict[str, Any],
    meta: dict[str, Any],
    candidate_text: str,
) -> str:
    """Build a self-contained judge input without exposing hidden source text."""
    payload = {
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
        "User-Agent": "humanizer_russian-model-evals/1",
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
    """Apply cheap structural and semantic consistency checks to judge JSON."""
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
        if "FAIL" in verdicts
        or judgment["semantic_violation"]
        or judgment["norm_violation"]
        else "UNCERTAIN"
        if "UNCERTAIN" in verdicts
        else "PASS"
    )
    if judgment["overall"] != expected_overall:
        raise ValueError(
            f"judge overall {judgment['overall']} conflicts with expectation rows; "
            f"expected {expected_overall}"
        )


def run_case(
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
    mapped_rules = [rules[rule_id] for rule_id in meta["rules"]]
    candidate_response = post_json(
        endpoint,
        api_key,
        response_payload(
            model=candidate_model,
            instructions=candidate_instructions(mapped_rules),
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
            input_text=judgment_input(case, meta, candidate_text),
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
        "name": case["name"],
        "rules": list(meta["rules"]),
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


def dry_run_report(
    selected: list[tuple[dict[str, Any], dict[str, Any]]],
    rules: dict[str, dict[str, Any]],
    *,
    candidate_model: str,
    judge_model: str,
    scope: str,
) -> dict[str, Any]:
    """Return a no-network plan showing exactly what the harness would run."""
    return {
        "schema_version": 1,
        "dry_run": True,
        "candidate_model": candidate_model,
        "judge_model": judge_model,
        "self_judged": candidate_model == judge_model,
        "scope": scope,
        "selected_cases": [
            {
                "id": case["id"],
                "name": case["name"],
                "rules": meta["rules"],
                "automation_levels": {
                    rule_id: rules[rule_id]["automation_level"] for rule_id in meta["rules"]
                },
                "counterexample": bool(meta.get("counterexample")),
            }
            for case, meta in selected
        ],
    }


def self_test() -> None:
    """Validate fixture joining, request shape, output parsing, and judge logic offline."""
    suite = load_json(DEFAULT_SUITE)
    mapping = load_json(DEFAULT_MAP)
    rules = load_gal_rules()
    selected = select_cases(
        suite,
        mapping,
        rules,
        scope="model-only",
        case_ids=set(),
        limit=None,
    )
    if not selected:
        raise AssertionError("model-only selection is empty")
    if not all(
        any(rules[rule_id]["automation_level"] == "MODEL_ONLY" for rule_id in meta["rules"])
        for _, meta in selected
    ):
        raise AssertionError("model-only selection admitted a case without a MODEL_ONLY rule")

    case, meta = selected[0]
    instructions = candidate_instructions([rules[rule_id] for rule_id in meta["rules"]])
    if "USER_INTENT" not in instructions or "SEMANTICS" not in instructions or "NORM" not in instructions:
        raise AssertionError("candidate hard constraints are missing")
    if any(expectation in instructions for expectation in case["expectations"]):
        raise AssertionError("candidate instructions leaked eval expectations")

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
        input_text=judgment_input(case, meta, "Тестовый ответ."),
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

    print(
        f"model eval harness self-test: OK; model-only selection={len(selected)} "
        f"of {len(suite['evals'])} evals"
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line options without requiring an API key for dry/self tests."""
    parser = argparse.ArgumentParser(description="Run contextual humanizer_russian evals via OpenAI Responses API")
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--map", dest="map_path", type=Path, default=DEFAULT_MAP)
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
    """Run offline validation, a dry plan, or the selected live eval cases."""
    args = parse_args()
    if args.self_test:
        self_test()
        return
    if args.limit is not None and args.limit <= 0:
        raise SystemExit("--limit must be positive")
    if args.retries < 0:
        raise SystemExit("--retries must be >= 0")

    suite = load_json(args.suite)
    mapping = load_json(args.map_path)
    rules = load_gal_rules()
    selected = select_cases(
        suite,
        mapping,
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
        except Exception as exc:  # keep a partial report; no secret is included
            failures.append({"id": str(case["id"]), "error": str(exc)})
            if not args.continue_on_error:
                break

    report = {
        "schema_version": 1,
        "suite": suite.get("suite"),
        "suite_version": suite.get("version"),
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
