# Claims audit — «Живой как жизнь»

Status: `AUDITED`.

This is the canonical claim inventory. Detailed external reasoning and source registry are in `claims-external.md`. A claim remains separate from an operational rule unless the rule has its own source basis and boundaries.

Final external statuses:

- `EXTERNAL_CONFIRMED` — modern authoritative/research source supports the operationally relevant core;
- `EXTERNAL_PARTIAL` — only a weaker/scoped version is supported;
- `EXTERNAL_CONTESTED` — modern evidence/model conflicts with the source's stronger generalization;
- `EXTERNAL_UNRESOLVED` — adequate confirmation was not established; do not operationalize as fact;
- `VALUE_ONLY` — source's evaluative/moral/aesthetic position, not empirical rule;
- `HISTORICAL_ONLY` — retained as source-period evidence only;
- `CURRENT_SAMPLE_VERIFIED` — some concrete modern samples checked, not the historical list as a whole.

| ID | Source claim | Locator | Kind | Final status | Rule consequence |
|---|---|---|---|---|---|
| CLM-01 | Language changes over time in vocabulary, meaning, pronunciation and government | `SRC:L468-L488` | linguistic/general | `EXTERNAL_CONFIRMED` | historical age cannot decide present norm |
| CLM-02 | Durable/widespread uptake can normalize an innovation | `SRC:L286-L313`; `L1183-L1203`; `L2570-L2582` | change/usage | `EXTERNAL_PARTIAL` | qualitative only; no frequency threshold |
| CLM-03 | Contextual ellipsis is a lawful Russian mechanism | `SRC:L369-L376` | grammar/discourse | `EXTERNAL_CONFIRMED` | preserve recoverable omission; classify construction |
| CLM-04 | Audience knowledge changes terminology fit | `SRC:L922-L936` | communication/style | `EXTERNAL_PARTIAL` | audience test, no universal comprehension score |
| CLM-05 | Context/register can reverse the judgment of the same form | `SRC:L937-L949`; `L1195-L1210`; `L1562-L1588` | stylistics | `EXTERNAL_CONFIRMED` | register is upstream of lexical cleanup |
| CLM-06 | Abbreviation survival is partly caused by pronounceability/euphony | `SRC:L1122-L1203` | causal linguistic | `EXTERNAL_UNRESOLVED` | pronounceability may be an editing criterion, not causal law |
| CLM-07 | Slang is often cohort/group-bound and transient | `SRC:L1508-L1524` | sociolinguistic | `EXTERNAL_CONFIRMED` (scoped) | store time/community context; never universalize |
| CLM-08 | Slang can reflect extra-linguistic social/psychological conditions | `SRC:L1471-L1494` | causal sociolinguistic | `EXTERNAL_PARTIAL` | language may index group processes; cause cannot be inferred from token |
| CLM-09 | Habitual rough slang impoverishes thought/feeling | `SRC:L1490-L1510` | psychological causal | `EXTERNAL_CONTESTED` | exclude as operational causal rule |
| CLM-10 | Slang reliably reveals moral/intellectual poverty | `SRC:L1404-L1415`; `L1514-L1524` | person-level inference | `EXTERNAL_CONTESTED` + internally counterexampled | never diagnose person from isolated marker |
| CLM-11 | Only dead languages lack jargon | `SRC:L1514-L1524` | universal rhetoric | `EXTERNAL_UNRESOLVED` | no operational use |
| CLM-12 | Group/professional jargon can migrate into wider vocabulary | `SRC:L1514-L1525` | sociolinguistic/historical | `EXTERNAL_PARTIAL` | migration possible, not inevitable |
| CLM-13 | Stable official formulae are functionally needed in some genres | `SRC:L1562-L1580` | genre/style | `EXTERNAL_PARTIAL` | preserve formal function; legal necessity requires separate domain source |
| CLM-14 | Dense deverbal nominalization is evidence of bureaucratization | `SRC:L1880-L1946` | stylistic diagnostic | `EXTERNAL_UNRESOLVED` quantitatively | soft candidate only; no suffix-count gate |
| CLM-15 | Dependency/case chains can create real role/attachment ambiguity | `SRC:L1880-L1946` | syntax | `EXTERNAL_CONFIRMED` (mechanism) | inspect parse/semantic roles, not case count |
| CLM-16 | Formulaic evaluation can replace independent thought | `SRC:L2017-L2103` | cognitive/educational | `EXTERNAL_UNRESOLVED` as causation | diagnose propositionless prose, not intelligence/thinking ability |
| CLM-17 | Rich vocabulary and varied intonation are necessary for “cultured” speech | `SRC:L2135-L2159`; `L2660-L2677` | quality/value | `VALUE_ONLY` | quality ideal only; no richness metric |
| CLM-18 | Linguistic correctness strongly tracks general culture/intellect | `SRC:L2140-L2159`; `L2660-L2677` | person-level causal/value | `EXTERNAL_CONTESTED` | exclude person-level moral/intellectual inference |
| CLM-19 | Coordinated institutions/media can reshape mass language practice | `SRC:L2160-L2275` | policy/sociolinguistic | `EXTERNAL_UNRESOLVED` in source's strong form | historical/policy claim only |
| CLM-20 | Normative conservatism is necessary for literary continuity | `SRC:L2276-L2342` | systemic/theoretical | `EXTERNAL_PARTIAL` | retain codification+variation tension, not necessity theorem |
| CLM-21 | Established usage can override literal compositional/etymological logic | `SRC:L2343-L2400`; `L2473-L2582` | semantics/phraseology | `EXTERNAL_CONFIRMED` | do not repair lexicalized forms by etymological arithmetic |
| CLM-22 | Rhythm/sound can justify semantic redundancy | `SRC:L2400-L2449` | prosody/style | `EXTERNAL_PARTIAL` | compare variants aloud; do not assert historical causation |
| CLM-23 | Russian suffix/allomorph choices are selected for aesthetic phonetic fitness | `SRC:L2430-L2472` | morphology/phonology causal | `EXTERNAL_CONTESTED` in strong form | modern morphophonological conditioning outranks aesthetic-only explanation |
| CLM-24 | Semantic bleaching/desemanticization is normal | `SRC:L2473-L2604` | lexical semantics | `EXTERNAL_CONFIRMED` | supports lexicalization/idiom boundaries |
| CLM-25 | Idioms are holistic and resist free substitution | `SRC:L2583-L2630`; `L2660-L2677` | phraseology | `EXTERNAL_PARTIAL` | stability yes; absolute “no variants” rejected |
| CLM-26 | Intentional idiom deformation can create effect through recoverable base model | `SRC:L2605-L2671` | phraseology/style | `EXTERNAL_CONFIRMED` (mechanism) | preserve motivated modification; distinguish contamination |
| CLM-27 | The final dictionary's historical prescriptions are current norm | `SRC:L2759-L4146`; caveats `L2762-L2777` | normative list | `CURRENT_SAMPLE_VERIFIED`; whole-list claim rejected | each imported item needs current authoritative verification |
| CLM-28 | Professional communities can maintain scoped norm-divergent variants | `SRC:L2762-L2768` | professional variation | `EXTERNAL_CONFIRMED` | strong scope rule; verify each concrete item today |
| CLM-29 | Familiar/home speech has different normalization constraints | `SRC:L2769-L2777` | register | `EXTERNAL_PARTIAL` | preserve familiar register; source's “not subject to normalization” is too absolute |
| CLM-30 | Historical counts, dates, anecdotes and attestations in the book | multiple; notes `SRC:L4147-L4530` | historical factual | `HISTORICAL_ONLY` unless later used | verify a datum only if an integration/output depends on it |

## Internal contradictions / self-limitations found before external research

1. The strongest anti-slang moral/psychological generalizations (CLM-09/10) are weakened by the book's own explicit examples of talented/decent young people using fashionable slang.
2. The defense of expressive redundancy is limited by a later note showing that an expressive formula can itself become bureaucratic through mechanical repetition.
3. Anti-purism is balanced by a defense of normative conservatism; extracting either half alone misrepresents the book.
4. The final prescriptive dictionary is preceded by professional and familiar-register exceptions, so it is not context-free even on the source's own terms.
5. `Language is not controlled by literal logic alone` does not mean `fresh semantic incoherence is acceptable`; chapter 10 explicitly distinguishes lexicalized historical oddity from a newly produced collision.
6. `Idioms are holistic` does not entail absolute invariability; chapter 10 itself then demonstrates deliberate decomposition, and modern phraseology also recognizes conventional variation.

## External audit outcome

The strongest externally supported transfer candidates are:

- contextual ellipsis as a real grammatical phenomenon;
- temporal/variant character of norm;
- professional variants as scoped variants;
- register-dependent judgments;
- semantic bleaching/desemanticization;
- phraseological stability together with real variation/modification;
- group/social functions of slang and the need to avoid deterministic person-level inference.

The strongest source claims that **must not** be operationalized as facts are:

- slang causing moral/intellectual impoverishment;
- isolated slang proving a person's moral/intellectual quality;
- aesthetic taste as the sole/primary mechanism of suffix selection;
- a fixed numerical nominalization/euphony/richness threshold;
- the whole 1960s prescriptive dictionary as 2026 norm.

See `claims-external.md` for external evidence registry and detailed disposition.
