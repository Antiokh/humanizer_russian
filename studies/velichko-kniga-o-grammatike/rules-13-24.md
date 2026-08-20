# Atomic rule cards — rules-13-24.md

Status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

## VEL-R13 — С количественными группами число сказуемого кодирует совокупность vs активное множество

- source_locator: `DOCX2004:P1085-P1113`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 7
- claim: При числительных, `несколько`, `большинство/ряд/часть` ед./мн. часто конкурируют и зависят от представления группы как целого или множества самостоятельных участников.
- project_class: `NATIVE_USAGE`
- grammar_domain: `agreement/information_structure`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить фокус на совокупности или отдельных деятелях.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны порядок слов, одушевлённость, распространители и семантика сказуемого.
- trigger: Формально допустимое согласование конфликтует с фокусом предложения.
- diagnosis: Группа — мера/совокупность или активные отдельные субъекты?
- preferred Russian model: На лекции присутствовало двадцать человек; двадцать участников подписали письма.
- possible repair: Сменить число только после проверки фокуса и справочника.
- positive example: Пять экспертов выступили по очереди.
- natural negative control: Прошло пять лет.
- boundary case: Многие случаи допускают оба варианта.
- counterexample: Не объявлять один вариант ошибкой из-за одного источника.
- exception: Современный справочник уточняет конкуренцию форм.
- do_not_infer: Не механизировать без morphology/dependencies.
- interactions with other rules: VEL-R12, VEL-R14
- confidence: `high`
- verification status: CURRENT USAGE/NORM CONFIRMED with Gramota; kept contextual

## VEL-R14 — `NOM + с + INSTR` различает равноправных участников и сопровождение

- source_locator: `DOCX2004:P1114-P1119`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 7
- claim: В `мать с дочерью` множественное сказуемое поддерживает равноправие участников, единственное — основной субъект + сопровождающее лицо.
- project_class: `NATIVE_USAGE`
- grammar_domain: `agreement/subject_relations`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить иерархию участников.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно понять, оба ли участника производят действие.
- trigger: Число сказуемого конфликтует с ролью второго участника.
- diagnosis: Можно ли заменить `с` на `и` без изменения смысла?
- preferred Russian model: Оля с Мариной пришли; мать с ребёнком пришла к врачу.
- possible repair: Сменить число или структуру.
- positive example: Директор с юристом подписали документ (оба подписанты).
- natural negative control: Директор вместе с юристом подписал документ.
- boundary case: Смысл иногда двусмыслен и требует явной перестройки.
- counterexample: Не полагаться на ближайшее существительное.
- exception: `я/ты с кем` согласуются по форме местоимения.
- do_not_infer: Не выводить социальную иерархию без контекста.
- interactions with other rules: VEL-R13
- confidence: `high`
- verification status: AUDITED; current hard-gate not established

## VEL-R15 — Немотивированное управление хранится как свойство лексемы

- source_locator: `DOCX2004:P1165-P1188`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 8
- claim: Часть управления нельзя вывести из общего значения падежа: оно является лексическим свойством слова/модели.
- project_class: `NATIVE_USAGE`
- grammar_domain: `government/lexicon`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Не подменять лексическую рамку семантически похожим падежом.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен словарь/корпус конкретной лексемы.
- trigger: Предлог кажется логичным, но не соответствует русской сочетаемости.
- diagnosis: Проверить управление и сравнить с однокоренными/синонимами.
- preferred Russian model: радоваться успеху; надеяться на помощь; восхищаться природой.
- possible repair: Исправить падеж/предлог или заменить главное слово.
- positive example: Он восхищается её работой.
- natural negative control: Он говорит о её работе.
- boundary case: Полисемия меняет рамку.
- counterexample: Не переносить управление одного синонима на другой.
- exception: Есть стилистические варианты (`о книге/про книгу`).
- do_not_infer: Не строить unconditional replacement map.
- interactions with other rules: VEL-R01, VEL-R16, VEL-R17
- confidence: `high`
- verification status: AUDITED

## VEL-R16 — Номинализация может менять управление

- source_locator: `DOCX2004:P1198-P1201`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 8
- claim: Отглагольное существительное не обязано наследовать управление глагола буквально: объект часто переоформляется.
- project_class: `AI_CALQUE`
- grammar_domain: `nominalization/government`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить роль объекта при смене части речи.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужна собственная валентность существительного.
- trigger: Номинализация механически сохраняет глагольный падеж/предлог.
- diagnosis: Сравнить рамки глагола и существительного по словарю/корпусу.
- preferred Russian model: изучать историю → изучение истории; любить живопись → любовь к живописи.
- possible repair: Исправить управление или вернуть глагольную конструкцию.
- positive example: обсуждать проект → обсуждение проекта.
- natural negative control: заботиться о детях → забота о детях.
- boundary case: Часть существительных сохраняет рамку.
- counterexample: Не считать номинализацию плохой сама по себе.
- exception: Регистровая уместность — отдельный вопрос.
- do_not_infer: Не выводить рамку только из словообразования.
- interactions with other rules: VEL-R01, VEL-R15
- confidence: `high`
- verification status: AUDITED

## VEL-R17 — Разные значения одной лексемы могут требовать разных рамок

- source_locator: `DOCX2004:P1219-P1223; P1765-P1774`
- provenance: `SOURCE_REPEATED`
- chapter/section: гл. 8, 10
- claim: У полисемичного слова управление различает значения: `верить кому / в кого`, `отражаться в / на`, `принадлежать кому / к группе`.
- project_class: `NATIVE_USAGE`
- grammar_domain: `valency/polysemy`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить именно выбранное значение.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно разрешить полисемию.
- trigger: Предлог формально правдоподобен, но переключает ЛСВ.
- diagnosis: Подставить толкование каждого значения и проверить его рамку.
- preferred Russian model: верить человеку vs верить в успех; отразиться в тексте vs на результате.
- possible repair: Выбрать правильную рамку или другой предикат.
- positive example: Опыт отразился на решении.
- natural negative control: Тема отражается в романе.
- boundary case: Некоторые контексты допускают два чтения.
- counterexample: Не исправлять только по частотности предлога.
- exception: Стилистические варианты требуют отдельной проверки.
- do_not_infer: Не объединять разные значения по одинаковой поверхности.
- interactions with other rules: VEL-R01, VEL-R15
- confidence: `high`
- verification status: AUDITED

## VEL-R18 — Трёхчленный агентивный пассив стилистически маркирован

- source_locator: `DOCX2004:P1257-P1270`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 9
- claim: Пассив с явно выраженным агентом в творительном естествен прежде всего в книжных стилях; в нейтральной прозе актив/безагентная форма часто естественнее.
- project_class: `NATIVE_USAGE`
- grammar_domain: `voice/register/information_structure`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить объектный фокус, агента и жанр.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны жанр и информационный фокус.
- trigger: Повторяющиеся `X сделан Y-ом` в нейтральном/разговорном тексте.
- diagnosis: Почему объект — тема? Нужен ли агент? Что меняется при активе?
- preferred Russian model: В отчёте пассив может быть уместен; в объяснении часто естественнее актив.
- possible repair: Сменить залог, убрать ненужного агента или сохранить пассив при функции.
- positive example: Эксперимент проведён независимой лабораторией.
- natural negative control: Я написал письмо вчера.
- boundary case: Научный/деловой текст допускает больше пассива.
- counterexample: Не объявлять пассив англицизмом по форме.
- exception: Источник даёт качественное, не количественное распределение.
- do_not_infer: Не механизировать как запрет творительного агента.
- interactions with other rules: VEL-R19, VEL-R20, VEL-M02
- confidence: `medium-high`
- verification status: AUDITED; distribution not quantified

## VEL-R19 — Посессивный результатив `у меня + краткое причастие` отделяет владельца результата от агента

- source_locator: `DOCX2004:P1355-P1361`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 9
- claim: В разговорной/литературно-разговорной речи результат в сфере лица может выражаться `у + род. + краткое причастие`, не утверждая, что лицо само агент.
- project_class: `NATIVE_USAGE`
- grammar_domain: `resultativity/possession/voice`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить результат и неопределённость исполнителя.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить посессора результата и агента.
- trigger: Формальный `мной + краткое причастие` там, где смысл «у меня уже готово».
- diagnosis: Важно, кто сделал, или важен готовый результат у лица?
- preferred Russian model: Билеты у меня куплены; документы у нас подготовлены.
- possible repair: Посессивный результатив, актив или нейтральный результат.
- positive example: У меня всё собрано к поездке.
- natural negative control: Отчёт подготовлен аудитором.
- boundary case: `у меня` может быть слишком разговорно для официального текста.
- counterexample: Не заменять агентивный пассив, если исполнитель важен.
- exception: Посессор может совпадать с агентом, но форма этого не кодирует.
- do_not_infer: Не приписывать действие владельцу результата.
- interactions with other rules: VEL-R04, VEL-R18
- confidence: `high`
- verification status: AUDITED; source gives explicit learner contrast

## VEL-R20 — Статическое состояние нельзя автоматически оформлять акциональным `-ся` пассивом

- source_locator: `DOCX2004:P1380-P1403`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 9
- claim: При статичном расположении/покрытии/состоянии рефлексивный акциональный пассив может дать неносительский процессуальный смысл; краткое причастие/локативная модель естественнее.
- project_class: `AI_CALQUE`
- grammar_domain: `voice/state/process`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить статичность и пространственно-атрибутивное отношение.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить происходящее действие и описание состояния.
- trigger: `заполняется/защищается/покрывается + твор.` в статичном описании.
- diagnosis: Это «что происходит?» или «что/где находится; чем покрыто/окружено»?
- preferred Russian model: Крепость окружена рвом; стена покрыта мозаикой.
- possible repair: Краткое причастие, локативная конструкция или активный статический глагол.
- positive example: Долина окружена горами.
- natural negative control: Крепость защищается гарнизоном от нападения.
- boundary case: `площадь постепенно заполняется людьми` — реальный процесс.
- counterexample: Не флагать `-ся` без теста на процесс/состояние.
- exception: Временные маркеры меняют reading.
- do_not_infer: Не сводить все `-ся` формы к кальке.
- interactions with other rules: VEL-R04, VEL-R18
- confidence: `high`
- verification status: AUDITED; source records learner errors

## VEL-R21 — `являться` не универсальная связка

- source_locator: `DOCX2004:P1434-P1456`
- provenance: `SOURCE_DIRECT + PROJECT_REFINED`
- chapter/section: гл. 10
- claim: `являться чем` книжно и функционально уже нейтрального `быть`; его систематическое использование как универсального `is` делает текст RKI/AI-like.
- project_class: `AI_CALQUE`
- grammar_domain: `copula/register/semantic_relation`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить тип отношения: идентификация, классификация, квалификация, оценка.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны жанр и семантическое отношение между именными частями.
- trigger: Частое `является` в нейтральном объяснении без квалифицирующей функции.
- diagnosis: Это простое `X — Y`, оценочная квалификация или специальный книжный предикат?
- preferred Russian model: Белград — столица Сербии; `является одним из критериев` допустимо в формальном тексте.
- possible repair: Нулевая связка/`это`/точный предикат или сохранение `является` по регистру.
- positive example: Этот показатель является одним из критериев отбора.
- natural negative control: Белград — столица Сербии.
- boundary case: Современный официальный язык допускает `являться` шире учебного описания 2004.
- counterexample: Не объявлять `X является Y` грамматической ошибкой.
- exception: Норма конкретной связки требует современных источников.
- do_not_infer: Не делать stop-word `является`.
- interactions with other rules: VEL-R05, VEL-R22, VEL-M03
- confidence: `medium-high`
- verification status: AUDITED as usage, not NORM

## VEL-R22 — `представлять собой` выражает сущностную характеристику, а не простую идентичность

- source_locator: `DOCX2004:P1457-P1459`
- provenance: `SOURCE_DIRECT`
- chapter/section: гл. 10
- claim: `представлять собой` уместно, когда раскрывается сущность/устройство объекта; как пустая замена `быть` оно тяжело и неточно.
- project_class: `NATIVE_USAGE`
- grammar_domain: `copula/semantic_relation`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить отношение объекта и характеристики.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужно различить сущностное описание и простую классификацию.
- trigger: Оборот соединяет два простых идентифицирующих имени.
- diagnosis: Вторая часть описывает устройство/содержание или только класс?
- preferred Russian model: Система представляет собой набор связанных модулей; файл — отчёт.
- possible repair: Нулевая связка/`это` или уточнение сущности.
- positive example: Архив представляет собой набор версионированных снимков.
- natural negative control: Этот файл — отчёт.
- boundary case: Книжность может быть уместна в определении.
- counterexample: Не убирать оборот, если он действительно раскрывает структуру.
- exception: Регистровый выбор зависит от жанра.
- do_not_infer: Не считать все составные связки канцеляритом.
- interactions with other rules: VEL-R21
- confidence: `high`
- verification status: AUDITED

## VEL-R23 — Причастный оборот не должен быть разорван определяемым словом

- source_locator: `DOCX2004:P1858-P1861`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 11
- claim: Определяемое слово не входит внутрь причастного оборота; разрыв создаёт неверное присоединение.
- project_class: `NORM`
- grammar_domain: `participle/attachment`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Причастный признак однозначно относится к head noun.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужен parse границ оборота.
- trigger: Зависимое слово причастия оказывается по другую сторону head noun и разрывает группу.
- diagnosis: Выделить `причастие + зависимые слова` и head noun.
- preferred Russian model: Купленные сестрой овощи / овощи, купленные сестрой.
- possible repair: Перенести head noun или весь оборот.
- positive example: Подготовленный командой отчёт отправили утром.
- natural negative control: Отчёт, подготовленный командой, отправили утром.
- boundary case: Сложные цепочки определений могут требовать полной перестройки.
- counterexample: Не путать с допустимыми соседними определениями.
- exception: Пунктуация зависит от позиции и обстоятельственного оттенка.
- do_not_infer: Не искать ошибку только по расстоянию.
- interactions with other rules: VEL-R24, VEL-R25
- confidence: `high`
- verification status: CURRENT NORM CONFIRMED: Gramota

## VEL-R24 — Причастие согласуется с реальным определяемым словом, а не ближайшим существительным

- source_locator: `DOCX2004:P1862`
- provenance: `SOURCE_DIRECT + EXTERNAL_CONFIRMED`
- chapter/section: гл. 11
- claim: Полное причастие совпадает с определяемым словом в роде, числе и падеже; вложенный родительный компонент не перехватывает согласование.
- project_class: `NORM`
- grammar_domain: `participle/agreement`
- automation_level: `MODEL_ONLY`
- semantic/function invariant: Сохранить синтаксическую связь определения и head noun.
- scope: sentence/phrase unless noted; see grammar_domain
- required context: Нужны morphology + dependencies.
- trigger: Причастие согласовано с ближайшим существительным, но относится к другому.
- diagnosis: Определить head noun по смыслу/структуре и проверить форму.
- preferred Russian model: на одном из концертов, проведённых в клубе.
- possible repair: Исправить форму причастия или перестроить оборот.
- positive example: В одном из писем, отправленных вчера, была ошибка.
- natural negative control: В письме, отправленном вчера, была ошибка.
- boundary case: Координация/эллипсис требуют полного разбора.
- counterexample: Не выбирать head noun по линейной близости.
- exception: Адъективированные причастия согласуются как прилагательные.
- do_not_infer: Не строить regex по окончаниям.
- interactions with other rules: VEL-R23
- confidence: `high`
- verification status: CURRENT NORM CONFIRMED: Gramota
