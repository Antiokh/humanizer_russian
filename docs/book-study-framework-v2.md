# Book Study Framework v2

## Source → Public Operational Knowledge

Этот документ задаёт единый протокол для книг, из которых проект хочет забрать **идеи, различия, концепции, диагностические модели, положительные операции и формулы**, но не публиковать саму книгу, её последовательный пересказ или набор авторских примеров.

Framework вырос из практики трёх параллельных book studies в `humanizer_russian`:

- Нора Галь: source map → атомарные правила → scope/provenance → eval map;
- Ильяхов/Сарычева: диагностика отдельно от положительных редакторских операций;
- Чуковский: guardrails отдельно от рекомендаций, а surface-lint отдельно от model-level reconstruction.

Из этого следует главное архитектурное решение:

> **Книга не превращается в один список правил.**
>
> Она превращается в граф разных типов знания с доказуемым происхождением, а затем — в самостоятельный публичный слой проекта.

---

## 1. Цель

Нам нужен результат, который одновременно удовлетворяет четырём требованиям.

### 1.1. Содержательная полнота

Не потерять различия из книги, которые способны изменить:

- диагноз;
- решение;
- действие;
- порядок действий;
- область применимости;
- исключение;
- оценку успешности результата.

### 1.2. Операциональность

Публичная база должна отвечать не только:

> «Что автор критикует?»

но и:

> «Что именно проверить?»
>
> «Что попробовать сделать вместо этого?»
>
> «Как понять, что стало лучше?»
>
> «Когда это правило применять нельзя?»

### 1.3. Трассируемость

Для любого важного элемента должно быть возможно восстановить:

`public card → source locator → provenance → project integration`

без публикации исходного текста.

### 1.4. Несубститутивность

Публичный репозиторий не должен становиться альтернативным изданием книги.

Практический принцип соответствует базовому различию между идеей/методом и конкретной формой их выражения: мы извлекаем и заново формализуем идеи, процессы, системы и методы, но не копируем литературное выражение источника. Это инженерная publication policy проекта, а не универсальное юридическое заключение для всех юрисдикций.

---

## 2. Два пространства: SOURCE и PUBLIC

Самая важная граница framework.

## 2.1. SOURCE WORKSPACE — приватный или временный

Здесь может находиться всё, что необходимо исследователю для полного разбора:

- EPUB/PDF/DOCX;
- извлечённый текст;
- OCR;
- временные chapter notes;
- поиск по полному тексту;
- candidate sentence pool;
- временные цитаты для проверки;
- локальные скрипты разбора;
- подробные заметки по авторским примерам.

**По умолчанию это не коммитится в публичный репозиторий.**

SOURCE WORKSPACE существует для исследования и проверки provenance.

## 2.2. PUBLIC KNOWLEDGE LAYER — коммитимый

Сюда попадает только производное знание:

- библиографическая metadata;
- fingerprint исходного файла, если допустимо;
- sparse source map;
- concepts;
- distinctions;
- diagnostics;
- positive operations;
- project formulas;
- guardrails;
- claims requiring external verification;
- interactions;
- synthetic evals;
- integration map;
- audit.

В публичном schema **нет обязательного поля `quote`**.

Если точная цитата действительно нужна для анализа формулировки, это отдельное исключение, а не обычный способ хранения знания.

---

## 3. Почему одного типа `RULE` недостаточно

Параллельные book studies показали, что одно поле `rule` смешивает слишком разные вещи.

Canonical framework разделяет минимум восемь типов knowledge units.

### `CONCEPT`

Определение, категория, модель или единица анализа.

Пример абстрактной формы:

`REGISTER_FIT` — соответствие языковой формы ситуации, аудитории и жанру.

Concept сам по себе ещё не говорит, что исправлять.

### `DISTINCTION`

Различие между двумя внешне похожими случаями, которое меняет решение.

Например:

`заимствование ≠ калька`;

`неопределённость как смысл ≠ неопределённость как пустая оболочка`.

Distinction особенно важно сохранять: именно они чаще всего теряются в кратких конспектах.

### `DIAGNOSTIC`

Что искать как потенциальную проблему.

Это не обязательно ошибка и не обязательно команда исправить.

Пример структуры:

`surface → diagnostic question`

а не:

`surface → delete`.

### `OPERATION`

Положительное действие, которое можно попробовать после диагностики.

Пример:

`оценка без основания → поднять уже имеющееся наблюдаемое основание`.

Каждая существенная книга должна проходить отдельный **positive-operation pass**. Первый проход по книге почти всегда переизвлекает запреты лучше, чем способы построить хороший вариант.

### `FORMULA`

Компактная процедурная или причинная модель.

Формула хранится **в проектной нотации**, а не как запоминающаяся авторская фраза.

Примеры допустимого типа:

`candidate → alternative → compare by function → verify`

`known context → new entity → relation → next entity`

`diagnose → transform → success test → guard → final read`

Это механизм, а не цитата.

### `GUARD`

Граница применимости.

Guard может быть:

- локальным полем конкретной операции;
- самостоятельным глобальным принципом, если он ограничивает много карточек.

Например:

`не добавлять агента, если он неизвестен и не нужен для смысла`.

### `CLAIM`

Утверждение источника, которое не следует сразу превращать в правило.

Например:

- норма языка;
- статистика;
- причинное утверждение о психологии;
- исторический факт;
- утверждение о современном употреблении;
- техническое утверждение.

Claim получает отдельный verification status.

### `INTERACTION`

Связь между knowledge units:

- prerequisite;
- sequence;
- conflict;
- refinement;
- joint optimization;
- creates-risk-for;
- supersedes-in-scope.

---

## 4. Canonical card

У каждого публичного knowledge unit должен быть общий минимальный contract.

```yaml
id:
kind: CONCEPT | DISTINCTION | DIAGNOSTIC | OPERATION | FORMULA | GUARD | CLAIM
name:

source:
  locators: []
  provenance:
  edition_confidence:

scope:
  domain:
  genre:
  audience:
  historical:
  level:

confidence:

project_role:
  layer:
  status:

meaning:
trigger:
diagnostic_question:
operation:
success_test:
guard:
counterexample:
invariants: []
do_not_infer: []

automation:
interactions: []

public_safety:
external_verification:
```

Не все поля обязательны для всех `kind`, но **пустой тип нельзя маскировать универсальной карточкой**.

---

## 5. Provenance

Минимальная таксономия.

### `SOURCE_DIRECT`

Автор явно формулирует идею.

### `SOURCE_REPEATED`

Идея устойчиво проводится в нескольких местах.

### `SOURCE_EXAMPLE_ONLY`

Есть отдельный пример, но обобщение уже может принадлежать проекту.

### `PROJECT_DERIVED`

Операционное правило создано проектом из материала источника.

### `PROJECT_REFINED`

Идея источника сохранена, но ограничена современной архитектурой, другим источником или обнаруженным counterexample.

### `PROJECT_FORMULA`

Проект самостоятельно формализовал механизм в компактную процедуру/нотацию.

### `EXTERNAL_CONFIRMED`

Независимый источник подтверждает claim или границу правила.

### `EXTERNAL_CONTESTED`

Есть существенные основания считать claim спорным, устаревшим или слишком сильным.

Ключевой запрет:

> `PROJECT_DERIVED`, `PROJECT_REFINED` и `PROJECT_FORMULA` нельзя выдавать за авторскую формулировку.

---

## 6. Scope — переносимость идеи

Каждая существенная карточка хранит область применимости независимо от provenance.

Минимум:

- `GENERAL`;
- `CONTEXTUAL`;
- `GENRE_SPECIFIC`;
- `AUDIENCE_SPECIFIC`;
- `PROFESSIONAL`;
- `SPOKEN`;
- `WRITTEN`;
- `TRANSLATION_SPECIFIC`;
- `AUTHOR_SPECIFIC`;
- `HISTORICAL`.

И отдельно уровень:

- token/word;
- phrase;
- sentence;
- paragraph;
- scene;
- document;
- corpus/author.

Это защищает от типичной ошибки:

> «Автор правильно заметил проблему в переводе → значит это универсальный закон оригинального русского текста».

---

## 7. Automation class

Книга не должна напрямую определять severity линтера.

У каждой диагностической или операционной карточки отдельное поле automation.

### `HARD_GATE`

Только детерминированная проблема с независимым основанием.

Одного авторитета книги недостаточно.

### `SOFT_SIGNAL`

Surface-признак, который стоит проверить.

### `EDITING_OPPORTUNITY`

Surface-признак + конкретная положительная операция, которую стоит сравнить.

Это предпочтительнее «warning без следующего шага».

### `MODEL_ONLY`

Нужны контекст, семантика, аудитория, морфология, discourse model или world knowledge.

### `REVIEW_GATE`

Финальная человеческая/модельная проверка целого результата.

### `METRIC_ONLY`

Наблюдаемая метрика без самостоятельного нормативного вывода.

---

## 8. Canonical pipeline

### Pass 0 — Source inventory

Зафиксировать:

- author;
- title;
- language;
- edition metadata;
- format;
- filename только в SOURCE workspace;
- fingerprint;
- точное TOC;
- стабильный locator strategy;
- проблемы reflow/pagination;
- недоступные страницы/разделы.

Создать coverage map до извлечения правил.

### Pass 1 — Sequential source read

Прочитать источник последовательно целиком.

Semantic search допустим как навигация, но не как доказательство полного покрытия.

Для каждого раздела временно фиксировать:

- concepts;
- distinctions;
- diagnostics;
- positive models;
- exceptions;
- claims;
- interactions;
- unresolved points.

После этого раздел получает `READ`, но не `VERIFIED`.

### Pass 2 — Independent concept model

До интеграции с текущим проектом построить модель **самой книги**.

Это anti-confirmation-bias gate.

Последовательность:

`BOOK → independent model → audit → project integration`

Не:

`existing project rule → search book for supporting sentence`.

### Pass 3 — Diagnostic extraction

Извлечь атомарные `DIAGNOSTIC`.

Для каждого:

- какой механизм;
- какой trigger;
- какой вопрос задать;
- какой ущерб возможен;
- что является только surface proxy.

Не писать операцию как `удалить X`, если книга на самом деле диагностирует функцию X.

### Pass 4 — Positive-operation reread

Второй сквозной проход.

Для каждого существенного раздела спросить:

1. Какой хороший вариант автор предлагает построить?
2. Что сделать после обнаружения проблемы?
3. Как перестроить содержание, порядок, синтаксис или решение?
4. Что является положительным образцом, а не просто отсутствием ошибки?
5. Как выглядит success test?

Результат — отдельные `OPERATION`, а не guardrails в отрицательной форме.

### Pass 5 — Formula extraction

Отдельно искать повторяемые процедуры и отношения.

Не хранить запоминающуюся авторскую формулировку по умолчанию.

Вместо этого:

1. выделить входные условия;
2. выделить преобразование;
3. выделить критерий выбора;
4. выделить выход;
5. выразить механизм собственной нотацией проекта.

Формула должна быть применима без копирования авторского примера.

### Pass 6 — Guard / counterexample pass

Для каждого contextual diagnostic/operation:

- найти корректный случай с тем же surface trigger;
- сформулировать `guard`;
- сформулировать `do_not_infer`;
- создать synthetic counterexample.

Если counterexample невозможно сформулировать, rule нужно отдельно проверить на чрезмерную широту.

### Pass 7 — Interaction pass

Перечитать знания не по главам, а по механизму.

Искать:

- duplicates;
- prerequisites;
- sequences;
- conflicts;
- compound failures;
- cases where one fix harms another dimension;
- document-level interactions.

### Pass 8 — Claims audit

Все externally verifiable assertions вынести из rule layer.

Statuses:

- `NOT_NEEDED_FOR_OPERATION`;
- `UNVERIFIED`;
- `CONFIRMED`;
- `CONTESTED`;
- `OUTDATED`;
- `SCOPE_LIMITED`.

Книга не превращается в нормативный/научный источник только потому, что мысль полезна редакторски.

### Pass 9 — Project integration

Только теперь сопоставлять с действующей архитектурой.

Каждая source-derived unit получает relation:

- `CONFIRMS`;
- `REFINES`;
- `EXTENDS`;
- `CONFLICTS`;
- `DUPLICATES`;
- `OUT_OF_SCOPE`.

Integration map должен отвечать:

`source unit → project layer → relation → proposed project change`

### Pass 10 — Automation pass

Для каждой идеи решить:

- линтер может увидеть trigger?
- умеет ли он отличить counterexample?
- можно ли предложить положительную operation?
- нужен ли model-only judge?

Принцип:

> если regex умеет увидеть поверхность, но не умеет проверить функцию, результат не может быть hard error.

### Pass 11 — Synthetic eval construction

Никаких book examples как основного eval corpus.

Для важных ideas нужны:

- clear failure;
- positive operation;
- preservation case;
- counterexample;
- tricky context;
- compound case при взаимодействии.

Особенно проверять:

> модель умеет **не исправлять хороший текст**.

### Pass 12 — Public distillation

До коммита преобразовать private extraction в public knowledge layer.

Операции distillation:

- убрать source prose;
- убрать авторские примеры;
- объединить повторяющиеся наблюдения;
- отвязать public structure от порядка страниц;
- переписать механизм собственной терминологией;
- оставить только locators для provenance;
- заменить source examples synthetic examples;
- вынести спорные source claims в claims registry.

### Pass 13 — Loss audit

Снова пройти источник и спросить:

- потеряно ли distinction;
- потеряно ли exception;
- потеряна ли positive operation;
- потерян ли counterexample;
- потеряна ли причина;
- потеряно ли interaction;
- потеряна ли formula;
- потеряна ли historical/scope boundary.

Критерий:

> по public knowledge layer можно принять эквивалентное operational decision, не имея перед глазами авторскую прозу.

### Pass 14 — Public-substitution audit

Отдельный gate перед публикацией.

Спросить:

1. Можно ли по public files восстановить значительную часть последовательности книги?
2. Идёт ли документ chapter-by-chapter с близким пересказом?
3. Сохранили ли мы слишком много уникальных авторских примеров?
4. Сохранили ли мы узнаваемые формулировки, когда достаточно было механизма?
5. Является ли source map картой provenance или фактически оглавлением с конспектом?
6. Можно ли удалить source locators, а operational framework всё ещё останется понятным?
7. Добавляет ли проект собственную структуру, терминологию, evals и integration logic?

Если public artifact полезен главным образом как сокращённая версия чтения книги — distillation недостаточна.

---

## 9. Public source map: что можно хранить

Source map нужен для provenance, но он должен быть **разреженным**.

Хорошо:

| Source locator | Extracted IDs | Status |
|---|---|---|
| chapter/section A | B-C01, B-D03, B-R02 | VERIFIED |
| chapter/section B | B-D04 | VERIFIED |

Допустимо коротко отметить domain/function раздела.

Не нужно в public source map:

- подробный последовательный пересказ главы;
- все аргументы автора;
- цепочку авторских примеров;
- длинные paraphrase-блоки.

Подробные chapter notes относятся к SOURCE workspace.

---

## 10. Формулы: отдельный contract

Поскольку цель проекта — сохранить не только советы, но и **формулы**, для них нужен специальный формат.

```yaml
id: BOOK-F01
kind: FORMULA
name:
inputs: []
transformation:
decision:
output:
success_condition:
guards: []
source_locators: []
provenance: PROJECT_FORMULA
```

Требования:

1. Формула описывает механизм, а не литературную фразу.
2. Переменные и названия принадлежат проекту.
3. Формула не должна требовать авторского примера для понимания.
4. Если формула источник-специфична, scope это показывает.
5. Если авторская формула сама является известным названием/термином, отдельно проверить, что именно требуется для атрибуции и что можно хранить публично.

---

## 11. Recommended public artifact set

Logical layout:

```text
studies/<book-slug>/
  manifest.md
  source-map.md
  concepts.md
  distinctions.md
  diagnostics.md
  operations.md
  formulas.md
  claims.md
  interactions.md
  integration.md
  audit.md
  evals/
```

Физически существующий проект может использовать свои каталоги `references/`, `knowledge/`, `evals/`.

Главное — чтобы `manifest` указывал реальные файлы.

### `manifest.md`

- source metadata;
- edition confidence;
- fingerprint status;
- coverage;
- public/private policy;
- counts by kind;
- paths to artifacts;
- current completion status.

### `source-map.md`

Sparse traceability only.

### `concepts.md` / `distinctions.md`

Модель предметной области книги.

### `diagnostics.md`

Что проверять.

### `operations.md`

Что попробовать сделать.

### `formulas.md`

Компактные механизмы в project notation.

### `claims.md`

Externally verifiable assertions.

### `interactions.md`

Как units работают вместе.

### `integration.md`

Что книга меняет в проекте.

### `audit.md`

Gaps, unresolved interpretations, external verification, public-safety doubts.

---

## 12. Existing project adapter

Для `humanizer_russian` текущие book branches уже показывают три разных физические реализации.

Framework **не требует немедленно их переписать**.

Достаточно, чтобы новые/обновлённые studies могли сопоставиться с canonical kinds:

### Nora Gal

- `GAL-*` atomic rules → mostly `DIAGNOSTIC + OPERATION + GUARD`;
- rule index → provenance/scope;
- source map → traceability;
- eval map → eval traceability.

### Ilyakhov / Sarycheva

- `ILY-*` → `DIAGNOSTIC`;
- `ILY-R*` → `OPERATION`;
- positive evals → operation verification.

### Chukovsky

- first pass → `GUARD / DISTINCTION / DIAGNOSTIC`;
- recommendations → `OPERATION`;
- syntax reconstruction → `MODEL_ONLY OPERATION`;
- linter suggestions → `SOFT_SIGNAL / EDITING_OPPORTUNITY`.

Это и есть причина canonical taxonomy: разные книги больше не обязаны притворяться одной и той же таблицей правил.

---

## 13. Quality gates

### Structural

- all IDs unique;
- all public knowledge units have source locator or explicit `PROJECT_ONLY`;
- all source locators exist in coverage;
- every important diagnostic has at least one operation or explicit reason `NO_OPERATION`;
- every contextual operation has guard;
- every contextual operation has counterexample;
- every operation has success test;
- every externally verifiable claim has status;
- every important unit has eval coverage;
- evals use synthetic examples;
- integration map contains no unknown IDs.

### Coverage

- every source section is `VERIFIED`, `NO_OPERATIONAL_CONTENT`, or explicit `GAP`;
- no silent skipped chapters;
- second positive-operation pass completed;
- formula pass completed;
- loss audit completed.

### Public safety

- no raw source file committed;
- no extracted full text committed;
- no sequential quote collection;
- no author-example corpus;
- source map sparse;
- public examples synthetic by default;
- memorable expression is not stored when mechanism is enough;
- public documents reorganize knowledge by project mechanism rather than source prose order.

### Semantic/manual

Automation cannot prove:

- faithful interpretation;
- absence of overgeneralization;
- quality of counterexamples;
- whether public paraphrase is too close;
- historical transfer validity;
- whether two cards are actually one mechanism.

These require review.

---

## 14. Completion states

### `INGESTED`

Source available and inventory built.

### `READ`

Sequential read complete.

### `MODELED`

Concepts/distinctions extracted independently of project.

### `OPERATIONALIZED`

Diagnostics, positive operations, formulas and guards extracted.

### `TRACEABLE`

Public units map to source locators and provenance.

### `EVALUATED`

Synthetic evals cover important behavior and preservation.

### `INTEGRATED`

Explicit integration map with project exists.

### `AUDITED`

Loss, overgeneralization, claims and public-substitution audits done.

### `PUBLIC_READY`

Public artifacts pass safety and completeness gates.

### `OPERATIONAL`

Project can normally use derived knowledge without reopening the book; source remains necessary for provenance disputes and future rereads.

---

## 15. Definition of Done

A book study is complete only when:

1. source inventory is reproducible;
2. source has been sequentially read;
3. coverage is explicit for every section;
4. concepts and distinctions are extracted before project integration;
5. diagnostics are separated from positive operations;
6. positive-operation reread is complete;
7. formulas/procedures have their own extraction pass;
8. contextual units have guards and counterexamples;
9. claims are separated from operational rules;
10. interactions are represented;
11. project integration relation is explicit;
12. automation level is explicit;
13. synthetic evals test change **and preservation**;
14. loss audit is complete;
15. public-substitution audit is complete;
16. public artifacts do not contain raw/full source text;
17. public structure is not a chapter-by-chapter surrogate of the book;
18. source locators remain sufficient for provenance;
19. unresolved gaps are explicit;
20. the resulting public system is useful because of its **own operational structure**, not because it reproduces the author's exposition.

---

## 16. Compact algorithm

The entire framework can be reduced to:

```text
SOURCE
  ↓
inventory + sequential read
  ↓
independent concepts/distinctions
  ↓
diagnostics
  ↓
positive operations
  ↓
project formulas
  ↓
guards + counterexamples
  ↓
interactions + claims audit
  ↓
project integration
  ↓
automation classification
  ↓
synthetic evals
  ↓
public distillation
  ↓
loss audit + public-substitution audit
  ↓
PUBLIC OPERATIONAL KNOWLEDGE
```

The central rule:

> **Preserve the mechanism; discard the source expression unless the expression itself is the object of analysis.**
