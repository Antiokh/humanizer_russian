#!/usr/bin/env python3
"""Russian-language norm, usage and register layer.

This library is deliberately split by confidence:
- NORM findings are only narrow mechanically defensible rules;
- NATIVE_USAGE findings point to a surface that deserves a Russian rewrite check;
- register/jargon findings become default only when the caller explicitly says
  the text is everyday/non-professional.

The module never treats a foreign word, borrowing or professional term as an
error merely because of its origin.
"""
from __future__ import annotations

import re
from typing import Any

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z'-]{1,})(?![A-Za-z0-9_])")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
MD_LINK_TARGET_RE = re.compile(r"\]\([^\n)]*\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(?P<body>.+?)\s*$")
SPLIT_CONTRAST_RE = re.compile(
    r"\bЭто\s+не\s+(?P<left>[^.!?\n]{1,160})\.\s+Это\s+(?P<right>[^.!?\n]{1,160})(?P<end>[.!?])",
    re.I,
)

# Tiny high-precision ontology for a mechanical candidate. This is not a
# general semantic engine: only explicit copular equations between a known
# member noun and its collection noun are surfaced. More general type/category
# collisions remain MODEL_ONLY.
MEMBER_COLLECTION_PATTERNS = [
    re.compile(
        r"\bкниг(?:а|и|у|ой|е|ами|ах)?\b\s*"
        r"(?:(?:—|-)\s*(?:это\s+)?|это\s+)"
        r"библиотек(?:а|и|у|ой|е|ами|ах)?\b",
        re.I,
    ),
]

LATIN_JARGON = {
    "prompt", "runtime", "pipeline", "framework", "benchmark", "preflight",
    "entrypoint", "adapter", "linter", "backend", "frontend", "deploy",
    "deployment", "review", "commit", "merge", "skill", "workflow", "token",
    "dataset", "roadmap", "guardrail", "debug", "release", "production",
    "staging", "feature", "branch", "pull", "request",
}
UPPER_TECH_TERMS = {"AI", "API", "CI", "CD", "JSON", "LLM", "UI", "UX", "SQL", "HTTP", "CLI"}

RUSSIAN_JARGON_PATTERNS = [
    re.compile(pattern, re.I)
    for pattern in [
        r"\bпромпт\w*\b",
        r"\bрантайм\w*\b",
        r"\bпайплайн\w*\b",
        r"\bфреймворк\w*\b",
        r"\bлинтер\w*\b",
        r"\bбенчмарк\w*\b",
        r"\bдепло(?:й|я|ем|ить|ится|енный|енные|енной)\w*\b",
        r"\bэндпоинт\w*\b",
        r"\b(?:бэ|бе)кенд\w*\b",
        r"\bфронтенд\w*\b",
        r"\bревью\w*\b",
        r"\bкоммит\w*\b",
        r"\bмерж\w*\b",
        r"\bскилл\w*\b",
        r"\bроадмап\w*\b",
    ]
]


def _line_no(text: str, start: int) -> int:
    return text.count("\n", 0, max(0, start)) + 1


def _finding(
    rule_id: str,
    phenomenon_id: str,
    project_class: str,
    automation_level: str,
    verdict: str,
    excerpt: str,
    line: int,
    reason: str,
    operation: str | None,
    reviewer_id: str | None = "russian",
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "phenomenon_id": phenomenon_id,
        "project_class": project_class,
        "automation_level": automation_level,
        "verdict": verdict,
        "reviewer_id": reviewer_id,
        "line": line,
        "excerpt": " ".join(excerpt.split())[:240],
        "reason": reason,
        "operation": operation,
        "confidence": None,
    }


def _visible_lines(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    fenced = False
    fence_marker = None
    for line_no, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not fenced:
                fenced = True
                fence_marker = marker
            elif marker == fence_marker:
                fenced = False
                fence_marker = None
            continue
        if not fenced:
            out.append((line_no, raw))
    return out


def _mask_inline(line: str) -> str:
    line = INLINE_CODE_RE.sub(" ", line)
    line = URL_RE.sub(" ", line)
    line = MD_LINK_TARGET_RE.sub("]", line)
    return line


def _heading_period_finding(raw: str, line_no: int) -> dict[str, Any] | None:
    match = HEADING_RE.match(raw)
    if not match:
        return None
    body = re.sub(r"\s+#+\s*$", "", match.group("body")).rstrip()
    if not body.endswith(".") or body.endswith("..."):
        return None
    return _finding(
        "RU-NORM-HEADING-PERIOD",
        "norm.heading_terminal_period",
        "NORM",
        "DEFAULT_MECHANICAL",
        "CHANGE",
        body,
        line_no,
        "В конце вынесенного заголовка точку опускают; вопросительный, восклицательный знак и многоточие сохраняются.",
        "remove_terminal_period_from_heading",
        reviewer_id=None,
    )


def _jargon_automation(register: str) -> str:
    return "DEFAULT_MECHANICAL" if register == "everyday" else "EXTENDED_SOFT"


def review(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    register = str(context.get("register") or "general").lower()
    findings: list[dict[str, Any]] = []
    visible = _visible_lines(text)

    for line_no, raw in visible:
        item = _heading_period_finding(raw, line_no)
        if item:
            findings.append(item)

    for line_no, raw in visible:
        clean = _mask_inline(raw)
        heading = HEADING_RE.match(clean)
        if heading:
            clean = heading.group("body")
        if not clean.strip():
            continue

        cyrillic_letters = len(CYRILLIC_RE.findall(clean))

        for rx in MEMBER_COLLECTION_PATTERNS:
            for match in rx.finditer(clean):
                findings.append(_finding(
                    "RU-SEM-MEMBER-COLLECTION-EQUATION",
                    "semantics.member_collection_equation",
                    "NATIVE_USAGE",
                    "DEFAULT_MECHANICAL",
                    "REVIEW",
                    match.group(0),
                    line_no,
                    "Похоже, отдельный объект/класс приравнен к названию коллекции таких объектов. Проверьте реальное отношение: книга может входить в библиотеку или быть сборником правил, но не становится библиотекой буквально.",
                    "replace_equation_with_real_member_collection_relation",
                ))

        for rx in RUSSIAN_JARGON_PATTERNS:
            for match in rx.finditer(clean):
                findings.append(_finding(
                    "RU-REGISTER-JARGON-TERM",
                    "russian.register_jargon_or_term",
                    "EDITING",
                    _jargon_automation(register),
                    "REVIEW",
                    match.group(0),
                    line_no,
                    "Профессиональный жаргонизм/термин: в бытовом тексте лучше заменить или объяснить; в профессиональном контексте он может быть самым точным вариантом.",
                    "replace_explain_or_keep_by_audience",
                ))

        for match in LATIN_TOKEN_RE.finditer(clean):
            token = match.group(1)
            lower = token.lower()
            is_known_term = lower in LATIN_JARGON or token in UPPER_TECH_TERMS
            if is_known_term:
                findings.append(_finding(
                    "RU-REGISTER-JARGON-TERM",
                    "russian.register_jargon_or_term",
                    "EDITING",
                    _jargon_automation(register),
                    "REVIEW",
                    token,
                    line_no,
                    "Англоязычный технический термин/жаргон: проверьте аудиторию. В бытовом тексте предпочтительны русский эквивалент или короткое объяснение.",
                    "replace_explain_or_keep_by_audience",
                ))

            if cyrillic_letters < 8:
                continue
            if token.isupper() or token[:1].isupper():
                continue
            findings.append(_finding(
                "RU-LEX-LATIN-IN-RUSSIAN",
                "russian.foreign_word_in_russian_prose",
                "NATIVE_USAGE",
                "DEFAULT_MECHANICAL",
                "REVIEW",
                token,
                line_no,
                "Латинское слово внутри русской фразы: проверьте, нужен ли оригинал, или естественнее русский эквивалент/транслитерация/пояснение.",
                "check_russian_equivalent_or_explain_term",
            ))

    prose_parts: list[str] = []
    line_map: list[int] = []
    for line_no, raw in visible:
        if HEADING_RE.match(raw):
            continue
        clean = _mask_inline(raw).strip()
        if clean:
            prose_parts.append(clean)
            line_map.append(line_no)
    prose = "\n".join(prose_parts)
    for match in SPLIT_CONTRAST_RE.finditer(prose):
        line = _line_no(prose, match.start())
        source_line = line_map[min(line - 1, len(line_map) - 1)] if line_map else line
        findings.append(_finding(
            "RU-NATIVE-SPLIT-CONTRAST",
            "native.split_negation_correction",
            "NATIVE_USAGE",
            "DEFAULT_MECHANICAL",
            "REVIEW",
            match.group(0),
            source_line,
            "Разорванное 'Это не X. Это Y.': сравните с единым русским противопоставлением или другой перестройкой; оставьте разрыв, если это намеренная резкая коррекция.",
            "compare_with_single_russian_contrast_or_keep_if_emphatic",
        ))

    return {
        "findings": findings,
        "metrics": {
            "register": register,
            "russian_language_findings": len(findings),
            "model_only_rules": ["RU-SEM-CATEGORY-COLLECTION"],
        },
    }


def self_test() -> None:
    cases = [
        ("# Заголовок.\nТекст.", "RU-NORM-HEADING-PERIOD"),
        ("Это не реальная рецензия. Это оценка по правилам.", "RU-NATIVE-SPLIT-CONTRAST"),
        ("Книги — это библиотеки знаний.", "RU-SEM-MEMBER-COLLECTION-EQUATION"),
        ("Мы используем prompt только для остатка.", "RU-REGISTER-JARGON-TERM"),
        ("Мы используем prompt только для остатка.", "RU-LEX-LATIN-IN-RUSSIAN"),
        ("Это обычный russianword в русской фразе.", "RU-LEX-LATIN-IN-RUSSIAN"),
    ]
    for text, rule in cases:
        rows = review(text, {"register": "everyday"})["findings"]
        assert any(item["rule_id"] == rule for item in rows), (text, rule, rows)

    clean = review(
        "# Заголовок\nЭто не ошибка, а предупреждение.\nКниги хранятся в библиотеках.",
        {"register": "everyday"},
    )["findings"]
    assert not any(item["rule_id"] == "RU-NORM-HEADING-PERIOD" for item in clean), clean
    assert not any(item["rule_id"] == "RU-NATIVE-SPLIT-CONTRAST" for item in clean), clean
    assert not any(item["rule_id"] == "RU-SEM-MEMBER-COLLECTION-EQUATION" for item in clean), clean


if __name__ == "__main__":
    self_test()
    print("Russian language layer: OK")
