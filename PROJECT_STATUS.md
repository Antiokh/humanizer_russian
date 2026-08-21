# Project status

## 2026-08-21 — eight-profile Russian editor operational

Canonical repository: `Antiokh/humanizer_russian`.

Volatile inventory facts are generated from repository manifests and rule indexes. See [`docs/capabilities.md`](docs/capabilities.md) for the human-readable snapshot and [`docs/capabilities.json`](docs/capabilities.json) for the machine-readable form. `scripts/validate_libraries.py` fails CI when those checked-in generated files drift from their sources.

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

All operational libraries use the normalized `review_v1` runtime contract. Exact enabled-library/reviewer inventory is generated in the capability snapshot rather than copied here.

## Runtime precision

Compact deduplication preserves the strongest compatible guardrail/severity and is order-invariant. Normalized findings are validated against one contract for project class, automation level, verdict and hard-gate legality before they can enter Compact or Board.

Russian prose-oriented mechanical checks share a length-preserving masker for fenced code, inline code, URLs, Markdown link targets and HTML comments. This keeps line/span mapping stable while preventing prose rules from firing solely on non-prose payloads.

## Russian core and Velichko

The Russian core owns current norm and general Russian-usage rules. Normative findings may become guardrails; native-usage, register, RKI-like interference and calque findings remain non-blocking unless independently established as `NORM`.

The A. V. Velichko study is **complete for the source supplied to the project**. The supplied file contains the introduction and chapter bodies 1–13; its table of contents advertises later chapters whose bodies are absent from that file. The study verified 100% of the physically available fragment and did not reconstruct missing material from headings alone.

If a legitimately obtained fuller source is supplied later, that is a new source cycle rather than unfinished work in the current study. Velichko contributes source-neutral Russian/RKI knowledge and is not an additional Editorial Board reviewer.

## Source libraries

Author/source libraries remain separate from current norm. New books in the same school enrich one long-lived library rather than creating extra votes. Repeated mechanisms reuse source-neutral `phenomenon_id` values where appropriate; new source locators are preserved as provenance.

Do not copy numeric inventories into this document. Current rule counts, automation distributions, source-cycle counts exposed by indexes, adapters and model-eval registration are generated in [`docs/capabilities.md`](docs/capabilities.md).

Source completeness is not inferred from rule counts. Where a library manifest explicitly records `source_status`, the generated JSON snapshot preserves that statement verbatim.

## Contextual model evals

`scripts/run_model_evals.py` is a manifest-driven, opt-in harness for contextual rules. Candidate and judge roles are separated; candidate prompts do not receive expected answers or counterexample labels. Live API calls remain outside CI.

All intended author/source libraries with model-eval support are now registered in the generic harness; the exact set is generated in the capability snapshot. Visson's older positive/negative/boundary research fixture remains separate from its project-authored runtime prompt suite rather than being special-cased in the generic harness.

A green model run is calibration evidence only. It cannot create current `NORM`, `HARD_GATE` or a mechanical rule by itself.

## Evidence providers

Evidence is kept separate from reviewer opinion. Provider state is generated in [`docs/capabilities.md`](docs/capabilities.md).

All currently unfinished provider families are explicitly `PROJECT`: they remain visible as roadmap scaffolds but are not runtime-selectable. `--evidence auto` and `--evidence all` consider only `OPERATIONAL` providers, and an explicit attempt to select a `PROJECT` provider is rejected rather than simulated as an unavailable feature.

The next evidence milestone is #49: promote one real, versioned, opt-in current normative-reference provider to `OPERATIONAL` only after its source, rights/terms, version/provenance, query contract and calibration are real. A frequency or corpus signal cannot substitute for normative evidence.

## Validation still requiring external resources

These are genuine external-validation tasks rather than unfinished repository plumbing:

1. **#22** — execute live contextual/model calibration using explicit API models and credentials;
2. **#23** — run the planned authenticated NKRЯ calibration for the remaining empirical Gal claims with exported queries and validated denominators;
3. **#24** — obtain an independent qualified philologist review of the prepared Russian-language boundary cases.

Until they are completed, the project must not claim live-model validation, completed NKRЯ measurement for those claims or independent philologist validation.

## Internal work still open

- **#49** — first operational current normative-reference evidence provider;
- **#58** — document-level preservation corpus and audited false-positive/noise baseline for realistic multi-paragraph texts.

Recent runtime hardening has already completed the former tails around prose masking, Compact severity/deduplication, normalized finding validation, Native `review_v1` migration and Visson/Rosenthal generic model-eval registration. Their implementation history remains in the corresponding closed issues and merged PRs rather than being duplicated here.

The next high-value internal step is #58: measure aggregate behavior on realistic good Russian before adding more mechanical heuristics.
