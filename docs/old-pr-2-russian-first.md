# Old PR #2 — Russian-first / native-usage architecture

Historical source: `Antiokh/humanizer--ru` PR #2, `Rebuild humanizer as Russian-first editor (humanizer+ru)`.

The branch became the staging ground for the independent `humanizer_russian` repository. It is intentionally not merged into `humanizer--ru/main`.

## Architecture carried forward

Hard constraints:

`SEMANTICS + NORM`

Selection among valid forms:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

The central split is between:

- **NORM** — what is valid/correct Russian;
- **NATIVE_USAGE** — which valid wording sounds natural to a native speaker in the given context;
- **AUTHOR** — how a specific person actually writes, derived from a corpus.

## Native-usage work carried forward

### Contextual economy

Russian does not need every sentence to repeat all recoverable context.

Examples:

- `— Кого любит Паша? — Машу.`
- `Первый вариант дорогой. Второй — быстрее.`
- zero/implicit subject when unambiguous.

### Repetition and common-material factoring

A grammatically valid sentence may still sound synthetic:

> Это не ошибка в расчёте, а ошибка в исходных данных.

Neutral native compression:

> Это ошибка не в расчёте, а в исходных данных.

Likewise:

> Мы не меняем цену, а меняем условия.

→

> Мы меняем не цену, а условия.

The rule is not “never repeat”. Intentional repetition such as `Никогда. Никогда больше.` is preserved.

### Information structure

Word order is selected from theme/rheme, prior context and intended focus rather than mechanically preserving English SVO or randomly varying syntax.

Both beginning and ending can be strong positions depending on the discourse move.

### Russian contrast

`не X, а Y`, `не только X, но и Y`, `X, но Y` are not hard-banned. The editor checks:

- whether the second part adds real semantic contrast/gain;
- whether repeated common material can be factored;
- whether the resulting word order matches the intended focus.

### Punctuation

Normative em dashes, colons, rhetorical questions and meaningful parcellation are not deleted for detector score.

## Old 34-rule audit

The active project moved the inherited rules into `references/rule-audit.md` and reclassified them rather than preserving a flat detector-driven list.

Notable changes:

- negative parallelism hard ban removed;
- rule of three becomes cluster-only warning;
- real hedging is preserved;
- stop-words are review triggers, not deletion commands;
- technical jargon is audience-dependent;
- short sentences/parcellation are checked by function;
- repeated verbs do not force synonym cycling;
- explicit paragraph connectors are not mandatory.

## Evidence audit

`references/evidence-audit.md` separates:

- normative claims;
- limited empirical findings;
- editorial heuristics;
- unsupported hypotheses.

Unsupported pseudo-precision from the old approach is not carried forward as active logic: fixed “burstiness” thresholds, bold-density rules, compulsory informal openings and detector-derived AI scores.

## Author profile work

The old branch introduced the first `humanizer+ru+user` tooling. It was reviewed and corrected before migration.

Current implementation:

- `scripts/profile_author.py`;
- `profiles/schema.json`;
- `references/author-profile.md`.

The generated v1 profile:

- preserves document boundaries;
- never creates n-grams across source files;
- does not expose raw filesystem paths;
- uses one strict schema shared by profiler, docs and CI;
- keeps observed errors separate from style;
- defaults to `imitate_errors=false`.

## CodeRabbit findings incorporated

Useful findings from the old PR review were verified and fixed:

1. **Document-boundary bug** — fixed by per-document sentence/n-gram aggregation.
2. **Schema drift** — fixed with one canonical profile v1 contract.
3. **Filesystem path leakage** — removed from generated profiles.
4. **`NATIVE_WARNING` accidentally treated as blocking** — corrected; it is always contextual.
5. **`а` only in repeated-common-material detection** — extended to a bounded `но` candidate and self-test.
6. **Eval documentation still said 18 scenarios** — updated to `ru-01` — `ru-21`.
7. **Unrelated RusGram citation** — replaced and the claim narrowed to distinguish zero subjects from ellipsis.
8. **Linter output contract missing `NATIVE_WARNING`** — now documented in README/skill/docs.

One automated suggestion about GPT availability was rejected after checking first-party product documentation; product availability is not frozen into the language architecture.

## Linter carried forward

The independent `scripts/lint.py` is a conservative surface linter.

Only reliable `ARTIFACT` findings affect its default exit status.

`NATIVE_WARNING`, `AI_PATTERN` and `STYLE_WARNING` are candidates requiring contextual review.

## Evals carried forward

`evals/russian-language.json` contains `ru-01` — `ru-21`, covering:

- normative contrast;
- semantic gain;
- colon/enumeration;
- ellipsis;
- theme/rheme;
- strong initial focus;
- SVO lock;
- possessive calques;
- particles;
- dangling gerunds;
- good/bad parcellation;
- rhetorical questions;
- jargon by audience;
- author errors;
- repeated noun/verb factoring;
- marked two-edge focus.

## Why the old PR is closed instead of merged

The work has become a separate project. Merging it into `humanizer--ru` would defeat the new separation: the old repository should remain a small compatibility fork, while `Antiokh/humanizer_russian` becomes the active development base.

Closing the old PR keeps CodeRabbit comments, diffs and history available as review provenance without changing the old `main`.
