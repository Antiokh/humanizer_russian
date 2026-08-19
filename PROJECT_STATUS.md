# Project status

## 2026-08-19 — independent repository initialized

The active development base is now `Antiokh/humanizer_russian` (project name: **humanizer+ru**).

Migrated/consolidated from the old `Antiokh/humanizer--ru` development lines:

- Nora Gal semantic editing layer;
- Russian norm layer;
- native-speaker usage layer;
- audit of the inherited 34 humanizer rules;
- evidence audit for AI-writing claims;
- author-profile framework and JSON Schema;
- deterministic surface linter;
- Russian/Nora Gal eval suites;
- Custom GPT instructions/setup/tests;
- owner feedback log;
- CI checks.

## Architecture at migration

Hard constraints:

`SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

## Review fixes incorporated

- preserve document boundaries in author profiling;
- do not emit corpus filesystem paths;
- use one canonical profile v1 schema;
- validate generated profiles in CI;
- keep `NATIVE_WARNING` non-gating;
- support repeated-common-material candidates with both `а` and `но`;
- document current `ru-01` — `ru-21` eval coverage;
- correct source mapping for zero-subject/ellipsis claims.

## 2026-08-19 — deep Nora Gal audit

The owner supplied an electronic text of Nora Gal's *Slovo zhivoe i mertvoe*. The source has now been analyzed as an editorial work rather than reduced to the original six coarse `SEM-*` patterns.

### Source-grounded structure

Completed:

- `references/nora-gal-source-map.md` — chapter-level provenance and transferability map;
- `references/nora-gal-source-labels.md` — exact internal ebook chapter labels, separate from typographically normalized display names;
- `references/nora-gal-rule-index.md` — 42 atomic `GAL-*` rules with source chapter, scope and derivation status;
- `references/nora-gal.md` — operational deep-editing rules;
- `evals/nora-gal.json` v2 — 45 functional scenarios;
- `evals/nora-gal-map.json` v2 — explicit `eval → rule → source chapter` mapping;
- complete eval coverage for all 42 atomic rules;
- more than ten explicit counterexamples protecting contextual rules from becoming stop-lists;
- `scripts/validate_nora_gal.py` — deterministic structural/traceability validator;
- CI invocation for the validator;
- deep Nora behavior integrated into `SKILL.md`, Custom GPT instructions/setup, evidence policy and manual smoke tests.

### What the deeper layer now covers

Beyond the original six coarse patterns:

- action hidden by nominalization;
- noun chains and agent visibility;
- event order;
- pseudoformal register and empty stamps;
- lexical precision, collocation and concrete wording without invention;
- borrowings and terms by audience rather than blacklist;
- persona, situation, age, era/culture and emotional tact;
- idiom contamination, literalization, polysemy and accidental sound effects;
- physical plausibility and speakability;
- Russian syntax, explicitness, focus, sentence boundaries and pace;
- subtext restraint;
- whole-before-detail, character continuity and POV;
- verification of doubtful references instead of guessing;
- editor-not-dictator, third-solution and self-edit behavior;
- compound failures where several problems must be solved jointly.

### Source policy

The electronic source does not provide a sufficiently trustworthy basis to assert an exact print-edition identity. Repository references therefore use **section/chapter titles**, not unstable ebook page numbers or an unverified print year.

No long passages from the book are copied into the repository. Project rules, explanations and eval prompts are original formulations; the source is used for method and provenance.

### Important non-rules preserved

The deep audit explicitly rejects these possible overgeneralizations:

- foreign word = error;
- passive = error;
- participle/gerund = error;
- long sentence = error;
- important information must always be sentence-final;
- unusual idiom = error;
- editor's preferred replacement = mandatory.

Most `GAL-*` findings remain contextual. They are not new regex gates.

## Deliberately not migrated as active architecture

- old sequential `patterns.md` as an authoritative rule set;
- detector-driven hard bans;
- pseudo `AI score` thresholds;
- old fork-specific changelog/history;
- decorative binary assets from the old repository.

The old materials remain available in the historical repository/PRs. If any old rule is reintroduced, it should first be reclassified under the new taxonomy and supported by an appropriate source or corpus test.

## Next work

- validate CI on the deep Nora Gal pull request;
- review CodeRabbit feedback on the new source-grounded layer;
- expand compound/paragraph-level Gal evals beyond single sentences;
- build/run a model-judge harness for `gal-01` — `gal-45` instead of relying only on fixture validation;
- add corpus-backed `NATIVE_USAGE` tests;
- incorporate philologist feedback;
- analyze additional Russian-language references and the user's licensed editing materials;
- evolve `humanizer+ru+user` beyond regex proxies toward morphological/corpus analysis;
- if needed, later map ebook chapter locators to a verified physical edition without changing rule IDs.
