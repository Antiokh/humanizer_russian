# Ilyakhov web supplement — integration matrix

The book study remains the canonical source for `ILY-R01`—`ILY-R102`. This web supplement records later/parallel public material without falsely back-attributing it to the supplied EPUB.

| Web finding | Sources | Relation to book core | Runtime decision |
|---|---|---|---|
| Stop words are prompts to think, not delete commands | IW-S02, S03, S05, S18, S19 | Narrows/reinforces R06, R07 and the native-usage boundary | Reference/model only; never a ban-list |
| Glavred score is not text quality | IW-S02, S19 | Reinforces R01, R04, R05 | Reference/model only |
| Present-time wrappers often hide unsupported generalization | IW-S01 | Extends R21 with R33, R37—R39 interaction | Broaden metric candidate set only |
| Generic corporate praise should be unpacked into observable detail | IW-S10, S11, S14—S16 | Strong examples for R15—R20, R85 | Extend existing R85 candidate lexicon conservatively |
| Company value should have operational consequence/trade-off | IW-S06 | New combination not represented cleanly by one core card | `IW-R01`, MODEL_ONLY |
| Removing pronouns mechanically makes prose unnatural | IW-S03, S04, S13 | Narrows stop-word/general deletion heuristics; reinforces NATIVE_USAGE | Counterexample/guard only |
| Infostyle can itself become a cargo cult | IW-S04, S09 | Cross-cutting guard over R04—R08 | `IW-R02`, MODEL_ONLY |
| Cliché is harmful through information loss, not dictionary membership | IW-S04, S12 | Reinforces R19, R20, R23 | Reference/model only |
| Indefinite words are candidates; preserve genuine uncertainty | IW-S05 | Extends R33, R37, R44 | Reference/model only |
| Bright figurative language needs function, freshness and genre fit; it must not camouflage an empty claim | IW-S07, S08 | Partly overlaps R19/R23 but adds image/function test | `IW-R03`, MODEL_ONLY |
| Common-knowledge wrappers without basis hide missing data | IW-S01, S17 | Reinforces R09/R10/R37—R39/R76 | Existing EXTENDED_SOFT + model context |
| Concision by itself does not produce useful prose | IW-S02, S14 | Reinforces R01—R07/R16/R17 | Reference/model only |
| Terms/adjectives can be legitimate when exact for context | IW-S18 | Reinforces R23/R26/R27/R40 | Counterexample/guard only |
| Tool recommendation is not an automatic correction | IW-S02, S09, S19 | Reinforces R04—R06 and project finding contract | Architecture guard |

## Supplemental rule cards

### IW-R01 — stated value requires operational consequence

- phenomenon: `editing.stated_value_requires_operational_consequence`
- class: `EDITING`
- automation: `MODEL_ONLY`
- trigger: a company/organization states a value mainly as self-evaluation.
- context required: genre, surrounding examples, actual operational evidence supplied by user.
- operation: ask what observable behavior, procedure, limitation or trade-off follows from the value; surface existing evidence rather than inventing it.
- false-positive risk: high if applied to a concise values list whose detailed examples exist elsewhere.
- positive: “Наша главная ценность — прозрачность” with no operational consequence anywhere nearby.
- negative: “Публикуем цены и changelog, потому что для нас важна прозрачность.”
- invariant: never fabricate a company process or value.

### IW-R02 — anti-editorial cargo cult

- phenomenon: `editing.anti_editorial_cargo_cult`
- class: `NATIVE_USAGE`
- automation: `MODEL_ONLY`
- trigger: a rewrite applies a stylistic technique mechanically and makes otherwise normal Russian less natural or less precise.
- operation: compare the edited form with a natural contextual version; restore needed pronouns, connective material, sentence shape or author rhythm.
- false-positive risk: high; requires before/after or obvious local damage.
- positive: deleting every pronoun creates telegraphic fragments.
- negative: removing an actually redundant pronoun without changing meaning or rhythm.
- invariant: this is not permission to preserve empty corporate filler.

### IW-R03 — figure of speech function test

- phenomenon: `editing.figure_of_speech_function_test`
- class: `EDITING`
- automation: `MODEL_ONLY`
- trigger: decorative/metaphorical language in informational or persuasive prose.
- operation: check genre fit, freshness/non-cliché status and whether a meaningful proposition remains under the image.
- false-positive risk: very high in literary, personal, comic and rhetorical genres.
- positive: a grand metaphor replaces evidence for a product claim.
- negative: an original metaphor deliberately carries tone or meaning in an essay.
- invariant: do not flatten author voice merely to make prose look informational.

## Stop-list integration policy

The historical `miripiruni/stop-words` file is evidence that a community stop-word corpus existed around Ilyakhov's material, not evidence that every token is bad or that the list equals the current Glavred database. It may seed candidate discovery and regression research. It may not directly become `DEFAULT_MECHANICAL`, `HARD_GATE`, or an automatic rewrite table.
