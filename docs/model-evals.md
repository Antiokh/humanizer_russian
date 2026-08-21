# Live model evaluation

`humanizer_russian` separates deterministic surface checks from contextual model behavior. Deterministic CI proves software/routing contracts; it does **not** prove that `MODEL_ONLY` linguistic/editorial rules are handled correctly by a live model.

`scripts/run_model_evals.py` is the opt-in, manifest-driven harness for that second layer.

## Library contract

A participating knowledge library declares in `libraries/<id>/library.json`:

- `model_eval_path` — synthetic/project eval suite;
- `model_eval_map_path` — case → canonical rule/source traceability;
- `rules_path` — canonical runtime rules.

The harness discovers only libraries with a complete declared contract. `scripts/validate_libraries.py` also rejects half-registered libraries and guards the intended operational registration set against silent disappearance.

Current registered libraries:

- Gal;
- Chukovsky;
- Ilyakhov/Sarycheva;
- Golub;
- Visson;
- Rosenthal.

Visson reuses the already audited `evals/lynn-visson.json` + `evals/lynn-visson-map.json` pair. Rosenthal uses a compact project-authored synthetic suite mapped to canonical `ROS-R*` rules across the integrated source cycles. The Rosenthal suite is intentionally preservation-heavy: historical/source-period advice never becomes current `NORM` merely because a model agrees with it.

## How one case runs

For each selected case the harness makes two independent API calls:

1. **candidate** — receives the user prompt, project hard constraints and only the mapped source-derived rule cards. It does **not** receive expected answers or counterexample labels;
2. **judge** — receives the prompt, candidate answer and explicit expectations, then returns a strict structured judgment.

The default scope is `model-only`: a case is selected when at least one mapped rule has `automation_level=MODEL_ONLY`. `--scope all` includes all mapped suite cases, including preservation/mechanical boundary cases where the library provides them.

This is calibration, not a normative truth oracle. Results remain model-, prompt- and snapshot-dependent. Model/judge agreement cannot turn a book recommendation into current `NORM` and cannot substitute for deterministic precision evidence required by mechanical rules.

## API contract

The harness uses the OpenAI Responses API directly over HTTPS and reads `OPENAI_API_KEY` only from the environment. It sends `store: false` and never writes the API key to reports. Candidate and judge model IDs are supplied explicitly rather than hard-coded.

Official references:

- `https://platform.openai.com/docs/quickstart/make-your-first-api-request`
- `https://platform.openai.com/docs/api-reference/responses`
- `https://platform.openai.com/docs/api-reference/models`

## Discover / dry-run

No API key or live cost:

```bash
python scripts/run_model_evals.py --self-test
python scripts/run_model_evals.py --library gal --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --library chukovsky --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --library ilyakhov --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --library golub --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --library visson --dry-run --model YOUR_MODEL
python scripts/run_model_evals.py --library rosenthal --dry-run --model YOUR_MODEL
```

The offline self-test iterates over every registered library and verifies:

- eval ↔ traceability-map joining;
- rule existence/provenance;
- `MODEL_ONLY` selection;
- no expectation leakage into candidate instructions;
- dry-run provenance construction;
- `store: false` request construction;
- strict JSON-schema judge request construction;
- Responses `output_text` extraction;
- consistency between per-expectation and overall verdicts.

## Live run

Minimal smoke run for one registered library:

```bash
export OPENAI_API_KEY='...'
python scripts/run_model_evals.py \
  --library gal \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --limit 3 \
  --output eval-results/gal-smoke.json
```

Full contextual run:

```bash
python scripts/run_model_evals.py \
  --library rosenthal \
  --model YOUR_CANDIDATE_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --scope model-only \
  --continue-on-error \
  --output eval-results/rosenthal-model-only.json
```

Use different candidate and judge models when practical. If the same model is used for both roles, the report records that weaker evidence boundary.

## Report contract

Reports include library/source context and per-case rule provenance together with:

- requested and returned candidate/judge model IDs;
- response IDs;
- token usage returned by the API;
- candidate text;
- per-expectation `PASS` / `FAIL` / `UNCERTAIN` judgments;
- semantic/norm violation flags;
- API/transport/parser failures.

Raw local result files belong under `eval-results/`, which is ignored by Git. Do not commit raw output automatically; review it case by case and source-control only conclusions useful for calibration.

## Exit codes

- `0` — all completed judgments pass and there are no API/parser failures;
- `1` — at least one completed case is `FAIL` or `UNCERTAIN`;
- `2` — API/transport/structured-output parsing failed for at least one case.

`--continue-on-error` controls whether the runner continues after an API/parser failure. It does not convert failures into passes.

## Promotion policy

A green model run is never enough to promote a rule to mechanical runtime. Promotion still requires:

1. a defensible observable surface or parser-backed signal;
2. true positives;
3. natural negative controls;
4. boundary and intentional-use counterexamples;
5. acceptable false-positive behavior on real Russian text;
6. no conflict with `USER_INTENT`, `SEMANTICS`, `NORM`, `AUTHOR` or `NATIVE_USAGE`.

If those conditions cannot be met, the correct state is still `MODEL_ONLY`.
