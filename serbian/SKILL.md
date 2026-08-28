---
name: humanizer_serbian_seed
description: Conservative Serbian-language editing seed that separates norm, native usage, interference, and accumulated AI-style signals.
---

# Serbian humanizer — seed policy

Improve Serbian prose because it is incorrect, unnatural, needlessly bureaucratic, calqued, structurally formulaic, or mismatched to the requested register. Do not rewrite text merely to make an AI detector happier.

## Priority order

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Among valid alternatives:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

`Do nothing` is a valid outcome.

## Serbian-specific invariants

- Treat Serbian Cyrillic and Serbian Latin as first-class scripts.
- Never convert script unless the user asks or accidental script mixing is itself the problem.
- Do not classify Latin script as less Serbian.
- Do not classify Cyrillic script as more formal by default.
- Ekavian and Ijekavian are both standard Serbian variants. Preserve the author’s configured/observed variant unless there is a concrete reason to change it.
- Preserve clitics, word order, aspect, ellipsis and repetition when they are doing real grammatical, informational or rhythmic work.

## Evidence classes

### NORM

Use modern standard-language evidence from Serbian standardization bodies and language institutions. A normative constraint may block an edit.

### NATIVE_USAGE

Use corpus and contextual evidence to choose among normative variants. Frequency does not create a norm.

### INTERFERENCE

Identify constructions that are grammatical or near-grammatical but patterned after another language. Keep English → Serbian and Russian → Serbian evidence separate.

### AI_STYLE_SIGNAL

These are accumulated stylistic diagnostics, never proof of authorship and never language errors by themselves.

Current seed signals:

1. repeated contrast scaffolds such as `nije A, već B` or `nije samo A, već i B`;
2. repeated three-member enumerations/descriptions;
3. identical section scaffolds repeated through a document;
4. excessive micro-headings in continuous prose;
5. generic metaphor chains and abstract “depth” language — model-only until calibrated;
6. suspicious English conceptual calques — classify as interference when supported, not as AI merely because an LLM also uses them.

## Required restraint

Never flag any of the following by itself:

- an em dash;
- one three-item list;
- one negative-parallelism construction;
- one metaphor;
- polished or error-free prose;
- Cyrillic;
- Latin script;
- Ekavian;
- Ijekavian.

Do not create Serbian equivalents of English “AI word lists” without Serbian evidence.

## Bureaucratic register

Serbian linguistic literature describes bureaucratic language through clusters such as verbosity, complexity, vagueness, stereotypy, impersonality, generalization and nominalization. Treat these as a contextual register profile. Do not ban nouns, passive constructions or `-nje` forms mechanically.

## Rewrite discipline

When editing:

1. preserve every factual claim and semantic relation;
2. fix actual Serbian-language problems first;
3. remove calques only when a natural Serbian alternative is justified;
4. reduce formulaic repetition when it is genuinely repetitive at document level;
5. keep distinctive authorial rhythm, particles, fragments, repetitions and colloquial choices when they fit the register;
6. never manufacture slang, mistakes or punctuation quirks to simulate a human author.

## Provenance

See `docs/serbian_public_sources.md` for the current source map and `docs/serbian_ai_signal_hypotheses.md` for hypotheses and counterexamples.
