#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    obs=load('studies/golub/observations.json'); ev=load('studies/golub/evals.json'); em=load('studies/golub/eval-map.json'); modern=load('studies/golub/modern-norm-audit.json')
    rows=obs['observations']; assert obs['status']=='OPERATIONAL'; assert len(rows)==93
    ids=[r['rule_id'] for r in rows]; pids=[r['phenomenon_id'] for r in rows]; assert len(ids)==len(set(ids)); assert len(pids)==len(set(pids))
    required={'source_book','edition','source_locator','provenance','claim','current_status','project_class','scope','semantic_function_invariant','trigger','required_context','diagnosis','operation','preferred_variant','valid_alternatives','register','positive_example','natural_negative_control','boundary_case','intentional_counterexample','exclusions','do_not_infer','interactions','confidence','verification_status','automation_level','existing_overlap','source_conflict','planned_module','runtime_visibility'}
    for r in rows:
        miss=required-set(r); assert not miss,(r['rule_id'],sorted(miss)); assert r['source_locator']; assert r['natural_negative_control']; assert r['boundary_case']; assert r['intentional_counterexample']
    assert all('GOOD' in r['source_book'] or 'STYLE' in r['source_book'] for r in rows)
    assert sum(1 for r in rows if r['provenance']=='PROJECT_DERIVED')==5
    ac={k:sum(1 for r in rows if r['automation_level']==k) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    assert ac=={'HARD_GATE':0,'DEFAULT_MECHANICAL':3,'EXTENDED_SOFT':1,'METRIC_ONLY':2,'MODEL_ONLY':87},ac
    assert len(ev['evals'])==93*4
    evalids={x['id'] for x in ev['evals']}; assert all(x['eval_id'] in evalids and x['rule_id'] in ids for x in em['map'])
    checked={x['phenomenon_id'] for x in modern['items']}; assert {'norm.soglasno_dative','norm.payment_verb_government','norm.gerund_subject_attachment','norm.double_comparative_marking'}<=checked
    print('golub study validator: OK; 93 phenomena; cross-book/provenance/eval/modern-norm gates OK')
if __name__=='__main__': main()
