# Contrast handling

## Do not ban the grammar

`не X, а Y`, `не только X, но и Y`, `X, но Y` are valid Russian constructions. The editor should not split or remove them solely to avoid an AI-associated pattern.

## Find the actual contrast

Before rewriting, compare the two sides and factor out shared material when it is informationally redundant.

Synthetic:

> Это не ошибка в расчёте, а ошибка в исходных данных.

Neutral native compression:

> Это ошибка не в расчёте, а в исходных данных.

Marked context-dependent form:

> Это не в расчёте ошибка, а в исходных данных.

The marked variant uses both edges of the phrase for information weight and should not become a default template.

## Do not synonymize mechanically

> Мы не меняем цену, а меняем условия.

Prefer checking:

> Мы меняем не цену, а условия.

before inventing a synonym for the second `меняем`.

## Semantic gain

The second component should actually replace, contrast, add or re-evaluate something. A decorative `не просто курс, а путешествие` can remain weak even though its grammar is fine.

How vivid the second component should be belongs to genre and author voice, not to the normative layer.
