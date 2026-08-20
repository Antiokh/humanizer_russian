# Unified Golub knowledge library

Two coauthored books feed one long-lived source library: `Книга о хорошей речи` (1997) + `Занимательная стилистика` (1988) → one deduplicated study.

- Deduplicated phenomena: **93**
- Cross-book overlap: **83**
- GOOD-only: **6**
- STYLE-only: **4**
- Analytic classes: `{'AI_CALQUE': 5, 'AUTHOR': 7, 'EDITING': 45, 'HISTORICAL': 9, 'NATIVE_USAGE': 6, 'NORM': 15, 'REGISTER': 6}`
- Automation: `{'HARD_GATE': 0, 'DEFAULT_MECHANICAL': 3, 'EXTENDED_SOFT': 1, 'METRIC_ONLY': 2, 'MODEL_ONLY': 87}`
- PROJECT_DERIVED AI_CALQUE observations: **5**
- Mandatory runtime-context growth: **none**

See `studies/golub/` for source inventory, complete coverage, atomic cards, cross-book audit, modern-norm verification, mechanical feasibility, integration matrix and audits.

## Rosenthal cycle-1 alignment

After Rosenthal cycle 1 entered `main`, Golub was re-audited against `ROS-R01..ROS-R46`. Equivalent mechanisms now reuse Rosenthal/source-neutral phenomenon IDs where appropriate. Shared surface detection for `согласно` and the paired conjunction is implemented once in `scripts/shared_russian_norm_surfaces.py`; Golub and Rosenthal adapters only attach their own provenance/verdict.
