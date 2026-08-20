#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    lib=json.loads((ROOT/'libraries/golub/library.json').read_text(encoding='utf-8')); rules=json.loads((ROOT/'libraries/golub/rules.json').read_text(encoding='utf-8')); rev=json.loads((ROOT/'reviewers/golub.json').read_text(encoding='utf-8'))
    assert lib['id']==rev['id']=='golub'; assert lib['adapter']=='review_v1'; assert lib['status']=='OPERATIONAL'; assert rules['rule_count']==93
    assert len({r['phenomenon_id'] for r in rules['rules']})==93
    by={r['rule_id']:r for r in rules['rules']}
    assert by['GOLUB-R40']['phenomenon_id']=='norm.soglasno_dative'
    assert by['GOLUB-R41']['phenomenon_id']=='norm.payment_verb_government'
    assert by['GOLUB-R59']['phenomenon_id']=='editing.paired_conjunction_alignment' and by['GOLUB-R59']['automation_level']=='EXTENDED_SOFT'
    spec=importlib.util.spec_from_file_location('lint_golub',ROOT/lib['linter_path']); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.self_test()
    out=m.review('Согласно приказа директора оплатить за проезд было более лучше.'); ids={x['rule_id'] for x in out['findings']}; assert {'GOLUB-R40','GOLUB-R41','GOLUB-R44'}<=ids
    keep=m.review('Согласно приказу директора можно заплатить за проезд. Этот вариант лучше.'); assert not keep['findings'],keep
    fixture=json.loads((ROOT/'tests/golub_cases.json').read_text(encoding='utf-8'))
    for case in fixture['cases']:
        got={x['rule_id'] for x in m.review(case['text'])['findings']}
        assert set(case.get('must_have',[])) <= got, (case,got)
        assert not (set(case.get('must_not_have',[])) & got), (case,got)
    assert not any(x['automation_level']=='MODEL_ONLY' for x in m.review('Длинное сложное предложение само по себе не ошибка.')['findings'])
    obs=json.loads((ROOT/'studies/golub/observations.json').read_text(encoding='utf-8'))['observations']; ob={r['rule_id']:r for r in obs}
    assert 'ROS-R44' in ob['GOLUB-R40']['existing_overlap'] and 'ROS-R30' in ob['GOLUB-R59']['existing_overlap']
    src=(ROOT/'scripts/lint_golub.py').read_text(encoding='utf-8')
    assert 'from shared_russian_norm_surfaces import' in src and 'SOGLASNO_GENITIVE = re.compile' not in src and 'MIXED_CORRELATIVE = re.compile' not in src
    print('golub integration validator: OK; dedup + preservation + adapter self-test OK')
if __name__=='__main__': main()
