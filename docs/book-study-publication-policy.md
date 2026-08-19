# Public publication policy for book-derived studies

Этот файл задаёт **консервативную инженерную политику проекта**, а не юридическое заключение для всех стран.

## Базовая граница

Публичный repository хранит самостоятельную формализацию:

- идей;
- концепций;
- различий;
- процедур;
- методов;
- систем;
- диагностических вопросов;
- положительных операций;
- project formulas;
- собственных synthetic examples/evals.

Публичный repository по умолчанию **не хранит**:

- raw book file;
- extracted full text;
- последовательный близкий пересказ;
- подробные chapter notes;
- набор авторских примеров;
- quote/candidate pool;
- узнаваемые длинные формулировки, если для работы достаточно механизма.

Такой подход согласуется с базовым idea/expression distinction: U.S. Copyright Office отдельно указывает, что copyright защищает конкретное авторское выражение, но не идеи, процедуры, процессы, системы, методы, концепции и принципы как таковые.

Официальные справочные страницы:

- https://www.copyright.gov/help/faq/faq-general.html
- https://www.copyright.gov/title17/92chap1.html#102
- https://copyright.gov/circs/ — Circular 33, Works Not Protected by Copyright

Это не означает, что любой пересказ автоматически безопасен. Именно поэтому framework использует отдельный `public-substitution audit`.

## Public-substitution test

Перед коммитом спросить:

1. Можно ли использовать наши файлы как сокращённую замену чтению книги?
2. Повторяем ли мы порядок книги и её аргументацию раздел за разделом?
3. Сохранили ли слишком много уникальных примеров автора?
4. Сохранили ли запоминающуюся формулировку вместо собственного механизма?
5. Является ли source map только provenance map или уже chapter summary?
6. Можно ли понять operational framework без доступа к source wording?

Если public artifact ценен прежде всего тем, что пересказывает источник, его нужно distill ещё раз.

## Формулы

Формула публикуется как **project notation**:

`inputs → transformation → decision → output → success test`

Даже если механизм найден в книге, имена переменных, компактная запись и интеграция принадлежат project layer и маркируются `PROJECT_FORMULA`.

Если важна именно оригинальная авторская фраза, а не механизм, это отдельный случай для ручного review.

## Source locators

Для provenance достаточно:

- chapter/section title;
- internal ebook locator;
- page number только если edition надёжно установлено;
- source fingerprint при возможности.

Locator не должен содержать длинный source excerpt.

## Default rule

> **Public: mechanism, distinction, operation, guard, formula, synthetic eval.**
>
> **Private/temporary: expression, raw text, close notes, author-example corpus.**
