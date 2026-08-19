# humanizer_russian

`humanizer_russian` — русский редактор и humanizer, который ставит естественный русский язык выше detector-driven трюков.

Проект не пытается сделать текст «менее грамотным, чтобы выглядел человеческим». Он сохраняет смысл и норму, механически ловит то, что можно проверить без модели, а контекстные правила подключает только там, где механика не даёт ответа.

## Приоритеты

Жёсткие ограничения:

`USER_INTENT + SEMANTICS + NORM`

Выбор среди допустимых вариантов:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

`NORM` отвечает на вопрос «можно ли так по-русски?». `NATIVE_USAGE` — «как из допустимых вариантов естественнее сказал бы носитель?». Это разные задачи.

## Два режима из одного движка

Проект развивает не две отдельные ветки продукта, а два entrypoint одного `main` и одного набора knowledge libraries.

### Compact humanizer

Для CI, быстрой проверки и проектов, которым не нужна редакционная коллегия:

```bash
python3 scripts/check.py text.md
python3 scripts/check.py --json text.md
```

Компактный режим схлопывает источник правил в короткий mechanical-first результат.

### Editorial board

Для глубокой редактуры с отдельными мнениями редакторских школ:

```bash
python3 scripts/review.py text.md --style neutral
python3 scripts/review.py text.md --style rslive_content --format json
```

Board сохраняет provenance каждого reviewer, группирует совпадающие явления через `phenomenon_id`, показывает `CONSENSUS`, `MAJORITY`, `SOURCE_CONFLICT` и применяет style policy. Имена авторов означают оценку по формализованной системе источника, а не реальную рецензию автора.

Подробнее: `BOARD_SKILL.md` и `docs/editorial-board-architecture.md`.

## Книги как библиотеки знаний

Каждый новый источник подключается через manifest:

```text
libraries/<author>/library.json
reviewers/<author>.json
scripts/lint_<author>.py
```

Исследование живёт в долгоживущей ветке по фамилии автора (`gal`, `ilyakhov`, `chukovsky`, ...). После merge такую ветку не удаляют: она периодически подтягивает свежий `main` и продолжает развивать rules/evals/provenance.

Разные авторы могут не соглашаться. Это не ошибка интеграции: source-specific `rule_id` сохраняется, а общий source-neutral `phenomenon_id` позволяет compact-режиму дедуплицировать сигнал и board-режиму показать конфликт.

Оригинальные охраняемые книги не должны храниться в публичном repo. Их можно держать в приватном source repo; в `humanizer_russian` попадают производные rules, locators, provenance, tests и audits.

См. `libraries/README.md` и `docs/source-integration-runbook.md`.

## Архитектурный контракт для разработки

Корневой [`AGENTS.md`](AGENTS.md) — обязательный контракт для coding/research agents и интеграции новых языковых слоёв. [`CONTRIBUTING.md`](CONTRIBUTING.md) содержит contributor protocol.

Ключевые требования:

- текущий `main` является архитектурной базой для интеграции Галь, Ильяхова, Чуковского и следующих источников;
- author branches не должны wholesale заменять `SKILL.md`, `BOARD_SKILL.md`, `scripts/check.py`, benchmark, CI или native layer;
- каждое новое правило получает явный уровень: `HARD_GATE`, `DEFAULT_MECHANICAL`, `EXTENDED_SOFT`, `MODEL_ONLY` или `METRIC_ONLY`;
- mechanical rule не попадает в default runtime без positive case, natural negative control и deterministic regression test;
- source namespace (`GAL-*`, `ILY-*`, `CHUK-*`) показывает provenance, а не автоматически severity;
- книжный совет остаётся `EDITING`, пока отдельно не доказано, что это современная `NORM`;
- reference/source-файлы не загружаются целиком в каждый runtime pass.

Для новых PR используется `.github/pull_request_template.md` с архитектурным checklist.

## Mechanical-first runtime

По умолчанию `check.py` показывает только сравнительно точные surface findings:

- технические артефакты;
- повтор общей части в противопоставлении;
- механически разорванное перечисление;
- ASCII-дефис на месте тире в прозе.

Контекстные AI/style эвристики не должны запускаться автоматически для каждого текста.

Если нужен глубокий compact-аудит:

```bash
python3 scripts/check.py --extended text.md
```

Extended mode добавляет SVO-lock proxies, context undercompression, possessive overexplication, Q/A-кластеры, повтор риторических формул, кальки и другие мягкие сигналы.

`scripts/lint.py` остаётся текущим core surface linter. Новые книги должны по возможности жить в source-specific modules и подключаться как libraries, а не раздувать один файл.

## Детерминированное тестирование

Основные regression tests не используют LLM-judge, web и полный набор reference-файлов:

```bash
python3 scripts/benchmark_lint.py
python3 scripts/benchmark_board.py
```

Корпуса: `tests/lint_cases.json` и `tests/editorial_board_cases.json`.

Новое mechanical rule должно иметь как минимум:

1. положительный пример;
2. естественный отрицательный контроль;
3. пограничный пример, если он нужен;
4. deterministic regression case.

Если проверку нельзя надёжно сделать механически, правило остаётся `EXTENDED_SOFT`, `METRIC_ONLY` или `MODEL_ONLY`.

## Ключевые идеи живого русского

### Контекстная экономия

Русский не требует автономной полноты каждого предложения:

> — Кого любит Паша? — Машу.

> Первый вариант дорогой. Второй — быстрее.

Если пропущенное однозначно восстанавливается из контекста, падежа, согласования или управления, его не нужно возвращать только ради полной структуры.

### Сначала убрать повтор, потом искать синоним

Синтетически:

> Это не ошибка в расчёте, а ошибка в исходных данных.

Нейтральнее:

> Это ошибка не в расчёте, а в исходных данных.

Синтетически:

> Мы не меняем цену, а меняем условия.

Нейтральнее:

> Мы меняем не цену, а условия.

Приоритет: опустить → вынести общий элемент → местоимение/нуль → перестроить → только потом точный синоним.

Намеренный повтор не удаляется автоматически:

> Никогда. Никогда больше.

### Порядок слов — не английский SVO

Падеж, согласование и управление кодируют значительную часть связей, поэтому порядок слов может работать на тему, рему, контраст и удар:

> Паша любит Машу.
>
> Машу любит Паша.
>
> Паша Машу любит.

Сильными могут быть оба края фразы: начало — ответ/возражение/рамка, конец — новое/итог.

### Противопоставление не запрещено

`не X, а Y`, `не только X, но и Y`, `X, но Y` — нормальные русские конструкции.

Проверяется не форма сама по себе, а:

- есть ли лишний общий повтор;
- что реально противопоставляется;
- приносит ли вторая часть новую информацию или переоценку;
- куда должен падать смысловой удар.

### Парцелляция проверяется по функции

Нормально:

> Обещал приехать. Не приехал.

В нейтральном перечислении чаще лучше:

> С такими курсами обычно две беды: либо теория, либо пересказ.

а не механическая рубка на три предложения.

### Частицы и разговорность не мусор

`же`, `ведь`, `всё-таки`, `вот`, `ну`, `просто` могут нести прагматику. Их нельзя удалять только потому, что без них фраза остаётся грамматичной.

## Файлы проекта

- `AGENTS.md` — обязательный архитектурный контракт;
- `SKILL.md` — compact runtime-spec;
- `BOARD_SKILL.md` — editorial-board orchestration;
- `libraries/` — подключаемые knowledge libraries;
- `reviewers/` — UI/provenance profiles рецензентов;
- `styles/` — редакционные политики;
- `scripts/check.py` — compact mechanical-first вход;
- `scripts/review.py` — editorial-board вход;
- `scripts/library_runtime.py` — загрузка/нормализация libraries;
- `scripts/editorial_board.py` — aggregation/conflict layer;
- `scripts/benchmark_lint.py` — compact deterministic benchmark;
- `scripts/benchmark_board.py` — board deterministic benchmark;
- `references/russian-language.md` — нормативная база;
- `references/native-russian.md` — систематизированный слой живого русского;
- `references/native-russian-user-context.md` — исходные наблюдения носителя для разработки правил;
- `references/author-profile.md` — персонализация.

Reference-файлы — база для разработки и разбора спорных случаев, а не обязательный payload каждого runtime-pass.

## Авторский профайлер

```bash
python3 scripts/profile_author.py corpus/ -o profile.json
```

Профиль строится по корпусу и может описывать частицы, n-граммы, sentence/paragraph distributions, code-switching, пунктуацию, stance и ручные локальные/поколенческие/профессиональные annotations.

Ошибки автора хранятся отдельно от голоса и по умолчанию не имитируются.

## CI

CI проверяет:

- компиляцию Python;
- architecture contract;
- library/reviewer/style schemas;
- self-test core linter;
- deterministic compact benchmark;
- deterministic editorial-board benchmark;
- author profiler + JSON Schema;
- валидность JSON fixtures.

## Критерий качества

Хороший `humanizer_russian` не обязан переписывать текст. Если механическая проверка чистая и текст уже звучит естественно, лучший результат может быть «оставить как есть».
