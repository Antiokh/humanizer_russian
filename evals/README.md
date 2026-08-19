# Eval-наборы humanizer_russian

Основные production-наборы:

- `evals/nora-gal.json` — семантический и литературный слой;
- `evals/russian-language.json` — норма, живой русский, кальки и взаимодействие правил;
- `evals/chukovsky.json` — регистр, позитивные редакторские операции, фразеология и историческая норма после независимого deep book study;
- `gpt/TESTS.md` — ручные smoke-тесты;
- `python3 scripts/lint.py --self-test` — детерминированные surface checks;
- `python3 scripts/benchmark_lint.py` — основной deterministic benchmark mechanical runtime.

Полный book-study eval-набор Чуковского хранится отдельно:

- `studies/chukovsky-zhivoy-kak-zhizn/evals.json` — 58 оригинальных сценариев: 38 direct atomic-rule evals + 20 compound interaction evals;
- `studies/chukovsky-zhivoy-kak-zhizn/eval-map.json` — rule ↔ concept ↔ source ↔ eval coverage.

Production suite намеренно короче independent study: runtime не должен загружать полную книгу/исследование для каждого текста.

## Приоритет

Жёсткие ограничения: `USER_INTENT + SEMANTICS + NORM`.

Среди допустимых вариантов: `AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE`.

Detector score не участвует в критерии успеха.

`EDITING_SUGGESTION` — не ошибка и не обязательная правка. Это указание построить и сравнить альтернативу по смыслу, норме, регистру, адресату, голосу и ритму.

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

Дополнительные normative/native границы, найденные в Chukovsky study, описаны в `references/russian-language.md` и проверяются в `evals/chukovsky.json`: ellipsis vs lexical reanalysis, historical prescription vs current norm, professional variant vs general norm, lexicalized expression vs fresh semantic collision.

## Nora Gal eval

Проверяется:

- конкретность без выдумывания;
- соответствие голосу;
- конфликт метафор;
- сочетаемость;
- синтаксическая калька;
- смысловой акцент и степень уверенности.

После Chukovsky integration действует дополнительная boundary rule: лексикализованная идиома с потухшей внутренней метафорой не должна ошибочно проваливать `SEM-METAPHOR-CONFLICT`; намеренная модификация идиомы не равна случайной контаминации.

## Chukovsky production eval

`evals/chukovsky.json` содержит 30 оригинальных integration-сценариев. Они проверяют:

- функциональный официальный регистр vs register leakage;
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

## Independent Chukovsky eval

`studies/chukovsky-zhivoy-kak-zhizn/evals.json` не является runtime-suite. Он проверяет полноту book study:

- каждому из 38 atomic rules соответствует отдельный original eval;
- всем 20 interaction groups соответствует compound eval;
- negative/counterexample cases обязательны;
- historical/source claims не считаются правилами только потому, что автор книги сформулировал их уверенно.

`eval-map.json` хранит source locators и связи rule → concept → eval, чтобы интеграция оставалась traceable.

## Как оценивать

Judge получает исходный текст, задачу, результат и expectations.

Проверяется функция, а не дословное совпадение с одним эталоном.

`NATIVE_WARNING`, `STYLE_WARNING`, `EDITING_SUGGESTION` и `AI_PATTERN` не являются автоматическим провалом. Намеренная и уместная конструкция может быть сохранена.

Главный negative eval: **не ухудшать уже хороший человеческий русский ради активности, формальной полноты или detector score**.

Для positive editing дополнительно проверяется сама операция выбора: построил ли редактор осмысленную альтернативу, сохранил ли семантику, регистр, роли, просодию и голос.

## Mechanical benchmark и Chukovsky checks

Основной mechanical runtime по-прежнему проверяется через:

```bash
python3 scripts/benchmark_lint.py
```

Chukovsky checks **не добавляются в default mechanical mode**: они контекстно зависимы и доступны через `scripts/lint.py` / `scripts/check.py --extended` как `EDITING_SUGGESTION`.

`scripts/chukovsky_checks.py` механически может только подсветить кандидатов:

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

Он не решает окончательную уместность регистра, семантические роли, current norm исторической формы, идиомность, авторское намерение, искренность или качества личности.

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
