# Ilyakhov / Sarycheva knowledge library

This library operationalizes the audited study of Максим Ильяхов and Людмила Сарычева, «Пиши, сокращай», without turning the book into a second humanizer or a normative grammar. It now also has a provenance-separated supplement from public editorial materials by Максим Ильяхов, Bureau advice and official Glavred documentation.

## Book source status

Primary book source: user-provided EPUB, SHA-256 `21eae50b5dfd29adfe60f9f52130494673b2e4231fab4d0f29827a392bacb38d`.

Study coverage is complete for the supplied file: 211/211 NCX nodes accounted for, 177/177 leaf sections read sequentially, 0 unread/inaccessible sections, 102 atomic rules, 30 counterexample classes, 32 isolated claims, 17 interactions and 67 original evals. Exact print-equivalent bibliographic metadata remains unresolved and is not guessed.

The source EPUB is not stored in the public repository.

## Public-web supplement

The supplement is deliberately kept separate from the book namespace:

- `libraries/ilyakhov/web-sources.json` — portable curated source/provenance index;
- `libraries/ilyakhov/web-rules.json` — structured supplemental model-only cards;
- `references/ilyakhov-web.md` — compact operational guidance from public web materials;
- `studies/ilyakhov-web/integration-matrix.md` — duplicate / extension / narrowing / new-rule mapping against the book core;
- `studies/ilyakhov-web/stopword-corpus.json` — research-only stop-word provenance and candidate groups.

The web study is **curated**, not represented as an exhaustive audit of every article Ilyakhov has published. The author's own 2017 index alone identifies 100 selected editor-facing articles from 142 written that year. High-yield sources are integrated first and carry explicit URLs and source kinds.

Three genuinely supplemental concepts are currently model-only and intentionally use a different identity namespace:

- `IW-R01` — stated corporate value requires an observable operational consequence or trade-off;
- `IW-R02` — anti-editorial cargo cult: a technique must not make normal Russian less natural merely to satisfy a rule/tool;
- `IW-R03` — figure-of-speech function test: decorative imagery must fit genre and must not camouflage an empty claim.

They are not attributed to the supplied EPUB and do not alter the canonical `ILY-R01`—`ILY-R102` count.

## Stop-word boundary

A historical public list assembled by a reader from Ilyakhov's materials is linked in comments under the 2014 article «Паразиты времени». Ilyakhov thanked the reader for collecting it. This is useful provenance, but it is **not** treated as an official, complete or current export of the Glavred database.

The project therefore does not import the list as an executable ban-list. Candidate membership can only trigger a contextual test. Public Ilyakhov and Glavred materials explicitly reinforce this policy: a stop word may be necessary, and a tool score is not a text-quality score.

## Runtime routing

The canonical book model has 102 rules. After mechanical feasibility and natural-Russian calibration:

- `HARD_GATE`: 0;
- source `DEFAULT_MECHANICAL`: 0;
- `EXTENDED_SOFT`: 9;
- `METRIC_ONLY`: 4;
- `MODEL_ONLY`: 89.

A separate `PROJECT_DERIVED` operator, `ILY-M01`, is the only `DEFAULT_MECHANICAL` rule. It is a deliberately narrow subset of `PS-R22 + PS-R29` for explicit light-verb/nominalization duplication. It is not presented as a direct rule or quotation of the authors.

Both compact and Editorial Board call the same `scripts/lint_ilyakhov.py` through `library_runtime`. The adapter is `review_v1`.

The web supplement primarily strengthens model guidance and counterexamples. Mechanical code is expanded only when a narrow surface remains defensible with positive and negative controls; the stop-word corpus itself never drives automatic rewrites.

## Native-Russian boundary

This library does not ban stop words, first-person frames, personal or possessive pronouns, passive constructions, nominalizations, participles, parcellation, long sentences, exact numbers, professional terminology, repetition or official register by category.

Where source advice conflicts with ordinary Russian ellipsis, agentless constructions, functional repetition, information structure, pragmatic particles, author voice or register requirements, the source rule is narrowed and `NATIVE_USAGE` takes priority.

## Shared phenomena already present in other libraries

The rule namespace remains source-specific (`ILY-*`), while genuinely shared mechanisms reuse existing `phenomenon_id` values:

- `ILY-R08` ↔ `CHUK-R22`: `editing.read_aloud_after_semantics`;
- `ILY-R16` ↔ `CHUK-R21`: `editing.proposition_before_evaluation`;
- `ILY-R19` ↔ `CHUK-R19`: `editing.template_without_semantic_gain`;
- `ILY-R23` ↔ `CHUK-R08`: `editing.register_scene_fit`;
- `ILY-R26` ↔ `CHUK-R07`: `editing.terminology_audience_fit`;
- `ILY-R29` / `ILY-M01` ↔ `CHUK-R17`: `editing.action_hidden_in_nominalization`;
- `ILY-R62` ↔ `CHUK-R24`: `editing.metadiscourse_announcement`.

These mappings mean only that the mechanism is shared. They do not imply equal scope, equal verdict, or automatic consensus.

## Provenance

Book core:

- `libraries/ilyakhov/rules.json` — runtime identities and phenomenon routing;
- `studies/pishi-sokrashchay/integration-matrix.md` — scope, trigger, context, false-positive risk, positive/negative/boundary cases, overlaps and NATIVE_USAGE conflict for all 102 book rules;
- `studies/pishi-sokrashchay/mechanical-feasibility.md` — why rules were mechanical, metric-only or model-only;
- `references/ilyakhov.md` — compact operational reference for MODEL_ONLY book residue;
- `studies/pishi-sokrashchay/audit.md` — loss and overgeneralization audit.

Web supplement:

- `libraries/ilyakhov/web-sources.json` — source URLs and classes, included in installable runtime packages;
- `libraries/ilyakhov/web-rules.json` — `IW-R01`—`IW-R03` structured cards;
- `references/ilyakhov-web.md` — runtime/model reference;
- `studies/ilyakhov-web/integration-matrix.md` — relationship to canonical book rules;
- `studies/ilyakhov-web/stopword-corpus.json` — research provenance and non-ban policy.

The reviewer profile represents the formalized system of the sources. User-facing output should say “По системе Максима Ильяхова и Людмилы Сарычевой” for the book core, and distinguish supplemental public material when provenance matters; never imply that either author personally reviewed the text.
