# Integration decision — Velichko 2004 available fragment

Status: `OPERATIONAL_FOR_AVAILABLE_FRAGMENT`.

## Architectural decision

Velichko is not added as an editorial persona or reviewer. The source is a grammar/RKI evidence layer. Provenance stays in `studies/velichko-kniga-o-grammatike/`, while source-neutral production guidance lives in the existing `russian` core.

The integration therefore consists of:

- source-neutral contextual cards under `libraries/russian/`;
- compact model-only residue in `references/russian-rki-grammar.md`;
- current-NORM refinement for participle/gerund/quantifier rules where independently verified;
- three `METRIC_ONLY` proxies for distributional audit;
- preservation tests proving that context-only RKI patterns are **not** turned into regex findings.

## Counts

- atomic observations: 35
- NORM: 5
- NATIVE_USAGE: 22
- AI_CALQUE: 8
- EDITING: 0
- HARD_GATE: 0
- DEFAULT_MECHANICAL: 0
- EXTENDED_SOFT: 0
- METRIC_ONLY: 3
- MODEL_ONLY: 32

## New RKI/interference families

1. overt-subject bias where Russian chooses an indefinite-personal/impersonal structure;
2. nominative-subject bias vs dative experiencer/infinitive subject;
3. valency transfer across synonyms, polysemy and nominalization;
4. action/state/result confusion in passive and event construal;
5. agentive-passive overuse and failure to use possessive resultatives where functionally natural;
6. `являться` / `представлять собой` used as generic equivalents of “be”;
7. aspect chosen from tense/form alone rather than modal/event meaning;
8. gerund/participle attachment and semantic-subject errors;
9. introductory-word placement that shifts epistemic scope.

## Explicit non-integrations

The following source statements are retained only in `claims.md` and are not production rules:

- absolute ban on `В лесу есть дом`;
- absolute `невозможно + perfective` formula;
- absolute `не нужно + imperfective` formula;
- source's stronger restriction against bare introductory `к радости`;
- treating chapter-10 scientific structures as universally more natural Russian;
- any normalization of syntactic phraseologisms merely because their internal syntax is idiomatic.

## Runtime effect

No new regex warning is introduced. Compact receives metrics only. Editorial Board/model reasoning gets concise source-neutral contextual instructions. Existing Russian mechanical output remains stable unless another already-existing rule fires.
