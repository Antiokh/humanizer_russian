#!/usr/bin/env python3
"""Проверяет, что публичная человекочитаемая оболочка проекта остаётся русской."""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

import package_gpt

ROOT = Path(__file__).resolve().parents[1]
CYRILLIC = re.compile(r"[А-Яа-яЁё]")
LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z'-]{2,}\b")
INLINE_CODE = re.compile(r"`[^`]*`")
RAW_URL = re.compile(r"https?://\S+")
MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")

# Явные остатки английского редакторского метаязыка. Машинные идентификаторы,
# API-термины и названия продуктов сюда намеренно не входят.
FORBIDDEN_FRAGMENTS = (
    "operational reference",
    "runtime reference",
    "compact contextual reference",
    "global decision rule",
    "contextual checks",
    "hard ban",
    "auto-delete",
    "generic humanizer",
    "author layer",
    "native layer",
    "detector score",
    "anti-detection",
    "production rule",
    "negative controls",
    "runtime policy",
    "source status:",
    "source locator:",
    "preserve when",
    "counterexample:",
    "guard:",
    "operation:",
    "current norm",
    "runtime boundary",
    "legacy aliases",
    "stance profile",
    "copywriting-схем",
    "plain text",
    "soft finding",
    "rki-like interference audit",
    "operational locators",
    "generated from the canonical",
    "purpose:",
    "use this file as reference material",
    "what to upload",
    "important boundary",
    "conversation starters",
    "full custom gpt package",
    "runtime upload:",
    "mechanical runtime",
    "self-check:",
    "the launcher embeds",
    "only claim that",
    "build a deterministic custom gpt package",
    "this package configures a custom gpt",
)

PUBLIC_ROOT_FILES = (
    "README.md",
    "SKILL.md",
    "BOARD_SKILL.md",
    "INSTALL.md",
    "PROJECT_STATUS.md",
    "CONTRIBUTING.md",
    "MIGRATION.md",
)


def has_cyrillic(value: object) -> bool:
    return bool(CYRILLIC.search(str(value or "")))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_russian_field(errors: list[str], path: Path, payload: dict, field: str) -> None:
    value = payload.get(field)
    if value is None or value == "":
        return
    if not has_cyrillic(value):
        errors.append(f"{path.relative_to(ROOT)}: поле {field!r} не содержит кириллицы: {value!r}")


def check_json_surfaces(errors: list[str]) -> None:
    for path in sorted((ROOT / "reviewers").glob("*.json")):
        payload = load_json(path)
        for field in ("display_name", "short_label", "review_label", "disclaimer"):
            require_russian_field(errors, path, payload, field)

    for path in sorted((ROOT / "styles").glob("*.json")):
        payload = load_json(path)
        for field in ("display_name", "description"):
            require_russian_field(errors, path, payload, field)

    for path in sorted((ROOT / "libraries").glob("*/library.json")):
        payload = load_json(path)
        for field in ("display_name", "notes"):
            require_russian_field(errors, path, payload, field)

    for path in sorted((ROOT / "evidence").glob("*/provider.json")):
        payload = load_json(path)
        for field in ("display_name", "description"):
            require_russian_field(errors, path, payload, field)


def check_workflow_names(errors: list[str]) -> None:
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = raw.strip()
            if not (stripped.startswith("name:") or stripped.startswith("- name:")):
                continue
            value = stripped.split(":", 1)[1].strip().strip("'\"")
            if value and not has_cyrillic(value):
                errors.append(
                    f"{path.relative_to(ROOT)}:{lineno}: видимое имя workflow/шага не русское: {value!r}"
                )


def public_markdown_files() -> list[Path]:
    result: list[Path] = []
    for rel in PUBLIC_ROOT_FILES:
        path = ROOT / rel
        if path.is_file():
            result.append(path)
    result.extend(sorted((ROOT / "docs").glob("*.md")))
    result.extend(
        path
        for path in sorted((ROOT / "references").glob("*.md"))
        if path.name != "native-russian-user-context.md"
    )
    result.extend(sorted((ROOT / "gpt").glob("*.md")))
    result.extend(sorted((ROOT / "libraries").glob("**/*.md")))
    return result


def visible_lines(path: Path):
    in_fence = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield lineno, raw


def normalized_visible_text(raw: str) -> str:
    text = INLINE_CODE.sub("", raw)
    text = MD_LINK.sub(r"\1", text)
    text = RAW_URL.sub("", text)
    return text.strip()


def looks_like_bibliography(raw: str) -> bool:
    low = raw.lower()
    return (
        "http://" in low
        or "https://" in low
        or "doi:" in low
        or "isbn" in low
        or " et al" in low
        or bool(re.search(r"\b(19|20)\d{2}\b", raw))
    )


def check_markdown(errors: list[str], paths: list[Path], root: Path = ROOT) -> None:
    for path in paths:
        rel = path.relative_to(root)
        for lineno, raw in visible_lines(path):
            lowered = raw.lower()
            for fragment in FORBIDDEN_FRAGMENTS:
                if fragment in lowered:
                    errors.append(f"{rel}:{lineno}: английский редакторский фрагмент: {fragment!r}")

            text = normalized_visible_text(raw)
            if not text or has_cyrillic(text) or looks_like_bibliography(raw):
                continue
            if text.startswith("|") or text.startswith(">"):
                continue
            words = LATIN_WORD.findall(text)
            if text.lstrip().startswith("#") and len(words) >= 2:
                allowed_heading = text.strip("# ") in {
                    "GPT Builder",
                    "Custom GPT",
                    "humanizer_russian",
                }
                if not allowed_heading:
                    errors.append(f"{rel}:{lineno}: англоязычный заголовок: {text!r}")
            elif len(words) >= 6:
                errors.append(f"{rel}:{lineno}: англоязычная проза: {text!r}")


def check_generated_gpt(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="humanizer-public-russian-") as td:
        dest = Path(td) / package_gpt.PACKAGE_ROOT
        package_gpt.build_directory(dest)
        generated = sorted(dest.glob("**/*.md"))
        local_errors: list[str] = []
        check_markdown(local_errors, generated, dest)
        errors.extend(f"generated-gpt/{item}" for item in local_errors)


def main() -> None:
    errors: list[str] = []
    check_json_surfaces(errors)
    check_workflow_names(errors)
    check_markdown(errors, public_markdown_files())
    check_generated_gpt(errors)

    if errors:
        print("Проверка русскоязычной публичной оболочки: найдены проблемы")
        for item in errors:
            print(f"- {item}")
        raise SystemExit(1)

    print("Проверка русскоязычной публичной оболочки: OK")


if __name__ == "__main__":
    main()
