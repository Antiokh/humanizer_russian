# Rosenthal MODEL_ONLY residue

This file is a compact routing reference. Canonical rule cards live in `rules.json` (cycle 1) and `rules-cycle2.json` (cycle 2); full studies are not loaded into ordinary runtime.

Mechanical surfaces currently emitted by `scripts/lint_rosenthal.py`: `ROS-R30`, `ROS-R44`, `ROS-R53`. `ROS-R10` remains metric-only.

## Cycle 2 contextual rules

| Rule | Phenomenon |
|---|---|
| `ROS-R47` | `editing.grammatical_synonym_choice` |
| `ROS-R48` | `editing.multi_criterion_revision` |
| `ROS-R49` | `editing.word_formation_register_fit` |
| `ROS-R50` | `editing.discourse_filler_function` |
| `ROS-R51` | `editing.borrowing_need_and_register` |
| `ROS-R52` | `editing.trope_register_fit` |
| `ROS-R54` | `norm.subjunctive_particle_duplication` |
| `ROS-R55` | `editing.expressive_syntax_choice` |
| `ROS-R56` | `editing.sentence_boundary_function` |
| `ROS-R57` | `editing.image_system_collision` |
| `ROS-R58` | `editing.rhetorical_figure_function` |
| `ROS-R59` | `norm.orthoepy_requires_current_verification` |

Cycle-1 MODEL_ONLY rules remain canonical in `libraries/rosenthal/rules.json`. Do not infer blanket bans on nominalization, passive, repetition, long sentences, participles, gerunds, colloquial markers, loanwords, tropes or rhetorical figures.
