#!/usr/bin/env python3
"""Conservative mechanical surface checks for the cumulative Rosenthal library."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

URL=re.compile(r"https?://\S+",re.I)
FENCED=re.compile(r"```.*?```|~~~.*?~~~",re.S)
INLINE_CODE=re.compile(r"`[^`\n]+`")
QUOTED=[re.compile(r"«[^»]*»",re.S),re.compile(r"“[^”]*”",re.S),re.compile(r'"[^"\n]*"')]
MARKDOWN_NON_PROSE=re.compile(r"^\s*(#|\||[-*+]\s|\d+[.)]\s|>)")
SOGLASNO_GENITIVE=re.compile(r"\bсогласно\s+(?:приказа|договора|закона|указа|регламента|протокола|плана|графика|кодекса|распоряжения|положения|решения|требования|постановления|соглашения|(?:данного|этого|нового|действующего|утвержд[её]нного|указанного|федерального|внутреннего|текущего|последнего)\s+(?:[А-Яа-яЁё-]+(?:ого|его)\s+){0,2}[А-Яа-яЁё-]+(?:а|я))\b",re.I)
MIXED_CORRELATIVE=re.compile(r"\bне\s+только\b(?:(?![.!?]).){0,180}?\bа\s+также\b",re.I|re.S)
# Whitelist avoids pseudo-morphological regex over positive adjectives such as `более раннее решение`.
DOUBLE_COMPARATIVE=re.compile(r"\b(?:более|менее)\s+(?:лучше|хуже|больше|меньше|выше|ниже|старше|младше|дальше|ближе|быстрее|медленнее|сильнее|слабее|дороже|дешевле|красивее|точнее|яснее|проще|сложнее|лучший|худший)\b",re.I)

def _blank(m:re.Match[str])->str: return ''.join('\n' if c=='\n' else ' ' for c in m.group(0))
def _prose(text:str)->str:
    out=FENCED.sub(_blank,text); out=INLINE_CODE.sub(_blank,out); out=URL.sub(_blank,out)
    for rx in QUOTED: out=rx.sub(_blank,out)
    lines=[]; in_frontmatter=False
    for i,line in enumerate(out.splitlines()):
        if i==0 and line.strip()=='---': in_frontmatter=True; lines.append(''); continue
        if in_frontmatter:
            lines.append('')
            if line.strip()=='---': in_frontmatter=False
            continue
        lines.append('' if MARKDOWN_NON_PROSE.match(line) else line)
    return '\n'.join(lines)
def _line(text:str,pos:int)->int: return text.count('\n',0,pos)+1
def _finding(rule_id,phenomenon_id,project_class,verdict,excerpt,line,reason,operation):
    return {'rule_id':rule_id,'phenomenon_id':phenomenon_id,'project_class':project_class,'automation_level':'EXTENDED_SOFT','verdict':verdict,'line':line,'excerpt':excerpt[:180],'reason':reason,'operation':operation,'confidence':None}
def review(text:str,context:dict|None=None)->dict:
    prose=_prose(text); findings=[]
    for m in SOGLASNO_GENITIVE.finditer(prose): findings.append(_finding('ROS-R44','norm.soglasno_dative','NORM','CHANGE',m.group(0),_line(prose,m.start()),'`согласно` в современном литературном русском требует дательного падежа; детектор ограничен высокоуверенными поверхностными формами.','replace_genitive_after_soglasno_with_dative'))
    for m in MIXED_CORRELATIVE.finditer(prose): findings.append(_finding('ROS-R30','editing.paired_conjunction_alignment','EDITING','REVIEW',m.group(0),_line(prose,m.start()),'Проверьте смешение `не только … а также`; нейтральная базовая пара — `не только … но и`.','restore_correlative_pair'))
    for m in DOUBLE_COMPARATIVE.finditer(prose): findings.append(_finding('ROS-R53','norm.double_comparative_marking','NORM','CHANGE',m.group(0),_line(prose,m.start()),'Форма одновременно маркирует степень сравнения аналитически и синтетически. Используйте один способ; намеренная языковая игра и метаязык исключены маскированием цитат/кода.','use_one_comparison_strategy'))
    return {'findings':findings,'metrics':{'rosenthal_metric_rule_ids':['ROS-R10'],'rosenthal_extended_findings':len(findings),'metrics_are_descriptive':True}}
def self_test()->None:
    def ids(s): return {x['rule_id'] for x in review(s)['findings']}
    assert 'ROS-R44' in ids('Согласно приказа директора документ обновили.')
    assert 'ROS-R44' not in ids('Согласно приказу директора документ обновили.')
    assert 'ROS-R30' in ids('Он не только проверил данные, а также исправил отчёт.')
    assert 'ROS-R30' not in ids('Он не только проверил данные, но и исправил отчёт.')
    assert 'ROS-R53' in ids('Этот вариант более лучше предыдущего.')
    assert 'ROS-R53' in ids('Новая версия более красивее старой.')
    assert 'ROS-R53' not in ids('Новая версия более красивая.')
    assert 'ROS-R53' not in ids('Новая версия красивее старой.')
    assert 'ROS-R53' not in ids('Это мой самый лучший друг.')
    assert 'ROS-R53' not in ids('Нам нужен более ранний поезд.')
    assert 'ROS-R53' not in ids('Форму «более лучше» обсуждают как пример.')
    assert not review('```text\nболее лучше\n```')['findings']
    print('rosenthal linter self-test: OK')
def main()->None:
    p=argparse.ArgumentParser(); p.add_argument('file',nargs='?'); p.add_argument('--json',action='store_true',dest='as_json'); p.add_argument('--self-test',action='store_true'); a=p.parse_args()
    if a.self_test: self_test(); return
    text=Path(a.file).read_text(encoding='utf-8') if a.file else sys.stdin.read(); result=review(text)
    print(json.dumps(result,ensure_ascii=False,indent=2) if a.as_json else '\n'.join(f"{x['rule_id']}:{x['line']} {x['excerpt']} — {x['reason']}" for x in result['findings']))
if __name__=='__main__': main()
