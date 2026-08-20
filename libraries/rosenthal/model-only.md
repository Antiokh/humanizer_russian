# Rosenthal MODEL_ONLY residue

This file is a compact routing reference. Canonical rule cards live in `rules.json` (cycle 1), `rules-cycle2.json` (cycle 2), `rules-cycle3.json` (cycle 3), and `rules-cycle5.json` (cycle 5). **Cycle 4 adds no new rule identities** and is routed through `provenance-cycle4.json`; full studies are not loaded into ordinary runtime.

Mechanical surfaces currently emitted by `scripts/lint_rosenthal.py`: `ROS-R30`, `ROS-R44`, `ROS-R53`. `ROS-R10` remains metric-only. Cycles 3–5 deliberately add no new mechanical finding.

## Cycle 2 contextual rules

`ROS-R47` grammatical synonym choice; `R48` multi-criterion revision; `R49` word-formation register; `R50` discourse-marker function; `R51` borrowing; `R52` trope fit; `R54` subjunctive-particle duplication; `R55` expressive syntax; `R56` sentence boundary; `R57` image collision; `R58` rhetorical figure; `R59` current-orthoepy verification.

## Cycle 3 contextual rules

| Rule | Phenomenon |
|---|---|
| `ROS-R60` | `ai_calque.false_friend_semantic_transfer` |
| `ROS-R61` | `editing.text_type_structure_fit` |
| `ROS-R62` | `editing.inter_sentence_information_progression` |
| `ROS-R63` | `editing.microtheme_cohesion` |
| `ROS-R64` | `editing.paragraph_boundary_function` |
| `ROS-R65` | `editing.logical_relation_fit` |
| `ROS-R66` | `editing.comparison_basis_consistency` |
| `ROS-R67` | `editing.multi_proposition_focus` |
| `ROS-R68` | `editing.terminology_audience_fit` |
| `ROS-R69` | `editing.reported_speech_fidelity` |
| `ROS-R70` | `editing.local_change_whole_fit` |
| `ROS-R71` | `author.expressive_compensation` |
| `ROS-R72` | `editing.edit_type_fit` |
| `ROS-R73` | `register.spoken_delivery_style_fit` |
| `ROS-R74` | `editing.pause_information_structure` |

## Cycle 4 provenance-only source

The 1997 fifth edition «Справочник по правописанию и стилистике» ends at §213 and substantially overlaps the already integrated stylistic lineage. It enriches 50 existing rule cards and records edition/current-norm boundaries, especially `более старший`, `клипс/клипса`, duplicate `бы`, government and parallel constructions. No source-period list is promoted to modern NORM by author authority.

## Cycle 5 contextual rules

| Rule | Phenomenon |
|---|---|
| `ROS-R75` | `editing.punctuation_variant_semantic_choice` |
| `ROS-R76` | `author.punctuation_system_intent` |
| `ROS-R77` | `register.spoken_syntax_punctuation` |
| `ROS-R78` | `native.serial_verb_unit_punctuation` |

Cycle 5 comes from the supplied DOCX «Справочник по русскому языку: орфография и пунктуация». Exact edition metadata is not recoverable from the supplied file. Concrete mandatory orthography and punctuation remain owned by current `russian/NORM`; the new Rosenthal cards cover only contextual choice and preservation boundaries.

Cycle-1 MODEL_ONLY rules remain canonical in `libraries/rosenthal/rules.json`. Do not infer blanket bans or automatic normalization of nominalization, passive, repetition, long sentences, participles, gerunds, colloquial markers, loanwords, tropes, rhetorical figures, paragraphing, ellipsis, spoken reduction, punctuation variation, authorial punctuation, conversational syntax, or adjacent same-form verbs.
