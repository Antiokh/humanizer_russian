# Decision log

## ADR-001 — Independent repository

Decision: develop `humanizer+ru` in `Antiokh/humanizer_russian`, not as a long-lived branch of `humanizer--ru`.

Reason: the new architecture is no longer a small patch to detector-driven humanizer rules.

## ADR-002 — Separate NORM and NATIVE_USAGE

Decision: academic correctness and native naturalness are different layers.

Reason: a grammatically valid sentence may still be synthetic; a native preference must not be misrepresented as a grammar rule.

## ADR-003 — Soft AI heuristics

Decision: AI/style/native findings do not gate publication automatically.

Reason: these signals have high context dependence and false-positive risk.

## ADR-004 — Corpus-derived author layer

Decision: author style is profiled from a corpus; errors are stored separately and not imitated by default.

## ADR-005 — Preserve upstream MIT notice under GPL project

Decision: keep the new repository's GPL-3.0 license while preserving the MIT notice for inherited material in `THIRD_PARTY_NOTICES.md`.
