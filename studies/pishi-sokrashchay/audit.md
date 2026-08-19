# Loss audit and overgeneralization audit

## 1. Completion

- NCX nodes accounted for: **211/211**.
- Leaf sections read sequentially: **177/177**.
- Unread/inaccessible sections: **0**.
- Leaf sections mapped directly to at least one concept/rule/claim: **159/177**.
- Leaf sections reviewed and intentionally left without a new unit: **18**.

## 2. Loss-audit method

After the first extraction, the source was rescanned against the derived registry rather than reread only by topic. The audit checked:

1. every leaf section against rule/concept/claim coverage;
2. boundary language that commonly changes rule strength (`но`, `если`, `иногда`, `не всегда`, `не нужно`, `это не значит`, etc.);
3. source examples that function as counterexamples rather than as positive prescriptions;
4. cross-chapter repetitions that actually introduce a new constraint;
5. late meta-sections that limit the earlier rules.

The boundary-marker scan surfaced **1347** occurrences across **160/177** leaf sections. These counts are navigation aids, not linguistic evidence or thresholds.

## 3. Sections with no new independent unit

| # | Section | Decision |
|---:|---|---|
| 1 | Максим Ильяхов, Людмила Сарычева ПИШИ, СОКРАЩАЙ (как создавать сильный текст) | title/front matter; no operational distinction |
| 2 | … | front matter/epigraph-like material; no operational distinction |
| 3 | … | front matter; no operational distinction |
| 5 | Откуда взялся информационный стиль | historical origin/context of informational style; context only |
| 7 | Как читать эту книгу | instructions for reading the book; no project writing rule beyond study methodology |
| 28 | Примеры вводных слов и словосочетаний | list/examples supporting earlier metadiscourse rules; no new mechanism |
| 49 | Закрепим | recap of bureaucracy section; no new mechanism |
| 55 | Примеры канцеляризмов | examples supporting bureaucratese/formalism rules; no new mechanism |
| 64 | Примеры зауми | examples supporting plain/precise language rules; no new mechanism |
| 71 | Историческая справка | historical context for euphemism terminology; retained as context, not current norm |
| 188 | Частный мастер | extended self-presentation example; evidence for existing rules, no new mechanism |
| 189 | Разработчик сайтов и приложений | extended self-presentation example; evidence for existing rules, no new mechanism |
| 190 | Агентство | extended company example; evidence for existing rules, no new mechanism |
| 191 | Дизайн-бюро | extended company example; evidence for existing rules, no new mechanism |
| 196 | Текст о пекарне | extended example/exercise; no new mechanism |
| 197 | Текст о библиотеке | extended example/exercise; no new mechanism |
| 204 | Отклик на вакансию программиста | worked job-application example; no new mechanism |
| 208 | Отклик на вакансию продюсера | worked job-application example; no new mechanism |

These sections remain part of 100% reading coverage. Example-heavy sections were not mined into extra rules merely to increase rule count.

## 4. Lost distinctions found during the second pass

The second pass materially changed the first extraction in several places:

- the book's own `Слушайте себя` section makes naturalness and semantic review a late constraint on earlier mechanical rules;
- the comma section argues for changing syntax rather than deleting punctuation; this became `PS-R101` rather than a comma-count rule;
- the section on weak real-world advantages was separated from generic anti-lying advice as `PS-R102`: a text editor must not invent a business advantage;
- exact numbers were split into uncertainty, consequential precision, lower-bound pricing, reader-scale interpretation and suspicious-measurement provenance;
- product advertising was split from general editing into scoped rules for benefit, limitations, evidence and demonstration;
- self-presentation and job application were kept as genre modules rather than silently promoted to general writing laws;
- the final `Дело не в словах` chapter was treated as a meta-rule against mechanically copying the book itself.

## 5. Overgeneralization audit

| Source advice at risk of overreach | Counterpressure | Project refinement |
|---|---|---|
| Стоп-слова → delete-list | Источник сам допускает функциональные стоп-слова. | PS-R06: только candidate + guard. |
| «Мне кажется» → удалить | Может кодировать реальную неуверенность/атрибуцию. | PS-R10/PS-R33 сохраняют эпистемический статус. |
| Скобки → второстепенное → удалить | Скобочная ремарка может быть функциональной или авторской. | PS-R14 оценивает иерархию, не знак. |
| Оценки → убрать | Оценка может быть содержанием жанра/голоса. | PS-R15 различает факт и отношение. |
| Усилители → запрет | Единичная гипербола может быть функциональна. | PS-R18 ловит только декоративное/неподдержанное усиление. |
| Штампы → запрет знакомых фраз | Стандартная формула может быть точной и полезной. | PS-R19 определяет штамп по функции/заменимости. |
| Канцелярит → всегда разговорный язык | Официальная/юридическая точность иногда обязательна. | PS-R22/23 сохраняют функцию регистра. |
| Эвфемизмы → всегда ложь | Такт, инклюзивность и юридический термин могут быть точнее. | PS-R24 проверяет сокрытие факта, а не мягкость. |
| Простые слова → бытовые слова | Профессиональный термин может быть самым точным для аудитории. | PS-R26/27/40 используют audience + precision. |
| Причастие/деепричастие → дефект | Часть речи сама по себе не доказывает нагрузку. | PS-R30 требует контекстного сравнения. |
| Пассив → актив | Пассив полезен для состояния/неважного агента. | PS-R31/32 не насаждают субъекта. |
| Неопределённость → уточнить | Неопределённость может быть самим фактом. | PS-R33 сохраняет реальное незнание. |
| Точные числа → удобные числа | Точность может быть юридически/финансово/научно значима. | PS-R35 сохраняет consequential precision. |
| Одна мысль на предложение → числовая норма | Новизна и нагрузка зависят от аудитории. | PS-R41–44 используют dependency/audience model. |
| Много запятых → удалить запятые | Тяжесть — свойство синтаксиса, не знака. | PS-R101 требует перестройки с сохранением нормы. |
| Действие в каждом предложении | Состояния и безличные конструкции естественны. | PS-R50 сохраняет их при функции. |
| Один абзац — одна мысль | Речь о доминирующей теме информационного абзаца. | PS-R53 не навязывает правило литературе. |
| Вступление/заключение обязательны | Источник сам допускает их отсутствие. | PS-R62/63 требуют функцию, не слот. |
| Картинка > текст > всегда | Сильное source claim без универсальной опоры. | PS-R70/100 превращают иерархию в media-choice test. |
| Конкретика > абстракция | Источник сам показывает полезность абстрактного обобщения. | PS-R73 требует поддержки, не уничтожения абстракции. |
| Факты всегда полезны | Правдивый факт может быть нерелевантен или вводить в ложный расчёт. | PS-R75/77 фильтруют по задаче/инференсу. |
| Польза объясняет любую покупку | Это широкая модель consumer psychology. | Оставлено в PS-CL16, не hard rule. |
| Награды/клиенты бесполезны | Иногда credential или client signal функционален. | PS-R91/92 требуют релевантность, не удаление. |
| Идеальный отклик → приглашение | Источник сам перечисляет неконтролируемые факторы. | PS-R97 запрещает обещать внешний результат. |
| Смысл важнее слов → слова не важны | Авторы называют это своей выбранной позицией; лексическая точность остаётся значимой. | PS-R04/26/99 сохраняют точность; PS-CL26 = AUTHOR_STANCE. |
| Главред 7 баллов → проектная метрика | Tool-specific рекомендация относится к исторической версии инструмента. | PS-CL27 = OUTDATED/TOOL_SPECIFIC. |

## 6. Claims boundary

`counterexamples-claims.md` contains **32** source claims that are not silently promoted to project facts. Status counts:

- `AUTHOR_STANCE`: 1
- `CONTESTED_BY_SOURCE`: 1
- `MODEL`: 1
- `OUTDATED/TOOL_SPECIFIC`: 1
- `PROJECT_REFINED`: 2
- `SCOPE_LIMITED`: 7
- `SOURCE_SCOPE_SUPPORTED`: 1
- `UNVERIFIED`: 18

No external verification was performed in this source-only study. External research, where needed, is a separate future pass.

## 7. Completeness result

Within the supplied EPUB, the study has no unread chapters and no known coverage gaps. `OPERATIONAL` can be claimed for the **source model** in the narrow framework sense: normal use of the derived registry does not require rereading the book. This does **not** mean every source claim is externally true, nor that every rule belongs in `humanizer_russian`.

Project adoption is therefore deferred to the separate `integration.md` pass.
