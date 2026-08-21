#!/usr/bin/env python3
"""Validate and install a packaged Agent Skill ZIP into a skills root."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _skill_name_from_text(text: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    frontmatter = text.split("---\n", 2)[1]
    for raw in frontmatter.splitlines():
        if raw.startswith("name:"):
            name = raw.split(":", 1)[1].strip().strip('"\'')
            if not NAME_RE.fullmatch(name) or len(name) > 64:
                raise ValueError(f"invalid Agent Skills name: {name!r}")
            return name
    raise ValueError("SKILL.md has no top-level name")


def _safe_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"unsafe archive path: {name!r}")
    if any(part in {"", "."} for part in path.parts):
        raise ValueError(f"invalid archive path: {name!r}")
    return path


def inspect_package(package: Path) -> tuple[str, dict, dict[str, bytes]]:
    with zipfile.ZipFile(package) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        if not infos:
            raise ValueError("skill package is empty")
        payloads: dict[str, bytes] = {}
        roots: set[str] = set()
        for info in infos:
            path = _safe_member(info.filename)
            roots.add(path.parts[0])
            unix_mode = (info.external_attr >> 16) & 0xFFFF
            if unix_mode & 0o170000 == 0o120000:
                raise ValueError(f"symlink entry is forbidden: {info.filename}")
            payloads[path.as_posix()] = archive.read(info)

    if len(roots) != 1:
        raise ValueError(f"skill package must contain exactly one root directory: {sorted(roots)}")
    root = next(iter(roots))
    skill_key = f"{root}/SKILL.md"
    manifest_key = f"{root}/_package/manifest.json"
    if skill_key not in payloads or manifest_key not in payloads:
        raise ValueError("skill package requires SKILL.md and _package/manifest.json")

    skill_name = _skill_name_from_text(payloads[skill_key].decode("utf-8"))
    if root != skill_name:
        raise ValueError(f"archive root {root!r} must match SKILL.md name {skill_name!r}")

    manifest = json.loads(payloads[manifest_key].decode("utf-8"))
    if manifest.get("skill_name") != skill_name:
        raise ValueError("package manifest skill_name does not match SKILL.md")
    rows = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        raise ValueError("package manifest has no files")
    expected = {str(row.get("path")): row for row in rows}
    packaged = {
        key.removeprefix(f"{root}/")
        for key in payloads
        if key != manifest_key
    }
    if set(expected) != packaged:
        missing = sorted(set(expected) - packaged)
        extra = sorted(packaged - set(expected))
        raise ValueError(f"package file inventory mismatch; missing={missing}, extra={extra}")
    for relative, row in expected.items():
        data = payloads[f"{root}/{relative}"]
        if row.get("sha256") != _sha256(data) or row.get("size") != len(data):
            raise ValueError(f"checksum/size mismatch: {relative}")
    return skill_name, manifest, payloads


def install(package: Path, dest_root: Path, *, force: bool = False) -> Path:
    skill_name, _manifest, payloads = inspect_package(package)
    dest_root.mkdir(parents=True, exist_ok=True)
    target = dest_root / skill_name
    if target.exists() and not force:
        raise FileExistsError(f"skill already exists: {target}; use --force to replace it")

    temp_parent = Path(tempfile.mkdtemp(prefix=f".{skill_name}-install-", dir=dest_root))
    staged = temp_parent / skill_name
    try:
        for archive_name, data in payloads.items():
            path = PurePosixPath(archive_name)
            relative = PurePosixPath(*path.parts[1:])
            destination = staged.joinpath(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            if relative.parts and relative.parts[0] == "scripts" and destination.suffix == ".py":
                destination.chmod(0o755)
        if _skill_name_from_text((staged / "SKILL.md").read_text(encoding="utf-8")) != skill_name:
            raise ValueError("installed SKILL.md changed during staging")
        if target.exists():
            shutil.rmtree(target)
        os.replace(staged, target)
    finally:
        shutil.rmtree(temp_parent, ignore_errors=True)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Install a packaged Agent Skill ZIP")
    parser.add_argument("package", type=Path)
    parser.add_argument("--dest-root", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--inspect", action="store_true", help="validate package without installing")
    args = parser.parse_args()

    package = args.package.resolve()
    if args.inspect:
        name, manifest, _payloads = inspect_package(package)
        print(
            json.dumps(
                {
                    "skill_name": name,
                    "skill_version": manifest.get("skill_version"),
                    "file_count": len(manifest.get("files", [])),
                    "excluded_features": manifest.get("excluded_features", []),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    target = install(package, args.dest_root.resolve(), force=args.force)
    print(target)


if __name__ == "__main__":
    main()
