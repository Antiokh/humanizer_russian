#!/usr/bin/env python3
"""Conservative mechanical surface checks for the Rosenthal source library.

The first source is rich in contextual style and historical norm. Accordingly,
only two narrow, currently verified surfaces are emitted. Everything requiring
semantics, morphology, syntax, register or authorial intent stays MODEL_ONLY.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

URL = re.compile(r"https?://\S+", re.I)
FENCED = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE = re.compile(r"`[^`\n]+`")
QUOTED = [re.compile(r"«[^»]*»", re.S), re.compile(r"“[^”]*”", re.S), re.compile(r'"[^"\n]*"')]
MARKDOWN_NON_PROSE = re.compile(r"^\s*(#|\||[-*+]\s|\d+[.)]\s|>)")

SOGLASNO_GENITIVE = re.compile(
    r"\bсогласно\s+(?:"
    r"приказа|договора|закона|указа|регламента|протокола|плана|графика|кодекса|"
    r"распоряжения|положения|решения|требования|постановления|соглашения|"
    r"(?:данного|этого|нового|действующего|утвержд[её]нного|указанного|"
    r"федерального|внутреннего|текущего|последнего)\s+(?:[А-Яа-яЁё-]+(?:ого|его)\s+){0,2}[А-Яа-яЁё-]+(?:а|я)"
    r")\b",
    re.I,
)
MIXED_CORRELATIVE = re.compile(
    r"\bне\s+только\b(?:(?![.!?]).){0,180}?\bа\s+также\b",
    re.I | re.S,
)

def _blank(m: re.Match[str]) -> str:
    return "".join("\n" if c == "\n" else " " for c in m.group(0))

def _prose(text: str) -> str:
    out=FENCED.sub(_blank,text)
    out=INLINE_CODE.sub(_blank,out)
    out=URL.sub(_blank,out)
    for rx in QUOTED:
        out=rx.sub(_blank,out)
    lines=[]
    in_frontmatter=False
    for i,line in enumerate(out.splitlines()):
        if i==0 and line.strip()=='---':
            in_frontmatter=True; lines.append(''); continue
        if in_frontmatter:
            lines.append('')
            if line.strip()=='---': in_frontmatter=False
            continue
        lines.append('' if MARKDOWN_NON_PROSE.match(line) else line)
    return "\n".join(lines)

def _line(text: str,pos: int)->int:
    return text.count("\n",0,pos)+1

def _finding(rule_id,phenomenon_id,project_class,verdict,excerpt,line,reason,operation):
    return {'rule_id':rule_id,'phenomenon_id':phenomenon_id,'project_class':project_class,'automation_level':'EXTENDED_SOFT','verdict':verdict,'line':line,'excerpt':excerpt[:180],'reason':reason,'operation':operation,'confidence':None}

def review(text: str, context: dict | None = None) -> dict:
    prose=_prose(text)
    findings=[]
    for m in SOGLASNO_GENITIVE.finditer(prose):
        findings.append(_finding('ROS-R44','norm.soglasno_dative','NORM','CHANGE',m.group(0),_line(prose,m.start()),'Предлог `согласно` в современном литературном русском требует дательного падежа. Поверхностный детектор ограничен формами, где родительный виден без морфологической догадки.','replace_genitive_after_soglasno_with_dative'))
    for m in MIXED_CORRELATIVE.finditer(prose):
        findings.append(_finding('ROS-R30','editing.paired_conjunction_alignment','EDITING','REVIEW',m.group(0),_line(prose,m.start()),'Проверьте смешение `не только … а также`. Базовая нейтральная парная конструкция — `не только … но и`; длинная синтаксическая структура требует контекстной проверки.','restore_correlative_pair'))
    return {'findings':findings,'metrics':{'rosenthal_metric_rule_ids':['ROS-R10'],'rosenthal_extended_findings':len(findings),'metrics_are_descriptive':True}}

def self_test()->None:
    def ids(s): return {x['rule_id'] for x in review(s)['findings']}
    assert 'ROS-R44' in ids('Согласно приказа директора документ обновили.')
    assert 'ROS-R44' in ids('Согласно действующего федерального закона срок изменён.')
    assert 'ROS-R44' not in ids('Согласно приказу директора документ обновили.')
    assert 'ROS-R44' not in ids('Согласно инструкции документ обновили.')
    assert 'ROS-R30' in ids('Он не только проверил данные, а также исправил отчёт.')
    assert 'ROS-R30' not in ids('Он не только проверил данные, но и исправил отчёт.')
    assert 'ROS-R30' not in ids('В цитате «не только точность, а также скорость» обсуждается смешанный союз.')
    assert not review('```text\nСогласно приказа директора.\n```')['findings']
    assert not review('# Согласно приказа директора')['findings']
    assert not review('Термин «согласно приказа» приведён как исторический пример.')['findings']
    print('rosenthal linter self-test: OK')

def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument('file',nargs='?')
    p.add_argument('--json',action='store_true',dest='as_json')
    p.add_argument('--self-test',action='store_true')
    a=p.parse_args()
    if a.self_test:
        self_test(); return
    text=Path(a.file).read_text(encoding='utf-8') if a.file else sys.stdin.read()
    result=review(text)
    print(json.dumps(result,ensure_ascii=False,indent=2) if a.as_json else '\n'.join(f"{x['rule_id']}:{x['line']} {x['excerpt']} — {x['reason']}" for x in result['findings']))

if __name__=='__main__': main()
