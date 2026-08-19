# Error versus preference

A humanizer must not collapse these categories:

- `LANGUAGE_ERROR`: violates Russian norm;
- `NATIVE_WARNING`: grammatical but potentially synthetic in context;
- `STYLE_WARNING`: a stylistic choice may be weak/repetitive;
- `AI_PATTERN`: probabilistic association with machine/translation behavior;
- `AUTHOR_MISMATCH`: inconsistent with a corpus-derived voice.

Example:

> Это не ошибка в расчёте, а ошибка в исходных данных.

This is not a language error. It can still receive a native-use suggestion to factor `ошибка` once.

That distinction prevents detector/editing preferences from being mislabeled as grammar.
