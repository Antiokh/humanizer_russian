# Editorial Board mode

`BOARD_SKILL.md` describes the expanded orchestration mode of `humanizer_russian`.

The compact product remains `SKILL.md` + `scripts/check.py`. Do not replace it with this mode.

## Goal

Use the same knowledge libraries and mechanical findings as compact mode, preserve source provenance/disagreement, and optionally attach independent evidence without turning evidence sources into fake reviewers.

## Runtime order

1. Preserve `USER_INTENT + SEMANTICS + NORM` as hard constraints.
2. Run registered mechanical knowledge libraries.
3. Normalize findings to the shared finding contract.
4. Group semantically equivalent findings by `phenomenon_id` and local excerpt/span.
5. Keep each reviewer verdict separate.
6. If explicitly requested, run optional Evidence providers against normalized findings.
7. Attach evidence without adding it to reviewer voting.
8. Apply style policy only after reviewer opinions are preserved.
9. Use model reasoning only for `MODEL_ONLY` residue or prose rendering.
10. Re-check semantics and norm before applying a rewrite.

## Reviewer semantics

A reviewer represents a formalized source system, not a simulation of the real author. UI should say `По системе ...`, not pretend the author personally reviewed the text.

## Evidence semantics and availability

Evidence providers are not reviewers. Corpus, spoken-language, lexical, normative or parsed data may support/contextualize a finding but must not enter `reviewer_verdicts`.

Default board mode performs **zero evidence-provider work**. Compact `scripts/check.py` never calls evidence providers.

```bash
python scripts/review.py text.md --style neutral
python scripts/review.py text.md --style neutral --evidence off
```

Opt in only when useful:

```bash
python scripts/review.py text.md --evidence current_usage,spoken_russian
python scripts/review.py text.md --evidence auto
```

`HUMANIZER_EVIDENCE=off` is a global kill switch. Remote providers cannot be enabled by default. Timeout/unavailability is fail-open (`SKIP`) and a global evidence budget prevents a missing service from hanging the board.

See `docs/evidence-provider-architecture.md` and `evidence/README.md`.

## Board statuses

- `CONSENSUS`
- `MAJORITY`
- `SOURCE_CONFLICT`
- `SINGLE_REVIEW`
- `REVIEW`
- `NO_ACTION`

Conflicts are data. Evidence does not turn a source conflict into consensus.

## Styles

Style files are editorial policies, not language rules. They may weight reviewers or define conflict handling, but cannot override semantic/norm guardrails.

## Context budget

Preferred flow:

`mechanical libraries -> normalized findings -> relevant rule cards -> optional targeted evidence -> optional model-only review`.

Do not read every book or query every corpus for every text. If evidence is unavailable, continue without it.

## CLI

```bash
python scripts/review.py text.md --style neutral
python scripts/review.py text.md --style rslive_content --format json
python scripts/review.py text.md --evidence current_usage --format json
```
