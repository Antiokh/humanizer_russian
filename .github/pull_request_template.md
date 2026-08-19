## Что меняется

<!-- Кратко: что добавляется/исправляется и зачем. -->

## Provenance / класс

<!-- Отметь применимое. Source namespace (GAL/ILY/CHUK/...) — provenance, а не severity. -->

- [ ] `NORM-*`
- [ ] `NATIVE-*`
- [ ] `EDIT-*`
- [ ] `AI-CALQUE-*`
- [ ] `AUTHOR-*`
- [ ] `ARTIFACT-*`
- [ ] source-specific: `GAL-*` / `ILY-*` / `CHUK-*` / другое

Источник / provenance:

## Automation level

- [ ] `HARD_GATE` — обоснована высокая точность и блокирующий характер
- [ ] `DEFAULT_MECHANICAL` — high-precision deterministic check
- [ ] `EXTENDED_SOFT` — неблокирующая эвристика
- [ ] `MODEL_ONLY` — требует смысла/контекста/голоса
- [ ] `METRIC_ONLY` — описательная метрика

Что сознательно **не** автоматизировано:

## Mechanical tests

Для нового mechanical rule:

- [ ] true positive
- [ ] natural negative control
- [ ] boundary case
- [ ] intentional-use counterexample (если применимо)
- [ ] exclusions для code/URL/quotes/markdown/dialogue (если нужны)
- [ ] regression case добавлен в `tests/lint_cases.json`
- [ ] `python scripts/benchmark_lint.py` проходит

Если менялось ожидание существующего negative test, объясни почему исходный test был неверен:

## Совместимость с архитектурой

- [ ] прочитан `AGENTS.md`
- [ ] текущий `main` использован как архитектурная база
- [ ] `USER_INTENT + SEMANTICS + NORM` сохранены как hard constraints
- [ ] `AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score` не нарушено
- [ ] source/book recommendations не превращены в `NORM` без отдельной верификации
- [ ] `NATIVE_USAGE` не перезаписан редакторской школой
- [ ] default runtime остаётся mechanical-first
- [ ] reference/knowledge files не добавлены как обязательный runtime context без необходимости
- [ ] core-файлы не заменены wholesale старой версией из source-ветки

## Проверка

- [ ] `python -m compileall -q scripts`
- [ ] `python scripts/lint.py --self-test`
- [ ] `python scripts/benchmark_lint.py`
- [ ] profiler/schema validation (если менялись)
- [ ] source-specific validator (если добавлен/изменён)
- [ ] JSON fixtures валидны

## False positives / риски

<!-- Где правило может ошибаться? Почему выбран именно этот automation level? -->

## Model/context evals

<!-- Только если правило действительно контекстное. Укажи preservation/counterexample cases. -->
