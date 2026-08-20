# Russian RKI/interference grammar diagnostics

This reference is a compact **source-neutral Russian core** layer derived from the audited available fragment of A. V. Velichko (ed.), *Книга о грамматике: Русский язык как иностранный* (2004), then narrowed by current normative checks. It is not a “Velichko style”.

Use it only after mechanical checks. Most rules here are `MODEL_ONLY`. Preserve `USER_INTENT + SEMANTICS + NORM` first.

## 1. Valency and government

Do not judge a case/preposition by surface similarity between words. Resolve the lexical-semantic variant and participant role first. Russian frames can differ between near-synonyms and between meanings of one verb. Nominalization may change government instead of inheriting the verb's frame mechanically.

Audit questions:

- What exact sense of the predicate is active?
- Which participant role is the dependent noun expressing?
- Is the frame lexically fixed or semantically motivated?
- Did a nominalization copy a foreign/verbal frame that Russian changes?

Do not build a regex replacement map for valency.

## 2. Subject realization

Russian does not require every semantic subject to appear as an overt nominative pronoun. Check whether the natural model is:

- indefinite-personal (`В магазине продают хлеб`);
- impersonal (`Мне холодно`, `Меня знобит`);
- dative-subject infinitive (`Мне завтра ехать`);
- natural-force impersonal (`Крышу сорвало ветром`);
- ordinary explicit nominative subject when the referent is discourse-relevant.

A high density of overt `я/мы/он/они` can trigger a document-level audit, but never licenses deletion by itself.

## 3. Process, transition, result and state

Before choosing aspect, voice or copula, identify which event phase is being asserted:

`process → boundary/transition → result → resulting state`.

Do not map an English progressive/passive form directly onto Russian morphology. The existing `ломаться` rule is one concrete case of this broader event-construal check.

## 4. Aspect under modality

Aspect in infinitive constructions can distinguish prohibition/non-necessity from inability to achieve a result, but lexical formulas are not absolute. Compare the intended event:

- `Дверь не открывать` — prohibition / non-performance;
- `Дверь не открыть: замок сломан` — inability to achieve the result;
- `В таком шуме невозможно спать` — natural imperfective activity impossibility.

Aspect selection remains contextual/model-only.

## 5. Voice and resultative perspective

Active and passive structures describe the same broad situation from different information-structural perspectives. Check register and discourse center rather than banning passive.

Three distinctions matter:

- agentive three-member passive is strongly book-oriented but legitimate when the agent matters;
- possessive resultative `у меня + краткое страдательное причастие` can naturally present an available result without identifying the doer (`Билеты у меня куплены`);
- stative/result description is not the same as an ongoing action-passive on `-ся`; do not write a process form merely because another language uses a passive form.

## 6. Copulas and classificatory predicates

Present-tense Russian often uses a zero copula. `есть`, `являться`, `представлять собой`, `состоять в`, `заключаться в`, `сводиться к` are not interchangeable generic equivalents of “be”.

Check semantic function and register:

- identity/classification may need a dash/`это` or zero copula;
- `являться` is bookish and should earn its semantic/register role rather than appear automatically;
- `представлять собой` is useful for revealing nature/structure, not simple naming.

Do not stop-list any of these words.

## 7. Participles

First enforce structural norm: the participial phrase must attach unambiguously to its real head; the participle must agree with that head. Only then compare a relative clause with participial compression.

Use a participle when it compresses a background property without changing time, reference or register. Do not introduce one by quota, and do not expand a clean participle into `который...` merely for simplicity.

## 8. Gerunds

Core check: the gerundial action and the action/state it modifies must share a permissible semantic subject.

Important guards:

- impersonal clause + infinitive can be normative when the gerund and infinitive share the semantic subject (`Проверяя расчёт, можно найти ошибку`);
- grammaticalized/prepositional forms such as `исходя из` are not ordinary free gerunds;
- attachment to an object infinitive can be ambiguous/peripheral and needs explicit semantic review.

Do not implement “no nominative subject → dangling gerund” as a regex.

## 9. Introductory words and scope

Parenthetic modality/source markers are not disposable filler. Position can change scope:

- `Олег, кажется, сказал, что приедет` — speaker uncertainty may concern the saying;
- `Олег сказал, что, кажется, приедет` — uncertainty scopes inside the reported proposition.

Also distinguish parenthetic framing from a predicative complement (`Как известно, ...` vs `Известно, что ...`).

## 10. Explicit non-rules from the source

Do **not** infer any of the following:

- `есть` is forbidden in present-tense existence;
- `невозможно` always requires perfective;
- `не нужно` always requires imperfective;
- bare `к радости` is ungrammatical;
- passive, participles or gerunds are inherently non-native;
- unusual colloquial syntactic phraseologisms should be regularized.

For provenance and full guards, see `studies/velichko-kniga-o-grammatike/`.
