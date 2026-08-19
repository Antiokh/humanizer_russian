# Project status

## 2026-08-19 — independent multi-library editor operational

The active canonical repository is `Antiokh/humanizer_russian`. The project name is **humanizer_russian**.

The repository now combines:

- Russian norm and native-usage layers;
- author-profile adaptation;
- source-specific editorial knowledge libraries for Nora Gal, Chukovsky and Ilyakhov/Sarycheva;
- deterministic compact checking and an Editorial Board runtime;
- optional external-evidence providers separated from reviewer votes;
- deterministic regression suites and CI;
- reproducible but opt-in live-model and NKRЯ research harnesses;
- a blind independent-philologist review protocol.

## Unified architecture

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Consequences:

- an editorial source cannot create a language error merely by authority;
- natural Russian is chosen among normative variants using context and information structure;
- author voice is protected among normative variants;
- detector-style signals are weak and never outrank semantics, norm or source-grounded editing;
- a valid outcome can be **no change**.

## Native-Russian layer

The current native layer is context-first rather than sentence-template-first:

- context economy and safe ellipsis;
- repeated common material factored before synonym substitution;
- Russian morphology allowed to carry relations instead of restoring English-like SVO;
- word order selected by theme/rheme, contrast and strong positions rather than fixed SVO;
- `не X, а Y` remains a normal Russian construction; repetition is reduced only when it adds no function;
- `а`, `но`, `зато` are not mechanically conflated;
- pragmatic particles are preserved by discourse function;
- parcellation is judged by function, not sentence length;
- good natural Russian is a negative control: the editor must be able to leave it alone.

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
python scripts/review.py --format json
```

The board preserves reviewer identity, disagreement and source provenance. `SEMANTICS`, `NORM` and `ARTIFACT` guardrails remain outside stylistic voting. Optional corpus/dictionary/normative evidence is also kept separate from reviewer votes.

## Operational source libraries

### Nora Gal

The full supplied EPUB of «Слово живое и мертвое» was studied sequentially:

- 35/35 EPUB spine documents covered;
- 30/30 content-bearing documents `VERIFIED`;
- 5/5 structural/title documents `NO_OPERATIONAL_CONTENT`;
- inaccessible/unread parts: none;
- source fingerprint and locators retained; the copyrighted book is not stored in the public repository.

Operational routing:

- 42 audited `GAL-*` rules;
- 0 `HARD_GATE`;
- 0 `DEFAULT_MECHANICAL`;
- 3 `EXTENDED_SOFT`;
- 3 `METRIC_ONLY`;
- 36 `MODEL_ONLY`.

The same `review_v1` library feeds compact and board modes.

### Chukovsky

The Chukovsky library remains operational with its audited source registry, extended mechanical candidates and model-only residue. It shares source-neutral phenomena with other libraries where the actual diagnostic question is the same rather than merely similar.

### Ilyakhov / Sarycheva

The Ilyakhov/Sarycheva library is integrated into the same architecture. Its `ILY-M01` nominalization route is `DEFAULT_MECHANICAL`; Gal and Chukovsky routes for the same `editing.action_hidden_in_nominalization` phenomenon remain softer. Default compact therefore exposes only the default-calibrated source, while extended compact may preserve all compatible provenances.

## Deterministic validation

The CI suite currently covers:

- Python compilation;
- architecture and JSON-schema contracts;
- knowledge-library manifests and routing;
- Nora Gal, Chukovsky and Ilyakhov/Sarycheva source/integration validation;
- source-adapter self-tests;
- base compact benchmark and source-specific compact benchmarks;
- source-specific deterministic benchmarks;
- Editorial Board regression and source-specific board integration;
- shared-phenomenon/provenance behavior;
- author-profile schema/privacy regression;
- repository JSON validation;
- offline validation of the live-model harness, NKRЯ replay runner and philologist-review protocol.

These deterministic tests validate software contracts. They do **not** substitute for live model results, corpus measurements or human linguistic review.

## Nora Gal external-evidence calibration

All 15 source-facing `GAL-CLAIM-*` items now have a separate modern evidence disposition in:

- `studies/nora-gal/external-evidence-2026.md`;
- `studies/nora-gal/external-evidence-2026.json`.

The source-facing claims are preserved rather than silently rewritten.

Current important boundaries:

- blanket avoidance of foreign words is not a current norm rule;
- participles/gerunds are normal grammatical resources; register/frequency questions are separate;
- sentence-final focus is not universal; information structure allows other focus positions;
- textual opacity does not license a psychological diagnosis of the author;
- historical claims that machines cannot use contextual literary information are obsolete as present-day absolutes, while literary-translation quality and voice remain real open problems;
- child-language input evidence supports only a narrower developmental claim, not a language-wide moral/historical conclusion;
- source/editorial agreement does not itself create `NORM`.

Claims `GAL-CLAIM-01`, `GAL-CLAIM-03` and `GAL-CLAIM-14` remain explicitly `TESTABLE_NOT_YET_MEASURED` where a real corpus result is required.

## Live model evaluation

`scripts/run_model_evals.py` is the reproducible opt-in harness for contextual/model-only evaluation.

It:

- joins the 45 Nora Gal fixtures to source rule cards;
- does not expose expected answers to the candidate model;
- judges candidate output in a separate structured-output call;
- records candidate/judge model IDs, response IDs and token usage;
- sends `store: false`;
- reads `OPENAI_API_KEY` only from the environment;
- supports dry-run and offline CI self-test.

**No live model benchmark has been executed by the project yet.** This remains open issue #22 and requires explicit API credentials/models plus acceptance of API usage cost.

## Corpus calibration

`studies/nora-gal/corpus-calibration-plan.md` defines the measurement discipline for the remaining empirical claims.

`scripts/run_ruscorpora_query.py` can replay a query exported from the NKRЯ web interface. It does not invent query/subcorpus JSON. Bearer credentials are restricted to the exact official HTTPS NKRЯ lexicogrammatical-concordance endpoint, and returned-page counts are explicitly not treated as prevalence or total corpus hits.

**No live NKRЯ calibration has been executed by the project yet.** Issue #23 requires an NKRЯ API token plus deliberately designed/exported subcorpus queries.

## Independent philologist review

The repository now contains a 28-case external-review protocol covering the highest-risk norm/native/editing boundaries.

The first pass is blind: `scripts/export_philologist_packet.py` removes project positions, rule IDs and phenomenon IDs before the reviewer sees the cases. A completed review has a JSON schema and semantic validation rules; `LANGUAGE_ERROR` requires a normative source, and context-sensitive classifications require a counterexample/boundary.

**No real philologist verdict is stored in the repository yet.** Issue #24 requires a qualified external reviewer. Synthetic validator fixtures are test plumbing only and are not linguistic evidence.

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

## True external blockers / next evidence

The remaining high-value validation work now depends on evidence that the repository cannot fabricate:

1. issue #22 — live contextual model benchmark with explicit API models/key;
2. issue #23 — real NKRЯ corpus measurements with authenticated exported queries;
3. issue #24 — independent qualified philologist review.

After those results exist, integrate them case by case. Only then consider promoting any additional rule from `MODEL_ONLY`/`EXTENDED_SOFT`, changing a normative classification, or adding new mechanical surface proxies.
