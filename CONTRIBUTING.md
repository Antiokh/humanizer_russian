# Contributing

`humanizer_russian` — единый проект русского редактора/humanizer с двумя product modes: compact и editorial board.

Перед изменением правил, линтера, skill или source-specific слоёв прочитай `AGENTS.md`, `docs/source-integration-runbook.md` и `libraries/README.md`.

## Core priorities

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Preference among valid forms:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Mechanical-first runtime:

```bash
python scripts/check.py text.md
```

Editorial-board runtime:

```bash
python scripts/review.py text.md --style neutral
```

Оба режима используют одни и те же libraries/rules. Не дублируй реализацию специально для board.

## Rule classes

- `NORM-*` — source-backed ограничение русского языка;
- `NATIVE-*` — предпочтение живого русского;
- `EDIT-*` — редакторская операция;
- `AI-CALQUE-*` — вероятностный машинный/переводной паттерн;
- `AUTHOR-*` — corpus-derived идиолект;
- `ARTIFACT-*` — технический след;
- `GAL-*`, `ILY-*`, `CHUK-*` и другие namespaces — provenance, не severity.

## Automation levels

- `HARD_GATE`;
- `DEFAULT_MECHANICAL`;
- `EXTENDED_SOFT`;
- `METRIC_ONLY`;
- `MODEL_ONLY`.

Для `DEFAULT_MECHANICAL` нужны true positive, natural negative control, boundary case, intentional counterexample (если применимо) и deterministic regression. Precision важнее recall.

## Books as knowledge libraries

Каждый крупный источник интегрируется как отдельная library:

```text
libraries/<author>/library.json
reviewers/<author>.json
scripts/lint_<author>.py
source-specific evals/references
```

Предпочтительный adapter для новых libraries — `review_v1`.

Каждый source finding сохраняет свой `rule_id`. Если несколько источников описывают один механизм, используйте общий source-neutral `phenomenon_id`.

Разногласие авторов не надо «чинить» при merge. Editorial board должен уметь показать `SOURCE_CONFLICT`; конкретный стиль может разрешить конфликт позже.

## Author branch lifecycle

Исследовательские ветки по фамилии автора (`gal`, `ilyakhov`, `chukovsky`, ...) — долгоживущие.

Перед очередным PR подтяни свежий `main` в author branch, сохрани архитектуру `main`, затем открой PR `<author-branch> -> main`. После merge ветку не удаляй.

Оригинальные книги не хранить в публичном repo. Если нужен постоянный source access, используйте приватный source repo; в public repo сохраняются производные rules, locators, provenance, tests и audits.

## Reviewer profiles and avatars

Reviewer profile — представление формализованной системы источника. Даже если UI показывает имя/аватар автора, текст должен ясно означать «по системе автора», а не реальную рецензию, цитату или endorsement.

Портреты добавлять только с понятной лицензией/источником; metadata хранить в reviewer profile.

## Mechanical tests

Перед PR:

```bash
python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/validate_libraries.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
python scripts/benchmark_board.py
```

Плюс source-specific validators/self-tests, если они есть.

Не удаляй natural negative tests ради нового rule. Если механика врёт без контекста — оставь правило soft/model-only.

## Source integration

Сначала study audit по `docs/book-study-framework.md`, затем Integration Matrix и Mechanical Feasibility, и только после этого runtime implementation.

`EDITING` идёт после `NATIVE_USAGE`. Книжная рекомендация не становится `NORM` без отдельной современной нормативной проверки.

Не откатывай wholesale core-файлы (`AGENTS.md`, `SKILL.md`, `BOARD_SKILL.md`, `scripts/check.py`, board/library runtime, benchmarks, CI, README).

## PR description

Укажи:

- provenance/source status;
- operational rules;
- automation levels;
- positive/negative/boundary tests;
- `phenomenon_id` overlaps;
- reviewer conflicts;
- compatibility with `NATIVE_USAGE`;
- compact behavior;
- board behavior;
- false-positive risks;
- model-only residue;
- runtime-context impact.
