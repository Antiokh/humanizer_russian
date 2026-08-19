# Library routing — Chukovsky rules → dual runtime

This is the Gate D/F supplement to `integration-matrix.md`. It was added after fresh `main` introduced pluggable knowledge libraries and the compact/editorial-board dual runtime.

`phenomenon_id` is source-neutral; `CHK-Rxx` remains source provenance. Multiple source rules may later share a phenomenon with Gal, Ilyakhov, native Russian or another library without being collapsed into one opinion.

| Rule | phenomenon_id | Planned implementation | Runtime visibility |
|---|---|---|---|
| R01 | `norm.historical_change_vs_current_norm` | model/reference + current authority | `MODEL_ONLY` |
| R02 | `editing.classify_language_innovation` | model/reference | `MODEL_ONLY` |
| R03 | `native.current_meaning_over_etymology` | model/reference | `MODEL_ONLY` |
| R04 | `native.recoverable_ellipsis` | model/reference | `MODEL_ONLY` |
| R05 | `native.ellipsis_vs_lexical_reanalysis` | model/reference + current valency evidence | `MODEL_ONLY` |
| R06 | `editing.borrowing_semantic_utility` | model/reference | `MODEL_ONLY` |
| R07 | `editing.terminology_audience_fit` | model/reference | `MODEL_ONLY` |
| R08 | `editing.register_scene_fit` | model/reference | `MODEL_ONLY` |
| R09 | `editing.abbreviation_reader_effort` | `scripts/lint_chukovsky.py` | `EXTENDED_SOFT: compact --extended + board` |
| R10 | `editing.no_classwide_wordformation_ban` | model/reference guard | `MODEL_ONLY` |
| R11 | `author.speaker_register_preservation` | model/reference + author/scene | `MODEL_ONLY` |
| R12 | `author.no_person_inference_from_slang` | model/reference guard | `MODEL_ONLY` |
| R13 | `editing.no_extralinguistic_cause_inference` | model/reference guard | `MODEL_ONLY` |
| R14 | `editing.functional_official_register` | model/reference | `MODEL_ONLY` |
| R15 | `editing.register_leakage_bureaucratic` | `scripts/lint_chukovsky.py` | `EXTENDED_SOFT: compact --extended + board` |
| R16 | `editing.direct_name_over_prestige_classifier` | model/reference | `MODEL_ONLY` |
| R17 | `editing.action_hidden_in_nominalization` | `scripts/lint_chukovsky.py` + model role reconstruction | `EXTENDED_SOFT: compact --extended + board` |
| R18 | `editing.modifier_semantic_subtraction` | `scripts/lint_chukovsky.py` + model A/B | `EXTENDED_SOFT: compact --extended + board` |
| R19 | `editing.template_without_semantic_gain` | `scripts/lint_chukovsky.py` + document-context model | `EXTENDED_SOFT: compact --extended + board` |
| R20 | `author.no_sincerity_inference_from_cliche` | model/reference guard | `MODEL_ONLY` |
| R21 | `editing.proposition_before_evaluation` | model/reference + source evidence | `MODEL_ONLY` |
| R22 | `editing.read_aloud_after_semantics` | Chukovsky metrics + model/read-aloud comparison | `METRIC_ONLY` |
| R23 | `editing.semantic_role_ambiguity` | future dependency assist; model now | `MODEL_ONLY` |
| R24 | `editing.metadiscourse_announcement` | `scripts/lint_chukovsky.py` + A/B model | `EXTENDED_SOFT: compact --extended + board` |
| R25 | `editing.procedural_question_packaging` | `scripts/lint_chukovsky.py` + model speech-act check | `EXTENDED_SOFT: compact --extended + board` |
| R26 | `editing.template_erases_subject_individuality` | document-level model | `MODEL_ONLY` |
| R27 | `editing.ground_interpretation_in_observation` | model/reference | `MODEL_ONLY` |
| R28 | `editing.correctness_not_sufficient_for_quality` | model/meta quality rule | `MODEL_ONLY` |
| R29 | `native.lexicalization_over_literal_logic` | model/reference + future phraseology assist | `MODEL_ONLY` |
| R30 | `native.expressive_redundancy` | model/reference | `MODEL_ONLY` |
| R31 | `editing.prosody_comparison` | Chukovsky metrics + model/read-aloud comparison | `METRIC_ONLY` |
| R32 | `native.idiom_as_lexical_unit` | model/reference + future phraseology assist | `MODEL_ONLY` |
| R33 | `author.deliberate_idiom_deformation` | model/reference | `MODEL_ONLY` |
| R34 | `editing.idiom_play_vs_contamination` | model/reference | `MODEL_ONLY` |
| R35 | `norm.historical_prescription_requires_current_verification` | model/reference + current authority | `MODEL_ONLY` |
| R36 | `norm.professional_variant_scope` | model/reference + current authority | `MODEL_ONLY` |
| R37 | `native.familiar_register_scope` | model/reference + scene | `MODEL_ONLY` |
| R38 | `norm.evidence_before_normalization` | model/reference guard | `MODEL_ONLY` |

## Library contract

- manifest: `libraries/chukovsky/library.json`;
- reviewer: `reviewers/chukovsky.json`;
- normalized adapter: `scripts/lint_chukovsky.py` (`review_v1`);
- mechanical implementation: `scripts/chukovsky_checks.py`;
- full provenance: `studies/chukovsky-zhivoy-kak-zhizn/`;
- compact default: no Chukovsky finding (`0 DEFAULT_MECHANICAL`);
- compact `--extended`: the seven `EXTENDED_SOFT` rules can appear with `library_id=chukovsky`;
- editorial board: the same seven normalized findings retain `reviewer_id=chukovsky`, `rule_id=CHK-Rxx`, and source-neutral `phenomenon_id`;
- model-only residue is not duplicated into mechanics and is loaded only when relevant.

## Overlap / future consensus candidates

Likely cross-library phenomenon IDs to reuse rather than mint duplicates:

- `editing.action_hidden_in_nominalization` — likely overlap with Gal/Ilyakhov layers;
- `editing.register_leakage_bureaucratic` — likely overlap with Gal/Ilyakhov officialese/cancelearite rules;
- `editing.modifier_semantic_subtraction` — likely overlap with information-style redundancy rules;
- `editing.template_without_semantic_gain` — overlap with generic/cliché/template diagnostics;
- `native.recoverable_ellipsis` — overlap with native Russian core;
- `native.expressive_redundancy` — overlap with native preservation of functional repetition;
- `native.idiom_as_lexical_unit` — overlap with Nora Gal idiom/metaphor boundary.

These overlaps should produce consensus or source conflict in board mode only when the underlying decision and local span really match. Do not merge rule IDs merely because vocabulary looks similar.
