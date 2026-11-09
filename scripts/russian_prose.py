#!/usr/bin/env python3
"""Shared masking helpers for Russian prose-oriented mechanical checks.

The helpers preserve text length and line breaks where span/line mapping matters.
Markdown headings, lists and blockquotes remain prose: only non-prose payloads
(code, URLs, comments, link targets and fenced regions) are masked.
"""
from __future__ import annotations

import re

FENCE_RE = re.compile(r"^\s{0,3}(?P<marker>`{3,}|~{3,})(?P<rest>.*)$")
INLINE_CODE_RE = re.compile(r"(?P<ticks>`+)(?P<body>[^`\n]*?)(?P=ticks)")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
MD_LINK_TARGET_RE = re.compile(r"\]\([^\n)]*\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
BACKTICK_RUN_RE = re.compile(r"`+")


def _mask_preserving_newlines(value: str) -> str:
    return "".join(ch if ch in "\r\n" else " " for ch in value)


def _fence_parts(line: str) -> tuple[str, int, str] | None:
    match = FENCE_RE.match(line)
    if not match:
        return None
    marker = match.group("marker")
    rest = match.group("rest")
    # CommonMark forbids backticks in the info string of a backtick fence.
    # In particular, ```inline``` is inline code, not an opening block fence.
    if marker[0] == "`" and "`" in rest:
        return None
    return marker[0], len(marker), rest


def _code_span_closer(text: str, start: int, width: int) -> re.Match[str] | None:
    """Find a matching delimiter within the same Markdown inline block.

    An unmatched delimiter cannot consume code from another paragraph or
    from a new block. Soft-wrapped lines can still close a code span.
    """
    limit = len(text)
    newline = text.find("\n", start)
    while newline >= 0:
        line_start = newline + 1
        line_end = text.find("\n", line_start)
        line = text[line_start:line_end if line_end >= 0 else len(text)].rstrip("\r")
        if (not line.strip()
                or _fence_parts(line) is not None
                or re.match(r"^ {0,3}(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", line)
                or re.fullmatch(r" {0,3}(?:=+|-+)\s*", line)):
            limit = line_start
            break
        newline = line_end
    return next(
        (run for run in BACKTICK_RUN_RE.finditer(text, start, limit)
         if len(run.group()) == width),
        None,
    )


def mask_fenced(text: str) -> str:
    """Mask fenced Markdown regions without opening fences inside HTML/code spans.

    Markdown comments and code spans are tracked for fence recognition only;
    their actual masking is performed by _mask_code_and_comments afterwards.
    """
    out: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    in_comment = False
    inline_width = 0
    offset = 0

    for raw in text.splitlines(keepends=True):
        body = raw.rstrip("\r\n")
        parts = _fence_parts(body)
        if fence_char is not None:
            if parts:
                char, length, rest = parts
                if char == fence_char and length >= fence_len and not rest.strip():
                    fence_char = None
                    fence_len = 0
            out.append(_mask_preserving_newlines(raw))
            offset += len(raw)
            continue

        # A marker in a comment or multiline code span is ordinary content.
        if not in_comment and not inline_width and parts:
            fence_char, fence_len, _ = parts
            out.append(_mask_preserving_newlines(raw))
            offset += len(raw)
            continue

        out.append(raw)
        i = 0
        while i < len(raw):
            if in_comment:
                close = raw.find("-->", i)
                if close < 0:
                    break
                in_comment = False
                i = close + 3
            elif inline_width:
                match = BACKTICK_RUN_RE.search(raw, i)
                if not match:
                    break
                if len(match.group()) == inline_width:
                    inline_width = 0
                i = match.end()
            elif raw.startswith("<!--", i):
                in_comment = True
                i += 4
            elif raw[i] == "`":
                match = BACKTICK_RUN_RE.match(raw, i)
                assert match is not None
                width = len(match.group())
                # Unmatched delimiters are literal; do not suppress later fences.
                if _code_span_closer(text, offset + match.end(), width) is not None:
                    inline_width = width
                i = match.end()
            else:
                i += 1
        offset += len(raw)
    return "".join(out)


def _mask_indented_code(text: str) -> str:
    """Mask indentation-based Markdown code at block boundaries.

    This must run before HTML-comment detection: an indented literal '<!--'
    cannot start a comment that hides subsequent prose.
    """
    out: list[str] = []
    paragraph_open = False
    for raw in text.splitlines(keepends=True):
        body = raw.rstrip("\r\n")
        if not body.strip():
            paragraph_open = False
            out.append(raw)
            continue
        if not paragraph_open and (body.startswith("    ") or body.startswith("\t")):
            out.append(_mask_preserving_newlines(raw))
            continue
        out.append(raw)
        paragraph_open = not bool(re.match(
            r"^\s{0,3}(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", body
        ))
    return "".join(out)

def _mask_code_and_comments(text: str) -> str:
    """Mask inline code and HTML comments without losing offsets or newlines.

    Markdown code spans can contain newlines and unequal internal backtick runs.
    Comment delimiters within code (and code delimiters within comments) are inert.
    """
    chars = list(text)
    i = 0
    while i < len(text):
        if text.startswith("<!--", i):
            close = text.find("-->", i + 4)
            end = len(text) if close < 0 else close + 3
        elif text[i] == "`":
            opener = BACKTICK_RUN_RE.match(text, i)
            assert opener is not None
            width = len(opener.group())
            closer = _code_span_closer(text, opener.end(), width)
            if closer is None:
                i = opener.end()
                continue
            end = closer.end()
        else:
            i += 1
            continue
        chars[i:end] = [ch if ch in "\r\n" else " " for ch in text[i:end]]
        i = end
    return "".join(chars)


def _mask_regex(text: str, pattern: re.Pattern[str]) -> str:
    return pattern.sub(lambda match: _mask_preserving_newlines(match.group(0)), text)


def mask_inline(line: str) -> str:
    """Mask inline non-prose spans on one line."""
    clean = _mask_code_and_comments(line)
    clean = URL_RE.sub(lambda m: " " * len(m.group(0)), clean)
    clean = MD_LINK_TARGET_RE.sub(lambda m: "]" + " " * (len(m.group(0)) - 1), clean)
    return clean


def mask_nonprose(text: str) -> str:
    """Return same-length text with non-prose regions replaced by whitespace."""
    masked = mask_fenced(_mask_indented_code(text))
    masked = _mask_code_and_comments(masked)
    masked = _mask_regex(masked, URL_RE)
    masked = MD_LINK_TARGET_RE.sub(
        lambda m: "]" + _mask_preserving_newlines(m.group(0)[1:]),
        masked,
    )
    assert len(masked) == len(text), (len(masked), len(text))
    return masked


def visible_lines(text: str) -> list[tuple[int, str]]:
    """Return original lines outside fenced regions, sharing fence semantics."""
    masked = mask_fenced(text)
    original = text.splitlines()
    visible = masked.splitlines()
    assert len(original) == len(visible)
    return [
        (line_no, line)
        for line_no, (line, candidate) in enumerate(zip(original, visible), start=1)
        if not line.strip() or candidate.strip()
    ]
