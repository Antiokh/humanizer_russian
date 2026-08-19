# Nora Gal — MODEL_ONLY residue

Этот файл — компактный operational reference для контекстного board-pass. Он **не заменяет book study** и не дублирует mechanical findings. Полные source fields, guards и preservation cases хранятся в `libraries/gal/rules/*.json`; provenance — в `studies/nora-gal/` и `references/nora-gal-source-map.md`.

Mechanical implementation уже отвечает за `GAL-KANZ-VERB`, `GAL-KANZ-PSEUDOFORMAL`, `GAL-EXPLICITNESS`; metric-only слой — за описательные метрики `GAL-KANZ-PARTICIPLE`, `GAL-SOUND-COLLISION`, `GAL-LONG-SENTENCE-CLARITY`. Ни одно из них не нужно повторно диагностировать моделью только потому, что оно есть в книге.

## 36 contextual rules

| Rule | Phenomenon | Source locator | Что нужно модели | Главный guard |
|---|---|---|---|---|
| `GAL-KANZ-NOUN-CHAIN` | `editing.nominal_chain_obscures_relations` | Откуда что берется?; Жечь или сушить?; Туманы… | восстановить отношения между существительными | не выдумывать одну трактовку двусмысленной цепи |
| `GAL-KANZ-PASSIVE` | `editing.passive_obscures_agent` | Откуда что берется?; Жечь или сушить? | понять, важен/известен ли агент | пассив нормативен; неизвестного агента не создавать |
| `GAL-EVENT-ORDER` | `editing.event_order_obscured` | Жечь или сушить? | временная логика и субъект | ретроспекция может быть намеренной |
| `GAL-KANZ-STAMP` | `editing.template_without_semantic_gain` | Откуда что берется?; Мертвый хватает живого | функция формулы в жанре | термин, цитата, пародия и жанровая формула допустимы |
| `GAL-KANZ-ABSTRACTION` | `editing.abstract_container_hides_specifics` | Словесная алгебра | доступна ли конкретика из контекста | не придумывать конкретику |
| `GAL-LEX-CONCRETE` | `editing.contextual_concreteness` | Словесная алгебра | что уже известно читателю | родовой термин может быть намеренным |
| `GAL-LEX-PRECISION` | `editing.lexical_precision` | Мертвый хватает живого; Сотри случайные черты…; Буква… | контекстное значение и оценка | редкое/многозначное слово может быть точным |
| `GAL-LEX-COLLOCATION` | `editing.collocation_mismatch` | На ножах; «Свинки замяукали» | идиома, домен, авторское намерение | необычная художественная/профессиональная сочетаемость допустима |
| `GAL-LEX-RARE-FIT` | `editing.marked_lexeme_register_fit` | Мертвый хватает живого; Кто мы и зачем мы? | значение, эпоха, голос | редкость сама по себе не дефект |
| `GAL-BORROWING-FIT` | `editing.borrowing_register_fit` | А если без них?; Куда же идет язык?; Веревка — вервие простое | аудитория, домен, эпоха | не делать stop-list заимствований |
| `GAL-TERM-AUDIENCE` | `editing.terminology_audience_fit` | Веревка — вервие простое | кто читатель и нужен ли термин | точный термин не упрощать до неточного бытового слова |
| `GAL-VOICE-PERSONA` | `editing.voice.persona_fit` | Не своим голосом; Мистер с аршином; Поклон мастерам | подтверждённый голос/корпус | AUTHOR выше EDITING |
| `GAL-VOICE-SITUATION` | `editing.voice.situation_fit` | Не своим голосом; Когда глохнет душа | ситуация, отношения, эмоция | холодность/формальность может быть намеренной |
| `GAL-VOICE-INTERNAL` | `editing.voice.internal_monologue_fit` | Не своим голосом | POV и тип внутренней речи | функциональный повтор не удалять |
| `GAL-VOICE-AGE` | `editing.voice.age_fit` | Не своим голосом; Пять чувств — и еще шестое | конкретный ребёнок и среда | не вводить сюсюканье/ошибки по возрасту |
| `GAL-REGISTER-ERA-CULTURE` | `editing.register_era_culture_fit` | А если без них?; Мистер с аршином; На ножах | эпоха, страна, социальная среда | анахронизм/доместикация могут быть авторским приёмом |
| `GAL-EMOTIONAL-TACT` | `editing.emotional_tone_fit` | Когда глохнет душа; Пять чувств — и еще шестое | эмоциональная температура и дистанция | чёрный юмор/цинизм/холодность могут быть намеренными |
| `GAL-IDIOM-CONTAMINATION` | `editing.idiom_play_vs_contamination` | «Свинки замяукали» | является ли гибрид случайным | игра слов и пародия сохраняются |
| `GAL-IDIOM-FUNCTION` | `editing.idiom_function_preservation` | «Свинки замяукали»; Буква…; Мадам де Займи и другие | значение, регистр, культурная функция | чужая форма может быть важна сама по себе |
| `GAL-IMAGE-COLLISION` | `editing.image_system_collision` | На ножах; Сотри случайные черты… | локальная система образов | сюрреализм/комизм могут быть намеренными |
| `GAL-IMAGE-LITERALIZATION` | `editing.image_literalization_collision` | На ножах; «Свинки замяукали» | активировал ли контекст буквальный смысл | намеренный каламбур сохранять |
| `GAL-POLYSEMY-COLLISION` | `editing.polysemy_accidental_collision` | На ножах | активировано ли нежелательное второе значение | художественная неоднозначность допустима |
| `GAL-PHYSICAL-PLAUSIBILITY` | `editing.physical_plausibility` | На ножах; Сотри случайные черты…; Пять чувств — и еще шестое | физика мира/сцены | сон, фантастика, метафора имеют свою условность |
| `GAL-SYNTAX-RUSSIAN` | `editing.non_native_syntactic_frame` | Туманы…; Буква…; … Или Дух?; SOS! | предтекст, тема/рема, идиома | свободный русский порядок слов не нормализовать к SVO |
| `GAL-FOCUS-WORD-ORDER` | `editing.information_focus_fit` | Туманы…; … Или Дух? | предыдущие предложения и интонация | важное может стоять и в начале; AUTHOR/NATIVE_USAGE выше |
| `GAL-SENTENCE-BOUNDARY` | `editing.sentence_boundary_function` | Туманы…; … Или Дух?; SOS! | логика, пауза, ритм | функциональная парцелляция сохраняется |
| `GAL-RHYTHM-PACE` | `editing.rhythm_pace_fit` | … Или Дух?; Многоликость таланта; Открытие Хэмингуэя; Музыка перевода | абзац/сцена и чтение вслух | не оптимизировать по числовой вариативности |
| `GAL-SUBTEXT-RESTRAINT` | `editing.subtext_overexplanation` | Открытие Хэмингуэя; Поклон мастерам | авторская степень недосказанности | справочный жанр может требовать явности |
| `GAL-WHOLE-BEFORE-DETAIL` | `editing.local_change_whole_fit` | Сотри случайные черты…; Поклон мастерам | сцена/документ целиком | локальный диссонанс может быть намеренным |
| `GAL-CHARACTER-CONTINUITY` | `editing.character_voice_continuity` | Сотри случайные черты…; Свет и сумрак Фицджеральда | предыдущие сцены/дуга героя | персонаж может закономерно меняться |
| `GAL-POV-CONSISTENCY` | `editing.pov_consistency` | Сотри случайные черты… | режим повествования | всеведение, свободно-косвенная речь и смена POV допустимы |
| `GAL-VERIFY-REFERENCE` | `editing.reference_requires_verification` | Предки Адама | внешний источник, если доступен | NEEDS_VERIFICATION не равно CHANGE |
| `GAL-EDITOR-NOT-DICTATOR` | `editing.preserve_valid_author_choice` | Кто мы и зачем мы? | отличить дефект от вкуса | NORM/SEMANTICS ошибки не защищаются авторским вкусом |
| `GAL-EDITOR-THIRD-SOLUTION` | `editing.find_third_solution` | Кто мы и зачем мы?; … Или Дух? | сравнить исходник и предложенную правку | не переписывать хороший текст бесконечно |
| `GAL-SELF-EDIT` | `editing.self_edit_fresh_read` | Кто мы и зачем мы? | перечитать результат после изменения | отсутствие нового дефекта не требует ещё одной правки |
| `GAL-COMPOUND-FAILURE` | `editing.compound_failure` | SOS!; сквозной метод | предложение/абзац как система | не суммировать warnings в quality/AI score и не переписывать без инварианта |

## Board contract

Контекстный reviewer должен формулироваться как **«По системе Норы Галь»**, выдавать `CHANGE`, `KEEP`, `REVIEW` или `NEEDS_VERIFICATION` только после применения guards и сохранять `rule_id` + `phenomenon_id`. Если другая библиотека даёт противоположный verdict на то же явление, это `SOURCE_CONFLICT`, а не повод стирать provenance или голосовать по большинству.
