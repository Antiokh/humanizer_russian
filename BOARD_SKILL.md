# Editorial Board mode

`BOARD_SKILL.md` describes the expanded orchestration mode of `humanizer_russian`.

The compact product remains `SKILL.md` + `scripts/check.py`. Do not replace it with this mode.

## Goal

Use the same knowledge libraries and mechanical findings as compact mode, but preserve source provenance and disagreements between editorial schools. The board may then produce reviewer-specific comments and a shared recommendation under a selected style policy.

## Runtime order

1. Preserve `USER_INTENT + SEMANTICS + NORM` as hard constraints.
2. Run registered mechanical knowledge libraries.
3. Normalize findings to the shared finding contract.
4. Group semantically equivalent findings by `phenomenon_id` and local excerpt/span.
5. Keep each reviewer verdict separate.
6. Apply style policy only after reviewer opinions are preserved.
7. Use model reasoning only for `MODEL_ONLY` residue or for prose rendering of already-selected findings.
8. Re-check semantics and norm before applying a proposed rewrite.

## Reviewer semantics

A reviewer represents a **formalized system extracted from a source**, not a simulation of the real author.

UI language should prefer:

- `По системе Норы Галь`;
- `По принципам Ильяхова и Сарычевой`;
- `По системе Чуковского`.

Do not present generated comments as authentic quotations, endorsements or real reviews by the author.

## Board statuses

- `CONSENSUS` — all participating reviewer systems that give a directional verdict agree.
- `MAJORITY` — direction exists, but not every reviewer gives the same verdict.
- `SOURCE_CONFLICT` — at least one reviewer says CHANGE and another says KEEP.
- `SINGLE_REVIEW` — only one reviewer has a finding for this phenomenon/span.
- `REVIEW` — signals exist but none is directional enough for automatic advice.
- `NO_ACTION` — reviewer systems explicitly favor keeping the form.

Conflicts are data. Do not erase them during source integration.

## Styles

Style files under `styles/` are editorial policies, not new language rules. They may weight reviewers or define conflict handling, but cannot override hard semantic/norm guardrails.

Examples:

- `neutral` — show disagreement and preserve voice;
- `rslive_content` — prioritize concrete, natural, low-pathos informational Russian.

## Context budget

The board must not read every book/reference for every text.

Preferred flow:

`mechanical libraries → normalized findings → relevant rule cards only → optional model-only review`.

If the mechanical layer already settles a finding, do not duplicate the same analysis in a long prompt.

## CLI

```bash
python scripts/review.py text.md --style neutral
python scripts/review.py text.md --style rslive_content --format json
```

Consumers such as `rslive_content` should integrate against this stable report rather than import internal source linters directly.
