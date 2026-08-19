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

## Deliberately not migrated as active architecture

- old sequential `patterns.md` as an authoritative rule set;
- detector-driven hard bans;
- pseudo `AI score` thresholds;
- old fork-specific changelog/history;
- decorative binary assets from the old repository.

The old materials remain available in the historical repository/PRs. If any old rule is reintroduced, it should first be reclassified under the new taxonomy and supported by an appropriate source or corpus test.

## Next work

- validate CI on the independent repository;
- expand corpus-backed `NATIVE_USAGE` tests;
- incorporate philologist feedback;
- analyze additional Russian-language references and the user's licensed editing materials;
- build a model-judge eval harness;
- evolve `humanizer+ru+user` beyond regex proxies toward morphological/corpus analysis.
