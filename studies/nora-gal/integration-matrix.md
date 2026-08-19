# Nora Gal integration matrix

This is the integration pass performed **after** the independent book study. The 42 detailed operational records live in `libraries/gal/rules/*.json`; this file summarizes routing decisions without duplicating every rule card.

## Source-study gate

- supplied EPUB fingerprint: `38bdce9dfaf93ea820aae3fd0c7da74e9c2a908f5a3c77da2764793535bf4aa9`;
- spine coverage: 35/35;
- content-bearing documents: 30/30 `VERIFIED`;
- structural/title documents: 5/5 `NO_OPERATIONAL_CONTENT`;
- inaccessible parts: none;
- claims, loss audit and overgeneralization audit: recorded under `studies/nora-gal/`.

The source study is therefore complete for the supplied EPUB. This does not establish an exact print-edition identity and does not turn historical editorial preferences into modern `NORM`.

## Runtime classification

| Automation level | Count | Runtime consequence |
|---|---:|---|
| `HARD_GATE` | 0 | no book-derived hard gates |
| `DEFAULT_MECHANICAL` | 0 | compact default remains silent for Gal |
| `EXTENDED_SOFT` | 3 | available through `check.py --extended` and board mechanical pass |
| `METRIC_ONLY` | 3 | descriptive metrics only; no finding/verdict |
| `MODEL_ONLY` | 36 | loaded only as contextual residue when relevant |
| **Total** | **42** | one source rule registry used by both modes |

Mechanical rules:

- `GAL-KANZ-VERB` → `editing.action_hidden_in_nominalization`;
- `GAL-KANZ-PSEUDOFORMAL` → `editing.register_pseudoformality`;
- `GAL-EXPLICITNESS` → `editing.excessive_explicitness`.

Metric-only rules:

- `GAL-KANZ-PARTICIPLE`;
- `GAL-SOUND-COLLISION`;
- `GAL-LONG-SENTENCE-CLARITY`.

Everything else remains `MODEL_ONLY`; the compact operational reference is `libraries/gal/model-only.md`.

## Shared phenomena already present in other libraries

The integration reused a source-neutral `phenomenon_id` only where the mechanism is genuinely the same:

| Gal rule | Shared phenomenon | Existing source rule | Decision |
|---|---|---|---|
| `GAL-KANZ-VERB` | `editing.action_hidden_in_nominalization` | `CHUK-R17` | exact operational overlap; retain both provenance records |
| `GAL-KANZ-STAMP` | `editing.template_without_semantic_gain` | `CHUK-R19` | same diagnostic question: does a ready-made formula contribute a proposition/function? |
| `GAL-TERM-AUDIENCE` | `editing.terminology_audience_fit` | `CHUK-R07` | same audience/terminology mechanism |
| `GAL-IDIOM-CONTAMINATION` | `editing.idiom_play_vs_contamination` | `CHUK-R34` | same distinction between accidental contamination and intentional idiom play |

Related but deliberately **not** collapsed:

- `GAL-KANZ-PSEUDOFORMAL` vs `CHUK-R15`: a narrow pseudoformal shell is related to bureaucratic register leakage but is not the same decision boundary;
- `GAL-REGISTER-ERA-CULTURE` vs `CHUK-R08`: Gal's rule includes era/cultural-world fit, which is broader than scene register;
- `GAL-EXPLICITNESS` vs native possessive/context-economy signals: the source rule is broader than the existing narrow native phenomena, so a shared ID would create false equivalence.

## Mechanical feasibility decisions

The feasibility order was string/regex → token/structure → metric → model-only.

Three narrow surface routes survived negative controls. They remain `EXTENDED_SOFT`, not `DEFAULT_MECHANICAL`, because quotation, legal/formal usage and contextual ownership can make the surface form intentional. Markdown code/URL/non-prose filtering uses the same core `prose_text` normalization as other source adapters.

A real cross-library route is retained for `Осуществляется проведение …`: both Gal and Chukovsky can report `editing.action_hidden_in_nominalization`. Compact mode deduplicates the common phenomenon while retaining both rule IDs in provenance; board mode retains separate reviewer findings in one phenomenon group.

No source rule was promoted to `NORM` or `HARD_GATE` from the book alone.

## NATIVE_USAGE audit

All 42 operational records contain `conflict_with_native_usage`. The main recurring guards are:

- preserve safe ellipsis and context economy;
- do not ban participles, passive, long sentences, borrowings or unusual word order as classes;
- preserve functional repetition, pragmatic particles, authorial rhythm and parceling;
- do not invent concrete facts or agents;
- `AUTHOR` outranks `EDITING` among normative variants;
- strong sentence-final focus is a tendency, not a universal rule.

## Conflict policy

No **source-grounded mechanical** Gal/Chukovsky conflict was discovered in this integration. Shared mechanical phenomena currently produce compatible `REVIEW` signals. A synthetic `SOURCE_CONFLICT` fixture is nevertheless included in `tests/gal_board_cases.json` to prove that the board preserves an actual future disagreement instead of converting it to majority truth.

## Claims left outside runtime

`studies/nora-gal/claims.md` records historical/corpus/causal claims that still need independent modern evidence. In particular: prevalence of bureaucratese, blanket attitudes to borrowings, frequency/style claims about participles and gerunds, strong final-focus generalizations, causal claims about thought and language, and historical claims about machine translation.

## Runtime contract

- library manifest: `libraries/gal/library.json`;
- reviewer: `reviewers/gal.json` (`По системе Норы Галь`);
- normalized adapter: `scripts/lint_gal.py` (`review_v1`);
- source-specific deterministic suite: `scripts/benchmark_gal.py` + `tests/gal_cases.json`;
- compact integration suite: `tests/gal_compact_cases.json`;
- board integration suite: `tests/gal_board_cases.json`;
- structural/source validator: `scripts/validate_nora_gal.py`.

The original book is not stored in the public repository.
