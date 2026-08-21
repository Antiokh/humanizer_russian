#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def resolved_observations(payload,cycle,study_dir=None):
    defaults=payload.get('card_defaults',{}); req=payload.get('required_resolved_fields',[])
    if not req: raise SystemExit(f'cycle{cycle} atomic-card contract missing')
    cards=payload.get('observations')
    if cards is None:
        if not study_dir or not payload.get('observation_parts'): raise SystemExit(f'cycle{cycle} observations missing')
        cards=[]
        for name in payload['observation_parts']: cards.extend(load(f'studies/{study_dir}/{name}').get('observations',[]))
    seen=set()
    for card in cards:
        oid=card.get('observation_id')
        if not oid or oid in seen: raise SystemExit(f'cycle{cycle} duplicate/missing observation id: {oid}')
        seen.add(oid); r={**defaults,**card}
        missing=[f for f in req if f not in r or r[f] in (None,'')]
        if missing: raise SystemExit(f'{oid}: unresolved atomic-card fields: {missing}')
        if r['current_status'] not in {'CURRENT_CONFIRMED','CURRENT_USAGE','SOURCE_PERIOD','CONTESTED','OBSOLETE'}: raise SystemExit(f'{oid}: invalid current_status')
        if r['project_class'] not in {'NORM','NATIVE_USAGE','EDITING','REGISTER','AI_CALQUE','AUTHOR','HISTORICAL'}: raise SystemExit(f'{oid}: invalid project_class')
    return seen
def eval_rule_ids(rows,study_name):
    refs=set()
    for row in rows:
        if 'rule_id' in row: refs.add(row['rule_id'])
        elif 'rule_ids' in row:
            v=row['rule_ids']
            if not isinstance(v,list) or not v: raise SystemExit(f'invalid eval rule_ids: {study_name}')
            refs.update(v)
        else: raise SystemExit(f'eval map row has no rule reference: {study_name}')
    return refs
def main():
    base=load('libraries/rosenthal/rules.json'); c2=load('libraries/rosenthal/rules-cycle2.json'); c3=load('libraries/rosenthal/rules-cycle3.json'); c5=load('libraries/rosenthal/rules-cycle5.json'); c6=load('libraries/rosenthal/rules-cycle6.json')
    idx=load('libraries/rosenthal/rules-index.json'); manifest=load('libraries/rosenthal/library.json')
    p2=load('libraries/rosenthal/provenance-cycle2.json'); p3=load('libraries/rosenthal/provenance-cycle3.json'); p4=load('libraries/rosenthal/provenance-cycle4.json'); p5=load('libraries/rosenthal/provenance-cycle5.json'); p6=load('libraries/rosenthal/provenance-cycle6.json')
    studies=[('rosenthal-a-kak-luchshe-skazat',2,63,12),('rosenthal-pravopisanie-proiznoshenie-redaktirovanie',3,95,16),('rosenthal-pravopisanie-stilistika',4,58,12),('rosenthal-orfografiya-punktuatsiya',5,74,14),('rosenthal-prakticheskaya-stilistika-2001',6,125,16)]
    observations={n:load(f'studies/{n}/observations.json') for n,_,_,_ in studies}
    items=base['rules']+c2['rules']+c3['rules']+c5['rules']+c6['rules']; ids=[x['rule_id'] for x in items]
    expected=[f'ROS-R{i:02d}' for i in range(1,47)]+[f'ROS-R{i}' for i in range(47,80)]
    if ids!=expected or len(ids)!=79 or len(ids)!=len(set(ids)): raise SystemExit('expected contiguous R01-R79')
    counts={k:sum(x['automation_level']==k for x in items) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    expected_counts={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':3,'METRIC_ONLY':1,'MODEL_ONLY':75}
    if counts!=expected_counts or counts!=idx['automation_counts']: raise SystemExit(f'automation mismatch {counts}')
    if idx['source_cycles']!=6 or idx['total_rule_count']!=79: raise SystemExit('expected 6 cycles / 79 rules')
    if [c2['rule_count'],c3['rule_count'],c5['rule_count'],c6['rule_count']]!=[13,15,4,1]: raise SystemExit('source rule counts mismatch')
    r79=c6['rules'][0]
    if (r79['rule_id'],r79['phenomenon_id'],r79['project_class'],r79['automation_level'])!=('ROS-R79','author.free_indirect_speech_dual_voice','AUTHOR','MODEL_ONLY'): raise SystemExit('R79 contract mismatch')
    if 'ROS-R79' in (ROOT/'scripts/lint_rosenthal.py').read_text(encoding='utf-8'): raise SystemExit('R79 leaked into linter')
    for n,c,no,_ in studies:
        o=observations[n]
        if o['atomic_observation_count']!=no or len(resolved_observations(o,c,n))!=no: raise SystemExit(f'cycle{c} observation mismatch')
    for p,num,new in [(p2,27,None),(p3,56,None),(p4,50,[]),(p5,14,['ROS-R75','ROS-R76','ROS-R77','ROS-R78']),(p6,64,['ROS-R79'])]:
        if p['existing_rules_enriched']!=num or len(p['map'])!=num: raise SystemExit(f'provenance count mismatch cycle {p.get("source_cycle")}')
        if new is not None and p.get('new_rule_ids')!=new: raise SystemExit('new rule ids mismatch')
        r=[x['rule_id'] for x in p['map']]
        if len(r)!=len(set(r)) or any(x not in set(ids) for x in r): raise SystemExit('invalid provenance target')
    if manifest['source_branch']!='rosenthal' or manifest['adapter']!='review_v1' or manifest['rules_path']!='libraries/rosenthal/rules-index.json': raise SystemExit('manifest routing mismatch')
    if idx['groups']!=manifest['rule_groups'] or len(manifest['rule_groups'])!=5 or len(manifest['provenance_maps'])!=5: raise SystemExit('cycle6 routing missing')
    for fp in idx['source_fingerprints']:
        if fp not in manifest['source_version']: raise SystemExit(f'manifest missing fingerprint {fp}')
    required=['source.md','coverage.md','observations.json','concepts.md','rules.md','interactions.md','claims.md','current-norm.md','integration-matrix.md','evals.json','eval-map.json','audit.md']
    existing=set(ids)
    for n,c,_,ne in studies:
        for f in required:
            if not (ROOT/'studies'/n/f).is_file(): raise SystemExit(f'missing study artifact: {n}/{f}')
        for part in observations[n].get('observation_parts',[]):
            if not (ROOT/'studies'/n/part).is_file(): raise SystemExit(f'missing observation part: {n}/{part}')
        e=load(f'studies/{n}/evals.json')['cases']; m=load(f'studies/{n}/eval-map.json')['map']
        if len(e)!=ne or {x['id'] for x in e}!={x['eval_id'] for x in m} or eval_rule_ids(m,n)-existing: raise SystemExit(f'eval mismatch: {n}')
    norm=(ROOT/'studies/rosenthal-prakticheskaya-stilistika-2001/current-norm.md').read_text(encoding='utf-8')
    for s in ['vopros/332830','vopros/100006','vopros/324406','slovar-trudnostey/soglasno','vopros/208929','SOURCE_PERIOD','CURRENT_CONFIRMED']:
        if s not in norm: raise SystemExit(f'missing cycle6 current norm: {s}')
    src=(ROOT/'studies/rosenthal-prakticheskaya-stilistika-2001/source.md').read_text(encoding='utf-8')
    for s in ['99c8cca2ecc144ab617c08b3187ed5ef772a8e2ce858a23d00c69e06366a25a5','2001','5-329-00322-9','382']:
        if s not in src: raise SystemExit(f'missing source identity: {s}')
    audit=(ROOT/'libraries/rosenthal/final-audit.md').read_text(encoding='utf-8')
    for s in ['79','ROS-R30','ROS-R44','ROS-R53','ROS-R79','64 existing','russian/NORM']:
        if s not in audit: raise SystemExit(f'final audit missing: {s}')
    reviewer=load('reviewers/rosenthal.json')
    if 'формализованным принципам' not in reviewer.get('display_name','').lower() or 'не реальная рецензия' not in reviewer.get('disclaimer','').lower(): raise SystemExit('unsafe attribution')
    if len(load('tests/rosenthal_cases.json')['cases'])<15: raise SystemExit('too few mechanical controls')
    print(f'rosenthal cumulative library: 79 rules across 6 sources; automation {counts}; cycle6 125 observations, R79 MODEL_ONLY, 64 enriched rules, 16 evals; final audit OK')
if __name__=='__main__': main()
