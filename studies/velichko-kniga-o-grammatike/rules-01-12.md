# Atomic rule cards — rules-01-12.md

Status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

## VEL-R01 — Валентность проверяется вместе со значением лексемы

- source_locator: `DOCX2004:P161; P1190-P1223`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: Введение; гл. 8
- claim: Падеж и предлог зависят от конкретного значения лексемы и роли зависимого компонента, а не от абстрактного «синонима».
- project_class: `NATIVE_USAGE`
- grammar_domain: `government/valency`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить участников ситуации и их семантические роли.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны ЛСВ главного слова и роль актанта.
- trigger: Формально правдоподобное, но неестественное управление; перенос рамки другого языка.
- diagnosis: Разрешить значение главного слова; проверить его валентностную рамку и смысл зависимого имени.
- preferred Russian model: `пользоваться чем`; `использовать что для чего/где/как`; `помогать кому`.
- possible repair: Исправить падеж/предлог либо выбрать предикат с нужной валентностью.
- positive example: Мы воспользовались архивом для проверки.
- natural negative control: Мы использовали архив как источник примеров.
- boundary case: `работать с данными` и `работать над моделью` выражают разные связи.
- counterexample: Не исправлять редкую рамку без словарной/корпусной проверки.
- exception: Мотивированные обстоятельственные формы варьируются по смыслу.
- do_not_infer: Не переносить управление одного синонима на всю группу.
- interactions with other rules: VEL-R15, VEL-R16, VEL-R17
- confidence: `high`
- verification status: AUDITED

## VEL-R02 — `прекратить + инфинитив` предполагает контролируемое прекращение

- source_locator: `DOCX2004:P403-P404`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 2
- claim: Фазовое `прекратить` обычно предполагает субъект, способный контролировать прекращение; для самопроизвольного процесса естественнее `перестать`.
- project_class: `NATIVE_USAGE`
- grammar_domain: `phase/agentivity`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить факт прекращения и степень контроля.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужна агентивность субъекта.
- trigger: Неодушевлённый/неконтролирующий субъект при `прекратить + инфинитив`.
- diagnosis: Может ли субъект намеренно остановить действие?
- preferred Russian model: Компания прекратила выпуск; станок перестал вращаться.
- possible repair: Заменить фазовый глагол или перестроить субъект.
- positive example: Редакция прекратила публиковать рубрику.
- natural negative control: Сервер перестал отвечать.
- boundary case: Организация может метонимически быть агенсом.
- counterexample: Не флагать неодушевлённость сама по себе.
- exception: Лексические исключения возможны.
- do_not_infer: Не объявлять это общей грамматической невозможностью.
- interactions with other rules: VEL-R03
- confidence: `medium-high`
- verification status: AUDITED

## VEL-R03 — `бросить + инфинитив` кодирует осознанный окончательный отказ

- source_locator: `DOCX2004:P405`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 2
- claim: `бросить + инфинитив` естественно при личном/агентивном субъекте и передаёт окончательный отказ с внутренним намерением.
- project_class: `NATIVE_USAGE`
- grammar_domain: `phase/agentivity`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить окончательность и волевой компонент.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно знать контроль и намерение субъекта.
- trigger: `бросить + инфинитив` без волевого агента или без значения отказа.
- diagnosis: Есть ли намерение больше не возобновлять действие?
- preferred Russian model: Он бросил курить; мотор перестал работать.
- possible repair: Выбрать `перестать/прекратить/кончить` по смыслу.
- positive example: Она бросила спорить и вышла.
- natural negative control: Сервис перестал отвечать.
- boundary case: Коллективы могут быть метонимическими агенсами.
- counterexample: Не заменять `бросил читать книгу`, если смысл именно «оставил».
- exception: `бросить проект` — отдельная рамка.
- do_not_infer: Не приписывать психологию сверх текста.
- interactions with other rules: VEL-R02
- confidence: `high`
- verification status: AUDITED

## VEL-R04 — Различать процесс, переход и результативное состояние

- source_locator: `DOCX2004:P344-P349; P916-P919; P1342-P1403`
- provenance: `SOURCE_REPEATED + PROJECT_REFINED`
- chapter/section: гл. 1, 6, 9
- claim: Русская форма выбирается по тому, представлен ли эпизод как процесс, граница изменения или актуальный результат.
- project_class: `NATIVE_USAGE`
- grammar_domain: `event_construal/aspect/result`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить временную фазу события.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно знать, что в фокусе: процесс, переход или состояние после него.
- trigger: Формально допустимая форма даёт неверное process/result reading.
- diagnosis: Разложить `до → изменение → после` и определить рематичную фазу.
- preferred Russian model: Процесс — глагол процесса; граница — СВ; состояние — краткое причастие/статив.
- possible repair: Сменить вид, залоговую или предикативную модель.
- positive example: Документ уже подписан.
- natural negative control: Комиссия подписывает документы весь день.
- boundary case: НСВ может быть итеративным, а не прогрессивным.
- counterexample: Не считать любой НСВ ошибочным процессом.
- exception: Жанр может сознательно менять перспективу.
- do_not_infer: Не сводить русский вид к английским временам.
- interactions with other rules: VEL-R08, VEL-R19, VEL-R20
- confidence: `high`
- verification status: AUDITED; overlaps existing break-state-transition

## VEL-R05 — Нулевая связка в настоящем — базовая модель, но `есть` не запрещено

- source_locator: `DOCX2004:P420-P422`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 2
- claim: В настоящем нейтральная связка `быть` обычно нулевая; явное `есть` не должно вставляться как универсальный эквивалент `to be`.
- project_class: `AI_CALQUE`
- grammar_domain: `copula/analyticity`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить идентификацию и прагматический акцент.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Различить нейтральную связку, эмфатическое/логическое и бытийное `есть`.
- trigger: Систематическое `есть` между двумя именными частями без функции.
- diagnosis: Можно ли удалить `есть` без потери контраста/категоричности/бытийности?
- preferred Russian model: Москва — столица; задача — проверить данные.
- possible repair: Нулевая связка, тире/`это` либо специальный связочный глагол.
- positive example: Главная причина — нехватка данных.
- natural negative control: Факт есть факт.
- boundary case: В городе есть театр — бытийная конструкция.
- counterexample: Не делать stop-word `есть`.
- exception: Пунктуация при нулевой связке зависит от структуры.
- do_not_infer: Не флагать все формы `есть`.
- interactions with other rules: VEL-R21, VEL-R22
- confidence: `high`
- verification status: AUDITED; AI_CALQUE project-derived

## VEL-R06 — Неопределённо-личная конструкция не требует фиктивного `они`

- source_locator: `DOCX2004:P726-P737`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 4
- claim: Если деятель неизвестен/неважен/не назван, русский использует 3-е лицо мн. без подлежащего; `они` без референта — типичная RKI-интерференция.
- project_class: `AI_CALQUE`
- grammar_domain: `subject_expression/reference`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить степень определённости деятеля.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен референт `они` в предшествующем контексте.
- trigger: `они + 3pl` при локативной рамке и отсутствии доступного множественного антецедента.
- diagnosis: Кого именно обозначает `они`? Если только «люди там», проверить нулевой субъект.
- preferred Russian model: В отделе заявки проверяют вручную.
- possible repair: Удалить фиктивное местоимение либо назвать реального агента.
- positive example: В сервисе телефоны ремонтируют на месте.
- natural negative control: Инженеры пришли. Они проверяют серверы.
- boundary case: Дальний, но ясный антецедент лицензирует местоимение.
- counterexample: Не удалять `они` при контрасте групп.
- exception: Экспрессивные формы типа `Тебе говорят!` особые.
- do_not_infer: Не считать любой явный субъект неносительским.
- interactions with other rules: VEL-M01
- confidence: `high`
- verification status: AUDITED; source labels learner error

## VEL-R07 — Инфинитивное предложение может кодировать субъект дательным

- source_locator: `DOCX2004:P758-P772`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 5
- claim: Независимый инфинитив часто выражает модальность при субъекте в дательном, без обязательного именительного + модального глагола.
- project_class: `NATIVE_USAGE`
- grammar_domain: `infinitive/subject_relations`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить модальность и носителя действия.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно определить долженствование, возможность, желание и регистр.
- trigger: Тяжёлая аналитическая конструкция там, где русский инфинитивный шаблон точнее.
- diagnosis: Можно ли выразить тот же модальный смысл дательным + инфинитивом без сдвига силы?
- preferred Russian model: Мне завтра выступать; кому звонить?; нам бы отдохнуть.
- possible repair: Перестроить в дательный + инфинитив или, наоборот, развернуть для официальности.
- positive example: Тебе завтра сдавать отчёт.
- natural negative control: Подрядчик обязан сдать отчёт до пяти.
- boundary case: Инфинитивная форма часто экспрессивнее/разговорнее.
- counterexample: Не заменять формальное обязательство разговорным шаблоном.
- exception: Субъект может быть обобщённым и не выражаться.
- do_not_infer: Не считать аналитическую модальную форму ошибкой.
- interactions with other rules: VEL-R08
- confidence: `high`
- verification status: AUDITED

## VEL-R08 — Вид инфинитива различает запрет, ненужность и невозможность

- source_locator: `DOCX2004:P785-P803; P1034-P1040`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 5, 6
- claim: В ряде модальных моделей НСВ и СВ кодируют разные смыслы: запрет/ненужность противопоставлены невозможности результата.
- project_class: `NATIVE_USAGE`
- grammar_domain: `aspect/modality`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Не менять тип модальности.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны смысл модального слова, видовая пара и контекст.
- trigger: Формально правильный инфинитив после `нельзя/не нужно/не...` даёт неверную модальность.
- diagnosis: Действие запрещено, не требуется или невозможно довести до результата?
- preferred Russian model: Нельзя входить = запрет; нельзя войти = невозможность.
- possible repair: Сменить вид или модальную конструкцию.
- positive example: Эту дверь нельзя открывать посетителям.
- natural negative control: Эту дверь нельзя открыть: замок сломан.
- boundary case: Контекст может нейтрализовать видовую оппозицию.
- counterexample: `невозможно жить` естественно с НСВ; учебное «всегда СВ» не универсально.
- exception: Не все видовые пары симметричны.
- do_not_infer: Не выводить вид по одному модальному слову.
- interactions with other rules: VEL-R04
- confidence: `high`
- verification status: AUDITED; teaching generalizations narrowed

## VEL-R09 — Стихийное действие естественно кодируется безличной моделью

- source_locator: `DOCX2004:P880-P899`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 6
- claim: Для непреднамеренного воздействия природной силы русский продуктивно использует объект + безличный глагол ср. рода + творительный силы.
- project_class: `NATIVE_USAGE`
- grammar_domain: `impersonal/event_construal`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить отсутствие намеренного агента.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно отличить силу как причинный фактор от агента объяснения.
- trigger: Калькированная активная/пассивная конструкция звучит тяжело при стихийном событии.
- diagnosis: Есть ли намеренный деятель? Нужен ли природный фактор как тема?
- preferred Russian model: Крышу сорвало ветром; дорогу занесло снегом.
- possible repair: Выбрать безличную модель, активный субъект-силу или пассив по жанру.
- positive example: Линию оборвало льдом.
- natural negative control: Ураган разрушил несколько домов.
- boundary case: В научном объяснении явный субъект-сила может быть лучше.
- counterexample: Не запрещать активную модель.
- exception: Лексический набор безличных глаголов ограничен.
- do_not_infer: Не считать неодушевлённый субъект калькой сам по себе.
- interactions with other rules: VEL-R04
- confidence: `high`
- verification status: AUDITED

## VEL-R10 — Состояние experiencer-а часто выражается косвенным субъектом

- source_locator: `DOCX2004:P920-P957`
- provenance: `SOURCE_REPEATED`
- chapter/section: гл. 6
- claim: Русский часто кодирует непроизвольное физическое/психическое состояние через дательный, винительный или `у + род.` experiencer вместо именительного агента.
- project_class: `NATIVE_USAGE`
- grammar_domain: `impersonal/state`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить различие между переживанием и активным действием.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно определить семантическую роль лица.
- trigger: SVO-конструкция делает состояние чрезмерно агентивным.
- diagnosis: Лицо действует или испытывает состояние? Какой предикат естественно выбирает падеж experiencer-а?
- preferred Russian model: Мне холодно; меня знобит; у меня заложило ухо.
- possible repair: Выбрать безличный предикат и его валентностную рамку.
- positive example: Мне неловко об этом просить.
- natural negative control: Я намеренно молчу.
- boundary case: Некоторые состояния допускают две концептуализации.
- counterexample: Не генерировать несуществующие безличные формы.
- exception: Лексическая валентность обязательна.
- do_not_infer: Не строить общий шаблон «эмоция → дательный».
- interactions with other rules: VEL-R01, VEL-R11
- confidence: `high`
- verification status: AUDITED

## VEL-R11 — Безличные `-ся` конструкции кодируют непроизвольность/условия протекания

- source_locator: `DOCX2004:P958-P968`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 6
- claim: Формы типа `мне работается/не спится/верится` представляют процесс как зависящий от состояния/условий, а не как обычное активное действие.
- project_class: `NATIVE_USAGE`
- grammar_domain: `impersonal/reflexive/state`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить степень контроля и субъективное качество протекания.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно отличить решение/способность от состояния протекания.
- trigger: Дословная личная конструкция не передаёт непроизвольность.
- diagnosis: Говорящий сообщает факт/намерение или то, «как ему идёт» действие?
- preferred Russian model: Мне сегодня не работается; ему не спится.
- possible repair: Выбрать безличную `-ся` форму или оставить личную при агентивном смысле.
- positive example: После разговора мне не спалось.
- natural negative control: Я не буду работать в воскресенье.
- boundary case: Не все глаголы образуют естественную модель.
- counterexample: Не генерировать форму по шаблону.
- exception: Утвердительные формы часто требуют обстоятельственного распространителя.
- do_not_infer: Не считать личное предложение менее русским по умолчанию.
- interactions with other rules: VEL-R10
- confidence: `medium-high`
- verification status: AUDITED

## VEL-R12 — `много/столько/сколько/мало` требуют единственного числа сказуемого

- source_locator: `DOCX2004:P1086`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 7
- claim: При подлежащем `столько, сколько, много, немного, мало, немало + род. мн.` сказуемое употребляется в единственном числе.
- project_class: `NORM`
- grammar_domain: `agreement/quantity`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Согласование соответствует типу количественного подлежащего.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен морфосинтаксический разбор.
- trigger: Множественное сказуемое при указанном количественном ядре.
- diagnosis: Установить, что количественное слово действительно ядро подлежащего.
- preferred Russian model: Сколько дней осталось? Собралось много людей.
- possible repair: Поставить сказуемое в единственное число.
- positive example: Накопилось много вопросов.
- natural negative control: Многие вопросы остались без ответа.
- boundary case: `несколько` допускает вариативность.
- counterexample: Не флагать по одному слову `много` без parse.
- exception: Сложные присоединённые конструкции требуют разбора.
- do_not_infer: Не путать `много` и `многие`.
- interactions with other rules: VEL-R13
- confidence: `high`
- verification status: CURRENT NORM CONFIRMED: Gramota.ru «Правильный выбор единственного и множественного числа сказуемого»
