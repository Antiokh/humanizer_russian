# Initial rules — legal-document book corpus

These are first-pass extractions. `PROJECT_REFINED` means the project narrows a source observation to avoid turning a stylistic tendency into a universal hard rule.

## LDB-001 — Genre determines composition

Source locator: `BOOK-MARYEVA-2015-2`, p. 121, ch. 7.
Scope: document.
Basis: `SOURCE_DIRECT`.
Level: document.
Confidence: high.

### What it checks

Do not impose one universal information order on all official/legal documents. Determine the genre first; composition and degree of formal rigidity depend on it.

### Trigger

A document is being generated or substantially restructured.

### Project use

Require/infer `document-profile` before genre-specific composition diagnostics.

### Do not apply automatically

Do not treat every deviation from a template as an error. Some genres have a rigid form; ordinary business correspondence allows more structural freedom.

## LDB-002 — Information order must express the logical relation

Source locator: `BOOK-MARYEVA-2015-2`, p. 121.
Scope: all professional documents.
Basis: `PROJECT_REFINED` from source examples.
Level: paragraph/document.
Confidence: high.

### What it checks

The order should make the intended relation recoverable: cause → consequence; thesis → argument → conclusion; ground → request/decision, when that relation is actually present.

### Do not infer

There is no universal rule that every document must use one of these exact sequences.

## LDB-003 — Document editing proceeds from whole to detail

Source locators: `BOOK-NOVOSELTSEVA-2018`, pp. 73–74; `BOOK-MARYEVA-2015-2`, p. 122.
Scope: editing workflow.
Basis: `SOURCE_REPEATED`.
Level: document.
Confidence: high.

### Diagnostic sequence

1. Read/check the document as a whole and identify its form/genre.
2. Check required/formal elements against the applicable current source.
3. Check factual sufficiency and internal consistency: numbers, dates, names, references.
4. Check composition/logical sequence.
5. Perform linguistic/stylistic editing.
6. Re-read the final document for semantics, logic, facts and communicative task.

### Interaction

This supports the project principle that legal-document mode must not begin with sentence-level beautification.

## LDB-004 — Conventional cliché is not an automatic style defect

Source locator: `BOOK-NOVOSELTSEVA-2018`, p. 7.
Scope: official-admin / legal register.
Basis: `SOURCE_DIRECT`.
Level: phrase.
Confidence: high.

### What it checks

Formulaic expressions can be functional conventions in official-business text. Do not flag a phrase merely because it is repeated across documents or would sound clichéd in ordinary prose.

### Trigger examples by class

- grounds/purpose formula;
- notification formula;
- standard legal collocation;
- standardized action formula.

### Negative boundary

This does not protect empty bureaucratic padding. The phrase must perform a document function or be an established domain collocation.

## LDB-005 — Legal wording prioritizes unambiguous interpretation

Source locators: `BOOK-ABRAMOVA-2017`, pp. 129–131; `BOOK-MOTYAKINA-LOPATIN-2016`, around p. 20.
Scope: legal documents.
Basis: `SOURCE_REPEATED`.
Level: sentence/document.
Confidence: high.

### What it checks

A legally significant formulation should make the relevant actor, action, object, condition, exception and consequence as determinate as the genre requires.

### Project diagnostics

- ambiguous referent;
- unclear condition scope;
- unclear exception attachment;
- deadline without a recoverable reference point;
- obligation without a recoverable obligated party;
- competing interpretations caused by coordination or modifier placement.

### Severity

Usually `REVIEW`; promote only when the contradiction or unresolved reference is mechanically provable.

## LDB-006 — Preserve established professional terminology

Source locators: `BOOK-ABRAMOVA-2017`, p. 130; `BOOK-MOTYAKINA-LOPATIN-2016`, around p. 20.
Scope: legal/official documents.
Basis: `PROJECT_REFINED`.
Level: term/document.
Confidence: high.

### What it checks

Prefer established, recognizable professional terms and formulations where they carry domain meaning. Generic anti-repetition editing must not silently replace them with approximate synonyms.

### Interaction

Overrides generic synonymization pressure but not correction of an actually wrong legal term.

## LDB-007 — Structural hierarchy is semantic, not decorative

Source locator: `BOOK-ABRAMOVA-2017`, pp. 129–130.
Scope: legal documents.
Basis: `SOURCE_DIRECT` + `PROJECT_REFINED`.
Level: document.
Confidence: medium-high.

### What it checks

Where a genre distinguishes functional parts, headings/sections should preserve those roles. Structure should help the reader distinguish grounds, operative provisions, rights, duties, findings, requests or other genre-specific functions.

### Negative boundary

Not every contract or legal document has legally ranked sections. Do not invent hierarchy merely to make a document look formal.

## LDB-008 — Directive modality must match the legal function

Source locator: `BOOK-BEGLOVA-2019`, p. 144 onward.
Scope: normative / official-admin.
Basis: `PROJECT_REFINED`.
Level: clause.
Confidence: medium-high.

### What it checks

Distinguish at least:

- obligation;
- prohibition;
- permission/right;
- recommendation;
- factual statement.

Do not paraphrase one class into another during editing.

### Mechanical opportunity

Build a modality lexicon as a diagnostic aid, but do not infer legal force from one token alone.

## LDB-009 — Avoid vague references where exactness is required

Source locator: `BOOK-MARYEVA-2015-2`, p. 122.
Scope: legal/official documents.
Basis: `PROJECT_REFINED`.
Level: phrase.
Confidence: high.

### What it checks

Expressions such as relative dates, unnamed documents, vague quantities or unclear referents are candidates for review when the text requires verifiable precision.

### Example classes

- `в прошлом году` where the legal/administrative period matters;
- `в ближайшее время` where a deadline is required;
- `указанный документ` with multiple possible antecedents.

### Negative boundary

Relative phrasing is not inherently wrong when the reference point is unambiguous and stable in context.

## LDB-010 — Direct word order is a register prior, not a hard grammar rule

Source locator: `BOOK-NOVOSELTSEVA-2018`, p. 8.
Scope: official-business prose.
Basis: `PROJECT_REFINED` from a source tendency.
Level: sentence.
Confidence: medium.

### What it checks

The source describes direct word order as characteristic of official-business syntax because it supports logical sequence and precision.

### Project constraint

Do **not** turn this into `subject-verb-object required`. Russian information structure still matters. Use only as a weak review prior when marked order causes ambiguity or obscures legal relations.

## LDB-011 — Formal requirements in old books are historical until revalidated

Source: corpus-wide project rule.
Scope: formal/document layout.
Basis: `PROJECT_DERIVED`.
Level: source governance.
Confidence: high.

### What it checks

A pre-2025 book may be valuable for language and genre conventions but must not activate a formatting/requisite rule solely on its authority.

### Resolution

Cross-check against current ГОСТ Р 7.0.97-2025, Rosarchive rules and other applicable current sources.
