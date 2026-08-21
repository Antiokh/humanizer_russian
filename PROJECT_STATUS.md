# Project status

## 2026-08-21 — eight-profile Russian editor operational

Canonical repository: `Antiokh/humanizer_russian`.

Current audited `main` before this documentation refresh: `c108a44794742f617ef91de1989cf7552d7ce463`.

The project currently combines:

- two project-core profiles: **Russian language / norm and usage** and **Native Russian**;
- six author/source libraries: **Nora Gal**, **Ilyakhov/Sarycheva**, **Chukovsky**, **Lynn Visson**, **D. E. Rosenthal**, **I. B. Golub**;
- the bounded A. V. Velichko RKI/grammar study integrated source-neutrally into the Russian core;
- deterministic Compact checking and provenance-preserving Editorial Board review;
- opt-in model-eval infrastructure for contextual rules;
- optional evidence-provider architecture kept separate from reviewer votes;
- deterministic source/library validation, preservation tests and external-review/corpus protocols.

## Core policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Consequences:

- editorial authority cannot create a language error by itself;
- current norm outranks historical or stylistic advice;
- native usage and information structure select among normative variants;
- author voice is protected among normative variants;
- detector-like signals remain weak diagnostics;
- **no change** is a valid result.

## Product modes

Compact:

```bash
python scripts/check.py text.md
python scripts/check.py --extended text.md
python scripts/check.py --register everyday text.md
```

Default Compact exposes only `HARD_GATE` and `DEFAULT_MECHANICAL` findings. `--extended` adds lower-confidence non-model mechanical/style candidates.

Editorial Board:

```bash
python scripts/review.py text.md --style neutral
```

Board preserves reviewer identity, provenance and disagreement. `SEMANTICS`, `NORM` and `ARTIFACT` guardrails stay outside stylistic voting. Real author/source disagreement remains `SOURCE_CONFLICT` rather than being averaged away.

Default profiles:

1. `russian` — current norm, syntax, punctuation, register and RKI-like interference;
2. `native` — contextual economy, ellipsis, information structure and native-usage preferences;
3. `gal` — Nora Gal;
4. `ilyakhov` — Maxim Ilyakhov / Lyudmila Sarycheva;
5. `chukovsky` — Korney Chukovsky;
6. `visson` — Lynn Visson;
7. `rosenthal` — D. E. Rosenthal;
8. `golub` — I. B. Golub.

Author names mean evaluation by formalized source-derived principles, not a personal review, quotation or endorsement.

## Source-library snapshot

Exact canonical counts live in library/source indexes. Current audited snapshot:

- **Nora Gal** — 42 audited book-derived rules: 3 `EXTENDED_SOFT`, 3 `METRIC_ONLY`, 36 `MODEL_ONLY`;
- **Ilyakhov/Sarycheva** — 102 audited source rules: 9 `EXTENDED_SOFT`, 4 `METRIC_ONLY`, 89 `MODEL_ONLY`; `ILY-M01` is a separate project-derived default-mechanical subset;
- **Chukovsky** — 38 audited rules: 7 `EXTENDED_SOFT`, 2 `METRIC_ONLY`, 29 `MODEL_ONLY`;
- **Lynn Visson** — 39 operational rules from 72 atomic observations: 2 `DEFAULT_MECHANICAL`, 3 `EXTENDED_SOFT`, 2 `METRIC_ONLY`, 32 `MODEL_ONLY`;
- **Rosenthal** — **79 cumulative rules across six fully processed source cycles**: 3 `EXTENDED_SOFT`, 1 `METRIC_ONLY`, 75 `MODEL_ONLY`. Cycle 6 added one contextual AUTHOR rule (`ROS-R79`) and 64 provenance enrichments, with no new mechanical detector;
- **Golub** — 93 deduplicated phenomena from two fully processed coauthored books: 3 narrow `DEFAULT_MECHANICAL` norm subsets, 1 `EXTENDED_SOFT`, 2 metrics, 87 contextual rules.

All six author/source libraries are enabled by default and use the normalized library runtime. The `native` project-core library still uses the legacy compatibility adapter; migration is tracked separately.

## Russian core and Velichko

The Russian core owns current norm and general Russian-usage rules. Normative findings may become guardrails; native-usage, register, RKI-like interference and calque findings remain non-blocking unless independently confirmed as `NORM`.

The available Velichko source was incomplete. The physically present chapters 1–13 were studied and integrated; chapter bodies 14–44 were absent and are not reconstructed. The missing source boundary is now tracked explicitly rather than implied as full-book coverage.

The integrated material contributes source-neutral contextual knowledge about valency/government, subject realization, event construal/aspect, passive/result-state distinctions, copular choice, participles, gerunds, quantitative agreement and introductory-word scope.

Velichko is not a ninth reviewer.

## Native-Russian layer

The native layer is context-first:

- safe ellipsis and context economy;
- factoring repeated common material before synonym substitution;
- morphology allowed to carry relations instead of restoring English-like SVO;
- word order by theme/rheme and contrast rather than a universal SVO template;
- functional repetition and particles preserved;
- participles/gerunds treated as normal Russian resources;
- good natural Russian is a negative control and may be left unchanged.

## Calques and event structure

The Russian layer includes a narrow `break → ломаться` model. It distinguishes pre-failure process, event boundary and result rather than treating `ломается` as a general equivalent of English `is breaking`. These findings remain `REVIEW`, not hard language errors.

A repository audit found that the calque sub-linter currently scans raw text rather than a shared prose-masked view; code/Markdown masking is tracked as an explicit bug tail.

## Source accumulation and deduplication

Long-lived author/source branches accumulate later books from the same school. New books do not create extra reviewer votes automatically.

When a later source repeats an existing phenomenon:

- preserve new source locator/provenance;
- reuse the source-neutral `phenomenon_id` when the diagnostic mechanism is genuinely the same;
- do not duplicate mechanical detectors;
- preserve actual `SOURCE_CONFLICT`;
- never promote historical prescription to current `NORM` by authority alone.

Rosenthal is now the strongest example: six source cycles feed one 79-rule library. Golub similarly deduplicates two books into one source school.

## Contextual/model evals

`scripts/run_model_evals.py` is manifest-driven. Candidate and judge are separated; candidate prompts do not receive expected answers. Live API calls remain opt-in and are not CI dependencies.

Current audit tail: Visson has an eval suite and map artifact but is missing the manifest map key required for discovery; Rosenthal has substantial contextual eval material but no runtime model-eval manifest contract yet. This is tracked in #48.

A green model run is calibration evidence only. It cannot create current `NORM`, `HARD_GATE` or a mechanical rule by itself.

## Evidence providers

Evidence is a separate axis, not a reviewer vote. Architecture exists for current usage, spoken Russian, discourse lexicon, normative reference and parsed Russian, with strict timeout/fail-open/default-off behavior.

The provider families are still planned rather than operational. The recommended first real provider is a versioned current normative-reference source because historical editorial libraries repeatedly need modern norm verification. Tracked in #49 and cross-library contract work in #26.

## External validation blockers

Three pre-existing external-validation issues remain genuinely open:

1. **#22** — run live contextual/model calibration with explicit API models and credentials;
2. **#23** — run real NKRЯ calibration for remaining Gal empirical claims with exported authenticated queries and validated denominators;
3. **#24** — obtain independent qualified philologist review of the Russian-language boundary cases.

Until completed, the project must not claim live-model validation, completed NKRЯ measurement for those claims or independent philologist validation.

## Audit tails opened 2026-08-21

- **#48** — register Visson and Rosenthal in the generic model-eval harness;
- **#49** — activate the first real opt-in normative evidence provider;
- **#50** — extend the bounded Velichko study when missing chapters are legitimately available;
- **#51** — synchronize long-lived source branches and prune obsolete merged refs;
- **#52** — derive volatile public capability snapshots from manifests to stop documentation drift;
- **#53** — mask code/structural Markdown before Russian calque/event-structure checks;
- **#54** — migrate `native` from `legacy_lint_v1` to `review_v1` after parity testing.

Roadmap #26 was also refreshed: generic model eval is now marked completed; cross-library evidence contract remains open.

## Branch state discovered by audit

At audited main `c108a447...`:

- `rosenthal` was identical to main;
- `golub` was behind 48 commits;
- `velichko` behind 83;
- `visson` behind 137;
- `ilyakhov` behind 146;
- `chukovsky` behind 158;
- `gal` behind 168;
- all were ahead by 0.

This is not lost work—the source changes are merged into main—but it leaves long-lived source branches stale for the next cycle. Cleanup/synchronization is #51.

## Deliberately not active architecture

- detector-driven hard bans or pseudo AI scores;
- grammatical degradation to look human;
- historical editorial authority promoted directly to `NORM`;
- blanket bans on passive, participles, gerunds, borrowings, long sentences, rhetorical questions or parcellation;
- majority vote of editorial sources treated as linguistic truth;
- model judges treated as primary deterministic correctness signals;
- corpus page counts treated as prevalence without a validated denominator.

## Recommended priority

1. Fix #53 first: it is a direct false-positive risk in default mechanical output.
2. Close #48: the generic model-eval architecture already exists; this is bounded integration debt.
3. Complete #26 item 4 and #49 together if a minimal evidence contract emerges naturally.
4. Do #51 branch hygiene before the next source-book cycle.
5. Do #54 as architecture cleanup after behavior is frozen by parity tests.
6. #50 depends on obtaining the missing legitimate source; do not block other work on it.

The next high-value progress is hardening precision and reproducibility, not adding generic stylistic heuristics.