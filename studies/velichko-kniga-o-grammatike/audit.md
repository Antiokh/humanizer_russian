# Final study audit — Velichko 2004 supplied fragment

Status: **OPERATIONAL_FOR_AVAILABLE_FRAGMENT**.

## Source gate

The complete advertised 2004 volume is unavailable, but the user explicitly confirmed on `2026-08-20` that the supplied fragment is all digital source available. The gate is therefore re-scoped from “full advertised book” to “full physically available fragment”.

This is not a waiver of provenance. The audit records both facts simultaneously:

- available fragment: sequentially read and audited in full;
- advertised chapters 14–44: unavailable and not inferred.

## Completion checklist

- [x] source fingerprint and edition identified
- [x] all 6330 rendered source lines / all available chapter bodies read
- [x] coverage map distinguishes available vs TOC-only chapters
- [x] grammar separated from teaching methodology
- [x] 35 atomic observation cards
- [x] canonical `rules.md` entry point plus maintainable split card files
- [x] required positive / natural-negative / boundary / counterexample fields
- [x] 14 concepts
- [x] 12 disputed/teaching/external-verification claims
- [x] interaction pass
- [x] integration matrix for every operational observation
- [x] mechanical feasibility before runtime design
- [x] model-only residue compressed into source-neutral Russian core guidance
- [x] source-neutral deduplication against existing Russian-core phenomena
- [x] all 32 non-metric observations mapped to production Russian-core cards
- [x] preservation controls exercised through Compact and Editorial Board
- [x] NORM subset independently checked against current references
- [x] external CodeRabbit review findings verified, fixed and resolved
- [x] repository-wide quality workflow green after the review-fix cycle

## NORM promoted in this cycle

Only five source observations are treated as NORM candidates/guardrails, and all remain context-aware `MODEL_ONLY` in runtime:

1. quantifier predicate-number behavior (`VEL-R12`) — **normative variation guard**, not singular-only enforcement;
2. participial phrase head attachment (`VEL-R23`);
3. participle agreement with its head (`VEL-R24`);
4. gerund semantic-subject control (`VEL-R27`);
5. gerund in impersonal + infinitive clauses when semantic subjects coincide (`VEL-R29`).

Current-reference verification narrows rather than expands automation: these are not regex rules.

## Current-reference conflicts and narrowing

### Quantifier agreement (`VEL-R12`)

The source and the Gramota Pismovnik reproduce the academic singular-agreement rule for `много/немного/мало/немало/столько/сколько`. Current Gramota Help Desk answers, however, explicitly recognize semantic plural agreement as normative: № 322014 (2025) allows both forms with `много людей` and calls plural the newer norm; № 320220 (2024) likewise recognizes plural with active persons; № 298593 (2018) says singular is preferable with `много`, but plural is not an error.

Project disposition: preserve the conflict/evolution as **current normative variation**. No singular-only repair, warning or stop rule is allowed. Both `Собралось много людей` and contextually licensed `Много людей пишут нам` are preservation cases.

### Introductory emotion phrases

The source rejects forms like bare `к радости, ...` without an explicit possessor, while current Gramota material recognizes `к радости` as an introductory combination. The source restriction is therefore not integrated.

### Gerund-like grammaticalization

Current Gramota explicitly treats `исходя из` as a preposition, confirming that a generic dangling-gerund rule needs a grammaticalization guard. Other forms in the source list are not blindly whitelisted.

## Production integration / deduplication audit

Velichko is not a reviewer persona. The study adds evidence to the long-lived source-neutral `russian` core.

- 13 new source-neutral `RU-*` model-only cards live in `libraries/russian/rki-rules.json`;
- existing Russian-core cards for gerund subject attachment, participle head attachment and participial compression are **enriched**, not duplicated;
- duplicate `phenomenon_id` values across `libraries/russian/rules.json` and `libraries/russian/rki-rules.json`: **0**;
- every `VEL-R01`…`VEL-R32` observation is mapped through `study_rule_ids` to at least one source-neutral Russian-core card;
- the three `VEL-M*` observations remain distributional metrics only.

## Mechanical audit

- new hard/default warning checks: **0**
- new extended warnings: **0**
- new metrics: **3**
- model-only observations: **32**

This is the intended precision-first outcome. Surface regex cannot reliably solve valency, LSV, semantic subject, aspect, action-vs-state passive, agreement semantics, discourse scope or natural information structure.

## Review-fix audit

CodeRabbit's forced PR review produced three actionable findings, all verified rather than accepted mechanically:

1. the passive metric proxy allowed a bare final `т`, causing false positives such as `Документ лежит перед нами.` near an instrumental pronoun — fixed by narrowing the precision-first proxy and adding the negative control;
2. fenced-code masking did not preserve the opening Markdown fence character/length, so an inner shorter fence could expose code as prose — fixed with exact fence tracking and a four-backtick/three-backtick regression test;
3. the original singular-only treatment of `много + род. мн.` contradicted current Gramota Help Desk evidence — fixed across the atomic card, production rule, claims, integration matrix, interactions, reference guidance and preservation benchmark.

All three review threads are resolved. The post-fix quality gate is green.

## Runtime preservation audit

The source-specific benchmark now exercises **both** Compact and Editorial Board routes. It verifies:

- 13 new source-neutral model-only RKI cards;
- 3 `METRIC_ONLY` proxies with identical Compact/Board metric output;
- 8 natural preservation controls, including plural semantic agreement with `много`;
- existing narrow Russian mechanics such as `процесс ломается` still route correctly;
- **0 new deterministic findings** from the Velichko contextual layer.

## Loss audit

The study preserves the decision-changing distinctions visible in the fragment: semantic function vs form, subject realization, lexical valency, event construal, aspect/modality, quantitative agreement, voice/register, state/result, participial and gerund control, and introductory scope. Methodological sequencing, exercises and teacher-facing simplifications are not promoted as linter rules.

## Overgeneralization audit

The main protected areas are: natural explicit pronouns, existential `есть`, quantitative plural agreement, agentive passive in bookish genres, participles/gerunds, grammaticalized `исходя из`, colloquial syntactic phraseologisms, and context-dependent aspect choice. See `counterexamples.md`.

## Remaining unavailable material

The missing 31 chapters include several high-priority domains: dedicated word-order/theme-rheme chapter, full aspect system, negation, motion verbs, reflexives, functional-semantic cause/purpose/condition/concession etc., secondary tense/aspect meanings and animacy. No claim is made about their content beyond TOC titles.

A future complete source can extend the same long-lived `velichko` branch without invalidating this bounded study. The branch must remain after merge.
