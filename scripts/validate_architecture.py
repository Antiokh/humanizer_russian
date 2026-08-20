#!/usr/bin/env python3
"""Guard mechanical-first, dual-runtime architecture against regressions."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED_FILES=["AGENTS.md","CONTRIBUTING.md","SKILL.md","BOARD_SKILL.md","docs/editorial-board-architecture.md","docs/evidence-provider-architecture.md","libraries/README.md","libraries/native/library.json","libraries/russian/library.json","libraries/russian/rules.json","evidence/README.md","evidence/_template/provider.json","reviewers/native.json","reviewers/russian.json","styles/neutral.json","schemas/evidence-provider.schema.json","schemas/evidence-item.schema.json","scripts/check.py","scripts/lint.py","scripts/lint_russian.py","scripts/library_runtime.py","scripts/evidence_runtime.py","scripts/editorial_board.py","scripts/review.py","scripts/validate_libraries.py","scripts/benchmark_lint.py","scripts/benchmark_board.py","tests/lint_cases.json","tests/editorial_board_cases.json","tests/russian_cases.json","tests/russian_board_cases.json","references/russian-core-rules.md",".github/workflows/quality.yml"]
AGENT_MARKERS=["USER_INTENT + SEMANTICS + NORM","AUTHOR > NATIVE_USAGE > EDITING > AI_CALQUE > detector score","Mechanical-first","DEFAULT_MECHANICAL","EXTENDED_SOFT","MODEL_ONLY","tests/lint_cases.json","Два продуктовых режима","Книги — подключаемые библиотеки знаний"]
CHECK_MARKERS=["MECHANICAL_RULES","--extended","--register","from library_runtime import compact_shape, run_libraries"]
BOARD_MARKERS=["Editorial Board mode","scripts/review.py","CONSENSUS","SOURCE_CONFLICT","Evidence","Russian language layer","RU-SEM-CATEGORY-COLLECTION"]
QUALITY_MARKERS=["python -m compileall -q scripts","python scripts/lint.py --self-test","python scripts/lint_russian.py","python scripts/benchmark_lint.py","python scripts/benchmark_lint.py tests/russian_cases.json","python scripts/validate_architecture.py","python scripts/validate_libraries.py","python scripts/benchmark_board.py","python scripts/benchmark_board.py tests/russian_board_cases.json"]
def read(x): return (ROOT/x).read_text(encoding="utf-8")
def main():
    failures=[]
    for f in REQUIRED_FILES:
        if not (ROOT/f).is_file(): failures.append(f"missing required architecture file: {f}")
    if not failures:
        agents=read("AGENTS.md"); check=read("scripts/check.py"); board=read("BOARD_SKILL.md"); quality=read(".github/workflows/quality.yml"); contributing=read("CONTRIBUTING.md")
        for m in AGENT_MARKERS:
            if m not in agents: failures.append(f"AGENTS.md lost required marker: {m}")
        for m in CHECK_MARKERS:
            if m not in check: failures.append(f"scripts/check.py lost compact-library marker: {m}")
        for m in BOARD_MARKERS:
            if m not in board: failures.append(f"BOARD_SKILL.md lost required marker: {m}")
        for m in QUALITY_MARKERS:
            if m not in quality: failures.append(f"quality workflow lost required check: {m}")
        if "evidence_runtime" in check or "run_evidence" in check: failures.append("scripts/check.py must not invoke evidence providers")
        if "humanizer+ru" in contributing: failures.append("CONTRIBUTING.md reintroduced deprecated project name humanizer+ru")
    if failures:
        print("ARCHITECTURE CONTRACT FAILED"); [print(f"- {x}") for x in failures]; raise SystemExit(1)
    print("Architecture contract: OK")
if __name__=="__main__": main()
