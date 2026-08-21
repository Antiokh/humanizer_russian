#!/usr/bin/env python3
"""Build a deterministic Custom GPT package from the current repository.

The package is intentionally different from the Agent Skill package:
- Instructions/ contains text to configure GPT Builder.
- Knowledge/ contains <=20 text-forward files suitable for GPT Knowledge upload.
- executable runtime scripts are not included, because GPT Knowledge is reference
  material rather than an installation mechanism for the Python runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "humanizer-russian-gpts"
MAX_KNOWLEDGE_FILES = 20
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

REFERENCE_EXCLUDE = {
    "native-russian-user-context.md",  # development/source-study material
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def skill_version() -> str:
    text = read_text(ROOT / "SKILL.md")
    match = re.search(r"(?m)^version:\s*[\"']?([^\"'\n]+)", text)
    return match.group(1).strip() if match else "unversioned"


def existing(paths: Iterable[str]) -> list[Path]:
    result: list[Path] = []
    for rel in paths:
        path = ROOT / rel
        if path.is_file():
            result.append(path)
    return result


def all_files(rel_dir: str) -> list[Path]:
    base = ROOT / rel_dir
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*") if p.is_file())


def format_source(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    text = read_text(path)
    suffix = path.suffix.lower()
    if suffix == ".md":
        body = text
    elif suffix == ".json":
        body = f"```json\n{text.rstrip()}\n```\n"
    else:
        body = f"```text\n{text.rstrip()}\n```\n"
    return f"\n---\n\n## Source: `{rel}`\n\n{body}"


def write_bundle(path: Path, title: str, purpose: str, sources: Iterable[Path]) -> list[str]:
    unique = sorted({p.resolve(): p for p in sources}.values(), key=lambda p: p.relative_to(ROOT).as_posix())
    rels = [p.relative_to(ROOT).as_posix() for p in unique]
    body = [
        f"# {title}\n\n",
        "Generated from the canonical `humanizer_russian` repository.\n\n",
        f"Purpose: {purpose}\n\n",
        "Use this file as reference material. Behavioral priorities and workflow live in `Instructions/INSTRUCTIONS.md`.\n",
    ]
    for src in unique:
        body.append(format_source(src))
    path.write_text("".join(body).rstrip() + "\n", encoding="utf-8")
    return rels


def reference_files() -> list[Path]:
    base = ROOT / "references"
    if not base.exists():
        return []
    return sorted(
        p for p in base.glob("*.md")
        if p.name not in REFERENCE_EXCLUDE
    )


def select_refs(refs: list[Path], *needles: str) -> list[Path]:
    selected: list[Path] = []
    for p in refs:
        name = p.name.lower()
        if any(needle.lower() in name for needle in needles):
            selected.append(p)
    return selected


def make_instructions(out: Path) -> None:
    source = read_text(ROOT / "gpt" / "INSTRUCTIONS.md")
    boundary = """# Custom GPT runtime boundary\n\nThis package configures a Custom GPT. Files in `Knowledge/` are reference material, not an installed Python runtime.\n\n- Do not claim that `scripts/check.py`, `review.py`, a mechanical linter, or an evidence provider was executed unless an actual external runtime/action executed it and returned a result.\n- In this package, canonical mechanical rules are included as knowledge so they can inform model review, but that is not equivalent to deterministic execution.\n- Evidence providers marked `PROJECT` remain unavailable and must not be presented as operational.\n- Preserve the user's facts and intent before style optimization.\n\nThe knowledge bundle filenames used by this package are listed in `Knowledge/00_INDEX.md`.\n\n---\n\n"""
    out.write_text(boundary + source, encoding="utf-8")


def builder_guide() -> str:
    return """# GPT Builder setup\n\n## Name\n\n`humanizer_russian · Русский редактор`\n\n## Description\n\nРусский редактор: естественный русский без кальки с английского, с сохранением смысла, нормы, жанра и авторского голоса.\n\n## What to upload\n\n1. Open the GPT editor.\n2. Paste the entire contents of `Instructions/INSTRUCTIONS.md` into the GPT **Instructions** field.\n3. Upload every `.md` file from `Knowledge/` into **Knowledge**. Do not upload the `Instructions/` files as Knowledge.\n4. Keep **Code Interpreter & Data Analysis** enabled when you want the GPT to edit or return user files.\n5. Enable **Web Search** only when current facts or a disputed/current language norm need external verification.\n6. Test in Preview using `Instructions/TESTS.md`.\n\n## Important boundary\n\nThis Custom GPT package is the model/instruction/knowledge build. It does not install the repository's deterministic Python runtime. A GPT Action or another actual execution surface is required before the GPT may truthfully say that `check.py` or an evidence provider ran.\n\n## Updating\n\nRebuild this archive from the repository instead of hand-copying reference files. The builder groups canonical libraries into a GPT-compatible set that stays below the Knowledge file-count limit.\n"""


def conversation_starters() -> str:
    return """# Conversation starters\n\n1. Отредактируй текст: сохрани смысл и голос автора, убери кальки и неестественные конструкции.\n2. Проведи глубокий аудит русского текста: норма, естественность, редактура и возможные AI-кальки.\n3. Переведи на русский так, чтобы результат звучал как оригинальный русский текст, а не перевод с английского.\n4. Сравни исходник и редактуру и покажи только изменения, которые действительно улучшают текст.\n"""


def build_directory(dest: Path) -> dict:
    if dest.exists():
        shutil.rmtree(dest)
    instructions = dest / "Instructions"
    knowledge = dest / "Knowledge"
    instructions.mkdir(parents=True)
    knowledge.mkdir(parents=True)

    make_instructions(instructions / "INSTRUCTIONS.md")
    (instructions / "GPT_BUILDER.md").write_text(builder_guide(), encoding="utf-8")
    (instructions / "CONVERSATION_STARTERS.md").write_text(conversation_starters(), encoding="utf-8")
    shutil.copy2(ROOT / "gpt" / "TESTS.md", instructions / "TESTS.md")

    refs = reference_files()
    assigned: set[Path] = set()
    source_map: dict[str, list[str]] = {}

    def bundle(filename: str, title: str, purpose: str, sources: Iterable[Path]) -> None:
        src = [p for p in sources if p.is_file()]
        for p in src:
            if p.parent == ROOT / "references":
                assigned.add(p)
        source_map[filename] = write_bundle(knowledge / filename, title, purpose, src)

    bundle(
        "01_RUSSIAN_LANGUAGE.md",
        "Russian language norm and mechanical rules",
        "Norm, punctuation/grammar surfaces, RKI-derived checks, and canonical Russian library metadata.",
        select_refs(refs, "russian-language")
        + all_files("libraries/russian")
        + existing(["docs/anti-calque.md"]),
    )
    bundle(
        "02_NATIVE_RUSSIAN.md",
        "Native Russian usage",
        "Natural information structure, context economy, contrast, particles, ellipsis, and anti-calque guidance.",
        select_refs(refs, "native-russian")
        + all_files("libraries/native")
        + existing(["docs/context-economy.md", "docs/contrast.md"]),
    )
    bundle(
        "03_NORA_GAL.md",
        "Nora Gal editorial layer",
        "Semantic and literary editing guidance plus canonical Gal rule metadata and provenance maps.",
        select_refs(refs, "nora-gal") + all_files("libraries/gal"),
    )
    bundle(
        "04_CHUKOVSKY.md",
        "Korney Chukovsky editorial layer",
        "Russian prose and style guidance derived from the Chukovsky library.",
        select_refs(refs, "chukovsky") + all_files("libraries/chukovsky"),
    )
    bundle(
        "05_ILYAKHOV.md",
        "Maxim Ilyakhov editing layer",
        "Information-style heuristics, with warnings kept distinct from hard language errors.",
        select_refs(refs, "ilyakhov") + all_files("libraries/ilyakhov"),
    )
    bundle(
        "06_VISSON.md",
        "Lynn Visson translation layer",
        "Russian/English translation interference, information structure, and Visson-derived checks.",
        select_refs(refs, "visson") + all_files("libraries/visson"),
    )
    bundle(
        "07_ROSENTHAL.md",
        "Rosenthal normative/editorial layer",
        "Rosenthal-derived Russian norm and stylistic checks.",
        select_refs(refs, "rosenthal") + all_files("libraries/rosenthal"),
    )
    bundle(
        "08_GOLUB.md",
        "Golub stylistics layer",
        "Russian stylistics, lexical and syntactic editing checks from the Golub library.",
        select_refs(refs, "golub") + all_files("libraries/golub"),
    )
    bundle(
        "09_AUTHOR_PROFILE.md",
        "Author profile and idiollect",
        "How to preserve a confirmed author voice without copying mistakes.",
        select_refs(refs, "author-profile")
        + all_files("profiles")
        + existing(["docs/author-layer.md"]),
    )
    bundle(
        "10_AUDITS_AND_CORRECTIONS.md",
        "Rule audit, evidence audit, and corrections",
        "Regression knowledge, disputed-rule handling, evidence boundaries, and accumulated corrections.",
        select_refs(refs, "rule-audit", "evidence-audit")
        + existing(["knowledge/corrections.md"]),
    )
    bundle(
        "11_EDITORIAL_BOARD.md",
        "Editorial Board",
        "Reviewer roles and board-level synthesis guidance.",
        existing(["BOARD_SKILL.md"]) + [p for p in all_files("reviewers") if p.name != "_template.json"],
    )
    bundle(
        "12_STYLES.md",
        "Style profiles",
        "Available style profiles and their constraints.",
        all_files("styles"),
    )
    bundle(
        "13_CAPABILITIES_AND_STATUS.md",
        "Capabilities and project status",
        "What is operational, diagnostic, or PROJECT-only; prevents the GPT from claiming unavailable integrations.",
        existing(["docs/capabilities.md", "PROJECT_STATUS.md"]),
    )

    leftovers = [p for p in refs if p not in assigned]
    if leftovers:
        bundle(
            "14_ADDITIONAL_REFERENCE.md",
            "Additional runtime reference",
            "Reference material not covered by a dedicated editorial library bundle.",
            leftovers,
        )

    knowledge_files = sorted(knowledge.glob("*.md"))
    index_lines = [
        "# humanizer_russian Knowledge index\n\n",
        "Upload every `.md` file in this directory to the GPT Knowledge section.\n\n",
        "The files are reference material. Instructions and workflow rules live in `Instructions/INSTRUCTIONS.md`.\n\n",
    ]
    for p in knowledge_files:
        index_lines.append(f"- `{p.name}`\n")
    (knowledge / "00_INDEX.md").write_text("".join(index_lines), encoding="utf-8")

    knowledge_files = sorted(knowledge.glob("*.md"))
    if len(knowledge_files) > MAX_KNOWLEDGE_FILES:
        raise RuntimeError(
            f"Knowledge file limit exceeded: {len(knowledge_files)} > {MAX_KNOWLEDGE_FILES}"
        )

    if any("native-russian-user-context" in p.read_text(encoding="utf-8") for p in knowledge_files):
        raise RuntimeError("development-only native-russian-user-context leaked into GPT Knowledge")

    root_readme = f"""# humanizer_russian — Custom GPT package\n\nVersion: `{skill_version()}`\n\nThis archive is for configuring a **Custom GPT (GPTs)**, not for installing the Agent Skill runtime.\n\n- Paste `Instructions/INSTRUCTIONS.md` into the GPT Instructions field.\n- Upload all `{len(knowledge_files)}` Markdown files from `Knowledge/` into GPT Knowledge.\n- Use `Instructions/GPT_BUILDER.md` for the remaining Builder settings.\n- Use `Instructions/TESTS.md` in Preview before publishing.\n\nThe package intentionally excludes executable scripts, CI, evals, source-study corpora, and PROJECT evidence runtime code. Canonical rule data needed for model-based review is embedded into the Knowledge bundles.\n"""
    (dest / "README.md").write_text(root_readme, encoding="utf-8")
    shutil.copy2(ROOT / "LICENSE", dest / "LICENSE")
    if (ROOT / "THIRD_PARTY_NOTICES.md").exists():
        shutil.copy2(ROOT / "THIRD_PARTY_NOTICES.md", dest / "THIRD_PARTY_NOTICES.md")

    inventory = []
    for p in sorted(x for x in dest.rglob("*") if x.is_file() and x.name != "_manifest.json"):
        data = p.read_bytes()
        inventory.append({
            "path": p.relative_to(dest).as_posix(),
            "sha256": sha256_bytes(data),
            "size": len(data),
        })

    manifest = {
        "schema_version": 1,
        "package": "humanizer-russian-gpts",
        "skill_version": skill_version(),
        "knowledge_file_count": len(knowledge_files),
        "knowledge_file_limit": MAX_KNOWLEDGE_FILES,
        "source_map": source_map,
        "files": inventory,
    }
    (dest / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def zip_directory(source: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            rel = Path(PACKAGE_ROOT) / path.relative_to(source)
            info = zipfile.ZipInfo(rel.as_posix(), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return sha256_bytes(output.read_bytes())


def inspect_zip(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        if not names:
            raise RuntimeError("empty archive")
        prefix = PACKAGE_ROOT + "/"
        if any(not name.startswith(prefix) for name in names):
            raise RuntimeError("archive contains files outside package root")
        required = {
            f"{PACKAGE_ROOT}/Instructions/INSTRUCTIONS.md",
            f"{PACKAGE_ROOT}/Instructions/GPT_BUILDER.md",
            f"{PACKAGE_ROOT}/Knowledge/00_INDEX.md",
            f"{PACKAGE_ROOT}/README.md",
            f"{PACKAGE_ROOT}/_manifest.json",
        }
        missing = sorted(required - set(names))
        if missing:
            raise RuntimeError(f"missing required archive files: {missing}")
        knowledge = [
            n for n in names
            if n.startswith(f"{PACKAGE_ROOT}/Knowledge/") and n.endswith(".md")
        ]
        if len(knowledge) > MAX_KNOWLEDGE_FILES:
            raise RuntimeError("archive exceeds Custom GPT Knowledge file limit")
        manifest = json.loads(zf.read(f"{PACKAGE_ROOT}/_manifest.json"))
        if manifest["knowledge_file_count"] != len(knowledge):
            raise RuntimeError("manifest knowledge count does not match archive")
    return {
        "archive": str(path),
        "sha256": sha256_bytes(path.read_bytes()),
        "bytes": path.stat().st_size,
        "knowledge_files": len(knowledge),
        "skill_version": manifest["skill_version"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "humanizer-russian-gpts.zip",
        help="ZIP archive output path",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        help="optional directory to keep the unpacked package",
    )
    parser.add_argument("--inspect", type=Path, help="inspect an existing GPT package and exit")
    args = parser.parse_args()

    if args.inspect:
        print(json.dumps(inspect_zip(args.inspect), ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    with tempfile.TemporaryDirectory(prefix="humanizer-russian-gpts-") as td:
        build = Path(td) / PACKAGE_ROOT
        manifest = build_directory(build)
        digest = zip_directory(build, args.output)
        if args.directory:
            if args.directory.exists():
                shutil.rmtree(args.directory)
            shutil.copytree(build, args.directory)

    result = inspect_zip(args.output)
    result["sha256"] = digest
    result["manifest_files"] = len(manifest["files"])
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
