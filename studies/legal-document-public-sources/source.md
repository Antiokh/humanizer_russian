# Public sources: legal and official-document layer

## Scope

Исследование открытой нормативно-методической базы для профессиональных русскоязычных документов.

Это не исследование одной книги, а тематический source bundle. Для каждого правила в `rules.md` должен быть указан конкретный источник.

## Sources

### DOC-GOST-2025

ГОСТ Р 7.0.97-2025 «Система стандартов по информации, библиотечному и издательскому делу. Организационно-распорядительная документация. Требования к оформлению документов».

- status: current standard
- effective: 2025-08-18
- official metadata: https://protect.gost.ru/gost/details/360994e3-9a70-47b9-ab3a-cf21809e26ed
- copyright note: не хранить/распространять полное официальное издание в репозитории; использовать source locators и проектные извлечения.

### DOC-VNIIDAD-GOST-2026

Методические рекомендации по применению ГОСТ Р 7.0.97-2025 / ВНИИДАД, 2026, 134 с.

- status: official methodological guidance
- publication date: 2026-04-17
- landing page: https://archives.gov.ru/documents/methodics/met-rek-gost-7-0-97-2025.shtml
- pdf: https://archives.gov.ru/sites/default/files/mr_po_gost_r_7.0.97_fin_sayt_1.pdf

### DOC-ROSARCHIVE-71

Приказ Росархива от 22.05.2019 № 71 «Об утверждении Правил делопроизводства в государственных органах, органах местного самоуправления».

- status: current base act; amendments must be tracked separately
- official publication: https://publication.pravo.gov.ru/Document/View/0001201912300064
- reference text: https://www.consultant.ru/document/cons_doc_LAW_342093/

### DOC-ROSARCHIVE-91-2026

Приказ Росархива от 09.07.2026 № 91 о внесении изменений в приказ № 71.

- registered: 2026-08-12, Минюст № 87817
- status checked on 2026-08-28: `PENDING_CHANGE`; reference system marks it as not yet effective
- reference: https://www.consultant.ru/document/cons_doc_LAW_541782/

### DOC-ROSARCHIVE-199

Методические рекомендации по разработке инструкций по делопроизводству, утв. приказом Росархива от 25.12.2020 № 199.

- status: official methodological guidance
- order: https://archives.gov.ru/documents/prik199_2020.shtml
- full HTML: https://archives.gov.ru/documents/methodics/2020-recommendations-deloproizvodstvo.shtml

### DOC-DUMA-LEGALTECH-2021

Методические рекомендации по юридико-техническому оформлению законопроектов, редакция 2021 года.

- status: official legal-technical guidance for draft legislation
- reference text: https://www.consultant.ru/document/cons_doc_LAW_379680/

## Source policy

- `CURRENT_NORM`: действующее требование;
- `PENDING_CHANGE`: изменение известно, но ещё не действует;
- `METHODICAL`: официальная методическая рекомендация;
- `PROJECT_DERIVED`: правило проекта, выведенное из источника;
- `DOMAIN_CONVENTION`: профессиональная практика, требующая отдельного подтверждения;
- `HISTORICAL`: устаревшее правило.

Нельзя повышать `METHODICAL` до `CURRENT_NORM` без нормативного основания.
