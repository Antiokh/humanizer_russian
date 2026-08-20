# Integration matrix

| Layer | Rosenthal result | Runtime |
|---|---|---|
| Source identity | SHA-256 + OPF metadata + full coverage | study only |
| Current norm | verified item-by-item, never inherited wholesale | Russian/NORM + Rosenthal provenance |
| Mechanical | ROS-R30, ROS-R44 | `scripts/lint_rosenthal.py` → compact `--extended` + Editorial Board |
| Metric | ROS-R10 | descriptive only |
| Contextual editing | 43 MODEL_ONLY rules | board/model reference, not regex |
| Cross-author overlap | shared `phenomenon_id`, source-specific `rule_id` | generic compact/board dedupe |
| Later Rosenthal sources | append provenance/rules to same library | long-lived `rosenthal` branch |

No Rosenthal rule is a HARD_GATE or DEFAULT_MECHANICAL finding in this first source cycle.
