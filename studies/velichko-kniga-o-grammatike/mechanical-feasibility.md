# Mechanical feasibility — Velichko 2004 available fragment

Precision-first decision: no new source-derived warning was promoted to regex/default mechanical. The fragment mostly contributes semantic grammar and RKI diagnostics. Three distributional signals are metrics only.

| rule_id | final level | best feasible mechanism | decision |
|---|---|---|---|
| VEL-R01 | `MODEL_ONLY` | lexical valency dictionary + morphology + model fallback | LSV and role assignment remain contextual |
| VEL-R02 | `MODEL_ONLY` | semantic agentivity | subject control/agency required |
| VEL-R03 | `MODEL_ONLY` | semantic agentivity | intention/finality required |
| VEL-R04 | `MODEL_ONLY` | event-semantic model | process/transition/result cannot be read from surface alone |
| VEL-R05 | `MODEL_ONLY` | syntax + discourse | existential/emphatic `есть` must be protected |
| VEL-R06 | `MODEL_ONLY` | discourse coreference + dependency parse | surface `они` is often perfectly natural |
| VEL-R07 | `MODEL_ONLY` | morphology + syntax + modality | dative semantic subject must be distinguished from ordinary dative |
| VEL-R08 | `MODEL_ONLY` | morphology + semantic event model | aspect is visible morphologically but interpretation is contextual |
| VEL-R09 | `MODEL_ONLY` | dependency + semantic roles | natural-force event construal required |
| VEL-R10 | `MODEL_ONLY` | lexical semantics + morphology | experiencer case is predicate-specific |
| VEL-R11 | `MODEL_ONLY` | lexical semantics + syntax | impersonal `-ся` is not a suffix-only class |
| VEL-R12 | `MODEL_ONLY` | morphology + dependency parse | could become mechanical later with reliable subject-head and predicate-number analysis; not regex |
| VEL-R13 | `MODEL_ONLY` | morphology + dependency + discourse | aggregate vs individuated focus required |
| VEL-R14 | `MODEL_ONLY` | dependency + semantic roles | `с + instrumental` can mean coordination or accompaniment |
| VEL-R15 | `MODEL_ONLY` | lexical valency dictionary + morphology + model fallback | fixed government needs lexical evidence |
| VEL-R16 | `MODEL_ONLY` | derivational lexicon + valency | nominalization does not change frames uniformly |
| VEL-R17 | `MODEL_ONLY` | lexical valency dictionary + word-sense disambiguation | polysemy determines frame |
| VEL-R18 | `MODEL_ONLY` | dependency + lexical semantics + register | surface passive form cannot determine appropriateness |
| VEL-R19 | `MODEL_ONLY` | semantic role + discourse | possessor vs agent distinction required |
| VEL-R20 | `MODEL_ONLY` | dependency + lexical semantics + register | action/state/result interpretation required |
| VEL-R21 | `MODEL_ONLY` | semantic relation + register | `являться` cannot be stop-listed |
| VEL-R22 | `MODEL_ONLY` | semantic relation + register | essence vs identity distinction required |
| VEL-R23 | `MODEL_ONLY` | morphology + dependency parse | attachment can be automated only with structural confidence |
| VEL-R24 | `MODEL_ONLY` | morphology + dependency parse | agreement needs the actual syntactic head |
| VEL-R25 | `MODEL_ONLY` | syntax + semantics + register | compression must preserve reference and readability |
| VEL-R26 | `MODEL_ONLY` | discourse temporal model | relative tense can neutralize by text plan |
| VEL-R27 | `MODEL_ONLY` | dependency/control analysis + exception lexicon | semantic subject and exceptions block regex |
| VEL-R28 | `MODEL_ONLY` | lexical/function classification | grammaticalized/prepositional uses must be separated first |
| VEL-R29 | `MODEL_ONLY` | dependency/control analysis + infinitive detection | shared semantic subject must be established |
| VEL-R30 | `MODEL_ONLY` | dependency/control + ambiguity analysis | object-infinitive controller is contextual |
| VEL-R31 | `MODEL_ONLY` | clause scope/discourse model | position changes proposition scope |
| VEL-R32 | `MODEL_ONLY` | clause structure | parenthetic vs complement proposition must be distinguished |
| VEL-M01 | `METRIC_ONLY` | surface statistical proxy | implemented with no threshold and no verdict |
| VEL-M02 | `METRIC_ONLY` | surface statistical proxy | implemented with no threshold and no verdict |
| VEL-M03 | `METRIC_ONLY` | surface statistical proxy | implemented with no threshold and no verdict |

## Promotion summary

- HARD_GATE: 0
- DEFAULT_MECHANICAL: 0
- EXTENDED_SOFT: 0
- METRIC_ONLY: 3
- MODEL_ONLY: 32

This is an intentional result, not missing implementation. The requested precision priority rejects regex approximations for valency, reference, aspect, theme/rheme, semantic subject and passive/stative interpretation.
