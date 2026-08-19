# Evidence-provider architecture

`humanizer_russian` separates editorial opinions from evidence.

```text
BOOK/SOURCE -> KNOWLEDGE LIBRARY -> NORMALIZED FINDING (reviewer verdict)
CORPUS/DICTIONARY/NORMATIVE REFERENCE/PARSED DATA -> EVIDENCE PROVIDER -> NORMALIZED EVIDENCE (not a vote)
finding + evidence + style -> EDITORIAL BOARD
```

A reviewer library answers: **what does this editorial system recommend?** An evidence provider answers: **what evidence is available about this phenomenon?**

## Runtime rule: evidence is optional

Evidence must never become a hidden availability or latency dependency.

- Compact `scripts/check.py` does not import or run evidence providers.
- Board `scripts/review.py` defaults to evidence **off**.
- Evidence is requested explicitly with `--evidence auto`, `--evidence all`, or provider ids.
- `--evidence off` and `HUMANIZER_EVIDENCE=off` disable it immediately.
- Remote providers are forbidden from `enabled_by_default=true`.
- Provider calls are subprocess-isolated and hard-timed.
- A global evidence budget caps total delay.
- Default failure policy is `SKIP`: timeout/unavailability is reported, not raised.

Unavailable evidence lowers evidence coverage; it does not block editing.

## Normalized contract

Provider manifests live under `evidence/<id>/provider.json`. Operational modules implement `evidence_v1` and return evidence keyed by the same source-neutral `phenomenon_id` namespace used by reviewer findings.

Evidence directions (`SUPPORTS_KEEP`, `SUPPORTS_CHANGE`, `CONTEXT`, `NEUTRAL`) are evidence, not verdicts. They must never be copied into `reviewer_verdicts`.

Board status/recommendation continues to be calculated from reviewer findings. Evidence remains attached and visible for contextual/model reasoning.

## Availability lifecycle

`PLANNED` means the source family is known but no runtime adapter is active. `OPERATIONAL` requires a tested module. `DISABLED` is intentionally unavailable.

Explicitly requesting `PLANNED` or `DISABLED` returns immediate `UNAVAILABLE` without a network attempt.

## Calibration use

Evidence providers also support offline calibration: candidate mechanical rule -> natural corpora -> false-positive analysis by genre/register -> automation-level decision. Do not invent universal numeric thresholds in advance.
