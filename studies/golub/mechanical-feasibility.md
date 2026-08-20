# Mechanical feasibility

Automation counts: `{'HARD_GATE': 0, 'DEFAULT_MECHANICAL': 3, 'EXTENDED_SOFT': 1, 'METRIC_ONLY': 2, 'MODEL_ONLY': 87}`. Precision is intentionally preferred over recall.

## DEFAULT_MECHANICAL

1. `norm.soglasno_dative` — lexical high-precision subset of known genitive errors after `согласно`; current norm independently confirmed.
2. `norm.payment_verb_government` — narrow lexical subset `оплатить за + known payment object`; deliberately does not try to model all valency.
3. `norm.double_comparative_marking` — local `более/менее + simple comparative` subset with quote/code/URL exclusions.

All shared surface regexes live in `scripts/shared_russian_norm_surfaces.py`, not in author adapters.

## EXTENDED_SOFT

- `editing.paired_conjunction_alignment`: reuse the already operational Rosenthal high-precision candidate for mixed `не только … а также`; Golub adds provenance, not a second regex.

No other source phenomenon was promoted merely to satisfy a quota. Context-sensitive duplication of conditional `бы`, nominalization, repetition, passive, long sentences and similar phenomena remain MODEL_ONLY or metrics unless an independently calibrated high-precision subset exists elsewhere in the shared runtime.

## METRIC_ONLY

- `editing.long_sentence_clarity`: sentence word-count distribution only.
- `editing.sound_collision`: crude phonographic echo candidates only.

## Shared implementation / no duplicate regex

Golub provenance overlaps existing source-neutral phenomena for nominalization, noun chains, terminology, borrowings, templates, information focus, participles/gerunds, imagery and sound. Those mechanisms are not reimplemented as separate author regexes. `scripts/lint_golub.py` contains no duplicate surface regex for mechanisms already implemented by Rosenthal. Shared patterns are factored into `scripts/shared_russian_norm_surfaces.py`; the adapter only maps matches to Golub provenance. The remaining two descriptive metrics stay local and non-normative.
