# Knowledge libraries

`humanizer_russian` treats every book/source layer as a pluggable knowledge library.

A library lives in `libraries/<id>/library.json`. It declares provenance, reviewer identity and the linter adapter/module used at runtime. The original book does **not** belong in this public repository.

Two product modes consume the same libraries:

- compact: `scripts/check.py` — one short mechanical-first verdict;
- editorial board: `scripts/review.py` — preserves reviewer provenance, disagreement and style policy.

## Add a new book

1. Keep the research in a long-lived author branch (`gal`, `ilyakhov`, `chukovsky`, ...).
2. Complete the book/source study and mechanical-feasibility pass.
3. Add a source-specific linter module where mechanical checks are justified.
4. Add `libraries/<id>/library.json` from `_template/library.json`.
5. Add `reviewers/<id>.json` from `reviewers/_template.json`.
6. Add deterministic positive/negative/boundary tests.
7. Run `scripts/validate_libraries.py`, `scripts/benchmark_lint.py`, and `scripts/benchmark_board.py`.
8. Merge the author branch into `main`; keep the author branch for later research.

## Runtime adapter contract

Preferred adapter: `review_v1`.

The declared Python module exports:

```python
def review(text: str) -> dict:
    return {
        "findings": [
            {
                "rule_id": "GAL-001",
                "phenomenon_id": "editing.action_hidden_in_nominalization",
                "project_class": "EDITING",
                "automation_level": "EXTENDED_SOFT",
                "verdict": "CHANGE",
                "excerpt": "...",
                "line": 1,
                "reason": "...",
                "operation": "recover_actor_action_object"
            }
        ],
        "metrics": {}
    }
```

`library_runtime.py` fills `library_id`, `source_namespace` and `reviewer_id` from the manifest, so source modules do not need to duplicate registry metadata.

`legacy_lint_v1` exists only to adapt the current core `scripts/lint.py` while source libraries migrate to the normalized contract.

## Findings are opinions, not merged truth

Two libraries may disagree. Do not erase that disagreement by collapsing rules during integration. Give semantically equivalent findings a shared `phenomenon_id`; the editorial-board layer can then show consensus, majority, compatible alternatives or conflict.

Book namespaces (`GAL-*`, `ILY-*`, `CHUK-*`) indicate provenance. They do not determine severity or normative status.
