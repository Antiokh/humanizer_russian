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

## Nora Gal knowledge library

The full supplied EPUB of Nora Gal's «Слово живое и мертвое» has been studied sequentially and integrated as the long-lived `gal` source library rather than as a second humanizer.

Source gate:

- 35/35 EPUB spine documents covered;
- 30/30 content-bearing documents `VERIFIED`;
- 5/5 structural/title documents `NO_OPERATIONAL_CONTENT`;
- inaccessible/unread parts: none;
- exact source fingerprint and chapter locators retained in the public derived study; the copyrighted book itself is not stored in the repository.

Operational routing:

- 42 audited `GAL-*` rules;
- 0 `HARD_GATE`;
- 0 `DEFAULT_MECHANICAL`;
- 3 `EXTENDED_SOFT`;
- 3 `METRIC_ONLY`;
- 36 `MODEL_ONLY`.

The library uses `review_v1` once for both compact and Editorial Board modes. Shared source-neutral phenomena are reused with Chukovsky for hidden action/nominalization, empty templates, terminology/audience fit and idiom play vs contamination. Related-but-not-identical mechanisms remain separate.

The deterministic PR suite passed architecture/schema validation, the Gal source validator, Gal linter self-test, 34/34 base compact cases, 5/5 Gal compact integration cases, 26 Gal source cases, 10 base board cases, 7 Gal board cases, shared Gal/Chukovsky compact deduplication and board provenance smoke tests. The library manifest is therefore `OPERATIONAL` for integration; contextual MODEL_ONLY behavior still requires real model evaluation in a later cycle.

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

`scripts/lint.py` remains the complete core surface engine. Source libraries add normalized source-specific adapters; `scripts/check.py` is the compact runtime filter.

Only `ARTIFACT` is an automatic publication gate. Other findings remain review candidates unless independently justified otherwise.

Current heuristic families include:

- repeated common material in contrasts;
- possessive overexplication;
- repeated explicit context / SVO-lock proxies;
- adjacent context undercompression;
- mechanically parcellated enumerations;
- serial short Q/A punchlines;
- calque phrase families and repeated rhetorical formulas;
- source-specific extended checks from operational knowledge libraries.

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

- run real model evaluations for Gal's 36 `MODEL_ONLY` rules and preservation cases;
- externally verify historical/corpus/normative claims before any promotion outside `EDITING`;
- expand the deterministic corpus before promoting more rules to mechanical mode;
- measure false positives on real native-speaker corpora;
- incorporate philologist feedback;
- analyze additional Russian-language references and licensed editing materials;
- add morphology/coreference tooling where regex is too weak;
- keep model-judge evals only for genuinely semantic/contextual behavior.
