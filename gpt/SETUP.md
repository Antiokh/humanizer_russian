# Настройка Custom GPT

## Название

`humanizer_russian · Русский редактор`

## Описание

Русский редактор с mechanical-first проверкой: сначала детерминированные проверки, затем при необходимости контекстный слой нормы, живой речи, редакторских школ и идиолекта автора.

## Полная GPT-сборка

Собирай Custom GPT не вручную и не из отдельных `check.py`/`lint.py`, а одной командой:

```bash
python3 scripts/package_gpt_runtime.py --output dist/humanizer-russian-gpts.zip
```

Архив содержит:

- `Instructions/` — текст для настройки GPT Builder;
- `Knowledge/` — тематически собранные reference-файлы;
- `Runtime/humanizer_runtime.py` — самодостаточный mechanical runtime для Code Interpreter.

`humanizer_runtime.py` автоматически встраивает тот же portable Agent Skill payload, который строится по `skill-package.json`. Поэтому GPT получает полный поддерживаемый набор текущих `check`, `review`, `lint`, `lint-*`, Editorial Board, author-profile runtime и нужные библиотеки/данные без ручной синхронизации Python-файлов.

## Что загружать в GPT Builder

1. Содержимое `Instructions/INSTRUCTIONS.md` вставь в поле **Instructions**.
2. Все `.md` из `Knowledge/` загрузи в **Knowledge**.
3. `Runtime/humanizer_runtime.py` тоже загрузи в GPT.
4. Обязательно включи **Code Interpreter & Data Analysis**.
5. Web Search включай только для задач, где действительно нужны текущие факты или внешняя проверка спорной/изменившейся нормы.
6. Conversation starters бери из `Instructions/CONVERSATION_STARTERS.md`.

Текущая сборка занимает 15 Knowledge-файлов + 1 runtime-файл = 16 загрузок из лимита 20.

## Mechanical workflow внутри GPT

Обычный проход:

```bash
python3 humanizer_runtime.py check --json text.md
```

Глубокий проход:

```bash
python3 humanizer_runtime.py check --extended --json text.md
```

Проверка целостности runtime:

```bash
python3 humanizer_runtime.py verify
```

Список доступных entrypoints:

```bash
python3 humanizer_runtime.py list
```

Коды возврата `1`/`2` у `check` могут означать найденные проблемы, а не падение программы. Сначала смотри JSON stdout.

GPT имеет право говорить, что mechanical check был выполнен, только если Code Interpreter реально запустил `humanizer_runtime.py`. Если runtime недоступен, это нужно сказать явно и продолжить только модельную редактуру.

## Что входит в runtime

Точный состав задаёт `skill-package.json`. Сейчас туда входят, в частности:

- `scripts/check.py`;
- `scripts/review.py`;
- `scripts/lint.py`;
- native/russian/calque/RKI linters;
- Chukovsky, Ilyakhov, Gal, Visson, Rosenthal, Golub linters;
- Editorial Board;
- author profile runtime;
- normalized libraries, reviewers, styles, references, schemas и evidence runtime data.

Evidence providers со статусом `PROJECT` от наличия runtime-кода не становятся operational.

## Knowledge

В GPT-сборке исходные reference-файлы и normalized libraries собраны в тематические бандлы. Не нужно вручную выбирать десятки файлов из `references/` и `libraries/`.

`references/native-russian-user-context.md` не попадает в GPT Knowledge: это материал разработки правил, а не обычный runtime-reference.

`evals/`, `tests/`, `studies/` и CI-файлы в GPT Knowledge не загружаются.

## Agent Skill — отдельная сборка

Для Skills-compatible среды остаётся отдельный пакет:

```bash
python3 scripts/package_skill.py --output dist/humanizer-russian.zip
```

GPT ZIP и Agent Skill ZIP — разные дистрибутивы, но executable runtime внутри GPT генерируется из того же Agent Skill allowlist.

## Проверка перед публикацией GPT

CI `.github/workflows/gpt-package.yml` должен:

- дважды собрать GPT ZIP и сравнить архивы побайтно;
- проверить общий лимит загружаемых GPT-файлов;
- запустить `humanizer_runtime.py verify`;
- проверить наличие всех основных linter entrypoints;
- сравнить JSON и exit code packaged `check` с прямым `scripts/check.py` в mechanical и extended режимах;
- загрузить в artifact именно проверенный ZIP.

После этого прогони `gpt/TESTS.md` в GPT Preview.

## Автоматические блокеры результата

Не публикуй результат редактуры, если:

- изменён факт, причинность или степень уверенности;
- создана реальная языковая ошибка;
- остался надёжный технический `ARTIFACT`;
- модель заявляет о проверке, которой не было.

`NATIVE_WARNING`, `AI_PATTERN`, `STYLE_WARNING`, `AUTHOR_MISMATCH` — не автоматические ошибки.
