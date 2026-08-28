# Rule interactions

## Defined terms vs repetition cleanup

`DOC-M05` and `DOC-P02` must run before general repetition/synonymization suggestions. A token or phrase recognized as a defined professional term should be protected from automatic synonym replacement.

## Document profile before structural lint

`DOC-N01`, `DOC-N02` and legislation-specific parts of `DOC-N03` activate only after profile resolution to `normative/legislation`.

## Reference parsing before hard gate

`DOC-N04` may become a hard failure only after the parser establishes with high confidence that the phrase is an internal document reference and the target cannot be resolved.

## Source status before rule activation

`DOC-P01` precedes all rules imported from normative sources. A rule with a future effective date or `PENDING_CHANGE` status must not be applied as current law.
