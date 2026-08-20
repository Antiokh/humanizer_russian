# Atomic rule cards — rules-25-35.md

Status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

## VEL-R25 — Причастная компрессия возможна только при структурной и семантической совместимости

- source_locator: `DOCX2004:P1863-P1897`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 11
- claim: `который + глагол` и причастный оборот не взаимозаменяемы безусловно; замена зависит от роли `который`, времени/вида и ясности агента.
- project_class: `NATIVE_USAGE`
- grammar_domain: `participle/compression`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Не потерять агента, время, вид и референцию.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен полный синтаксический разбор придаточного.
- trigger: Избыточные `который...` или искусственно нагромождённые причастия.
- diagnosis: Можно ли построить причастие без смены субъекта/объекта и двусмысленности?
- preferred Russian model: данные, полученные вчера; но `данные, о которых говорили` не сворачиваются простой заменой.
- possible repair: Сжать придаточное или развернуть тяжёлый оборот.
- positive example: Данные, полученные вчера, уже проверены.
- natural negative control: Данные, о которых мы говорили вчера, изменились.
- boundary case: Пассивная/активная конверсия меняет фокус.
- counterexample: Не считать `который` AI-маркером сам по себе.
- exception: Разговорная речь обычно избегает тяжёлых причастных цепочек.
- do_not_infer: Не вводить квоту на причастия.
- interactions with other rules: VEL-R23, VEL-R24, VEL-R26
- confidence: `high`
- verification status: AUDITED

## VEL-R26 — Время причастия читается относительно временного плана текста

- source_locator: `DOCX2004:P1900-P1937`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 11
- claim: Настоящее/прошедшее причастие НСВ зависит от плана повествования, одновременности и абстрактности признака; формы иногда нейтрализуются.
- project_class: `NATIVE_USAGE`
- grammar_domain: `participle/tense/discourse`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить временное отношение признака к основной ситуации и моменту речи.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен дискурс/абзац, а не локальная фраза.
- trigger: Форма причастия конфликтует с общим временным планом.
- diagnosis: Признак актуален сейчас, был актуален тогда, абстрактен или одновременен основной ситуации?
- preferred Russian model: работавший здесь до 2024; метод, позволяющий сравнивать версии.
- possible repair: Сменить временную форму или развернуть придаточное.
- positive example: Сотрудник, работавший здесь до 2024 года, переехал.
- natural negative control: Метод, позволяющий сравнивать версии, используется и сейчас.
- boundary case: В историческом повествовании настоящее причастие может быть относительным.
- counterexample: Не согласовывать время причастия механически с главным глаголом.
- exception: Источник сам описывает зоны нейтрализации.
- do_not_infer: Не делать regex по суффиксам.
- interactions with other rules: VEL-R25
- confidence: `medium-high`
- verification status: AUDITED; MODEL_ONLY

## VEL-R27 — Деепричастие требует общего семантического субъекта

- source_locator: `DOCX2004:P2044-P2046`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 12
- claim: В базовой личной конструкции действие деепричастия и основного предиката относится к одному субъекту.
- project_class: `NORM`
- grammar_domain: `gerund/subject_attachment`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Один участник выполняет оба действия, если нет специального исключения.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен семантический субъект, не только формальное подлежащее.
- trigger: Деепричастный оборот логически относится не к субъекту основной предикации.
- diagnosis: Кто выполняет действие деепричастия и кто — основного предиката/инфинитива?
- preferred Russian model: Проверив данные, аналитик нашёл ошибку.
- possible repair: Вернуть общий субъект, сделать придаточное или перестроить основное предложение.
- positive example: Открыв файл, я увидел ошибку.
- natural negative control: Открыв файл, на экране появилась ошибка.
- boundary case: Безличные конструкции с инфинитивом и грамматикализованные обороты — отдельные случаи.
- counterexample: Не флагать только из-за отсутствия именительного подлежащего.
- exception: См. VEL-R28/29.
- do_not_infer: Не применять правило «к ближайшему существительному».
- interactions with other rules: VEL-R28, VEL-R29, VEL-R30
- confidence: `high`
- verification status: CURRENT NORM CONFIRMED: Gramota 2025/2026

## VEL-R28 — `исходя из/учитывая/...` могут грамматикализоваться и не подчиняться простому subject rule

- source_locator: `DOCX2004:P2047-P2048`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED_PARTIAL`
- chapter/section: гл. 12
- claim: Некоторые формы в книжной речи приближаются к предлогам/служебным оборотам и не всегда требуют совпадающего подлежащего как обычное деепричастие.
- project_class: `NATIVE_USAGE`
- grammar_domain: `gerund/grammaticalization`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Не ломать закрепившуюся служебную функцию.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить живое добавочное действие и грамматикализованный оборот.
- trigger: Dangling-gerund checker флагает `исходя из/учитывая` в безличной/номинальной конструкции.
- diagnosis: Можно ли заменить на `на основании/с учётом` без изменения смысла?
- preferred Russian model: Исходя из этих данных, можно пересчитать оценку.
- possible repair: Сохранить служебный оборот или заменить на прозрачный предлог.
- positive example: Исходя из условий задачи, получаем два решения.
- natural negative control: Подходя к окну, мне стало холодно.
- boundary case: `учитывая` может быть настоящим деепричастием.
- counterexample: Не делать unconditional whitelist.
- exception: Грамота фиксирует `исходя из` как предлог.
- do_not_infer: Не считать всякое `учитывая` служебным.
- interactions with other rules: VEL-R27, VEL-R29
- confidence: `high`
- verification status: AUDITED; `исходя из` externally confirmed

## VEL-R29 — В безличном предложении деепричастие допустимо при инфинитиве с общим субъектом

- source_locator: `DOCX2004:P2056-P2059`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 12
- claim: Безличная конструкция может нормативно содержать деепричастие, если оно относится к инфинитиву и субъект двух действий совпадает.
- project_class: `NORM`
- grammar_domain: `gerund/impersonal/infinitive`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить общий семантический субъект деепричастия и инфинитива.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны инфинитив и его контролёр/подразумеваемый субъект.
- trigger: Checker видит деепричастие при безличном предикате.
- diagnosis: Есть ли инфинитив? Кто его субъект? Совпадает ли он с субъектом деепричастия?
- preferred Russian model: Можно решить задачу, проверив исходные данные.
- possible repair: Сохранить; при несовпадении субъектов перестроить.
- positive example: Нам пришлось ждать, сидя в коридоре.
- natural negative control: Проверив данные, мне стало ясно решение.
- boundary case: Модальные предикативы без инфинитива не лицензируют оборот.
- counterexample: Не требовать именительного субъекта при контролируемом инфинитиве.
- exception: Грамматикализованные обороты см. VEL-R28.
- do_not_infer: Не маркировать все безличные + gerund как dangling.
- interactions with other rules: VEL-R27, VEL-R28
- confidence: `high`
- verification status: CURRENT NORM CONFIRMED: Gramota 328468/315990

## VEL-R30 — Деепричастие при объектном инфинитиве — зона повышенной двусмысленности

- source_locator: `DOCX2004:P2061-P2064`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 12
- claim: Если деепричастие относится к субъекту объектного инфинитива, связь становится периферийной/двусмысленной, особенно в препозиции.
- project_class: `NATIVE_USAGE`
- grammar_domain: `gerund/control/attachment`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Читатель должен однозначно понимать исполнителя добавочного действия.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить matrix subject и субъект инфинитива.
- trigger: `A попросил/заставил B сделать X, сделав Y` или препозиционный оборот при объектном инфинитиве.
- diagnosis: К кому естественно присоединяется оборот — к матричному субъекту или исполнителю инфинитива?
- preferred Russian model: При двух чтениях развернуть отдельное придаточное.
- possible repair: Явно назвать субъекта, переместить оборот или заменить придаточным.
- positive example: Редактор попросил автора уточнить вывод после проверки автором данных.
- natural negative control: Автор решил уточнить вывод, проверив данные.
- boundary case: Постпозиция и сильный контекст иногда снимают двусмысленность.
- counterexample: Не запрещать все деепричастия рядом с инфинитивом.
- exception: Субъектный инфинитив обычно безопаснее.
- do_not_infer: Не определять субъекта по одной позиции.
- interactions with other rules: VEL-R27
- confidence: `medium-high`
- verification status: AUDITED; source calls some cases peripheral

## VEL-R31 — Позиция вводного слова меняет область действия модальности

- source_locator: `DOCX2004:P2231`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 13
- claim: Перемещение `кажется/по-видимому` между матричной и придаточной частью может менять, какую пропозицию говорящий считает неуверенной.
- project_class: `NATIVE_USAGE`
- grammar_domain: `introductory_words/scope`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить scope модальности и источник оценки.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно синтаксическое дерево и прагматика.
- trigger: Автоматическая перестановка вводного слова ради ритма/humanization.
- diagnosis: Какую пропозицию модифицирует вводный компонент до и после перестановки?
- preferred Russian model: `Олег, кажется, сказал...` ≠ `Олег сказал, что, кажется, ...`.
- possible repair: Вернуть вводный компонент в нужную клаузу.
- positive example: Похоже, сервер уже восстановился.
- natural negative control: Он сказал, что сервер, похоже, восстановился. (другой scope)
- boundary case: Контекст может нейтрализовать различие.
- counterexample: Не переставлять вводные как декоративные токены.
- exception: Часть вводных слов имеет более свободный scope.
- do_not_infer: Не удалять как «воду» без проверки эпистемической функции.
- interactions with other rules: VEL-R32
- confidence: `high`
- verification status: AUDITED

## VEL-R32 — Вводная конструкция и изъяснительное придаточное — разные модели

- source_locator: `DOCX2004:P2232-P2234`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 13
- claim: `как известно, ...` — вводная рамка; `известно, что...` — предикативная модель. Их механическое смешение создаёт RKI-like синтаксис.
- project_class: `NATIVE_USAGE`
- grammar_domain: `introductory_words/clause_structure`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить синтаксический статус и источник сообщения.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить вводный компонент и управляющий предикат.
- trigger: Смешение `как известно, что...` / `по словам X, что...` без другой опоры.
- diagnosis: Есть ли у `что` управляющий предикат? После удаления вводного оборота остаётся грамматическая структура?
- preferred Russian model: Как известно, у правила есть исключения. / Известно, что у правила есть исключения.
- possible repair: Убрать лишний союз или заменить вводную рамку полноценным сказуемым.
- positive example: Как известно, русский допускает эллипсис.
- natural negative control: Известно, что русский допускает эллипсис.
- boundary case: В сложном предложении `что` может зависеть от другого компонента.
- counterexample: Не regex-ить любую последовательность `, что` после вводного.
- exception: Некоторые формы омонимичны членам предложения.
- do_not_infer: Не сводить вводность к списку слов.
- interactions with other rules: VEL-R31
- confidence: `high`
- verification status: AUDITED; MODEL_ONLY due structural ambiguity

## VEL-M01 — Метрика явных местоименных субъектов

- source_locator: `DOCX2004:P711-P737`
- provenance: `PROJECT_DERIVED`
- chapter/section: гл. 4
- claim: Высокая доля явных `я/мы/они` может быть сигналом RKI/translation-like синтаксиса, но не ошибкой.
- project_class: `AI_CALQUE`
- grammar_domain: `metric/subject_expression`
- automation_level: `METRIC_ONLY`
- semantic/function invariant: Не снижать референциальную ясность ради метрики.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны жанр и разметка референции.
- trigger: Высокая доля явных субъектов при доступном/неопределённом деятеле.
- diagnosis: Измерять без нормативного порога; затем выборочно проверять контекст.
- preferred Russian model: Metric only.
- possible repair: Контекстный эллипсис/односоставная конструкция только при ясности.
- positive example: Проверили файл. Нашли две ошибки.
- natural negative control: Они проверили файл, а мы сверили журнал.
- boundary case: Контраст требует явных субъектов.
- counterexample: Мемуары могут естественно иметь много `я`.
- exception: Baseline жанрозависим.
- do_not_infer: Не выдавать score за качество.
- interactions with other rules: VEL-R06
- confidence: `medium`
- verification status: AUDITED as METRIC_ONLY

## VEL-M02 — Метрика плотности трёхчленного агентивного пассива

- source_locator: `DOCX2004:P1257-P1270`
- provenance: `PROJECT_DERIVED`
- chapter/section: гл. 9
- claim: Высокая плотность `объект + пассив + агент твор.` в нейтральном тексте может сигнализировать книжную/переводную упаковку.
- project_class: `AI_CALQUE`
- grammar_domain: `metric/voice/register`
- automation_level: `METRIC_ONLY`
- semantic/function invariant: Не уничтожать функциональный объектный фокус.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны жанр и morphosyntax.
- trigger: Повторяющиеся агентивные пассивы на коротком отрезке.
- diagnosis: Считать распределение без порога; проверять функции выборочно.
- preferred Russian model: Metric only.
- possible repair: Сравнить с активом/безагентным пассивом.
- positive example: Данные проверила команда.
- natural negative control: Образцы исследованы независимой лабораторией.
- boundary case: Научный/юридический baseline другой.
- counterexample: Один пассив ничего не доказывает.
- exception: Творительный может быть не агентом.
- do_not_infer: Не regex-ить по окончанию.
- interactions with other rules: VEL-R18
- confidence: `medium`
- verification status: AUDITED as METRIC_ONLY

## VEL-M03 — Метрика плотности книжных связок `являться/представлять собой`

- source_locator: `DOCX2004:P1434-P1459`
- provenance: `PROJECT_DERIVED`
- chapter/section: гл. 10
- claim: Частое использование книжных связок как универсального `быть` может быть AI/RKI-сигналом; отдельное употребление обычно допустимо.
- project_class: `AI_CALQUE`
- grammar_domain: `metric/copula/register`
- automation_level: `METRIC_ONLY`
- semantic/function invariant: Не стирать точные квалификационные/сущностные отношения.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны жанр и семантическая классификация.
- trigger: Высокая доля связок в нейтральном объяснении.
- diagnosis: Считать как распределительный сигнал; проверять по VEL-R21/22.
- preferred Russian model: Metric only.
- possible repair: Нулевая связка/`это`/точный глагол только при сохранении смысла.
- positive example: Система — набор модулей.
- natural negative control: Показатель является одним из критериев.
- boundary case: Научный текст допускает больше.
- counterexample: Не использовать как stop-word.
- exception: Лексическое `являться` вне связки не относится.
- do_not_infer: Не менять без semantic parse.
- interactions with other rules: VEL-R21, VEL-R22
- confidence: `medium`
- verification status: AUDITED as METRIC_ONLY
