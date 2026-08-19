#!/usr/bin/env python3
"""Aggregate normalized findings without erasing reviewer disagreement."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


def key_excerpt(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())[:180]


def group_findings(findings: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    guardrails = [f for f in findings if not f.get("reviewer_id") or f.get("project_class") in {"ARTIFACT", "NORM"}]
    review_findings = [f for f in findings if f not in guardrails]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for finding in review_findings:
        groups[(finding["phenomenon_id"], key_excerpt(finding.get("excerpt", "")))].append(finding)
    return guardrails, [build_group(items) for items in groups.values()]


def build_group(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_reviewer: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        by_reviewer[item["reviewer_id"]].append(item)

    verdicts = {}
    for reviewer, rows in by_reviewer.items():
        values = {row["verdict"] for row in rows}
        if "CHANGE" in values and "KEEP" in values:
            verdicts[reviewer] = "CONFLICT"
        elif "CHANGE" in values:
            verdicts[reviewer] = "CHANGE"
        elif "KEEP" in values:
            verdicts[reviewer] = "KEEP"
        else:
            verdicts[reviewer] = "REVIEW"

    visible = [v for v in verdicts.values() if v != "REVIEW"]
    if "CHANGE" in visible and "KEEP" in visible:
        status = "SOURCE_CONFLICT"
    elif len(verdicts) == 1:
        status = "SINGLE_REVIEW"
    elif visible and all(v == "CHANGE" for v in visible) and len(visible) == len(verdicts):
        status = "CONSENSUS"
    elif visible and all(v == "KEEP" for v in visible) and len(visible) == len(verdicts):
        status = "NO_ACTION"
    elif "CHANGE" in visible:
        status = "MAJORITY"
    elif "KEEP" in visible:
        status = "MAJORITY"
    else:
        status = "REVIEW"

    operations = [x.get("operation") for x in items if x.get("operation")]
    return {
        "phenomenon_id": items[0]["phenomenon_id"],
        "excerpt": items[0].get("excerpt", ""),
        "status": status,
        "reviewer_verdicts": verdicts,
        "operations": list(dict.fromkeys(operations)),
        "findings": items,
    }


def apply_style(groups: list[dict[str, Any]], style: dict[str, Any]) -> list[dict[str, Any]]:
    weights = style.get("reviewer_weights", {})
    policy = style.get("conflict_policy", "show_alternatives")
    for group in groups:
        score = 0.0
        for reviewer, verdict in group["reviewer_verdicts"].items():
            weight = float(weights.get(reviewer, 1.0))
            if verdict == "CHANGE":
                score += weight
            elif verdict == "KEEP":
                score -= weight
        group["style_score"] = round(score, 3)
        if group["status"] == "SOURCE_CONFLICT" and policy == "preserve_original":
            group["recommendation"] = "KEEP"
        elif group["status"] == "SOURCE_CONFLICT" and policy == "weighted_majority":
            group["recommendation"] = "CHANGE" if score > 0 else "KEEP" if score < 0 else "SHOW_ALTERNATIVES"
        elif group["status"] == "SOURCE_CONFLICT":
            group["recommendation"] = "SHOW_ALTERNATIVES"
        elif score > 0:
            group["recommendation"] = "CHANGE"
        elif score < 0:
            group["recommendation"] = "KEEP"
        else:
            group["recommendation"] = "REVIEW"
    return groups


def build_board(findings: list[dict[str, Any]], style: dict[str, Any]) -> dict[str, Any]:
    guardrails, groups = group_findings(findings)
    groups = apply_style(groups, style)
    return {
        "guardrails": guardrails,
        "groups": groups,
        "summary": {
            "guardrails": len(guardrails),
            "groups": len(groups),
            "consensus": sum(1 for g in groups if g["status"] == "CONSENSUS"),
            "conflicts": sum(1 for g in groups if g["status"] == "SOURCE_CONFLICT"),
        },
    }
