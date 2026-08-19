# Source inventory — Корней Чуковский, «Живой как жизнь»

Study status: `OPERATIONAL_FOR_INTEGRATION`; sequential reading and independent audit complete.

## Source

- Author: Корней Иванович Чуковский
- Title in EPUB: «Живой как жизнь»
- Publisher metadata: «Зебра Е», Москва
- Year: 2010
- ISBN: 978-5-94663-511-0
- Language: Russian
- Edition note in text: `2-е издание, исправленное и дополненное`
- Uploaded file: `Chukovskiy_Zhivoy-kak-zhizn.311856.fb2.epub`
- MIME/format: EPUB (`application/epub+zip`), apparently converted from FB2
- Source size: 402302 bytes
- SHA-256: `e4db5cef1d6d3483b232020994953aada176f4cde5597d314a0a152428e41bf9`
- EPUB identifier: `urn:uuid:c2b19dcb-dc6c-41a6-a010-2fcaa92da391`
- FB2 source id embedded in OPF: `OOoFBTools-2013-1-29-1-11-46-91`
- FB2 document version: `1.03`
- EPUB conversion metadata: FB2EPUB 0.5.0; conversion date 2026-08-15

## Current-chat primary-source revalidation

Before the integration pass on `2026-08-19`, the EPUB available in the current conversation was reopened directly rather than trusting the previous study artifacts alone.

Revalidation results:

- recomputed SHA-256 exactly matched the recorded fingerprint above;
- EPUB ZIP structure opened successfully;
- OPF metadata was reread directly and matched author/title/publisher/year/ISBN recorded here;
- NCX was reread directly and contained the same 12 top-level TOC entries listed below;
- spine/source sampling confirmed the front matter, ten chapters, appendix, dictionary and notes structure used by `coverage.md`.

This check confirms that the integration is grounded in the same supplied primary source that the independent study claims to cover. It does not replace the sequential-reading evidence in `coverage.md`.

## Bibliographic confidence

High confidence for author/title/publisher/year/ISBN because they are embedded in the supplied EPUB metadata. The text itself identifies the edition only as the second, corrected and expanded edition; this study does not infer a full publication-history stemma from that note.

The core prose repeatedly refers to the 1960s and ends with `1962—1966`, but the supplied file is a 2010 publication. Historical claims and normative judgments are therefore recorded as claims from the source period, not silently treated as 2026 norm.

## Exact internal TOC

The EPUB NCX contains 12 top-level entries:

1. Глава первая — «Старое и новое»
2. Глава вторая — «Мнимые болезни и подлинные»
3. Глава третья — «Иноплеменные слова»
4. Глава четвертая — «Умслопогасы»
5. Глава пятая — «Вульгаризмы»
6. Глава шестая — «Канцелярит»
7. Глава седьмая — «Школьная словесность»
8. Глава восьмая — «Наперекор стихиям»
9. Глава девятая — «О складе и ладе»
10. Глава десятая — «О пользе невнимания и забвения»
11. Приложение — «Новый русский язык»
12. «Словарь»

The EPUB also contains front matter before chapter 1. It is included in sequential coverage because it contains edition/source framing.

## Locator policy

Primary locator for this study: rendered source line range in the uploaded file, whose current parsed representation contains 4530 lines.

Full locator span: `SRC:L1-L4530`.

Format:

`SRC:L<start>-L<end>`

For chapter-level provenance, also include chapter/section (`Гл. 6, II`) when available. EPUB XHTML filename/anchor may be added as a secondary locator, but line ranges are primary because they are directly reproducible through the file reader used for this study.

Do not use semantic-search snippets as evidence of full reading. Sequential coverage is established only by contiguous reads from line 1 through line 4530.

## Completion evidence

- full coverage: `coverage.md`;
- independent loss / overgeneralization / claims audit: `audit.md`;
- explicit re-audit before runtime integration: `re-audit-2026-08-19.md`;
- integration classification: `integration-matrix.md` (created after the study gate).

## Source/copyright policy

The supplied book is used as a research source. Study artifacts preserve operational distinctions, provenance, exceptions, counterexamples, methods, and short locators; they do not reproduce the book chapter by chapter, copy long passages, or attempt to substitute for the original text.

Examples in rules/evals must be original unless a very short source phrase is itself the object of analysis.
