# Mechanical feasibility report

The search order for every source rule was:

`regex → tokenizer → morphology → dependency/statistical check → metric → MODEL_ONLY`.

The point is not to maximize the number of regexes. A mechanical implementation is accepted only when its surface evidence is strong enough to survive natural negative controls.

## Result by mechanism

### 1. Narrow lexical / phrase patterns

Useful mechanically, but usually only in extended mode:

- `PS-R09` common-knowledge wrappers — regex candidate; function remains contextual.
- `PS-R11` verbal numbering — tokenizer/regex cluster; normal in algorithms, so extended only.
- `PS-R13` ceremonial politeness — phrase **cluster**, not a single polite formula.
- `PS-R18` decorative intensification — lexical **cluster**, never a ban on one intensifier.
- `PS-R21` present-time wrappers — phrase candidate with explicit temporal-contrast exclusions.
- `PS-R22` bureaucratic shells — conservative phrase candidates; legal/official register creates FP risk.
- `PS-R62` meta-introduction — narrow informational-genre candidate only.
- `PS-R63` ritual conclusion — narrow candidate only.
- `PS-R76` suspicious precision — only a very narrow broad-population percentage pattern can be surfaced; the claim still requires verification.
- `PS-R85` generic self-presentation benefit — only generic-praise clusters, scoped to extended review.

These are `EXTENDED_SOFT`, not default correctness rules.

### 2. Project-derived high-precision subset

`PS-R22` + `PS-R29` jointly motivate a narrower operator:

**ILY-M01 — bureaucratic tautology**

Detect only explicit light-verb / nominalization duplication such as forms equivalent to:

- `осуществить проведение ...`;
- `произвести выполнение ...`;
- `провести осуществление ...`.

This is intentionally much narrower than either source rule. It does **not** flag normal combinations such as `провести исследование`, `осуществить переход`, `выполнить проверку` or a normal passive result phrase.

Feasibility: regex + morphology-lite inflection lists are sufficient. No LLM is needed for the narrow subset. Candidate for `DEFAULT_MECHANICAL` after deterministic negative controls pass.

### 3. Token/structure metrics

Mechanically measurable but not safe to call an error:

- `PS-R48` — span between paired correlatives (`не только … но и`, `как … так и`, `если … то`): `METRIC_ONLY` for span length / token distance.
- `PS-R50` — density of state predicates / copular descriptions: `METRIC_ONLY`; definitions and state descriptions are normal Russian.
- `PS-R101` — comma count / multi-comma sentence count: `METRIC_ONLY`; punctuation itself is not the defect.

No threshold from the book is promoted to a language rule.

### 4. Morphology/dependency candidates rejected from current runtime

The following could in principle benefit from a morphological or dependency parser, but the available deterministic evidence would still not resolve the semantic question reliably enough:

- `PS-R29` broad nominalization detection;
- `PS-R30` participial/gerund load;
- `PS-R31` passive event vs state;
- `PS-R32` whether an actor should be named;
- `PS-R45` weak glue between independent messages;
- `PS-R46` nested subordination whose hierarchy is or is not transparent;
- `PS-R47` removable cognitive frame vs necessary attribution;
- `PS-R49` bad parcellation vs contextual ellipsis;
- `PS-R51` semantically redundant homogeneous members.

A parser can identify surface structure but not reliably decide whether the structure is functionally justified. These remain `MODEL_ONLY` or, where noted, metric-only.

### 5. Semantic / discourse / audience rules

The majority of the source model necessarily remains `MODEL_ONLY`. This includes:

- reader task and goal;
- truth, confidence, attribution and unsupported generalization;
- whether an evaluation has sufficient evidence;
- whether a word is simple **for this audience**;
- whether a euphemism hides a material fact;
- whether uncertainty is genuine;
- whether numeric precision is consequential;
- what entities are new to the reader;
- paragraph dominant theme;
- didactic known→new ordering;
- relevance of facts;
- product benefit and limitations;
- self-presentation usefulness;
- vacancy requirement matching;
- final naturalness/content review;
- whether a non-text medium is better.

Regexes for these would produce pseudo-linguistic noise.

## Old implementation demotions

The old author-branch linter is narrowed as follows:

- `я считаю, что` / similar frames: **remove as mechanical finding**; model-only because attribution/uncertainty may be essential.
- broad nominalization regex: **remove from default**; retain only narrow tautological subset as `ILY-M01`.
- state-predicate cluster: **metric only**.
- long-correlative fixed character threshold: **metric only**.
- single common-knowledge, politeness, intensifier or time phrase: never a default error; extended candidate only.
- generic intro/conclusion/praise: extended and genre-sensitive only.

## Mechanical implementation plan

1. New `scripts/lint_ilyakhov.py` owns source-specific findings and metrics.
2. `scripts/lint.py` aggregates it.
3. `scripts/check.py` exposes only `ILY-M01` in default mechanical mode; all other Ilyakhov findings require `--extended`.
4. Source-specific self-tests include true positives, natural negatives, boundaries and intentional-use controls.
5. Central benchmark adds regression cases without weakening existing negative controls.
6. Only after deterministic tests pass is the model-only residue summarized in the runtime reference layer.

## Expected source-rule automation distribution

The full 102 source rules are classified conservatively:

- `HARD_GATE`: 0
- `DEFAULT_MECHANICAL`: 0
- `EXTENDED_SOFT`: 10
- `METRIC_ONLY`: 3
- `MODEL_ONLY`: 89

`ILY-M01` is a **PROJECT_DERIVED** default-mechanical subset of `PS-R22` + `PS-R29`; it is not counted as a source rule and is not presented as a direct quotation/rule of the authors.
