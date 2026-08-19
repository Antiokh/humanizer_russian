# Cross-review prompt for parallel book-study chats

Скопируй этот prompt в параллельный чат, который уже разбирал другую книгу в `Antiokh/humanizer_russian`.

```text
Посмотри ветку `agent/book-study-framework-v2`, прежде всего:

- `docs/book-study-framework-v2.md`
- `docs/book-study-card-schema.md`

Задача — не похвалить framework и не переписать его целиком, а проверить его на опыте КОНКРЕТНО ТВОЕЙ книги и ветки.

Сначала кратко перечисли, какие артефакты и проходы реально понадобились в твоём book study.

Затем сделай gap analysis по framework v2:

1. Какие важные виды знания из твоей книги framework НЕ умеет выразить?
2. Какие поля/card types лишние или слишком абстрактные?
3. Есть ли у тебя случай, который не помещается в:
   CONCEPT / DISTINCTION / DIAGNOSTIC / OPERATION / FORMULA / GUARD / CLAIM / INTERACTION?
4. Достаточно ли чётко разведены diagnostic и positive operation?
5. Достаточно ли framework защищает от превращения author advice в hard ban?
6. Есть ли важный positive pass, который framework не требует?
7. Есть ли interaction/compound behavior, которое framework теряет?
8. Достаточно ли automation taxonomy:
   HARD_GATE / SOFT_SIGNAL / EDITING_OPPORTUNITY / MODEL_ONLY / REVIEW_GATE / METRIC_ONLY?
9. Сможет ли public/private split реально сохранить идеи твоей книги, не превращая public repo в её последовательный пересказ?
10. Какие текущие файлы в ТВОЕЙ ветке по этому framework стоило бы оставить public, какие distilled, а какие вообще держать только в SOURCE workspace?
11. Не слишком ли строг public-substitution audit? Не слишком ли слаб?
12. Какие quality gates можно реально автоматизировать?
13. Какие requirements framework создадут ложное чувство полноты?
14. Какие 3–10 конкретных изменений ты предлагаешь внести?

После анализа:
- предложи точные изменения в `docs/book-study-framework-v2.md`;
- при необходимости предложи изменения card schema;
- НЕ мержи ничего;
- не перестраивай свою book branch под framework автоматически;
- сначала оставь свои предложения как review/change proposal, чтобы их можно было сравнить с отзывами других book chats.

Особенно приведи 2–5 реальных примеров ИЗ СТРУКТУРЫ ТВОЕГО STUDY (не длинные цитаты из книги), на которых видно, зачем нужна предлагаемая поправка.
```

## Что мы хотим получить от нескольких параллельных чатов

После Норы Галь, Ильяхова/Сарычевой, Чуковского и следующих книг должны появиться независимые поправки.

Затем их можно свести по принципу:

- повторяется у нескольких книг → вероятный framework primitive;
- требуется одной конкретной книгой → domain extension;
- конфликтует между книгами → framework должен поддерживать оба варианта, а не выбирать школу;
- относится к текущему `humanizer_russian`, а не к book study вообще → оставить в project adapter.
