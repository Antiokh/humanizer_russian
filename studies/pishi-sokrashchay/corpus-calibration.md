# Natural-Russian corpus calibration — Ilyakhov layer

Date: 2026-08-19.

Purpose: test the **mechanical surface implementation**, especially `EXTENDED_SOFT`, against a large sample of ordinary edited Russian before promoting or trusting any additional regex. This is not a source study and does not alter what the book says.

## Corpus

Source: Russian Wikipedia plaintext extracts retrieved through the MediaWiki API by `scripts/calibrate_ilyakhov_corpus.py`.

- 30 fixed articles;
- 218,167 words in the retrieved snapshot;
- domains mixed across science, humanities, law, technology, geography, history and biographies;
- no article text is committed to the repository;
- revision IDs/timestamps are emitted by the calibration tool so the web sample is reproducible as a recorded snapshot rather than presented as immutable.

The one-off GitHub Actions calibration ran successfully in workflow run `32277897923`, job `96149506724`.

## Raw finding counts before calibration changes

| surface rule | hits | hits / 100k words | decision |
|---|---:|---:|---|
| `ilyakhov: bureaucratic tautology` (`ILY-M01`, default) | 0 | 0 | keep default; no false-positive evidence in this corpus |
| `ilyakhov: bureaucratic-shell candidate` | 2 | 0.917 | keep extended only; both hits were in `Право`, exactly the register where a false positive is plausible |
| `ilyakhov: verbal-numbering cluster` | 3 | 1.375 | keep extended only; naturally occurs in structured exposition, so never promote by surface form |
| `ilyakhov: present-time wrapper` | 51 | 23.377 | **demote from finding to metric-only** |
| all other Ilyakhov extended rules | 0 | 0 | no promotion: zero natural-corpus hits do not establish precision on positive cases |

Total source-layer findings before demotion: 56.

### Why `PS-R21` is demoted

The 51 present-time hits appeared throughout ordinary encyclopedic prose (`Физика`, `Биология`, `Психология`, `Русский язык`, `Философия` and others). The previous local-window exception (`раньше`, `ранее`, `теперь` etc. within roughly the surrounding sentence/window) did not capture the larger discourse function: an encyclopedia can legitimately establish a current state after historical material that is farther away.

Therefore the phrase itself is too weak to justify even an `EXTENDED_SOFT` finding. It remains measurable as:

- `ilyakhov_present_time_wrappers`;
- `ilyakhov_present_time_wrappers_without_local_contrast`.

The model/editor may still apply the source idea contextually, but regex does not accuse the phrase.

## Revision snapshot

| article | pageid | revid | revision time | words |
|---|---:|---:|---|---:|
| Математика | 1193 | 150448945 | 2025-12-04T17:37:01Z | 2,136 |
| Физика | 384 | 153208332 | 2026-05-21T08:17:04Z | 3,681 |
| Биология | 68 | 153725539 | 2026-06-27T13:43:16Z | 1,872 |
| Медицина | 2703 | 152924543 | 2026-04-29T21:08:05Z | 2,943 |
| Психология | 1003 | 153222977 | 2026-05-22T09:15:32Z | 4,804 |
| Лингвистика | 20 | 150966703 | 2026-01-02T19:11:49Z | 2,079 |
| Русский язык | 345 | 154480312 | 2026-08-16T16:43:27Z | 13,094 |
| Философия | 4255418 | 154126680 | 2026-07-27T07:29:54Z | 9,432 |
| Право | 30236 | 154264731 | 2026-08-05T22:02:30Z | 5,994 |
| Экономика | 10678 | 153991389 | 2026-07-17T11:36:13Z | 851 |
| Москва | 71 | 154475554 | 2026-08-16T11:08:15Z | 13,501 |
| Санкт-Петербург | 45 | 154516190 | 2026-08-18T08:56:27Z | 13,492 |
| Сербия | 21320 | 154425235 | 2026-08-14T09:39:50Z | 11,110 |
| История России | 23572 | 153790384 | 2026-07-02T11:30:36Z | 20,035 |
| Вторая мировая война | 41 | 154499576 | 2026-08-17T16:02:18Z | 17,005 |
| Интернет | 263 | 154293571 | 2026-08-08T04:22:24Z | 4,567 |
| Программирование | 13024 | 153881756 | 2026-07-09T13:22:24Z | 1,336 |
| Машинное обучение | 471913 | 154089659 | 2026-07-24T15:42:15Z | 1,745 |
| Искусственный интеллект | 2665 | 154454755 | 2026-08-15T15:23:21Z | 10,301 |
| Космическое пространство | 13546 | 154436313 | 2026-08-14T18:01:05Z | 4,971 |
| Солнечная система | 4265 | 154351086 | 2026-08-09T17:51:47Z | 7,852 |
| Железнодорожный транспорт | 2483 | 154340615 | 2026-08-09T16:28:14Z | 5,608 |
| Электроэнергетика | 550725 | 153904045 | 2026-07-11T07:22:28Z | 3,205 |
| Вода | 377 | 154373804 | 2026-08-10T21:46:07Z | 4,635 |
| Архитектура | 2677 | 152223516 | 2026-03-14T14:39:11Z | 2,308 |
| Театр | 13680 | 153289187 | 2026-05-26T16:18:41Z | 3,378 |
| Музыка | 463 | 154096337 | 2026-07-25T03:48:31Z | 4,252 |
| Пушкин, Александр Сергеевич | 537 | 154419144 | 2026-08-13T21:59:17Z | 10,622 |
| Толстой, Лев Николаевич | 739095 | 153908448 | 2026-07-11T13:52:10Z | 18,054 |
| Достоевский, Фёдор Михайлович | 1456 | 154503837 | 2026-08-17T19:06:23Z | 13,304 |

## Interpretation limits

This corpus is useful for **false-positive discovery**, not for estimating recall or proving that a rule is good:

- Wikipedia is mostly edited expository prose, not chat, advertising, letters or job applications;
- a zero-hit rule may simply have no trigger in these genres;
- a hit is not automatically a false positive; it identifies a place requiring manual contextual review;
- the corpus changes over time, hence revision metadata;
- source rules still require the book-study provenance and the existing NATIVE_USAGE guards.

## Outcome

No additional source rule is promoted to `DEFAULT_MECHANICAL` or `HARD_GATE`.

The calibration instead removes one accusation from the linter: `PS-R21` present-time wording is now **METRIC_ONLY** mechanically. This is the intended precision-first behavior: when natural negative material breaks the heuristic, narrow or demote the heuristic rather than weakening the negative control.
