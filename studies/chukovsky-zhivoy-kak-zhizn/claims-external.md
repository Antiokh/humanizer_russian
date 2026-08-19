# External claims audit — «Живой как жизнь»

Status: `AUDITED` as an **external-claims pass**, not as bulk validation of every historical dictionary entry.

This file is deliberately downstream of the independent source extraction. External material is used to classify source claims, not to rewrite what the book says.

## Status vocabulary

- `EXTERNAL_CONFIRMED` — modern authoritative/research source supports the operationally relevant core.
- `EXTERNAL_PARTIAL` — a weaker/scoped version is supported; the source's stronger wording is not.
- `EXTERNAL_CONTESTED` — modern evidence or the evidence model conflicts with the source's generalization.
- `EXTERNAL_UNRESOLVED` — no adequate modern evidence was established in this pass; do not operationalize as fact.
- `VALUE_ONLY` — normative/moral/aesthetic position, not a claim this study can validate as empirical fact.
- `HISTORICAL_ONLY` — retained as source-period material; no current operational consequence.
- `CURRENT_SAMPLE_VERIFIED` — some concrete current examples were checked, but the historical list as a whole was not.

## External source registry

**EXT-01 — Грамота.ру, Большой орфоэпический словарь: система нормативных помет.**  
Modern normative description explicitly records multiple variants within the literary norm, their relative use, older/younger norms and professional pronunciation/stress variants.

**EXT-02 — Грамота.ру, current entry `искра`.**  
General literary stress `и́скра`; professional `искра́` is explicitly recorded.

**EXT-03 — Грамота.ру, current entry `квартал`.**  
General literary `кварта́л`; the first-syllable stress is recorded only as professional-colloquial for one meaning in the metadictionary, while the orthoepic dictionary marks it nonstandard as a general pronunciation. This is a useful example of source/register sensitivity and dictionary-layer nuance.

**EXT-04 — Русская корпусная грамматика, `Неопределённо-личные предложения`.**  
Explicitly contrasts a null subject that cannot be recovered from context with incomplete/elliptical sentences where the missing subject is contextually recoverable.

**EXT-05 — Русская корпусная грамматика, `Сочинение и подчинение` / coordination.**  
Documents Russian ellipsis in coordination, including omission of repeated predicates/components.

**EXT-06 — Русская корпусная грамматика, `Дательный падеж`.**  
Describes productive elliptical constructions in which verbal semantics is reconstructed from a nonverbal expression.

**EXT-07 — Институт языкознания РАН, project on phraseological metaphor and variation.**  
Modern phraseology explicitly studies idioms, collocations, lexical-grammatical change, variation and discourse-dependent modification.

**EXT-08 — Институт языкознания РАН, work/publications on idiom variation (P. S. Dronov; phraseology project/materials).**  
Provides direct modern evidence that idioms can have standard variants and nonstandard/creative modifications. This limits Chukovsky's absolute statements about invariability.

**EXT-09 — Институт языкознания РАН, emotive phraseology database.**  
Defines idioms through high stability, reproducibility and idiomaticity, while treating internal image/meaning separately. Supports holistic phraseological treatment without implying absolute formal invariance.

**EXT-10 — Русская корпусная грамматика, `Предлог`, section on desemanticization.**  
Shows that conventional grammatical/lexical constructions may contain elements whose independent semantics is strongly reduced and whose use is lexically governed.

**EXT-11 — Русская корпусная грамматика, `Деепричастие`, form formation.**  
Shows that suffix choice is conditioned by grammatical properties and stem morphophonology, including final segment, stress and syllable structure. This supplies a concrete counterweight to a purely aesthetic causal account of morphological form choice.

**EXT-12 — Danescu-Niculescu-Mizil et al./research accessible via PMC, `Niche as a Determinant of Word Fate in Online Groups`.**  
Empirically studies community-specific word fate; discusses slang/jargon as carrying social value and group-solidarity/identity functions and notes transitory subgroup vocabulary.

**EXT-13 — research accessible via PMC, `Tracking group identity through natural language within groups`.**  
Multiple studies show language can contain correlates of group identity, but the authors explicitly emphasize context dependence and limitations. This supports scoped social signaling and argues against deterministic person-level diagnosis from isolated lexical markers.

**EXT-14 — Institute of Linguistics RAS bibliographic/theoretical material on literary language and functional-stylistic variation.**  
Modern descriptions of literary language allow functional-stylistic and social variation; codification is compatible with variation rather than requiring one context-free form.

## Claim-by-claim external disposition

| Claim | Final external status | Audit result | Operational consequence |
|---|---|---|---|
| CLM-01 language continuously changes | `EXTERNAL_CONFIRMED` | EXT-01 explicitly distinguishes older/younger current norms; modern corpus grammar is synchronic precisely because variation/change are empirical objects. | Historical age never proves current correctness. |
| CLM-02 durable usage can normalize innovation | `EXTERNAL_PARTIAL` | Older/younger norm and current variant recording support change/adoption, but the book gives no measurable threshold for “durable/widespread”. | Use as qualitative model only; no frequency cutoff. |
| CLM-03 ellipsis is lawful in Russian | `EXTERNAL_CONFIRMED` | EXT-04/05/06 explicitly describe several kinds of ellipsis and distinguish them from other null-element constructions. | R04/R05 are valid, but recovery conditions must be construction-specific. |
| CLM-04 audience knowledge affects terminology fit | `EXTERNAL_PARTIAL` | Sociolinguistic/register research supports contextual language variation; no universal comprehension threshold exists. | Audience-fit remains contextual, not score-based. |
| CLM-05 context/register can reverse stylistic judgment | `EXTERNAL_CONFIRMED` | EXT-01/02/03 explicitly encode professional vs general pronunciation; EXT-14 supports functional variation. | Strong support for scoped register decisions. |
| CLM-06 abbreviation survival partly follows pronunciation/euphony | `EXTERNAL_UNRESOLVED` | This pass did not find adequate direct evidence for the source's causal claim about abbreviation survival. | Reader-effort/pronounceability may be tested editorially; do not state causal law. |
| CLM-07 slang is often cohort/group-bound and transient | `EXTERNAL_CONFIRMED` (scoped) | EXT-12 directly studies group-specific word fate and transitory subgroup vocabulary. | Supports temporal/community metadata, not a rule that all slang is short-lived. |
| CLM-08 slang reflects extra-linguistic social/psychological conditions | `EXTERNAL_PARTIAL` | EXT-12/13 support social/group associations and dynamic relationships, but causal direction is context-dependent. | Safe: language can index group processes; unsafe: a lexical item proves a cause. |
| CLM-09 rough slang causes impoverished thought/feeling | `EXTERNAL_CONTESTED` | No adequate evidence found for this causal claim; EXT-12/13 instead show slang/language can perform identity and solidarity functions, with contextual limitations. | Exclude as operational causal rule. |
| CLM-10 slang reliably reveals moral/intellectual poverty | `EXTERNAL_CONTESTED` | Modern research uses aggregate/contextual linguistic correlates and explicitly warns about context; the book itself supplies counterexamples. | Never infer morality/intelligence from an isolated slang marker. |
| CLM-11 only dead languages lack jargon | `EXTERNAL_UNRESOLVED` | Rhetorical universal not established by this audit. | No operational use. |
| CLM-12 professional/group jargon can feed wider vocabulary | `EXTERNAL_PARTIAL` | EXT-12 demonstrates changing word fate and social diffusion in communities; exact path into literary standard is not universally established by that evidence. | Treat migration as possible, not inevitable. |
| CLM-13 official formulae are necessary in some genres | `EXTERNAL_PARTIAL` | Functional/register theory supports genre-specific conventionality, but no specific modern legal formula is verified here. | Preserve formal function; legal necessity requires domain-specific verification. |
| CLM-14 nominalization density diagnoses bureaucratization | `EXTERNAL_UNRESOLVED` | Source examples are strong stylistic evidence, but no calibrated modern corpus threshold was established. | Candidate/metric only; never hard threshold from suffix count. |
| CLM-15 case/dependency chains can create syntactic ambiguity | `EXTERNAL_CONFIRMED` (mechanism) | Modern grammar treats case as expressing multiple semantic/syntactic relations and documents dependency structure; ambiguous attachment/roles are structurally real. | Diagnose parse/roles, not number of genitives/instrumentals. |
| CLM-16 formulaic evaluative language replaces independent thought | `EXTERNAL_UNRESOLVED` as psychological causation | The textual phenomenon is source-observable; the stronger cognitive causal statement was not independently established. | Diagnose propositionless/template prose; do not diagnose thinking ability. |
| CLM-17 rich vocabulary + varied intonation are necessary for “cultured speech” | `VALUE_ONLY` | “Cultured” is the author's value category; no defensible scalar threshold follows. | Preserve as quality ideal, never metric or gate. |
| CLM-18 linguistic correctness tracks general culture/intellect | `EXTERNAL_CONTESTED` as deterministic inference | No adequate basis found for the book's strong person-level moral/intellectual inference; modern sociolinguistic evidence emphasizes contextual/social variation. | Exclude person-level diagnosis. |
| CLM-19 coordinated institutions/media can change mass language | `EXTERNAL_UNRESOLVED` in the strong source formulation | Language planning is a real field, but this pass did not verify the source's Soviet-era causal strength/prescription. | Historical/policy claim only unless separately researched. |
| CLM-20 normative conservatism is necessary for continuity | `EXTERNAL_PARTIAL` | EXT-01/14 show codification plus variation and temporally stratified norm; “necessary” is a stronger theoretical claim than the audit establishes. | Keep dynamic-equilibrium concept, not necessity theorem. |
| CLM-21 established usage can override literal compositional logic/etymology | `EXTERNAL_CONFIRMED` | EXT-10 documents desemanticization/lexically governed combinations; modern phraseology distinguishes conventional idiomatic meaning from component meaning. | Do not “repair” lexicalized expressions by etymological arithmetic. |
| CLM-22 rhythm/sound can justify semantic redundancy | `EXTERNAL_PARTIAL` | General prosodic/stylistic plausibility is strong, but the source's explanations for particular fixed phrases are interpretive rather than experimentally demonstrated. | Use A/B read-aloud as editorial criterion, not causal history. |
| CLM-23 Russian suffix/allomorph choices are selected for aesthetic fitness | `EXTERNAL_CONTESTED` in strong form | EXT-11 directly shows suffix selection conditioned by grammar and morphophonology; this does not support “only/primarily aesthetic taste” as the mechanism. | Keep sound sensitivity; reject aesthetic-only causal explanation. |
| CLM-24 semantic bleaching/lexicalization is normal | `EXTERNAL_CONFIRMED` | EXT-10 documents desemanticization; EXT-07/09 support conventionalized phraseological meaning/internal form distinction. | Strong support for R03/R29/R32. |
| CLM-25 idioms are holistic and resist free substitution | `EXTERNAL_PARTIAL` | EXT-07/09 support stability/idiomaticity; EXT-08 shows real idiom variation, so “no variants” is too strong. | Rule becomes “no free synonym substitution; verify conventional variants.” |
| CLM-26 intentional idiom deformation can create effect | `EXTERNAL_CONFIRMED` (mechanism) | EXT-07/08 explicitly study modification/transformation and discourse-dependent idiom change. | Preserve deliberate, interpretable modifications; distinguish from contamination. |
| CLM-27 final dictionary prescriptions are current norm | `CURRENT_SAMPLE_VERIFIED`, whole-list claim rejected | EXT-01–03 confirm that modern norm is variant- and register-sensitive. Several source examples remain recognizable, but the historical list cannot be validated as a unit. | Every imported item requires individual current verification. |
| CLM-28 professional communities maintain scoped variants | `EXTERNAL_CONFIRMED` | EXT-01 explicitly documents professional pronunciation variants; EXT-02 gives `искра́`. | Strong support for professional-scope rule, with current item-by-item verification. |
| CLM-29 familiar/home speech has different normalization constraints | `EXTERNAL_PARTIAL` | Modern functional/social variation supports register dependence; the source's “does not fall under normalization” wording is too absolute. | Preserve situational familiarity but keep semantic/norm/task constraints. |
| CLM-30 historical counts/anecdotes | `HISTORICAL_ONLY` | Not exhaustively fact-checked because no operational rule depends on exact counts. | Keep locators; verify an individual datum only if later used externally. |

## Specific modern-norm sample checks from the historical dictionary caveat

These checks are illustrative and intentionally **not** a bulk revalidation of `Словарь`.

### `искра`

Chukovsky's pre-dictionary caveat presents professional `искра́`. Current Big Orthoepic Dictionary material on Gramota records general `и́скра` and a professional variant `искра́` (EXT-01/02).

Disposition: the **scoping principle survives**, and this sample remains current as a professional variant.

### `квартал`

The source mentions accountants' `ква́ртал` as a professional usage. Current Gramota material is more nuanced: the general orthoepic norm is `кварта́л`, while the metadictionary also labels `ква́ртал` professional-colloquial for the “three-month period” meaning (EXT-03).

Disposition: this is exactly why a historical pair cannot be imported without source/register-aware current verification.

## Important negative findings

1. No external evidence found here justifies a rule `slang → moral/intellectual defect`.
2. No external evidence justifies a numerical `nominalization count → cancelearite` threshold.
3. No external evidence justifies a numerical `euphony/richness/humanity` score.
4. The source's strong aesthetic explanation of Russian suffix selection is overclaimed relative to modern morphophonological descriptions.
5. The source's absolute claim that idioms admit no variants is too strong; modern phraseology explicitly studies conventional variation and creative modification.
6. The source's final dictionary cannot be treated as a 2026 authority; current normative sources explicitly encode temporal and professional variants.

## What remains unresolved after the external pass

- a quantitative model of when an innovation becomes established;
- direct empirical survival model for Russian abbreviations based on pronounceability;
- calibrated corpus evidence for bureaucratic nominalization density;
- psychological causal effects of formulaic school prose on independent thinking;
- the strong language-policy causal program of chapter 8;
- a causal historical account for the source's particular rhythm/euphony explanations;
- the current status of every individual pair in the historical dictionary.

These unresolved claims do **not** block the study from being operational because none is required as an unqualified rule. They remain explicit research questions and must not be silently promoted during integration.
