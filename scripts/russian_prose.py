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


def _mask_preserving_newlines(value: str) -> str:
    return "".join(ch if ch in "\r\n" else " " for ch in value)


def _fence_parts(line: str) -> tuple[str, int, str] | None:
    match = FENCE_RE.match(line)
    if not match:
        return None
    marker = match.group("marker")
    return marker[0], len(marker), match.group("rest")


def mask_fenced(text: str) -> str:
    """Mask fenced Markdown regions while preserving exact offsets/newlines."""
    out: list[str] = []
    fence_char: str | None = None
    fence_len = 0

    for raw in text.splitlines(keepends=True):
        body = raw.rstrip("\r\n")
        parts = _fence_parts(body)
        if fence_char is None:
            if parts:
                fence_char, fence_len, _ = parts
                out.append(_mask_preserving_newlines(raw))
            else:
                out.append(raw)
            continue

        if parts:
            char, length, rest = parts
            closes = char == fence_char and length >= fence_len and not rest.strip()
            out.append(_mask_preserving_newlines(raw))
            if closes:
                fence_char = None
                fence_len = 0
            continue

        out.append(_mask_preserving_newlines(raw))

    return "".join(out)


def _mask_regex(text: str, pattern: re.Pattern[str]) -> str:
    return pattern.sub(lambda match: _mask_preserving_newlines(match.group(0)), text)


def mask_inline(line: str) -> str:
    """Mask inline non-prose spans on one line."""
    clean = INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)
    clean = URL_RE.sub(lambda m: " " * len(m.group(0)), clean)
    clean = MD_LINK_TARGET_RE.sub(lambda m: "]" + " " * (len(m.group(0)) - 1), clean)
    clean = HTML_COMMENT_RE.sub(lambda m: " " * len(m.group(0)), clean)
    return clean


def mask_nonprose(text: str) -> str:
    """Return same-length text with non-prose regions replaced by whitespace."""
    masked = mask_fenced(text)
    masked = _mask_regex(masked, HTML_COMMENT_RE)
    masked = _mask_regex(masked, INLINE_CODE_RE)
    masked = _mask_regex(masked, URL_RE)
    masked = MD_LINK_TARGET_RE.sub(
        lambda m: "]" + _mask_preserving_newlines(m.group(0)[1:]),
        masked,
    )
    assert len(masked) == len(text), (len(masked), len(text))
    return masked


def visible_lines(text: str) -> list[tuple[int, str]]:
    """Return non-fenced original lines with robust Markdown fence handling."""
    out: list[tuple[int, str]] = []
    fence_char: str | None = None
    fence_len = 0

    for line_no, raw in enumerate(text.splitlines(), start=1):
        parts = _fence_parts(raw)
        if fence_char is None:
            if parts:
                fence_char, fence_len, _ = parts
                continue
            out.append((line_no, raw))
            continue

        if parts:
            char, length, rest = parts
            if char == fence_char and length >= fence_len and not rest.strip():
                fence_char = None
                fence_len = 0
        # Every line inside the fence, including shorter inner markers, stays hidden.

    return out
