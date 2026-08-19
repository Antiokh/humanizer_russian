# Architecture

`humanizer+ru` is organized around two hard constraints and several preference layers. Editorial sources such as Nora Gal do **not** form an additional authority above them: they provide methods for diagnosing and improving variants inside this architecture.

## Hard constraints

### SEMANTICS

Preserve facts, referents, causality, negation, scope, point of view and degree of certainty. A stylistically better sentence that changes these is a failed edit.

### NORM

Stay within valid Russian orthography, punctuation, agreement, government and syntax unless the user explicitly requests nonstandard stylization.

## Preference layers

### AUTHOR

When a reliable corpus/profile exists, prefer the author's established idiom, register, particles, jargon, rhythm and discourse habits.

### NATIVE_USAGE

Among grammatically valid variants, prefer the one that sounds natural to a Russian native speaker in the current context. This layer handles unnecessary repetition, contextual economy, information structure and marked word order.

### EDITING

Improve clarity, density, lexical precision, coherence of imagery and fit between wording and situation without inventing facts.

Nora Gal, information-style methods and other editorial traditions operate primarily here, but they also act as **diagnostic lenses across the whole text**. For example, a Gal-style check can expose a semantic error (wrong event order or reference), a norm error (dangling gerund), a native-usage problem (foreign syntax), or an author mismatch (wrong voice). The source does not itself determine the severity class.

### AI_CALQUE

Remove observable translation/LLM patterns: possessive over-explicitness, SVO lock, slogan rhetoric, literal collocations and locally self-contained sentence chains.

### Detector score

External diagnostic only. It must never override a higher layer.

## Editorial evidence is not another priority ladder

`references/nora-gal.md` is an operational editorial layer derived from the provided text of Nora Gal's *Slovo zhivoe i mertvoe*.

`references/nora-gal-source-map.md` records where each family of rules comes from and marks transferability:

- `G` — general Russian editing;
- `C` — contextual;
- `T` — primarily translation-specific;
- `H` — historically situated.

That distinction prevents four common mistakes:

1. turning Gal's stylistic advice into academic grammar;
2. turning her historically strong preference for Russian vocabulary into a blanket ban on modern borrowings;
3. turning observations about translation into universal rules for original Russian prose;
4. treating a good editor's reaction as proof that the editor's own replacement is mandatory.

## Conflict rule

A lower layer may not improve its own metric by degrading a higher layer.

Examples:

- deleting an em dash to satisfy a detector while worsening Russian punctuation is forbidden;
- splitting `не X, а Y` into two fragments solely because the pattern is associated with LLMs is forbidden;
- removing `же` as a stop-word when it encodes disagreement with prior context is forbidden;
- imitating a corpus author's missing commas to appear human is disabled by default;
- replacing a professional borrowing with an awkward Russian coinage merely because a historical editorial source preferred native vocabulary is forbidden;
- simplifying a long authorial period solely because it is long is forbidden;
- making every sentence locally more vivid if the accumulated changes alter the character or emotional stance is forbidden.

## Why NATIVE_USAGE is separate from NORM

`Это не ошибка в расчёте, а ошибка в исходных данных` can be grammatically acceptable while sounding unnecessarily synthetic because the common word `ошибка` is repeated.

`Это ошибка не в расчёте, а в исходных данных` stays inside the same norm but is often more natural.

That distinction is central to the project: normative sources determine what is allowed; native usage selects among allowed forms; author data can then override the generic preference when the author's actual voice supports another choice.

## Why Nora Gal is not just a final style pass

The original six-rule prototype treated Gal as a late semantic cleanup. The full source does not support that simplification. Her method repeatedly moves between levels:

- recover the actual action hidden by nominalizations;
- verify event order and references;
- choose a word by exact meaning, speaker, era and emotional situation;
- see whether an idiom or metaphor becomes physically absurd in context;
- rebuild foreign syntax as Russian syntax;
- preserve rhythm, sentence boundaries, subtext and author individuality;
- evaluate a local word against the whole character and scene;
- verify doubtful quotations, allusions and facts rather than guessing;
- distinguish a real error from an editor's preference.

Therefore `GAL-*` checks are cross-cutting diagnostics. They return the appropriate existing class (`SEMANTIC_ERROR`, `LANGUAGE_ERROR`, `NATIVE_WARNING`, `STYLE_WARNING`, `AUTHOR_MISMATCH`) rather than creating a new severity hierarchy.

## Joint-edit rule

A difficult sentence is not edited by independently toggling surface patterns.

1. Recover the semantic frame.
2. Identify agent, action, object and event order.
3. Remove unnecessary abstraction or repeated common material.
4. Rebuild natural Russian syntax and information structure.
5. Check lexical precision, collocation, imagery and physical plausibility.
6. Check persona, situation, era, emotional temperature and author profile.
7. Check rhythm, sentence boundaries and subtext in the surrounding passage.
8. Re-read the result for damage introduced by the edit itself.

This is shared by the `NATIVE_USAGE` architecture and the deeper Gal layer: rules work together.

## Editor behavior

The editor is allowed to insist on facts, meaning, requirements and actual language errors. For style, the editor should identify the problem before proposing a replacement.

If the first proposed rewrite erases the author's voice, it is not validated by the mere fact that the original sentence was rough. Search for a third solution that fixes the diagnosed problem while preserving authorship.

This is operationalized as:

- `GAL-EDITOR-NOT-DICTATOR`;
- `GAL-EDITOR-THIRD-SOLUTION`;
- `GAL-SELF-EDIT`.
