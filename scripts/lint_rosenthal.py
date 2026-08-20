#!/usr/bin/env python3
"""Conservative mechanical surfaces for the cumulative Rosenthal library."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from shared_russian_norm_surfaces import iter_soglasno_genitive,iter_mixed_correlative,iter_double_comparative,prose_surface
def _line(t,p): return t.count('\n',0,p)+1
def _finding(rule_id,pid,pc,verdict,m,text,reason,operation):
    return {'rule_id':rule_id,'phenomenon_id':pid,'project_class':pc,'automation_level':'EXTENDED_SOFT','verdict':verdict,'line':_line(text,m.start()),'excerpt':m.group(0)[:180],'reason':reason,'operation':operation,'confidence':None}
def review(text,context=None):
    prose=prose_surface(text); f=[]
    for m in iter_soglasno_genitive(prose): f.append(_finding('ROS-R44','norm.soglasno_dative','NORM','CHANGE',m,prose,'`согласно` в современном литературном русском требует дательного падежа; детектор ограничен высокоуверенными поверхностными формами.','replace_genitive_after_soglasno_with_dative'))
    for m in iter_mixed_correlative(prose): f.append(_finding('ROS-R30','editing.paired_conjunction_alignment','EDITING','REVIEW',m,prose,'Проверьте смешение `не только … а также`; нейтральная базовая пара — `не только … но и`.','restore_correlative_pair'))
    for m in iter_double_comparative(prose): f.append(_finding('ROS-R53','norm.double_comparative_marking','NORM','CHANGE',m,prose,'Форма одновременно маркирует степень сравнения аналитически и синтетически. Используйте один способ; намеренная языковая игра и метаязык исключены маскированием цитат/кода.','use_one_comparison_strategy'))
    return {'findings':f,'metrics':{'rosenthal_metric_rule_ids':['ROS-R10'],'rosenthal_extended_findings':len(f),'metrics_are_descriptive':True}}
def self_test():
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
def main():
    p=argparse.ArgumentParser(); p.add_argument('file',nargs='?'); p.add_argument('--json',action='store_true',dest='as_json'); p.add_argument('--self-test',action='store_true'); a=p.parse_args()
    if a.self_test: self_test(); return
    text=Path(a.file).read_text(encoding='utf-8') if a.file else sys.stdin.read(); result=review(text)
    print(json.dumps(result,ensure_ascii=False,indent=2) if a.as_json else '\n'.join(f"{x['rule_id']}:{x['line']} {x['excerpt']} — {x['reason']}" for x in result['findings']))
if __name__=='__main__': main()
