# Dual runtime: compact humanizer + editorial board

`humanizer_russian` has one codebase and two product modes.

## Compact

`scripts/check.py` is the cheap mechanical-first path. **Compact never invokes evidence providers**, so corpus/API availability cannot slow or break the normal skill.

## Editorial board

`scripts/review.py` preserves source opinions, disagreement and style policy. Evidence providers are optional and off by default.

## Four independent axes

1. **Source libraries** — native Russian, Gal, Ilyakhov/Sarycheva, Chukovsky, future books. They produce reviewer findings.
2. **Evidence providers** — corpora, spoken Russian, discourse lexicons, current normative references, parsed data. They produce evidence, not votes.
3. **Product mode** — compact or editorial board.
4. **Editorial style** — neutral, `rslive_content`, future business/literary/social profiles.

Both findings and evidence use source-neutral `phenomenon_id`, while provenance remains separate.

## Availability boundary

Normal `check.py` and normal `review.py` perform no external evidence queries. Evidence is explicit via `--evidence ...`. Provider calls are hard-timed; the whole evidence phase has a global budget; failures are skipped by default; `HUMANIZER_EVIDENCE=off` disables everything immediately.

## Voting boundary

Reviewer disagreement remains `CONSENSUS`, `MAJORITY`, `SOURCE_CONFLICT`, `SINGLE_REVIEW`, `REVIEW`, or `NO_ACTION`. Evidence is attached after grouping and does not modify reviewer verdicts or style score automatically.

Hard constraints remain outside voting: `USER_INTENT + SEMANTICS + NORM`.

See `docs/evidence-provider-architecture.md` for the evidence contract.
