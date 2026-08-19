# Coverage map — «Живой как жизнь»

This file tracks **sequential reading of the supplied EPUB**, not semantic-search coverage.

Allowed terminal statuses: `READ`, `EXTRACTED`, `VERIFIED`, `NO_OPERATIONAL_CONTENT`. A section is not complete while only partially read.

| # | Source section | Status | Sequential coverage | Operational notes | Unresolved |
|---|---|---|---|---|---|
| 0 | Front matter | READ | `SRC:L1-L47` | edition/title framing | none yet |
| 1 | Гл. 1 «Старое и новое» | READ | contiguous read completed | language change; norm vs age/cohort; adoption; usage; ellipsis; innovation vs stability | locators to pin after full read |
| 2 | Гл. 2 «Мнимые болезни и подлинные» | READ | contiguous read completed | semantic drift; dynamic language + stable current norm; diagnosis before prohibition; source/social bias in lexical judgments | locators to pin after full read |
| 3 | Гл. 3 «Иноплеменные слова» | READ | contiguous read completed | borrowing by need/precision/audience/register; assimilation; anti-category judgment | locators to pin after full read |
| 4 | Гл. 4 «Умслопогасы» | READ | contiguous read completed | abbreviation/splinter words; economy; pronounceability; uptake; official invention vs organic adoption; genre fit | locators to pin after full read |
| 5 | Гл. 5 «Вульгаризмы» | READ | contiguous read completed | character voice vs author voice; slang as register; causes vs surface; temporary group vocabulary; expressive exceptions | claims about morality/psychology require audit |
| 6 | Гл. 6 «Канцелярит» | UNREAD | partial only: sequential read has entered chapter and reached `SRC:L1619`; chapter not yet complete | official forms can be functional; register leakage identified | continue from L1620 |
| 7 | Гл. 7 «Школьная словесность» | UNREAD | not yet reached sequentially | — | — |
| 8 | Гл. 8 «Наперекор стихиям» | UNREAD | not yet reached sequentially | — | — |
| 9 | Гл. 9 «О складе и ладе» | UNREAD | not yet reached sequentially | — | — |
| 10 | Гл. 10 «О пользе невнимания и забвения» | UNREAD | not yet reached sequentially | — | — |
| 11 | Приложение «Новый русский язык» | UNREAD | not yet reached sequentially | — | — |
| 12 | «Словарь» | UNREAD | not yet reached sequentially | — | — |

## Coverage gate

Current book-level status: `READ_IN_PROGRESS`.

The study must **not** be called complete until every row above is either `VERIFIED` or explicitly `NO_OPERATIONAL_CONTENT`, and the contiguous read reaches `SRC:L4530` with no unlisted gaps.
