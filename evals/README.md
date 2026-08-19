# Eval-наборы

Основные production-наборы:

- `evals/nora-gal.json` — семантический слой;
- `evals/russian-language.json` — норма, живой русский и взаимодействие правил;
- `evals/chukovsky.json` — production-интеграция Чуковского: регистр, позитивные редакторские операции, фразеология, историческая норма;
- `gpt/TESTS.md` — ручные smoke-тесты;
- `python3 scripts/lint.py --self-test` — детерминированные surface checks.

Полный book-study eval-набор Чуковского хранится отдельно:

- `studies/chukovsky-zhivoy-kak-zhizn/evals.json` — 58 оригинальных сценариев: 38 прямых atomic-rule evals + 20 compound interaction evals;
- `studies/chukovsky-zhivoy-kak-zhizn/eval-map.json` — rule ↔ concept ↔ source ↔ eval coverage.

Production suite намеренно короче независимого study: он проверяет интерфейсы, которые реально вошли в текущую архитектуру, а study сохраняет полную provenance/coverage модель книги.

## Приоритет

`SEMANTICS / NORM > AUTHOR > NATIVE_USAGE > EDITING > AI heuristics`

При конфликте выигрывает сценарий, который сохраняет смысл, не ломает русский язык, учитывает автора/регистр и не заставляет текст быть синтетически полным.

`EDITING_SUGGESTION` — не ошибка и не обязательная правка. Он означает: здесь есть осмысленная альтернативная операция, которую нужно построить и сравнить с исходником.

## russian-language.json

Набор содержит `ru-01` — `ru-21`:

1. нормативное `не X, а Y` не считается AI-ошибкой;
2. противопоставление должно иметь смысловой прирост;
3. обобщение + перечисление восстанавливает двоеточие;
4. однословный ответ с контекстным эллипсисом сохраняется;
5. повтор существительного/сказуемого можно опустить;
6. тема/рема меняют порядок слов;
7. ударный ответ может стоять в начале после вопроса;
8. SVO-lock и повторное называние субъекта перестраиваются по контексту;
9. английская местоименная переэксплицитность убирается;
10. прагматическая частица не удаляется как мусор;
11. висячее деепричастие считается языковой проблемой;
12. бессмысленная парцелляция собирается обратно;
13. осмысленная парцелляция сохраняется;
14. единичный риторический вопрос разрешён;
15. стоп-слово не удаляется без проверки функции;
16. профессиональный жаргон оценивается по аудитории;
17. ошибки из author profile не имитируются по умолчанию;
18. при противительной оценке второй компонент может быть коммуникативно сильнее;
19. `Это не ошибка..., а ошибка...` проверяется на вынос общей части;
20. `Мы не меняем..., а меняем...` проверяется на вынос общего глагола;
21. маркированный порядок слов проверяет совместную работу сильного начала, сильного конца, контекста и компрессии.

Новые normative/native границы из deep study описаны в `references/russian-language.md` и дополнительно проверяются в Chukovsky production suite: ellipsis vs lexical reanalysis, историческая рекомендация vs current norm, профессиональный вариант vs общая норма.

## Nora Gal eval

Проверяется:

- конкретность без выдумывания;
- соответствие голосу;
- конфликт живых метафор;
- сочетаемость;
- синтаксическая калька;
- смысловой акцент и степень уверенности.

После Chukovsky integration добавлена принципиальная граница: лексикализованная идиома с потухшей внутренней метафорой не должна ошибочно проваливать `SEM-METAPHOR-CONFLICT`; намеренная модификация идиомы не равна случайной контаминации.

## Chukovsky production eval

`evals/chukovsky.json` содержит 30 оригинальных сценариев, проверяющих:

- функциональный официальный регистр и register leakage;
- deletion A/B для метадискурса;
- action recovery без выдумывания агента;
- функциональную номинализацию;
- semantic subtraction определения;
- cliché/template cluster vs единичное нормальное употребление;
- proposition-first и no-invention boundary;
- expert term vs public audience;
- reader-effort для аббревиатур;
- ellipsis vs lexical reanalysis;
- идиому как целое;
- intentional idiom mutation vs contamination;
- historical prescription vs current authority;
- scoped professional variant;
- familiar register;
- expressive redundancy;
- read-aloud after semantics;
- dependency/case ambiguity;
- запрет infer sincerity/personality from cliché/slang;
- fresh semantic collision vs lexicalized oddity;
- direct name vs prestige classifier;
- document-level template operation даже без повторяющихся слов.

## Как оценивать

Semantic/native/editing eval получает:

- исходный текст;
- задачу;
- результат;
- expectations сценария.

Judge проверяет функцию, а не дословное совпадение с одним эталоном.

`NATIVE_WARNING`, `STYLE_WARNING`, `EDITING_SUGGESTION` и `AI_PATTERN` не являются автоматическим провалом: намеренная и уместная конструкция может быть сохранена.

Для positive editing важно проверять не только конечную краткость, но и операцию выбора: построил ли редактор осмысленную альтернативу, сохранил ли семантику, регистр, роли, просодию и голос.

## Детерминированный Chukovsky pass

`scripts/chukovsky_checks.py` подключён к `scripts/lint.py` и выдаёт только `EDITING_SUGGESTION` для surface-кандидатов:

- metadiscourse deletion test;
- bureaucratic-register cluster;
- light verb + nominalization;
- nominalization cluster;
- modifier subtraction candidate;
- evaluative-template cluster;
- fresh abstract collision candidate;
- repeated `вопрос` packaging;
- abbreviation-density candidate;
- ending-echo read-aloud test.

Ни одна из этих находок не является hard gate. Линтер не решает окончательную уместность регистра, семантические роли, статус идиомы, текущую норму исторической формы или авторское намерение.

## Будущий корпусный eval

Нужен русский корпус:

- хорошие человеческие тексты разных жанров;
- плохие человеческие тексты;
- сырые LLM-тексты;
- LLM после разных humanizer;
- литературные и маркированные тексты;
- рабочие/технические тексты с жаргоном;
- официальные тексты как negative controls для `REGISTER_LEAK`;
- авторские корпуса для `humanizer+ru+user`;
- пары `исходник → редакторская правка` для калибровки `EDITING_SUGGESTION`.

Численные пороги допустимы только после калибровки с документированными false-positive/false-negative rates.
