# Source Integration Runbook

Этот runbook описывает, как интегрировать в `humanizer_russian` отдельную исследовательскую/source-ветку: Галь, Ильяхова, Чуковского или любой следующий источник.

Цель: сначала доказать, что источник разобран корректно и полно, затем встроить его в текущую архитектуру `main`, отдавая приоритет воспроизводимым механическим проверкам с хорошими отрицательными контролями.

## Главный принцип

Нельзя начинать интеграцию с merge старой source-ветки в `main`.

Работа идёт через два независимых gate:

1. **STUDY GATE** — источник сначала проходит `docs/book-study-framework.md`.
2. **INTEGRATION GATE** — только после этого его знания переносятся поверх текущего `main` по mechanical-first архитектуре из `AGENTS.md`.

Source branch — источник знаний и provenance. `main` — источник архитектуры.

---

## Phase 0. Старт

Перед любыми изменениями:

1. прочитать `AGENTS.md`;
2. прочитать `docs/book-study-framework.md`;
3. если study ещё не завершён — использовать `docs/book-study-prompt.md`;
4. определить source branch/PR и его source-specific файлы;
5. не менять core runtime до завершения STUDY GATE.

Для старых веток, созданных до текущего `main`, не использовать их `SKILL.md`, `README.md`, `scripts/lint.py`, CI и другие core-файлы как архитектурную базу.

---

# Gate A — STUDY GATE

## A1. Проверить полноту source study

Источник должен пройти framework как самостоятельная система знаний.

Минимально проверить:

- есть source inventory;
- есть полная карта покрытия/оглавления;
- источник прочитан последовательно, а не по snippets;
- нет скрытых `UNREAD` при заявленной полноте;
- выделены concepts, rules, positive operations, guards, counterexamples;
- описаны interactions;
- source claims отделены от project-derived выводов;
- исторические/нормативные/эмпирические claims вынесены на внешнюю проверку;
- есть evals и preservation/counterexample cases;
- проведены loss audit и overgeneralization audit;
- provenance восстанавливается до source locator;
- публичные файлы не копируют защищённый текст источника.

Статус study перед интеграцией должен быть минимум `AUDITED`; для завершённой интеграции предпочтительно `OPERATIONAL`.

Если этих артефактов нет, **не переходить к runtime integration**. Сначала закончить study.

## A2. Не принимать старую реализацию как доказательство

Если source-ветка уже содержит regex, linter, hard bans или старый `SKILL.md`, они считаются только кандидатами.

Нужно заново спросить для каждой идеи:

- что именно утверждает источник;
- каков scope;
- это норма, native usage, editing advice, AI heuristic или author behavior;
- есть ли отрицательный пример;
- можно ли это надёжно определить поверхностно;
- что будет false positive.

Наличие кода в старой ветке не повышает automation level автоматически.

---

# Gate B — INTEGRATION GATE

После прохождения STUDY GATE создать **новую integration branch от текущего `main`**.

Рекомендуемое имя:

```text
integration/<source>
```

Примеры:

```text
integration/nora-gal
integration/ilyakhov
integration/chukovsky
```

Не использовать source branch как новую базу runtime.

## B1. Сначала построить Integration Matrix

До изменения `scripts/lint.py` или `SKILL.md` составить таблицу для **каждого operational rule/operation** источника.

Минимальные поля:

```text
rule_id
source_locator
project_class
scope
automation_level
surface_trigger
required_context
false_positive_risk
positive_case
negative_control
boundary_case
existing_overlap
native_usage_conflict
planned_module
runtime_visibility
```

Где:

### `project_class`

Одно из:

- `NORM`
- `NATIVE_USAGE`
- `EDITING`
- `AI_CALQUE`
- `AUTHOR`
- `ARTIFACT`

Source namespace (`GAL-*`, `ILY-*`, `CHUK-*`) хранит provenance, но не заменяет project class.

### `automation_level`

Одно из:

- `HARD_GATE`
- `DEFAULT_MECHANICAL`
- `EXTENDED_SOFT`
- `MODEL_ONLY`
- `METRIC_ONLY`

## B2. Mechanical feasibility pass — сделать ДО prompt integration

Для каждого rule сначала попытаться найти дешёвый наблюдаемый сигнал.

Порядок вопросов:

1. Есть ли surface trigger, который можно определить без semantic model?
2. Можно ли отделить true positive от естественного negative control?
3. Можно ли исключить code/URL/quote/dialogue/markdown и другие очевидные ложные зоны?
4. Требуется ли морфология/dependency parser вместо regex?
5. Можно ли сделать статистическую/структурную проверку без утверждения «это ошибка»?
6. Если механическая проверка возможна, какой минимальный уровень автоматизации ей честно соответствует?

Цель этого pass — **не автоматизировать максимум**, а вынести максимум надёжной работы из prompt/runtime контекста.

Если правило требует понимания смысла, референтов, жанра, темы/ремы, идиомы, POV, характера, эмоционального такта или авторского намерения — оставить `MODEL_ONLY`.

Не писать псевдолингвистический regex только ради механизации.

## B3. Приоритет реализации

Реализовывать в следующем порядке:

### 1. HARD_GATE

Только если правило действительно однозначно и блокирующее.

### 2. DEFAULT_MECHANICAL

Высокая precision, дешёвая проверка, доказанные negative controls.

Каждое новое default rule требует:

- true positive;
- natural negative control;
- boundary case;
- intentional-use counterexample, если применимо;
- regression case в `tests/lint_cases.json`;
- зелёный `scripts/benchmark_lint.py`.

### 3. EXTENDED_SOFT

Полезная механическая эвристика, но с заметным false-positive risk.

Она может жить в source-specific linter и попадать только в `--extended`.

### 4. METRIC_ONLY

Считать, но не оценивать без калибровки.

### 5. MODEL_ONLY

Только после того, как mechanical layer забрал всё, что можно проверить без модели.

Именно на этом этапе добавлять адресные reference instructions/model evals.

---

## B4. Source-specific modules

Для крупного источника предпочитать отдельный модуль:

```text
scripts/lint_gal.py
scripts/lint_ilyakhov.py
scripts/chukovsky_checks.py
```

или другое ясное source-specific имя.

Главный `scripts/lint.py` агрегирует findings, но не превращается в свалку всех regex проекта.

Source-specific findings по умолчанию неблокирующие, пока отдельно не доказан `HARD_GATE`.

`scripts/check.py` остаётся контроллером default mechanical runtime. Новое правило не попадает туда автоматически только потому, что оно реализовано в коде.

---

## B5. Контекст только после механики

После mechanical feasibility/implementation pass посмотреть, что осталось.

Для остатка:

- сократить source knowledge до operational reference;
- не загружать book study целиком в обычный runtime;
- model-only instructions делать адресными;
- evals проверяют не только исправление, но и preservation/no-op;
- source map/provenance используется при аудите, а не на каждую пользовательскую фразу.

Цель: model layer получает только unresolved semantic cases, а не повторно делает работу линтера.

---

## B6. Проверка конфликтов с core Russian layer

Каждый source rule проверить против:

- `NORM`;
- `NATIVE_USAGE`;
- контекстной экономии;
- правил удаления немотивированных повторов;
- информационной структуры;
- функциональной парцелляции;
- прагматических частиц;
- author profile.

Если книжная рекомендация конфликтует с живым русским, сначала сузить её scope. Не понижать `NATIVE_USAGE` до уровня книжной рекомендации.

---

## B7. Интеграционные тесты

До изменения большого prompt/skill слоя должны быть готовы mechanical tests.

Обязательные команды:

```bash
python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
```

Если добавлен source validator — он также включается в CI.

Если source-specific linter имеет self-test — он запускается отдельно.

Model evals идут **после** mechanical regression suite и не заменяют его.

---

# Recommended agent workflow

## Step 1 — Audit only

Первый агент/первый этап не должен сразу редактировать runtime.

Его задача:

1. пройти source branch по `book-study-framework`;
2. закрыть gaps;
3. получить `AUDITED/OPERATIONAL` study;
4. построить Integration Matrix;
5. выдать mechanical feasibility report;
6. перечислить, какие правила кандидат в default/extended/model-only;
7. не менять core runtime до завершения отчёта.

## Step 2 — Mechanical implementation

После approval/самопроверки матрицы:

1. создать fresh branch от `main`;
2. перенести source-specific knowledge/provenance;
3. сначала реализовать mechanical candidates;
4. добавить deterministic tests и negative controls;
5. измерить ложные срабатывания;
6. только надёжные правила добавить в default checker;
7. остальные оставить extended/model-only.

## Step 3 — Contextual integration

Только затем:

1. добавить model-only instructions;
2. сократить runtime context;
3. добавить semantic/model evals;
4. интегрировать source layer в `SKILL.md` и GPT-инструкции;
5. проверить, что prompt не дублирует mechanical checker.

## Step 4 — Final integration audit

Перед merge ответить:

- что из source study реально вошло в runtime;
- что механизировано;
- что осталось extended;
- что осталось model-only;
- какие правила сознательно не автоматизированы;
- какие negative controls защищают native Russian;
- где есть unresolved claims;
- не вырос ли обязательный runtime context без необходимости;
- не удалены ли базовые mechanical tests/CI gates.

---

# Что запрещено при интеграции

- merge старого source branch поверх `main` с wholesale conflict resolution;
- считать book rule нормой без отдельной normative verification;
- делать hard ban из surface pattern без negative controls;
- удалять существующие clean tests ради нового rule;
- загружать весь book study в prompt обычного runtime;
- объявлять JSON model evals «пройденными», если модель не запускалась;
- дублировать в prompt то, что уже надёжно делает механический checker;
- оптимизироваться под detector score;
- заменять естественный русский «более книжным» только ради соответствия автору источника.

---

# Короткая формула

```text
SOURCE
  ↓
BOOK STUDY FRAMEWORK
  ↓
AUDITED / OPERATIONAL KNOWLEDGE
  ↓
INTEGRATION MATRIX
  ↓
MECHANICAL FEASIBILITY PASS
  ↓
DEFAULT MECHANICAL / EXTENDED / METRIC
  ↓
MODEL-ONLY RESIDUE
  ↓
SKILL + SOURCE REFERENCES
  ↓
DETERMINISTIC CI + MODEL EVALS
  ↓
MERGE
```

Главный критерий: после интеграции источник должен усиливать общий движок, а не добавлять ещё один автономный prompt-слой.