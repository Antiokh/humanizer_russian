# Nora Gal — NKRЯ corpus calibration plan

This plan operationalizes the three historical/empirical source claims that the 2026 evidence audit deliberately leaves as `TESTABLE_NOT_YET_MEASURED`:

- `GAL-CLAIM-01` — spread/prevalence of bureaucratic constructions across registers;
- `GAL-CLAIM-03` — register/frequency claims about participial and gerund constructions;
- `GAL-CLAIM-14` — broad claims about vocabulary impoverishment/change.

It is a **measurement plan, not a result**. No number from this file may be cited as corpus evidence until the queries have actually been run and the returned material manually checked.

## Why NKRЯ is suitable

The National Corpus of the Russian Language provides separate and/or filterable written, newspaper, social-media and spoken material, supports user-defined subcorpora by metadata such as date/genre/sphere, and exposes lexicogrammatical search. In September 2025 NKRЯ also opened a public API for researchers/developers/teachers.

The API requires an authenticated access key. The official documentation says a logged-in user can obtain a key and use it as a Bearer token. Project automation must therefore read a token from an environment variable or local secret store and must never commit it.

Official API documentation:

- https://ruscorpora.ru/news/257
- https://ruscorpora.github.io/public-api/
- https://ruscorpora.ru/api/v1/openapi.json
- https://ruscorpora.github.io/public-api/about-api/search/index.html
- https://ruscorpora.github.io/public-api/about-api/search/common-format.html
- https://ruscorpora.github.io/public-api/about-api/search/lex-gramm.html
- https://ruscorpora.github.io/public-api/about-api/search/subcorpus.html
- https://ruscorpora.github.io/public-api/about-api/search/formula-rule.html
- https://ruscorpora.github.io/public-api/about-api/results/concordance.html

The official OpenAPI currently exposes `POST /api/v1/lex-gramm/concordance`; the request body is a `LexGramQuery`. The documented attribute vocabulary includes syntactic values `partp` (expanded participial construction) and `gerp` (gerund construction).

## Reproducibility rule

Do not hand-author a complicated API JSON query from memory when the web interface can export the exact query. NKRЯ's own API guide recommends:

1. build the intended query and subcorpus in the search UI;
2. open the result page;
3. press `Ctrl+Shift+E` to copy the generated JSON;
4. save that JSON as the canonical query fixture;
5. run the API request with the fixture unchanged except for explicitly versioned pagination/sampling fields.

Every published measurement should store:

- date of run;
- NKRЯ API/OpenAPI version if available;
- corpus/subcorpus definition;
- exact exported query JSON;
- corpus size in words/documents reported for that run;
- raw hit/document counts supplied by the API/interface;
- normalized rate and denominator;
- a manually reviewed random/stratified sample of hits;
- false-positive/exclusion notes;
- interpretation limits.

## `GAL-CLAIM-01`: bureaucratic-register diffusion

### Hypothesis to test

A predeclared family of administrative constructions becomes more frequent outside official/business writing over time.

This is **not equivalent** to “bad language increases.” The observable object must be a construction family, not an aesthetic label.

### Marker families

Start with high-precision source-derived constructions already present in project rules, then expand only after manual validation:

1. light/service verb + deverbal noun (`осуществлять/производить` + action nominalization);
2. administrative purpose frames such as `в целях осуществления ...`;
3. paper-deictic/formal frames only if a query can distinguish genuine document genre from leakage.

Do not aggregate every nominalization, passive or formal word into a “bureaucratese score.”

### Comparison design

Use matched period slices and compare at least:

- official/business or institutional prose (positive/register source);
- newspaper/publicistic prose;
- social-media material where date coverage permits;
- spoken material where comparable metadata/coverage permits.

For each construction family report IPM or hits per million corpus words where a valid denominator is available. If only concordance sample counts are available, label them as sample counts and do not convert them into prevalence estimates.

### Interpretation

Evidence for diffusion requires a register-by-time interaction, not merely a higher modern raw count in a larger corpus. A marker that remains concentrated in official prose does not support the source's “spread into everyday language” narrative.

## `GAL-CLAIM-03`: participles/gerunds by register

### Hypotheses to test separately

1. expanded participial constructions (`syntax=partp`) differ in frequency by register;
2. gerund constructions (`syntax=gerp`) differ in frequency by register;
3. density inside a sentence/document differs from simple occurrence frequency.

Do **not** test the vague proposition “participles are dead/dry.” Dryness is a reader-response/style judgment and requires a different study.

### Query basis

The NKRЯ API formula documentation explicitly lists:

- `partp` — распространенный причастный оборот;
- `gerp` — деепричастный оборот.

Use the preferred/disambiguated analyses where supported. Run the same grammatical query across comparable written and spoken/register subcorpora.

### Required controls

- separate participial and gerund constructions;
- compare normalized frequencies, not raw hits;
- inspect at least a sample of parsed hits for tagging errors;
- do not infer grammatical incorrectness from lower spoken frequency;
- do not turn a corpus frequency result into a universal style ban.

## `GAL-CLAIM-14`: vocabulary “impoverishment”

The source rhetoric is not operational enough to query directly. Before any corpus call, choose and preregister a specific observable.

Candidate observables:

- lemma-type/token diversity within equal-size samples;
- lexical dispersion across documents;
- proportion of high-frequency vocabulary within matched genres;
- diversity of content-word lemmas after controlling for sample size;
- domain-specific vocabulary breadth within the **same** genre/topic class.

### Invalid comparison

Do not compare a small literary/historical sample directly to a massive modern newspaper/social corpus and call a lower raw type/token ratio “impoverishment.” TTR is highly sample-size sensitive; topic and genre composition also change lexical diversity.

### Minimum acceptable design

1. choose one observable and document why it represents the proposed claim;
2. create matched genre/topic/time subcorpora;
3. equalize or statistically control sample size;
4. use lemmatized content words where appropriate;
5. bootstrap/sample repeatedly rather than rely on one draw;
6. publish uncertainty and sensitivity to corpus composition;
7. describe the result as lexical-distribution change, not civilizational “decline,” unless that evaluative step is independently defined and justified.

## API runner boundary

A project runner can safely automate **replay and capture** once exact NKRЯ query fixtures have been exported. It should:

- read `RUSCORPORA_API_TOKEN` from the environment;
- POST canonical fixtures to `https://ruscorpora.ru/api/v1/lex-gramm/concordance`;
- save raw responses under an ignored local results directory;
- record request SHA-256 and run timestamp;
- never commit the token;
- never infer prevalence from a paginated concordance page unless the API returns an explicit total/denominator that has been validated against documentation.

This repository does not yet ship claim-specific query fixtures because doing so without first building/exporting the intended subcorpora in the NKRЯ UI would create false reproducibility. The next executable step requires an NKRЯ access key and deliberate subcorpus definitions, not another heuristic guess.

## Promotion boundary

Even a strong corpus result changes only the **empirical evidence status** of a source claim. It does not by itself promote a Gal rule to `NORM`, `HARD_GATE` or `DEFAULT_MECHANICAL`.

Mechanical promotion still requires a high-precision observable with negative controls and acceptable false-positive behavior; normative promotion still requires an independent normative source.
