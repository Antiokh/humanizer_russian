#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    base=load('libraries/rosenthal/rules.json'); c2=load('libraries/rosenthal/rules-cycle2.json'); idx=load('libraries/rosenthal/rules-index.json'); manifest=load('libraries/rosenthal/library.json'); prov=load('libraries/rosenthal/provenance-cycle2.json'); obs=load('studies/rosenthal-a-kak-luchshe-skazat/observations.json'); cases=load('tests/rosenthal_cases.json')['cases']
    items=base['rules']+c2['rules']; ids=[x['rule_id'] for x in items]
    expected=[f'ROS-R{i:02d}' for i in range(1,47)]+[f'ROS-R{i}' for i in range(47,60)]
    if ids!=expected: raise SystemExit(f'Rosenthal IDs are not cumulative/contiguous: {ids[-15:]}')
    counts={k:sum(x['automation_level']==k for x in items) for k in ['HARD_GATE','DEFAULT_MECHANICAL','EXTENDED_SOFT','METRIC_ONLY','MODEL_ONLY']}
    if counts!=idx['automation_counts']: raise SystemExit(f'automation mismatch {counts} != {idx["automation_counts"]}')
    if idx['total_rule_count']!=59 or len(items)!=59: raise SystemExit('expected 59 cumulative Rosenthal rules')
    if c2['rule_count']!=13 or c2['automation_counts']!={'HARD_GATE':0,'DEFAULT_MECHANICAL':0,'EXTENDED_SOFT':1,'METRIC_ONLY':0,'MODEL_ONLY':12}: raise SystemExit('cycle2 split mismatch')
    if obs['atomic_observation_count']!=63 or len(obs['observations'])!=63: raise SystemExit('cycle2 observation count mismatch')
    defaults=obs.get('card_defaults',{}); required_fields=obs.get('required_resolved_fields',[])
    if not required_fields: raise SystemExit('cycle2 atomic-card contract missing')
    seen_obs=set()
    for card in obs['observations']:
        oid=card.get('observation_id')
        if not oid or oid in seen_obs: raise SystemExit(f'duplicate/missing observation id: {oid}')
        seen_obs.add(oid); resolved={**defaults,**card}
        missing=[f for f in required_fields if f not in resolved or resolved[f] in (None,'')]
        if missing: raise SystemExit(f'{oid}: unresolved atomic-card fields: {missing}')
        if resolved['current_status'] not in {'CURRENT_CONFIRMED','CURRENT_USAGE','SOURCE_PERIOD','CONTESTED','OBSOLETE'}: raise SystemExit(f'{oid}: invalid current_status {resolved["current_status"]}')
        if resolved['project_class'] not in {'NORM','NATIVE_USAGE','EDITING','REGISTER','AI_CALQUE','AUTHOR','HISTORICAL'}: raise SystemExit(f'{oid}: invalid project_class {resolved["project_class"]}')
    if prov['existing_rules_enriched']!=27 or len(prov['map'])!=27: raise SystemExit('cycle2 provenance enrichment mismatch')
    if manifest['source_branch']!='rosenthal' or manifest['adapter']!='review_v1': raise SystemExit('manifest routing mismatch')
    if len(manifest.get('rule_groups',[]))!=2 or manifest['rules_path']!='libraries/rosenthal/rules-index.json': raise SystemExit('cumulative rule routing missing')
    for fp in idx['source_fingerprints']:
        if fp not in manifest['source_version']: raise SystemExit(f'manifest missing fingerprint {fp}')
    required=['source.md','coverage.md','observations.json','concepts.md','rules.md','interactions.md','claims.md','current-norm.md','integration-matrix.md','evals.json','eval-map.json','audit.md']
    study=ROOT/'studies/rosenthal-a-kak-luchshe-skazat'
    for name in required:
        if not (study/name).is_file(): raise SystemExit(f'missing cycle2 study artifact: {name}')
    evals=load('studies/rosenthal-a-kak-luchshe-skazat/evals.json')['cases']; emap=load('studies/rosenthal-a-kak-luchshe-skazat/eval-map.json')['map']
    if len(evals)!=12 or {x['id'] for x in evals}!={x['eval_id'] for x in emap}: raise SystemExit('cycle2 eval map mismatch')
    if len(cases)<15: raise SystemExit('too few cumulative Rosenthal mechanical controls')
    norm=(study/'current-norm.md').read_text(encoding='utf-8')
    for needle in ['gramota.ru/journal/stati/nauka/bolee-luchshe-bolee-veselee','gramota.ru/spravka/vopros/331581','самый лучший']:
        if needle not in norm: raise SystemExit(f'missing current-norm evidence/boundary: {needle}')
    print(f'rosenthal cumulative library: {len(items)} rules; automation {counts}; cycle2 63 observations, 13 new rules, 27 enriched rules, {len(cases)} mechanical controls; OK')
if __name__=='__main__': main()
