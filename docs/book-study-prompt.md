# Reusable prompt for deep book study

Ниже — универсальный промпт для глубокого разбора книги по `docs/book-study-framework.md`.

Его задача — получить не обзор и не конспект, а воспроизводимую рабочую базу знаний с полной картой покрытия, provenance, ограничениями, counterexamples и evals.

---

## Полный промпт

Изучи предоставленную книгу **полностью и последовательно**, а затем преврати её в операционализируемую базу знаний для проекта.

Не начинай с поиска подтверждений уже существующим правилам проекта. Сначала построй **независимую модель книги**, только потом интегрируй её в текущую архитектуру.

Следуй `docs/book-study-framework.md`.

### 1. Coverage map

Сначала построй карту всех глав/разделов источника.

Для каждого раздела веди статус:

- `UNREAD`
- `READ`
- `EXTRACTED`
- `VERIFIED`

Не считай книгу изученной по semantic-search snippets, оглавлению или нескольким «важным» главам.

### 2. Independent model of the book

До интеграции с проектом опиши:

- главную проблему книги;
- основные concepts;
- distinctions;
- причинные модели;
- diagnostics;
- positive recommendations;
- exceptions/guards;
- критерии хорошего результата;
- meta-methods автора;
- идеи, которые повторяются в разных главах;
- внутренние напряжения или противоречия;
- идеи, которые плохо помещаются в существующую архитектуру проекта.

Не подгоняй эту модель под текущие namespaces проекта.

### 3. Operational extraction

Во втором проходе для каждого содержательного раздела извлеки, если есть:

- `CONCEPT`;
- `DISTINCTION`;
- `DIAGNOSTIC`;
- `POSITIVE_RECOMMENDATION`;
- `GUARD` / `COUNTEREXAMPLE`;
- `CLAIM`;
- `META_METHOD`.

Не своди книгу к списку анти-паттернов.

Для каждого diagnostic отдельно ищи положительный ответ на вопрос:

> Что редактор должен сделать вместо этого?

### 4. Provenance

Для каждой производной единицы укажи происхождение:

- `SOURCE_DIRECT`;
- `SOURCE_REPEATED`;
- `SOURCE_EXAMPLE_ONLY`;
- `PROJECT_DERIVED`;
- `PROJECT_REFINED`;
- `EXTERNAL_NORM`;
- `EXTERNAL_CORPUS`;
- `EXTERNAL_RESEARCH`.

Не выдавай собственный вывод за прямое утверждение автора.

### 5. Scope

Укажи применимость:

- general prose;
- translation;
- fiction;
- business;
- journalism;
- speech;
- formal/conversational register;
- historical usage;
- specific audience;
- specific language pair;
- другие реально необходимые ограничения.

### 6. Rule card

Если знание становится operational rule, используй структуру:

```yaml
id: ...
name: ...
kind: diagnostic | recommendation | guard | norm | heuristic
source: ...
derivation: ...
scope: ...
when: ...
problem: ...
operation: ...
success_test: ...
guards: ...
counterexamples: ...
automation: ...
```

Не смешивай `when` и `operation`.

### 7. Positive model pass

После extraction отдельно проверь, что у каждой крупной темы есть положительная модель:

- что делать;
- как строить хороший вариант;
- как проверить успех;
- какие компромиссы допустимы.

Если остались только запреты, сделай дополнительный проход.

### 8. Interaction pass

Найди взаимодействия между правилами.

Для каждого значимого конфликта укажи:

```yaml
rule_a: ...
rule_b: ...
conflict: ...
priority: ...
resolution: ...
```

Особенно проверяй конфликты:

- краткость vs необходимая оговорка;
- конкретность vs запрет на выдумывание;
- отсутствие повторов vs ритм/эмфаза;
- разговорность vs профессиональная точность;
- простота vs терминологическая точность.

### 9. Automation level

Каждую потенциальную автоматизацию классифицируй:

- `HARD_GATE`;
- `SOFT_SIGNAL`;
- `EDITING_OPPORTUNITY`;
- `MODEL_ONLY`;
- `METRIC_ONLY`.

Не превращай книжную рекомендацию в hard gate без отдельной нормативной/эмпирической базы.

### 10. Mechanical tests

Для каждого механического правила добавь минимум:

- true positive;
- false-positive candidate;
- boundary case;
- intentional-use counterexample;
- другой genre/register, если это влияет;
- exclusions для code/quotes/examples, если нужны.

### 11. Model evals

Для model-only/contextual правил добавь оригинальные сценарии:

1. straightforward problem;
2. counterexample;
3. preservation case;
4. compound interaction case.

Не копируй примеры книги. Создавай новые.

### 12. Claims audit

Отдельно выпиши claims про:

- современную языковую норму;
- частотность употребления;
- историю;
- психологию/когницию;
- статистику;
- технологии;
- этимологию;
- социальные/культурные явления.

Для каждого:

```yaml
claim: ...
source_status: source_only | externally_verified | disputed | outdated
verification_source: ...
```

Если claim может устареть или источник исторический, перепроверь по современной авторитетной базе перед превращением в правило проекта.

### 13. Loss audit

После извлечения спроси:

> Что важного потерялось, потому что не помещается в формат правил?

Проверь большие concepts, эстетические критерии, длинные reasoning chains, exceptions, meta-methods и исторический контекст.

### 14. Overgeneralization audit

Для каждого правила проверь:

- не сделан ли общий запрет из одного примера;
- не потерян ли scope;
- не перенесён ли translation-specific совет в оригинальный текст;
- не превращено ли историческое предпочтение в современную норму;
- есть ли естественный counterexample;
- может ли конструкция быть намеренно полезной.

### 15. Public/private boundary

Не коммить в публичный репозиторий:

- исходную книгу;
- extracted full text;
- большие цитаты;
- последовательный chapter-by-chapter surrogate;
- временные quote pools.

В публичный слой можно вынести:

- оригинально сформулированные rules/concepts;
- sparse source map;
- собственные evals;
- validators;
- operational workflow;
- copyright-safe integration analysis.

### 16. Definition of Done

Не называй разбор законченным, пока:

- все разделы прочитаны;
- coverage map закрыт;
- independent model построен;
- concepts/distinctions/diagnostics/positive recommendations извлечены;
- guards/counterexamples сохранены;
- provenance и scope указаны;
- interaction pass выполнен;
- claims audit выполнен;
- mechanical tests есть;
- model evals есть;
- loss audit выполнен;
- overgeneralization audit выполнен;
- public layer не заменяет чтение книги;
- интеграция в проект сделана только после независимой модели источника.

---

## Короткая команда для следующих книг

> Примени `docs/book-study-framework.md` к этой книге полностью. Сначала sequential coverage и independent model, затем operational extraction с provenance/scope/guards/positive operations, interaction/claims/loss/overgeneralization audits, mechanical tests и model evals. Не подгоняй книгу под существующие правила и не публикуй source-derived surrogate книги.
