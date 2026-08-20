# Source inventory — Величко, «Книга о грамматике»

Study status: `INGESTED`; full-book study is **BLOCKED_BY_SOURCE** and must not advance to `AUDITED` / `OPERATIONAL`.

## Requested source

The integration request names:

- **Title:** «Книга о грамматике. Лингводидактические основы преподавания русского языка как иностранного»
- **Editor:** А. В. Величко
- **Edition identified by the publisher:** Moscow University Press, 2024
- **ISBN:** `978-5-19-011994-7`
- **Extent:** 742 pp. (+ 2 unnumbered pp.)
- **Publisher record:** https://msupress.com/catalogue/books/book/kniga-o-grammatike-lingvodidakticheskie-osnovy-prepodavaniya-russkogo-yazyka-kak-inostrannogo/

This is a collective monograph and is not bibliographically identical to the file supplied in the current task.

## Supplied file

- Uploaded file: `velichko_av_red_kniga_o_grammatike_russkii_iazyk_kak_inostra.docx`
- Format: DOCX
- Size: `396529` bytes
- SHA-256: `bed226342fc11ce67df63281a8581a37cf4e13f8d838225c962294ff3640c5d8`
- Parsed representation: 98 rendered pages / 6330 source-reader lines
- DOCX structure: 2257 paragraphs, 1882 non-empty paragraphs, 4 tables, 234 sections
- Embedded media under `word/media/`: none

The supplied file identifies itself as:

- **Title:** «Книга о грамматике: Русский язык как иностранный»
- **Edition:** 2nd corrected and expanded edition
- **Publisher:** Издательство Московского университета
- **Year:** 2004
- **ISBN:** `5-211-05040-1`
- **Claimed extent:** 816 pp.

Therefore the task currently contains a **different edition/title** from the 2024 monograph named in the request.

## Completeness check of the supplied 2004 file

The DOCX table of contents advertises the complete 2004 book: three sections and chapters 1–44, including the later chapters on word order, aspect, verbs of motion, reflexive verbs, secondary aspect-tense meanings, number and animacy.

The actual body does not contain those chapters. It contains:

- front matter;
- preface;
- introduction «Что такое грамматика РКИ»;
- chapters 1–13 only;
- the bibliography at the end of chapter 13;
- printed pagination ending at **174–175**.

No body heading for chapters 14–44 occurs after chapter 13. Their names occur only in the table of contents. The archive contains no hidden page-image media that could contain the missing pages.

This is therefore a truncated extract of the 2004 edition, not a complete 816-page source.

## Locator policy for the supplied extract

Until the complete target source exists, provisional primary locators use the parsed uploaded-file line space:

`SRC2004:L<start>-L<end>`

Accessible span: `SRC2004:L1-L6330`.

The locator must always carry the `2004` provenance marker. It must not be cited as evidence for the 2024 monograph.

## What is allowed before the blocker is resolved

Allowed:

- source inventory and completeness audit;
- edition comparison;
- coverage map of what is physically available;
- preservation of high-value preliminary observations from chapters 1–13 as **non-operational candidates**;
- independent verification planning.

Not allowed:

- claiming that the requested monograph has been read completely;
- treating TOC-only chapters as read;
- promoting the study to `READ`, `EXTRACTED`, `AUDITED`, or `OPERATIONAL` at book level;
- runtime integration into `libraries/russian` on the basis of this partial source;
- opening the final integration PR;
- silently substituting a 2009/2018/other revision for either the supplied 2004 edition or requested 2024 edition.

## Required resolution

Preferred resolution: provide the **complete 2024 monograph** named in the task (`ISBN 978-5-19-011994-7`).

If the intended target is actually the 2004 second edition, explicitly re-scope the task to that edition and provide the missing body beginning after printed page 175 through the end of the 816-page volume.

Once the complete target source is available, restart Gate A from source fingerprinting and sequential full-book reading. The long-lived branch `velichko` is intentionally retained for that continuation.
