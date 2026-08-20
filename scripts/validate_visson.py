#!/usr/bin/env python3
"""Validate complete Lynn Visson study, integration matrix and runtime adapter."""
from __future__ import annotations
import importlib.util, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SHA="45cd09d0101caa90effa2f7943d4ddf45659536857ae548910fccad144c806ca"
EXPECTED_CLASSES={"NORM":2,"NATIVE_USAGE":22,"EDITING":2,"AI_CALQUE":13}
EXPECTED_AUTO={"HARD_GATE":0,"DEFAULT_MECHANICAL":2,"EXTENDED_SOFT":3,"METRIC_ONLY":2,"MODEL_ONLY":32}
REQUIRED={"rule_id","phenomenon_id","source_locator","provenance","project_class","semantic_invariant","scope","automation_level","surface_trigger","required_context","false_positive_risk","positive_case","natural_negative_control","boundary_case","intentional_counterexample","existing_overlap","planned_module","runtime_visibility","english_pattern","russian_native_pattern","likely_interference","diagnosis","possible_russian_repairs","operation","do_not_infer"}

def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def main():
    failures=[]
    def check(c,m):
        if not c: failures.append(str(m))
    source=(ROOT/'studies/lynn-visson/source.md').read_text(encoding='utf-8')
    coverage=(ROOT/'studies/lynn-visson/coverage.md').read_text(encoding='utf-8')
    audit=(ROOT/'studies/lynn-visson/audit.md').read_text(encoding='utf-8')
    obs=(ROOT/'studies/lynn-visson/observations.md').read_text(encoding='utf-8')
    matrix=(ROOT/'studies/lynn-visson/integration-matrix.md').read_text(encoding='utf-8')
    for marker in [SHA,'55/55 content XHTML documents','117/117 endnotes','index_split_002.xhtml','index_split_056.xhtml']:
        check(marker in source,f"source missing {marker}")
    for marker in ['55/55','117/117','Inaccessible or unread parts: **none**']:
        check(marker in coverage,f"coverage missing {marker}")
    check(len(re.findall(r"`V-OBS-\d{2}`",obs))==72,'atomic observation count != 72')
    check('OPERATIONAL' in audit,'audit status')
    for marker in ['39','DEFAULT_MECHANICAL','MODEL_ONLY','VISSON-NORM-ASK-QUESTION','VISSON-CALQUE-PRETEND-CLAUSE']:
        check(marker in matrix,f"matrix missing {marker}")

    index=load('libraries/visson/rules.json'); rules=[]
    for rel in index['groups']: rules.extend(load(rel)['rules'])
    check(index.get('source_fingerprint_sha256')==SHA,'rules source fingerprint')
    check(index.get('rule_count')==39 and len(rules)==39,'rule count')
    ids=[r['rule_id'] for r in rules]; check(len(ids)==len(set(ids)),'duplicate rule ids')
    for r in rules:
        miss=REQUIRED-set(r); check(not miss,f"{r.get('rule_id')}: missing {sorted(miss)}")
        check(r.get('rule_id','').startswith('VISSON-'),r.get('rule_id'))
    classes=dict(Counter(r['project_class'] for r in rules)); auto=dict(Counter(r['automation_level'] for r in rules))
    for k in EXPECTED_AUTO: auto.setdefault(k,0)
    check(classes==EXPECTED_CLASSES,classes); check(auto==EXPECTED_AUTO,auto)
    model_ids={r['rule_id'] for r in rules if r['automation_level']=='MODEL_ONLY'}
    residue=(ROOT/'libraries/visson/model-only.md').read_text(encoding='utf-8')
    check(not [x for x in model_ids if f'`{x}`' not in residue],'model-only residue incomplete')

    manifest=load('libraries/visson/library.json'); reviewer=load('reviewers/visson.json')
    check(manifest.get('adapter')=='review_v1','adapter'); check(manifest.get('source_branch')=='visson','branch')
    check(manifest.get('status')=='OPERATIONAL','manifest status'); check(manifest.get('enabled_by_default') is True,'enabled')
    check(reviewer.get('library_id')=='visson','reviewer library'); check(reviewer.get('avatar') is None,'reviewer avatar')
    check('не реальная рецензия' in reviewer.get('disclaimer','').casefold(),'reviewer disclaimer')
    for ref in manifest.get('references',[]): check((ROOT/ref).is_file(),f'missing ref {ref}')

    suite=load('evals/lynn-visson.json'); mp=load('evals/lynn-visson-map.json')
    check(len(suite['evals'])==39 and len(mp['cases'])==39,'eval count')
    check([x['id'] for x in suite['evals']]==[x['id'] for x in mp['cases']],'eval map ids')
    check({x['rule_id'] for x in suite['evals']}==set(ids),'eval rule coverage')

    path=ROOT/'scripts/lint_visson.py'; spec=importlib.util.spec_from_file_location('lint_visson_validate',path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.self_test()
    sample=mod.review('Я хочу спросить у вас вопрос. Он претендует, что ничего не знает.')
    got={x['rule_id'] for x in sample['findings']}; check({'VISSON-NORM-ASK-QUESTION','VISSON-CALQUE-PRETEND-CLAUSE'}<=got,got)
    check(set(mod.METRIC_RULE_IDS)=={r['rule_id'] for r in rules if r['automation_level']=='METRIC_ONLY'},'metric ids drift')

    claims=(ROOT/'studies/lynn-visson/claims.md').read_text(encoding='utf-8')
    check('амбициозный проект' in claims and 'STRONGLY_NARROWED_2026' in claims,'ambitious narrowing missing')
    check('break → ломаться' in audit,'break provenance guard missing')

    if failures:
        print('Lynn Visson validation FAILED')
        for x in failures: print(f'- {x}')
        raise SystemExit(1)
    print(f"Lynn Visson validation: OK (55/55 content docs + 117/117 notes; 72 observations; 39 rules; classes={classes}; automation={auto})")
if __name__=='__main__': main()
