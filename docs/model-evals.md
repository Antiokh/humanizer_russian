# Live model evaluation

`humanizer_russian` separates deterministic surface checks from contextual model behavior. The deterministic CI suite does **not** prove that the 36 Nora Gal `MODEL_ONLY` rules work in a live model. `scripts/run_model_evals.py` is the opt-in harness for that second layer.

## What it measures

The harness reads:

- `evals/nora-gal.json` — original project prompts and explicit expectations;
- `evals/nora-gal-map.json` — rule/source traceability;
- `libraries/gal/rules/*.json` — canonical rule cards and guards.

For each selected case it makes two independent API calls:

1. **candidate** — receives the user prompt, project hard constraints and only the mapped Gal rule cards. It does **not** receive the eval expectations;
2. **judge** — receives the prompt, candidate answer and explicit expectations, then returns a strict structured judgment.

The default scope is `model-only`: a case is selected only when at least one mapped Gal rule has `automation_level=MODEL_ONLY`. `--scope all` runs the complete 45-case suite, including mechanical/metric preservation cases.

This is a model benchmark, not a normative truth oracle. Results remain model-, prompt- and snapshot-dependent. A judge disagreement is evidence for calibration, not permission to promote an editorial rule to `NORM`.

## API contract

The harness uses the OpenAI Responses API directly over HTTPS and reads `OPENAI_API_KEY` only from the environment. It sends `store: false` and never writes the API key to output. Candidate model IDs are supplied explicitly rather than hard-coded, because model availability changes over time.

OpenAI's current official API documentation describes the Responses API as the primary text-generation interface and documents Structured Outputs under `text.format` with `type: json_schema`. API keys should be kept in environment variables rather than embedded in source code.

Official references:

- `https://platform.openai.com/docs/quickstart/make-your-first-api-request`
- `https://platform.openai.com/docs/api-reference/responses`
- `https://platform.openai.com/docs/api-reference/models`

## Offline checks

No API key or network call:

```bash
python scripts/run_model_evals.py --self-test
python scripts/run_model_evals.py --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --dry-run --model YOUR_MODEL --scope all
```

The self-test verifies:

- eval ↔ traceability-map joining;
- `MODEL_ONLY` case selection;
- no expectation leakage into the candidate prompt;
- `store: false` request construction;
- strict JSON-schema judge request construction;
- Responses `output_text` extraction;
- judge/overall consistency rules.

## Live run

Minimal smoke run:

```bash
export OPENAI_API_KEY='...'
python scripts/run_model_evals.py \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --limit 3 \
  --output eval-results/gal-smoke.json
```

One case:

```bash
python scripts/run_model_evals.py \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --case gal-34 \
  --output eval-results/gal-34.json
```

Full contextual run:

```bash
python scripts/run_model_evals.py \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --scope model-only \
  --continue-on-error \
  --output eval-results/gal-model-only.json
```

Full 45-case run:

```bash
python scripts/run_model_evals.py \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --scope all \
  --continue-on-error \
  --output eval-results/gal-all.json
```

Use different candidate and judge models for stronger evidence when practical. If they are the same, the report records `self_judged: true`; such a result should be treated as weaker evidence.

## Exit codes

- `0` — all completed judgments are `PASS` and there are no API/parser failures;
- `1` — at least one completed case is `FAIL` or `UNCERTAIN`;
- `2` — API/transport/structured-output parsing failed for at least one case.

`--continue-on-error` controls whether the runner continues after an API/parser failure. It does not convert failures into passes.

## Result handling

Local result files belong under `eval-results/`, which is ignored by Git. A report records:

- candidate and judge model IDs returned by the API;
- response IDs;
- token usage reported by the API;
- candidate text;
- per-expectation verdicts and reasons;
- semantic/norm violation flags;
- transport/parser failures.

Do not commit raw benchmark output automatically. Review it first. Only aggregate findings that are useful for project calibration should become source-controlled research notes.

## Promotion policy

A green model run is not enough to promote a rule from `MODEL_ONLY` to `EXTENDED_SOFT` or `DEFAULT_MECHANICAL`. Promotion still requires:

1. a mechanically observable surface proxy;
2. positive cases;
3. natural negatives;
4. boundary and intentional counterexamples;
5. acceptable false-positive behavior on real Russian text;
6. no conflict with `SEMANTICS`, `NORM`, `AUTHOR` or `NATIVE_USAGE`.
