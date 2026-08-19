# Project status

## 2026-08-19 — independent repository initialized

The active development base is `Antiokh/humanizer_russian`. The project name is **humanizer_russian**.

Migrated/consolidated from the old `Antiokh/humanizer--ru` development lines:

- Nora Gal semantic editing layer;
- Russian norm layer;
- native-speaker usage layer;
- audit of the inherited humanizer rules;
- evidence audit for AI-writing claims;
- author-profile framework and JSON Schema;
- deterministic surface linter;
- Russian/Nora Gal eval suites;
- Custom GPT instructions/setup/tests;
- owner feedback log;
- CI checks.

## Unified architecture

One project, several internal layers.

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

`NORM` defines what is admissible Russian. `NATIVE_USAGE` selects the form that sounds natural to a native speaker. `AUTHOR` refines that choice when a corpus/profile is available.

## Native-Russian redesign incorporated

- paragraph/context-first editing rather than isolated-sentence rewriting;
- context economy and safe ellipsis;
- repeated common material is factored before synonym substitution;
- Russian morphology is allowed to carry relations instead of restoring English-like SVO;
- word order is chosen by information structure and strong initial/final positions;
- contrast is Russified instead of mechanically split into `Это не X. Это Y.`;
- parcellation is judged by function, not by sentence length;
- pragmatic particles and conversational register are preserved by function;
- anglo-American slogan/Q&A rhetoric is treated as a cluster, not a hard ban;
- good human Russian is a negative eval: no rewrite is a valid result.

## Linter status

`scripts/lint.py` remains a conservative surface linter. Only `ARTIFACT` is gating.

Added soft candidates for:

- repeated common material in contrasts;
- possessive overexplication;
- repeated explicit context / SVO-lock proxies;
- adjacent context undercompression;
- mechanically parcellated enumerations;
- serial short Q/A punchlines;
- calque phrase families and repeated rhetorical formulas.

The linter does not claim to infer grammar, theme/rheme or authorship from regexes.

## Author profile status

Author adaptation is an internal layer of `humanizer_russian`, not a separate product.

The profiler now tracks:

- discourse and self-repair markers;
- content tokens, n-grams and sentence starts;
- code-switching;
- sentence/paragraph distributions;
- punctuation habits;
- contrast and Q/A surface metrics;
- hedge/certainty markers.

Manual annotations are available for confirmed local, generational, professional, preferred and avoided vocabulary. Errors remain separate from voice and are not imitated by default.

## Evals

`evals/russian-language.json` v2 covers 24 native-language scenarios, including context compression, strong edges, real dialogue vs slogan Q/A, register preservation, author annotations and no-op editing of already-good human text.

`gpt/TESTS.md` mirrors the same architecture as smoke tests.

## Deliberately not active architecture

- detector-driven hard bans;
- pseudo `AI score` thresholds;
- old sequential pattern lists as an authoritative grammar;
- separate product names for Russian/native/author layers;
- deliberate grammatical degradation to look human.

## Next work

- incorporate philologist feedback;
- analyze additional Russian-language references and licensed editing materials;
- build a model-judge eval harness;
- add corpus-backed thresholds only after measuring false positives/negatives;
- evolve author profiling toward morphological/coreference analysis without pretending regex proxies are linguistic truth.