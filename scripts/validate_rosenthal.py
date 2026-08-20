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
        for name in payload['observation_parts']:
            cards.extend(load(f'studies/{study_dir}/{name}').get('observations',[]))
    seen=set()
    for card in cards:
        oid=card.get('observation_id')
        if not oid or oid in seen: raise SystemExit(f'cycle{cycle} duplicate/missing observation id: {oid}')
        seen.add(oid); r={**defaults,**card}
        missing=[f for f in req if f not in r or r[f] in (None,'')]
        if missing: raise SystemExit(f'{oid}: unresolved atomic-card fields: {missing}')
        if r['current_status'] not in {'CURRENT_CONFIRMED','CURRENT_USAGE','SOURCE_PERIOD','CONTESTED','OBSOLETE'}: raise SystemExit(f'{oid}: invalid current_status {r["current_status"]}')
        if r['project_class'] not in {'NORM','NATIVE_USAGE','EDITING','REGISTER','AI_CALQUE','AUTHOR','HISTORICAL'}: raise SystemExit(f'{oid}: invalid project_class {r["project_class"]}')
    return seen

def main():
    base=load('libraries/rosenthal/rules.json'); c2=load('libraries/rosenthal/rules-cycle2.json'); c3=load('libraries/rosenthal/rules-cycle3.json'); c5=load('libraries/rosenthal/rules-cycle5.json')
    idx=load('libraries/rosenthal/rules-index.json'); manifest=load('libraries/rosenthal/library.json')
    p2=load('libraries/rosenthal/provenance-cycle2.json'); p3=load('libraries/rosenthal/provenance-cycle3.json'); p4=load('libraries/rosenthal/provenance-cycle4.json'); p5=load('libraries/rosenthal/provenance-cycle5.json')
    o2=load('studies/rosenthal-a-kak-luchshe-skazat/observations.json'); o3=load('studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/observations.json'); o4=load('studies/rosenthal-pravopisanie-stilistika/observations.json'); o5=load('studies/rosenthal-orfografiya-punktuatsiya/observations.json')
    items=base['rules']+c2['rules']+c3['rules']+c5['rules']; ids=[x['rule_id'] for x in items]
    expected=[f'ROS-R{i:02d}' for i in range(1,47)]+[f'ROS-R{i}' for i in range(47,79)]
    if ids!=expected: raise SystemExit(f'Rosenthal IDs not cumulative/contiguous: {ids[-20:]}')
    if len(ids)!=78 or len(ids)!=len(set(ids)): raise SystemExit('expected 78 unique cumulative rules')
    counts={k:sum(x['automation_level']==k for x in items) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    if counts!=idx['automation_counts']: raise SystemExit(f'automation mismatch {counts} != {idx["automation_counts"]}')
    if idx['source_cycles']!=5 or idx['total_rule_count']!=78: raise SystemExit('expected 5 cycles / 78 cumulative rules')
    if c2['rule_count']!=13 or c2['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':1,'METRIC_ONLY':0,'MODEL_ONLY':12}: raise SystemExit('cycle2 split mismatch')
    if c3['rule_count']!=15 or c3['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':0,'METRIC_ONLY':0,'MODEL_ONLY':15}: raise SystemExit('cycle3 split mismatch')
    if any(x['automation_level']!='MODEL_ONLY' for x in c3['rules']): raise SystemExit('cycle3 must not add pseudo-mechanical findings')
    if c5['rule_count']!=4: raise SystemExit('cycle5 rule count mismatch')
    if c5['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':0,'METRIC_ONLY':0,'MODEL_ONLY':4}: raise SystemExit('cycle5 split mismatch')
    if any(x['automation_level']!='MODEL_ONLY' for x in c5['rules']): raise SystemExit('cycle5 must remain MODEL_ONLY')
    if len({x['phenomenon_id'] for x in c5['rules']})!=4: raise SystemExit('duplicate cycle5 phenomenon_id')
    if o2['atomic_observation_count']!=63 or len(resolved_observations(o2,2))!=63: raise SystemExit('cycle2 observation mismatch')
    if o3['atomic_observation_count']!=95 or len(resolved_observations(o3,3,'rosenthal-pravopisanie-proiznoshenie-redaktirovanie'))!=95: raise SystemExit('cycle3 observation mismatch')
    if o4['atomic_observation_count']!=58 or len(resolved_observations(o4,4,'rosenthal-pravopisanie-stilistika'))!=58: raise SystemExit('cycle4 observation mismatch')
    if o5['atomic_observation_count']!=74 or len(resolved_observations(o5,5,'rosenthal-orfografiya-punktuatsiya'))!=74: raise SystemExit('cycle5 observation mismatch')
    if p2['existing_rules_enriched']!=27 or len(p2['map'])!=27: raise SystemExit('cycle2 provenance mismatch')
    if p3['existing_rules_enriched']!=56 or len(p3['map'])!=56: raise SystemExit('cycle3 provenance mismatch')
    if p4['existing_rules_enriched']!=50 or len(p4['map'])!=50 or p4.get('new_rule_ids')!=[]: raise SystemExit('cycle4 provenance mismatch')
    if p5['existing_rules_enriched']!=14 or len(p5['map'])!=14 or p5.get('new_rule_ids')!=['ROS-R75','ROS-R76','ROS-R77','ROS-R78']: raise SystemExit('cycle5 provenance mismatch')
    existing=set(ids)
    for row in p3['map']:
        if row['rule_id'] not in existing or int(row['rule_id'].split('R')[-1])>=60: raise SystemExit(f'cycle3 provenance target invalid: {row}')
    p4_ids=[x['rule_id'] for x in p4['map']]
    if len(p4_ids)!=len(set(p4_ids)) or any(x not in existing for x in p4_ids): raise SystemExit('cycle4 provenance target invalid/duplicate')
    expected_p4={f'ROS-R{i:02d}' for i in range(1,47)}|{'ROS-R47','ROS-R49','ROS-R53','ROS-R54'}
    if set(p4_ids)!=expected_p4: raise SystemExit(f'cycle4 provenance set mismatch: {sorted(set(p4_ids)^expected_p4)}')
    p5_ids=[x['rule_id'] for x in p5['map']]
    expected_p5={'ROS-R14','ROS-R17','ROS-R30','ROS-R37','ROS-R41','ROS-R46','ROS-R50','ROS-R55','ROS-R56','ROS-R58','ROS-R65','ROS-R69','ROS-R73','ROS-R74'}
    if len(p5_ids)!=len(set(p5_ids)) or set(p5_ids)!=expected_p5: raise SystemExit(f'cycle5 provenance set mismatch: {sorted(set(p5_ids)^expected_p5)}')
    if manifest['source_branch']!='rosenthal' or manifest['adapter']!='review_v1': raise SystemExit('manifest routing mismatch')
    if manifest['rules_path']!='libraries/rosenthal/rules-index.json': raise SystemExit('manifest must route through cumulative index')
    if idx['groups']!=manifest['rule_groups'] or len(manifest.get('rule_groups',[]))!=4: raise SystemExit('cycle5 rule-group routing missing')
    if len(manifest.get('provenance_maps',[]))!=4: raise SystemExit('cycle5 provenance routing missing')
    for fp in idx['source_fingerprints']:
        if fp not in manifest['source_version']: raise SystemExit(f'manifest missing fingerprint {fp}')
    required=['source.md','coverage.md','observations.json','concepts.md','rules.md','interactions.md','claims.md','current-norm.md','integration-matrix.md','evals.json','eval-map.json','audit.md']
    for study_name in ['rosenthal-a-kak-luchshe-skazat','rosenthal-pravopisanie-proiznoshenie-redaktirovanie','rosenthal-pravopisanie-stilistika','rosenthal-orfografiya-punktuatsiya']:
        for name in required:
            if not (ROOT/'studies'/study_name/name).is_file(): raise SystemExit(f'missing study artifact: {study_name}/{name}')
    for study_name,payload in [('rosenthal-pravopisanie-proiznoshenie-redaktirovanie',o3),('rosenthal-pravopisanie-stilistika',o4),('rosenthal-orfografiya-punktuatsiya',o5)]:
        for name in payload.get('observation_parts',[]):
            if not (ROOT/'studies'/study_name/name).is_file(): raise SystemExit(f'missing observation part: {study_name}/{name}')
    for study_name,n in [('rosenthal-a-kak-luchshe-skazat',12),('rosenthal-pravopisanie-proiznoshenie-redaktirovanie',16),('rosenthal-pravopisanie-stilistika',12),('rosenthal-orfografiya-punktuatsiya',14)]:
        e=load(f'studies/{study_name}/evals.json')['cases']; m=load(f'studies/{study_name}/eval-map.json')['map']
        if len(e)!=n or {x['id'] for x in e}!={x['eval_id'] for x in m}: raise SystemExit(f'eval map mismatch: {study_name}')
        if {x['rule_id'] for x in m}-existing: raise SystemExit(f'eval maps unknown rules: {study_name}')
    cases=load('tests/rosenthal_cases.json')['cases']
    if len(cases)<15: raise SystemExit('too few cumulative Rosenthal mechanical controls')
    norm3=(ROOT/'studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/current-norm.md').read_text(encoding='utf-8')
    for needle in ['gramota.ru/meta/ambitsioznyy','gramota.ru/meta/agressivnyy','query=%D0%BF%D1%80%D0%B0%D1%87%D0%B5%D1%87%D0%BD%D0%B0%D1%8F','OBSOLETE','SOURCE_PERIOD']:
        if needle not in norm3: raise SystemExit(f'missing cycle3 current-norm evidence/boundary: {needle}')
    norm4=(ROOT/'studies/rosenthal-pravopisanie-stilistika/current-norm.md').read_text(encoding='utf-8')
    for needle in ['vopros/324406','query=%D0%BA%D0%BB%D0%B8%D0%BF%D1%81','vopros/331581','OBSOLETE','SOURCE_PERIOD']:
        if needle not in norm4: raise SystemExit(f'missing cycle4 current-norm evidence/boundary: {needle}')
    gal=load('libraries/gal/rules/editor_workflow.json')['rules']
    if not any(x.get('phenomenon_id')=='editing.local_change_whole_fit' for x in gal): raise SystemExit('expected cross-school whole-fit overlap with Gal')
    norm5=(ROOT/'studies/rosenthal-orfografiya-punktuatsiya/current-norm.md').read_text(encoding='utf-8')
    for needle in ['vopros/314903','vopros/306315','SOURCE_PERIOD','CURRENT_CONFIRMED']:
        if needle not in norm5: raise SystemExit(f'missing cycle5 current-norm evidence/boundary: {needle}')
    source5=(ROOT/'studies/rosenthal-orfografiya-punktuatsiya/source.md').read_text(encoding='utf-8')
    if 'UNKNOWN_IN_SUPPLIED_DOCX' not in source5: raise SystemExit('cycle5 must not invent edition metadata')
    print(f'rosenthal cumulative library: {len(items)} rules across 5 sources; automation {counts}; cycle5 74 observations, 4 new MODEL_ONLY rules, 14 enriched rules, 14 preservation/context evals; OK')
if __name__=='__main__': main()
