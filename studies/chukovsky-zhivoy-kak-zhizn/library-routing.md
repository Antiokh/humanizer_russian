# Library routing — Chukovsky rules → dual runtime

This is the Gate D/F supplement to `integration-matrix.md`. It records the migration from the historical study-card namespace to the canonical knowledge-library runtime namespace.

- historical study card: `CHK-Rxx` (retained so the research history and existing study cross-links do not break);
- canonical runtime/source `rule_id`: `CHUK-Rxx` (matches `source_namespace=CHUK`);
- source-neutral `phenomenon_id`: mechanism shared across libraries when the underlying editorial decision is genuinely the same.

The machine-readable canonical map is `libraries/chukovsky/rules.json`.

| Study | Runtime rule_id | phenomenon_id | Planned implementation | Runtime visibility |
|---|---|---|---|---|
| R01 | `CHUK-R01` | `norm.historical_change_vs_current_norm` | model/reference + current authority | `MODEL_ONLY` |
| R02 | `CHUK-R02` | `editing.classify_language_innovation` | model/reference | `MODEL_ONLY` |
| R03 | `CHUK-R03` | `native.current_meaning_over_etymology` | model/reference | `MODEL_ONLY` |
| R04 | `CHUK-R04` | `native.recoverable_ellipsis` | model/reference | `MODEL_ONLY` |
| R05 | `CHUK-R05` | `native.ellipsis_vs_lexical_reanalysis` | model/reference + current valency evidence | `MODEL_ONLY` |
| R06 | `CHUK-R06` | `editing.borrowing_semantic_utility` | model/reference | `MODEL_ONLY` |
| R07 | `CHUK-R07` | `editing.terminology_audience_fit` | model/reference | `MODEL_ONLY` |
| R08 | `CHUK-R08` | `editing.register_scene_fit` | model/reference | `MODEL_ONLY` |
| R09 | `CHUK-R09` | `editing.abbreviation_reader_effort` | `scripts/lint_chukovsky.py` | `EXTENDED_SOFT: compact --extended + board` |
| R10 | `CHUK-R10` | `editing.no_classwide_wordformation_ban` | model/reference guard | `MODEL_ONLY` |
| R11 | `CHUK-R11` | `author.speaker_register_preservation` | model/reference + author/scene | `MODEL_ONLY` |
| R12 | `CHUK-R12` | `author.no_person_inference_from_slang` | model/reference guard | `MODEL_ONLY` |
| R13 | `CHUK-R13` | `editing.no_extralinguistic_cause_inference` | model/reference guard | `MODEL_ONLY` |
| R14 | `CHUK-R14` | `editing.functional_official_register` | model/reference | `MODEL_ONLY` |
| R15 | `CHUK-R15` | `editing.register_leakage_bureaucratic` | `scripts/lint_chukovsky.py` | `EXTENDED_SOFT: compact --extended + board` |
| R16 | `CHUK-R16` | `editing.direct_name_over_prestige_classifier` | model/reference | `MODEL_ONLY` |
| R17 | `CHUK-R17` | `editing.action_hidden_in_nominalization` | `scripts/lint_chukovsky.py` + model role reconstruction | `EXTENDED_SOFT: compact --extended + board` |
| R18 | `CHUK-R18` | `editing.modifier_semantic_subtraction` | `scripts/lint_chukovsky.py` + model A/B | `EXTENDED_SOFT: compact --extended + board` |
| R19 | `CHUK-R19` | `editing.template_without_semantic_gain` | `scripts/lint_chukovsky.py` + document-context model | `EXTENDED_SOFT: compact --extended + board` |
| R20 | `CHUK-R20` | `author.no_sincerity_inference_from_cliche` | model/reference guard | `MODEL_ONLY` |
| R21 | `CHUK-R21` | `editing.proposition_before_evaluation` | model/reference + source evidence | `MODEL_ONLY` |
| R22 | `CHUK-R22` | `editing.read_aloud_after_semantics` | Chukovsky metrics + model/read-aloud comparison | `METRIC_ONLY` |
| R23 | `CHUK-R23` | `editing.semantic_role_ambiguity` | future dependency assist; model now | `MODEL_ONLY` |
| R24 | `CHUK-R24` | `editing.metadiscourse_announcement` | `scripts/lint_chukovsky.py` + A/B model | `EXTENDED_SOFT: compact --extended + board` |
| R25 | `CHUK-R25` | `editing.procedural_question_packaging` | `scripts/lint_chukovsky.py` + model speech-act check | `EXTENDED_SOFT: compact --extended + board` |
| R26 | `CHUK-R26` | `editing.template_erases_subject_individuality` | document-level model | `MODEL_ONLY` |
| R27 | `CHUK-R27` | `editing.ground_interpretation_in_observation` | model/reference | `MODEL_ONLY` |
| R28 | `CHUK-R28` | `editing.correctness_not_sufficient_for_quality` | model/meta quality rule | `MODEL_ONLY` |
| R29 | `CHUK-R29` | `native.lexicalization_over_literal_logic` | model/reference + future phraseology assist | `MODEL_ONLY` |
| R30 | `CHUK-R30` | `native.expressive_redundancy` | model/reference | `MODEL_ONLY` |
| R31 | `CHUK-R31` | `editing.prosody_comparison` | Chukovsky metrics + model/read-aloud comparison | `METRIC_ONLY` |
| R32 | `CHUK-R32` | `native.idiom_as_lexical_unit` | model/reference + future phraseology assist | `MODEL_ONLY` |
| R33 | `CHUK-R33` | `author.deliberate_idiom_deformation` | model/reference | `MODEL_ONLY` |
| R34 | `CHUK-R34` | `editing.idiom_play_vs_contamination` | model/reference | `MODEL_ONLY` |
| R35 | `CHUK-R35` | `norm.historical_prescription_requires_current_verification` | model/reference + current authority | `MODEL_ONLY` |
| R36 | `CHUK-R36` | `norm.professional_variant_scope` | model/reference + current authority | `MODEL_ONLY` |
| R37 | `CHUK-R37` | `native.familiar_register_scope` | model/reference + scene | `MODEL_ONLY` |
| R38 | `CHUK-R38` | `norm.evidence_before_normalization` | model/reference guard | `MODEL_ONLY` |

## Library contract

- manifest: `libraries/chukovsky/library.json`;
- canonical rule registry: `libraries/chukovsky/rules.json`;
- reviewer: `reviewers/chukovsky.json`;
- normalized adapter: `scripts/lint_chukovsky.py` (`review_v1`);
- mechanical implementation: `scripts/chukovsky_checks.py`;
- full provenance: `studies/chukovsky-zhivoy-kak-zhizn/`;
- compact default: no Chukovsky finding (`0 DEFAULT_MECHANICAL`);
- compact `--extended`: the seven `EXTENDED_SOFT` rules can appear with `library_id=chukovsky`;
- editorial board: the same seven normalized findings retain `reviewer_id=chukovsky`, canonical `rule_id=CHUK-Rxx`, and source-neutral `phenomenon_id`;
- model-only residue is exactly the 29 entries marked `MODEL_ONLY` in `rules.json`; it is not duplicated into mechanical code and is loaded only when relevant.

## Existing-library overlap audit

At this migration point the enabled `main` libraries before Chukovsky consist only of `native`. None of the Chukovsky canonical phenomena is an exact duplicate of an already-registered native mechanical `phenomenon_id`, so no existing ID was silently renamed just to manufacture consensus.

Conceptual overlap exists and must guide future integrations:

- `editing.action_hidden_in_nominalization` — likely overlap with future Gal/Ilyakhov libraries;
- `editing.register_leakage_bureaucratic` — likely overlap with Gal/Ilyakhov officialese/cancelearite rules;
- `editing.modifier_semantic_subtraction` — likely overlap with information-style redundancy rules;
- `editing.template_without_semantic_gain` — overlap with generic/cliché/template diagnostics;
- `native.recoverable_ellipsis` — overlaps the native-Russian preservation principle, but there is no existing identical mechanical phenomenon id;
- `native.expressive_redundancy` — overlaps native preservation of functional repetition;
- `native.idiom_as_lexical_unit` — likely overlaps Nora Gal idiom/metaphor boundaries.

These relationships may produce consensus or source conflict only after another registered library emits a directional finding for the same mechanism and local span. Do not merge rule IDs merely because vocabulary looks similar.
