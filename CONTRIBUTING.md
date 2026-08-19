# Contributing

`humanizer_russian` — единый проект русского редактора/humanizer.

Перед изменением правил, линтера, skill или source-specific слоёв прочитай корневой [`AGENTS.md`](AGENTS.md). Он является обязательным архитектурным контрактом и для людей, и для coding/research agents.

## Главная архитектура

Жёсткие ограничения:

`USER_INTENT + SEMANTICS + NORM`

Выбор среди допустимых вариантов:

`AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`

Runtime — **mechanical-first**:

```bash
python scripts/check.py text.md
```

Более рискованные эвристики:

```bash
python scripts/check.py --extended text.md
```

Reference-файлы и model reasoning подключаются адресно, а не целиком на каждый текст.

## Перед добавлением правила

Сначала классифицируй его:

- `NORM-*` — source-backed ограничение русского языка;
- `NATIVE-*` — предпочтение/наблюдение живого русского среди допустимых вариантов;
- `EDIT-*` — редакторская операция или рекомендация;
- `AI-CALQUE-*` — вероятностный машинный/переводной паттерн;
- `AUTHOR-*` — corpus-derived идиолект;
- `ARTIFACT-*` — технический след;
- `GAL-*`, `ILY-*`, `CHUK-*` и другие source namespaces — provenance, а не автоматическая severity.

Не называй native preference грамматической ошибкой. Не называй книжный совет нормой. Не называй нормальную русскую конструкцию AI-паттерном только из-за её частоты у LLM.

## Выбери уровень автоматизации

Каждое правило должно явно попасть в один из уровней:

- `HARD_GATE` — только действительно надёжное блокирующее нарушение;
- `DEFAULT_MECHANICAL` — высокоточная детерминированная surface-проверка;
- `EXTENDED_SOFT` — полезная, но более рискованная эвристика;
- `MODEL_ONLY` — смысл/дискурс/голос/жанр/идиома/просодия;
- `METRIC_ONLY` — описательная статистика без порога.

Книжная рекомендация или detector marker не становятся hard gate автоматически.

## Mechanical rule: обязательный тестовый пакет

Для любого нового mechanical rule нужны минимум:

1. true positive;
2. natural negative control;
3. boundary case;
4. intentional-use counterexample, если применимо;
5. exclusions для code/URL/quotes/markdown/dialogue, если нужны;
6. regression case в `tests/lint_cases.json`;
7. успешный `python scripts/benchmark_lint.py`.

Для `DEFAULT_MECHANICAL` приоритет — precision. Если negative controls не проходят, правило остаётся `EXTENDED_SOFT` или `MODEL_ONLY`.

Не удаляй существующий negative test только ради того, чтобы новая эвристика стала зелёной. Если ожидание теста действительно было неверным, объясни изменение в PR.

## Evidence expectations

Для `NORM-*` приводи актуальный авторитетный источник.

Для `AI-CALQUE-*` с числовым порогом документируй корпус, язык, жанры, модели/дату и false-positive behavior. Без калибровки это мягкая эвристика.

Для `NATIVE-*` нужны положительные и отрицательные примеры и контекст. Corpus evidence и review филолога усиливают правило, но не превращают его автоматически в академическую норму.

Для книжных источников сохраняй provenance и scope. Исторические нормативные claims перепроверяй по современному источнику.

## Интеграция Галь, Ильяхова, Чуковского и следующих источников

Текущий `main` — архитектурная база.

Старую source-ветку нельзя мержить выбором `theirs` поверх core-файлов. Нужно переносить source-specific знания поверх текущей mechanical-first архитектуры.

Особенно не откатывай wholesale:

- `AGENTS.md`;
- `SKILL.md`;
- `scripts/check.py`;
- `scripts/lint.py`;
- `scripts/benchmark_lint.py`;
- `tests/lint_cases.json`;
- `.github/workflows/quality.yml`;
- `README.md`;
- этот файл.

Для крупных source-linters предпочитай отдельные модули (`lint_ilyakhov.py`, `chukovsky_checks.py` и т. п.) с агрегацией в основном линтере.

`EDITING` идёт после `NATIVE_USAGE`: редакторская школа не должна заставлять русский звучать менее естественно.

## Evals

Deterministic surface rules проверяются benchmark-ом, а не model judge.

Model evals используются для контекстных задач: смысл, тема/рема, голос, register, POV, идиомы, сложное взаимодействие правил.

Каждый meaningful contextual rule должен иметь preservation/counterexample case.

Не называй JSON fixtures «пройденным benchmark», если модель фактически не запускалась.

## Author profiles

Не храни raw corpus paths, приватный исходный текст или психологические диагнозы в generated profile.

Ошибки автора отделяй от стиля и по умолчанию не имитируй.

## Перед PR

Запусти минимум:

```bash
python -m compileall -q scripts
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
```

Если менялся profiler/schema или source-specific validator — запусти и их.

CI должен добавлять новые проверки к существующим, а не заменять базовый compile/self-test/benchmark.

В PR явно укажи:

- provenance;
- новые правила/операции;
- automation level каждого класса;
- hard gates и обоснование;
- positive/negative/boundary tests;
- риск false positives;
- что остаётся model-only;
- конфликт/совместимость с `NATIVE_USAGE`;
- нужен ли новый runtime context (по умолчанию — минимальный и адресный).
