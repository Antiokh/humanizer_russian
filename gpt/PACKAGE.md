# Пакет Custom GPT

У `humanizer_russian` два формата распространения:

- Agent Skill: `dist/humanizer-russian.zip`, собирается `scripts/package_skill.py`;
- полный пакет Custom GPT: `dist/humanizer-russian-gpts.zip`, собирается `scripts/package_gpt_runtime.py`.

Сборка Custom GPT повторно использует существующий упаковщик Knowledge, а затем добавляет автономный рабочий контур для Code Interpreter, созданный по тому же белому списку `skill-package.json`, что и пакет Agent Skill.

## Сборка

```bash
python3 scripts/package_gpt_runtime.py --output dist/humanizer-russian-gpts.zip
```

Необязательная распакованная копия:

```bash
python3 scripts/package_gpt_runtime.py \
  --output dist/humanizer-russian-gpts.zip \
  --directory dist/humanizer-russian-gpts
```

Проверка:

```bash
python3 scripts/package_gpt_runtime.py --inspect dist/humanizer-russian-gpts.zip
```

## Структура архива

```text
humanizer-russian-gpts/
├── Instructions/
│   ├── INSTRUCTIONS.md
│   ├── GPT_BUILDER.md
│   ├── CONVERSATION_STARTERS.md
│   └── TESTS.md
├── Knowledge/
│   ├── 00_INDEX.md
│   ├── 01_RUSSIAN_LANGUAGE.md
│   ├── 02_NATIVE_RUSSIAN.md
│   ├── 03_NORA_GAL.md
│   ├── 04_CHUKOVSKY.md
│   ├── 05_ILYAKHOV.md
│   ├── 06_VISSON.md
│   ├── 07_ROSENTHAL.md
│   ├── 08_GOLUB.md
│   ├── 09_AUTHOR_PROFILE.md
│   ├── 10_AUDITS_AND_CORRECTIONS.md
│   ├── 11_EDITORIAL_BOARD.md
│   ├── 12_STYLES.md
│   ├── 13_CAPABILITIES_AND_STATUS.md
│   └── 14_ADDITIONAL_REFERENCE.md  # при необходимости
├── Runtime/
│   └── humanizer_runtime.py
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
└── _manifest.json
```

## Что загружать в GPT Builder

1. Вставьте `Instructions/INSTRUCTIONS.md` в поле **Instructions**.
2. Загрузите все файлы `.md` из `Knowledge/`.
3. Загрузите `Runtime/humanizer_runtime.py`.
4. Включите **Code Interpreter & Data Analysis**.
5. При желании скопируйте заготовки начала диалога.
6. Перед публикацией запустите `humanizer_runtime.py verify` и примеры Preview из `Instructions/TESTS.md`.

Текущий пакет использует 15 файлов Knowledge + 1 рабочий файл = **16 загрузок в GPT**, то есть укладывается в ограничение GPT на 20 файлов.

## Содержимое рабочего контура

`humanizer_runtime.py` генерируется автоматически; это не вторая вручную написанная реализация. Он содержит детерминированный ZIP Agent Skill, собранный из `skill-package.json`, поэтому переносит поддерживаемые рабочие скрипты и данные вместе:

- `check.py`, `review.py`, `lint.py`;
- все текущие точки входа `lint_*` для русского языка, живого употребления, Чуковского, Ильяхова, Галь, Виссон, Розенталя и Голуб;
- рабочий контур редколлегии и профиля автора;
- нормализованные библиотеки, профили рецензентов, стили, справочные материалы, схемы и данные слоя дополнительных источников, включённые белым списком Agent Skill.

Запускатель проверяет хеш встроенного ZIP, умеет сверять каждый встроенный файл с манифестом Agent Skill и компилирует все встроенные Python-файлы.

## Команды рабочего контура

```bash
python3 humanizer_runtime.py verify
python3 humanizer_runtime.py list
python3 humanizer_runtime.py check --json text.md
python3 humanizer_runtime.py check --extended --json text.md
```

Дополнительные команды, перечисляемые `list`, открывают упакованные точки входа рецензирования и линтеров.

## Граница достоверности

GPT может утверждать, что механическая проверка действительно запускалась, только если Code Interpreter фактически выполнил `humanizer_runtime.py`. Рассуждение только по Knowledge не является детерминированным запуском.

Источники дополнительных данных со статусом `PROJECT` остаются недоступны, даже если общий модуль этого слоя присутствует во встроенном пакете Agent Skill.

## Гарантии CI

Рабочий процесс сборки GPT-пакета должен:

- дважды собирать итоговый архив и сравнивать его побайтово;
- удерживать число загружаемых в GPT файлов не выше 20;
- запускать `humanizer_runtime.py verify`;
- сравнивать JSON-вывод и код завершения упакованного `check` с прямым `scripts/check.py` из репозитория для механического и расширенного режимов;
- публиковать как артефакт ровно тот ZIP, который прошёл проверки.
