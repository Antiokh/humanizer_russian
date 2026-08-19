# Migration history

`humanizer_russian` is an independent repository and the canonical project name.

It was separated from `Antiokh/humanizer--ru` on 2026-08-19 after the Russian-language work had grown beyond a small compatibility fork.

Historical branch/PR titles below are preserved only as references to old GitHub objects; they are not current product names.

## Source lines that were consolidated

### 1. Nora Gal semantic layer

Old repository:

- PR #1: `Add Nora Gal semantic language checks`;
- branch: `agent/add-nora-gal-language-patterns`;
- old head before the Russian-first work was stacked on it: `23da69d075cafd2423903146bc24d8beddf6ae5a`.

That line introduced the semantic/literary layer in `references/nora-gal.md`, semantic evals and GPT guidance. The important idea was to treat abstraction, voice, metaphor conflicts, collocation and translated syntax as contextual semantic checks rather than regex hard bans.

### 2. Russian-first / native-usage layer

Old repository:

- PR #2: `Rebuild humanizer as Russian-first editor (humanizer+ru)` — historical title;
- original working branch: `agent/russian-language-layer`;
- migration staging branch: `humanizer_russian`.

This line introduced the architecture that separates internal responsibilities:

- `SEMANTICS` — factual and logical preservation;
- `NORM` — grammatical and punctuation constraints;
- `NATIVE_USAGE` — natural choices made by Russian native speakers among valid forms;
- `AUTHOR` — a corpus-derived idiolect layer;
- `EDITING` and `AI_CALQUE` — later editorial passes;
- detector score — diagnostic only, never the optimization target.

All of these are now parts of one `humanizer_russian` project.

It also introduced:

- `references/russian-language.md`;
- `references/native-russian.md`;
- `references/rule-audit.md`;
- `references/evidence-audit.md`;
- author profiling and `profiles/schema.json`;
- a conservative surface linter;
- Russian-language evals and smoke tests;
- CI checks.

## Later native-Russian refinement

The next pass added a separate source-of-context file, `references/native-russian-user-context.md`, to preserve the owner's observations about actual native speech before formalizing them into rules.

The implementation then moved further toward:

- paragraph/context-first editing;
- safe ellipsis and context economy;
- factoring repeated common material before synonym substitution;
- information-structure-aware word order;
- strong initial/final positions;
- distinction between real dialogue and slogan Q/A;
- one unified author-personalization layer inside the same project.

## Why this is not a GitHub fork

The repository is intentionally independent. It still credits the projects and code it grew from, but future architecture does not need to remain compatible with detector-driven assumptions of the old fork.

## Old repository policy after migration

`Antiokh/humanizer--ru` can remain the small compatibility/historical fork. Old PR and commit history remains useful as review context, but active development belongs in `Antiokh/humanizer_russian`.