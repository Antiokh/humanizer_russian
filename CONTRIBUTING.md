# Contributing

`humanizer_russian` is one Russian editor/humanizer with compact and editorial-board modes.

Core constraints: `USER_INTENT + SEMANTICS + NORM`. Preference: `AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score`.

Read `AGENTS.md`, `docs/source-integration-runbook.md`, `libraries/README.md`; for corpora/dictionaries/external data also read `docs/evidence-provider-architecture.md`.

## Books

Books/editorial systems are knowledge libraries with reviewer profiles. Source-specific `rule_id` preserves provenance; shared mechanisms reuse a source-neutral `phenomenon_id`. Preserve `SOURCE_CONFLICT`.

Long-lived author branches (`gal`, `ilyakhov`, `chukovsky`, ...) stay after merge.

## Evidence providers

A corpus, dictionary, current normative reference or parser is **not a reviewer**. Put it under `evidence/<provider>/provider.json` and use `evidence_v1` only when operational.

Rules:

- compact `scripts/check.py` never calls evidence providers;
- board evidence is explicit/off by default;
- network provider must have `enabled_by_default: false`;
- `HUMANIZER_EVIDENCE=off` is a kill switch;
- default `failure_policy` is `SKIP`;
- hard timeout + global evidence budget are mandatory;
- unavailability must not break editing;
- corpus frequency is not current norm by itself;
- evidence direction never becomes a reviewer vote.

Operational provider tests must cover success, unavailable/failure, timeout, default-off behavior, vote separation and provenance.

## Mechanical tests

Before PR:

```bash
python -m compileall -q scripts
python scripts/validate_architecture.py
python scripts/validate_libraries.py
python scripts/lint.py --self-test
python scripts/benchmark_lint.py
python scripts/benchmark_board.py
```

Do not delete natural negative controls to make a rule green. If mechanics require semantics/context, leave the rule soft/model-only.
