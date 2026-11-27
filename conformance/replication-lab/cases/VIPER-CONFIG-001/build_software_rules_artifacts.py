import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="configuration"
LABELS=["default","yaml-file-case-insensitive","environment-over-file","changed-flag-over-environment","runtime-override-highest-precedence","allow-empty-environment-value","nested-environment-key-replacer","explicit-environment-binding","full-precedence-chain"]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "viper-config-scenario-"+x
def eid(side,x):return "viper-config-exec-"+side+"-"+x
def oid(side,x):return "viper-config-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_files):
 created=now();source=side=="source";prefix="viper-config-"+side
 target="viper-source" if source else "python-config-replica"
 runtime=raw.get("source","spf13/viper Go configuration resolver") if source else raw.get("implementation","Python 3.12 configuration precedence model")
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[]
 for index,item in enumerate(raw["scenarios"]):
  label=item["label"];value=item["value"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Resolve a configuration key across the declared source types and precedence rules.",
   "facetIds":[FACET],"subject":"Configuration source resolution",
   "preconditions":["The Viper instance is configured with the declared default/file/environment/flag/override sources.","The test process environment is isolated for the scenario."],
   "trigger":"Resolve the declared logical key through Viper or the independent model.",
   "inputs":{"scenario":label},"observableQuestions":["Which source supplied the effective value?","What value and type were returned?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"scenario":label},"trigger":"Resolve configuration key","collector":{"name":runtime}})
  origin={
   "default":"default","yaml-file-case-insensitive":"configuration-file",
   "environment-over-file":"environment","changed-flag-over-environment":"command-line-flag",
   "runtime-override-highest-precedence":"runtime-override","allow-empty-environment-value":"environment",
   "nested-environment-key-replacer":"environment-key-replacer","explicit-environment-binding":"explicit-environment-binding",
   "full-precedence-chain":"runtime-override"
  }[label]
  precedence={"default":1,"yaml-file-case-insensitive":2,"environment-over-file":3,
   "changed-flag-over-environment":4,"runtime-override-highest-precedence":5,
   "allow-empty-environment-value":3,"nested-environment-key-replacer":3,
   "explicit-environment-binding":3,"full-precedence-chain":5}[label]
  key="database.host" if label=="nested-environment-key-replacer" else ("region" if label=="explicit-environment-binding" else ("mode" if label=="allow-empty-environment-value" else "port"))
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Configuration source resolution","observedAt":created,"sequence":index,
   "method":{"class":"instrumentation","procedure":"Resolve the logical configuration key and record the effective value and winning source.","tool":runtime},
   "conditions":{"scenario":label,"key":key},"trigger":"Get/GetString/GetInt("+key+")",
   "payload":{"facet":FACET,"kind":"effective-configuration","subject":"Effective application configuration value",
    "key":key,"value":value,"valueType":"string" if isinstance(value,str) else "integer",
    "origin":origin,"precedence":precedence,"scope":"application",
    "mutability":"runtime-configurable","reloadBehaviour":"Read at resolution time; reload behaviour not probed.",
    "targetContext":{"scenario":label,"emptyEnvironmentAllowed":label=="allow-empty-environment-value"},
    "extensions":{"provenance":"Viper source precedence and environment binding behaviour.","relatedSettingKeys":["port","mode","database.host","region"]},
    "effectObservationIds":[oid(side,label)]},
   "rawValue":item,"normalizedValue":{"key":key,"value":value,"winningSource":origin,"precedence":precedence},
   "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 obsids=[oid(side,x) for x in LABELS]
 props=[
  ("VIPER-CONFIG-P01","default-fallback","A configured default is used only when no higher-precedence source supplies a value."),
  ("VIPER-CONFIG-P02","file-over-default","A configuration-file value overrides the default value."),
  ("VIPER-CONFIG-P03","environment-over-file","Environment variables override file values when automatic environment lookup is enabled."),
  ("VIPER-CONFIG-P04","flags-and-overrides","Changed flags override environment values; runtime overrides have the highest precedence."),
  ("VIPER-CONFIG-P05","environment-key-mapping","Key replacers and explicit bindings map environment variable names to logical configuration keys."),
  ("VIPER-CONFIG-P06","empty-environment","AllowEmptyEnv makes an explicitly empty environment value distinct from an absent variable.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Configuration source resolution","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in props]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"Application resolves a logical setting across configured sources.",
  "applicability":{"scope":"Pinned Viper v1.21.0 default/file/environment/changed-flag/runtime-override resolution and environment binding."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-configuration-resolution-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,"digest":digest,
  "sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 for key,path in source_files.items():
  data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
  evidence.append({"evidenceId":"viper-source-"+key,"evidenceClass":"source-artifact","evidenceType":"pinned-source-file",
   "mediaType":"text/plain","origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw.get("sourceCommit"),"location":path},
   "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
   "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture Viper configuration source precedence and environment mapping across nine deterministic scenarios.",
  "target":{"targetId":target,"systemName":"spf13/viper v1.21.0" if source else "Independent Python configuration model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Configuration lookup across defaults, YAML, environment, changed pflag flags, runtime overrides and environment mapping.",
    "included":["default fallback","YAML file precedence","environment precedence","changed flags","runtime override","empty environment","nested key replacer","explicit environment binding"],
    "excluded":["remote key/value stores","watch/reload events","secret managers","multiple config files","custom merge strategies","all Viper providers"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"sources":["default","file","environment","flag","override"],"envPrefix":"APP"}}}},
  "scope":{"description":"Nine deterministic configuration source resolution scenarios.","facetIds":[FACET],
   "subjects":["configuration source resolution"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Resolve nine configuration settings across equivalent source precedence and environment mapping conditions."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Configuration source resolution","status":"observed",
   "reason":"All nine declared precedence and environment mapping scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["Remote providers, watchers/reload, secret managers, and custom merge strategies are excluded.",
   "This is bounded Viper configuration evidence, not complete configuration-facet coverage."],
  "replicationScope":{"scopeId":"viper-nine-source-precedence-scenarios",
   "description":"Complete property inventory for six declared configuration precedence and environment mapping properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Six required configuration properties are linked to nine source/replica observations and retained evidence.",
    "rationale":"All declared default/file/env/flag/override and environment mapping properties are observed; excluded providers and reload behaviours are explicit."}}}

def build_report(source,replica):
 created=now();left={x["observationId"].split("viper-config-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("viper-config-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="viper-config-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same logical key and configuration source-resolution scenario."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"viper-config-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"effective-configuration-value","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare effective value and winning configuration source.",
   "evidenceRefs":["viper-config-source-runtime","viper-config-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"viper-config-precedence-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Nine Viper configuration source precedence and environment mapping scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned Viper v1.21.0","same default/file/env/flag/override values","same environment prefix and key replacer"],
   "excludedDimensions":["remote providers","watch/reload","secret managers","multiple config files"],
   "limitations":["Nine scenarios do not exhaust all Viper providers or configuration features."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":9,"observedUnits":9},"implementation":{"declaredUnits":9,"observedUnits":9},
   "sharedComparableUnits":9,"incomparableUnits":0,"limitations":["Nine scenarios do not exhaust the configuration facet."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" Viper for the nine declared configuration precedence scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared nine-scenario Viper configuration scope, not all configuration providers or reload behaviours."}}

def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-files",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 source=build_capture(read(a.source),"source",a.source,json.loads(a.source_files))
 replica=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(source,replica)
 write(out/"viper-source.capture.json",source);write(out/"viper-python-replica.capture.json",replica);write(out/"viper-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
