# Safety of automatic edits

Automatic rewrite is intentionally narrow in legal-document mode.

Allowed mechanically only when semantics cannot change, e.g. formatting normalization with deterministic target.

Prefer `REVIEW` for:

- terminology substitutions;
- movement of conditions/exceptions;
- restructuring obligations;
- changing cross-references;
- splitting legal sentences;
- adding/removing definitions.

The legal-document layer should diagnose first and rewrite only with context.
