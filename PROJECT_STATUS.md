# Project status

## 2026-08-20 — eight-profile multi-library Russian editor operational

The active canonical repository is `Antiokh/humanizer_russian`. The project name is **humanizer_russian**.

The current `main` combines:

- two project-core reviewer profiles: **Russian language / norm and usage** and **Native Russian**;
- six operational author/source libraries: **Nora Gal**, **Ilyakhov/Sarycheva**, **Chukovsky**, **Lynn Visson**, **D. E. Rosenthal**, and **I. B. Golub**;
- the bounded A. V. Velichko RKI/grammar study integrated source-neutrally into the Russian core rather than exposed as a separate reviewer vote;
- deterministic Compact checking and a provenance-preserving Editorial Board runtime;
- optional external-evidence providers kept separate from reviewer votes;
- deterministic regression suites, source-specific validation workflows, and opt-in research harnesses;
- author-profile adaptation and a blind independent-philologist review protocol.

## Unified architecture

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Consequences:

- an editorial source cannot create a language error merely by authority;
- current normative constraints outrank historical or stylistic recommendations;
- natural Russian is chosen among normative variants using context and information structure;
- author voice is protected among normative variants;
- detector-style signals are weak and never outrank semantics, norm or source-grounded editing;
- a valid outcome can be **no change**.

## Runtime

Compact default:

```bash
python scripts/check.py text.md
```

This exposes only high-confidence/default-mechanical findings and technical artifacts from enabled libraries.

Extended compact audit:

```bash
python scripts/check.py --extended text.md
```

This adds lower-confidence mechanical/style candidates. Source-neutral `phenomenon_id` values allow compatible findings from several libraries to deduplicate while preserving provenance.

Editorial Board:

```bash
python scripts/review.py text.md --style neutral
```

The board preserves reviewer identity, disagreement and source provenance. `SEMANTICS`, `NORM` and `ARTIFACT` guardrails remain outside stylistic voting. If author/source conclusions conflict, `SOURCE_CONFLICT` is preserved rather than resolved by choosing one source or averaging them away.

The default board currently has eight profiles:

1. `russian` — current norm, syntax, punctuation, lexical fit, register and RKI-like interference;
2. `native` — contextual economy, ellipsis, information structure and native-usage preferences;
3. `gal` — Nora Gal;
4. `ilyakhov` — Maxim Ilyakhov / Lyudmila Sarycheva;
5. `chukovsky` — Korney Chukovsky;
6. `visson` — Lynn Visson;
7. `rosenthal` — D. E. Rosenthal;
8. `golub` — I. B. Golub.

Author names mean “evaluation by formalized source-derived principles”, not a real review, quotation, endorsement or personal opinion of the author.

## Current source-library snapshot

Exact operational counts live in each `libraries/<id>/library.json`; the current snapshot is:

- **Nora Gal** — 42 audited book-derived rules: 3 `EXTENDED_SOFT`, 3 `METRIC_ONLY`, 36 `MODEL_ONLY`;
- **Ilyakhov/Sarycheva** — 102 audited source rules: 9 `EXTENDED_SOFT`, 4 `METRIC_ONLY`, 89 `MODEL_ONLY`; `ILY-M01` is a separate project-derived `DEFAULT_MECHANICAL` subset rather than a direct author rule;
- **Chukovsky** — 38 audited rules: 7 `EXTENDED_SOFT`, 2 `METRIC_ONLY`, 29 `MODEL_ONLY`;
- **Lynn Visson** — 39 operational rules derived from 72 atomic observations: 2 `DEFAULT_MECHANICAL`, 3 `EXTENDED_SOFT`, 2 `METRIC_ONLY`, 32 `MODEL_ONLY`;
- **Rosenthal** — 74 cumulative rules across four fully read source cycles: 3 `EXTENDED_SOFT`, 1 `METRIC_ONLY`, 70 `MODEL_ONLY`. Cycle 4 adds provenance to existing phenomena rather than duplicate rule IDs or new mechanical detectors;
- **Golub** — 93 deduplicated phenomena from two fully read books coauthored with D. E. Rosenthal: 3 narrow `DEFAULT_MECHANICAL` norm subsets, 1 `EXTENDED_SOFT`, 2 descriptive metrics, 87 contextual rules. The two books form one Golub source school and never become two votes inside that library.

All six author/source libraries are enabled by default and feed the same normalized library runtime.

## Russian core and the Velichko study

The Russian core owns current norm and general Russian-usage rules. Normative findings may become guardrails; native-usage, register, RKI-like interference and calque findings remain non-blocking unless independently confirmed as `NORM`.

The available 2004 Velichko fragment was studied as a bounded source and integrated into this core. Its useful grammar/RKI observations cover, among other things, valency and government, subject realization, event construal and aspect, passive/result-state distinctions, copular choice, participles, gerunds, quantitative agreement and introductory-word scope.

Velichko is deliberately **not** a ninth reviewer: the study contributes source-neutral Russian-core knowledge. Unavailable source chapters are not reconstructed or claimed as covered.

## Native-Russian layer

The native layer is context-first rather than sentence-template-first:

- context economy and safe ellipsis;
- repeated common material factored before synonym substitution;
- Russian morphology allowed to carry relations instead of restoring English-like SVO;
- word order selected by theme/rheme, contrast and strong positions rather than fixed SVO;
- `не X, а Y` remains a normal Russian construction; repetition is reduced only when it adds no function;
- pragmatic particles are preserved by discourse function;
- parcellation is judged by function, not sentence length;
- good natural Russian is a negative control: the editor must be able to leave it alone.

## Source accumulation and deduplication

Long-lived author branches remain the research branches for additional sources by the same author/school. New books do not automatically create new reviewer identities.

When a later source repeats an existing phenomenon:

- preserve the new source locator/provenance;
- reuse the source-neutral `phenomenon_id` where the diagnostic question is genuinely the same;
- do not duplicate mechanical detectors merely because another book states the same rule;
- preserve `SOURCE_CONFLICT` when sources truly disagree;
- never promote a historical prescription to current `NORM` by source authority alone.

Rosenthal is the clearest current example: four source cycles feed one long-lived library, while later cycles can enrich provenance without multiplying runtime rules.

Golub is similarly deduplicated across two coauthored books; shared mechanical surfaces with Rosenthal are factored into common Russian-norm surface logic rather than copied independently per author.

## Deterministic validation

Repository validation is split between the base `quality` workflow and focused source workflows.

The current workflow set includes:

- base architecture/library/JSON validation and Compact/Editorial Board regressions;
- bounded Velichko integration validation;
- Gal, Chukovsky and Ilyakhov source/library benchmarks in the base quality workflow;
- dedicated `visson-quality`, `rosenthal-quality` and `golub-quality` workflows;
- separate external-evidence workflows where configured for Chukovsky and Ilyakhov;
- offline tests for the live-model harness, NKRЯ replay runner and philologist-review protocol.

These deterministic tests validate software and study contracts. They do **not** substitute for live model results, corpus measurements or independent human linguistic review.

## External evidence and open blockers

Optional corpus, dictionary and normative-reference evidence is kept separate from reviewer votes. Evidence can support, weaken or contextualize a claim; it does not become an additional member of the Editorial Board.

Three explicit external-validation issues remain open:

1. **#22** — run the live Nora Gal contextual/model benchmark with explicit API models and credentials;
2. **#23** — run real NKRЯ corpus calibration for the remaining Gal empirical claims using authenticated exported queries and validated denominators;
3. **#24** — obtain an independent qualified philologist review of the Russian-language boundary cases.

Until those are completed, the project must not claim live-model calibration, completed NKRЯ measurement for those claims, or external philologist validation.

## Author profile

Author adaptation remains an internal layer. The profiler tracks discourse/self-repair markers, content n-grams, sentence starts, code-switching, sentence/paragraph distributions, punctuation habits, stance markers and explicit manual annotations.

Errors remain separate from voice and are not imitated by default. Source paths are not emitted by the canonical profile output.

## Deliberately not active architecture

- detector-driven hard bans;
- pseudo `AI score` thresholds;
- grammatical degradation to look human;
- historical editorial authority promoted directly to `NORM`;
- automatic stop-word deletion;
- one universal SVO/word-order template;
- blanket bans on passive, participles, gerunds, borrowings, long sentences, rhetorical questions or parcellation;
- majority vote of editorial sources treated as linguistic truth;
- model-judge evals treated as the primary deterministic correctness signal;
- corpus page counts treated as prevalence without a validated denominator.

The next high-value progress is therefore not another generic style heuristic. It is either a carefully integrated new source cycle or one of the three real external-validation steps above.
