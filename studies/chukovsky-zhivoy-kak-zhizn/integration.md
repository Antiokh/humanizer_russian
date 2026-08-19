# Integration pass — independent Chukovsky study → current `humanizer_russian`

Status: `OPERATIONAL_FOR_INTEGRATION`.

This file is the current integration record for the independent study of Корней Чуковский, «Живой как жизнь». The deep research history remains in the other files in this directory; this document intentionally describes the **current** runtime architecture rather than preserving stale implementation snapshots.

## Architecture

The source is integrated as one knowledge library consumed by both product modes:

```text
BOOK / supplied source
  → audited study
  → libraries/chukovsky/rules.json
  → scripts/chukovsky_checks.py
  → scripts/lint_chukovsky.py (review_v1)
  → scripts/check.py              # compact
  → scripts/review.py             # editorial board
```

There is no second Chukovsky humanizer and no separate copy of the rules for board mode.

Current `main` remains the architecture authority. Chukovsky contributes source knowledge and source-specific mechanics without replacing core `SKILL.md`, library runtime, board runtime or current Russian guardrails.

## Source/study gate

The source study was completed before runtime integration and then re-audited rather than trusting previous regexes or prompt rules.

Current inventory:

- full source coverage: `SRC:L1-L4530`;
- 14/14 source units `VERIFIED`;
- 22 concepts;
- 38 atomic rules;
- 33 counterexample boundary families;
- 20 interaction groups;
- 30 externally auditable claim groups;
- 58 independent source-study evals: 38 direct + 20 compound;
- loss audit complete;
- overgeneralization audit complete.

Primary-source identity and fingerprint are recorded in `source.md` and `libraries/chukovsky/library.json`. The original copyrighted book is not stored in the public repository.

## Rule identity

The deep study historically used `CHK-R01` … `CHK-R38`. Those IDs remain stable inside the research artifacts so links and research history are not destroyed.

The knowledge-library runtime uses canonical source IDs `CHUK-R01` … `CHUK-R38`, matching `source_namespace=CHUK`.

The complete mapping is machine-readable in:

`libraries/chukovsky/rules.json`

Each canonical rule has a source-neutral `phenomenon_id`. `rule_id` preserves Chukovsky provenance; `phenomenon_id` is reused across libraries only when the underlying mechanism is genuinely the same.

## Classification of all 38 rules

Automation:

- `HARD_GATE`: **0**;
- `DEFAULT_MECHANICAL`: **0**;
- `EXTENDED_SOFT`: **7**;
- `METRIC_ONLY`: **2**;
- `MODEL_ONLY`: **29**.

Project classes:

- `NORM`: 4;
- `NATIVE_USAGE`: 7;
- `EDITING`: 23;
- `AUTHOR`: 4;
- `AI_CALQUE`: 0;
- `ARTIFACT`: 0.

The complete contextual classification — source locator, scope, semantic invariant, trigger, required context, false-positive risk, positive case, natural negative/boundary, overlaps and NATIVE_USAGE conflict risk — remains canonical in `integration-matrix.md` and the atomic cards in `rules.md`.

## Mechanical feasibility result

Every rule was considered in the required order:

`exact/string → regex → tokenizer → morphology → dependency/statistical → metric → MODEL_ONLY`.

The audit deliberately rejected pseudo-linguistic shortcuts where semantics or context are required. In particular, the runtime does **not** treat the following as automatic errors:

- genitive/case counts;
- `наличие/отсутствие` or another abstract antonym pair as a semantic collision by itself;
- one formal marker as cancelearite;
- a bare `-ение/-ание/-ция` count as bad style;
- one cliché as a dead stamp;
- suffix echo as bad style;
- slang as evidence about personality/intellect;
- a foreign token as a defect;
- a historical dictionary pair as a current automatic correction.

## Accepted `EXTENDED_SOFT` mechanics

Exactly seven canonical source rules have mechanical candidates:

1. `CHUK-R09` — `editing.abbreviation_reader_effort`;
2. `CHUK-R15` — `editing.register_leakage_bureaucratic`;
3. `CHUK-R17` — `editing.action_hidden_in_nominalization`;
4. `CHUK-R18` — `editing.modifier_semantic_subtraction`;
5. `CHUK-R19` — `editing.template_without_semantic_gain`;
6. `CHUK-R24` — `editing.metadiscourse_announcement`;
7. `CHUK-R25` — `editing.procedural_question_packaging`.

They are implemented once in `scripts/chukovsky_checks.py` and normalized by `scripts/lint_chukovsky.py`.

All seven remain suggestions/candidates. They do not become language errors, AI attribution or publication gates solely because a surface trigger fired.

## `METRIC_ONLY`

Two rules remain descriptive metrics rather than findings:

- `CHUK-R22` — `editing.read_aloud_after_semantics`;
- `CHUK-R31` — `editing.prosody_comparison`.

Ending/suffix echo is measured only to support a later read-aloud comparison. It is **not** emitted as `EDITING_SUGGESTION` and has no “bad Russian” threshold.

## `MODEL_ONLY` residue

The remaining 29 rules are explicitly listed in `libraries/chukovsky/rules.json:model_only_rule_ids`.

They require one or more of:

- current norm evidence;
- semantics or semantic roles;
- discourse/coreference;
- register/scene/audience;
- idiom/lexicalization status;
- authorial intention;
- functional repetition/prosody;
- independent evidence for claims about a speaker/person.

A contextual board pass should load only the relevant rule cards/operational reference. It must not read the whole book or whole study on every request, and it must not repeat analysis already supplied by a mechanical finding.

## NATIVE_USAGE compatibility

No Chukovsky `EDITING` recommendation may override the project’s higher-priority constraints and native layer.

Preserve where functional:

- recoverable ellipsis and context economy;
- natural information structure and Russian word order;
- functional/expressive repetition;
- pragmatic particles;
- intentional parcellation;
- Russian contrast structures;
- professional/familiar/author register;
- author profile.

Historical taste is not current `NORM`. Any mandatory normative correction derived from the historical source requires separate current verification.

## Compact mode

Default compact mode:

```bash
python scripts/check.py text.md
```

shows no Chukovsky finding because this library currently has `0 DEFAULT_MECHANICAL` rules.

Extended compact mode:

```bash
python scripts/check.py --extended text.md
```

may show the seven `EXTENDED_SOFT` findings from the same `review_v1` library used by the board.

If several libraries emit the same compatible `phenomenon_id` for the same local surface, compact may collapse them into one row while preserving source provenance in machine output. A directional CHANGE/KEEP conflict is never collapsed into fake agreement.

## Editorial-board mode

```bash
python scripts/review.py text.md --style neutral
```

receives the same normalized findings and preserves:

- `library_id=chukovsky`;
- `reviewer_id=chukovsky`;
- canonical `rule_id=CHUK-Rxx`;
- source-neutral `phenomenon_id`.

The reviewer label means «По системе Корнея Чуковского», not that the historical author personally reviewed the current text.

Cross-author disagreement is data. `CHANGE` vs `KEEP` becomes `SOURCE_CONFLICT`; style policy may choose how a concrete publication reacts, but it does not erase reviewer verdicts.

## Existing-library overlap audit

Before this Chukovsky library is merged, current `main` has only the enabled `native` library. No Chukovsky phenomenon is an exact duplicate of an already-registered native mechanical `phenomenon_id`, so this migration does not invent consensus by renaming unrelated signals.

Conceptual overlap is documented in `library-routing.md` for later operational libraries, especially:

- `editing.action_hidden_in_nominalization` — likely Gal/Ilyakhov overlap;
- `editing.register_leakage_bureaucratic` — likely Gal/Ilyakhov overlap;
- `editing.modifier_semantic_subtraction` — likely information-style overlap;
- `editing.template_without_semantic_gain` — likely template/cliché overlap;
- `native.recoverable_ellipsis` — overlaps native-Russian preservation principles;
- `native.expressive_redundancy` — overlaps functional-repetition preservation;
- `native.idiom_as_lexical_unit` — likely Nora Gal idiom/metaphor boundary.

Reuse a `phenomenon_id` later only when mechanism and local editorial decision match.

## Tests and preservation controls

Deterministic source-specific tests live in `tests/chukovsky_cases.json`. They include positive triggers plus natural negatives/boundaries for warning hierarchy, ordinary project language, official formulas, functional nominalization, restrictive modifiers, evidence-backed phrasing, genuine `вопрос`, expert abbreviations, normal `наличие или отсутствие`, intentional repetition, familiar register, expert terminology and metric-only prosody.

Board regression tests separately cover Chukovsky provenance, natural negatives, shared-phenomenon consensus contract, source-conflict contract and guardrail behavior.

`evals/chukovsky.json` contains contextual/model scenarios. They are fixtures, not a passed deterministic benchmark until a real model/judge run occurs.

## Remaining work after this migration cycle

The next useful work is empirical rather than adding broad regexes:

- run the seven extended checks on a larger native corpus and measure false positives;
- experiment with dependency assistance for `CHUK-R23` without promoting it prematurely;
- evaluate a current phraseology/idiom resource for `CHUK-R32`–`CHUK-R34`;
- run the contextual/model eval suite through an actual judge harness;
- perform item-level current normative verification only when a historical dictionary prescription is needed for a real decision.

The long-lived branch `chukovsky` must remain after merge for the next research cycle.
