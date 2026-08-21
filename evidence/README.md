# Evidence providers

Evidence providers are an optional fourth axis of `humanizer_russian`.

They are **not reviewer libraries** and do not vote in the editorial board. A provider supplies corpus, spoken-language, lexical-pragmatic, normative, parsed-corpus, or research evidence for a `phenomenon_id` that the editor is already considering.

```text
BOOK/SOURCE -> REVIEW LIBRARIES -> findings
CORPORA/DICTIONARIES/REFERENCE -> EVIDENCE PROVIDERS -> evidence
STYLE -> policy

findings + evidence -> EDITORIAL BOARD
```

## Runtime contract

Evidence is deliberately cheap to disable and impossible to make a hidden dependency of the compact skill:

- `scripts/check.py` never runs evidence providers.
- `scripts/review.py` runs no evidence provider unless `--evidence ...` is supplied.
- `--evidence off` or omitting the option means zero provider work.
- `HUMANIZER_EVIDENCE=off` is a global kill switch.
- `PROJECT` is a scaffold state, not a runtime state: project-only providers cannot be selected explicitly and are excluded from both `auto` and `all`.
- only `OPERATIONAL` providers are runtime-eligible.
- remote providers must have `enabled_by_default: false`.
- every operational provider is isolated in a subprocess with a hard per-provider timeout.
- the whole evidence pass has a global budget (`HUMANIZER_EVIDENCE_BUDGET_MS`, default 1200 ms).
- provider failures/timeouts are `SKIP` by default and appear in `evidence_status`; they do not fail the review.
- a provider may use `failure_policy: ERROR` only for explicit research workflows.

This means an unavailable corpus/API can reduce evidence quality only after an actual provider has been promoted to `OPERATIONAL`; unfinished project scaffolds cannot masquerade as enabled features.

## Provider manifest

A provider lives at `evidence/<provider_id>/provider.json` and follows `schemas/evidence-provider.schema.json`.

Important fields: stable `id`, `status`, `evidence_type`, optional `module_path`, `enabled_by_default`, `network_required`, `failure_policy`, `timeout_ms`, capabilities and references.

Provider states are deliberately strict:

- `PROJECT` — design/scaffold only; must have `enabled_by_default: false` and cannot be selected by runtime;
- `OPERATIONAL` — implemented and audited enough to run; requires `module_path`;
- `DISABLED` — implemented or historical provider intentionally unavailable to runtime.

Promotion from `PROJECT` to `OPERATIONAL` is an explicit reviewed change. Adding a module file by itself does not activate anything.

The preferred adapter is `evidence_v1`:

```python
def collect(text: str, context: dict, timeout_ms: int) -> dict:
    return {"evidence": [...]}
```

The runtime supplies normalized findings in `context` so a provider can query only relevant phenomena.

## Evidence item

Normalized evidence follows `schemas/evidence-item.schema.json` and includes `provider_id`, `phenomenon_id`, evidence type, direction, target scope, reason and provenance.

`direction` is **not a reviewer verdict**. It can be `SUPPORTS_KEEP`, `SUPPORTS_CHANGE`, `CONTEXT`, or `NEUTRAL`. Editorial votes remain reviewer findings. Evidence is attached to matching phenomena without changing board status/recommendation automatically.

## Epistemic boundaries

Frequency is not norm. A social-media corpus cannot promote a form to `NORM`.

A normative source can support a norm decision only when its scope/version/entry is identified.

A book/reviewer cannot use corpus popularity as a reason to erase register, author voice, functional repetition, pragmatic particles, ellipsis, or information structure.

## Project provider families

The repository currently contains project-only manifests for `current_usage`, `spoken_russian`, `discourse_lexicon`, `normative_reference`, and `parsed_russian`.

They are intentionally non-operational until a concrete source/API, rights/terms, query contract, caching strategy, calibration tests and runtime module are chosen. `--evidence all` does not include them, and requesting one by ID is an error rather than a simulated `UNAVAILABLE` run.
