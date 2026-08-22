# Ilyakhov web supplement — audit

## Scope

This pass integrates a curated set of high-yield public materials into the existing `ilyakhov` editorial library. It does **not** claim exhaustive coverage of Maxim Ilyakhov's entire blog, Bureau advice archive or the live Glavred rule database.

Portable source provenance lives in `libraries/ilyakhov/web-sources.json`. The current index contains 24 sources/discovery surfaces:

- author-primary blog materials;
- author advice on Bureau pages;
- official Glavred service documentation and handbook index;
- author/Bureau discovery indexes;
- one historical third-party stop-word list, explicitly marked `THIRD_PARTY_ACKNOWLEDGED`.

The author's 2017 index states that it selects 100 editor-facing articles out of 142 written that year. The current Bureau author page indexes hundreds more advices. Those indexes are registered as discovery surfaces, not as proof that every linked item was individually audited in this pass.

## Main result

Most useful web material does not justify creating new independent rules. It narrows or strengthens the existing book model:

- stop words → `ILY-R06/R07` plus stronger non-ban guard;
- time parasites → `ILY-R21` plus evidence/generalization interactions;
- unsupported obviousness → `ILY-R09/R10/R37—R39`;
- corporate clichés → `ILY-R15—R20/R85`;
- terminology/adjectives → `ILY-R23/R26/R27/R40` plus counterexamples;
- concision/tool score → `ILY-R01—R07` and anti-cargo-cult guard.

Three genuinely useful supplemental cards remain after deduplication:

- `IW-R01` — stated corporate value requires an operational consequence/trade-off;
- `IW-R02` — anti-editorial cargo cult, including detector-driven damage to normal Russian;
- `IW-R03` — figure-of-speech function test.

All three are `MODEL_ONLY`. None is `NORM`, `HARD_GATE` or `DEFAULT_MECHANICAL`.

The August 2026 Bureau advice on normal punctuation and constructions being misread as AI output directly reinforces `IW-R02`: typography and valid Russian syntax must not be degraded merely to appear less machine-generated.

## Mechanical changes

Only two existing surfaces were widened:

1. `ILY-R21` metric inventory now recognizes several multiword present-time wrappers documented in «Паразиты времени». It remains `METRIC_ONLY`; generic `сейчас` is deliberately excluded from the regex because it often carries literal temporal meaning.
2. `ILY-R85` gains several corporate-cliché phrase candidates (`полный спектр`, `комплексный подход`, `кратчайшие сроки`, `быстро и качественно`). R85 still emits only in `--extended` and only when at least two generic-benefit patterns occur in one sentence.

Positive and negative controls are encoded in `scripts/lint_ilyakhov.py` and `tests/lint_cases.json`.

## Stop-list finding

A public historical list exists at `miripiruni/stop-words`. In a 2014 comment under «Паразиты времени», its author said he had collected Ilyakhov's stop words for a highlighting script; Ilyakhov thanked him for collecting the list.

This establishes useful historical provenance, but not authorship, completeness or current Glavred equivalence. The project therefore records the URL and curated candidate groups in `stopword-corpus.json` rather than copying the list into an executable ban table.

Official Glavred documentation says its maintained database includes rules, stop words, examples and links and covers a much broader taxonomy than a flat word list. No public complete current Glavred stop-word export was established in this pass.

## Strong counterexamples retained

- a stop word can be semantically necessary;
- personal/possessive pronouns can be required for natural Russian or contrast;
- an adjective can be a technical term rather than empty praise;
- present-time wording can encode a real period contrast;
- uncertainty can be honest and meaningful;
- a metaphor can be the point of literary/personal/rhetorical prose;
- official/legal nominalization can be functional;
- a high tool or detector score does not imply a good text;
- normal dashes, quotation marks and valid constructions must not be mutilated to mimic a presumed human surface.

## Attribution boundary

`ILY-R01`—`ILY-R102` continue to mean rules audited from the supplied EPUB. `IW-R*` means a supplemental web-derived card. A future book edition or another full source must receive its own source audit instead of being silently folded into the old EPUB provenance.

## Follow-up candidates

Not promoted in this pass:

- crawl/classification of the full author/Bureau archive;
- systematic audit of all 100 articles in the 2017 author index and the current Bureau author index;
- a separate audit of the current interactive «Пиши, сокращай» edition;
- direct Glavred API benchmarking against local findings;
- calibration of individual historical stop-list tokens on a natural corpus.

These are useful follow-ups, but none is required for the current library to use the high-confidence web supplement safely.
