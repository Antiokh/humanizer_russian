# Migration history

`humanizer_russian` is an independent repository for the Russian humanizer/editor project.

It was separated from `Antiokh/humanizer--ru` on 2026-08-19 after the Russian-language work had grown beyond a small compatibility fork.

## Source lines that were consolidated

### Nora Gal semantic layer

The earlier line introduced semantic/literary checks for abstraction, voice, metaphor conflicts, collocation and translated syntax. These remain contextual semantic checks rather than regex hard bans.

### Russian-first / native-usage layer

The project now separates:

- `USER_INTENT` — task/function preservation;
- `SEMANTICS` — factual and logical preservation;
- `NORM` — grammatical and punctuation constraints;
- `NATIVE_USAGE` — natural choices made by Russian native speakers among valid forms;
- `AUTHOR` — corpus-derived idiolect;
- `EDITING` / `AI_CALQUE` — later editorial passes;
- detector score — diagnostic only, never optimization target.

## Runtime change: mechanical first

After migration the project moved away from treating large context files as the primary runtime engine.

Default check:

```bash
python scripts/check.py text.md
```

Deep heuristic audit:

```bash
python scripts/check.py --extended text.md
```

The full surface linter still exists in `scripts/lint.py`, but `check.py` exposes only the higher-precision subset by default.

## Testing change

Primary linter correctness is now tested deterministically:

```bash
python scripts/benchmark_lint.py
```

Corpus: `tests/lint_cases.json`.

This benchmark uses positive and negative controls without LLM judges, web calls or reference-file retrieval. Context/model evals remain for behavior that is genuinely semantic and cannot be settled by regex/statistical checks.

## Review feedback incorporated

- author-profile sentence/n-gram/paragraph statistics preserve document boundaries;
- source filesystem paths are not written to `profile.json`;
- profiler and schema use one contract;
- generated profiles are validated in CI;
- `NATIVE_WARNING` is non-gating;
- repeated common material is checked in Russian contrasts;
- native-language evals include no-op/good-human controls;
- runtime reference loading is selective rather than mandatory.

## Why this is not a compatibility fork

Future architecture does not need to preserve detector-driven assumptions of the old fork. Old rules may be reintroduced only after reclassification and testing.

## Policy for future rules

A rule is promoted to default mechanical runtime only after it has a deterministic positive case and a natural negative control. Rules with high context dependence remain extended/contextual.
