# Настройка Custom GPT

## Название

`humanizer_russian · Русский редактор`

## Описание

Русский редактор с mechanical-first проверкой: сначала дешёвые детерминированные surface checks, затем при необходимости контекстный слой нормы, живой речи и идиолекта автора.

## Instructions

Скопируй `gpt/INSTRUCTIONS.md` в поле Instructions.

## Runtime-файлы: минимальный набор

Для обычной работы не нужно превращать Knowledge в свалку всех reference-файлов.

Минимум:

1. `SKILL.md`;
2. `scripts/check.py`;
3. `scripts/lint.py`.

Если доступен Code Interpreter, `scripts/check.py` — первый runtime-pass.

## Source pack: подключать по задаче

Дополнительные файлы нужны не всегда:

- `references/russian-language.md` — когда спорим о норме;
- `references/native-russian.md` — когда нужен глубокий разбор естественности;
- `references/nora-gal.md` — семантическая/литературная редактура;
- `references/rule-audit.md` и `references/evidence-audit.md` — аудит правил;
- `references/author-profile.md` — персонализация;
- `knowledge/corrections.md` — работа над регрессиями.

`references/native-russian-user-context.md` — исходный материал для разработки правил. Его не нужно тащить в каждый runtime-сеанс.

Не загружай `evals/*.json` как Knowledge: это тесты.

## Проверка проекта

Deterministic regression test:

```bash
python3 scripts/benchmark_lint.py
```

Корпус: `tests/lint_cases.json`.

Он не использует модель, web или reference-файлы.

Полный surface linter можно проверить отдельно:

```bash
python3 scripts/lint.py --self-test
```

Author profiler:

```bash
python3 scripts/profile_author.py corpus/ -o profile.json
```

Профиль валидируется по `profiles/schema.json`.

## Возможности

Для mechanical runtime нужен инструмент исполнения кода. Web Search включай только если сама задача редактуры требует проверки текущих или спорных фактов.

## Подсказки для начала разговора

1. `Отредактируй текст. Сначала прогони mechanical check, потом правь только найденное и очевидные контекстные проблемы.`
2. `Проведи глубокий аудит: mechanical + extended, но не считай warnings ошибками автоматически.`
3. `Сделай по-русски естественно, не разворачивай контекст в полные учебниковые предложения.`
4. `Подстрой текст под profile.json, но не копируй ошибки автора.`

## Перед публикацией конфигурации

Прогони:

- `python3 scripts/benchmark_lint.py`;
- `python3 scripts/lint.py --self-test`;
- `gpt/TESTS.md`;
- `evals/russian-language.json` и `evals/nora-gal.json` как отдельные model-evals, а не замену mechanical tests;
- `profile_author.py` на небольшом корпусе с schema-validation.

## Автоматические блокеры результата

Не публикуй результат редактуры, если:

- изменён факт, причинность или степень уверенности;
- создана реальная языковая ошибка;
- остался надёжный технический `ARTIFACT`;
- модель заявляет о проверке, которой не было.

`NATIVE_WARNING`, `AI_PATTERN`, `STYLE_WARNING`, `AUTHOR_MISMATCH` — не автоматические ошибки.

## Обновление

После изменения mechanical rule сначала добавь positive/negative regression cases в `tests/lint_cases.json`, затем меняй runtime-поведение. Reference-файл без теста не должен сам по себе превращаться в обязательное правило.
