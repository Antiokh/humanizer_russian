# Integration pass — independent Chukovsky study → current humanizer_russian

Status: `INTEGRATION_APPLIED_PENDING_REVIEW`.

This file was created **after** `audit.md` marked the independent study complete. The branch was then merged forward to the current mechanical-first `main`, and the production integration was rebuilt on top of that architecture instead of preserving an older runtime snapshot.

## Current architecture constraint

The current project is mechanical-first:

1. `scripts/check.py` default mode exposes only high-precision mechanical findings;
2. `scripts/check.py --extended` exposes softer contextual/style/AI findings;
3. contextual rules live primarily in reference/model layers;
4. a new regex does not become default runtime merely because it can be written.

Chukovsky integration therefore **does not expand `MECHANICAL_RULES`**. Its surface checks are `EDITING_SUGGESTION` visible in extended/linter output only.

## Integration principles

1. `USER_INTENT`, `SEMANTICS` and current `NORM` remain hard constraints.
2. A historical book does not become a 2026 normative authority merely by being influential.
3. Chukovsky contributes chiefly:
   - register/audience diagnostics;
   - positive editing operations;
   - anti-purist boundary conditions;
   - rhythm/read-aloud diagnostics;
   - lexicalization/idiom boundaries;
   - evidence discipline for historical prescriptions.
4. Surface regex may emit only soft candidates for these phenomena. It must not infer final register fit, idiom status, sincerity, personality, semantic roles or current norm.
5. Independent rule/eval IDs remain in `studies/...`; production-facing rules are expressed as semantic/editorial operations.

## Mapping of all 38 independent rules

| Independent rule | Coverage before integration | Integration decision | Production destination |
|---|---|---|---|
| CHK-R01 generational taste ≠ current norm | partial | `REFINE` | historical/current-norm gate in `SKILL.md`, `russian-language.md`, `chukovsky.md` |
| CHK-R02 classify innovation before judging | not explicit | `ADD_REFERENCE` | classification step in `chukovsky.md`; current-norm workflow in SKILL |
| CHK-R03 current meaning ≠ etymology | missing | `ADD_REFERENCE` | lexicalization boundary in Russian/Chukovsky references |
| CHK-R04 recoverable ellipsis | strong | `REFINE` | explicit `recoverable ≠ must delete` |
| CHK-R05 ellipsis vs lexical reanalysis | partial | `REFINE` | `russian-language.md` + SKILL |
| CHK-R06 borrowing by semantic work | partial | `REFINE` | term/audience test |
| CHK-R07 terminology by audience | partial | `REFINE` | scene/register stage |
| CHK-R08 lexical fit by scene | partial | `REFINE` | scene/register stage |
| CHK-R09 abbreviation by reader effort | missing | `ADD` | Chukovsky reference + extended linter candidate |
| CHK-R10 no class-wide formation bans | implicit | `REFINE` | Chukovsky reference |
| CHK-R11 character/professional voice | strong | `REFINE` | speaker-role-scene wording |
| CHK-R12 no person diagnosis from one slang marker | partial | `ADD_BOUNDARY` | Chukovsky reference + SKILL final control |
| CHK-R13 symptom ≠ cause | strong semantic guardrail | `REFINE` | Chukovsky inference boundary |
| CHK-R14 preserve functional official formulas | missing | `ADD` | register stage |
| CHK-R15 official-register leakage | partial | `ADD + EXTENDED_SOFT` | `EDITING_SUGGESTION` bureaucratic cluster |
| CHK-R16 direct noun vs prestige classifier | missing | `ADD_MODEL` | direct-name A/B test |
| CHK-R17 recover action from nominal packaging | warning only | `ADD + EXTENDED_SOFT` | action recovery + nominalization candidates |
| CHK-R18 semantic subtraction for modifiers | missing | `ADD + EXTENDED_SOFT` | modifier A/B test |
| CHK-R19 stamps by repeated function | AI clustering partially | `REFINE + EXTENDED_SOFT` | editing cluster before provenance inference |
| CHK-R20 cliché ≠ insincerity | missing | `ADD_BOUNDARY` | model/reference only |
| CHK-R21 proposition before evaluation | Nora partly | `REFINE` | proposition-first/no-invention |
| CHK-R22 read aloud after semantics | missing | `ADD + EXTENDED_SOFT` | prosody pass + ending-echo candidate |
| CHK-R23 dependency/case ambiguity, not counts | already warns against counts | `REFINE_MODEL` | role reconstruction; no regex case-count gate |
| CHK-R24 metadiscourse deletion test | previously AI-family heuristic | `CORRECT + EXTENDED_SOFT` | remove single announcement from AI attribution; emit A/B suggestion |
| CHK-R25 `вопрос` packaging | missing | `EXTENDED_SOFT` | repeated procedural-shell candidate |
| CHK-R26 preserve subject individuality | author layer partial | `ADD_REFERENCE` | document-level template/function test |
| CHK-R27 ground interpretation before boilerplate | Nora partial | `REFINE` | proposition/inference boundary |
| CHK-R28 correctness not sufficient | architectural premise | `REFINE` | explicitly reject synonym/richness score |
| CHK-R29 conventional expression vs literal logic | missing | `ADD_REFERENCE` | lexicalization check |
| CHK-R30 expressive redundancy | native repetition already | `REFINE` | prosody/idiom function before deletion |
| CHK-R31 sound/rhythm as comparison, not formula | missing | `ADD_MODEL` | post-semantic read-aloud, no score |
| CHK-R32 idiom as lexical whole | missing in Nora layer | `ADD_NORA_BOUNDARY` | `SEM-IDIOM-BOUNDARY` |
| CHK-R33 deliberate idiom deformation | general humor exception only | `REFINE_NORA` | preserve recoverable deliberate modification |
| CHK-R34 play vs contamination | weak | `REFINE_NORA` | two-hypothesis diagnostic, unresolved allowed |
| CHK-R35 historical prescription → current verification | evidence policy partial | `ADD_NORM_POLICY` | SKILL + Russian reference |
| CHK-R36 professional variant scoped | jargon only, not norm variant | `ADD_NORM_POLICY` | current-authority + professional scope |
| CHK-R37 familiar/home register | author layer partial | `REFINE` | scene layer; source's absolute exemption weakened |
| CHK-R38 evidence-based norm vs taste | strong | `REFINE` | explicit historical-source provenance |

## Production rule families after integration

### `NORM-HISTORICAL-VERIFY`

Historical prescription → classify phenomenon → verify current authoritative norm → check recognized variant/register → decide.

### `NORM-PROFESSIONAL-VARIANT`

A current professional variant is preserved only inside the relevant professional scope and only after current verification.

### `NATIVE-ELLIPSIS-REANALYSIS`

Before restoring a missing complement, distinguish contextual ellipsis from a construction with its own current lexical/syntactic valency.

### `EDIT-REGISTER-FIT`

Determine speaker, addressee, genre and purpose before lexical simplification. Preserve functional official/professional/familiar forms; flag leakage only where function is absent.

### `EDIT-DIRECT-NAME`

Compare prestige/abstract classifier with the exact ordinary noun. Prefer direct naming only when no technical/legal/taxonomic distinction disappears.

### `EDIT-ACTION-RECOVERY`

For dense nominal packaging, reconstruct `actor → action → object/result` before stylistic polishing. Do not invent an unknown actor.

### `EDIT-MODIFIER-SUBTRACTION`

A/B without the modifier; keep scope, contrast, degree, time, stance, terminology and expressive function.

### `EDIT-METADISCOURSE-DELETE-TEST`

A/B with/without the announcing frame; retain real modality, warning hierarchy, navigation and contrast.

### `EDIT-PROPOSITION-FIRST`

Replace generic evaluative shell with the source-supported proposition/observation when it exists. Never fabricate specificity.

### `EDIT-TEMPLATE-CLUSTER`

Diagnose repetition of phrase/function/document operation plus absent semantic gain, not one token. Fix the operation rather than rotating synonyms.

### `EDIT-ABBREVIATION-EFFORT`

Judge abbreviation by reader effort and audience, not character count alone.

### `EDIT-PROSODY-PASS`

After semantic reconstruction, compare aloud for accidental echo, clumsy cadence or lost emphasis. Prosody is not a numeric gate.

### `SEM-IDIOM-BOUNDARY`

Before metaphor/collocation repair, determine whether the expression is lexicalized. Potukhshaya internal metaphor is not a fresh metaphor conflict.

### `SEM-IDIOM-MUTATION`

Compare intentional reactivation with accidental contamination. Preserve motivated, recoverable play; correct/request context when no effect is recoverable.

## Actual code/runtime integration

### Default mechanical mode

Unchanged in principle. `scripts/check.py` still filters to the existing `MECHANICAL_RULES` and does not expose Chukovsky soft candidates by default.

### Extended/linter mode

`scripts/chukovsky_checks.py` is imported by `scripts/lint.py` and emits only `EDITING_SUGGESTION` for:

- metadiscourse deletion test;
- bureaucratic-register cluster;
- light verb + nominalization;
- nominalization cluster;
- modifier subtraction candidate;
- evaluative-template cluster;
- fresh abstract collision candidate;
- repeated `вопрос` packaging;
- abbreviation-density candidate;
- ending-echo read-aloud test.

False-positive tightening applied during integration:

- a single `важно отметить` is no longer attributed to AI; it gets an editing A/B suggestion;
- one ordinary connector such as `кроме того` is not enough for an AI-family finding;
- softer AI phrase families require family-specific clustering;
- a bare process noun such as `осуществление проекта` does not satisfy light-verb + nominalization;
- one formal marker is insufficient for register-leak candidate;
- no case-count, idiom, current-norm, sincerity or personality verdict is done by regex.

### Tests

- `scripts/lint.py --self-test` covers Chukovsky integration and negative controls;
- `scripts/benchmark_lint.py` still checks the unchanged mechanical-default benchmark;
- `scripts/validate_book_study.py` structurally checks 100% coverage, unique IDs, rule-card fields, source locators, direct rule eval coverage and compound interaction eval coverage;
- `evals/chukovsky.json` contains 30 production integration scenarios;
- independent `studies/.../evals.json` contains 58 scenarios and remains provenance/evaluation material rather than runtime payload.

## What the linter is explicitly forbidden to decide

- current norm of a historical dictionary pair;
- whether a professional variant is current;
- final register fit;
- semantic roles in an ambiguous dependency chain;
- whether an idiom is conventional or deliberately modified without context/resource support;
- sincerity, intelligence, morality or psychological traits;
- aesthetic quality of prosody;
- audience comprehension without audience metadata.

## Claims deliberately rejected/downgraded during integration

Not transferred as production facts:

- slang → moral/intellectual impoverishment;
- isolated slang → person diagnosis;
- aesthetic taste as sole/primary explanation of suffix/allomorph selection;
- absolute idiom invariability;
- numerical nominalization/euphony/richness/humanity thresholds;
- whole historical `Словарь` as 2026 rewrite map.

## Integration completion conditions

- [x] independent study completed before integration;
- [x] current `main` architecture inspected after independent audit;
- [x] branch merged forward to current mechanical-first `main` before final runtime edits;
- [x] all 38 independent rules mapped;
- [x] production reference added;
- [x] Russian norm/native boundary refined;
- [x] Nora Gal idiom boundary refined;
- [x] SKILL updated without expanding default mechanical mode;
- [x] extended linter integration added;
- [x] production eval suite added;
- [x] structural study validator added to CI;
- [ ] PR-level external review complete;
- [ ] final corpus false-positive calibration complete.

Therefore integration is applied and testable, but the PR intentionally remains draft until the two unchecked review/calibration gates are satisfied.
