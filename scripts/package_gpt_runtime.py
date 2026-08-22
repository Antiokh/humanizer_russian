#!/usr/bin/env python3
"""Build the full Custom GPT package with the deterministic Python runtime."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

import package_gpt
import package_skill

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = package_gpt.PACKAGE_ROOT
MAX_UPLOAD_FILES = 20


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _build_embedded_skill() -> tuple[bytes, dict]:
    with tempfile.TemporaryDirectory(prefix="humanizer-gpt-runtime-") as td:
        path = Path(td) / "humanizer-russian.zip"
        result = package_skill.build_package(path)
        return path.read_bytes(), result


def _launcher(payload: bytes, result: dict) -> str:
    encoded = base64.b85encode(payload).decode("ascii")
    chunks = "\n".join(f"    {encoded[i:i+100]!r}" for i in range(0, len(encoded), 100))
    return f'''#!/usr/bin/env python3
"""Self-contained humanizer_russian runtime for Custom GPT Code Interpreter.
Generated from the same skill-package.json allowlist as the Agent Skill ZIP.
"""
from __future__ import annotations
import argparse, base64, hashlib, io, json, py_compile, subprocess, sys, tempfile, zipfile
from pathlib import Path

SKILL_NAME = "humanizer-russian"
SKILL_VERSION = {str(result.get("skill_version") or "unversioned")!r}
PAYLOAD_SHA256 = {str(result["sha256"])!r}
FILE_COUNT = {int(result["file_count"])}
_PAYLOAD = (\n{chunks}\n)
ENTRYPOINTS = {{
    "check": "scripts/check.py",
    "review": "scripts/review.py",
    "lint": "scripts/lint.py",
    "lint-native": "scripts/lint_native.py",
    "lint-russian": "scripts/lint_russian.py",
    "lint-russian-all": "scripts/lint_russian_all.py",
    "lint-russian-calques": "scripts/lint_russian_calques.py",
    "lint-russian-rki-metrics": "scripts/lint_russian_rki_metrics.py",
    "lint-chukovsky": "scripts/lint_chukovsky.py",
    "lint-ilyakhov": "scripts/lint_ilyakhov.py",
    "lint-gal": "scripts/lint_gal.py",
    "lint-visson": "scripts/lint_visson.py",
    "lint-rosenthal": "scripts/lint_rosenthal.py",
    "lint-golub": "scripts/lint_golub.py",
    "editorial-board": "scripts/editorial_board.py",
    "evidence-runtime": "scripts/evidence_runtime.py",
    "profile-author": "scripts/profile_author.py",
}}

def payload_bytes():
    data = base64.b85decode("".join(_PAYLOAD))
    if hashlib.sha256(data).hexdigest() != PAYLOAD_SHA256:
        raise RuntimeError("embedded runtime hash mismatch")
    return data

def extract(dest: Path) -> Path:
    root = dest.resolve()
    with zipfile.ZipFile(io.BytesIO(payload_bytes()), "r") as zf:
        for info in zf.infolist():
            target = (dest / info.filename).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"unsafe embedded path: {{info.filename}}")
            if info.is_dir():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))
    skill = dest / SKILL_NAME
    if not skill.is_dir():
        raise RuntimeError("embedded skill root missing")
    return skill

def verify(skill: Path) -> dict:
    manifest = json.loads((skill / "_package/manifest.json").read_text(encoding="utf-8"))
    rows = manifest.get("files", [])
    if len(rows) != FILE_COUNT:
        raise RuntimeError("embedded file count mismatch")
    compiled = 0
    for row in rows:
        path = skill / row["path"]
        data = path.read_bytes()
        if len(data) != int(row["size"]) or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise RuntimeError(f"embedded file integrity failure: {{row['path']}}")
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
            compiled += 1
    return {{"skill": SKILL_NAME, "version": SKILL_VERSION, "files_verified": len(rows),
             "python_files_compiled": compiled, "entrypoints": sorted(ENTRYPOINTS),
             "payload_sha256": PAYLOAD_SHA256}}

def main() -> int:
    p = argparse.ArgumentParser(description="humanizer_russian runtime")
    p.add_argument("command", choices=[*sorted(ENTRYPOINTS), "list", "verify", "extract"])
    p.add_argument("args", nargs=argparse.REMAINDER)
    ns = p.parse_args()
    if ns.command == "list":
        print(json.dumps({{"skill": SKILL_NAME, "version": SKILL_VERSION,
                          "entrypoints": ENTRYPOINTS, "payload_sha256": PAYLOAD_SHA256}},
                         ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if ns.command == "extract":
        target = Path(ns.args[0] if ns.args else "humanizer-russian-runtime").resolve()
        target.mkdir(parents=True, exist_ok=True)
        print(extract(target))
        return 0
    with tempfile.TemporaryDirectory(prefix="humanizer-runtime-") as td:
        skill = extract(Path(td))
        if ns.command == "verify":
            print(json.dumps(verify(skill), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        proc = subprocess.run([sys.executable, str(skill / ENTRYPOINTS[ns.command]), *ns.args], cwd=skill)
        return int(proc.returncode)
if __name__ == "__main__":
    raise SystemExit(main())
'''


def _builder(knowledge_count: int, upload_count: int) -> str:
    return f"""# GPT Builder setup

## Name
`humanizer_russian · Русский редактор`

## Description
Русский редактор: mechanical-first проверка, затем естественный русский без кальки с английского, с сохранением смысла, нормы, жанра и авторского голоса.

## Upload
1. Paste `Instructions/INSTRUCTIONS.md` into the GPT **Instructions** field.
2. Upload all **{knowledge_count}** `.md` files from `Knowledge/`.
3. Upload `Runtime/humanizer_runtime.py`.
4. Total package uploads: **{upload_count} / {MAX_UPLOAD_FILES}**.
5. Enable **Code Interpreter & Data Analysis**. It is required for the mechanical runtime.
6. Web Search is optional and should be used only for current facts or genuinely current/disputed language evidence.

## Mechanical runtime
For ordinary editing, save the user's text to a UTF-8 file and execute the uploaded runtime:

```bash
python3 humanizer_runtime.py check --json text.md
```

For deep audit:

```bash
python3 humanizer_runtime.py check --extended --json text.md
```

Self-check:

```bash
python3 humanizer_runtime.py verify
python3 humanizer_runtime.py list
```

The launcher embeds the complete supported Agent Skill runtime: `check`, `review`, generic `lint`, all current `lint-*` entrypoints, Editorial Board, author-profile runtime, normalized libraries, reviewers, styles, schemas and runtime data.

A non-zero `check` exit code can mean the checker found blocking findings. Read the JSON output; do not treat every non-zero exit as a runtime crash.

Only claim that a mechanical check ran when Code Interpreter actually executed `humanizer_runtime.py`. Evidence providers marked `PROJECT` remain unavailable.
"""


def _instructions() -> str:
    source = (ROOT / "gpt/INSTRUCTIONS.md").read_text(encoding="utf-8")
    boundary = """# Packaged mechanical runtime

This GPT package includes `humanizer_runtime.py` as an uploaded code file. With Code Interpreter & Data Analysis enabled, execute it before model-based editing.

- Ordinary pass: `python3 humanizer_runtime.py check --json text.md`.
- Deep pass: `python3 humanizer_runtime.py check --extended --json text.md`.
- Exit code 1/2 can represent findings; inspect stdout JSON before diagnosing failure.
- Say that mechanical checking ran only after the runtime actually executed.
- If the file or Code Interpreter is unavailable, say that the mechanical pass could not run and continue with model-only editing.
- `PROJECT` evidence providers are still unavailable.

---

"""
    return boundary + source


def _rebuild_manifest(dest: Path, base: dict, skill_result: dict, knowledge_count: int) -> dict:
    files = []
    for p in sorted(x for x in dest.rglob("*") if x.is_file() and x.name != "_manifest.json"):
        data = p.read_bytes()
        files.append({"path": p.relative_to(dest).as_posix(), "sha256": _sha256(data), "size": len(data)})
    manifest = {
        "schema_version": 2,
        "package": PACKAGE_ROOT,
        "skill_version": base["skill_version"],
        "knowledge_file_count": knowledge_count,
        "runtime_file_count": 1,
        "gpt_upload_file_count": knowledge_count + 1,
        "gpt_upload_file_limit": MAX_UPLOAD_FILES,
        "embedded_skill": {k: skill_result[k] for k in ("sha256", "bytes", "file_count")},
        "source_map": base.get("source_map", {}),
        "files": files,
    }
    (dest / "_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_directory(dest: Path) -> dict:
    base = package_gpt.build_directory(dest)
    runtime_dir = dest / "Runtime"
    runtime_dir.mkdir()
    payload, skill_result = _build_embedded_skill()
    (runtime_dir / "humanizer_runtime.py").write_text(_launcher(payload, skill_result), encoding="utf-8")

    knowledge = sorted((dest / "Knowledge").glob("*.md"))
    upload_count = len(knowledge) + 1
    if upload_count > MAX_UPLOAD_FILES:
        raise RuntimeError(f"GPT upload file limit exceeded: {upload_count} > {MAX_UPLOAD_FILES}")

    (dest / "Instructions/INSTRUCTIONS.md").write_text(_instructions(), encoding="utf-8")
    (dest / "Instructions/GPT_BUILDER.md").write_text(_builder(len(knowledge), upload_count), encoding="utf-8")
    index = dest / "Knowledge/00_INDEX.md"
    index.write_text(index.read_text(encoding="utf-8").rstrip() + "\n\n- Runtime upload: `Runtime/humanizer_runtime.py`\n", encoding="utf-8")
    (dest / "README.md").write_text(
        f"# humanizer_russian — full Custom GPT package\n\n"
        f"Version: `{base['skill_version']}`\n\n"
        f"Paste `Instructions/INSTRUCTIONS.md` into Instructions. Upload all {len(knowledge)} files from `Knowledge/` plus `Runtime/humanizer_runtime.py`: **{upload_count}/{MAX_UPLOAD_FILES} files**. Enable Code Interpreter & Data Analysis.\n\n"
        "The runtime is generated from the same `skill-package.json` allowlist as the Agent Skill distribution, so the GPT receives the complete supported mechanical checker/linter runtime rather than a hand-maintained subset.\n",
        encoding="utf-8",
    )
    return _rebuild_manifest(dest, base, skill_result, len(knowledge))


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        prefix = PACKAGE_ROOT + "/"
        runtime = prefix + "Runtime/humanizer_runtime.py"
        if runtime not in names:
            raise RuntimeError("runtime file missing")
        knowledge = [n for n in names if n.startswith(prefix + "Knowledge/") and n.endswith(".md")]
        runtime_files = [n for n in names if n.startswith(prefix + "Runtime/") and not n.endswith("/")]
        count = len(knowledge) + len(runtime_files)
        if count > MAX_UPLOAD_FILES:
            raise RuntimeError("GPT upload limit exceeded")
        manifest = json.loads(zf.read(prefix + "_manifest.json"))
        if manifest["gpt_upload_file_count"] != count:
            raise RuntimeError("manifest upload count mismatch")
        return {"archive": str(path), "sha256": _sha256(path.read_bytes()), "bytes": path.stat().st_size,
                "knowledge_files": len(knowledge), "runtime_files": len(runtime_files),
                "gpt_upload_files": count, "skill_version": manifest["skill_version"],
                "embedded_skill_files": manifest["embedded_skill"]["file_count"],
                "embedded_skill_sha256": manifest["embedded_skill"]["sha256"]}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=ROOT / "dist/humanizer-russian-gpts.zip")
    p.add_argument("--directory", type=Path)
    p.add_argument("--inspect", type=Path)
    ns = p.parse_args()
    if ns.inspect:
        print(json.dumps(inspect(ns.inspect), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    with tempfile.TemporaryDirectory(prefix="humanizer-gpts-full-") as td:
        build = Path(td) / PACKAGE_ROOT
        manifest = build_directory(build)
        digest = package_gpt.zip_directory(build, ns.output)
        if ns.directory:
            if ns.directory.exists():
                shutil.rmtree(ns.directory)
            shutil.copytree(build, ns.directory)
    result = inspect(ns.output)
    result["sha256"] = digest
    result["manifest_files"] = len(manifest["files"])
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
