# Migration history

`humanizer_russian` is an independent repository for the project branded as **humanizer+ru**.

It was separated from `Antiokh/humanizer--ru` on 2026-08-19 after the Russian-language work had grown beyond a small compatibility fork.

## Source lines that were consolidated

### 1. Nora Gal semantic layer

Old repository:

- PR #1: `Add Nora Gal semantic language checks`
- branch: `agent/add-nora-gal-language-patterns`
- old head before the Russian-first work was stacked on it: `23da69d075cafd2423903146bc24d8beddf6ae5a`

That line introduced the semantic/literary layer in `references/nora-gal.md`, semantic evals and GPT guidance. The important idea was to treat abstraction, voice, metaphor conflicts, collocation and translated syntax as contextual semantic checks rather than regex hard bans.

### 2. Russian-first / native-usage layer

Old repository:

- PR #2: `Rebuild humanizer as Russian-first editor (humanizer+ru)`
- original working branch: `agent/russian-language-layer`
- migration staging branch: `humanizer_russian`

This line introduced the architecture that separates:

- `SEMANTICS` — factual and logical preservation;
- `NORM` — grammatical and punctuation constraints;
- `NATIVE_USAGE` — natural choices made by Russian native speakers among valid forms;
- `AUTHOR` — a corpus-derived idiolect layer;
- `EDITING` and `AI_CALQUE` — later editorial passes;
- detector score — diagnostic only, never the optimization target.

It also introduced:

- `references/russian-language.md`;
- `references/native-russian.md`;
- `references/rule-audit.md`;
- `references/evidence-audit.md`;
- author profiling and `profiles/schema.json`;
- a conservative surface linter;
- Russian-language evals and smoke tests;
- CI checks.

## Review feedback incorporated before migration

The old PR review was used as a final staging review. Valid findings were fixed before or during migration:

- author-profile sentence and n-gram statistics now preserve document boundaries;
- source filesystem paths are no longer written to `profile.json`;
- profiler, schema, documentation and CI use one canonical profile v1 contract;
- generated author profiles are validated against the JSON Schema in CI;
- `NATIVE_WARNING` is documented as non-gating;
- repeated common material is checked for contrasts with both `а` and `но`;
- Russian-language eval documentation covers the current `ru-01` — `ru-21` suite;
- an unrelated RusGram citation for zero subjects/ellipsis was replaced with references that match the claims.

One automated-review suggestion was explicitly rejected: a claim that only Business/Enterprise/Edu workspaces can create GPTs. The setup documentation follows the current official OpenAI guidance instead: GPT building/editing is available to paid ChatGPT users, with additional role/workspace controls in managed workspaces.

## Why this is not a GitHub fork

The new repository is intentionally independent. The project still credits the projects and code it grew from, but future architecture does not need to remain compatible with the detector-driven assumptions of the old fork.

## Old repository policy after migration

`Antiokh/humanizer--ru` should remain the small compatibility fork. The semantic/NATIVE_USAGE development branches and their PRs can be closed after the migrated code is verified in this repository.

The old PR and commit history remains on GitHub as historical review context even after the development branches are removed.
