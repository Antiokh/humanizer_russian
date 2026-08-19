# Rule interactions — independent Chukovsky study

Status: `EXTRACTED`.

This pass reorganizes the extracted rules by mechanism rather than chapter. It does not yet compare them with existing project rules.

## I01 — Novelty triage

**Rules:** R01 → R02 → {R03, R04, R05, R06, R09, R10, R35}  
**Type:** prerequisite / routing

A novel-looking form should not be edited until its mechanism is classified. The most important failure is routing every unfamiliar form to “error”.

Compound failure example: an editor sees an unfamiliar clipped professional term, treats novelty as corruption, expands it, then accidentally makes expert prose less natural. R01 blocks age/taste bias, R02 classifies, R07/R09 test audience effort, R36 tests professional scope.

---

## I02 — Context first, lexical judgment second

**Rules:** R08 before R06/R07/R09/R11/R14/R15/R36/R37  
**Type:** prerequisite / scope

Audience and communicative scene are upstream of most vocabulary decisions. The same surface item can be:

- necessary specialist terminology;
- natural familiar speech;
- characterizing slang;
- inappropriate bureaucratic leakage.

The decision cannot be reproduced from the token alone.

---

## I03 — Official formula conflict: R14 vs R15

**Rules:** R14 ↔ R15  
**Type:** apparent contradiction resolved by genre

R14 says preserve formal templates when the genre needs them. R15 says remove official-register leakage where the formal function is absent.

Resolution question: **what institutional/genre function does the formula perform here?**

A detector that only recognizes bureaucratic vocabulary will systematically violate one of these rules.

---

## I04 — Compression conflict: R04/R09/R17/R30

**Rules:** R04, R09, R17, R30  
**Type:** competing economies

The book contains several different kinds of “economy”:

- omit recoverable content (R04);
- abbreviate when it saves reader effort (R09);
- unpack nominal packaging even if the result uses more words (R17);
- retain semantic repetition when it carries expressive force (R30).

Therefore raw character/word count is not the objective. The relevant cost is communicative effort plus preserved function.

---

## I05 — Ellipsis vs semantic reanalysis

**Rules:** R04 ↔ R05  
**Type:** diagnostic fork

Surface form: a complement appears absent.

Two incompatible analyses:

1. R04: complement is recoverable → omission may be natural;
2. R05: no complement is mentally supplied → word has a standalone/new lexical use.

Bad automation “restores” a complement in both cases and can change meaning.

---

## I06 — Direct language vs technical precision

**Rules:** R16/R17 ↔ R06/R07/R14/R36  
**Type:** conflict / priority by semantic gain

Direct nouns and verbs are preferred only when the abstract/technical form adds no useful distinction. A specialist category, legal label or process noun may be necessary.

Resolution test: remove the technical packaging in a trial version and compare **semantic delta**, not prettiness.

---

## I07 — Template detection vs legitimate repetition

**Rules:** R19 ↔ R30; R19 ↔ R28  
**Type:** conflict

Repeated wording can be:

- dead formula replacing thought (R19);
- deliberate rhythm/refrain (R30);
- exact terminology required by a narrow task (R28 counterexample).

The key variables are repeated function and semantic gain, not frequency alone.

---

## I08 — Modifier deletion vs expressive force

**Rules:** R18 ↔ R30/R31  
**Type:** conflict

Semantic subtraction may label an adjective informationally redundant. Before deleting it, check whether it contributes:

- contrast;
- stance;
- rhythm;
- emotional duration;
- conventional phrase value.

A purely semantic optimizer can make prose correct but dead.

---

## I09 — Proposition-first vs no-invention boundary

**Rules:** R21 + R27  
**Type:** compound guardrail

The source pushes the writer away from generic evaluative shells toward concrete engagement. But the input may not contain the detail needed to make the prose concrete.

Correct sequence:

1. identify the evaluation shell;
2. locate source-supported proposition/evidence;
3. state it if present;
4. if absent, do **not** fabricate specificity.

This is an important compound eval target.

---

## I10 — Voice preservation vs norm correction

**Rules:** R11/R37 ↔ R38/R35  
**Type:** conflict

Character/familiar voice can justify non-neutral vocabulary and register, but it does not automatically justify every grammar or reference error.

Need separate questions:

- is this form a deliberate/register-consistent voice feature?
- is it recognized in the relevant variety/community?
- is it simply an error with no voice function?

Historical examples in Chukovsky cannot settle the modern answer without R35.

---

## I11 — Slang observation vs person-level inference

**Rules:** R11 + R12 + R13  
**Type:** inference boundary

R11 may preserve slang because it accurately represents a speaker. R12 blocks the leap from one slang marker to moral/intellectual diagnosis. R13 blocks the further leap from editing the surface to claiming the underlying person/social cause is fixed.

This interaction is especially important because chapter 5 itself contains both strong moral claims and explicit counterexamples.

---

## I12 — Read-aloud pass after semantic reconstruction

**Rules:** R17/R23 → R22/R31  
**Type:** sequence

Sound should usually be checked after participant roles and proposition are stabilized. Otherwise a smoother rewrite may accidentally alter who did what.

Recommended independent sequence from the source:

`recover event/dependencies → preserve meaning → read aloud → adjust rhythm/sound`.

---

## I13 — Literal logic vs idiom recognition

**Rules:** R03/R29 → R32  
**Type:** prerequisite

Before diagnosing a metaphorical or logical contradiction, ask whether the expression is lexicalized/fixed. If it is, its components may no longer carry their old literal meanings.

This prevents “repairing” a normal idiom based on etymology.

---

## I14 — Idiom preservation vs deliberate deformation

**Rules:** R32 ↔ R33 → R34  
**Type:** exception handling

Default: established idiom is a whole (R32).

Exception: intentional decomposition/deformation can be expressive (R33).

Decision: R34 distinguishes artistic play from accidental contamination. Surface pattern alone is insufficient.

---

## I15 — Normative conservatism vs language change

**Rules:** R01/R02/R03 ↔ R38; concept C18  
**Type:** systemic tension

The book deliberately keeps two forces in tension:

- language changes and inherited objections can be wrong;
- a literary norm needs stability and cannot accept every spontaneous form immediately.

Any system that extracts only the anti-purist half or only the prescriptive half misrepresents the book.

---

## I16 — Historical dictionary is downstream of scope

**Rules:** R35 after R08; R36/R37 constrain R35  
**Type:** prerequisite / exception

The final dictionary begins with explicit professional and familiar-style caveats. Therefore a modern application pipeline cannot be:

`pair found → rewrite`.

It must be:

`identify phenomenon → identify scene/community → verify current norm → preserve recognized variant or correct`.

---

## I17 — Document-level “same operation” failure

**Rules:** R19, R21, R26, R28  
**Type:** document-level compound effect

A document may avoid repeated words and still be template-driven if every paragraph performs the same discourse move:

`generic claim → generic praise → generic conclusion`.

Conversely, deliberate terminological repetition can coexist with varied reasoning.

The document-level unit is therefore **operation/function**, not lexical diversity score.

---

## I18 — Register leakage can trigger semantic failure

**Rules:** R15 + R17 + R23 + R25  
**Type:** compound failure

Cancelearite is not only aesthetic. In the source, bureaucratic packaging can obscure participant roles, invert relation structure or create absurd semantic collisions.

A full diagnostic sequence is:

1. detect register mismatch;
2. unpack noun/action structure;
3. resolve dependencies;
4. replace empty procedural shells with the real act;
5. compare proposition before/after.

---

## I19 — “Good phrase becomes stamp” temporal interaction

**Rules:** R19 + R30  
**Type:** temporal/contextual

The source notes that an expressive pair can later become a bureaucratic cliché. Therefore neither “this formula was once expressive” nor “this formula is often a cliché” settles the present occurrence.

Decision variables: current context, frequency, function, voice and actual expressive load.

---

## I20 — Evidence hierarchy inside the book

**Rules:** R35/R38 + all source-derived rules  
**Type:** provenance/meta

The book contains several evidence types:

- Chukovsky's direct prescription;
- cited linguists' arguments;
- historical anecdotes;
- literary examples;
- reader letters;
- isolated jokes/parodies;
- broad moral/social claims;
- a prescriptive dictionary.

They do not support equal-strength rules. `SOURCE_EXAMPLE_ONLY` must not silently become a universal prohibition. Strong historical/current-norm claims belong in `claims.md` until verified.
