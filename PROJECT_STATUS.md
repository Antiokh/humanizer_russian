# Project status

## 2026-08-19 — independent repository initialized

The active development base is `Antiokh/humanizer_russian`. The project name is **humanizer_russian**.

The repository consolidates:

- Nora Gal semantic editing layer;
- Russian norm layer;
- native-speaker usage layer;
- audit of inherited humanizer rules;
- evidence audit for AI-writing claims;
- author-profile framework and JSON Schema;
- deterministic surface linter;
- Russian/Nora Gal eval suites;
- Custom GPT instructions/setup/tests;
- owner feedback log;
- CI checks.

## Unified architecture

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

## Native-Russian redesign

- paragraph/context-first editing rather than isolated-sentence rewriting;
- context economy and safe ellipsis;
- repeated common material factored before synonym substitution;
- Russian morphology allowed to carry relations instead of restoring English-like SVO;
- word order chosen by information structure and strong initial/final positions;
- contrast Russified instead of mechanically split into `Это не X. Это Y.`;
- parcellation judged by function, not sentence length;
- pragmatic particles and conversational register preserved by function;
- anglo-American slogan/Q&A rhetoric treated as a cluster, not a hard ban;
- good human Russian is a negative eval: no rewrite is a valid result.

## Mechanical-first runtime

The runtime is now explicitly split into two passes.

Default:

```bash
python scripts/check.py text.md
```

This exposes only cheap/high-precision surface checks plus technical artifacts.

Optional deep audit:

```bash
python scripts/check.py --extended text.md
```

This adds lower-confidence native/style/AI heuristics such as repeated explicit context, undercompression, possessive overexplication and rhetorical clusters.

Reference files are source material for disputed cases and rule development, not mandatory runtime payload.

## Deterministic regression testing

Primary linter benchmark:

```bash
python scripts/benchmark_lint.py
```

Corpus: `tests/lint_cases.json`.

The benchmark uses positive cases, clean native-language controls and explicit must-not-find checks. No LLM judge, web request or reference-file retrieval is involved.

Policy for a new mechanical rule:

- positive example;
- natural negative control;
- boundary example when needed;
- deterministic regression case.

Rules that cannot meet that bar stay in extended/context layers.

## Linter status

`scripts/lint.py` remains the complete surface engine. `scripts/check.py` is the runtime filter.

Only `ARTIFACT` is an automatic publication gate. Other findings remain review candidates.

Current heuristic families include:

- repeated common material in contrasts;
- possessive overexplication;
- repeated explicit context / SVO-lock proxies;
- adjacent context undercompression;
- mechanically parcellated enumerations;
- serial short Q/A punchlines;
- calque phrase families and repeated rhetorical formulas.

## Author profile status

Author adaptation is an internal layer of `humanizer_russian`.

The profiler tracks:

- discourse and self-repair markers;
- content tokens, n-grams and sentence starts;
- code-switching;
- sentence/paragraph distributions;
- punctuation habits;
- contrast and Q/A surface metrics;
- hedge/certainty markers;
- manual annotations for confirmed local, generational, professional, preferred and avoided vocabulary.

Errors remain separate from voice and are not imitated by default.

## Evals

Model/context evals remain useful for genuinely semantic questions, but they are no longer the primary test of linter correctness.

The primary regression signal is the deterministic linter corpus. Model evals cover the residual context-dependent behavior.

## Deliberately not active architecture

- detector-driven hard bans;
- pseudo `AI score` thresholds;
- old sequential pattern lists as authoritative grammar;
- separate product names for Russian/native/author layers;
- deliberate grammatical degradation to look human;
- mandatory loading of all context/reference files;
- model-judge evals as the primary correctness signal.

## Next work

- expand the deterministic corpus before promoting more rules to mechanical mode;
- measure false positives on real native-speaker corpora;
- incorporate philologist feedback;
- analyze additional Russian-language references and licensed editing materials;
- add morphology/coreference tooling where regex is too weak;
- keep model-judge evals only for genuinely semantic/contextual behavior.
