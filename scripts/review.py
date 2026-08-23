#!/usr/bin/env python3
"""Режим редколлегии с необязательными источниками дополнительных данных."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from editorial_board import build_board
from library_runtime import load_style, reviewer_profiles, run_libraries

REGISTER_LABELS = {
    "general": "общий",
    "everyday": "бытовой",
    "professional": "профессиональный",
    "technical": "технический",
}
STATUS_LABELS = {
    "SOURCE_CONFLICT": "конфликт источников",
    "SINGLE_REVIEW": "одно мнение",
    "CONSENSUS": "консенсус",
    "NO_ACTION": "без изменений",
    "MAJORITY": "большинство",
    "REVIEW": "нужна проверка",
}
VERDICT_LABELS = {
    "CHANGE": "изменить",
    "KEEP": "оставить",
    "REVIEW": "проверить",
    "CONFLICT": "конфликт",
}
RECOMMENDATION_LABELS = {
    **VERDICT_LABELS,
    "SHOW_ALTERNATIVES": "показать варианты",
}
EVIDENCE_DIRECTION_LABELS = {
    "SUPPORTS_KEEP": "в пользу сохранения",
    "SUPPORTS_CHANGE": "в пользу изменения",
    "CONTEXT": "контекст",
    "NEUTRAL": "нейтрально",
}
EVIDENCE_STATUS_LABELS = {
    "OK": "готово",
    "PROJECT": "проектный источник",
    "UNAVAILABLE": "недоступно",
    "ERROR": "ошибка",
    "SKIPPED": "пропущено",
}
PROJECT_CLASS_LABELS = {
    "ARTIFACT": "технический артефакт",
    "NORM": "норма русского языка",
    "NATIVE_USAGE": "естественное употребление",
    "EDITING": "редактура",
    "AI_CALQUE": "калька или машинный паттерн",
    "AUTHOR": "авторский голос",
}


def _label(mapping: dict[str, str], value: object) -> str:
    key = str(value or "")
    return mapping.get(key, key)


def _parse_evidence_arg(value):
    if value is None or value.strip().lower() in {"", "off", "none", "false", "0"}:
        return None
    if value.strip().lower() in {"auto", "all"}:
        return value.strip().lower()
    return [x.strip() for x in value.split(",") if x.strip()]


def run_review(
    text,
    style_id="neutral",
    library_ids=None,
    evidence_ids=None,
    register="general",
):
    style = load_style(style_id)
    findings, metrics = run_libraries(
        text,
        library_ids=library_ids,
        context={"mode": "editorial_board", "register": register, "style_id": style_id},
    )
    evidence = []
    evidence_status = []
    if evidence_ids is not None:
        from evidence_runtime import run_evidence

        evidence, evidence_status = run_evidence(
            text,
            evidence_ids,
            context={
                "findings": findings,
                "style_id": style_id,
                "library_ids": library_ids or "default",
                "register": register,
            },
        )
    board = build_board(findings, style, evidence=evidence)
    profiles = reviewer_profiles()
    used = sorted({f["reviewer_id"] for f in findings if f.get("reviewer_id")})
    return {
        "schema_version": 1,
        "mode": "editorial_board",
        "style": style,
        "register": register,
        "libraries": library_ids or "default",
        "evidence_request": evidence_ids or "off",
        "reviewers": {
            key: profiles.get(key, {"id": key, "display_name": key}) for key in used
        },
        "findings": findings,
        "metrics": metrics,
        "evidence": evidence,
        "evidence_status": evidence_status,
        "board": board,
    }


def render_markdown(report):
    register = _label(REGISTER_LABELS, report.get("register", "general"))
    lines = [
        "## Редколлегия humanizer_russian",
        "",
        f"Стиль: **{report['style']['display_name']}**. Регистр: **{register}**.",
        "",
    ]
    guardrails = report["board"]["guardrails"]
    if guardrails:
        lines += ["### Обязательные замечания", ""]
        for item in guardrails:
            project_class = _label(PROJECT_CLASS_LABELS, item.get("project_class"))
            rule_name = item.get("display_rule_ru") or item["rule_id"]
            lines.append(
                f"- **{project_class}** `{item['rule_id']}` — {rule_name}: "
                f"{item.get('excerpt', '')} — {item.get('reason', '')}"
            )
        lines.append("")

    for group in report["board"]["groups"]:
        display_names = []
        for finding in group["findings"]:
            name = finding.get("display_rule_ru")
            if name and name not in display_names:
                display_names.append(name)
        heading = " / ".join(display_names) if display_names else group["phenomenon_id"]
        lines += [
            f"### {heading}",
            "",
            f"Код: `{group['phenomenon_id']}`",
            f"Фрагмент: `{group.get('excerpt', '')}`",
            (
                "Итог коллегии: **"
                f"{_label(STATUS_LABELS, group['status'])} → "
                f"{_label(RECOMMENDATION_LABELS, group['recommendation'])}**"
            ),
            "",
        ]
        by = {}
        for finding in group["findings"]:
            by.setdefault(finding["reviewer_id"], []).append(finding)
        for reviewer_id, rows in by.items():
            name = report["reviewers"].get(reviewer_id, {}).get(
                "display_name", reviewer_id
            )
            verdict = _label(VERDICT_LABELS, group["reviewer_verdicts"][reviewer_id])
            lines.append(f"- **{name}: {verdict}**")
            for finding in rows:
                lines.append(f"  - {finding.get('reason') or finding['rule_id']}")
        if group.get("evidence"):
            lines.append("- **Дополнительные данные (не голос редактора):**")
            for item in group["evidence"]:
                direction = _label(
                    EVIDENCE_DIRECTION_LABELS, item.get("direction", "CONTEXT")
                )
                lines.append(
                    f"  - `{item.get('provider_id', 'evidence')}` / {direction}: "
                    f"{item.get('reason', '')}"
                )
        lines.append("")

    bad = [
        item
        for item in report.get("evidence_status", [])
        if item.get("status") != "OK"
    ]
    if bad:
        lines += ["### Статус дополнительных источников", ""]
        for item in bad:
            status = _label(EVIDENCE_STATUS_LABELS, item.get("status"))
            lines.append(
                f"- `{item['provider_id']}`: {status} — {item.get('message', '')}"
            )
        lines.append("")

    if not guardrails and not report["board"]["groups"]:
        lines.append("Механические библиотеки не нашли замечаний.")
    lines += [
        "",
        "_Имена авторов обозначают оценку по формализованным правилам источника, а не реальную рецензию или цитату автора._",
        "_Дополнительные источники дают данные для проверки, а не дополнительные голоса редколлегии._",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Редколлегия humanizer_russian для проверки русского текста"
    )
    parser.add_argument("file", nargs="?", help="файл с текстом; без файла читается stdin")
    parser.add_argument("--style", default="neutral", help="профиль редакторского стиля")
    parser.add_argument(
        "--libraries",
        help="список библиотек через запятую; по умолчанию используются активные",
    )
    parser.add_argument(
        "--register",
        choices=["general", "everyday", "professional", "technical"],
        default="general",
        help="регистр текста: general, everyday, professional или technical",
    )
    parser.add_argument(
        "--evidence",
        help="дополнительные источники: off (по умолчанию), auto, all или список идентификаторов через запятую",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="формат вывода: json или markdown",
    )
    args = parser.parse_args()
    text = (
        Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    )
    ids = (
        [x.strip() for x in args.libraries.split(",") if x.strip()]
        if args.libraries
        else None
    )
    evidence_ids = _parse_evidence_arg(args.evidence)
    report = run_review(
        text,
        style_id=args.style,
        library_ids=ids,
        evidence_ids=evidence_ids,
        register=args.register,
    )
    print(
        json.dumps(report, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(report),
        end="\n" if args.format == "json" else "",
    )


if __name__ == "__main__":
    main()
