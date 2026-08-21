# Настройка Custom GPT

## Название

`humanizer_russian · Русский редактор`

## Описание

Русский редактор с mechanical-first проверкой: сначала дешёвые детерминированные surface checks, затем при необходимости контекстный слой нормы, живой речи и идиолекта автора.

## Instructions

Скопируй `gpt/INSTRUCTIONS.md` в поле Instructions.

## Runtime: больше не собирать вручную из трёх файлов

Старый вариант `SKILL.md + scripts/check.py + scripts/lint.py` больше не является рабочей runtime-установкой. Текущий `check.py` использует normalized knowledge libraries и зависит от manifests, reviewers, source-specific linters и общих runtime-модулей.

Для Skills-compatible среды собирай поддерживаемый пакет:

```bash
python3 scripts/package_skill.py --output dist/humanizer-russian.zip
```

Проверка пакета без установки:

```bash
python3 scripts/install_skill.py \
  dist/humanizer-russian.zip \
  --dest-root /tmp/unused \
  --inspect
```

Полный порядок описан в `INSTALL.md`. CI устанавливает этот ZIP в чистый каталог и запускает Compact/Editorial Board уже из установленной копии.

Если конкретная поверхность Custom GPT не поддерживает переносимый Agent Skill как каталог с исполняемыми ресурсами, используй `gpt/INSTRUCTIONS.md` только как instruction layer. Не заявляй, что mechanical runtime выполнен, если код фактически не запускался.

## Source pack: подключать по задаче

Дополнительные reference-файлы для ручного/Knowledge-контекста нужны не всегда:

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

Незавершённые evidence providers имеют статус `PROJECT` и не могут быть включены. Не выдавай наличие manifest за рабочую интеграцию.

## Подсказки для начала разговора

1. `Отредактируй текст. Сначала прогони mechanical check, потом правь только найденное и очевидные контекстные проблемы.`
2. `Проведи глубокий аудит: mechanical + extended, но не считай warnings ошибками автоматически.`
3. `Сделай по-русски естественно, не разворачивай контекст в полные учебниковые предложения.`
4. `Подстрой текст под profile.json, но не копируй ошибки автора.`

## Перед публикацией конфигурации

Прогони:

- `python3 scripts/benchmark_lint.py`;
- `python3 scripts/lint.py --self-test`;
- `python3 scripts/benchmark_documents.py`;
- clean-install workflow из `.github/workflows/skill-package.yml`;
- `gpt/TESTS.md`;
- model-evals отдельно от mechanical tests;
- `profile_author.py` на небольшом корпусе с schema-validation.

## Автоматические блокеры результата

Не публикуй результат редактуры, если:

- изменён факт, причинность или степень уверенности;
- создана реальная языковая ошибка;
- остался надёжный технический `ARTIFACT`;
- модель заявляет о проверке, которой не было.

`NATIVE_WARNING`, `AI_PATTERN`, `STYLE_WARNING`, `AUTHOR_MISMATCH` — не автоматические ошибки.

## Обновление

После изменения mechanical rule сначала добавь positive/negative regression cases, затем меняй runtime-поведение. Reference-файл без теста не должен сам по себе превращаться в обязательное правило.
