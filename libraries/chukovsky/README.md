# Chukovsky knowledge library

This directory is the runtime-facing integration of Корней Чуковский, «Живой как жизнь».

It is not a second humanizer and does not contain the book. The same normalized library output is consumed by both product modes:

```text
source study
  -> libraries/chukovsky/rules.json
  -> scripts/chukovsky_checks.py
  -> scripts/lint_chukovsky.py (review_v1)
  -> scripts/check.py              # compact
  -> scripts/review.py             # editorial board
```

## Rule identity

`CHUK-Rxx` is the canonical runtime/source `rule_id` and matches `source_namespace=CHUK`.

The older `CHK-Rxx` identifiers remain in the deep study as historical research-card IDs. `rules.json` maps each historical card to exactly one canonical runtime ID so the migration does not rewrite or destroy the research history.

`phenomenon_id` is source-neutral. It is reused across authors only when the underlying mechanism and editorial decision are genuinely the same.

## Study and detail sources

The book study remains under `studies/chukovsky-zhivoy-kak-zhizn/` and is the provenance layer. In particular:

- `rules.md` — scope, semantic invariant, positive operation, guards and counterexamples;
- `integration-matrix.md` — project class, automation, trigger, required context, false-positive risk, natural negatives, overlaps and NATIVE_USAGE conflicts;
- `counterexamples.md` — boundary families;
- `interactions.md` — rule interactions;
- `evals.json` + `eval-map.json` — source-study preservation/compound cases;
- `references/chukovsky.md` — compact operational reference for contextual use.

The runtime registry deliberately does not copy that prose into every JSON row.

## Automation split

The canonical 38-rule registry currently contains:

- `HARD_GATE`: 0;
- `DEFAULT_MECHANICAL`: 0;
- `EXTENDED_SOFT`: 7;
- `METRIC_ONLY`: 2;
- `MODEL_ONLY`: 29.

The seven mechanical rules are implemented once in `scripts/chukovsky_checks.py` and normalized once in `scripts/lint_chukovsky.py`. Compact and board do not have separate implementations.

## MODEL_ONLY loading policy

`rules.json:model_only_rule_ids` is the explicit residue. A future contextual board pass should:

1. select only relevant `MODEL_ONLY` IDs;
2. load `references/chukovsky.md` and, when necessary, the corresponding historical rule card via `study_rule_id`;
3. use its source locator, scope, guard/counterexample and preservation eval mapping;
4. never load the whole book or whole study by default;
5. never duplicate a mechanical finding in model instructions.

Model JSON fixtures in `evals/chukovsky.json` are test scenarios only. They are not a passed deterministic benchmark until a real model/judge harness is run.

## Compact behavior

Default compact mode shows no Chukovsky finding because the library has no `DEFAULT_MECHANICAL` rule.

`python scripts/check.py --extended text.md` may show the seven `EXTENDED_SOFT` candidates. Compatible duplicate phenomena from multiple libraries can be collapsed into one compact row, with source provenance preserved in the JSON report. Directional CHANGE/KEEP conflicts are not collapsed.

## Editorial-board behavior

`python scripts/review.py text.md --style neutral` keeps `reviewer_id=chukovsky`, canonical `CHUK-Rxx` provenance and source-neutral `phenomenon_id`.

Cross-author disagreement remains `SOURCE_CONFLICT`; a style policy may choose a recommendation but must not overwrite the source verdicts.

## Existing-library overlap audit

Before this library is merged, `main` has only the enabled `native` knowledge library. No Chukovsky `phenomenon_id` is an exact duplicate of a registered native mechanical phenomenon. Conceptual overlaps with native ellipsis/repetition protections and likely future Gal/Ilyakhov libraries are documented in `library-routing.md` and must be reused when those sources become operational.
