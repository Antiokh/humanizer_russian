# Proposed profile contract

Suggested future CLI/API shape:

```text
--register legal
--document-profile official-admin
--document-profile normative
--document-profile normative/legislation
--document-profile contractual
--document-profile legal-procedural
```

`register` changes linguistic priors; `document-profile` enables document-level structural rules. These should remain separate so a legal professional can write an ordinary email without triggering legislation structure checks.
