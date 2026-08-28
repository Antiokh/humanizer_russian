# Review checklist for this layer

Before merging:

- no source rule is applied outside its genre without explicit `PROJECT_DERIVED` status;
- no pending 2026 Rosarchive amendment is labeled current;
- no full copyrighted ГОСТ text is committed;
- all legislation-only rules are gated by `normative/legislation`;
- defined-term protection does not disable ordinary repetition checks globally;
- hard failures require high parser confidence;
- specialist-book gaps remain visible in audit.
