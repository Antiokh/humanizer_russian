# Completeness, loss and overgeneralization audit — «Живой как жизнь»

Status: `INDEPENDENT_STUDY_VERIFIED`.

This audit closes the independent phase **before any comparison with current project rules**.

## 1. Source completeness gate

The supplied EPUB was read sequentially from `SRC:L1` through `SRC:L4530` with no unavailable sections. A reader truncation around chapter 3 was explicitly recovered by rereading from `SRC:L840`; the final read sequence has no unlisted gap.

All source units were included:

- front matter;
- 10 numbered chapters;
- appendix `Новый русский язык`;
- final `Словарь`;
- end notes.

No section is marked unavailable.

## 2. Chapter-by-chapter loss audit

The question for each source section is: **what decision-relevant distinction would disappear if this section were removed from the study artifacts?**

| Section | Distinct operational content retained | Concepts/rules/claims carrying it | Loss verdict |
|---|---|---|---|
| Front matter `L1-L36` | edition/source identity and historical framing | `source.md` | `NO_OPERATIONAL_LOSS` |
| Ch. 1 `L37-L439` | change vs current norm; generational bias; normalization over time; ellipsis vs lexical reanalysis | C01–C04; R01–R05; CLM-01–03 | `COVERED` |
| Ch. 2 `L440-L664` | do not call every novelty a “disease”; diagnose mechanism before prohibition; language change does not abolish norm | C01–C02; R01–R03, R38; CLM-01–02 | `COVERED` |
| Ch. 3 `L665-L1000` | borrowing by need/precision; reader/audience and communicative context | C03, C05; R06–R08; CLM-04–05 | `COVERED` |
| Ch. 4 `L1001-L1342` | compression vs opaque aggregation; pronunciation/uptake/register; no class-wide ban on abbreviations/coinages | C03, C06; R08–R10; CLM-06 | `COVERED` |
| Ch. 5 `L1343-L1529` | character/professional voice; slang as group phenomenon; explicit counterexample to moral inference; symptom vs cause | C07–C08; R11–R13; CLM-07–12 | `COVERED` |
| Ch. 6 `L1530-L2008` | official formula vs register leakage; pseudo-scientific inflation; direct naming; action burial; modifiers; clichés; sincerity boundary; dependency ambiguity; metadiscourse; `вопрос` packaging; read-aloud | C03, C09–C14; R14–R25; CLM-13–15 | `COVERED` |
| Ch. 7 `L2009-L2159` | word not equal stamp; individuality vs template; concrete proposition vs generic interpretation; correctness not sufficient; intonational quality | C11–C12, C22; R19, R21–R22, R26–R28; CLM-16–18 | `COVERED` |
| Ch. 8 `L2160-L2275` | source's explicit normative intervention; language-policy program; correction of alleged standard errors; culture/intellect claims | C19, C22; R35/R38 as verification-and-norm process; CLM-18–20, CLM-30 | `COVERED_AS_RULES_PLUS_CLAIMS` |
| Ch. 9 `L2276-L2472` | normative conservatism vs change; literal logic limits; expressive redundancy; sound/rhythm; strong aesthetic causal claims | C13–C14, C18; R29–R31, R38; CLM-20–23 | `COVERED` |
| Ch. 10 `L2473-L2677` | semantic bleaching; lexicalization; conventional vs fresh semantic oddity; idiom holism; creative deformation vs contamination; closing value claims | C15–C17, C22; R03, R29, R32–R34; CLM-17–18, CLM-21, CLM-24–26 | `COVERED` |
| Appendix `L2678-L2758` | accelerated lexical/abbreviation change as historical descriptive snapshot; collect living usage rather than judge whole classes | C01–C02, C06; R01–R02, R09–R10; CLM-30 | `COVERED_DESCRIPTIVELY` |
| Dictionary `L2759-L4146` | heterogeneous historical prescriptions; professional + familiar caveats; current-verification requirement | C20–C21; R35–R37; CLM-27–29 | `COVERED_WITHOUT_COPYING_LIST` |
| Notes `L4147-L4530` | provenance/qualifications; especially explicit note that an expressive formula can become a bureaucratic stamp | interaction I19; R19/R30; CLM-30 | `COVERED` |

### Chapter 8 specific check

A possible loss was: “the book also actually corrects errors; perhaps the extraction became pure descriptivism.” This is prevented by R38 + R35:

- current unambiguous norm can justify correction;
- the historical source cannot itself define 2026 norm;
- moral/cultural inferences around the error are not silently inherited.

No separate rule `correct errors` was added because it would collapse the distinction between **confirmed current norm** and **Chukovsky's historical list of forms he disliked**. The operationally faithful action is `verify current norm → correct if confirmed`, already represented by R35/R38.

### Dictionary specific check

The dictionary occupies a large share of the EPUB, but reproducing hundreds of `нельзя → надо` pairs would be both poor modern methodology and unnecessary source copying. Its **decision-relevant structure** is retained:

1. it is historical prescriptive evidence;
2. it mixes heterogeneous phenomena;
3. it is preceded by professional and familiar-register exceptions;
4. each concrete item is a modern norm candidate, not a current rule;
5. samples were externally checked and demonstrate why bulk import is unsafe.

Therefore no operational content is lost by not reproducing the full table.

## 3. Concept loss audit

22 concepts were extracted. They cover five independent source mechanisms:

1. **change/norm/usage:** C01, C02, C18, C19, C20, C21;
2. **context/register/audience/voice:** C03, C05, C06, C07, C09;
3. **semantic and syntactic clarity:** C04, C08, C10, C12;
4. **template/rhythm/sound:** C11, C13, C14, C22;
5. **lexicalization/phraseology:** C15, C16, C17.

Loss check: every major chapter has at least one concept or an explicit claim-only outcome. No decision-relevant chapter depends only on summary prose in `coverage.md`.

## 4. Atomic rule completeness audit

38 atomic rules were extracted. Every rule contains:

- source locator;
- scope;
- basis/provenance;
- level;
- confidence;
- diagnostic question;
- semantic/functional invariant;
- trigger;
- possible operation;
- exceptions;
- `Do not infer` boundary;
- interaction references;
- original positive example;
- original counterexample;
- verification procedure.

`counterexamples.md` additionally records 33 boundary patterns that prevent automatic overreach.

No rule is allowed to become a source-independent universal merely because its trigger is regex-detectable.

## 5. Rule-by-rule overgeneralization audit

| Rule(s) | Overgeneralization risk checked | Final source-faithful disposition |
|---|---|---|
| R01 | `new = correct` or `old = wrong` | keep as pre-verdict guardrail only |
| R02 | classification interpreted as acquittal | keep; classification routes to later test |
| R03 | “etymology never matters” | keep scoped to current conventional meaning |
| R04 | `recoverable → must omit` | keep as permission/preservation, not deletion command |
| R05 | every missing complement treated as lexical reanalysis | keep as diagnostic fork with R04 |
| R06 | `borrowing = good` after rejecting `borrowing = bad` | keep; semantic work + audience required |
| R07 | universal readability threshold | keep contextual; no numerical threshold |
| R08 | fixed global style label | keep scene-dependent |
| R09 | `shorter token = cheaper for reader` | reject; retain reader-effort model |
| R10 | all coinages protected from correction | reject; only class-wide prohibition is blocked |
| R11 | every slang/pro term assumed intentional voice | keep only with speaker/scene evidence |
| R12 | broad denial that language can signal identity | reject; only deterministic person-level inference is blocked |
| R13 | claim that style never has causal effects | reject; rule blocks unsupported causal leap only |
| R14 | all official wording declared legally required | reject; preserve only demonstrated genre function |
| R15 | every formal token in informal prose = cancelearite | reject; require register/function mismatch |
| R16 | concrete noun always better | reject; technical/taxonomic distinction can justify classifier |
| R17 | every nominalization must become a verb | reject; recover event only when clearer without semantic loss |
| R18 | every predictable adjective removable | reject; semantic subtraction must preserve scope/contrast/stance |
| R19 | common word/collocation = cliché | reject; require cluster/repeated discourse function |
| R20 | cliché says nothing about sincerity ever | refine: cliché alone is insufficient; independent evidence may exist |
| R21 | “make vague text specific” by invention | explicitly prohibited; proposition must be source-supported |
| R22 | read-aloud smoothness as norm | reject; sound is comparison channel after semantics |
| R23 | `N` genitives/instrumentals = error | explicitly rejected; parse/role ambiguity is target |
| R24 | `важно отметить` always delete | explicitly rejected; preserve real modality/navigation |
| R25 | noun `вопрос` itself bad | explicitly rejected; only procedural shell is targeted |
| R26 | individuality always outranks standardized schema | scoped; taxonomies/comparison matrices can need same criteria |
| R27 | primary experience makes criticism/scholarship unnecessary | rejected; rule only blocks unsupported boilerplate/intent attribution |
| R28 | richness = synonym count | explicitly rejected; quality is not a lexical-diversity score |
| R29 | established oddity licenses fresh semantic incoherence | explicitly rejected; lexicalized vs fresh is required distinction |
| R30 | semantic redundancy always expressive | explicitly rejected; current function and stamp history matter |
| R31 | Chukovsky's aesthetic phonetic history treated as scientific fact | rejected; current rule only keeps read-aloud comparison |
| R32 | “idioms never vary” | weakened after external audit: no **free** substitution; conventional variation exists |
| R33 | every idiom deviation is artistry | rejected; context/effect required |
| R34 | every deviation without obvious joke is error | rejected; unresolved is allowed when intent cannot be inferred |
| R35 | historical dictionary ignored completely | rejected; it remains candidate/provenance, not current authority |
| R36 | professional variant applies generally | explicitly scoped to current professional community |
| R37 | familiar speech has no norms | weakened; familiar register differs, but semantic/task/norm constraints remain |
| R38 | editor intuition has no value | rejected; intuition can raise a question, but mandatory correction needs reproducible evidence |

Overgeneralization verdict: `PASS_WITH_SCOPES`.

## 6. Source claims audit

30 externally relevant claim groups were inventoried in `claims.md` and externally classified in `claims-external.md`.

Key outcomes:

- 9 claim groups have an externally confirmed operational core;
- multiple others are only partially supported and remain scoped;
- strong moral/intellectual claims about slang are not admissible as text-editor rules;
- strong aesthetic-only causal explanations of morphology are not admissible as linguistic fact;
- no bulk validation of the historical dictionary was claimed;
- unresolved claims remain explicit rather than being silently deleted or upgraded.

This means uncertainty is preserved instead of being converted into false precision.

## 7. Eval completeness audit

`evals.json` contains:

- 38 direct atomic-rule evals (`chk-e01`…`chk-e38`);
- 20 compound interaction evals (`chk-c01`…`chk-c20`);
- total: 58 original scenarios.

`eval-map.json` records:

- source locators and concept linkage for all 38 rules;
- direct eval for every rule;
- compound eval coverage for all 20 interaction groups.

Important negative/counterexample behavior is explicitly tested, including:

- new ≠ automatically correct;
- official register can be valid;
- slang can be voice without proving personality;
- nominalizations can be functional;
- one cliché-like phrase is not a cluster;
- cliché does not prove insincerity;
- evaluation can itself be the task;
- technical repetition can be necessary;
- semantic redundancy can be expressive;
- idioms can have variants;
- familiar speech is not constraint-free;
- historical prescription can be confirmed by a current source without remaining “historical only”.

Eval-loss verdict: `PASS`.

## 8. Interaction audit

20 compound interactions were explicitly modeled in `interactions.md` and mapped to at least one compound eval each.

The highest-risk interactions are:

- R14 vs R15: official formula vs register leakage;
- R04 vs R05: ellipsis vs lexical reanalysis;
- R19 vs R30: dead template vs expressive repetition;
- R18 vs R30/R31: semantic subtraction vs prosodic function;
- R21/R27: concrete proposition vs invention;
- R11/R37 vs R35/R38: voice vs confirmed norm;
- R32 vs R33/R34: idiom stability vs deliberate mutation vs contamination;
- R01/R03 vs R38: language change vs normative stabilization.

No important interaction identified in the source remains without an eval.

## 9. Provenance audit

Rules were not flattened into one confidence class.

Particularly important `PROJECT_DERIVED/PROJECT_REFINED` operations:

- R16 direct-name test;
- R17 actor/action recovery;
- R18 semantic-subtraction test;
- R21 proposition-first operation;
- R23 dependency-role diagnostic boundary;
- R24 deletion A/B test;
- R31 non-deterministic read-aloud implementation boundary;
- R35 historical-to-current verification pipeline;
- R37 weakening of the source's absolute familiar-style exemption.

These are traceable operationalizations, not claims that Chukovsky wrote the algorithm in those terms.

## 10. External-evidence audit

External research was deliberately performed **after** source extraction.

It changed several conclusions rather than merely decorating them:

1. modern normative sources explicitly recognize older/younger and professional variants;
2. modern Russian grammar confirms contextual ellipsis while distinguishing it from other null-subject mechanisms;
3. modern phraseology recognizes both stability and real idiom variation/modification;
4. modern morphophonology provides grammatical/phonological conditioning that makes Chukovsky's aesthetic-only suffix explanation too strong;
5. modern research on group language supports social/identity functions and contextual correlations, not moral/intellectual diagnosis from isolated slang.

External audit therefore produced both confirmations and downgrades, as required by the framework.

## 11. Publication / copyright audit

`PASS`.

The study artifacts do not reproduce chapters, the full dictionary, or a large set of source examples. They preserve:

- operational distinctions;
- source locators;
- short names of phenomena;
- original study examples/evals;
- claims/provenance/exception structure.

The final historical dictionary is represented by its **type structure and verification policy**, not copied as a substitute reference work.

## 12. Explicit unresolved list

The following remain unresolved and are deliberately not operationalized as facts:

1. quantitative threshold for language innovation becoming established;
2. direct causal survival model for Russian abbreviations based on pronounceability;
3. calibrated modern threshold for cancelearite/nominalization density;
4. psychological causal effect of formulaic school prose on independent thought;
5. strong chapter-8 language-policy causal claims;
6. causal historical explanation of individual rhythm/euphony examples;
7. current status of every single prescription in the 1960s dictionary.

None is silently assumed during integration.

## 13. Independent-study completion gate

- [x] source inventory complete;
- [x] 100% sequential reading complete;
- [x] coverage map complete;
- [x] concepts extracted;
- [x] atomic rules extracted;
- [x] counterexamples explicit;
- [x] interactions modeled;
- [x] claims inventoried and externally audited;
- [x] original eval suite built;
- [x] eval map built;
- [x] loss audit complete;
- [x] overgeneralization audit complete;
- [x] unresolved claims explicit;
- [x] copyright/publication audit complete;
- [x] no unavailable chapter/section.

**Independent deep-book-study status: `COMPLETE`.**

Only now may the integration pass inspect and compare the current project architecture.
