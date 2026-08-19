# Book Study Card Schema

Этот документ задаёт минимальный общий contract для knowledge units. Он намеренно не является жёсткой JSON Schema v1: сначала framework должен пройти cross-review на нескольких книгах.

## 1. Common header

Каждый knowledge unit должен иметь:

```yaml
id: BOOK-KIND-NN
kind:
name:

source:
  locators:
    - "stable source locator"
  provenance: SOURCE_DIRECT | SOURCE_REPEATED | SOURCE_EXAMPLE_ONLY | PROJECT_DERIVED | PROJECT_REFINED | PROJECT_FORMULA | EXTERNAL_CONFIRMED | EXTERNAL_CONTESTED
  edition_confidence: exact | probable | unknown

scope:
  domain: []
  genre: []
  audience: []
  historical: false
  level: word | phrase | sentence | paragraph | scene | document | corpus

confidence: high | medium | low

project_role:
  layer:
  status: candidate | accepted | contested | deprecated | out_of_scope

public_safety: DERIVED | REVIEW | PRIVATE_ONLY
```

`source.locators` указывают место, но не содержат source prose.

## 2. CONCEPT

```yaml
kind: CONCEPT
definition:
boundaries:
  includes: []
  excludes: []
related: []
```

Главный тест: concept помогает различать случаи, а не просто даёт красивое название.

## 3. DISTINCTION

```yaml
kind: DISTINCTION
left:
right:
decision_difference:
diagnostic_question:
counterexample:
```

Distinction считается потерянным, если после extraction два разных случая снова получают одинаковое решение.

## 4. DIAGNOSTIC

```yaml
kind: DIAGNOSTIC
meaning:
trigger:
diagnostic_question:
possible_harm:
surface_proxy:
invariants: []
guard:
counterexample:
do_not_infer: []
automation:
  class: SOFT_SIGNAL | EDITING_OPPORTUNITY | MODEL_ONLY | METRIC_ONLY
  confidence:
```

Diagnostic никогда не должен скрыто содержать команду `delete`.

## 5. OPERATION

```yaml
kind: OPERATION
when:
operation:
inputs_required: []
success_test:
invariants: []
guard:
counterexample:
fallback:
automation:
  class: EDITING_OPPORTUNITY | MODEL_ONLY | REVIEW_GATE
```

Главное различие:

- diagnostic: `что проверить`;
- operation: `что построить/сравнить`.

## 6. FORMULA

```yaml
kind: FORMULA
inputs: []
transformation:
decision:
output:
success_condition:
guards: []
notation_owner: project
```

`notation_owner: project` означает, что компактная запись создана проектом, даже если механизм source-derived.

## 7. GUARD

```yaml
kind: GUARD
applies_to: []
condition:
prohibits:
reason:
counterexample_if_ignored:
```

Standalone guard нужен только если ограничение используется несколькими units. Иначе guard лучше хранить внутри operation/diagnostic.

## 8. CLAIM

```yaml
kind: CLAIM
claim:
claim_type: normative | scientific | statistical | historical | legal | technical | usage | causal | other
needed_for_operation: true | false
verification_status: NOT_NEEDED | UNVERIFIED | CONFIRMED | CONTESTED | OUTDATED | SCOPE_LIMITED
external_sources: []
```

Claim не становится hard rule без отдельного основания.

## 9. INTERACTION

```yaml
kind: INTERACTION
units: []
relation: prerequisite | sequence | conflict | refinement | joint_optimization | creates_risk_for | duplicate | supersedes_in_scope
description:
resolution:
compound_eval:
```

## 10. Project integration record

Это не source unit, а bridge:

```yaml
source_unit:
project_layer:
relation: CONFIRMS | REFINES | EXTENDS | CONFLICTS | DUPLICATES | OUT_OF_SCOPE
proposed_change:
required_external_evidence:
status:
```

## 11. Eval record

```yaml
id:
units: []
case_type: failure | positive_operation | preservation | counterexample | tricky | compound
prompt:
expectations: []
false_positive_if:
semantic_loss_if:
source_locators: []
```

Book examples по умолчанию не использовать.

## 12. Public-safety status

### `DERIVED`

Можно публиковать как самостоятельную проектную формулировку.

### `REVIEW`

Есть риск близкой зависимости от авторской формулировки, последовательности или уникального примера.

### `PRIVATE_ONLY`

Raw text, OCR, подробный close paraphrase, candidate quote pool, author-example corpus и другие source-workspace artifacts.

## 13. Proposed ID families

Framework не требует переименовывать существующие правила, но для новых studies можно использовать:

- `BOOK-C##` — concept;
- `BOOK-X##` — distinction;
- `BOOK-D##` — diagnostic;
- `BOOK-R##` — operation/recommendation;
- `BOOK-F##` — formula;
- `BOOK-G##` — standalone guard;
- `BOOK-CL##` — claim;
- `BOOK-I##` — interaction;
- `book-e##` — eval.

Существующие `GAL-*`, `ILY-*`, `ILY-R*`, `REC-*` сохраняются и маппятся через adapter.
