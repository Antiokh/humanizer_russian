# Knowledge libraries

`humanizer_russian` treats books/editorial systems as pluggable knowledge libraries.

A library lives in `libraries/<id>/library.json`. Two product modes consume the same libraries: compact `scripts/check.py` and editorial board `scripts/review.py`.

## Libraries are not evidence providers

Books/editorial systems answer **what this system recommends** and produce reviewer findings.

Corpora, dictionaries, current normative references and parsed datasets answer **what evidence is available**. They belong under `evidence/`, never become reviewer votes, and are optional/off by default. See `evidence/README.md`.

## Add a book

1. Keep research in a long-lived author branch.
2. Complete source study and mechanical-feasibility pass.
3. Add a source-specific linter where justified.
4. Add `libraries/<id>/library.json` and `reviewers/<id>.json`.
5. Add deterministic positive/negative/boundary tests.
6. Run library/lint/board validators.
7. Merge to `main`; keep the author branch.

Preferred adapter is `review_v1`. A finding contains `rule_id`, source-neutral `phenomenon_id`, project class, automation level, verdict, excerpt/location, reason and optional operation.

Two libraries may disagree. Preserve that disagreement. Book namespaces indicate provenance, not severity.

Evidence may use the same `phenomenon_id` to contextualize a finding, but remains a separate report field and does not enter `reviewer_verdicts`.
