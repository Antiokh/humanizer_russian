# Project status

`humanizer_russian` is an operational Russian-language editing system with two product modes over one shared set of knowledge libraries: fast mechanical Compact checking and provenance-preserving Editorial Board review.

Volatile inventory facts are generated from repository manifests and rule indexes instead of being maintained in this document by hand:

- human-readable snapshot: [`docs/capabilities.md`](docs/capabilities.md);
- machine-readable snapshot: [`docs/capabilities.json`](docs/capabilities.json);
- generator/checker: [`scripts/generate_capabilities.py`](scripts/generate_capabilities.py).

`python scripts/validate_libraries.py` fails when the checked-in snapshot no longer matches the manifests, rules or evidence-provider states.

## Core policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among valid variants:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Consequences:

- editorial authority does not create a language error by itself;
- current norm outranks historical or stylistic advice;
- native usage and information structure select among normative variants;
- author voice is protected among normative variants;
- detector-like signals are diagnostics, not optimization targets;
- **no change** is a valid result.

## Product modes

Compact:

```bash
python scripts/check.py text.md
python scripts/check.py --extended text.md
python scripts/check.py --register everyday text.md
```

Default Compact exposes only `HARD_GATE` and `DEFAULT_MECHANICAL` findings. `--extended` adds explicitly allowed lower-confidence mechanical/style candidates; metric-only and model-only signals are not leaked into that surface.

Editorial Board:

```bash
python scripts/review.py text.md --style neutral
```

Board preserves reviewer identity, provenance and real disagreement. `NORM` and technical artifact guardrails remain outside stylistic voting. Evidence providers are a separate axis and never become reviewer votes.

The exact current set of enabled profiles, adapters, rule counts, automation levels and model-eval registrations is generated in [`docs/capabilities.md`](docs/capabilities.md).

## Runtime architecture

All operational knowledge libraries now use the normalized `review_v1` contract. The shared runtime validates finding values at the library boundary rather than accepting unknown classes, automation levels or verdicts and silently downgrading them.

Compact deduplication is severity-aware and deterministic. Compatible findings on the same phenomenon/surface retain complete provenance while a stronger guardrail cannot be hidden by library order. CLI blocking behavior is derived from normalized project classes rather than legacy display labels.

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

The next evidence milestone is #49: activate one real, versioned, opt-in current normative-reference provider with explicit provenance and fail-open behavior. A frequency or corpus signal cannot substitute for normative evidence.

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
