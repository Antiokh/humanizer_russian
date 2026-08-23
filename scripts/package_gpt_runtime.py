#!/usr/bin/env python3
"""Собирает полный пакет Custom GPT с детерминированным Python-runtime."""
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
    chunks = "\n".join(
        f"    {encoded[i:i+100]!r}" for i in range(0, len(encoded), 100)
    )
    return f'''#!/usr/bin/env python3
"""Автономный runtime humanizer_russian для Custom GPT Code Interpreter.
Сгенерирован из того же белого списка skill-package.json, что и ZIP Agent Skill.
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
        raise RuntimeError("хеш встроенного runtime не совпадает")
    return data

def extract(dest: Path) -> Path:
    root = dest.resolve()
    with zipfile.ZipFile(io.BytesIO(payload_bytes()), "r") as zf:
        for info in zf.infolist():
            target = (dest / info.filename).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"небезопасный путь во встроенном пакете: {{info.filename}}")
            if info.is_dir():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))
    skill = dest / SKILL_NAME
    if not skill.is_dir():
        raise RuntimeError("корневой каталог встроенного skill не найден")
    return skill

def verify(skill: Path) -> dict:
    manifest = json.loads((skill / "_package/manifest.json").read_text(encoding="utf-8"))
    rows = manifest.get("files", [])
    if len(rows) != FILE_COUNT:
        raise RuntimeError("число встроенных файлов не совпадает с манифестом")
    compiled = 0
    for row in rows:
        path = skill / row["path"]
        data = path.read_bytes()
        if len(data) != int(row["size"]) or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise RuntimeError(f"нарушена целостность встроенного файла: {{row['path']}}")
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
            compiled += 1
    return {{"skill": SKILL_NAME, "version": SKILL_VERSION, "files_verified": len(rows),
             "python_files_compiled": compiled, "entrypoints": sorted(ENTRYPOINTS),
             "payload_sha256": PAYLOAD_SHA256}}

def main() -> int:
    p = argparse.ArgumentParser(description="runtime humanizer_russian")
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
    return f"""# Настройка GPT Builder

## Название
`humanizer_russian · Русский редактор`

## Описание
Русский редактор: сначала механическая проверка, затем естественный русский без кальки с английского, с сохранением смысла, нормы, жанра и авторского голоса.

## Что загрузить
1. Вставьте `Instructions/INSTRUCTIONS.md` в поле GPT **Instructions**.
2. Загрузите все **{knowledge_count}** файлов `.md` из `Knowledge/`.
3. Загрузите `Runtime/humanizer_runtime.py`.
4. Всего загрузок в пакете: **{upload_count} / {MAX_UPLOAD_FILES}**.
5. Включите **Code Interpreter & Data Analysis**. Он нужен для механического рабочего контура.
6. **Web Search** необязателен; используйте его только для актуальных фактов или действительно текущих и спорных языковых данных.

## Механический рабочий контур
Для обычной редактуры сохраните пользовательский текст в файл UTF-8 и запустите загруженный runtime:

```bash
python3 humanizer_runtime.py check --json text.md
```

Для глубокого аудита:

```bash
python3 humanizer_runtime.py check --extended --json text.md
```

Самопроверка:

```bash
python3 humanizer_runtime.py verify
python3 humanizer_runtime.py list
```

Запускатель содержит полный поддерживаемый runtime Agent Skill: `check`, `review`, общий `lint`, все текущие точки входа `lint-*`, редколлегию, рабочий контур авторского профиля, нормализованные библиотеки, профили рецензентов, стили, схемы и данные рабочего контура.

Ненулевой код завершения `check` может означать, что проверка нашла блокирующие замечания. Читайте JSON-вывод и не считайте любой ненулевой код падением runtime.

Утверждать, что механическая проверка выполнялась, можно только если Code Interpreter действительно запустил `humanizer_runtime.py`. Провайдеры доказательств со статусом `PROJECT` остаются недоступными.
"""


def _instructions() -> str:
    source = (ROOT / "gpt/INSTRUCTIONS.md").read_text(encoding="utf-8")
    boundary = """# Упакованный механический рабочий контур

Этот пакет GPT включает `humanizer_runtime.py` как загружаемый файл кода. Если включён Code Interpreter & Data Analysis, запускайте его до модельной редактуры.

- Обычный проход: `python3 humanizer_runtime.py check --json text.md`.
- Глубокий проход: `python3 humanizer_runtime.py check --extended --json text.md`.
- Коды завершения 1/2 могут означать найденные замечания; перед выводом о сбое проверьте JSON в stdout.
- Говорить, что механическая проверка выполнялась, можно только после реального запуска runtime.
- Если файл или Code Interpreter недоступны, прямо скажите, что механический проход не запустился, и продолжайте только модельную редактуру.
- Провайдеры доказательств со статусом `PROJECT` по-прежнему недоступны.

---

"""
    return boundary + source


def _rebuild_manifest(
    dest: Path, base: dict, skill_result: dict, knowledge_count: int
) -> dict:
    files = []
    for p in sorted(
        x for x in dest.rglob("*") if x.is_file() and x.name != "_manifest.json"
    ):
        data = p.read_bytes()
        files.append(
            {
                "path": p.relative_to(dest).as_posix(),
                "sha256": _sha256(data),
                "size": len(data),
            }
        )
    manifest = {
        "schema_version": 2,
        "package": PACKAGE_ROOT,
        "skill_version": base["skill_version"],
        "knowledge_file_count": knowledge_count,
        "runtime_file_count": 1,
        "gpt_upload_file_count": knowledge_count + 1,
        "gpt_upload_file_limit": MAX_UPLOAD_FILES,
        "embedded_skill": {
            k: skill_result[k] for k in ("sha256", "bytes", "file_count")
        },
        "source_map": base.get("source_map", {}),
        "files": files,
    }
    (dest / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_directory(dest: Path) -> dict:
    base = package_gpt.build_directory(dest)
    runtime_dir = dest / "Runtime"
    runtime_dir.mkdir()
    payload, skill_result = _build_embedded_skill()
    (runtime_dir / "humanizer_runtime.py").write_text(
        _launcher(payload, skill_result), encoding="utf-8"
    )

    knowledge = sorted((dest / "Knowledge").glob("*.md"))
    upload_count = len(knowledge) + 1
    if upload_count > MAX_UPLOAD_FILES:
        raise RuntimeError(
            f"Превышен лимит файлов GPT: {upload_count} > {MAX_UPLOAD_FILES}"
        )

    (dest / "Instructions/INSTRUCTIONS.md").write_text(
        _instructions(), encoding="utf-8"
    )
    (dest / "Instructions/GPT_BUILDER.md").write_text(
        _builder(len(knowledge), upload_count), encoding="utf-8"
    )
    index = dest / "Knowledge/00_INDEX.md"
    index.write_text(
        index.read_text(encoding="utf-8").rstrip()
        + "\n\n- Файл runtime для загрузки: `Runtime/humanizer_runtime.py`\n",
        encoding="utf-8",
    )
    (dest / "README.md").write_text(
        f"# humanizer_russian — полный пакет Custom GPT\n\n"
        f"Версия: `{base['skill_version']}`\n\n"
        f"Вставьте `Instructions/INSTRUCTIONS.md` в поле Instructions. Загрузите все {len(knowledge)} файлов из `Knowledge/` и `Runtime/humanizer_runtime.py`: **{upload_count}/{MAX_UPLOAD_FILES} файлов**. Включите Code Interpreter & Data Analysis.\n\n"
        "Runtime генерируется из того же белого списка `skill-package.json`, что и дистрибутив Agent Skill. Поэтому GPT получает полный поддерживаемый механический контур проверок и линтеров, а не вручную поддерживаемое подмножество.\n",
        encoding="utf-8",
    )
    return _rebuild_manifest(dest, base, skill_result, len(knowledge))


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        prefix = PACKAGE_ROOT + "/"
        runtime = prefix + "Runtime/humanizer_runtime.py"
        if runtime not in names:
            raise RuntimeError("файл runtime отсутствует")
        knowledge = [
            n
            for n in names
            if n.startswith(prefix + "Knowledge/") and n.endswith(".md")
        ]
        runtime_files = [
            n for n in names if n.startswith(prefix + "Runtime/") and not n.endswith("/")
        ]
        count = len(knowledge) + len(runtime_files)
        if count > MAX_UPLOAD_FILES:
            raise RuntimeError("превышен лимит загрузок GPT")
        manifest = json.loads(zf.read(prefix + "_manifest.json"))
        if manifest["gpt_upload_file_count"] != count:
            raise RuntimeError("число загрузок в манифесте не совпадает с архивом")
        return {
            "archive": str(path),
            "sha256": _sha256(path.read_bytes()),
            "bytes": path.stat().st_size,
            "knowledge_files": len(knowledge),
            "runtime_files": len(runtime_files),
            "gpt_upload_files": count,
            "skill_version": manifest["skill_version"],
            "embedded_skill_files": manifest["embedded_skill"]["file_count"],
            "embedded_skill_sha256": manifest["embedded_skill"]["sha256"],
        }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist/humanizer-russian-gpts.zip",
        help="путь к выходному ZIP-архиву",
    )
    p.add_argument(
        "--directory",
        type=Path,
        help="необязательный каталог для распакованного пакета",
    )
    p.add_argument(
        "--inspect",
        type=Path,
        help="проверить существующий пакет и завершить работу",
    )
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
