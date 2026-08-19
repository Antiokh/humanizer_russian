# Claims audit — Nora Gal source study

This file records source claims that must not silently become runtime rules. Where contemporary verification would be needed, the study says so instead of filling the gap from general knowledge.

The source classifications below are intentionally historical/source-facing. The separate modern evidence pass is `studies/nora-gal/external-evidence-2026.md`; it may narrow or mark a claim testable/obsolete without rewriting what the book itself says.

| ID | Source locator | Claim / source position | Classification | Verification status | Runtime consequence |
|---|---|---|---|---|---|
| `GAL-CLAIM-01` | «Откуда что берется?» | Канцелярит широко распространяется из официальной речи в журналистику, быт и другие регистры. | historical/empirical + rhetorical | `NEEDS_HISTORICAL_CORPUS_IF_ASSERTED` | We can diagnose a concrete chancery construction without asserting prevalence. |
| `GAL-CLAIM-02` | «Куда же идет язык?» | Очень сильная уверенность, что почти всегда можно обойтись без иностранного слова. | historical/editorial preference | `EXTERNAL_CONTESTED_BY_MODERN_DOMAIN_USAGE` | Never turn into foreign-word stop-list; use contextual borrowing/audience rule only. |
| `GAL-CLAIM-03` | «Жечь или сушить?» | Some participial/gerund constructions are treated as alien to ordinary living speech and as a source of dryness. | historical/corpus tendency | `NEEDS_MODERN_GENRE_CORPUS` | Runtime may review overload/clarity, not ban the grammatical forms. |
| `GAL-CLAIM-04` | «… Или Дух?» | Russian logical/emotional stress is said to fall very often near the end. | linguistic/editorial tendency | `PROJECT_REFINED` | Current NATIVE_USAGE controls actual information structure; strong sentence-initial focus remains possible. |
| `GAL-CLAIM-05` | «Веревка — вервие простое» and related passages | Muddy or pretentious wording is repeatedly associated with muddy thought. | psychological/causal | `UNVERIFIED_CAUSAL_CLAIM` | Diagnose the text, not the author's cognition/personality. |
| `GAL-CLAIM-06` | «Буква…» | Historical argument about the inability of machine translation to solve contextual literary translation. | technical/historical | `OBSOLETE_FOR_CURRENT_TECH_WITHOUT_NEW_EVIDENCE` | Do not use in current product claims or automation design. |
| `GAL-CLAIM-07` | «Музыка перевода» | Strong translations are said to age mainly in micro-details while the whole remains alive if the core method is right. | editorial/historical value judgment | `TASTE/HISTORICAL` | Not a runtime rule or measurable quality claim. |
| `GAL-CLAIM-08` | «Пять чувств — и еще шестое» | The language adults/books give children is presented as particularly consequential for the future of language. | educational/causal | `NEEDS_EXTERNAL_EVIDENCE_IF_ASSERTED` | Voice-age/tact rules do not require this causal claim. |
| `GAL-CLAIM-09` | «Для ясности» | Practical comparison of variants is presented as the book's primary method rather than an exhaustive linguistic theory. | methodological/source self-description | `SOURCE_METHOD` | Supports counterexample/eval design; does not define NORM. |
| `GAL-CLAIM-10` | «Кто мы и зачем мы?» | An editor may correctly detect a problem yet propose a poor replacement. | editorial method | `SOURCE_REPEATED` | Supports separation of finding from operation and the third-solution rule. |
| `GAL-CLAIM-11` | «Многоликость таланта», «От миссис Уоррен до Маугли», «От Джойса до Голсуорси», «Свет и сумрак Фицджеральда» | A strong translator changes their own surface manner to serve very different authors. | translation method / positive model | `SOURCE_REPEATED` | Generalized only as a guard against flattening distinct author voices. |
| `GAL-CLAIM-12` | «Музыка перевода» | Rhythmic/functional equivalence can require a different word count and different syntax than the source. | translation method | `SOURCE_REPEATED` | Word count and surface similarity must not be optimization targets by themselves. |
| `GAL-CLAIM-13` | «Предки Адама» | A translator/editor must consult reference sources when a factual/cultural detail is doubtful. | professional method | `SOURCE_DIRECT` | Becomes a verification workflow, not proof that a suspicious phrase is wrong. |
| `GAL-CLAIM-14` | «Мертвый хватает живого», «Куда же идет язык?» | The book contains broad judgments about vocabulary impoverishment and the direction of contemporary language. | historical sociolinguistic judgment | `NEEDS_PERIOD_CORPUS_AND_MODERN_COMPARISON` | Keep out of universal current-language rules. |
| `GAL-CLAIM-15` | «Пять чувств — и еще шестое» | «Truth/humanity/tact» are treated as an essential extra faculty of a writer/editor. | normative-aesthetic meta claim | `SOURCE_VALUE` | Treat as a limit on mechanical certainty, not as a machine-detectable property. |

## 2026 external-evidence disposition

The current external review does **not** overwrite the source-status column above. Its disposition is:

| Claim | 2026 disposition |
|---|---|
| `GAL-CLAIM-01` | `TESTABLE_NOT_YET_MEASURED` |
| `GAL-CLAIM-02` | `REFINED_BY_CURRENT_USAGE/NORM` |
| `GAL-CLAIM-03` | `REFINED_BY_CURRENT_LINGUISTICS` + `TESTABLE_NOT_YET_MEASURED` |
| `GAL-CLAIM-04` | `REFINED_BY_CURRENT_LINGUISTICS` |
| `GAL-CLAIM-05` | `NOT_ESTABLISHED_CAUSALLY` |
| `GAL-CLAIM-06` | `OBSOLETE_AS_ABSOLUTE` |
| `GAL-CLAIM-07` | `VALUE_JUDGMENT` |
| `GAL-CLAIM-08` | `SUPPORTED_NARROWLY` |
| `GAL-CLAIM-09` | `SOURCE_METHOD` |
| `GAL-CLAIM-10` | `SOURCE_METHOD` |
| `GAL-CLAIM-11` | `SUPPORTED_NARROWLY` |
| `GAL-CLAIM-12` | `SUPPORTED_NARROWLY` |
| `GAL-CLAIM-13` | `SOURCE_METHOD` |
| `GAL-CLAIM-14` | `TESTABLE_NOT_YET_MEASURED` |
| `GAL-CLAIM-15` | `VALUE_JUDGMENT` |

See `studies/nora-gal/external-evidence-2026.md` for evidence, limits and URLs. In particular, **the corpus-dependent claims 01/03/14 have not been measured by this project yet**; availability of NKRЯ makes them testable but is not itself a result.

## Claims deliberately not upgraded to NORM

None of the book's stylistic recommendations is sufficient by itself to classify a construction as a modern Russian-language error. `NORM` requires independent normative support from the project's language layer. The integration pass must keep that separation.