#!/usr/bin/env python3
"""Editorial-board mode with optional fail-open evidence providers."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from editorial_board import build_board
from library_runtime import load_style,reviewer_profiles,run_libraries

def _parse_evidence_arg(value):
    if value is None or value.strip().lower() in {"","off","none","false","0"}: return None
    if value.strip().lower() in {"auto","all"}: return value.strip().lower()
    return [x.strip() for x in value.split(",") if x.strip()]

def run_review(text,style_id="neutral",library_ids=None,evidence_ids=None,register="general"):
    style=load_style(style_id)
    findings,metrics=run_libraries(
        text,
        library_ids=library_ids,
        context={"mode":"editorial_board","register":register,"style_id":style_id},
    )
    evidence=[]; evidence_status=[]
    if evidence_ids is not None:
        from evidence_runtime import run_evidence
        evidence,evidence_status=run_evidence(text,evidence_ids,context={"findings":findings,"style_id":style_id,"library_ids":library_ids or "default","register":register})
    board=build_board(findings,style,evidence=evidence); profiles=reviewer_profiles(); used=sorted({f["reviewer_id"] for f in findings if f.get("reviewer_id")})
    return {"schema_version":1,"mode":"editorial_board","style":style,"register":register,"libraries":library_ids or "default","evidence_request":evidence_ids or "off","reviewers":{k:profiles.get(k,{"id":k,"display_name":k}) for k in used},"findings":findings,"metrics":metrics,"evidence":evidence,"evidence_status":evidence_status,"board":board}

def render_markdown(report):
    lines=["## Редколлегия humanizer_russian","",f"Стиль: **{report['style']['display_name']}**. Регистр: **{report.get('register','general')}**.",""]; guardrails=report["board"]["guardrails"]
    if guardrails:
        lines += ["### Guardrails",""]+[f"- **{x['project_class']}** `{x['rule_id']}`: {x.get('excerpt','')} — {x.get('reason','')}" for x in guardrails]+[""]
    for g in report["board"]["groups"]:
        lines += [f"### {g['phenomenon_id']}","",f"Фрагмент: `{g.get('excerpt','')}`",f"Итог коллегии: **{g['status']} → {g['recommendation']}**",""]
        by={}
        for f in g["findings"]: by.setdefault(f["reviewer_id"],[]).append(f)
        for rid,rows in by.items():
            name=report["reviewers"].get(rid,{}).get("display_name",rid); lines.append(f"- **{name}: {g['reviewer_verdicts'][rid]}**")
            for f in rows: lines.append(f"  - {f.get('reason') or f['rule_id']}")
        if g.get("evidence"):
            lines.append("- **Evidence (не голос):**")
            for e in g["evidence"]: lines.append(f"  - `{e.get('provider_id','evidence')}` / {e.get('direction','CONTEXT')}: {e.get('reason','')}")
        lines.append("")
    bad=[x for x in report.get("evidence_status",[]) if x.get("status")!="OK"]
    if bad:
        lines += ["### Evidence status",""]+[f"- `{x['provider_id']}`: {x['status']} — {x.get('message','')}" for x in bad]+[""]
    if not guardrails and not report["board"]["groups"]: lines.append("Механические библиотеки не нашли замечаний.")
    lines += ["","_Имена авторов обозначают оценку по формализованным правилам источника, а не реальную рецензию или цитату автора._","_Evidence providers дают данные, а не дополнительные голоса редколлегии._"]
    return "\n".join(lines).rstrip()+"\n"

def main():
    p=argparse.ArgumentParser(description="Editorial-board review for humanizer_russian")
    p.add_argument("file",nargs="?")
    p.add_argument("--style",default="neutral")
    p.add_argument("--libraries")
    p.add_argument("--register",choices=["general","everyday","professional","technical"],default="general")
    p.add_argument("--evidence",help="off (default), auto, all, or comma-separated provider ids")
    p.add_argument("--format",choices=["json","markdown"],default="markdown")
    a=p.parse_args()
    text=Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read(); ids=[x.strip() for x in a.libraries.split(",") if x.strip()] if a.libraries else None; evidence_ids=_parse_evidence_arg(a.evidence); report=run_review(text,style_id=a.style,library_ids=ids,evidence_ids=evidence_ids,register=a.register)
    print(json.dumps(report,ensure_ascii=False,indent=2) if a.format=="json" else render_markdown(report),end="\n" if a.format=="json" else "")
if __name__=="__main__": main()
