#!/usr/bin/env python3
"""Aggregate normalized findings without erasing reviewer disagreement."""
from __future__ import annotations
import re
from collections import defaultdict
from typing import Any

def key_excerpt(text): return re.sub(r"\s+"," ",text.strip().lower())[:180]

def _evidence_matches_group(item,group):
    if item.get("phenomenon_id")!=group.get("phenomenon_id"): return False
    if item.get("target_scope","PHENOMENON")=="PHENOMENON": return True
    if item.get("target_scope")!="SPAN": return False
    line=int(item.get("line",0) or 0); group_lines={int(f.get("line",0) or 0) for f in group.get("findings",[]) if int(f.get("line",0) or 0)>0}
    if line>0 and line in group_lines: return True
    return bool(key_excerpt(item.get("excerpt","")) and key_excerpt(item.get("excerpt",""))==key_excerpt(group.get("excerpt","")))

def attach_evidence(groups,evidence=None):
    for group in groups:
        matched=[x for x in (evidence or []) if _evidence_matches_group(x,group)]; group["evidence"]=matched
        group["evidence_summary"]={"total":len(matched),"supports_keep":sum(x.get("direction")=="SUPPORTS_KEEP" for x in matched),"supports_change":sum(x.get("direction")=="SUPPORTS_CHANGE" for x in matched),"context":sum(x.get("direction")=="CONTEXT" for x in matched),"neutral":sum(x.get("direction")=="NEUTRAL" for x in matched)}
    return groups

def group_findings(findings):
    guardrails=[f for f in findings if not f.get("reviewer_id") or f.get("project_class") in {"ARTIFACT","NORM"}]; review=[f for f in findings if f not in guardrails]; groups=defaultdict(list)
    for f in review: groups[(f["phenomenon_id"],key_excerpt(f.get("excerpt","")))].append(f)
    return guardrails,[build_group(x) for x in groups.values()]

def build_group(items):
    by=defaultdict(list)
    for x in items: by[x["reviewer_id"]].append(x)
    verdicts={}
    for reviewer,rows in by.items():
        vals={r["verdict"] for r in rows}
        verdicts[reviewer]="CONFLICT" if {"CHANGE","KEEP"}<=vals else "CHANGE" if "CHANGE" in vals else "KEEP" if "KEEP" in vals else "REVIEW"
    visible=[v for v in verdicts.values() if v!="REVIEW"]
    if "CHANGE" in visible and "KEEP" in visible: status="SOURCE_CONFLICT"
    elif len(verdicts)==1: status="SINGLE_REVIEW"
    elif visible and all(v=="CHANGE" for v in visible) and len(visible)==len(verdicts): status="CONSENSUS"
    elif visible and all(v=="KEEP" for v in visible) and len(visible)==len(verdicts): status="NO_ACTION"
    elif "CHANGE" in visible or "KEEP" in visible: status="MAJORITY"
    else: status="REVIEW"
    ops=[x.get("operation") for x in items if x.get("operation")]
    return {"phenomenon_id":items[0]["phenomenon_id"],"excerpt":items[0].get("excerpt",""),"status":status,"reviewer_verdicts":verdicts,"operations":list(dict.fromkeys(ops)),"findings":items,"evidence":[],"evidence_summary":{"total":0,"supports_keep":0,"supports_change":0,"context":0,"neutral":0}}

def apply_style(groups,style):
    weights=style.get("reviewer_weights",{}); policy=style.get("conflict_policy","show_alternatives")
    for g in groups:
        score=sum(float(weights.get(r,1.0))*(1 if v=="CHANGE" else -1 if v=="KEEP" else 0) for r,v in g["reviewer_verdicts"].items()); g["style_score"]=round(score,3)
        if g["status"]=="SOURCE_CONFLICT" and policy=="preserve_original": g["recommendation"]="KEEP"
        elif g["status"]=="SOURCE_CONFLICT" and policy=="weighted_majority": g["recommendation"]="CHANGE" if score>0 else "KEEP" if score<0 else "SHOW_ALTERNATIVES"
        elif g["status"]=="SOURCE_CONFLICT": g["recommendation"]="SHOW_ALTERNATIVES"
        elif score>0: g["recommendation"]="CHANGE"
        elif score<0: g["recommendation"]="KEEP"
        else: g["recommendation"]="REVIEW"
    return groups

def build_board(findings,style,evidence=None):
    guardrails,groups=group_findings(findings); groups=apply_style(attach_evidence(groups,evidence),style)
    return {"guardrails":guardrails,"groups":groups,"summary":{"guardrails":len(guardrails),"groups":len(groups),"consensus":sum(g["status"]=="CONSENSUS" for g in groups),"conflicts":sum(g["status"]=="SOURCE_CONFLICT" for g in groups),"evidence_items_attached":sum(len(g.get("evidence",[])) for g in groups)}}
