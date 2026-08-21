#!/usr/bin/env python3
"""Build a deterministic portable Agent Skill ZIP from the runtime allowlist."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_CONFIG = ROOT / "skill-package.json"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def skill_properties(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    props: dict[str, str] = {}
    in_metadata = False
    for raw in frontmatter.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            in_metadata = line == "metadata:"
            if ":" in line and not in_metadata:
                key, value = line.split(":", 1)
                props[key.strip()] = value.strip().strip('"\'')
        elif in_metadata and ":" in line:
            key, value = line.split(":", 1)
            props[f"metadata.{key.strip()}"] = value.strip().strip('"\'')
    name = props.get("name", "")
    description = props.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        raise ValueError(f"invalid Agent Skills name: {name!r}")
    if not description or len(description) > 1024:
        raise ValueError("SKILL.md description must contain 1..1024 characters")
    return props


def _safe_repo_path(relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError(f"unsafe package path: {relative!r}")
    path = (ROOT / Path(*rel.parts)).resolve()
    root = ROOT.resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"package path escapes repository: {relative!r}")
    return path


def collect_files(config: dict) -> list[tuple[str, Path]]:
    relative_paths: set[str] = set()
    for relative in [*config.get("root_files", []), *config.get("runtime_scripts", [])]:
        path = _safe_repo_path(str(relative))
        if not path.is_file():
            raise FileNotFoundError(f"required package file is missing: {relative}")
        if path.is_symlink():
            raise ValueError(f"symlinks are not allowed in skill packages: {relative}")
        relative_paths.add(PurePosixPath(str(relative)).as_posix())

    for relative_dir in config.get("runtime_directories", []):
        directory = _safe_repo_path(str(relative_dir))
        if not directory.is_dir():
            raise FileNotFoundError(f"required package directory is missing: {relative_dir}")
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            if path.is_symlink():
                raise ValueError(f"symlinks are not allowed in skill packages: {path}")
            if "__pycache__" in path.parts or path.name.endswith((".pyc", ".pyo")):
                continue
            relative_paths.add(path.relative_to(ROOT).as_posix())

    forbidden = tuple(str(x).rstrip("/") + "/" for x in config.get("forbidden_prefixes", []))
    violations = sorted(
        relative
        for relative in relative_paths
        if any(relative == prefix[:-1] or relative.startswith(prefix) for prefix in forbidden)
    )
    if violations:
        raise ValueError("forbidden development files entered skill package: " + ", ".join(violations))
    return [(relative, ROOT / relative) for relative in sorted(relative_paths)]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _zip_info(name: str, executable: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    mode = 0o755 if executable else 0o644
    info.external_attr = (mode & 0xFFFF) << 16
    info.create_system = 3
    return info


def build_package(output: Path) -> dict:
    config = load_json(PACKAGE_CONFIG)
    props = skill_properties(ROOT / "SKILL.md")
    skill_name = str(config.get("skill_name") or "")
    if skill_name != props["name"]:
        raise ValueError(
            f"skill-package.json skill_name {skill_name!r} != SKILL.md name {props['name']!r}"
        )

    files = collect_files(config)
    file_rows = []
    payloads: dict[str, bytes] = {}
    for relative, path in files:
        data = path.read_bytes()
        payloads[relative] = data
        file_rows.append({"path": relative, "sha256": _sha256(data), "size": len(data)})

    package_manifest = {
        "schema_version": 1,
        "skill_name": skill_name,
        "skill_version": props.get("metadata.version"),
        "format": "agent-skills-directory-zip",
        "files": file_rows,
        "excluded_features": config.get("excluded_features", []),
    }
    manifest_bytes = (json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for relative in sorted(payloads):
            arcname = f"{skill_name}/{relative}"
            archive.writestr(
                _zip_info(arcname, executable=relative.startswith("scripts/") and relative.endswith(".py")),
                payloads[relative],
            )
        archive.writestr(
            _zip_info(f"{skill_name}/_package/manifest.json"),
            manifest_bytes,
        )

    result = {
        "path": str(output),
        "skill_name": skill_name,
        "skill_version": props.get("metadata.version"),
        "file_count": len(file_rows),
        "sha256": _sha256(output.read_bytes()),
        "bytes": output.stat().st_size,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Build portable humanizer-russian Agent Skill ZIP")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "humanizer-russian.zip")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = build_package(args.output.resolve())
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"skill package: {result['path']} ({result['file_count']} files, "
            f"{result['bytes']} bytes, sha256={result['sha256']})"
        )


if __name__ == "__main__":
    main()
