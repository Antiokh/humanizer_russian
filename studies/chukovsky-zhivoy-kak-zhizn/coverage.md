# Coverage map — «Живой как жизнь»

This file tracks **sequential reading of the supplied EPUB**, not semantic-search coverage.

The source was read contiguously from `SRC:L1` through `SRC:L4530`. A previously truncated reader window around the middle of chapter 3 was explicitly re-read from `SRC:L840`, so the final sequence has no unlisted gap.

Allowed statuses: `READ`, `EXTRACTED`, `VERIFIED`, `NO_OPERATIONAL_CONTENT`. Every row below is now `VERIFIED` because concepts, atomic rules, counterexamples, interactions, claims, eval mapping, loss audit and overgeneralization audit have all been completed.

| # | Source section | Status | Exact source range | Operational content captured for extraction | Unavailable material |
|---|---|---|---|---|---|
| 0 | Front matter | VERIFIED | `SRC:L1-L36` | title/edition/source framing | none |
| 1 | Гл. 1 «Старое и новое» | VERIFIED | `SRC:L37-L439` | language change vs present norm; generational bias; adoption/usage; semantic shift; contextual ellipsis; innovation + continuity | none |
| 2 | Гл. 2 «Мнимые болезни и подлинные» | VERIFIED | `SRC:L440-L664` | diagnosis before prohibition; multiple alleged “diseases”; social/personal bias in judgments; dynamic language but nonzero norm | none |
| 3 | Гл. 3 «Иноплеменные слова» | VERIFIED | `SRC:L665-L1000` | borrowing by need/precision; assimilation; audience; register; context; anti-category judgments | none |
| 4 | Гл. 4 «Умслопогасы» | VERIFIED | `SRC:L1001-L1342` | abbreviations/splinters; economy; pronounceability; uptake; organic vs bureaucratic formation; register; authorial innovation | none |
| 5 | Гл. 5 «Вульгаризмы» | VERIFIED | `SRC:L1343-L1529` | character voice vs author voice; slang as group/register phenomenon; time-bounded vocabulary; expressive migration; cause vs surface | none |
| 6 | Гл. 6 «Канцелярит» | VERIFIED | `SRC:L1530-L2008` | functional official style vs register leakage; prestige inflation; nominalization; redundant modifiers; semantic opacity; stock frames; sound/read-aloud diagnostics | none |
| 7 | Гл. 7 «Школьная словесность» | VERIFIED | `SRC:L2009-L2159` | template clusters; generic judgment replacing observation; individuality vs schema; concrete vs abstract; own judgment; intonational literacy | none |
| 8 | Гл. 8 «Наперекор стихиям» | VERIFIED | `SRC:L2160-L2275` | current norm and explicit correction; possibility/limits of deliberate normalization; collective language policy; broad cultural claims | none |
| 9 | Гл. 9 «О складе и ладе» | VERIFIED | `SRC:L2276-L2472` | normative conservatism + change; nonliteral language; logic vs established usage; expressive redundancy; rhythm/phonetics; economy is not mere word deletion | none |
| 10 | Гл. 10 «О пользе невнимания и забвения» | VERIFIED | `SRC:L2473-L2677` | lexicalization; semantic bleaching; idiom holism; etymology vs current meaning; deliberate idiom deformation vs accidental contamination | none |
| 11 | Приложение «Новый русский язык» | VERIFIED | `SRC:L2678-L2758` | historical snapshot of accelerated lexical compression/change; descriptive collection over blanket condemnation | none |
| 12 | «Словарь» | VERIFIED | `SRC:L2759-L4146` | historical prescriptive pairs; explicit professional and familiar-register caveats; mixed phenomena requiring current verification | none |
| 13 | Примечания | VERIFIED | `SRC:L4147-L4530` | provenance for examples/claims; qualifications and later comments, including the warning that even expressive formulas can become bureaucratic templates | none |

## Sequential-read log

Contiguous windows used in the final pass:

- `SRC:L1-L500`
- `SRC:L501-L839` plus explicit recovery read beginning at `SRC:L840`
- `SRC:L840-L1099`
- `SRC:L1100-L1359`
- `SRC:L1360-L1619`
- `SRC:L1620-L1879`
- `SRC:L1880-L2139`
- `SRC:L2140-L2399`
- `SRC:L2400-L2659`
- `SRC:L2660-L2919`
- `SRC:L2920-L3419`
- `SRC:L3420-L3919`
- `SRC:L3920-L4419`
- `SRC:L4420-L4530`

No source section is unavailable in the supplied EPUB.

## Coverage gate

Book-level source coverage: `100% VERIFIED`.

- first source line: `SRC:L1`
- last source line: `SRC:L4530`
- unlisted gaps: none
- unavailable chapters/appendices/dictionary/notes: none

The independent completion evidence is in `audit.md`. Integration is tracked separately in `integration.md` and does not retroactively define the independent findings.
