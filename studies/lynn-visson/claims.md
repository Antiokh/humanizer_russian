# Claims and non-rule material — Lynn Visson

The following source material was deliberately **not** converted into lint rules.

| Claim area | Source treatment | Project disposition |
|---|---|---|
| Russian vs American “optimism/negativity” | broad cultural generalizations, especially chapters II–III | `CONTEXT_ONLY`; surface negation is analyzed grammatically/pragmatically, not psychologically |
| Fatalism, individual responsibility and passive/active expression | chapter IV combines language examples with cultural/psychological explanations | linguistic constructions retained; national-character causality `UNVERIFIED/CONTEXT_ONLY` |
| Political correctness vocabulary and US etiquette | historically situated early-2000s material | `HISTORICAL/PRAGMATIC`; no direct Russian lint rule |
| Who may give advice, how often people thank/apologize/congratulate | pragmatic/cultural observations | `CONTEXT_ONLY`; speech-act formula matching only |
| Monochronic vs polychronic cultures and punctuality | chapter VI | `CULTURAL_CLAIM`; not a grammar rule |
| Meal, drinking and table etiquette | chapter VII | lexical distinctions may survive; etiquette claims do not |
| Gesture, gaze, smile, body distance | chapter IX | `MULTIMODAL_CONTEXT_ONLY`; text linter cannot infer them |
| Russian `амбициозный` is substantially more negative than English ambitious | chapter VIII false friends | `STRONGLY_NARROWED_2026`: modern Gramota dictionaries explicitly include positive/success-oriented senses including «амбициозный проект» |
| Every listed false friend remains equally sharp today | implied pedagogical list | `REQUIRES_CURRENT_USAGE_CHECK`; lexical change can weaken contrast |

## External checks performed for operationalization

- Gramota answer №267016 and answer №304939 explicitly treat `спросить вопрос` as an error/tavtology outside intentional language play; this supports `VISSON-NORM-ASK-QUESTION`.
- Gramota Metadictionary / Big Explanatory Dictionary currently gives `амбициозный` a success-oriented sense and examples including `амбициозный проект`; therefore no ban on that collocation was created.
- Modern Russian grammar/corpus references support negative-concord constructions such as `никто не ...`; the Visson observation is not by itself the normative authority.

## Still requiring corpus/dictionary verification

- current frequency and register of corporate/IT `митинг`;
- whether any domains now use year-scale `декада` productively enough to require exceptions;
- contemporary distribution of standalone `Хорошего дня` and whether it still carries noticeable English influence;
- current spoken-Russian acceptance of particular English-shaped `just → просто` discourse uses;
- corpus calibration for explicit-subject density and SVO regularity (metrics intentionally have no threshold).
