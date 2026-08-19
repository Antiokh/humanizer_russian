# Contributing

`humanizer+ru` distinguishes language norm, native usage, editorial preference and AI heuristics. New rules should preserve that distinction.

## Before adding a rule

Classify it:

- `NORM-*` — source-backed Russian-language constraint;
- `SEM-*` — semantic/literary correctness;
- `NATIVE-*` — native-speaker preference among valid forms;
- `EDIT-*` — editorial clarity/density;
- `AI-CALQUE-*` — probabilistic machine/translation pattern;
- `AUTHOR-*` — corpus-derived idiolect behavior;
- `ARTIFACT-*` — technical trace.

Do not call a native preference a grammar rule. Do not call a grammar rule an AI pattern.

## Evidence expectations

For `NORM-*`, cite a directly relevant authoritative source.

For `AI-CALQUE-*` with a numeric threshold, document the corpus, language, genres, models/date and false-positive behavior. Without calibration, keep it a soft heuristic.

For `NATIVE-*`, provide positive and negative examples and explain context. Corpus evidence and philologist review are welcome, but the rule remains separate from academic norm unless a normative source supports it.

## Evals

Every meaningful rule should have at least one counterexample where the same surface form must be preserved.

A good eval suite contains:

- positive cases;
- negative/counterexample cases;
- ambiguity cases;
- author/genre exceptions;
- semantic-preservation checks.

## Linter

Regex/linter rules should be conservative. If correctness depends on meaning, discourse or authorial intent, emit a soft warning and let contextual review decide.

Only reliable technical `ARTIFACT` findings should affect the default exit status.

## Author profiles

Do not store raw corpus paths, private source text or inferred psychological diagnoses in generated profiles. Keep `observed_errors` separate from style and do not imitate errors by default.
