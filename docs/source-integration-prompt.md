# Reusable prompt: integrate the current book as a long-lived knowledge library

Use this when the book/author is already in the conversation context.

```text
Продолжи работу с текущей книгой/автором в `Antiokh/humanizer_russian`.

Книга уже находится в контексте этого чата. Не спрашивай заново автора/название/файл, если они уже известны. Если оригинал перестал быть доступен в контексте и provenance нельзя восстановить, используй подключённый приватный source repo, если он доступен. Не копируй оригинальную книгу в публичный repo.

Работай в долгоживущей ветке по фамилии автора (`gal`, `ilyakhov`, `chukovsky`, ...). Ветку после merge не удалять.

Сначала прочитай и соблюдай:
- `AGENTS.md`
- `docs/book-study-framework.md`
- `docs/source-integration-runbook.md`
- `docs/editorial-board-architecture.md`
- `libraries/README.md`

ПОРЯДОК РАБОТЫ

1. STUDY AUDIT
   Перепроверь существующий разбор книги по book-study framework: coverage, provenance, locators, atomic rules, positive operations, guards, counterexamples, interactions, claims, loss audit, overgeneralization audit и preservation evals. Если есть gaps — сначала дочитай/доразбери книгу.

2. INTEGRATION MATRIX
   Для всех operational rules зафиксируй:
   rule_id, source_locator, provenance, project_class, scope, semantic_invariant, automation_level, surface_trigger, required_context, false_positive_risk, positive_case, natural_negative_control, boundary_case, intentional_counterexample, existing_overlap, native_usage_conflict, phenomenon_id, planned_module, runtime_visibility.

3. MECHANICAL FEASIBILITY
   Для каждого правила сначала попытайся решить задачу без LLM:
   exact pattern -> regex -> tokenizer -> morphology -> dependency/statistical analysis -> metric-only.
   Precision важнее recall. Не делай псевдолингвистический regex для задачи, которой реально нужен смысл.

4. SOURCE LIBRARY
   Интегрируй автора как отдельную knowledge library, а не как часть единой «редакторской истины».
   Добавь/обнови:
   - source-specific linter module;
   - `libraries/<author>/library.json`;
   - `reviewers/<author>.json`;
   - source-specific tests/evals;
   - производные references/provenance.

   Новые механические модули должны по возможности использовать adapter `review_v1`.

5. PRESERVE DISAGREEMENT
   Разные авторы могут не соглашаться.
   Не стирай конфликт при merge.
   Если разные source rules описывают один механизм, сохрани разные `rule_id`, но дай общий source-neutral `phenomenon_id`.

6. IMPLEMENT MECHANICAL FIRST
   Порядок:
   HARD_GATE -> DEFAULT_MECHANICAL -> EXTENDED_SOFT -> METRIC_ONLY -> MODEL_ONLY.

   Для DEFAULT_MECHANICAL обязательны:
   - true positive;
   - natural negative control;
   - boundary case;
   - intentional counterexample, если применимо;
   - exclusions;
   - deterministic regression.

7. SUPPORT BOTH PRODUCT MODES

   COMPACT:
   `python scripts/check.py text.md`

   EDITORIAL BOARD:
   `python scripts/review.py text.md --style neutral`

   Compact должен давать короткий объединённый результат.
   Board должен сохранять reviewer provenance, consensus/majority/source conflict и style policy.

8. MODEL-ONLY RESIDUE
   Только после mechanical pass интегрируй остаток в короткие contextual references/skill instructions.
   Не загружай полный book study в runtime и не дублируй prompt-ом то, что уже проверяет код.

9. NATIVE RUSSIAN COMPATIBILITY
   Любое книжное EDITING-rule проверяй против `USER_INTENT + SEMANTICS + NORM` и существующего `NATIVE_USAGE`. Книжная школа не должна уничтожать естественный русский, эллипсис, функциональные повторы, информационную структуру, частицы или авторский голос.

10. TEST
   До PR запусти:
   `python -m compileall -q scripts`
   `python scripts/validate_architecture.py`
   `python scripts/validate_libraries.py`
   `python scripts/lint.py --self-test`
   `python scripts/benchmark_lint.py`
   `python scripts/benchmark_board.py`
   плюс source-specific validators/self-tests.

11. BRANCH LIFECYCLE
   Перед PR аккуратно подтяни свежий `main` в author branch, сохранив архитектуру main.
   Финальный PR: `<author-branch> -> main`.
   После merge author branch сохранить для следующего цикла.

В финале дай отчёт:
- study status;
- число operational rules;
- HARD_GATE / DEFAULT_MECHANICAL / EXTENDED_SOFT / METRIC_ONLY / MODEL_ONLY;
- новые mechanical checks и negative controls;
- какие правила были сужены/оставлены model-only;
- какие `phenomenon_id` пересекаются с другими авторами;
- где обнаружены реальные source conflicts;
- результаты compact и board benchmarks;
- вырос ли обязательный runtime context;
- что осталось на следующий проход.

Главная формула:
BOOK -> AUDITED STUDY -> INTEGRATION MATRIX -> MECHANICAL FEASIBILITY -> KNOWLEDGE LIBRARY -> COMPACT + EDITORIAL BOARD -> MODEL-ONLY RESIDUE -> CI -> AUTHOR BRANCH -> MAIN -> KEEP BRANCH.
```
