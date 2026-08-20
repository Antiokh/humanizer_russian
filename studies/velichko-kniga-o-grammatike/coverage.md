# Coverage map — Величко, «Книга о грамматике»

This file records source availability before semantic extraction. It deliberately does **not** treat a table-of-contents entry as read content.

Book-level status: `INGESTED / BLOCKED_BY_SOURCE`.

## Locator basis

For the supplied DOCX extract, locators use zero-based `python-docx` paragraph indexes:

`DOCX2004:P<start>-P<end>`

The document has 2257 paragraphs. This locator is edition-specific and must not be transferred to the 2024 monograph.

## Supplied 2004 extract

| # | Section | Availability | Locator | Study status | High-value domains visible | Blocker |
|---|---|---|---|---|---|---|
| 0 | Front matter / TOC | available | `DOCX2004:P0-P110` | READ_FOR_SOURCE_AUDIT | bibliographic data, full advertised 44-chapter structure | TOC is not chapter content |
| — | Предисловие | available | `DOCX2004:P111-P133` | READ_FOR_SOURCE_AUDIT | RKI scope; typical learner errors; method vs linguistic description | none inside extract |
| — | Введение «Что такое грамматика РКИ» | available | `DOCX2004:P134-P213` | READ_FOR_SOURCE_AUDIT | function→form; syntax basis; valency; semantic/function choice; national-specific expression | none inside extract |
| 1 | Структурные схемы простого предложения | available | `DOCX2004:P214-P352` | READ_FOR_SOURCE_AUDIT | subject/predicate models; state/result; impersonal vs two-member organization | none inside extract |
| 2 | Регулярные реализации простого предложения | available | `DOCX2004:P353-P470` | READ_FOR_SOURCE_AUDIT | phase/modality; zero copula; predicate case; semantic restrictions of linking verbs | none inside extract |
| 3 | Фразеологизированные структуры | available | `DOCX2004:P471-P671` | READ_FOR_SOURCE_AUDIT | colloquial native syntactic inventory; pragmatic/intonational restrictions | mostly NATIVE_USAGE / pragmatics, not direct lint |
| 4 | Глагольно-личные предложения | available | `DOCX2004:P672-P751` | READ_FOR_SOURCE_AUDIT | definite/generalized/indefinite-personal; subject omission; excess pronoun learner error | none inside extract |
| 5 | Инфинитивные и номинативные предложения | available | `DOCX2004:P752-P849` | READ_FOR_SOURCE_AUDIT | dative subject; modal aspect choice; nominal existence/event models; learner overuse of two-member clauses | none inside extract |
| 6 | Безличные предложения | available | `DOCX2004:P850-P1067` | READ_FOR_SOURCE_AUDIT | state/event construal; experiencer cases; natural-force constructions; result predicates | none inside extract |
| 7 | Согласование при количественных сочетаниях | available | `DOCX2004:P1068-P1136` | READ_FOR_SOURCE_AUDIT | formal vs semantic agreement; information-structure effects; number variation | NORM claims need current independent verification |
| 8 | Глагольное и именное управление | available | `DOCX2004:P1137-P1239` | READ_FOR_SOURCE_AUDIT | valency, cases, prepositions, motivated/unmotivated government, lexical-semantic restrictions | none inside extract |
| 9 | Пассивные структуры | available | `DOCX2004:P1240-P1409` | READ_FOR_SOURCE_AUDIT | active/passive perspective; action vs state/result; colloquial possessive resultative; learner passive calques | none inside extract |
| 10 | Основные структуры языка науки | available | `DOCX2004:P1410-P1772` | READ_FOR_SOURCE_AUDIT | classification/definition/part-whole/causation/possession; semantic valency; nominalizations and bookish predicates | scientific register must not become universal native preference |
| 11 | Причастие и причастный оборот | available | `DOCX2004:P1773-P2002` | READ_FOR_SOURCE_AUDIT | agreement/head attachment; relative-clause alternation; temporal perspective; passive/result distinction | NORM claims need current independent verification |
| 12 | Деепричастие и деепричастный оборот | available | `DOCX2004:P2003-P2130` | READ_FOR_SOURCE_AUDIT | shared subject; impersonal exceptions; lexicalized/prepositional gerunds; aspect and temporal relation | norm/periphery distinctions require verification |
| 13 | Вводные слова | available | `DOCX2004:P2131-P2256` | READ_FOR_SOURCE_AUDIT | modality, authorization, metatext, theme/rheme placement, scope via position | none inside extract |
| 14–44 | Remaining chapters advertised by the 2004 TOC | **missing** | no body locator | UNAVAILABLE | functional-semantic relations, word order, negation, aspect, motion, reflexives, adjective forms, secondary tense/aspect, animacy, etc. | source physically absent |

The supplied extract ends after the chapter 13 bibliography at printed pages **174–175**.

## Requested 2024 monograph

The requested source is the 2024 collective monograph, ISBN `978-5-19-011994-7`, 742 pages. Its complete body is not present in the uploaded file. The supplied 2004 extract cannot establish sequential coverage of the requested edition.

Therefore:

- requested 2024 full-book coverage: **0% established**;
- supplied 2004 extract availability: front matter + introduction + chapters 1–13 only;
- supplied 2004 advertised chapters 14–44: **unavailable**;
- book-level `READ` status: **forbidden** until a complete target source is supplied.

## Missing high-priority material

The missing body includes precisely several domains prioritized for `humanizer_russian`:

- functional-semantic expression of time, cause, condition, purpose, concession, comparison, possession and modality;
- negation;
- word order / communicative organization;
- verbal aspect as a system;
- motion verbs;
- reflexive verbs;
- full vs short adjectives;
- secondary tense/aspect meanings;
- number and animacy cases.

These cannot be reconstructed from the TOC, from other editions, or from general model knowledge while retaining source provenance.

## Gate result

Gate A fails because source completeness fails before extraction completeness can even be assessed.

No runtime integration, integration matrix, mechanical rule promotion, model-only prompt update, benchmark claim, or final PR should occur until the correct complete source is available.
