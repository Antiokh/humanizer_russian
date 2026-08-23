#!/usr/bin/env python3
"""Генерирует детерминированные публичные снимки возможностей из манифестов.

Сгенерированные файлы содержат только факты, которые репозиторий хранит
в машиночитаемом виде. Нарративные утверждения вроде «полностью прочитано»
не выводятся из числа правил; source_status копируется дословно из манифеста
владельца, если это поле есть.
"""
from __future__ import annotations

import argparse
import difflib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "capabilities.json"
MD_PATH = ROOT / "docs" / "capabilities.md"
AUTOMATION_LEVELS = (
    "HARD_GATE",
    "DEFAULT_MECHANICAL",
    "EXTENDED_SOFT",
    "METRIC_ONLY",
    "MODEL_ONLY",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rule_inventory(path: Path) -> dict[str, Any]:
    """Собирает карточки правил из прямого файла правил или сгруппированного индекса."""
    seen_paths: set[Path] = set()
    source_rules: list[dict[str, Any]] = []
    project_derived_rules: list[dict[str, Any]] = []

    def visit(current: Path) -> None:
        current = current.resolve()
        if current in seen_paths:
            return
        seen_paths.add(current)
        payload = load(current)
        direct = payload.get("rules", [])
        derived = payload.get("project_derived_rules", [])
        if direct:
            if not isinstance(direct, list):
                raise ValueError(f"{current.relative_to(ROOT)}: rules должен быть списком")
            source_rules.extend(direct)
        if derived:
            if not isinstance(derived, list):
                raise ValueError(
                    f"{current.relative_to(ROOT)}: project_derived_rules должен быть списком"
                )
            project_derived_rules.extend(derived)
        for relative in payload.get("groups", []):
            visit(ROOT / str(relative))

    visit(path)
    all_rules = source_rules + project_derived_rules
    ids = [str(item.get("rule_id") or "") for item in all_rules]
    missing_ids = [item for item, rule_id in zip(all_rules, ids) if not rule_id]
    duplicates = sorted(rule_id for rule_id, count in Counter(ids).items() if count > 1)
    if missing_ids:
        raise ValueError(f"{path.relative_to(ROOT)}: правило без rule_id")
    if duplicates:
        raise ValueError(
            f"{path.relative_to(ROOT)}: дублирующиеся идентификаторы правил: {', '.join(duplicates)}"
        )

    automation = Counter(str(item.get("automation_level") or "") for item in all_rules)
    unknown = sorted(level for level in automation if level not in AUTOMATION_LEVELS)
    if unknown:
        raise ValueError(
            f"{path.relative_to(ROOT)}: неизвестные уровни автоматизации: {', '.join(unknown)}"
        )

    root_payload = load(path)
    declared = root_payload.get("total_rule_count", root_payload.get("rule_count"))
    if declared is not None and not isinstance(declared, int):
        raise ValueError(f"{path.relative_to(ROOT)}: объявленное число правил должно быть целым")
    actual_count = len(all_rules)
    source_count = len(source_rules)
    if declared is not None and declared not in {actual_count, source_count}:
        raise ValueError(
            f"{path.relative_to(ROOT)}: объявлено {declared} правил, но это не совпадает "
            f"ни с числом правил источника {source_count}, ни с общим числом {actual_count}"
        )

    return {
        "rule_count": actual_count,
        "source_rule_count": source_count,
        "project_derived_rule_count": len(project_derived_rules),
        "declared_rule_count": declared,
        "source_cycles": root_payload.get("source_cycles"),
        "automation_counts": {
            level: automation.get(level, 0) for level in AUTOMATION_LEVELS
        },
    }


def build_snapshot() -> dict[str, Any]:
    manifests: list[dict[str, Any]] = []
    for path in sorted((ROOT / "libraries").glob("*/library.json")):
        if path.parent.name.startswith("_"):
            continue
        manifest = load(path)
        rules_path = manifest.get("rules_path")
        inventory = _rule_inventory(ROOT / rules_path) if rules_path else None
        manifests.append(
            {
                "id": manifest["id"],
                "display_name": manifest["display_name"],
                "source_type": manifest["source_type"],
                "reviewer_id": manifest["reviewer_id"],
                "adapter": manifest["adapter"],
                "enabled_by_default": bool(
                    manifest.get("enabled_by_default", False)
                ),
                "status": manifest.get("status"),
                "source_status": manifest.get("source_status"),
                "rules_path": rules_path,
                "rules": inventory,
                "model_eval": {
                    "registered": bool(
                        manifest.get("model_eval_path")
                        and manifest.get("model_eval_map_path")
                    ),
                    "suite_path": manifest.get("model_eval_path"),
                    "map_path": manifest.get("model_eval_map_path"),
                },
            }
        )

    manifests.sort(key=lambda item: item["id"])
    enabled = [item for item in manifests if item["enabled_by_default"]]

    reviewer_profiles: dict[str, dict[str, Any]] = {}
    for path in sorted((ROOT / "reviewers").glob("*.json")):
        if path.name.startswith("_"):
            continue
        profile = load(path)
        reviewer_profiles[profile["id"]] = profile
    active_reviewer_ids = sorted({item["reviewer_id"] for item in enabled})
    missing_profiles = sorted(set(active_reviewer_ids) - set(reviewer_profiles))
    if missing_profiles:
        raise ValueError(
            f"нет профилей активных рецензентов: {', '.join(missing_profiles)}"
        )

    providers: list[dict[str, Any]] = []
    for path in sorted((ROOT / "evidence").glob("*/provider.json")):
        if path.parent.name.startswith("_"):
            continue
        provider = load(path)
        providers.append(
            {
                "id": provider["id"],
                "status": provider["status"],
                "enabled_by_default": bool(provider["enabled_by_default"]),
            }
        )
    providers.sort(key=lambda item: item["id"])

    model_eval_ids = sorted(
        item["id"] for item in manifests if item["model_eval"]["registered"]
    )
    evidence_status_counts = Counter(item["status"] for item in providers)

    return {
        "schema_version": 1,
        "generated_by": "scripts/generate_capabilities.py",
        "summary": {
            "library_count": len(manifests),
            "enabled_library_count": len(enabled),
            "active_reviewer_count": len(active_reviewer_ids),
            "active_reviewer_ids": active_reviewer_ids,
            "model_eval_library_count": len(model_eval_ids),
            "model_eval_library_ids": model_eval_ids,
            "evidence_provider_count": len(providers),
            "evidence_status_counts": dict(sorted(evidence_status_counts.items())),
        },
        "libraries": manifests,
        "evidence_providers": providers,
    }


def render_json(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"


def _automation_text(rules: dict[str, Any] | None) -> str:
    if not rules:
        return "—"
    counts = rules["automation_counts"]
    short = {
        "HARD_GATE": "HARD",
        "DEFAULT_MECHANICAL": "DEFAULT",
        "EXTENDED_SOFT": "EXT",
        "METRIC_ONLY": "METRIC",
        "MODEL_ONLY": "MODEL",
    }
    return ", ".join(f"{short[level]}={counts[level]}" for level in AUTOMATION_LEVELS)


def render_markdown(snapshot: dict[str, Any]) -> str:
    summary = snapshot["summary"]
    lines = [
        "# Снимок возможностей проекта",
        "",
        "> Сгенерировано `scripts/generate_capabilities.py`. Не редактируйте этот файл вручную.",
        "",
        f"Включённых библиотек: **{summary['enabled_library_count']}**; активных рецензентов: "
        f"**{summary['active_reviewer_count']}**; библиотек с модельными проверками: "
        f"**{summary['model_eval_library_count']}**.",
        "",
        "Активные рецензенты: `" + "`, `".join(summary["active_reviewer_ids"]) + "`.",
        "",
        "## Библиотеки",
        "",
        "| Библиотека | Тип | Адаптер | Правила | Циклы источников | Автоматизация | Модельные проверки |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for item in snapshot["libraries"]:
        rules = item["rules"]
        rule_count = str(rules["rule_count"]) if rules else "—"
        source_cycles = (
            str(rules["source_cycles"])
            if rules and rules.get("source_cycles") is not None
            else "—"
        )
        model_eval = "да" if item["model_eval"]["registered"] else "нет"
        lines.append(
            f"| `{item['id']}` — {item['display_name']} | `{item['source_type']}` | "
            f"`{item['adapter']}` | {rule_count} | {source_cycles} | "
            f"{_automation_text(rules)} | {model_eval} |"
        )

    lines.extend(
        [
            "",
            "Столбец «Правила» считает канонические рабочие карточки, доступные через `rules_path`; "
            "проектные производные карточки включаются в число и отдельно отражаются в `capabilities.json`. "
            "Если число отсутствует, манифест библиотеки не задаёт `rules_path`.",
            "",
            "Полнота источника **не выводится** из числа правил. Если у библиотеки есть машиночитаемый "
            "`source_status`, его точное значение сохраняется в `capabilities.json`.",
            "",
            "## Источники дополнительных данных",
            "",
            "| Источник | Статус | Включён по умолчанию |",
            "|---|---|---|",
        ]
    )
    for provider in snapshot["evidence_providers"]:
        enabled = "да" if provider["enabled_by_default"] else "нет"
        lines.append(f"| `{provider['id']}` | `{provider['status']}` | {enabled} |")
    lines.append("")
    return "\n".join(lines)


def _check(path: Path, expected: str) -> bool:
    actual = path.read_text(encoding="utf-8") if path.is_file() else ""
    if actual == expected:
        return True
    print(f"сгенерированный снимок возможностей устарел: {path.relative_to(ROOT)}")
    for line in difflib.unified_diff(
        actual.splitlines(),
        expected.splitlines(),
        fromfile=str(path.relative_to(ROOT)),
        tofile=f"generated:{path.relative_to(ROOT)}",
        lineterm="",
    ):
        print(line)
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="завершиться ошибкой, если сохранённые снимки расходятся с манифестами репозитория",
    )
    args = parser.parse_args()

    snapshot = build_snapshot()
    json_text = render_json(snapshot)
    md_text = render_markdown(snapshot)
    if args.check:
        if not (_check(JSON_PATH, json_text) and _check(MD_PATH, md_text)):
            raise SystemExit(1)
        print("снимок возможностей актуален")
        return

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json_text, encoding="utf-8")
    MD_PATH.write_text(md_text, encoding="utf-8")
    print(f"записаны {JSON_PATH.relative_to(ROOT)} и {MD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
