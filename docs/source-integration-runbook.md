# Source Integration Runbook

Этот runbook описывает интеграцию книги/автора в `humanizer_russian` как **долгоживущей knowledge library**.

Главные принципы:

- `main` — источник архитектуры;
- ветка по фамилии автора (`gal`, `ilyakhov`, `chukovsky`, ...) — долгоживущая линия исследования источника;
- ветку автора после merge не удалять;
- одна и та же библиотека должна обслуживать два режима продукта: compact humanizer и editorial board;
- сначала mechanical feasibility, потом model-only residue;
- разные авторы могут не соглашаться, и этот конфликт надо сохранять.

## Phase 0 — start

Перед изменениями прочитать:

1. `AGENTS.md`;
2. `docs/book-study-framework.md`;
3. `docs/editorial-board-architecture.md`;
4. `libraries/README.md`;
5. при неполном study — `docs/book-study-prompt.md`.

Если книга уже доступна в текущем чате/контексте, использовать её как первичный источник. Если оригинал недоступен, допускается приватный source repo. Оригинальные охраняемые книги не копировать в публичный репозиторий.

## Gate A — STUDY

До runtime integration проверить источник по `book-study-framework`:

- source inventory и полное покрытие;
- последовательное чтение, а не snippets;
- atomic rules/concepts/positive operations;
- guards и counterexamples;
- interactions;
- provenance/locators;
- claims, требующие внешней проверки;
- loss audit и overgeneralization audit;
- preservation/no-op evals.

Минимальный статус для интеграции — `AUDITED`, предпочтительный — `OPERATIONAL`.

Старые regex, hard bans и старый `SKILL.md` из author branch считаются кандидатами, а не доказательством правильной автоматизации.

## Gate B — INTEGRATION MATRIX

До изменения core runtime составить матрицу для всех operational rules:

```text
rule_id
source_locator
provenance
project_class
scope
semantic_invariant
automation_level
surface_trigger
required_context
false_positive_risk
positive_case
natural_negative_control
boundary_case
intentional_counterexample
existing_overlap
native_usage_conflict
phenomenon_id
planned_module
runtime_visibility
```

`project_class`:

- `NORM`
- `NATIVE_USAGE`
- `EDITING`
- `AI_CALQUE`
- `AUTHOR`
- `ARTIFACT`

`automation_level`:

- `HARD_GATE`
- `DEFAULT_MECHANICAL`
- `EXTENDED_SOFT`
- `METRIC_ONLY`
- `MODEL_ONLY`

Source namespace (`GAL-*`, `ILY-*`, `CHUK-*`) — provenance, не severity.

## Gate C — MECHANICAL FEASIBILITY

Для каждого правила сначала проверить, можно ли вынести работу из prompt:

1. exact/string pattern;
2. regex;
3. tokenization;
4. morphology;
5. dependency parse;
6. structural/statistical signal;
7. metric-only;
8. только затем `MODEL_ONLY`.

Precision важнее recall. Если естественный negative control ломается, правило сужается или остаётся soft/model-only.

Не писать псевдолингвистический regex для задач, которым реально нужны смысл, референты, тема/рема, идиома, жанр, POV или авторское намерение.

## Gate D — SOURCE LIBRARY

Работа продолжается **в ветке автора**, а не в одноразовой integration branch.

Перед очередным PR аккуратно подтянуть свежий `main` в author branch. При конфликтах core-файлов архитектурный приоритет имеет текущий `main`; source-specific знания переносятся поверх него.

Для крупного источника добавить:

```text
scripts/lint_<author>.py        # или другой ясный source-specific module
libraries/<author>/library.json
reviewers/<author>.json
references/...                  # только производные знания/locators
source-specific evals/tests
```

Новые библиотеки предпочитают adapter `review_v1` из `libraries/README.md`.

### `phenomenon_id`

Это source-neutral идентификатор явления. Если несколько авторов описывают одну проблему, их `rule_id` остаются разными, но `phenomenon_id` должен совпадать там, где механизм действительно один.

Пример:

```text
GAL-...  ┐
ILY-...  ├─> editing.action_hidden_in_nominalization
CHUK-... ┘
```

Так compact mode может дедуплицировать сигнал, а editorial board — показать независимые мнения.

## Gate E — IMPLEMENTATION ORDER

Обязательный порядок:

1. `HARD_GATE` — только однозначные блокирующие случаи;
2. `DEFAULT_MECHANICAL` — high precision + deterministic negative controls;
3. `EXTENDED_SOFT` — полезные, но шумные surface heuristics;
4. `METRIC_ONLY` — измерять без ложной нормативности;
5. `MODEL_ONLY` — остаток после механизации.

Для `DEFAULT_MECHANICAL` нужны:

- true positive;
- natural negative control;
- boundary case;
- intentional-use counterexample, если применимо;
- exclusions (code/URL/quotes/dialogue/markdown), если нужны;
- deterministic regression.

Не удалять negative test ради зелёного CI.

## Gate F — TWO PRODUCT MODES

Каждая интегрированная библиотека должна быть совместима с обоими режимами.

### Compact

```bash
python scripts/check.py text.md
```

Короткая механическая проверка. Не обязана показывать provenance всех редакторов.

### Editorial board

```bash
python scripts/review.py text.md --style neutral
```

Сохраняет `reviewer_id`, группирует findings по `phenomenon_id`, показывает consensus/majority/conflict и применяет style policy.

Редакционный конфликт — нормальный результат. Не превращать разных авторов в одну «общую истину» при интеграции.

## Gate G — MODEL-ONLY RESIDUE

Только после mechanical pass:

- сделать короткие operational references;
- не грузить полный book study в обычный runtime;
- подгружать только релевантные rule cards;
- добавить preservation/no-op model evals;
- не дублировать в prompt то, что уже надёжно проверяет код.

## Compatibility with Russian core

Любое книжное правило проверить против:

- `USER_INTENT + SEMANTICS + NORM`;
- `NATIVE_USAGE`;
- контекстной экономии и эллипсиса;
- отсутствия немотивированных повторов;
- информационной структуры;
- функциональной парцелляции;
- прагматических частиц;
- author profile.

Если `EDITING`-совет конфликтует с живым русским, сначала сузить scope книжного правила.

## Tests before PR

Минимум:

```bash
python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/validate_libraries.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
python scripts/benchmark_board.py
```

Плюс source-specific self-test/validator, если он добавлен.

## PR and branch lifecycle

Финальный PR идёт:

```text
<author-branch> -> main
```

После merge ветку автора **сохранить**. Следующий цикл:

1. checkout author branch;
2. merge свежий `main`;
3. продолжить study/rules/tests;
4. открыть следующий PR из той же ветки.

Таким образом:

- `main` = стабильный собранный движок;
- `gal` / `ilyakhov` / `chukovsky` = непрерывная история исследований конкретных источников.

## Short formula

```text
BOOK / PRIVATE SOURCE
  -> AUDITED STUDY
  -> INTEGRATION MATRIX
  -> MECHANICAL FEASIBILITY
  -> SOURCE LIBRARY + NORMALIZED FINDINGS
  -> COMPACT + EDITORIAL BOARD
  -> MODEL-ONLY RESIDUE
  -> DETERMINISTIC CI
  -> AUTHOR BRANCH -> MAIN
  -> KEEP AUTHOR BRANCH
```
