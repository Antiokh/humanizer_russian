# Integration Gate A audit

This audit is performed before changing runtime behavior. The primary source remains the user-provided EPUB; the committed study is treated as a derived model, not as proof that old regexes or project rules are correct.

## Study status

The source model passes the structural completion gate:

- 211 / 211 NCX nodes accounted for;
- 177 / 177 leaf sections read sequentially;
- unread or inaccessible source sections: 0;
- 26 concepts;
- 102 atomic operational rules;
- 30 counterexample classes with every rule mapped;
- 32 source claims isolated from operational rules;
- 17 cross-rule interactions;
- 67 original eval cases with every rule covered;
- explicit loss audit and overgeneralization audit.

`coverage.md`, `rules-*.md`, `counterexamples-claims.md`, `interactions.md`, `evals-*.md` and `audit.md` therefore remain the provenance layer for this integration.

## What was rechecked against the primary source

The already completed sequential reading is not replaced by semantic search. During this integration pass the source-derived model was rechecked against the source passages already available in the conversation, especially the sections that constrain mechanical application:

1. `Слушайте себя`: formal rule application may create unnatural, synthetic prose; naturalness and meaning are final constraints.
2. The comma/syntax discussion: sentence difficulty is addressed by restructuring syntax, not by deleting normative punctuation.
3. Homogeneous members: close synonyms may be redundant, but diagnostically distinct or specialist lists are explicitly preservable.
4. New entities: reader preparation matters; the source does not justify a universal numeric “one thought” threshold.
5. Product-writing rules: the authors explicitly frame their five-rule scheme as their systematization rather than final truth.
6. Job applications: even a strong application does not guarantee a reply; uncontrollable external causes remain.
7. `Дело не в словах`: mindless copying of informational-style formulas is itself a failure.

No new source gap was found. Exact print-equivalent edition metadata remains unknown and is still marked as a bibliographic gap rather than guessed.

## Provenance audit

The study keeps source statements separate from project refinements. The main integration risk is not missing provenance but **promotion**: a source heuristic can be mistakenly upgraded to a language norm or deterministic error.

The following boundaries are mandatory:

- no book-derived rule becomes `NORM` merely because the book states it;
- no book-derived pattern becomes evidence of AI authorship;
- source claims about cognition, buying, reading, HR behavior, punctuation difficulty or media hierarchy stay in the claims audit unless independently verified;
- `SOURCE_EXAMPLE_ONLY` material is not generalized without a project-derived guard;
- project-derived mechanical subsets must be named as project operators and linked back to source rules without being attributed verbatim to the authors.

## Audit of the old `ilyakhov` runtime layer

The previous author branch is useful as historical implementation evidence, but its regexes are not accepted automatically.

Problems found in the old source-specific linter:

- all occurrences of cognitive frames such as `я считаю, что` could be flagged even when they preserve attribution or uncertainty;
- broad nominalization patterns could hit ordinary Russian such as `провести исследование`;
- state-predicate clusters could treat normal definitions/states as defects;
- long-correlative character thresholds were implementation heuristics, not source-backed linguistic thresholds;
- generic intros, conclusions and praise are strongly genre-dependent;
- old self-tests did not provide a complete TP / natural-negative / boundary / intentional-use contract for every default-capable rule.

These old checks are candidates only. The current `main` architecture and `NATIVE_USAGE` layer govern the new implementation.

## Atomic-rule audit result

The 102 `PS-R*` units are sufficiently atomic for integration. Some source rules contain a mechanically detectable **subset** and a larger contextual remainder. The integration matrix therefore classifies the full source rule conservatively and, where useful, derives a narrower project operator. This avoids falsely declaring the whole source rule deterministic.

Example: `PS-R22` / `PS-R29` motivate checking bureaucratic and nominalized shells. The full rules need semantics and register context; only a very narrow tautological shell such as `осуществить проведение ...` is suitable for default mechanical detection.

## Positive operations audit

The source study preserves positive operations rather than only bans: simplify at the level of the real problem; remove empty shell then restore useful material; support evaluation with existing evidence; expose action without inventing an actor; explain new entities through known ones; structure by reader task; convert properties into relevant scenarios; state limitations honestly; and perform a final naturalness/content review.

These positive operations remain model-side unless a deterministic surface subset exists. Mechanical code reports candidates; it does not perform semantic rewriting.

## Counterexample and native-Russian audit

The counterexample layer is accepted as mandatory, not optional documentation. Especially protected are:

- real uncertainty and attribution;
- exact legal/financial/scientific values;
- legitimate official terminology;
- professional vocabulary for expert audiences;
- passive/result-state and agentless Russian when the actor is irrelevant or unknown;
- contextual ellipsis;
- functional repetition and homogeneous lists;
- long but transparent syntax;
- non-utilitarian genres;
- standard templates that genuinely solve a task.

Where an Ilyakhov editing preference conflicts with `NATIVE_USAGE`, `NATIVE_USAGE` wins.

## Gate A conclusion

Source model status: **OPERATIONAL for provenance/integration**. Runtime status: **not yet approved** until the integration matrix, feasibility report and deterministic calibration are complete.
