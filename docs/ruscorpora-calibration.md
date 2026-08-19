# Reproducible NKRЯ calibration workflow

The Nora Gal corpus claims are intentionally separated from the source study. `scripts/run_ruscorpora_query.py` exists to **replay an already designed and exported NKRЯ query**, not to invent a query or turn a concordance page into a prevalence estimate.

## Official API contract used

The National Corpus of the Russian Language currently documents a public API with bearer authentication. Its OpenAPI 1.0.2 schema exposes `POST /api/v1/lex-gramm/concordance` with a `LexGramQuery` JSON body. The official search guide recommends building the intended search and subcorpus in the web interface and pressing `Ctrl+Shift+E` on the result page to copy the generated JSON.

Official references:

- `https://ruscorpora.github.io/public-api/`
- `https://ruscorpora.ru/api/v1/openapi.json`
- `https://ruscorpora.github.io/public-api/about-api/search/index.html`
- `https://ruscorpora.github.io/public-api/about-api/search/common-format.html`
- `https://ruscorpora.github.io/public-api/about-api/search/lex-gramm.html`
- `https://ruscorpora.github.io/public-api/about-api/search/subcorpus.html`
- `https://ruscorpora.github.io/public-api/about-api/search/formula-rule.html`
- `https://ruscorpora.github.io/public-api/about-api/results/concordance.html`

The formula documentation exposes, among other syntax values, `partp` for an expanded participial construction and `gerp` for a gerund construction. These are suitable starting points for `GAL-CLAIM-03`, but the project must still define the exact comparison subcorpora before running them.

## Why the runner does not generate query JSON

A reproducible corpus claim requires a deliberately chosen subcorpus. Hand-building the request in project code would hide assumptions about period, genre, sphere, disambiguation, distance, sampling and pagination. The official UI can export the exact query that produced a result, so the project treats that exported JSON as the research fixture.

Workflow:

1. Log in to NKRЯ and obtain API access according to the official documentation.
2. Build the search and subcorpus in the NKRЯ web UI.
3. Run the search and, on the results page, press `Ctrl+Shift+E`.
4. Save the copied JSON locally, for example as `queries/claim03-written-partp.json`.
5. Inspect the JSON and record what corpus slice it represents.
6. Dry-run the fixture through the project runner.
7. Run the live request only after the design is accepted.
8. Review returned examples for false matches before calculating or publishing any aggregate.

## Offline dry run

```bash
python scripts/run_ruscorpora_query.py queries/claim03-written-partp.json --dry-run
```

The dry run validates that the fixture contains `corpus` and `lexGramm`, computes a canonical SHA-256 and records the query metadata without contacting NKRЯ.

Offline harness test:

```bash
python scripts/run_ruscorpora_query.py --self-test
```

## Live replay

The runner reads the API key only from `RUSCORPORA_API_TOKEN`:

```bash
export RUSCORPORA_API_TOKEN='...'
python scripts/run_ruscorpora_query.py \
  queries/claim03-written-partp.json \
  --output corpus-results/claim03-written-partp.json
```

`corpus-results/` is ignored by Git. The saved report includes:

- timestamp;
- fixture file name;
- canonical query SHA-256;
- endpoint;
- corpus/subcorpus presence and request params;
- raw response SHA-256;
- raw API response;
- counts of groups/documents/snippet groups/snippets actually returned on that page.

It never writes `RUSCORPORA_API_TOKEN` or the `Authorization` header.

## Important counting boundary

A concordance response is paginated. The runner therefore calls its counts `returned_*` and explicitly states that they are **not corpus prevalence or total hit counts**. It does not sum page-level data into an IPM or prevalence number by inference.

For a publishable frequency comparison, first establish from NKRЯ documentation/output which field is the valid total numerator and which corpus/subcorpus statistic is the valid word-count denominator. Then normalize consistently across matched slices and record that calculation separately.

## Claim-specific use

For `GAL-CLAIM-01`, export separate matched queries/subcorpora for the predeclared bureaucratic constructions across institutional, publicistic/newspaper and non-official registers and comparable periods. A raw modern hit count is not evidence of diffusion.

For `GAL-CLAIM-03`, export separate `partp` and `gerp` searches across deliberately matched written/spoken/register slices. Lower spoken frequency is not a grammatical error and does not by itself establish “dryness.”

For `GAL-CLAIM-14`, this lexicogrammatical concordance runner is not sufficient by itself. Lexical-diversity work needs a preregistered measure, matched/equalized samples and a separate analysis pipeline; do not force a “vocabulary impoverishment” conclusion out of concordance counts.

## Evidence promotion

A successful API response proves only that the query executed. A reviewed, normalized corpus result may change a claim's empirical evidence status. It still does not promote a Nora Gal editorial rule to `NORM`, `HARD_GATE` or `DEFAULT_MECHANICAL` without the project's separate normative/mechanical criteria.
