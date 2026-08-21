# Branch cleanup note

Audit date: 2026-08-21.

The repository intentionally keeps long-lived source branches for recurring book/source work. These branches must **not** be deleted:

- `gal`
- `chukovsky`
- `ilyakhov`
- `visson`
- `velichko`
- `rosenthal`
- `golub`
- `main`

At audited `main` `c108a44794742f617ef91de1989cf7552d7ce463`, only `rosenthal` was synchronized. Other long-lived branches were behind main and ahead by 0. Synchronization and cleanup are tracked in issue #51.

## Temporary/merged refs to review

Deletion must be manual and only after checking that a branch contains no unique unmerged research. Candidate stale refs include:

- `migration-test`
- `migration-test-2`
- `migration-test-3`
- `ci-validation`
- `tmp-noop`
- `golub-recovery-inspect`
- `sync/velichko-main-20260820`
- merged `docs/*` branches
- merged `feature/*` branches
- superseded `agent/*` and `study/*` branches

Do not delete a branch merely because its name looks temporary. Compare it with `main` first.

The current GitHub integration used by the audit does not expose branch-ref deletion, so destructive cleanup is deliberately left as an explicit manual action.