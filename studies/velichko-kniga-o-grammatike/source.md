# Source inventory — А. В. Величко (ред.), «Книга о грамматике»

Study status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

## Scope decision

The integration request originally named the later monograph «Книга о грамматике. Лингводидактические основы преподавания русского языка как иностранного». The only digital source available in the task is an earlier, truncated DOCX. On `2026-08-20` the user explicitly confirmed that this is the complete digital material available to them and that no other version was found.

Therefore this study is intentionally **re-scoped to the supplied 2004 fragment**. It may become operational for the material physically present in the file, while preserving a hard provenance boundary: chapters absent from the file are `UNAVAILABLE` and are never reconstructed from the table of contents, model knowledge, or another edition.

This status means “operational for 100% of the available fragment”, **not** “the complete 816-page book has been processed”.

## Supplied source

- Uploaded file: `velichko_av_red_kniga_o_grammatike_russkii_iazyk_kak_inostra.docx`
- Title inside file: «Книга о грамматике: Русский язык как иностранный»
- Editor: А. В. Величко
- Edition: 2nd corrected and expanded edition
- Publisher: Издательство Московского университета
- Year: 2004
- ISBN: `5-211-05040-1`
- Claimed full-volume extent: 816 pp.
- Actual supplied body: front matter, preface, introduction, chapters 1–13; ends at printed pp. 174–175
- Rendered source-reader representation: 98 pages / 6330 lines
- DOCX structure checked: 2257 paragraphs; 1882 non-empty paragraphs; 4 tables; 234 sections
- Embedded page-image media: none
- SHA-256: `bed226342fc11ce67df63281a8581a37cf4e13f8d838225c962294ff3640c5d8`

## Completeness boundary

The table of contents advertises chapters 1–44. Bodies for chapters 14–44 are absent. The body contains chapter headings only for chapters 1–13 and terminates after the bibliography of chapter 13.

Coverage facts used throughout the study:

- available chapter bodies: **13 / 44**;
- unavailable advertised chapter bodies: **31**;
- sequential coverage of physically available body: **100%**;
- coverage of the advertised full book: **partial and explicitly incomplete**.

## Locator policy

Primary source locators use zero-based `python-docx` paragraph indexes for this exact file:

`DOCX2004:P<start>-P<end>`

Single-paragraph locators use `DOCX2004:P<n>`. These locators are edition- and file-specific.

The source-reader line space `SRC2004:L1-L6330` is retained as a secondary reproducibility aid but production cards use paragraph locators because they map cleanly to the DOCX structure.

## Available internal structure

1. Предисловие
2. Введение — «Что такое грамматика РКИ»
3. Гл. 1 — Структурные схемы (модели) простого предложения
4. Гл. 2 — Регулярные реализации простого предложения
5. Гл. 3 — Фразеологизированные структуры русского предложения
6. Гл. 4 — Глагольно-личные предложения
7. Гл. 5 — Инфинитивные и номинативные предложения
8. Гл. 6 — Безличные предложения
9. Гл. 7 — Согласование подлежащего и сказуемого при количественных сочетаниях
10. Гл. 8 — Глагольное и именное управление
11. Гл. 9 — Пассивные структуры
12. Гл. 10 — Основные структуры языка науки
13. Гл. 11 — Причастие и причастный оборот
14. Гл. 12 — Деепричастие и деепричастный оборот
15. Гл. 13 — Вводные слова

Advertised but absent: chapters 14–44, including the dedicated chapters on functional-semantic relations, negation, word order, aspect, motion verbs, reflexives, full/short adjectives, secondary tense/aspect meanings, number and animacy.

## Provenance and copyright policy

The public repository stores derived observations, distinctions, counterexamples, original evals, locators and verification notes. It does not reproduce long source passages or reconstruct missing chapters.

`VEL-*` IDs exist only in the study/provenance layer. Integrated Russian rules receive source-neutral `RU-*` IDs and `phenomenon_id` values under `libraries/russian/`; no fictional “Velichko reviewer” is created.
