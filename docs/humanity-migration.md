# “Humanity” / native-Russian layer migration

The work that began as “make the text look less AI-written” was reframed during development into a native-language problem.

## Core change

Old question:

> Which surface features make a detector think this is AI?

New question:

> Given the same meaning and correct Russian, which form would a native speaker naturally choose here?

This produced the separate `NATIVE_USAGE` layer.

## Main rules carried forward

- context can carry recoverable information;
- common repeated material is factored before synonymization;
- exact repetition is preserved when rhetorically functional;
- case/agreement/government allow word order to follow information structure;
- sentence beginning and ending can both carry strong focus;
- parcellation is evaluated by function;
- particles can encode relation to prior context;
- native preferences are not mislabelled as grammar;
- native warnings are non-gating;
- author-specific habits are derived from corpus data instead of injected generically.

## Key example

Synthetic but grammatical:

> Это не ошибка в расчёте, а ошибка в исходных данных.

Neutral native compression:

> Это ошибка не в расчёте, а в исходных данных.

Marked correction under suitable context:

> Это не в расчёте ошибка, а в исходных данных.

The project treats these as a joint compression + information-structure decision, not as independent “remove repetition” and “randomize word order” operations.
