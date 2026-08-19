# Dual runtime: compact humanizer + editorial board

`humanizer_russian` has one codebase and two product modes.

## 1. Compact humanizer

Entry point: `scripts/check.py`.

Purpose: cheap mechanical-first verification and a short unified verdict. It is the default for CI, quick checks and projects that do not need reviewer provenance.

It consumes the same underlying rule engine but exposes only calibrated default mechanical findings unless `--extended` is requested.

## 2. Editorial board

Entry point: `scripts/review.py`.

Purpose: detailed review where provenance matters. It preserves separate opinions from source libraries, detects agreement/conflict, applies a style policy and can later hand only unresolved `MODEL_ONLY` cases to a model.

The board does not duplicate rule implementations from compact mode.

## Three independent axes

### Source libraries

Examples: native Russian, Nora Gal, Ilyakhov/Sarycheva, Chukovsky, future books or house-style corpora.

Each source has a manifest under `libraries/<id>/library.json`, an optional mechanical linter module, references/evals, and a reviewer profile.

### Product mode

- compact;
- editorial board.

### Editorial style

Examples: neutral, `rslive_content`, business, literary, social, academic.

A style decides how to resolve editorial disagreement; it does not rewrite the source rules themselves.

## Shared normalized finding

Every source library eventually produces a finding with at least:

- `rule_id`;
- `phenomenon_id`;
- `project_class`;
- `automation_level`;
- `verdict`;
- `reviewer_id`;
- `excerpt`/location;
- `reason`;
- optional `operation`.

`phenomenon_id` is deliberately source-neutral. If Gal and Ilyakhov detect the same underlying phenomenon, they should use the same phenomenon id while retaining different source rule ids.

## Why reviewer disagreement is preserved

Editorial sources are not a single hierarchy of truth. One source may value compression while another protects rhythm, colloquiality or imagery. A source conflict is therefore an expected result, not an integration failure.

Hard constraints remain outside voting:

`USER_INTENT + SEMANTICS + NORM`.

No style or majority vote may authorize a semantic regression or a real language error.

## Adding books as libraries

The long-lived branch named for the author remains the research line. It periodically merges current `main`, evolves the study, and opens PRs back to `main`.

The integration target is a library contract, not a monolithic prompt:

`book → audited study → rules → mechanical feasibility → source linter/tests → library manifest → reviewer → board`.

Original copyrighted books should live outside this public repository (for example in a private source repository). The public repo stores derived rules, locators, tests and provenance, not book dumps.

## Consumer contract

External repositories should prefer stable CLIs/JSON over importing internal linters:

```bash
python scripts/check.py page.md --json
python scripts/review.py page.md --style rslive_content --format json
```

This lets a consumer switch between compact and board mode without learning the internals of Gal/Ilyakhov/Chukovsky modules.
