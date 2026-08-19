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
- remote providers must have `enabled_by_default: false`.
- every operational provider is isolated in a subprocess with a hard per-provider timeout.
- the whole evidence pass has a global budget (`HUMANIZER_EVIDENCE_BUDGET_MS`, default 1200 ms).
- provider failures/timeouts are `SKIP` by default and appear in `evidence_status`; they do not fail the review.
- a provider may use `failure_policy: ERROR` only for explicit research workflows.

This means an unavailable corpus/API can reduce evidence quality but cannot stall or break the normal humanizer path.

## Provider manifest

A provider lives at `evidence/<provider_id>/provider.json` and follows `schemas/evidence-provider.schema.json`.

Important fields: stable `id`, `status`, `evidence_type`, optional `module_path`, `enabled_by_default`, `network_required`, `failure_policy`, `timeout_ms`, capabilities and references.

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

## Planned provider families

The repository reserves disabled/planned manifests for `current_usage`, `spoken_russian`, `discourse_lexicon`, `normative_reference`, and `parsed_russian`.

They are intentionally non-operational until a concrete source/API, rights/terms, query contract, caching strategy, and calibration tests are chosen.
