# Технический обзор humanizer_russian

Этот файл хранит детали, которые нужны разработчику или агенту, но мешают README быть понятным с первого экрана.

## Один движок, два режима

`humanizer_russian` не поддерживает две независимые реализации.

- Compact: `scripts/check.py`.
- Editorial Board: `scripts/review.py`.

Оба режима используют один набор knowledge libraries. Правило не должно иметь отдельную реализацию для compact и board.

## Базовая иерархия

Жёсткие ограничения:

`USER_INTENT + SEMANTICS + NORM`

Выбор среди допустимых вариантов:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Редакторская школа не отменяет норму, живой русский или подтверждённый авторский голос.

## Mechanical-first

Сначала выполняется дешёвая воспроизводимая проверка. Контекстная модель подключается только к остаточным случаям, где surface analysis недостаточен.

Уровни автоматизации:

- `HARD_GATE` — только действительно надёжное блокирующее нарушение;
- `DEFAULT_MECHANICAL` — high-precision проверка обычного compact runtime;
- `EXTENDED_SOFT` — полезная, но более шумная механическая эвристика;
- `METRIC_ONLY` — измерение без автоматического вывода;
- `MODEL_ONLY` — семантика, дискурс, жанр, идиома, POV, голос и другие контекстные задачи.

Для нового default mechanical rule обязательны positive case, natural negative control, boundary case и deterministic regression test.

## Knowledge libraries

Каждый источник подключается через отдельную библиотеку:

```text
libraries/<id>/library.json
reviewers/<reviewer_id>.json
scripts/lint_<source>.py
```

Manifest хранит идентичность библиотеки, namespace источника, reviewer, adapter и linter path. Большой study книги в manifest не копируется.

Для новых библиотек предпочтителен adapter `review_v1`. Старый core linter подключён через compatibility adapter.

## Нормализованный finding

Source-specific правило сохраняет собственный `rule_id`, например `GAL-KANZ-VERB`. Одновременно finding получает source-neutral `phenomenon_id`, например `editing.action_hidden_in_nominalization`.

Это позволяет двум книгам описывать одно явление независимо друг от друга.

Нормализованный finding содержит как минимум:

```text
rule_id
phenomenon_id
library_id
source_namespace
reviewer_id
project_class
automation_level
verdict
line / excerpt
reason
operation
confidence
```

## Compact

Обычный запуск:

```bash
python3 scripts/check.py text.md
python3 scripts/check.py --json text.md
```

По умолчанию выводятся только `HARD_GATE` и `DEFAULT_MECHANICAL`. Мягкие механические эвристики доступны через:

```bash
python3 scripts/check.py --extended text.md
```

Compact не должен симулировать редколлегию или загружать полный source study.

## Editorial Board

Запуск:

```bash
python3 scripts/review.py text.md --style neutral
python3 scripts/review.py text.md --style rslive_content --format json
```

`scripts/editorial_board.py` группирует findings по явлениям и сохраняет мнения reviewer'ов. Текущий контракт предусматривает, в частности:

- `CONSENSUS`;
- `MAJORITY`;
- `SOURCE_CONFLICT`;
- `SINGLE_REVIEW` / `REVIEW`;
- `NO_ACTION`.

Конфликт источников считается допустимым результатом. Style policy применяется после того, как отдельные verdict'ы сохранены.

Имена реальных авторов в UI означают «оценка по формализованной системе автора», а не настоящую цитату или личную рецензию.

## Styles

Редакционные политики лежат в `styles/`. Они не должны быть зашиты в source-specific linter.

Автор отвечает за собственную систему рекомендаций. Style profile отвечает за то, как конкретный проект разрешает несколько допустимых рекомендаций.

## Long-lived author branches

Исследование книги развивается в долгоживущей ветке по фамилии автора: `gal`, `ilyakhov`, `chukovsky` и т. п.

Перед очередным PR ветка подтягивает свежий `main`. При конфликтах архитектурным источником истины остаётся `main`, а author branch сохраняет source study, provenance, rules и evals.

После merge author branch не удаляется.

## Оригиналы книг

Публичный репозиторий не должен содержать полные защищённые тексты книг. Оригиналы можно хранить в отдельном приватном source repo или использовать из текущего контекста агента.

В публичный проект переносятся производные материалы: собственные формулировки правил, locators, source maps, tests, audits и provenance.

## Основные файлы

- `AGENTS.md` — обязательный архитектурный контракт;
- `SKILL.md` — compact runtime instructions;
- `BOARD_SKILL.md` — orchestration для Editorial Board;
- `libraries/` — knowledge libraries;
- `reviewers/` — reviewer metadata;
- `styles/` — editorial policies;
- `scripts/library_runtime.py` — загрузка и нормализация libraries;
- `scripts/check.py` — compact entrypoint;
- `scripts/review.py` — board entrypoint;
- `scripts/editorial_board.py` — aggregation/conflict layer;
- `references/` — source-backed contextual knowledge;
- `tests/` — deterministic corpora.

## Проверки

Минимальный набор перед merge:

```bash
python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/validate_libraries.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
python scripts/benchmark_board.py
```

CI также валидирует JSON schemas/fixtures и smoke-tests author profiler и board output.

Model evals нужны для `MODEL_ONLY` задач, но не заменяют deterministic benchmark для механических правил.

## Добавление источника

Полный процесс: [`source-integration-runbook.md`](source-integration-runbook.md).

Главная последовательность:

`SOURCE → STUDY → ATOMIC RULES → LIBRARY → MECHANICAL FEASIBILITY → NORMALIZED FINDINGS → COMPACT + BOARD → MODEL-ONLY RESIDUE → TESTS → MERGE`.
