# Coverage map — Величко 2004, supplied fragment

Book-level status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

This ledger distinguishes **physical source availability** from advertised table-of-contents coverage. Every available chapter body was read sequentially and audited. Missing chapters remain unavailable.

| # | Section | Availability | Locator | Status | Main operational content | Unresolved / boundary |
|---|---|---|---|---|---|---|
| 0 | Front matter / TOC | available | `DOCX2004:P0-P110` | VERIFIED | bibliographic frame; advertised 44-chapter structure | TOC-only items are not content |
| — | Предисловие | available | `DOCX2004:P111-P133` | VERIFIED | RKI scope; learner errors; grammar vs method | methodological material excluded from lint rules |
| — | Введение «Что такое грамматика РКИ» | available | `DOCX2004:P134-P213` | VERIFIED | function→form; syntax basis; valency; national-specific expression | theoretical school labels not promoted to rules |
| 1 | Структурные схемы простого предложения | available | `DOCX2004:P214-P352` | VERIFIED | subject/predicate models; state/result; one-member resources | some full/short-adjective teaching statements deferred |
| 2 | Регулярные реализации | available | `DOCX2004:P353-P470` | VERIFIED | phase/modality; zero copula; predicate case; agentivity | lexical restrictions remain context/model-only |
| 3 | Фразеологизированные структуры | available | `DOCX2004:P471-P671` | VERIFIED | productive colloquial idiomatic syntax; pragmatic constraints | preservation controls, not normalization targets |
| 4 | Глагольно-личные предложения | available | `DOCX2004:P672-P751` | VERIFIED | definite/generalized/indefinite-personal; omitted actor; explicit-`они` learner error | discourse coreference required |
| 5 | Инфинитивные и номинативные | available | `DOCX2004:P752-P849` | VERIFIED | dative subject; modal aspect; nominal event/existence | `В лесу есть дом` warning narrowed, not banned |
| 6 | Безличные предложения | available | `DOCX2004:P850-P1067` | VERIFIED | experiencer cases; natural-force constructions; result predicates; impersonal `-ся` | lexical semantics required |
| 7 | Количественное согласование | available | `DOCX2004:P1068-P1136` | VERIFIED | formal vs semantic agreement; quantifiers; joint subjects | NORM subset independently verified |
| 8 | Глагольное и именное управление | available | `DOCX2004:P1137-P1239` | VERIFIED | valency; lexical government; nominalization shift; polysemy | needs LSV/context; no regex |
| 9 | Пассивные структуры | available | `DOCX2004:P1240-P1409` | VERIFIED | voice perspective; agentive passive register; possessive resultative; stative/action split | frequency claims kept distributional |
| 10 | Язык науки | available | `DOCX2004:P1410-P1772` | VERIFIED | semantic linking predicates; scientific valency frames; relation templates | scientific register must not become universal native preference |
| 11 | Причастие | available | `DOCX2004:P1773-P2002` | VERIFIED | head attachment; agreement; relative-clause alternation; temporal perspective | NORM subset independently verified |
| 12 | Деепричастие | available | `DOCX2004:P2003-P2130` | VERIFIED | shared subject; impersonal+infinitive exception; grammaticalization; ambiguity | NORM/exceptions independently checked |
| 13 | Вводные слова | available | `DOCX2004:P2131-P2256` | VERIFIED | modality/source/scope; position changes scope | source's `к радости` restriction conflicts with current reference |
| 14–44 | Remaining advertised chapters | **missing** | none | UNAVAILABLE | not inferred | 31 chapter bodies absent |

## Sequential-read evidence

The uploaded document was read contiguously through the source-reader representation `SRC2004:L1-L6330`. The available chapter headings were independently located in the body; chapter 13 is the final body chapter. No chapter 14+ body heading exists after it.

## Extraction totals

For the available fragment:

- concepts: **14**;
- atomic observations/rules: **35**;
- external/teaching/contested claim groups: **12**;
- automation disposition: **32 MODEL_ONLY**, **3 METRIC_ONLY**, **0 HARD_GATE**, **0 DEFAULT_MECHANICAL**, **0 EXTENDED_SOFT**;
- source classes: **5 NORM**, **22 NATIVE_USAGE**, **8 AI_CALQUE**, **0 EDITING** operational rules.

The absence of DEFAULT_MECHANICAL rules is deliberate. The strongest new phenomena in this fragment depend on lexical meaning, semantic subject, discourse scope, aspectual interpretation or register. Precision would be harmed by regex promotion.

## Coverage gate

- 100% of the **physically available fragment**: `VERIFIED`;
- 13/44 advertised chapter bodies available;
- 31/44 advertised chapter bodies: `UNAVAILABLE`;
- no missing body is reconstructed from the TOC;
- study may support bounded integration, but no report may call the 816-page book “fully processed”.
