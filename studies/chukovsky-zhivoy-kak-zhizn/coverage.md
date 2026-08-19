# Coverage map — «Живой как жизнь»

This file tracks **sequential reading of the supplied EPUB**, not semantic-search coverage.

The source was read contiguously from `SRC:L1` through `SRC:L4530`. A previously truncated reader window around the middle of chapter 3 was explicitly re-read from `SRC:L840`, so the final sequence has no unlisted gap.

Allowed statuses: `UNREAD`, `READ`, `EXTRACTED`, `VERIFIED`, `NO_OPERATIONAL_CONTENT`. Every row below is now `VERIFIED` because concepts, atomic rules, counterexamples, interactions, claims, eval mapping, loss audit and overgeneralization audit have all been completed.

`C/R/CLM` counts below mean concepts / atomic rules / claim groups linked to that section. An item can legitimately appear in more than one chapter when the source develops it across chapters, so column totals are not expected to equal the global unique counts.

Last complete recheck: `2026-08-19`.

| # | Source section | Status | Exact range | Main task / operational ideas | Linked C/R/CLM | Material flags | Unresolved after audit | Last recheck | Unavailable |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Front matter | VERIFIED | `SRC:L1-L36` | establish edition/source framing | `0/0/0` | bibliographic, historical framing | none | 2026-08-19 | none |
| 1 | Гл. 1 «Старое и новое» | VERIFIED | `SRC:L37-L439` | distinguish language change from present norm; catch generational bias; model adoption; distinguish contextual ellipsis from lexical change | `4/5/3` | historical + general + spoken/written | quantitative threshold for “established” innovation remains unresolved | 2026-08-19 | none |
| 2 | Гл. 2 «Мнимые болезни и подлинные» | VERIFIED | `SRC:L440-L664` | diagnose mechanism before calling novelty a disease; preserve both change and current norm | `2/4/2` | historical + meta-normative | no numeric adoption criterion | 2026-08-19 | none |
| 3 | Гл. 3 «Иноплеменные слова» | VERIFIED | `SRC:L665-L1000` | separate functional borrowing from prestige borrowing; make audience/context part of lexical judgment | `2/3/2` | audience-specific + professional + historical | no universal audience-comprehension threshold | 2026-08-19 | none |
| 4 | Гл. 4 «Умслопогасы» | VERIFIED | `SRC:L1001-L1342` | distinguish useful compression from opaque aggregation; assess uptake, pronunciation, register; reject class-wide bans on formations | `2/3/1` | historical + professional + word-formation | causal effect of pronounceability on survival not established | 2026-08-19 | none |
| 5 | Гл. 5 «Вульгаризмы» | VERIFIED | `SRC:L1343-L1529` | preserve character/community voice; distinguish slang marker from person-level inference; separate linguistic symptom from extra-linguistic cause | `2/3/6` | social/register + spoken + historical | strong slang→mind/morality causation contested; universal jargon claim unresolved | 2026-08-19 | none |
| 6 | Гл. 6 «Канцелярит» | VERIFIED | `SRC:L1530-L2008` | distinguish functional official style from leakage; expose prestige inflation; recover actions/roles; test modifiers/metadiscourse; diagnose template clusters and acoustic heaviness | `6/12/3` | genre-specific + official + scientific/technical + syntax | no calibrated nominalization threshold; legal necessity of individual formulas requires domain sources | 2026-08-19 | none |
| 7 | Гл. 7 «Школьная словесность» | VERIFIED | `SRC:L2009-L2159` | distinguish word from stamp; preserve individuality; put concrete engagement before boilerplate; distinguish correctness from richer verbal quality | `3/6/3` | educational + analytical + document-level | psychological causal claim about templates and thought unresolved | 2026-08-19 | none |
| 8 | Гл. 8 «Наперекор стихиям» | VERIFIED | `SRC:L2160-L2275` | record that source also advocates correction/normalization; separate current norm from historical prescription; isolate language-policy and culture claims | `1/2/4` | historical + policy + normative | strong mass-language-policy causation unresolved; person-level culture/intellect claims rejected for production | 2026-08-19 | none |
| 9 | Гл. 9 «О складе и ладе» | VERIFIED | `SRC:L2276-L2472` | hold norm conservatism and language change together; distinguish literal logic from usage; preserve expressive redundancy; use sound/rhythm as comparison dimension | `3/4/4` | historical + prosodic + stylistic | aesthetic-only causal account of morphology contested; no euphony metric | 2026-08-19 | none |
| 10 | Гл. 10 «О пользе невнимания и забвения» | VERIFIED | `SRC:L2473-L2677` | model semantic bleaching/lexicalization; treat idiom holistically; distinguish deliberate idiom deformation from accidental contamination; keep fresh semantic collision separate | `4/6/6` | phraseological + diachronic + author-specific | absolute idiom invariability rejected; conventional variants require current phraseological evidence | 2026-08-19 | none |
| 11 | Приложение «Новый русский язык» | VERIFIED | `SRC:L2678-L2758` | historical snapshot of rapid lexical compression/change; prefer descriptive collection over blanket condemnation | `3/4/1` | historical + lexical + descriptive | historical anecdotes/counts not exhaustively fact-checked because no rule depends on them | 2026-08-19 | none |
| 12 | «Словарь» | VERIFIED | `SRC:L2759-L4146` | treat `нельзя → надо` pairs as heterogeneous historical norm candidates; apply professional/familiar caveats before any current use | `2/3/3` | historical + normative + professional + familiar | current status of every individual pair intentionally remains unverified; each requires item-level current authority before production use | 2026-08-19 | none |
| 13 | Примечания | VERIFIED | `SRC:L4147-L4530` | preserve provenance and later qualifications; capture the counterexample that an originally expressive formula can become a bureaucratic stamp | `1/2/1` | historical + provenance + boundary material | individual historical publication/count claims verified only when later operationally needed | 2026-08-19 | none |

## Pass-1 extraction ledger

The sequential reading recorded, for every section, the framework-required categories:

- **main task** — compressed into the `Main task / operational ideas` column above;
- **new concepts** — traced through `concepts.md` and the `C` count;
- **candidate rules** — traced through `rules.md` and the `R` count;
- **exceptions / boundary examples** — consolidated in every rule card and `counterexamples.md`;
- **positive models** — encoded as each rule's original `Positive example` plus preservation evals;
- **cross-references** — normalized by mechanism in `interactions.md`;
- **claims for external verification** — traced through `claims.md` and the `CLM` count.

The study does not reproduce source examples chapter-by-chapter; boundary information is retained through independent examples and provenance locators instead.

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

## Global unique extraction counts

- concepts: `22`;
- atomic rules: `38`;
- claim groups: `30`;
- counterexample boundary families: `33`;
- interaction groups: `20`;
- independent original evals: `58` (`38` direct + `20` compound).

## Coverage gate

Book-level source coverage: `100% VERIFIED`.

- first source line: `SRC:L1`;
- last source line: `SRC:L4530`;
- unlisted gaps: none;
- unavailable chapters/appendices/dictionary/notes: none;
- every source section has operational status and unresolved list;
- every section has last-recheck date;
- every decision-relevant chapter contribution is mapped onward into concepts/rules/claims or explicitly retained as historical/provenance material.

The independent completion evidence is in `audit.md`. Integration is tracked separately in `integration.md` and does not retroactively define the independent findings.
