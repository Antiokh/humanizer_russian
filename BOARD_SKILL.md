# Editorial Board mode

`BOARD_SKILL.md` describes the expanded orchestration mode of `humanizer_russian`.

The compact product remains `SKILL.md` + `scripts/check.py`. Do not replace it with this mode.

## Goal

Use the same knowledge libraries and mechanical findings as compact mode, preserve source provenance/disagreement, and optionally attach independent evidence without turning evidence sources into fake reviewers.

## Runtime order

1. Preserve `USER_INTENT + SEMANTICS + NORM` as hard constraints.
2. Run registered mechanical knowledge libraries, including the project-core `russian` layer.
3. Normalize findings to the shared finding contract.
4. Group semantically equivalent findings by `phenomenon_id` and local excerpt/span.
5. Keep each reviewer verdict separate.
6. If explicitly requested, run optional Evidence providers against normalized findings.
7. Attach evidence without adding it to reviewer voting.
8. Apply style policy only after reviewer opinions are preserved.
9. Use model reasoning only for `MODEL_ONLY` residue or prose rendering.
10. Re-check semantics and norm before applying a rewrite.

## Russian language layer

The `russian` library is not another editing school. It contains current-norm guardrails and source-neutral Russian usage/register diagnostics.

Mechanical examples:

- final full stop in a **structurally marked** Markdown heading -> `NORM` guardrail;
- `1.` followed by a lowercase list item -> rubrication guardrail;
- adjacent `Это не X. Это Y.` -> review the split contrast, but keep it when emphatic correction is functional;
- lowercase Latin word inside Russian prose -> check whether a Russian equivalent or explanation is preferable;
- known technical jargon/terms -> check audience/register;
- an unmarked short plain-text line that looks like a heading -> soft candidate to mark structurally or punctuate as ordinary prose;
- mismatched lowercase/uppercase list punctuation -> soft list-formatting review.

The caller may specify register:

```bash
python scripts/review.py text.md --register everyday
python scripts/review.py text.md --register technical
```

In `everyday`, known technical jargon is surfaced more aggressively. It still remains a review finding, not a language error merely because it is jargon or a borrowing.

### Heading semantics are not heading markup

Do not grant heading punctuation merely because a line *means* a section title. A heading must be structurally/typographically identified by the target format: Markdown/HTML heading, document style, explicit rubrication or another reliable signal.

If output is plain text and the line is visually indistinguishable from ordinary prose, choose explicitly:

- mark it using a representation available to the target medium; or
- treat it as ordinary text and punctuate/connect it accordingly.

The actual-heading rule and the pseudoheading review are intentionally different findings.

### Model-only Russian syntax residue

After mechanics, load only the relevant cards from:

- `libraries/russian/rules.json`;
- `libraries/russian/rki-rules.json`;
- `references/russian-language.md`;
- `references/russian-rki-grammar.md`.

The RKI cards are source-neutral Russian-core diagnostics. Their study provenance is retained in `studies/velichko-kniga-o-grammatike/`; there is no Velichko reviewer vote. When Velichko confirms or refines a phenomenon already present in the Russian core, enrich the existing `RU-*` card instead of creating a second source-neutral rule for the same `phenomenon_id`.

In particular review:

- `RU-NORM-GERUND-SUBJECT-ATTACHMENT` — shared semantic subject, including the normative impersonal + infinitive case when the gerund and infinitive have the same controller;
- `RU-NATIVE-GERUND-GRAMMATICALIZED-GUARD` — distinguish a free gerund from grammaticalized/prepositional uses such as `исходя из`; do not turn a partial list into an unconditional whitelist;
- `RU-NATIVE-GERUND-OBJECT-INFINITIVE-ATTACHMENT` — when a matrix subject and the controller of an object infinitive compete, resolve who performs the gerundial action before editing;
- `RU-NATIVE-GERUND-FRAME-POSITION` — background/frame gerunds often work preposed, while a gerund tied to the second conjunct or preparing an antithesis/vector shift should stay close to that conjunct; this is information structure, not a universal positional norm;
- `RU-NORM-PARTICIPLE-HEAD-ATTACHMENT` and `RU-NORM-PARTICIPLE-AGREEMENT` — identify the true head first, then agree the participle with that head rather than the nearest noun;
- `RU-NATIVE-PARTICIPLE-TEMPORAL-FIT` — preserve relative time and register after structural checks;
- `RU-NATIVE-PARTICIPIAL-COMPRESSION` — consider a natural participial phrase instead of reflexively expanding everything into `который + глагол`;
- `RU-RKI-VALENCY-FRAME-FIT` — resolve lexical sense and participant role before changing case/preposition or copying a frame through nominalization;
- `RU-NATIVE-SUBJECT-REALIZATION` — compare overt nominative subject with indefinite-personal, impersonal and dative-infinitive Russian models without deleting a functional subject;
- `RU-NATIVE-EVENT-CONSTRUAL` — distinguish process, boundary/transition, result and resulting state before choosing aspect/voice;
- `RU-NATIVE-PASSIVE-RESULT-STATE` — choose active/passive/resultative perspective by information focus and register rather than banning passive;
- `RU-NATIVE-COPULA-SEMANTIC-FIT` — do not use `есть`, `являться`, `представлять собой` as interchangeable generic `be`, but do not stop-list them;
- `RU-NATIVE-INTRODUCTORY-SCOPE` — keep parenthetic modality/source marking with the proposition it actually scopes over;
- `RU-RKI-SYNTACTIC-INTERFERENCE-AUDIT` — broader fallback for government, valency, prepositions, agreement, word order/theme-rheme, aspect/tense, clause structure, homogeneous constructions, pronoun reference and punctuation transfer.

The three RKI distribution signals in `scripts/lint_russian_rki_metrics.py` are `METRIC_ONLY`. They have no normative threshold and never vote or emit `CHANGE` by themselves.

Do **not** force participles/gerunds for decorative variety or by quota. They are desirable as available Russian syntactic resources when they improve compression and keep the attachment clear.

### Model-only semantic relation check

Apply `RU-SEM-CATEGORY-COLLECTION` when a definition or metaphor appears to confuse an object with a collection/container made of objects of that class.

Example to challenge:

> Книги — это библиотеки знаний.

First establish the real relation, then rewrite. Preserve a metaphor only if it adds deliberate useful meaning.

See `references/russian-language.md`, `references/russian-rki-grammar.md` and `docs/russian-error-priorities.md`.

## Reviewer semantics

A reviewer represents a formalized source system, not a simulation of the real author. UI should say `По системе ...`, not pretend the author personally reviewed the text.

## Evidence semantics and availability

Evidence providers are not reviewers. Corpus, spoken-language, lexical, normative or parsed data may support/contextualize a finding but must not enter `reviewer_verdicts`.

Default board mode performs **zero evidence-provider work**. Compact `scripts/check.py` never calls evidence providers.

```bash
python scripts/review.py text.md --style neutral
python scripts/review.py text.md --style neutral --evidence off
```

Opt in only when useful:

```bash
python scripts/review.py text.md --evidence current_usage,spoken_russian
python scripts/review.py text.md --evidence auto
```

`HUMANIZER_EVIDENCE=off` is a global kill switch. Remote providers cannot be enabled by default. Timeout/unavailability is fail-open (`SKIP`) and a global evidence budget prevents a missing service from hanging the board.

See `docs/evidence-provider-architecture.md` and `evidence/README.md`.

## Board statuses

- `CONSENSUS`
- `MAJORITY`
- `SOURCE_CONFLICT`
- `SINGLE_REVIEW`
- `REVIEW`
- `NO_ACTION`

Conflicts are data. Evidence does not turn a source conflict into consensus.

## Styles

Style files are editorial policies, not language rules. They may weight reviewers or define conflict handling, but cannot override semantic/norm guardrails.

## Context budget

Preferred flow:

`mechanical libraries -> normalized findings -> relevant rule cards -> optional targeted evidence -> optional model-only review`.

Do not read every book or query every corpus for every text. If evidence is unavailable, continue without it.

## CLI

```bash
python scripts/review.py text.md --style neutral
python scripts/review.py text.md --style rslive_content --format json
python scripts/review.py text.md --register everyday --format json
python scripts/review.py text.md --evidence current_usage --format json
```
