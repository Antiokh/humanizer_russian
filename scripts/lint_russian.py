#!/usr/bin/env python3
"""Russian-language norm, usage, rubrication and register layer.

The library separates mechanically defensible norm checks from contextual
Russian-usage candidates. It deliberately does not infer a heading merely from
its meaning: heading punctuation is licensed by structural/typographic
rubrication, while an unmarked plain-text pseudoheading is only a soft editing
candidate.
"""
from __future__ import annotations

import re
from typing import Any

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
CYRILLIC_WORD_RE = re.compile(r"[А-Яа-яЁё-]+")
LATIN_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z'-]{1,})(?![A-Za-z0-9_])")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
MD_LINK_TARGET_RE = re.compile(r"\]\([^\n)]*\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(?P<body>.+?)\s*$")
LIST_RE = re.compile(
    r"^\s*(?P<marker>(?:[-*+]|(?:\d+|[А-Яа-яA-Za-z])[.)]))\s+(?P<body>.+?)\s*$"
)
SPLIT_CONTRAST_RE = re.compile(
    r"\bЭто\s+не\s+(?P<left>[^.!?\n]{1,160})\.\s+Это\s+(?P<right>[^.!?\n]{1,160})(?P<end>[.!?])",
    re.I,
)

# Tiny high-precision ontology for one mechanically useful semantic candidate.
# General category/container collisions stay MODEL_ONLY.
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
    """Return all non-fenced lines, including blanks needed for rubrication."""
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


def _plain_inline_text(text: str) -> str:
    """Drop a few Markdown emphasis markers without pretending to parse Markdown."""
    return re.sub(r"[*_~]+", "", text).strip()


def _first_cyrillic_letter(text: str) -> str:
    match = CYRILLIC_RE.search(_plain_inline_text(text))
    return match.group(0) if match else ""


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
        "Строка структурно размечена как заголовок: финальную точку в вынесенной рубрике опускают; ? ! … сохраняются.",
        "remove_terminal_period_from_marked_heading",
        reviewer_id=None,
    )


def _next_nonblank(visible: list[tuple[int, str]], index: int) -> tuple[int, str] | None:
    for item in visible[index + 1 :]:
        if item[1].strip():
            return item
    return None


def _unmarked_heading_finding(
    visible: list[tuple[int, str]], index: int
) -> dict[str, Any] | None:
    """Surface only high-ish-signal pseudoheadings; never call them NORM errors."""
    line_no, raw = visible[index]
    clean = _plain_inline_text(_mask_inline(raw))
    if not clean or HEADING_RE.match(raw) or LIST_RE.match(raw):
        return None
    if raw.lstrip().startswith((">", "|")):
        return None
    if clean.endswith((".", "?", "!", "…", ":", ";", ",")):
        return None
    words = CYRILLIC_WORD_RE.findall(clean)
    if not 2 <= len(words) <= 10:
        return None
    first = _first_cyrillic_letter(clean)
    if not first or not first.isupper():
        return None
    prev_blank = index == 0 or not visible[index - 1][1].strip()
    if not prev_blank:
        return None
    following = _next_nonblank(visible, index)
    if not following:
        return None
    following_clean = _plain_inline_text(_mask_inline(following[1]))
    # Requiring a substantial following line avoids treating a stack of labels
    # as prose headings. It remains an EXTENDED_SOFT candidate because plain
    # text can intentionally use captions, titles and UI labels.
    if len(CYRILLIC_WORD_RE.findall(following_clean)) < 5:
        return None
    return _finding(
        "RU-STYLE-UNMARKED-HEADING",
        "russian.unmarked_heading_candidate",
        "EDITING",
        "EXTENDED_SOFT",
        "REVIEW",
        clean,
        line_no,
        "Строка выглядит как рубрика по функции, но в plain text ничем не размечена. Либо оформите её настоящим заголовком средствами целевого формата, либо включите в обычный текст и пунктуируйте как предложение.",
        "mark_as_heading_or_punctuate_as_sentence",
    )


def _list_groups(visible: list[tuple[int, str]]) -> list[list[tuple[int, str, re.Match[str]]]]:
    groups: list[list[tuple[int, str, re.Match[str]]]] = []
    current: list[tuple[int, str, re.Match[str]]] = []
    previous_line = None
    for line_no, raw in visible:
        match = LIST_RE.match(raw)
        if match and (previous_line is None or line_no == previous_line + 1):
            current.append((line_no, raw, match))
        elif match:
            if current:
                groups.append(current)
            current = [(line_no, raw, match)]
        else:
            if current:
                groups.append(current)
                current = []
        previous_line = line_no
    if current:
        groups.append(current)
    return [group for group in groups if len(group) >= 2]


def _list_findings(visible: list[tuple[int, str]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for group in _list_groups(visible):
        for index, (line_no, raw, match) in enumerate(group):
            marker = match.group("marker")
            body = _plain_inline_text(match.group("body"))
            first = _first_cyrillic_letter(body)
            if not first:
                continue
            terminal = body[-1:] if body else ""
            dot_marker = marker.endswith(".")
            is_last = index == len(group) - 1

            # A number/letter followed by a dot introduces a capitalized rubric.
            if dot_marker and first.islower():
                findings.append(_finding(
                    "RU-NORM-LIST-DOT-MARKER-CAPITAL",
                    "norm.list_marker_case_alignment",
                    "NORM",
                    "DEFAULT_MECHANICAL",
                    "CHANGE",
                    raw.strip(),
                    line_no,
                    "После номера/литеры с точкой рубрика начинается с прописной буквы и оформляется как самостоятельный пункт.",
                    "capitalize_item_after_dot_marker_and_end_with_period",
                    reviewer_id=None,
                ))
                continue
            if dot_marker and first.isupper() and terminal in {",", ";"}:
                findings.append(_finding(
                    "RU-NORM-LIST-DOT-MARKER-CAPITAL",
                    "norm.list_marker_case_alignment",
                    "NORM",
                    "DEFAULT_MECHANICAL",
                    "CHANGE",
                    raw.strip(),
                    line_no,
                    "Пункт, введённый номером/литерой с точкой и начатый с прописной, обычно завершается точкой, а не запятой или точкой с запятой.",
                    "end_dot_marker_item_as_sentence",
                    reviewer_id=None,
                ))
                continue

            if dot_marker:
                continue

            # Bullets and parenthesized markers normally form a lowercase
            # continuation. We only surface mismatches; proper-name initials and
            # the final full stop of the entire enumeration are protected.
            if first.islower() and not is_last and terminal == ".":
                findings.append(_finding(
                    "RU-LIST-CASE-PUNCTUATION-CONSISTENCY",
                    "russian.list_case_punctuation_alignment",
                    "EDITING",
                    "EXTENDED_SOFT",
                    "REVIEW",
                    raw.strip(),
                    line_no,
                    "Строчный пункт внутри продолжающегося перечня обычно отделяется запятой или точкой с запятой; точка делает его самостоятельным предложением и требует другой схемы списка.",
                    "align_list_case_marker_and_terminal_punctuation",
                ))
            elif first.islower() and not is_last and terminal not in {",", ";", ":"}:
                findings.append(_finding(
                    "RU-LIST-CASE-PUNCTUATION-CONSISTENCY",
                    "russian.list_case_punctuation_alignment",
                    "EDITING",
                    "EXTENDED_SOFT",
                    "REVIEW",
                    raw.strip(),
                    line_no,
                    "У строчного пункта продолжающегося перечня нет разделительного знака. Для простого пункта возможна запятая, для более сложного обычно нужна точка с запятой.",
                    "align_list_case_marker_and_terminal_punctuation",
                ))
            elif first.isupper() and terminal in {",", ";"}:
                findings.append(_finding(
                    "RU-LIST-CASE-PUNCTUATION-CONSISTENCY",
                    "russian.list_case_punctuation_alignment",
                    "EDITING",
                    "EXTENDED_SOFT",
                    "REVIEW",
                    raw.strip(),
                    line_no,
                    "Прописная буква вместе с запятой/точкой с запятой смешивает две схемы оформления. Проверьте: либо самостоятельные пункты с прописной и точкой, либо синтаксически продолжающийся перечень со строчной. Имя собственное — исключение.",
                    "align_list_case_marker_and_terminal_punctuation",
                ))
    return findings


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
    for index in range(len(visible)):
        item = _unmarked_heading_finding(visible, index)
        if item:
            findings.append(item)
    findings.extend(_list_findings(visible))

    for line_no, raw in visible:
        clean = _mask_inline(raw)
        heading = HEADING_RE.match(clean)
        if heading:
            clean = heading.group("body")
        list_match = LIST_RE.match(clean)
        if list_match:
            clean = list_match.group("body")
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
        if HEADING_RE.match(raw) or LIST_RE.match(raw):
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

    model_only = [
        "RU-SEM-CATEGORY-COLLECTION",
        "RU-NORM-GERUND-SUBJECT-ATTACHMENT",
        "RU-NATIVE-GERUND-FRAME-POSITION",
        "RU-NORM-PARTICIPLE-HEAD-ATTACHMENT",
        "RU-NATIVE-PARTICIPIAL-COMPRESSION",
        "RU-RKI-SYNTACTIC-INTERFERENCE-AUDIT",
    ]
    return {
        "findings": findings,
        "metrics": {
            "register": register,
            "russian_language_findings": len(findings),
            "model_only_rules": model_only,
        },
    }


def self_test() -> None:
    cases = [
        ("# Заголовок.\nТекст.", "RU-NORM-HEADING-PERIOD", False),
        ("Это не реальная рецензия. Это оценка по правилам.", "RU-NATIVE-SPLIT-CONTRAST", False),
        ("Книги — это библиотеки знаний.", "RU-SEM-MEMBER-COLLECTION-EQUATION", False),
        ("Мы используем prompt только для остатка.", "RU-REGISTER-JARGON-TERM", False),
        ("Мы используем prompt только для остатка.", "RU-LEX-LATIN-IN-RUSSIAN", False),
        ("Это обычный russianword в русской фразе.", "RU-LEX-LATIN-IN-RUSSIAN", False),
        ("1. первый пункт\n2. Второй пункт.", "RU-NORM-LIST-DOT-MARKER-CAPITAL", False),
        ("\nКниги как сборники правил\nНовая книга превращается в набор проверяемых и контекстных правил.", "RU-STYLE-UNMARKED-HEADING", False),
        ("- первый пункт.\n- второй пункт.", "RU-LIST-CASE-PUNCTUATION-CONSISTENCY", False),
    ]
    for text, rule, _ in cases:
        rows = review(text, {"register": "everyday"})["findings"]
        assert any(item["rule_id"] == rule for item in rows), (text, rule, rows)

    clean = review(
        "# Заголовок\nЭто не ошибка, а предупреждение.\nКниги хранятся в библиотеках.\n\n- первый пункт;\n- второй пункт.",
        {"register": "everyday"},
    )["findings"]
    forbidden = {
        "RU-NORM-HEADING-PERIOD",
        "RU-NATIVE-SPLIT-CONTRAST",
        "RU-SEM-MEMBER-COLLECTION-EQUATION",
        "RU-LIST-CASE-PUNCTUATION-CONSISTENCY",
    }
    assert not any(item["rule_id"] in forbidden for item in clean), clean


if __name__ == "__main__":
    self_test()
    print("Russian language layer: OK")
