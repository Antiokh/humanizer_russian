#!/usr/bin/env python3
"""Optional evidence-provider runtime with fail-open hard timeouts."""
from __future__ import annotations
import importlib.util, json, multiprocessing as mp, os, queue, time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "evidence"
DEFAULT_BUDGET_MS = 1200
GLOBAL_DISABLE_VALUES = {"0", "false", "off", "disabled", "no"}

def load_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))

def provider_manifests(include_disabled=False):
    out=[]
    for path in sorted(EVIDENCE_ROOT.glob("*/provider.json")):
        if path.parent.name.startswith("_"): continue
        item=load_json(path); item["_manifest_path"]=str(path.relative_to(ROOT))
        if include_disabled or item.get("enabled_by_default", False): out.append(item)
    return out

def evidence_globally_enabled():
    return os.getenv("HUMANIZER_EVIDENCE", "").strip().lower() not in GLOBAL_DISABLE_VALUES

def _safe_module_path(relative):
    path=(ROOT/relative).resolve()
    if ROOT != path and ROOT not in path.parents: raise ValueError(f"evidence module escapes repository root: {relative}")
    if not path.is_file(): raise FileNotFoundError(f"evidence module missing: {relative}")
    return path

def _import_module(relative):
    path=_safe_module_path(relative)
    spec=importlib.util.spec_from_file_location("humanizer_evidence_"+path.stem, path)
    if spec is None or spec.loader is None: raise RuntimeError(f"cannot import evidence module: {relative}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def normalize_evidence(item, manifest):
    required={"phenomenon_id","direction","target_scope","reason"}; missing=sorted(required-set(item))
    if missing: raise ValueError(f"{manifest['id']} evidence missing fields: {', '.join(missing)}")
    out=dict(item); out["provider_id"]=manifest["id"]; out.setdefault("evidence_type",manifest["evidence_type"])
    out.setdefault("strength","UNSPECIFIED"); out.setdefault("scope",""); out.setdefault("line",0); out.setdefault("excerpt",""); out.setdefault("provenance",[])
    return out

def _worker(module_path, text, context, timeout_ms, out_queue):
    try:
        module=_import_module(module_path)
        if not hasattr(module,"collect"): raise AttributeError(f"{module_path} must export collect(text, context=..., timeout_ms=...)")
        result=module.collect(text, context=context, timeout_ms=timeout_ms)
        if not isinstance(result,dict): raise TypeError("evidence collect() must return a dict")
        out_queue.put({"ok":True,"result":result})
    except BaseException as exc:
        out_queue.put({"ok":False,"error_type":type(exc).__name__,"message":str(exc)[:500]})

def _ctx():
    methods=mp.get_all_start_methods(); return mp.get_context("fork" if "fork" in methods else "spawn")

def _status(provider_id,status,started,count=0,message=""):
    return {"provider_id":provider_id,"status":status,"elapsed_ms":round((time.perf_counter()-started)*1000,1),"evidence_count":count,"message":message}

def run_provider(manifest, text, context=None, *, hard_timeout_ms=None):
    started=time.perf_counter(); pid=manifest["id"]
    if manifest.get("status")!="OPERATIONAL": return [],_status(pid,"UNAVAILABLE",started,message=f"status={manifest.get('status')}")
    module_path=manifest.get("module_path")
    if not module_path: return [],_status(pid,"UNAVAILABLE",started,message="module_path is not configured")
    timeout_ms=max(25,int(hard_timeout_ms or manifest.get("timeout_ms",800)))
    ctx=_ctx(); q=ctx.Queue(maxsize=1); proc=ctx.Process(target=_worker,args=(module_path,text,context or {},timeout_ms,q),daemon=True)
    proc.start(); proc.join(timeout_ms/1000)
    if proc.is_alive():
        proc.terminate(); proc.join(0.2); return [],_status(pid,"TIMEOUT",started,message=f"hard timeout {timeout_ms} ms")
    try: payload=q.get(timeout=0.1)
    except queue.Empty: payload={"ok":False,"error_type":"ProviderProcessError","message":f"provider process exited with code {proc.exitcode} without a result"}
    if not payload.get("ok"):
        status=_status(pid,"UNAVAILABLE",started,message=f"{payload.get('error_type','Error')}: {payload.get('message','')}")
        if manifest.get("failure_policy","SKIP")=="ERROR": raise RuntimeError(f"{pid}: {status['message']}")
        return [],status
    items=[normalize_evidence(x,manifest) for x in payload["result"].get("evidence",[])]
    return items,_status(pid,"OK",started,count=len(items))

def _resolve_requested(provider_ids):
    if provider_ids is None: return []
    if provider_ids=="auto": return [m for m in provider_manifests(False) if m.get("status")=="OPERATIONAL"]
    all_items=provider_manifests(True); by_id={m["id"]:m for m in all_items}
    if provider_ids=="all": return all_items
    missing=sorted(set(provider_ids)-set(by_id))
    if missing: raise ValueError(f"unknown evidence providers: {', '.join(missing)}")
    return [by_id[x] for x in provider_ids]

def run_evidence(text, provider_ids, *, context=None, budget_ms=None):
    manifests=_resolve_requested(provider_ids)
    if not manifests: return [],[]
    if not evidence_globally_enabled():
        return [],[{"provider_id":m["id"],"status":"DISABLED","elapsed_ms":0.0,"evidence_count":0,"message":"disabled by HUMANIZER_EVIDENCE"} for m in manifests]
    budget_ms=max(25,int(budget_ms or os.getenv("HUMANIZER_EVIDENCE_BUDGET_MS",DEFAULT_BUDGET_MS))); deadline=time.perf_counter()+budget_ms/1000
    evidence=[]; statuses=[]
    for manifest in manifests:
        remaining=int((deadline-time.perf_counter())*1000)
        if remaining<=0:
            statuses.append({"provider_id":manifest["id"],"status":"TIMEOUT","elapsed_ms":0.0,"evidence_count":0,"message":f"global evidence budget {budget_ms} ms exhausted"}); continue
        items,status=run_provider(manifest,text,context=context,hard_timeout_ms=min(int(manifest.get("timeout_ms",remaining)),remaining))
        evidence.extend(items); statuses.append(status)
    return evidence,statuses

def _self_test():
    planned={"id":"planned","status":"PLANNED","evidence_type":"CORPUS_USAGE","failure_policy":"SKIP","timeout_ms":50}
    items,status=run_provider(planned,"текст"); assert items==[] and status["status"]=="UNAVAILABLE"
    fast={"id":"fast","status":"OPERATIONAL","evidence_type":"CORPUS_USAGE","failure_policy":"SKIP","timeout_ms":250,"module_path":"tests/fixtures/evidence_fast.py"}
    items,status=run_provider(fast,"Ну вот.",context={"findings":[]}); assert status["status"]=="OK" and items and items[0]["provider_id"]=="fast",status
    slow={"id":"slow","status":"OPERATIONAL","evidence_type":"CORPUS_USAGE","failure_policy":"SKIP","timeout_ms":30,"module_path":"tests/fixtures/evidence_slow.py"}
    items,status=run_provider(slow,"текст"); assert items==[] and status["status"]=="TIMEOUT",status
    print("evidence runtime self-test: OK")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--self-test",action="store_true"); a=p.parse_args()
    if a.self_test: _self_test()
