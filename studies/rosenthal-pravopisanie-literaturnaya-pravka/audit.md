# Audit

## Loss audit

The source was read sequentially to the final index. Orthography and punctuation are not omitted from coverage; they are deliberately delegated to the current Russian norm layer to avoid duplicate historical engines. Literary-editing sections §§139–213 were converted into 46 deduplicated operational/context rules.

## Overgeneralization audit

Rejected transformations:

- `nominalization = bad`: source explicitly licenses nominalizations in science, technology, official/business language, headings and plans.
- `standard formula = stamp`: source explicitly distinguishes functional standards from exhausted templates.
- `passive = bad`: active/passive/impersonal constructions distribute information differently.
- `repetition = bad`: repetition may be expressive or structural.
- `idiom variation = error`: intentional deformation and usage change exist.
- `book says so = current norm`: historical form lists require current verification.
- `gerund must have nominative subject`: current norm preserves controlled impersonal + infinitive constructions.
- broad regex for lexical government: rejected; most valency needs morphology/dependency/context.

## Mechanical feasibility

Two surfaces survive precision-first automation: a high-confidence subset of genitive forms after `согласно`, and a bounded mixed-correlative candidate `не только … а также`. Both exclude quotes/code/Markdown structural text. Prosody remains metric-only.
