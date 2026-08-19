# Deep book study: «Пиши, сокращай»

Independent source study performed under `docs/book-study-framework.md`.

## Status

- source: user-provided EPUB;
- SHA-256: `21eae50b5dfd29adfe60f9f52130494673b2e4231fab4d0f29827a392bacb38d`;
- TOC nodes: **211 / 211 reviewed**;
- leaf sections: **177 / 177 sequentially read**;
- concepts: **26**;
- atomic rules: **102**;
- reusable counterexample classes: **30** (every rule mapped);
- audited source claims: **32**;
- interactions: **17**;
- synthetic evals: **67**;
- unread source sections: **0**;
- unresolved bibliographic gaps: publisher/publication date/exact print-equivalent edition are not established from EPUB metadata.

## Independence

Extraction was completed from the supplied source before comparison with the existing `ilyakhov` project branch.  
Project integration is isolated in `integration.md`, `integration-map.md` and the integration/calibration artifacts.

The book remains the primary source for its editorial model. `external-claims-evidence.md` is a **separate outside-evidence calibration** for factual/causal claims; it must not be read back into the book as if the authors supplied that evidence.

## Public-source policy

The repository contains derived concepts, rules, source locators and original test cases. It does **not** contain the EPUB, chapter text, a quote corpus or a sequential close paraphrase of the book.

The natural-Russian calibration also does not commit fetched Wikipedia article text: only aggregate counts, revision metadata and the calibration method are retained.

Files:

- `source.md` — source inventory, edition confidence, locator strategy and source-handling policy;
- `coverage.md` — complete structural coverage of all 211 NCX nodes;
- `concepts.md` — conceptual model;
- `rules-*.md` — atomic operational rules;
- `counterexamples-claims.md` — preservation cases and source-internal claims audit;
- `external-claims-evidence.md` — external empirical calibration of all 32 claims, clearly separated from source provenance;
- `interactions.md` — rule graph;
- `evals-*.md` — original synthetic eval suite;
- `audit.md` — loss and overgeneralization audits;
- `integration.md` — separate post-study mapping to `humanizer_russian`;
- `integration-map.md` — proposed source-study → runtime adapter, created only after the independent pass;
- `integration-matrix.md` — Gate-A classification before implementation;
- `mechanical-feasibility.md` — mechanical-first feasibility decisions plus post-test demotions;
- `corpus-calibration.md` — 30-article / 218,167-word natural-Russian false-positive probe and the resulting PS-R21 demotion.
