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
- [x] required positive / natural-negative / boundary / counterexample fields
- [x] 14 concepts
- [x] 12 disputed/teaching/external-verification claims
- [x] interaction pass
- [x] integration matrix for every operational observation
- [x] mechanical feasibility before runtime design
- [x] model-only residue compressed into source-neutral Russian core guidance
- [x] preservation controls for natural Russian variation
- [x] NORM subset independently checked against current references

## NORM promoted in this cycle

Only five source observations are treated as NORM candidates/guardrails, and all remain context-aware MODEL_ONLY in runtime:

1. `много/столько/сколько/мало/...` predicate-number behavior (`VEL-R12`);
2. participial phrase head attachment (`VEL-R23`);
3. participle agreement with its head (`VEL-R24`);
4. gerund semantic-subject control (`VEL-R27`);
5. gerund in impersonal + infinitive clauses when semantic subjects coincide (`VEL-R29`).

Current-reference verification narrows rather than expands automation: these are not regex rules.

## External conflict found

The strongest source conflict in the available fragment concerns introductory emotion phrases. The source rejects forms like bare `к радости, ...` without an explicit possessor, while current Gramota material recognizes `к радости` as an introductory combination. The source restriction is therefore not integrated.

Current Gramota also explicitly treats `исходя из` as a preposition, confirming that an exception is required around any generic dangling-gerund check.

## Mechanical audit

- new hard/default warning checks: **0**
- new extended warnings: **0**
- new metrics: **3**
- model-only observations: **32**

This is the intended precision-first outcome. Surface regex cannot reliably solve valency, LSV, semantic subject, aspect, action-vs-state passive, discourse scope or natural information structure.

## Loss audit

The study preserves the decision-changing distinctions visible in the fragment: semantic function vs form, subject realization, lexical valency, event construal, aspect/modality, voice/register, state/result, participial and gerund control, and introductory scope. Methodological sequencing, exercises and teacher-facing simplifications are not promoted as linter rules.

## Overgeneralization audit

The main protected areas are: natural explicit pronouns, existential `есть`, quantitative plural agreement, agentive passive in bookish genres, participles/gerunds, grammaticalized `исходя из`, colloquial syntactic phraseologisms, and context-dependent aspect choice. See `counterexamples.md`.

## Remaining unavailable material

The missing 31 chapters include several high-priority domains: dedicated word-order/theme-rheme chapter, full aspect system, negation, motion verbs, reflexives, functional-semantic cause/purpose/condition/concession etc., secondary tense/aspect meanings and animacy. No claim is made about their content beyond TOC titles.

A future complete source can extend the same long-lived `velichko` branch without invalidating this bounded study.
