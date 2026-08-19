# Ilyakhov / Sarycheva knowledge library

This library operationalizes the audited study of Максим Ильяхов and Людмила Сарычева, «Пиши, сокращай», without turning the book into a second humanizer or a normative grammar.

## Source status

Primary source: user-provided EPUB, SHA-256 `21eae50b5dfd29adfe60f9f52130494673b2e4231fab4d0f29827a392bacb38d`.

Study coverage is complete for the supplied file: 211/211 NCX nodes accounted for, 177/177 leaf sections read sequentially, 0 unread/inaccessible sections, 102 atomic rules, 30 counterexample classes, 32 isolated claims, 17 interactions and 67 original evals. Exact print-equivalent bibliographic metadata remains unresolved and is not guessed.

The source EPUB is not stored in the public repository.

## Runtime routing

The source model has 102 rules. After mechanical feasibility and natural-Russian calibration:

- `HARD_GATE`: 0;
- source `DEFAULT_MECHANICAL`: 0;
- `EXTENDED_SOFT`: 9;
- `METRIC_ONLY`: 4;
- `MODEL_ONLY`: 89.

A separate `PROJECT_DERIVED` operator, `ILY-M01`, is the only `DEFAULT_MECHANICAL` rule. It is a deliberately narrow subset of `PS-R22 + PS-R29` for explicit light-verb/nominalization duplication. It is not presented as a direct rule or quotation of the authors.

Both compact and Editorial Board call the same `scripts/lint_ilyakhov.py` through `library_runtime`. The adapter is `review_v1`.

## Native-Russian boundary

This library does not ban stop words, first-person frames, passive constructions, nominalizations, participles, parcellation, long sentences, exact numbers, professional terminology, repetition or official register by category.

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

- `libraries/ilyakhov/rules.json` — runtime identities and phenomenon routing;
- `studies/pishi-sokrashchay/integration-matrix.md` — scope, trigger, context, false-positive risk, positive/negative/boundary cases, overlaps and NATIVE_USAGE conflict for all 102 source rules;
- `studies/pishi-sokrashchay/mechanical-feasibility.md` — why rules were mechanical, metric-only or model-only;
- `references/ilyakhov.md` — compact operational reference for MODEL_ONLY residue;
- `studies/pishi-sokrashchay/audit.md` — loss and overgeneralization audit.

The reviewer profile represents the formalized system of the source. User-facing output should say “По системе Максима Ильяхова и Людмилы Сарычевой”, not imply that either author personally reviewed the text.
