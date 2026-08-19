# Old PR #1 — Nora Gal semantic layer

Historical source: `Antiokh/humanizer--ru` PR #1, `Add Nora Gal semantic language checks`.

The useful work from that branch is now part of `humanizer_russian` and no longer needs to be merged into the old fork.

## What was carried forward

The semantic layer was preserved, but reorganized so it is not tied to sequential pattern numbers that can collide with upstream rules.

Current namespace:

- `SEM-ABSTRACT-ALGEBRA` — empty abstractions / «словесная алгебра»;
- `SEM-VOICE-MISMATCH` — language that is grammatically valid but implausible for the speaker/situation;
- `SEM-METAPHOR-CONFLICT` — conflicting image systems / «слова на ножах»;
- `SEM-COLLOCATION` — broken/crossed collocations / «вывихнутое сочетание»;
- `SEM-SYNTAX-CALQUE` — foreign syntactic organization;
- `SEM-FOCUS` — semantic/information focus.

The active source is now `references/nora-gal.md`.

## Important design change

Nora Gal rules are contextual semantic/editorial checks, not hard bans and not regex truth.

The new hierarchy first protects:

1. `SEMANTICS` — no invented facts or changed confidence;
2. `NORM` — no real Russian-language errors;
3. `NATIVE_USAGE` — natural Russian among valid forms;
4. Nora Gal/editorial cleanup.

This prevents a semantic-editing rule from improving style by inventing specificity or overriding an intentional author voice.

## Review feedback preserved

The old CodeRabbit review correctly highlighted two risks in the first version:

- semantic checks could be skipped in audit-only workflows;
- “make it concrete” could accidentally reward invented facts not present in the source.

The independent project addresses these directly:

- semantic preservation is a hard invariant in `SKILL.md`, `gpt/INSTRUCTIONS.md` and `docs/semantic-preservation.md`;
- Nora Gal guidance explicitly says that missing specifics must not be invented;
- `evals/nora-gal.json` contains semantic-preservation expectations rather than a single canonical rewrite.

## Tests migrated

`evals/nora-gal.json` contains six semantic scenarios:

- abstraction without invention;
- voice mismatch;
- metaphor conflict;
- broken collocation;
- foreign-syntax calque;
- semantic focus preservation.

Manual coverage is also included in `gpt/TESTS.md`.

## Why the old PR is closed instead of merged

The old PR was stacked into a fork whose architecture still treated many detector correlations as language rules. The semantic layer now belongs to a larger independent architecture in `Antiokh/humanizer_russian`.

Closing the old PR preserves its discussion/history while avoiding accidental changes to `humanizer--ru/main`.
