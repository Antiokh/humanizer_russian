# Independent philologist review packet

This packet is for an external specialist in contemporary Russian grammar, syntax, stylistics and/or editing. Its purpose is to audit the project's boundary between **language norm**, **marked but acceptable Russian**, **native-speaker preference**, **editorial preference**, **author-dependent choice**, and questions that require more context or corpus evidence.

It is **not** an AI-detector review. The reviewer should not answer “does this look AI-generated?” and should not optimize text to fool a detector. The project treats detector evidence as a separate, weak layer.

## Architecture being reviewed

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among variants that satisfy those constraints:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

The key distinction is deliberate:

- `NORM` asks whether a construction is linguistically acceptable/correct in contemporary Russian and should be supported by an appropriate normative/grammatical source when classified as an error;
- `NATIVE_USAGE` asks which acceptable variant is more natural in the specified context;
- `EDITING` asks whether an acceptable formulation is clearer, more economical, more precise or better fitted to genre/function;
- `AUTHOR` protects a confirmed individual voice among normative variants;
- `SEMANTICS` blocks edits that change fact, referent, causality, thesis or degree of certainty.

The reviewer is specifically asked to detect places where the project accidentally turns a stylistic preference into a language rule, or conversely treats a real normative problem as mere style.

## Independence protocol

The first pass should be blind to the project's own answer.

Do **not** send `reviews/philologist-cases.json` directly to the reviewer: that internal registry contains `project_position`, `rule_ids` and `phenomena` for traceability.

Generate the blind packet instead:

```bash
python scripts/export_philologist_packet.py --format md --output /tmp/philologist-review.md
```

or:

```bash
python scripts/export_philologist_packet.py --format json --output /tmp/philologist-review.json
```

The exporter is self-tested so the blind packet contains no `project_position` and no `GAL-*`, `CHUK-*` or `ILY-*` rule IDs.

After the reviewer completes the first pass, the project may disclose the internal positions and source mappings for a second-pass discussion. Do not overwrite the first-pass answers; preserve both if the reviewer changes a judgment after seeing the project rationale.

## Requested primary classification

Choose one per case:

- `LANGUAGE_ERROR` — a real error/non-normative construction. A normative or grammatical source is required.
- `NORMATIVE_VARIANT` — an ordinary acceptable variant with no independent reason to prefer a rewrite.
- `MARKED_BUT_ACCEPTABLE` — acceptable Russian, but marked by register, order, prosody, rhetoric or other conditions.
- `NATIVE_PREFERENCE` — several variants are acceptable, but one is systematically more natural for a native speaker in the specified context.
- `EDITING_PREFERENCE` — not a language issue; a contextual editorial operation may improve clarity, precision, economy or structure.
- `AUTHOR_DEPENDENT` — the right choice materially depends on established author/character voice.
- `NEEDS_CONTEXT` — the supplied context is insufficient to choose responsibly.
- `NEEDS_CORPUS` — an empirical usage/frequency claim is needed before classifying the preference.
- `NEEDS_NORM_SOURCE` — the reviewer suspects a normative boundary but will not call it an error without checking an appropriate source.

Also choose a practical verdict:

- `KEEP`
- `CHANGE`
- `REVIEW`
- `NEEDS_VERIFICATION`

Confidence is `LOW`, `MEDIUM` or `HIGH`.

## Evidence discipline

If `primary_class=LANGUAGE_ERROR`, give a source that actually supports the relevant norm. A style handbook saying “prefer X” is not automatically evidence that Y is ungrammatical.

For contested usage, distinguish:

1. dictionary/grammar/normative status;
2. corpus distribution;
3. genre/register preference;
4. individual authorial preference.

If a claim is corpus-dependent, say `NEEDS_CORPUS` rather than estimating prevalence from intuition.

For context-sensitive recommendations, give at least one counterexample or boundary where the opposite choice is valid. The validation schema deliberately requires this for marked/native/editorial/author/context classifications.

## High-risk areas covered by the 28 cases

The case set deliberately concentrates on boundaries likely to produce harmful overgeneralization:

- theme/rheme and Russian word order;
- strong initial focus vs final-focus tendencies;
- `не X, а Y` and factoring common repeated material;
- functional repetition;
- functional differences among `а`, `но`, `зато`;
- dialogue ellipsis, zero subjects and referential ambiguity;
- gerund subject agreement vs legitimate participial/gerund use;
- passive voice;
- nominalization and official/technical register;
- parcellated enumeration vs purposeful parcellation;
- pragmatic particles;
- professional borrowings and audience fit;
- literal calques/collocations;
- idiom contamination vs wordplay;
- metaphor/image collision vs intentional artistic effect;
- author voice and editorial overreach;
- POV consistency;
- possessive over-explicitness;
- repeated explicit subjects/context undercompression;
- semantic gain in contrast constructions;
- colon before introduced enumeration;
- long-sentence clarity without numerical bans;
- agreement of multiple editorial sources vs independent language norm.

## Files

Internal canonical cases:

- `reviews/philologist-cases.json`

Blind exporter:

- `scripts/export_philologist_packet.py`

Fillable result template:

- `reviews/philologist-review-template.json`

Completed-review schema:

- `schemas/philologist-review.schema.json`

Validator:

- `scripts/validate_philologist_review.py`

## Completing a review

Copy the template outside the repository or to a local ignored file, fill all 28 cases, then validate:

```bash
cp reviews/philologist-review-template.json philologist-review.local.json
python scripts/validate_philologist_review.py philologist-review.local.json
```

`*.local.json` is already ignored by Git.

A completed review requires:

- reviewer name;
- qualification;
- affiliation or `independent`;
- conflict-of-interest statement;
- review date;
- exactly one answer for PHIL-01..PHIL-28;
- primary class, verdict and confidence;
- a non-empty reason;
- normative source for every `LANGUAGE_ERROR`;
- a counterexample/boundary for context-sensitive classifications.

The reviewer may leave `preferred_variant`, `normative_source`, `counterexample` or `notes` empty only where they are genuinely not applicable under the validation rules.

## Integration policy after human review

Do not count the 28 answers as votes for a generic “quality score.” Integrate them case by case.

A reviewer can:

- confirm or reject a `NORM` boundary;
- downgrade a supposed norm to marked/native/editorial preference;
- identify a missing exception or counterexample;
- request a corpus test;
- identify terminology that is linguistically inaccurate;
- show that two project phenomena should be merged or split.

A reviewer cannot by authority alone:

- turn a personal taste into `NORM`;
- make an editorial rule a `HARD_GATE` without a reliable mechanical condition;
- prove AI authorship;
- justify semantic changes;
- override an established authorial choice when the alternative is also normative without explaining the functional reason.

When integrating feedback, preserve the original review artifact and add project decisions separately. Do not silently rewrite the expert's answer to match the code.
