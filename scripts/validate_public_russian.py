#!/usr/bin/env python3
"""Проверяет русскоязычную пользовательскую оболочку без ложных срабатываний на код и лицензии."""
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
    "preserve when",
    "counterexample:",
    "guard:",
    "operation:",
    "current norm",
    "runtime boundary",
    "legacy aliases",
    "stance profile",
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
)

PUBLIC_MARKDOWN = (
    "README.md",
    "SKILL.md",
    "BOARD_SKILL.md",
    "INSTALL.md",
    "PROJECT_STATUS.md",
    "CONTRIBUTING.md",
    "MIGRATION.md",
    "gpt/INSTRUCTIONS.md",
    "gpt/PACKAGE.md",
    "gpt/SETUP.md",
    "gpt/TESTS.md",
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
    allowed_machine_names = re.compile(r"^humanizer-russian(?:-[a-z0-9]+)*$")
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = raw.strip()
            if not (stripped.startswith("name:") or stripped.startswith("- name:")):
                continue
            value = stripped.split(":", 1)[1].strip().strip("'\"")
            if not value or has_cyrillic(value) or allowed_machine_names.fullmatch(value):
                continue
            errors.append(
                f"{path.relative_to(ROOT)}:{lineno}: видимое имя workflow/шага не русское: {value!r}"
            )


def visible_lines(path: Path):
    in_fence = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
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
        or bool(re.search(r"\b(19|20)\d{2}\b", raw))
    )


def check_markdown(errors: list[str], paths: list[Path], root: Path = ROOT) -> None:
    for path in paths:
        if path.name in {"LICENSE", "THIRD_PARTY_NOTICES.md"}:
            continue
        rel = path.relative_to(root)
        for lineno, raw in visible_lines(path):
            text = normalized_visible_text(raw)
            if not text:
                continue
            lowered = text.lower()
            for fragment in FORBIDDEN_FRAGMENTS:
                if fragment in lowered:
                    errors.append(f"{rel}:{lineno}: английский редакторский фрагмент: {fragment!r}")
            if has_cyrillic(text) or looks_like_bibliography(raw):
                continue
            if text.startswith("|") or text.startswith(">"):
                continue
            words = LATIN_WORD.findall(text)
            if text.lstrip().startswith("#") and len(words) >= 2:
                allowed_heading = text.strip("# ") in {"GPT Builder", "Custom GPT", "humanizer_russian"}
                if not allowed_heading:
                    errors.append(f"{rel}:{lineno}: англоязычный заголовок: {text!r}")
            elif len(words) >= 8:
                errors.append(f"{rel}:{lineno}: англоязычная проза: {text!r}")


def check_public_markdown(errors: list[str]) -> None:
    paths = [ROOT / rel for rel in PUBLIC_MARKDOWN if (ROOT / rel).is_file()]
    check_markdown(errors, paths)


def check_generated_gpt(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="humanizer-public-russian-") as td:
        dest = Path(td) / package_gpt.PACKAGE_ROOT
        package_gpt.build_directory(dest)
        user_surface = [
            dest / "README.md",
            dest / "Instructions/INSTRUCTIONS.md",
            dest / "Instructions/GPT_BUILDER.md",
            dest / "Instructions/CONVERSATION_STARTERS.md",
            dest / "Instructions/TESTS.md",
            dest / "Knowledge/00_INDEX.md",
        ]
        local_errors: list[str] = []
        check_markdown(local_errors, [p for p in user_surface if p.is_file()], dest)
        errors.extend(f"generated-gpt/{item}" for item in local_errors)


def main() -> None:
    errors: list[str] = []
    check_json_surfaces(errors)
    check_workflow_names(errors)
    check_public_markdown(errors)
    check_generated_gpt(errors)

    if errors:
        print("Проверка русскоязычной публичной оболочки: найдены проблемы")
        for item in errors:
            print(f"- {item}")
        raise SystemExit(1)

    print("Проверка русскоязычной публичной оболочки: OK")


if __name__ == "__main__":
    main()
