# Rosenthal operational reference

Use the Rosenthal library as a contextual editorial source, not as an impersonation or a frozen historical norm. Prefer current `russian` NORM where a modern rule exists.

Canonical source-specific rule cards are routed through `libraries/rosenthal/rules-index.json`. Five owner-supplied source cycles are integrated; cycle 4 is provenance-only and therefore does not add a rule file. For contextual review load only relevant `ROS-Rxx` cards; do not load or reproduce the copyrighted books.

Cycle 3 is a coauthored 3rd edition (Розенталь, Джанджакова, Кабанова; ЧеРо, 1999). Attribute its unique observations to the edition/source unless authorship of a particular passage is independently established.

Cycle 4 is D. E. Rosenthal, «Справочник по правописанию и стилистике», 5th corrected/expanded edition, ИК «Комплект», 1997. It is older and narrower than cycle 3 and ends at §213. Its value is independent edition provenance and evidence of norm change; later/current normative evidence wins where prescriptions differ.

Cycle 5 is the supplied DOCX «Справочник по русскому языку: орфография и пунктуация». The exact edition, publisher and year are not recoverable from that file, so they stay unknown rather than being inferred from external copies. It adds four MODEL_ONLY mechanisms: semantic choice among legitimate punctuation variants, coherent authorial punctuation, punctuation of spoken syntax, and same-form serial verb units. Concrete spelling tables and mandatory punctuation inventories remain current `russian/NORM` territory.

Mechanical findings are already emitted by `scripts/lint_rosenthal.py` and must not be duplicated by a model pass. Cycles 3–5 add no new mechanical finding. Cohesion, logic, audience, reported-speech fidelity, edit depth, dated morphology and most punctuation choices remain contextual or dictionary-dependent.
