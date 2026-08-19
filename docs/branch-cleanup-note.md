# Branch cleanup note

Branch deletion is not exposed by the current GitHub integration. After the old PRs are closed, obsolete refs can be removed manually in GitHub:

Old repo:
- `agent/add-nora-gal-language-patterns`
- `agent/russian-language-layer`
- `humanizer_russian`

New repo temporary refs created during migration:
- `migration-test`
- `migration-test-2`
- `migration-test-3`
- `ci-validation` (after CI validation is finished)

Do not delete `main`.
