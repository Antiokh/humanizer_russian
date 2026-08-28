# Serbian AI-style hypotheses

Status: research hypotheses for calibration. None of these signals proves AI authorship.

## H1 — contrast-template density

Repeated instances of Serbian contrast frames such as:

- `A nije B, već C`
- `A nije samo B, već i C`
- `Ne samo A, već i B`
- `Ne A, već B`

may become formulaic when they recur at high density or in near-identical syntactic positions.

Source seed: Bojan Viculin, P.U.L.S.E, 2026.

Counterexample requirement: a single occurrence is normal Serbian and must not trigger a finding.

## H2 — repeated triplets

Repeated three-member lists and repeated descriptions with three coordinated adjectives/adverbs may form a detectable document-level scaffold.

Source seed: Bojan Viculin, P.U.L.S.E, 2026.

Counterexample requirement: ordinary rhetorical triplets and factual lists are valid Serbian.

## H3 — structural over-regularity

Identical section labels, paragraph openings, or internal mini-templates repeated across many document sections are a stronger signal than individual “AI words”.

Community seed: Serbian discussion of a political programme in which the same two labels reportedly recur once per measure across dozens of measures.

This should be measured as repetition/entropy, not with a blacklist.

## H4 — micro-heading density

Headings every few lines can make generated prose look mechanically partitioned.

Source seed: P.U.L.S.E analysis.

Counterexample requirement: reference documentation, FAQs, API docs and slide-like notes legitimately use dense headings.

## H5 — generic metaphor chains

Repeated generic metaphors (`tkivo`, `arena`, `bojno polje`, `ogledalo`, `mašina`, etc.) combined with abstract claims may create an inflated, generic register.

This is model-only until calibrated. Individual metaphors are not findings.

## H6 — English conceptual calques

Literal conceptual transfers such as `alat za razumevanje` may be grammatical yet unnatural in specific Serbian contexts.

This belongs to `INTERFERENCE`, not AI detection. It requires context and corpus validation.

## Rejected naive signals

### Em dash

Serbian users explicitly report that humans who have long used `—` are now accused of AI use. Therefore dash presence is a social stereotype and a required negative test, not a rule.

### Error-free prose

A Serbian learner discussion jokingly treats “too many mistakes for ChatGPT” as evidence of human authorship. This shows a perception bias, not a valid detector feature.

### Cyrillic vs Latin

Both scripts are normal Serbian. Script choice is not an AI signal.
