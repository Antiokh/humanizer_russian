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
        if not study_dir or not payload.get('observation_parts'):
            raise SystemExit(f'cycle{cycle} observations missing')
        cards=[]
        for name in payload['observation_parts']:
            part=load(f'studies/{study_dir}/{name}')
            cards.extend(part.get('observations',[]))
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
    base=load('libraries/rosenthal/rules.json')
    c2=load('libraries/rosenthal/rules-cycle2.json')
    c3=load('libraries/rosenthal/rules-cycle3.json')
    idx=load('libraries/rosenthal/rules-index.json')
    manifest=load('libraries/rosenthal/library.json')
    p2=load('libraries/rosenthal/provenance-cycle2.json')
    p3=load('libraries/rosenthal/provenance-cycle3.json')
    o2=load('studies/rosenthal-a-kak-luchshe-skazat/observations.json')
    o3=load('studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/observations.json')
    cases=load('tests/rosenthal_cases.json')['cases']
    items=base['rules']+c2['rules']+c3['rules']; ids=[x['rule_id'] for x in items]
    expected=[f'ROS-R{i:02d}' for i in range(1,47)]+[f'ROS-R{i}' for i in range(47,75)]
    if ids!=expected: raise SystemExit(f'Rosenthal IDs are not cumulative/contiguous: {ids[-20:]}')
    if len(ids)!=len(set(ids)): raise SystemExit('duplicate Rosenthal rule_id')
    counts={k:sum(x['automation_level']==k for x in items) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    if counts!=idx['automation_counts']: raise SystemExit(f'automation mismatch {counts} != {idx["automation_counts"]}')
    if idx['source_cycles']!=3 or idx['total_rule_count']!=74 or len(items)!=74: raise SystemExit('expected 3 cycles / 74 cumulative Rosenthal rules')
    if c2['rule_count']!=13 or c2['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':1,'METRIC_ONLY':0,'MODEL_ONLY':12}: raise SystemExit('cycle2 split mismatch')
    if c3['rule_count']!=15 or c3['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':0,'METRIC_ONLY':0,'MODEL_ONLY':15}: raise SystemExit('cycle3 split mismatch')
    if any(x['automation_level']!='MODEL_ONLY' for x in c3['rules']): raise SystemExit('cycle3 must not add pseudo-mechanical findings')
    if o2['atomic_observation_count']!=63 or len(resolved_observations(o2,2))!=63: raise SystemExit('cycle2 observation mismatch')
    if o3['atomic_observation_count']!=95 or len(resolved_observations(o3,3,'rosenthal-pravopisanie-proiznoshenie-redaktirovanie'))!=95: raise SystemExit('cycle3 observation mismatch')
    if p2['existing_rules_enriched']!=27 or len(p2['map'])!=27: raise SystemExit('cycle2 provenance mismatch')
    if p3['existing_rules_enriched']!=56 or len(p3['map'])!=56: raise SystemExit('cycle3 provenance mismatch')
    existing=set(ids)
    for row in p3['map']:
        if row['rule_id'] not in existing or int(row['rule_id'].split('R')[-1])>=60: raise SystemExit(f'cycle3 provenance target invalid: {row}')
    if manifest['source_branch']!='rosenthal' or manifest['adapter']!='review_v1': raise SystemExit('manifest routing mismatch')
    if len(manifest.get('rule_groups',[]))!=3 or len(manifest.get('provenance_maps',[]))!=2: raise SystemExit('cycle3 cumulative routing missing')
    if manifest['rules_path']!='libraries/rosenthal/rules-index.json': raise SystemExit('manifest must route through cumulative index')
    for fp in idx['source_fingerprints']:
        if fp not in manifest['source_version']: raise SystemExit(f'manifest missing fingerprint {fp}')
    required=['source.md','coverage.md','observations.json','concepts.md','rules.md','interactions.md','claims.md','current-norm.md','integration-matrix.md','evals.json','eval-map.json','audit.md']
    for study_name in ['rosenthal-a-kak-luchshe-skazat','rosenthal-pravopisanie-proiznoshenie-redaktirovanie']:
        study=ROOT/'studies'/study_name
        for name in required:
            if not (study/name).is_file(): raise SystemExit(f'missing study artifact: {study_name}/{name}')
    for name in o3.get('observation_parts',[]):
        if not (ROOT/'studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie'/name).is_file(): raise SystemExit(f'missing cycle3 observation part: {name}')
    e2=load('studies/rosenthal-a-kak-luchshe-skazat/evals.json')['cases']; m2=load('studies/rosenthal-a-kak-luchshe-skazat/eval-map.json')['map']
    if len(e2)!=12 or {x['id'] for x in e2}!={x['eval_id'] for x in m2}: raise SystemExit('cycle2 eval map mismatch')
    e3=load('studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/evals.json')['cases']; m3=load('studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/eval-map.json')['map']
    if len(e3)!=16 or {x['id'] for x in e3}!={x['eval_id'] for x in m3}: raise SystemExit('cycle3 eval map mismatch')
    if {x['rule_id'] for x in m3}-{x['rule_id'] for x in items}: raise SystemExit('cycle3 eval maps unknown rules')
    if len(cases)<15: raise SystemExit('too few cumulative Rosenthal mechanical controls')
    norm3=(ROOT/'studies/rosenthal-pravopisanie-proiznoshenie-redaktirovanie/current-norm.md').read_text(encoding='utf-8')
    for needle in ['gramota.ru/meta/ambitsioznyy','gramota.ru/meta/agressivnyy','query=%D0%BF%D1%80%D0%B0%D1%87%D0%B5%D1%87%D0%BD%D0%B0%D1%8F','OBSOLETE','SOURCE_PERIOD']:
        if needle not in norm3: raise SystemExit(f'missing cycle3 current-norm evidence/boundary: {needle}')
    gal=load('libraries/gal/rules/editor_workflow.json')['rules']
    if not any(x.get('phenomenon_id')=='editing.local_change_whole_fit' for x in gal): raise SystemExit('expected cross-school whole-fit overlap with Gal')
    c3p={x['phenomenon_id'] for x in c3['rules']}
    if len(c3p)!=15: raise SystemExit('duplicate cycle3 phenomenon_id')
    print(f'rosenthal cumulative library: {len(items)} rules; automation {counts}; cycle3 95 observations, 15 new MODEL_ONLY rules, 56 enriched rules, {len(e3)} preservation/context evals; OK')
if __name__=='__main__': main()
