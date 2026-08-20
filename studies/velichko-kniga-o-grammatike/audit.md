# Study audit — Величко, «Книга о грамматике»

Status: **BLOCKED AT SOURCE COMPLETENESS**.

This audit exists to prevent a partial or wrong-edition study from being promoted into the Russian runtime layer.

## Gate A decision

`FAIL` — source integrity/completeness.

The task names the 2024 collective monograph «Книга о грамматике. Лингводидактические основы преподавания русского языка как иностранного» (ISBN `978-5-19-011994-7`, 742 pp.). The uploaded DOCX identifies itself as the 2004 second edition «Книга о грамматике: Русский язык как иностранный» (ISBN `5-211-05040-1`, advertised as 816 pp.) and physically stops after chapter 13 at printed pp. 174–175.

A study based on this file cannot truthfully satisfy the project requirement “read the source completely before integration”.

## Integrity checks completed

- uploaded file fingerprinted with SHA-256;
- DOCX opened successfully with `python-docx`;
- paragraph/table/section counts checked;
- ZIP contents inspected for hidden media/page scans: none;
- file TOC compared with body headings;
- body termination checked at the end of chapter 13;
- publisher metadata for the named 2024 monograph checked independently;
- long-lived branch `velichko` created from fresh `main` before study artifacts were written.

## Why substitution is not acceptable

Other editions can be useful as independent evidence, but they cannot fill a provenance hole. Chapter numbering, ordering, authorship and revisions differ between editions. Reconstructing missing chapters from another edition would create false source locators and make later rule audits unreliable.

The same applies to general linguistic knowledge: it can verify a claim independently, but it cannot stand in for the missing primary-source passage when the rule claims Velichko provenance.

## High-value signals already visible in the supplied extract

These are **revisit markers only**, not extracted atomic rules and not runtime decisions. They are recorded so the continuation can resume efficiently once the complete target source is supplied.

1. **Meaning → form rather than form-only grammar.** The introduction explicitly treats universal semantic functions as having language-specific Russian realizations. This matches the intended `function → natural form → interference form → repair` architecture.
2. **Valency is lexical-semantic, not merely case morphology.** The source contrasts `пользоваться чем`, `использовать что для чего / где / как`, and similar patterns; chapter 8 develops motivated vs lexically fixed government and polysemy-dependent frames.
3. **Learner subject overexpression.** The chapter on indefinite-personal sentences explicitly marks insertion of `они` into a construction whose point is to leave the actor unnamed as a typical learner error.
4. **Two-member bias in learner Russian.** The nominal-sentence chapter notes a tendency to force an explicit present-tense predicate where Russian naturally permits a nominative/existential presentation.
5. **State / process / result construal.** Chapters on basic models, impersonal sentences and passive structures repeatedly distinguish ongoing action, state and result rather than treating tense morphology as sufficient.
6. **Aspect can encode modal semantics.** Infinitive constructions contrast imperfective prohibition/non-necessity with perfective objective impossibility; this is inherently contextual and should not become a regex rule.
7. **Natural-force events prefer Russian-specific impersonal models.** Constructions such as an affected object plus instrumental natural force and neuter singular predicate are treated as a recurrent learner difficulty.
8. **Passive is a perspective choice and register choice.** Three-member agentive passive is described as strongly book-oriented and rare in ordinary conversation; possessive resultative structures provide a more conversational result-focused alternative in some contexts.
9. **Statal vs action passive matters.** The source records learner errors where a reflexive action-passive form is used to describe a static spatial/property relation that Russian normally encodes with a stative/resultative construction.
10. **Scientific linking predicates are not interchangeable.** `есть`, `являться`, `представлять собой`, `состоять в`, `заключаться в`, `сводиться к` have narrower semantic and register constraints than a generic “to be” equivalent.
11. **Participial compression has hard attachment/agreement constraints and softer usage constraints.** Head attachment and agreement are potentially NORM; preference between participial and relative-clause forms is context/register dependent.
12. **Gerund subject attachment has a core norm plus exceptions.** The shared-subject rule is central, but lexicalized/preposition-like forms (`исходя из`, `учитывая`, etc.) and some infinitival impersonal constructions require exclusions. Existing `RU-NORM-GERUND-SUBJECT-ATTACHMENT` therefore needs refinement rather than a simplistic regex.
13. **Word position can alter scope/reference.** Even chapter 13 shows that relocating an introductory/modal element changes whose uncertainty is expressed. This is a direct warning against surface-only handling of reference and information structure.
14. **Native colloquial syntax includes constructions a formal grammar may not predict.** Syntactic phraseologisms are productive, frequent spoken patterns and must be protected as negative controls against over-normalization.
15. **Grammar and methodology are interleaved.** Many passages switch from describing Russian constraints to advice about sequencing classroom material; only the former can become project rules.

None of these markers has yet been assigned a final `project_class`, automation level, severity or `phenomenon_id` because doing so before complete-source extraction would violate the study gate.

## Runtime audit

No files under `libraries/russian/`, `references/`, `scripts/`, Compact runtime, or Editorial Board runtime were changed in this blocked pass.

This is intentional. Existing Russian rules already cover several neighboring phenomena (abstract `ломаться`, gerund subject attachment, participle head attachment, generic RKI syntactic-interference audit). Premature source-specific additions would create overlap before the full source can be mapped.

## Tests

Full integration tests were **not run as completion evidence**, because there is no runtime integration to validate and the source study is not eligible for `AUDITED`/`OPERATIONAL` status.

The next complete-source pass must run the full required suite only after extraction, verification, integration matrix, mechanical feasibility review and runtime changes are complete.

## Unblocking criteria

One of the following is required:

1. **Preferred:** complete 2024 monograph, ISBN `978-5-19-011994-7`; or
2. explicit re-scope to the 2004 second edition plus a complete file containing the missing body after printed p. 175 through the end of the volume.

After unblocking:

- refingerprint the complete source;
- rebuild exact TOC/coverage from that source;
- read it sequentially with no gaps;
- only then create atomic observation cards, counterexamples, claims/evidence, integration matrix and runtime rules;
- verify NORM claims independently;
- run Compact/Board/RKI/Velichko tests;
- open `velichko -> main` PR only after green gates.
