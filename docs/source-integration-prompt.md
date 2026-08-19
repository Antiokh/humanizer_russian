# Reusable prompt: integrate a source branch into humanizer_russian

Используй этот prompt для Codex/агента, который интегрирует уже существующую source-ветку или книжный слой в основной `humanizer_russian`.

Заменить placeholders `<SOURCE_NAME>`, `<SOURCE_BRANCH>` и `<SOURCE_PR>`.

```text
Работаем в репозитории Antiokh/humanizer_russian.

Источник/слой: <SOURCE_NAME>
Source branch: <SOURCE_BRANCH>
Source PR: <SOURCE_PR>

ЦЕЛЬ

Аккуратно интегрировать знания из source branch в текущий main проекта humanizer_russian.

НЕ начинай с merge/rebase старой ветки и НЕ переноси её core-файлы wholesale.

Сначала прочитай и соблюдай:
1. AGENTS.md
2. docs/book-study-framework.md
3. docs/source-integration-runbook.md

Если source study ещё не соответствует framework, сначала завершай study. Для этого используй docs/book-study-prompt.md.

РАБОТА ИДЁТ В ДВА GATE.

====================
GATE A — STUDY AUDIT
====================

На этом этапе НЕ меняй runtime/core-файлы.

1. Проверь source branch/PR как book/source study по docs/book-study-framework.md.
2. Убедись, что источник реально разобран последовательно, а не по snippets.
3. Проверь coverage, provenance, locators, concepts, atomic rules, positive operations, guards, counterexamples, interactions, claims, evals, loss audit и overgeneralization audit.
4. Если есть gaps — сначала закрой их.
5. Старый код/regex/hard bans из source branch считай только кандидатами, а не доказательством правильной автоматизации.
6. Для normative/historical/usage claims не считай саму книгу достаточной современной нормативной опорой.

Не переходи к интеграции, пока study не достиг минимум AUDITED; предпочтительно OPERATIONAL.

После study audit создай INTEGRATION MATRIX для всех operational rules/operations.

Для каждого элемента укажи:
- rule_id
- source_locator
- provenance
- project_class: NORM | NATIVE_USAGE | EDITING | AI_CALQUE | AUTHOR | ARTIFACT
- scope
- semantic invariant
- automation_level: HARD_GATE | DEFAULT_MECHANICAL | EXTENDED_SOFT | MODEL_ONLY | METRIC_ONLY
- surface_trigger
- required_context
- false_positive_risk
- positive_case
- natural_negative_control
- boundary_case
- intentional_counterexample
- overlap_with_existing_rules
- possible_conflict_with_NATIVE_USAGE
- implementation_plan
- planned_module
- runtime_visibility

После матрицы сделай отдельный MECHANICAL FEASIBILITY REPORT:
- какие правила можно проверить без LLM;
- каким нужен regex;
- каким нужен morphology/dependency/statistical parser;
- какие можно считать только метриками;
- какие честно остаются model-only;
- какие старые mechanical implementations слишком широкие и должны быть понижены.

СТОП-УСЛОВИЕ:
до завершения Integration Matrix + Mechanical Feasibility Report не переписывай SKILL.md, scripts/lint.py, scripts/check.py и GPT runtime instructions.

============================
GATE B — IMPLEMENTATION
============================

После завершения Gate A:

1. Создай fresh integration branch ОТ ТЕКУЩЕГО main, например integration/<source>.
2. Текущий main — архитектурная база. Source branch — база знаний/provenance.
3. Переноси source-specific файлы и знания поверх main. Не откатывай core-файлы к старой версии ветки.

ПОРЯДОК РЕАЛИЗАЦИИ ОБЯЗАТЕЛЕН:

A. MECHANICAL FIRST

Сначала реализуй всё, что можно надёжно проверить кодом.

Приоритет:
1. HARD_GATE — только реально однозначные блокирующие случаи.
2. DEFAULT_MECHANICAL — high precision surface rules.
3. EXTENDED_SOFT — полезные, но более шумные механические эвристики.
4. METRIC_ONLY — измеряем, но не называем ошибкой без калибровки.
5. MODEL_ONLY — остаток после механизации.

Для каждого mechanical rule добавь:
- true positive;
- natural negative control;
- boundary case;
- intentional-use counterexample, если применимо;
- exclusions для code/URL/quotes/dialogue/markdown, если нужны;
- regression case в tests/lint_cases.json или source-specific deterministic suite.

Нельзя продвигать правило в DEFAULT_MECHANICAL только потому, что его легко написать regex-ом.
Precision важнее recall.

Если natural negative control ломается — сначала сузь правило. Не удаляй отрицательный тест ради зелёного CI.

Для крупного источника предпочитай source-specific module, например:
- scripts/lint_<source>.py
- scripts/<source>_checks.py

Главный scripts/lint.py агрегирует результаты.
scripts/check.py решает, что разрешено показывать в default mechanical runtime.

B. TEST MECHANICS BEFORE PROMPT

До расширения SKILL/prompt обязательно запусти:

python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py

Запусти source-specific validator/self-test, если он добавлен.

Сначала почини deterministic suite. Только потом переходи к contextual integration.

C. MODEL-ONLY RESIDUE

После mechanical pass посмотри, что осталось.

Model-only должны оставаться правила, требующие:
- семантики;
- референтов;
- темы/ремы;
- жанра;
- идиом;
- POV;
- характера;
- эмоционального такта;
- длинного контекста;
- авторского намерения.

Для них:
- делай короткие operational references;
- не загружай полный study в обычный runtime;
- добавь preservation/no-op evals;
- не дублируй в prompt то, что уже делает механический checker.

D. RUSSIAN CORE COMPATIBILITY

Для каждого source rule отдельно проверь совместимость с уже принятым NATIVE_USAGE:
- контекстная экономия;
- безопасный эллипсис;
- отсутствие немотивированных повторов;
- сначала опущение/вынос/перестройка, потом синоним;
- свободный русский порядок слов и информационная структура;
- функциональная парцелляция;
- прагматические частицы;
- нормальная русская пунктуация;
- author profile.

Если EDITING source конфликтует с NATIVE_USAGE, сначала сузь scope source rule. Не делай книжный стиль новым универсальным русским.

E. FINAL INTEGRATION

Только после mechanical + model-only разделения:
- обнови SKILL.md;
- обнови GPT instructions/setup/tests, если это действительно нужно;
- добавь source-specific references;
- добавь structural validator в CI, если нужен;
- сохрани selective context loading.

В финальном отчёте и PR явно перечисли:
1. Study status.
2. Сколько source rules/operations рассмотрено.
3. Сколько стало HARD_GATE.
4. Сколько DEFAULT_MECHANICAL.
5. Сколько EXTENDED_SOFT.
6. Сколько METRIC_ONLY.
7. Сколько MODEL_ONLY.
8. Какие старые source rules были понижены/отброшены и почему.
9. Какие negative controls добавлены.
10. Какие false-positive risks остаются.
11. Что сознательно не автоматизировано.
12. Не вырос ли обязательный runtime context.
13. Какие source-specific files добавлены.
14. Все ли базовые CI gates сохранены.

НЕ ДЕЛАЙ:
- wholesale merge старого source branch;
- hard ban из книжной рекомендации;
- detector-driven оптимизацию;
- удаление native Russian rules ради source style;
- огромный prompt вместо механической проверки;
- псевдолингвистический regex для model-only задачи;
- автоматическое превращение source namespace в severity.

Ключевая формула:
SOURCE → STUDY FRAMEWORK → AUDITED KNOWLEDGE → INTEGRATION MATRIX → MECHANICAL FEASIBILITY → MECHANICAL IMPLEMENTATION → MODEL-ONLY RESIDUE → SKILL/REFERENCES → CI/EVALS → MERGE.
```
