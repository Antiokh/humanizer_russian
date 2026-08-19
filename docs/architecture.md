# Architecture

`humanizer+ru` is organized around two hard constraints and several preference layers.

## Hard constraints

### SEMANTICS

Preserve facts, referents, causality, negation, scope and degree of certainty. A stylistically better sentence that changes these is a failed edit.

### NORM

Stay within valid Russian orthography, punctuation, agreement, government and syntax unless the user explicitly requests nonstandard stylization.

## Preference layers

### AUTHOR

When a reliable corpus/profile exists, prefer the author's established idiom, register, particles, jargon, rhythm and discourse habits.

### NATIVE_USAGE

Among grammatically valid variants, prefer the one that sounds natural to a Russian native speaker in the current context. This layer handles unnecessary repetition, contextual economy, information structure and marked word order.

### EDITING

Improve clarity, density and concrete wording without inventing facts. Nora Gal and information-style methods primarily operate here and at the semantic boundary.

### AI_CALQUE

Remove observable translation/LLM patterns: possessive over-explicitness, SVO lock, slogan rhetoric, literal collocations and locally self-contained sentence chains.

### Detector score

External diagnostic only. It must never override a higher layer.

## Conflict rule

A lower layer may not improve its own metric by degrading a higher layer.

Examples:

- deleting an em dash to satisfy a detector while worsening Russian punctuation is forbidden;
- splitting `не X, а Y` into two fragments solely because the pattern is associated with LLMs is forbidden;
- removing `же` as a stop-word when it encodes disagreement with prior context is forbidden;
- imitating a corpus author's missing commas to appear human is disabled by default.

## Why NATIVE_USAGE is separate from NORM

`Это не ошибка в расчёте, а ошибка в исходных данных` can be grammatically acceptable while sounding unnecessarily synthetic because the common word `ошибка` is repeated.

`Это ошибка не в расчёте, а в исходных данных` stays inside the same norm but is often more natural.

That distinction is central to the project: normative sources determine what is allowed; native usage selects among allowed forms; author data can then override the generic preference when the author's actual voice supports another choice.
