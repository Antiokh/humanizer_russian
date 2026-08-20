# Rosenthal MODEL_ONLY residue

Canonical cumulative routing lives in `rules-index.json`. Rule groups now cover cycles 1, 2, 3 and 5; cycle 4 is provenance-only.

Mechanical surfaces emitted by `scripts/lint_rosenthal.py` remain only `ROS-R30`, `ROS-R44`, `ROS-R53`. `ROS-R10` remains metric-only. **Cycles 3–5 add no mechanical findings.**

## Cycle 5 contextual rules

| Rule | Phenomenon |
|---|---|
| `ROS-R75` | `editing.punctuation_variant_semantic_choice` |
| `ROS-R76` | `author.punctuation_system_intent` |
| `ROS-R77` | `register.spoken_syntax_punctuation` |
| `ROS-R78` | `native.serial_verb_unit_punctuation` |

Do not infer blanket bans or automatic normalization of punctuation variation, authorial punctuation, parcellation, topic segmentation, conversational syntax, or adjacent same-form verbs. Current `russian/NORM` owns concrete mandatory orthography and punctuation.
