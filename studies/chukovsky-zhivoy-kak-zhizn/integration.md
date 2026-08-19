# Integration pass — independent Chukovsky study → current humanizer+ru

Status: `INTEGRATION_DESIGNED`.

This file was created **after** `audit.md` marked the independent study complete. The mapping below compares the 38 independently extracted rules with the actual current `main` architecture, rather than reverse-engineering rules from an earlier Chukovsky branch.

## Integration principles

1. `SEMANTICS` and current `NORM` remain hard constraints.
2. A historical book does not become a 2026 normative authority merely by being influential.
3. Chukovsky contributes chiefly:
   - register/audience diagnostics;
   - positive editing operations;
   - anti-purist boundary conditions;
   - rhythm/read-aloud diagnostics;
   - lexicalization/idiom boundaries;
   - evidence discipline for historical prescriptions.
4. Surface regex may emit only soft candidates for these phenomena. It must not infer final register fit, idiom status, sincerity, personality, semantic roles or current norm.
5. Independent rule/eval IDs remain in `studies/...`; production-facing rules use the project's semantic namespaces (`NORM-*`, `EDIT-*`, etc.).

## Mapping of all 38 independent rules

| Independent rule | Current project coverage before integration | Integration decision | Destination / implementation |
|---|---|---|---|
| CHK-R01 generational taste ≠ current norm | partial in `evidence-audit.md`; not explicit in workflow | `REFINE` | add historical/current-norm gate to `SKILL.md` + `references/chukovsky.md`; evidence cross-reference |
| CHK-R02 classify innovation before judging | missing as explicit routing step | `ADD_SKILL` | pre-verdict classification in Chukovsky reference; concise workflow note in SKILL |
| CHK-R03 current meaning ≠ etymology | missing | `ADD_REFERENCE` | lexicalization/etymology section in Chukovsky reference; norm-facing warning in `russian-language.md` |
| CHK-R04 preserve recoverable ellipsis | already strong in `russian-language.md`/`native-russian.md` | `ALREADY_COVERED + REFINE` | add explicit `recoverable = permission, not command to omit` |
| CHK-R05 ellipsis vs lexical reanalysis | current `russian-language.md` separates some zero elements but not this exact distinction | `REFINE` | add lexical-reanalysis diagnostic to `russian-language.md` |
| CHK-R06 borrowing by semantic work | partial: professional anglicism not hard ban | `REFINE` | term-choice decision test in SKILL/reference |
| CHK-R07 terminology by audience | partial in rule audit/author layer | `REFINE` | explicit audience step before lexical cleanup |
| CHK-R08 judge lexical fit by scene | partial via Nora voice mismatch | `REFINE` | dedicated register/scene stage before simplification |
| CHK-R09 abbreviation by reader effort | largely missing | `ADD_SKILL` | `EDIT-ABBREVIATION-EFFORT`; linter only opaque-cluster candidate |
| CHK-R10 no class-wide ban on formations | implicit anti-hard-ban policy | `REFINE` | Chukovsky reference + rule-audit note |
| CHK-R11 preserve character/professional voice | strong in author profile/Nora | `ALREADY_COVERED + REFINE` | add speaker-role-scene wording, no duplicate algorithm |
| CHK-R12 no person diagnosis from one slang marker | author profile says do not diagnose personality, but not explicit for slang | `REFINE` | explicit inference boundary in author/Chukovsky reference |
| CHK-R13 symptom ≠ extra-linguistic cause | SKILL already forbids new causes/diagnoses | `ALREADY_COVERED + REFINE` | add source-grounded explanation to Chukovsky reference |
| CHK-R14 preserve functional official formulas | missing explicit positive rule | `ADD_SKILL` | register stage; formal genre exception |
| CHK-R15 official-register leakage | Nora voice mismatch partly covers it | `ADD_SKILL + LINTER_SOFT` | `EDIT-REGISTER-LEAK`; conservative bureaucratic cluster candidate only |
| CHK-R16 direct name vs prestige classifier | missing explicit operation | `ADD_SKILL` | `EDIT-DIRECT-NAME`; model-level semantic-delta test |
| CHK-R17 recover action from nominal packaging | rule audit only says WARN | `ADD_SKILL + LINTER_SOFT` | `EDIT-ACTION-RECOVERY`; soft light-verb/nominalization candidates |
| CHK-R18 semantic subtraction for modifiers | missing | `ADD_SKILL + LINTER_SOFT` | `EDIT-MODIFIER-SUBTRACTION`; only conservative candidate lexemes in surface linter |
| CHK-R19 stamps by cluster/function | AI layer already cluster-oriented | `REFINE + LINTER_SOFT` | distinguish `EDITING_SUGGESTION` from provenance/AI inference; cliché cluster belongs first to editing |
| CHK-R20 cliché ≠ insincerity | missing | `ADD_REFERENCE` | explicit inference boundary; model only |
| CHK-R21 proposition before evaluation | Nora concrete/no-invention partly covers it | `REFINE` | `EDIT-PROPOSITION-FIRST` in SKILL/reference |
| CHK-R22 read-aloud after semantics | missing | `ADD_SKILL + LINTER_SOFT` | separate final prosody pass; linter can surface dense ending echo only |
| CHK-R23 dependency/case ambiguity, not counts | rule audit already warns against counts | `REFINE / MODEL_ONLY` | semantic-role reconstruction in SKILL/reference; no regex case-count gate |
| CHK-R24 deletion test for metadiscourse | current linter wrongly treats single announcement as AI pattern | `CORRECT_LINTER + ADD_SKILL` | move to `EDITING_SUGGESTION`; A/B deletion test; no automatic deletion |
| CHK-R25 `вопрос` packaging | missing | `LINTER_SOFT + REFERENCE` | only repeated procedural-shell cluster; final decision model-level |
| CHK-R26 preserve subject individuality vs template | partially author layer, not analytical-document layer | `ADD_REFERENCE` | document-level template operation test; avoid forcing into core short workflow |
| CHK-R27 ground interpretation before boilerplate | Nora specificity partly | `REFINE` | reference + proposition/no-invention check |
| CHK-R28 correctness not sufficient for quality | architecture already assumes editing beyond norm | `ALREADY_COVERED + REFINE` | make explicit that “richness” is not synonym/entropy score |
| CHK-R29 conventional expression vs literal logic | missing | `ADD_REFERENCE` | lexicalization boundary before semantic/metaphor diagnosis |
| CHK-R30 expressive redundancy | native layer already preserves intentional repetition | `REFINE` | add prosodic/idiomatic function explicitly; `recoverable ≠ must delete` |
| CHK-R31 sound/rhythm as comparison, not formula | missing | `ADD_SKILL / MODEL_ONLY` | read-aloud A/B; no euphony score |
| CHK-R32 idiom as lexical whole | missing in Nora layer | `ADD_NORA_BOUNDARY` | update `nora-gal.md`: lexicalized idiom is not live metaphor conflict; no free synonym substitution |
| CHK-R33 deliberate idiom deformation | Nora has general humor exception but not phraseological mechanism | `REFINE_NORA` | preserve recoverable deliberate modification |
| CHK-R34 intentional play vs contamination | Nora collocation mentions crossed expressions, but intent boundary weak | `REFINE_NORA` | two-hypothesis diagnostic; unresolved allowed |
| CHK-R35 historical prescription → current verification | evidence audit partly but not general process | `ADD_NORM_POLICY` | SKILL + Russian-language reference; historical dictionary stays candidate only |
| CHK-R36 professional variant scoped to community | current project handles professional jargon but not normative variants | `ADD_NORM_POLICY` | explicit current-professional-variant rule; verify modern source per item |
| CHK-R37 familiar/home register situation-dependent | author profile partially covers informal register | `REFINE` | scene layer; do not literalize source's absolute “outside normalization” wording |
| CHK-R38 evidence-based normalization vs taste | strong in `evidence-audit.md` | `ALREADY_COVERED + REFINE` | link historical-source policy and keep intuition as candidate, not mandatory verdict |

## Integration totals

A rule can have more than one implementation target, so these categories are not a partition of 38.

- substantially already covered before integration: R04, R11, R13, R28, R38;
- existing rule requires material refinement: R01, R04–R08, R10–R13, R19, R21, R23, R26–R28, R30, R33–R34, R37–R38;
- new explicit positive/core workflow operation: R02, R09, R14–R18, R21–R22, R24, R31, R35–R36;
- model/reference only because surface automation would overclaim: R03, R12–R13, R16, R20–R21, R23, R26–R29, R31–R38;
- safe surface-linter candidate: R09, R15, R17–R19, R22, R24–R25;
- source claim deliberately rejected/downgraded rather than integrated: moral/intellectual slang causation, absolute idiom invariability, aesthetic-only morphology causation, whole historical dictionary as current norm.

## Production rule families after integration

### `NORM-HISTORICAL-VERIFY`

A historical prescription is evidence about a historical norm debate, not current authority. Before correction, classify the phenomenon and verify a current authoritative source and recognized register/variant.

### `NORM-PROFESSIONAL-VARIANT`

A current authoritative source may recognize a professional variant. Keep it only inside the relevant professional scope; do not universalize it into general literary norm.

### `NATIVE-ELLIPSIS-REANALYSIS`

Before “restoring” an omitted complement, distinguish contextual ellipsis from a lexical/syntactic construction that genuinely does not contain that argument.

### `EDIT-REGISTER-FIT`

Determine speaker, addressee, genre and purpose before simplifying vocabulary. Preserve functional official/professional/familiar language; flag leakage only when the register has no function.

### `EDIT-DIRECT-NAME`

Compare a prestige/abstract classifier with the ordinary exact noun. Prefer the direct noun only when the classifier adds no real classification, legal or technical distinction.

### `EDIT-ACTION-RECOVERY`

For dense nominal packaging, reconstruct `actor → action → object/result` before polishing. Never invent an unknown actor.

### `EDIT-MODIFIER-SUBTRACTION`

Delete a modifier in an A/B copy and ask what semantic distinction disappears. Keep scope, contrast, degree, time, stance and technical classification.

### `EDIT-METADISCOURSE-DELETE-TEST`

Compare with/without an announcing frame. Keep it only if it contributes real modality, warning hierarchy, navigation or contrast.

### `EDIT-PROPOSITION-FIRST`

When generic evaluation substitutes for content, surface the source-supported proposition/observation first. If the source does not contain the proposition, do not invent it.

### `EDIT-TEMPLATE-CLUSTER`

A cliché is diagnosed by repeated phrase/function and absent semantic gain, not by one token. Repair the repeated discourse operation, not through random synonym rotation.

### `EDIT-ABBREVIATION-EFFORT`

Judge abbreviations by reader effort: recognition, audience, first-use expansion, pronunciation and actual economy—not by length alone.

### `EDIT-PROSODY-PASS`

After semantic reconstruction, compare aloud for accidental echo, clumsy cadence and lost emphasis. Prosody is a comparison dimension, not a numerical gate.

### `SEM-IDIOM-BOUNDARY`

Before `SEM-METAPHOR-CONFLICT` or `SEM-COLLOCATION`, determine whether the expression is lexicalized. A fixed idiom is processed as a unit. Conventional variants and deliberate modifications exist; free synonym substitution is not allowed.

### `SEM-IDIOM-MUTATION`

For a deviated idiom compare two hypotheses: intentional reactivation vs accidental contamination. Preserve the first when the base model and added effect are recoverable; correct/request context for the second.

## Linter boundary

The deterministic linter must not decide:

- current norm of a historical dictionary pair;
- whether a professional variant is current;
- whether an idiom is fixed or creatively modified;
- speaker sincerity or moral/intellectual qualities;
- semantic roles in a syntactically ambiguous chain;
- final register fit;
- whether prosody is aesthetically good;
- whether a term is understandable to a specific audience without audience metadata.

It may emit `EDITING_SUGGESTION` for surface places where the model/editor should run one of the tests above. These suggestions never fail the publication gate.

## Independent-study material retained outside production rules

`studies/chukovsky-zhivoy-kak-zhizn/` remains the provenance-rich source of truth for:

- all 22 concepts;
- all 38 atomic rules;
- 33 counterexample boundary families;
- 20 interaction groups;
- 30 audited claim groups;
- 58 original direct/compound evals;
- source/coverage/loss/overgeneralization audits.

Production files intentionally remain smaller; integration must not make `SKILL.md` a substitute copy of the study.
