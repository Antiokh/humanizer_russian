# External-source reproducibility gap

Status: `CLOSED` for `EXT-01` … `EXT-14` metadata as of 2026-08-20.

The primary-book study remains fully covered and reproducibly located by `SRC:L…` locators. This note concerns only the **secondary external verification registry** used to calibrate historical/editorial claims.

## Closure

Exact reproducibility metadata now lives in:

- `claims-external.md` — narrative claim-by-claim audit;
- `external-evidence-2026.json` — machine-readable source registry and dispositions.

For every `EXT-01` … `EXT-14`, the JSON registry records where applicable:

- canonical HTTPS URL;
- stable bibliographic identifier (DOI / PMCID / project identifier) when one exists;
- title and responsible organization/authors;
- exact entry, section or content locator;
- edition/layer/version metadata where the resource supplies it;
- access date.

The three pronunciation/norm sources explicitly retain their dictionary layer. Research-paper sources retain stable DOI identifiers; PMC-backed items also retain PMCID/PMID metadata.

## Re-audit result

Closing the bibliography gap **does not promote** any Chukovsky rule to current `NORM`, `HARD_GATE` or `DEFAULT_MECHANICAL`.

The external audit still has unresolved/contested/value-only claims. In particular:

- unresolved causal or historical generalizations stay unresolved;
- a modern source supporting a mechanism does not validate every stronger formulation in the book;
- historical dictionary prescriptions still require current item-by-item normative verification at decision time;
- source/editorial agreement never creates `NORM` by vote.

The machine-readable registry therefore stores `may_promote_norm_or_hard_gate: false` for every claim disposition.

## Runtime consequence

None of the seven Chukovsky `EXTENDED_SOFT` mechanics depends on the external registry for its surface trigger, so this pass changes provenance/reproducibility only.

`CHUK-R01`, `CHUK-R35`, `CHUK-R36` and `CHUK-R38` remain `MODEL_ONLY` wherever current evidence is required before a mandatory normative correction.

## Remaining research questions

Closing this locator/access-metadata gap does not answer the open substantive questions already listed in `claims-external.md`, including quantitative innovation thresholds, abbreviation-survival causation, bureaucratic nominalization calibration, psychological claims about formulaic prose, historical language-policy causation, and full revalidation of every dictionary item in the source.
