# Serbian public-source baseline

This document is the research baseline for a Serbian-language sibling of `humanizer_russian`.

The first implementation should keep four evidence classes separate:

1. `NORM` — modern Serbian standard-language constraints backed by standardization bodies and language institutions.
2. `NATIVE_USAGE` — attested Serbian usage, collocations, information structure, and register.
3. `INTERFERENCE` — calques and contact-language effects, especially English → Serbian and Russian → Serbian.
4. `AI_STYLE_SIGNAL` — recurring stylistic patterns associated with LLM-generated Serbian. These are diagnostic signals, not proof of AI authorship and not language errors by themselves.

## Public normative and institutional sources

### Odbor za standardizaciju srpskog jezika

- https://www.ossj.rs/
- Public decisions, recommendations, corrections, positions and explanations concerning Serbian standard language.
- Treat an individual decision according to its scope. Do not generalize a narrow recommendation into a universal rule without independent support.

### Institut za srpski jezik SANU — Odsek za standardni jezik

- https://www.isj.sanu.ac.rs/odseci/odsek-za-standardni-jezik/
- The department explicitly works on description and modernization of contemporary Serbian norm.

### Rečnik lingvističkih termina

- https://www.lingvistickitermini.rs/
- Useful for formalized concepts and source-backed stylistic phenomena.
- Example: `birokratski jezik` is characterized by verbosity, complexity, vagueness, stereotypy, impersonality, generalization and nominalization. Those properties should be modeled as register/style signals rather than automatic errors.

### srWaC 1.1

- https://www.clarin.si/repository/xmlui/handle/11356/1063
- Serbian web corpus, approximately 555M tokens / 25.6M sentences / 1.35M texts.
- Publicly available under CC BY-SA 4.0.
- Paragraph-deduplicated, morphosyntactically annotated and lemmatized.
- Intended use in this project: empirical calibration of collocations, phrase frequencies and false-positive rates. Corpus frequency never creates `NORM` by itself.

## Public analyses of AI-generated Serbian

### Bojan Viculin — “Razotkrivanje šablona AI (VI) generisanog teksta” (P.U.L.S.E, 25 Apr 2026)

- https://pulse.rs/razotkrivanje-sablona-vi-generisanog-teksta/
- Serbian-language analysis of a long text suspected of heavy LLM generation.
- The author repeatedly identifies the following recurring patterns:
  - negative contrast templates: `A nije B, već C`, `A nije samo B, već i C`, `Ne samo A, već i B`;
  - repeated three-part enumerations and three-adjective/adverb descriptions;
  - unusually smooth transitions and formulaic organization;
  - excessive micro-headings;
  - repeated grand metaphors (`tkivo`, `arena`, `bojno polje`, etc.) and hyperbole;
  - generic / content-light assertions and insufficient problematization;
  - unnatural English-derived phrases such as `alat za razumevanje` / `tools for understanding` in contexts where Serbian would normally choose another formulation;
  - repetitive sentence architecture and repeated lexical frames.

These findings must be encoded as `AI_STYLE_SIGNAL` or `INTERFERENCE`, not `NORM`, unless a separate normative source establishes an actual language error.

### Serbian community observations

Public Serbian Reddit discussions provide useful hypothesis material but are not normative evidence:

- `r/AskSerbia`: “Kako prepoznajete Ai tekst?” — users mention punctuation such as em dashes as a social AI cue, while simultaneously demonstrating that real humans use them. This is a strong counterexample against dash-removal rules.
- `r/serbia`: discussion of a political programme points to exact repetition of the same section labels across dozens of measures as an obvious generation template. This supports document-level repetition metrics rather than lexical bans.
- `r/Serbian`: a learner’s error-rich Serbian was explicitly described as “too many mistakes for ChatGPT”, showing that fluency / cleanliness itself is socially read as an AI cue but is not sufficient evidence.

Community material belongs only in hypothesis/evaluation datasets unless independently validated.

## Initial project policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Choice among valid Serbian alternatives:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

Consequences:

- Never rewrite a correct sentence only to lower an AI-detector score.
- Never ban em dashes, three-item lists, headings or contrast constructions globally.
- Detect accumulation: a single `nije samo … već` is ordinary Serbian; many nearly identical instances in a short text are a useful style signal.
- Keep Cyrillic and Latin orthographies first-class. Rules should normalize both scripts to a shared internal representation where possible, while reporting the original surface form.
- Ekavian and Ijekavian Serbian are both legitimate standard variants; do not treat one as an error solely because the other was configured as default.

## First implementable rule families

1. `sr_ai_negative_parallelism_density`
   - Count repeated contrast frames such as `nije (samo)? … već/nego …`.
   - Document-level soft signal only.

2. `sr_ai_triplet_density`
   - Detect repeated three-item enumerations / three-coordinate adjective or adverb sequences.
   - Soft signal; require accumulation and syntactic plausibility.

3. `sr_ai_heading_fragmentation`
   - Detect abnormally frequent headings relative to prose length.
   - Especially useful for Markdown and generated reports.

4. `sr_ai_repeated_section_scaffold`
   - Detect identical heading/lead scaffolds repeated many times, e.g. the same two section labels across dozens of items.
   - High-confidence artifact/style signal at document level, but not proof of AI authorship.

5. `sr_style_bureaucratic_nominalization`
   - Model clusters of nominalization, impersonality and vague administrative phrasing using Institute terminology.
   - Start model-only / extended; avoid crude suffix bans.

6. `sr_interference_tool_metaphor`
   - Track suspicious English `tool` metaphors (`alat za X`) as contextual candidates, not blanket errors.
   - Validate candidate phrases against srWaC before promotion.

7. `sr_script_mixing`
   - Flag accidental Cyrillic/Latin mixing within the same lexical token or tightly scoped prose segment, while allowing URLs, code, quotations and names.
   - Candidate for deterministic mechanical validation after normative confirmation.

## Explicit anti-rules

The first Serbian version must include regression tests proving that these alone are not findings:

- one em dash;
- one three-item list;
- one `nije A, već B` construction;
- one metaphor;
- polished grammar;
- use of Latin script;
- use of Cyrillic script;
- Ekavian vs Ijekavian choice.
