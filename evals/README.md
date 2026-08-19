# Eval-наборы humanizer_russian

Основные production-наборы:

- `evals/nora-gal.json` — семантический и литературный слой;
- `evals/russian-language.json` — норма, живой русский, кальки и взаимодействие правил;
- `evals/chukovsky.json` — контекстный integration-suite для регистра, исторической нормы, фразеологии и редакторских операций;
- `gpt/TESTS.md` — ручные smoke-тесты;
- `python3 scripts/lint.py --self-test` — агрегированный surface self-test;
- `python3 scripts/benchmark_lint.py` — основной deterministic benchmark default/extended linter behavior;
- `python3 scripts/benchmark_chukovsky.py` — отдельный deterministic benchmark Chukovsky surface layer.

Полный book-study eval-набор Чуковского хранится отдельно:

- `studies/chukovsky-zhivoy-kak-zhizn/evals.json` — 58 оригинальных сценариев: 38 direct atomic-rule evals + 20 compound interaction evals;
- `studies/chukovsky-zhivoy-kak-zhizn/eval-map.json` — rule ↔ concept ↔ source ↔ eval traceability.

Production suite намеренно короче independent study: обычный runtime не должен загружать полное исследование.

## Приоритет

Жёсткие ограничения: `USER_INTENT + SEMANTICS + NORM`.

Среди допустимых вариантов: `AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE`.

Detector score не участвует в критерии успеха.

`EDITING_SUGGESTION` — не ошибка и не обязательная правка. Это surface-кандидат на конкретный A/B-тест, который затем решается по смыслу, текущей норме, регистру, адресату и голосу.

## Что проверяет russian-language.json

Версия 2 содержит 24 сценария. Основные классы:

- нормативное `не X, а Y` не считается AI-ошибкой;
- общий материал в противопоставлении и повтор глагола проверяются на вынос/опущение;
- вторая часть противопоставления должна приносить реальный смысловой прирост;
- перечисление после вводящей части не режется точками без функции;
- однословные ответы и эллипсис сохраняются;
- тема/рема и сильные края меняют допустимый порядок слов;
- SVO-lock и повторное называние субъекта проверяются на context undercompression;
- избыточные притяжательные местоимения рассматриваются как кандидат на кальку;
- прагматические частицы не удаляются как filler;
- реальный диалог не путается с рекламным Q/A-кластером;
- серийная англо-американская question-answer риторика рассматривается кластером;
- профессиональный code-switching оценивается по аудитории;
- author profile не копирует ошибки;
- локальная/поколенческая лексика требует подтверждения, а не выводится из одной частоты;
- хороший человеческий текст может получить no-op;
- редактор учитывает контекст между абзацами;
- персонализация остаётся внутренним слоем единого `humanizer_russian`.

После Chukovsky integration дополнительно действуют границы из `references/russian-language.md`: ellipsis vs lexical reanalysis, historical prescription vs current norm, scoped professional variant и lexicalized expression vs fresh semantic problem.

## Nora Gal eval

Проверяется:

- конкретность без выдумывания;
- соответствие голосу;
- конфликт метафор;
- сочетаемость;
- синтаксическая калька;
- смысловой акцент и степень уверенности.

После Chukovsky integration добавлена boundary rule: лексикализованная идиома с потухшей внутренней метафорой не должна ошибочно проваливать `SEM-METAPHOR-CONFLICT`; намеренная модификация идиомы не равна случайной контаминации.

## Chukovsky production eval

`evals/chukovsky.json` содержит оригинальные context/model scenarios для:

- функционального официального регистра vs register leakage;
- metadiscourse A/B с сохранением warning hierarchy;
- action recovery без выдумывания агента;
- функциональной номинализации;
- semantic subtraction определения;
- template cluster vs единичного нормального употребления;
- proposition-first с no-invention boundary;
- expert term vs public audience;
- reader effort для сокращений;
- ellipsis vs lexical reanalysis;
- idiомы как целого и idiom mutation vs contamination;
- historical prescription vs current authority;
- scoped professional/familiar register;
- expressive redundancy;
- semantic-role ambiguity;
- запрета infer sincerity/personality from cliché/slang;
- direct name vs реального классификатора.

Эти сценарии не считаются пройденным deterministic benchmark без запуска модели/judge.

## Chukovsky deterministic benchmark

`tests/chukovsky_cases.json` проверяет только механически допустимую часть:

- 7 `EXTENDED_SOFT` surface families;
- естественные negative controls;
- preservation cases;
- metric-only prosodic observation;
- отсутствие отвергнутого semantic-collision regex.

Chukovsky не добавляет правил в default `MECHANICAL_RULES` в этом цикле.

Ритм/эхо окончаний — `METRIC_ONLY`: метрика может подсказать место для чтения вслух, но не создаёт `EDITING_SUGGESTION` и не является стилевой ошибкой.

## Как оценивать model/context evals

Judge получает исходный текст, задачу, результат и expectations.

Проверяется функция, а не дословное совпадение с одним эталоном.

`NATIVE_WARNING`, `STYLE_WARNING`, `EDITING_SUGGESTION` и `AI_PATTERN` не являются автоматическим провалом. Намеренная и уместная конструкция может быть сохранена.

Главный negative eval: **не ухудшать уже хороший человеческий русский ради активности, формальной полноты или detector score**.

Для редакторских операций дополнительно проверяется, построена ли осмысленная альтернатива и сохранены ли семантика, регистр, роли, просодия и голос.

## Будущий корпусный eval

Нужен русский корпус из:

- хороших человеческих текстов разных жанров;
- плохих человеческих текстов;
- сырых LLM-текстов;
- LLM после разных humanizer;
- литературных и маркированных текстов;
- разговорных и ASR-текстов;
- рабочих/технических текстов с жаргоном;
- официальных/юридических текстов как negative controls для ложного register-leak;
- авторских корпусов для проверки `AUTHOR`;
- пар `исходник → редакторская правка` для калибровки `EDITING_SUGGESTION`.

Численные пороги допустимы только после калибровки с документированными false-positive/false-negative rates.
