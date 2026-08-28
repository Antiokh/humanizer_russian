# Legal document layer — implementation plan

## Phase 1 — public-source mechanics

Safe candidates for code before specialist books:

1. `defined-term-order` — `(далее — X)` and use-before-definition detection.
2. `defined-term-collision` — one short name introduced for multiple full names.
3. `internal-reference-resolution` — references to numbered sections/points/apps must resolve when parser confidence is high.
4. `legislation-preamble-content` — only under explicit `normative/legislation` profile; detect obvious numbered articles/definition patterns/imperative prescriptions inside a marked preamble as `REVIEW`.
5. `source-effective-date` — rules have jurisdiction/status/effective dates and cannot activate while `PENDING_CHANGE`.

## Phase 2 — book-derived language mechanics

After specialist books:

- stable legal terminology vs harmful synonymization;
- legal collocation and terminology errors;
- syntax of rights, duties, prohibitions, permissions and conditions;
- placement/scope of qualifiers and exceptions;
- information order in official and legal genres;
- accepted formulae vs empty bureaucratic padding;
- sentence/document ambiguity diagnostics;
- genre-specific composition.

## Phase 3 — document profiles

Profiles should enable rules, not globally rewrite style:

- `official-admin`
- `normative`
- `normative/legislation`
- `contractual`
- `legal-procedural`

The default humanizer remains general Russian and should not acquire legal-document warnings unless a profile is selected or strongly inferred.
