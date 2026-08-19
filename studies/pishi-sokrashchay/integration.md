# Post-study integration pass

This file was written **after** the independent source model, coverage, loss audit and overgeneralization audit were completed.

It is not part of the source extraction. It maps the source study onto the current `humanizer_russian` architecture.

## 1. Existing project architecture

Current base architecture:

`SEMANTICS / NORM > AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

The book is an editorial source. It does not define Russian grammar, contemporary norm or AI provenance.

Therefore:

- source-derived recommendations default to `EDITING`;
- a recommendation can support `SEMANTICS` only when the actual edit would change a fact, attribution, quantity, causality or certainty;
- syntax advice that collides with natural Russian is constrained by `NATIVE_USAGE`;
- author voice remains above generic editing preferences;
- nothing in this book alone creates an `AI_PATTERN`;
- nothing in this book alone creates a deterministic `HARD_GATE`.

## 2. What the independent study confirms from the existing `ilyakhov` branch

Only after completing the independent extraction, the study was compared with the existing `ilyakhov` branch.

The earlier branch's split into diagnostic `ILY-*` and positive `ILY-R*` was substantively sound. The independent pass re-derived most of its central mechanisms:

- simplify without semantic loss;
- stop-word as candidate rather than delete-list;
- remove shell, then raise useful information;
- common-knowledge, verbal-numbering, politeness, intensifier and time-wrapper checks;
- evaluation → existing evidence/scenario;
- bureaucratic shell and nominalization → event/action;
- precise term over decorative complexity;
- real uncertainty must survive;
- numeric precision depends on task and consequences;
- new-entity cognitive load rather than «one thought» counting;
- do not force an actor/SVO;
- parcellation ≠ contextual ellipsis;
- long correlatives are a distance/load issue, not a ban;
- paragraph dominant-theme / first-sentence navigation;
- known → new scaffolding;
- concrete support for abstraction;
- facts selected by reader task;
- naturalness as the final editing review.

This convergence is useful because it was obtained independently rather than by searching the book for support of the existing registry.

## 3. What the deep study adds or separates more clearly

The new `PS-*` registry is intentionally larger because it preserves distinctions that the earlier 36+24 model compressed.

Important additions:

1. **Reader-task layer before editing** — `PS-R01`, `PS-R02`, `PS-R56`–`PS-R61`.
2. **Truth/claim-strength layer** — `PS-R03`, `PS-R37`–`PS-R40`, plus a separate claims audit.
3. **Register/formalism split** — bureaucratic opacity is separated from legitimate official register (`PS-R22`–`PS-R24`).
4. **Pseudo-diagnostic language** — psychology/medical labels without evidence (`PS-R28`).
5. **Consequential number handling** — uncertainty, exactness, lower bounds, measurement provenance and accidental arithmetic are separate (`PS-R33`–`PS-R36`, `PS-R74`–`PS-R77`).
6. **Punctuation guard** — heavy syntax is not repaired by deleting normative commas (`PS-R101`).
7. **Headline integrity** — topic/navigation/attention/context-isolation are separate (`PS-R64`–`PS-R67`).
8. **Didactic structure** — known→new, subject introduction, demonstration, practice and troubleshooting (`PS-R68`–`PS-R73`).
9. **Commercial module** — product benefit, limitations, evidence and audience respect (`PS-R79`–`PS-R82`).
10. **Self-presentation module** — role, usefulness, specificity, details, scenarios, limitations, mission, credentials and client cases (`PS-R83`–`PS-R92`).
11. **Job-application module** — requirement mapping, targeting, proof and honest gaps (`PS-R93`–`PS-R96`).
12. **Meta-anti-template rule** — do not mechanically copy the book's own formulas (`PS-R98`).
13. **No invented advantage** — editing cannot repair a weak product/company by fabricating strengths (`PS-R102`).
14. **Non-text solution** — illustration/demo/table/interface can sometimes solve the reader task better than prose (`PS-R100`).

## 4. Proposed project adoption

Do **not** paste all 102 rules into `SKILL.md`.

Use a two-tier architecture.

### Tier A — compact SKILL operators

The main skill should contain a compact workflow built from these families:

1. task and semantic invariant — `PS-R01`–`PS-R05`;
2. functional surface check — `PS-R06`–`PS-R14`;
3. evaluation/evidence — `PS-R15`–`PS-R18`, `PS-R37`–`PS-R40`;
4. specificity/register/action — `PS-R19`–`PS-R32`;
5. uncertainty and numbers — `PS-R33`–`PS-R36`, `PS-R74`–`PS-R77`;
6. cognitive load and syntax — `PS-R41`–`PS-R52`, `PS-R101`;
7. paragraph/goal/structure — `PS-R53`–`PS-R63`;
8. headings/didactics — `PS-R64`–`PS-R73`;
9. final content/naturalness review — `PS-R78`, `PS-R98`–`PS-R100`, `PS-R102`.

### Tier B — scoped modules

Load only when the genre requires them:

- `commercial`: `PS-R79`–`PS-R82`;
- `self_presentation`: `PS-R83`–`PS-R92`;
- `job_application`: `PS-R93`–`PS-R96`.

This prevents a generic Russian humanizer from turning every text into a landing page or cover letter.

## 5. Proposed linter boundary

The linter may detect **surface opportunities**, not apply source advice automatically.

| Rule | Suggested automation | Reason |
|---|---|---|
| `PS-R06` | `SOFT_SIGNAL` | known candidate families; function still contextual |
| `PS-R09` | `SOFT_SIGNAL` | common-knowledge wrappers are lexically visible |
| `PS-R11` | `SOFT_SIGNAL` | verbal-numbering cluster |
| `PS-R13` | `SOFT_SIGNAL` | repeated ceremonial politeness |
| `PS-R18` | `SOFT_SIGNAL` | clustered intensifiers, not single token |
| `PS-R21` | `SOFT_SIGNAL` | common empty present-time wrappers |
| `PS-R22` | `EDITING_OPPORTUNITY` | bureaucratic shell candidates |
| `PS-R29` | `EDITING_OPPORTUNITY` | light-verb/nominalization candidates |
| `PS-R48` | `SOFT_SIGNAL` | very long correlative dependency |
| `PS-R54` | `REVIEW_GATE` | requires paragraph/document interpretation |
| `PS-R62` | `EDITING_OPPORTUNITY` only with narrow meta-lead patterns | genre-sensitive |
| `PS-R63` | `EDITING_OPPORTUNITY` only with ritual conclusion patterns | genre-sensitive |
| `PS-R76` | `SOFT_SIGNAL` | suspicious precision prompts source verification; never means false |
| `PS-R101` | `METRIC_ONLY` | comma count cannot be a defect by itself |

All other `PS-*` rules remain `MODEL_ONLY` unless corpus testing justifies a conservative proxy.

No book-derived finding should exit non-zero by itself.

## 6. Mapping to project layers

### `SEMANTICS`

Especially relevant:

`PS-R03`, `PS-R12`, `PS-R24`, `PS-R28`, `PS-R33`–`PS-R40`, `PS-R66`, `PS-R76`, `PS-R77`, `PS-R81`, `PS-R97`, `PS-R102`.

They become semantic errors only after context establishes actual distortion or unsupported strengthening. The source pattern itself is not an error.

### `NATIVE_USAGE`

Especially relevant:

`PS-R08`, `PS-R30`–`PS-R32`, `PS-R45`–`PS-R50`, `PS-R78`, `PS-R101`.

These are precisely where literal informational-style rules can make Russian mechanical. `NATIVE_USAGE` remains the higher arbitration layer.

### `EDITING`

All other general rules are editing opportunities/operations.

### `AUTHOR`

The book does not provide a generic author-profile model. Instead its rules create preservation constraints: subjective stance, deliberate rhythm, genre-specific evaluation, functional asides and voice must survive when the confirmed author uses them.

### `AI_CALQUE`

None of the `PS-*` units are evidence of AI authorship. Some overlap with modern LLM habits (bureaucratic shells, generic praise, meta-intros), but that relationship must be established separately.

## 7. Claims that must not enter SKILL as facts

`counterexamples-claims.md` isolates broad claims about cognition, buying, illustrations, recommendations, HR behaviour, language simplification, punctuation, reader psychology and the historical Главред score.

These can motivate tests but must not be stated as established science or current product truth without separate evidence.

## 8. Migration recommendation

The independent study should become the provenance foundation for the Ilyakhov/Sarycheva layer, but the existing `ILY-*` IDs should **not** be mass-renamed yet.

Recommended next step after review:

1. keep `PS-*` as study/source IDs;
2. keep `ILY-*` as project/operator IDs;
3. create an adapter map `PS-* → ILY-* / new project operator`;
4. merge duplicates;
5. promote only stable, cross-reviewed operations into the main SKILL;
6. retain domain modules outside the always-on core;
7. run corpus false-positive testing before expanding the regex linter.

This keeps source fidelity separate from runtime API stability.
