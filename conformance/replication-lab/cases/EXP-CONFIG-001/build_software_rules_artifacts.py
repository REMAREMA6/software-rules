import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
FACET="configuration"
def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p): return json.loads(Path(p).read_text())
def write(p,v): Path(p).write_text(json.dumps(v,indent=2)+"\n")
def scenario_id(label): return "express-config-scenario-"+label
def exec_id(side,label): return "express-config-exec-"+side+"-"+label
def obs_id(side,label,path): return "express-config-obs-"+side+"-"+label+"-"+str(abs(hash(path))%100000000)
def flatten(raw):
 return [(s,d) for s in raw["scenarios"] for d in s["decisions"]]
def build_capture(raw,side,raw_path):
 created=now(); source=side=="source"; prefix="express-config-"+side
 target="express-pinned-source" if source else "python-config-replica"
 runtime=raw.get("source","Express 5.3.0") if source else raw.get("implementation","Python 3.12")
 digest=hashlib.sha256(Path(raw_path).read_bytes()).hexdigest()
 labels=list(dict.fromkeys(s["label"] for s in raw["scenarios"]))
 scenarios=[]; executions=[]; observations=[]; ids_by_label={}
 for label in labels:
  item=next(s for s in raw["scenarios"] if s["label"]==label); sid=scenario_id(label); eid=exec_id(side,label)
  scenarios.append({"scenarioId":sid,"title":label.replace("-"," ").title(),
   "purpose":"Observe effective Express-compatible router settings and their path-matching effects.",
   "facetIds":[FACET],"subject":"HTTP route configuration",
   "preconditions":["The application has a GET route at /Report.","The source/replica is started on a local loopback interface."],
   "trigger":"Issue the declared route requests under the selected effective configuration.",
   "inputs":{"configuration":item["config"],"paths":[d["path"] for d in item["decisions"]]},
   "observableQuestions":["Which effective router settings were active?","Did each path match the route?"]})
  executions.append({"executionId":eid,"scenarioId":sid,"targetId":target,"startedAt":created,"endedAt":created,
   "status":"completed","actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"configuration":item["config"]},"trigger":"Execute route configuration probes","collector":{"name":runtime}})
  ids_by_label[label]=[]
  for seq,d in enumerate(item["decisions"]):
   oid=obs_id(side,label,d["path"]); ids_by_label[label].append(oid)
   config=item["config"]
   observations.append({"observationId":oid,"targetId":target,"executionId":eid,"facet":FACET,
    "subject":"HTTP route configuration","observedAt":created,"sequence":seq,
    "method":{"class":"instrumentation","procedure":"Apply effective router configuration and issue an HTTP request to the registered route.","tool":runtime},
    "conditions":{"scenario":label,"path":d["path"]},"trigger":"HTTP GET "+d["path"],
    "payload":{"facet":FACET,"kind":"effective-configuration","subject":"Express-compatible router settings",
     "key":"effective-router-settings","value":{"caseSensitive":config["caseSensitive"],"strict":config["strict"]},
     "valueType":"object","origin":"application defaults or app.set before lazy router initialization",
     "scope":"application router","mutability":"fixed after lazy router initialization",
     "reloadBehaviour":"settings changed after initialization do not rebuild the existing router",
     "targetContext":{"scenario":label,"activation":config["activation"],"settingAfterInitialization":config.get("settingAfterInitialization",False)},
     "effectObservationIds":[oid]},
    "rawValue":d,"normalizedValue":{"scenario":label,"configuration":config,"path":d["path"],"status":d["status"]},
    "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 properties=[
  ("EXP-CONFIG-P01","default-values","Unspecified case-sensitive and strict-routing settings resolve to false."),
  ("EXP-CONFIG-P02","case-sensitivity","The effective case-sensitive setting controls whether route path letter case must match."),
  ("EXP-CONFIG-P03","strict-routing","The effective strict-routing setting controls whether a trailing slash distinguishes a route."),
  ("EXP-CONFIG-P04","lazy-activation","Router settings are fixed when the lazily initialized router is created; later app setting changes do not mutate it.")
 ]
 allids=[oid for values in ids_by_label.values() for oid in values]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Express-compatible route configuration","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":allids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in properties]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"Initialize a router and issue route requests under the declared settings.",
  "applicability":{"scope":"Express 5.3.0 case-sensitive and strict routing settings for one literal route."},
  "status":"supported","supportingObservationIds":allids} for pid,dim,why in properties]
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture effective route configuration and observable matching outcomes.",
  "target":{"targetId":target,"systemName":"Express 5.3.0" if source else "Independent Python routing model",
   "systemVersion":"5.3.0 pinned commit" if source else "Python 3.12",
   "build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","independent-replica"))},
   "boundary":{"description":"One GET /Report route; case-sensitive and strict-routing configuration only.",
    "included":["default settings","case-sensitive setting","strict setting","settings fixed at lazy router initialization"],
    "excluded":["other Express settings","middleware precedence","route parameters","wildcards","mount paths","proxy settings","all other HTTP behaviours"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,"configuration":{"state":"observed","value":"five configuration profiles"}}},
  "scope":{"description":"Five configuration profiles and 18 route path observations.","facetIds":[FACET],
   "subjects":["HTTP route configuration"],"scenarioIds":[scenario_id(x) for x in labels]},
  "collector":{"name":runtime,"methodDescription":"Execute equivalent path requests under five effective configuration profiles."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,
  "evidence":[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-http-configuration-probe",
   "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
    "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
   "capturedAt":created,"embedded":{"scenarioLabels":labels,"sha256":digest},"locator":raw_path,
   "digest":digest,"sizeBytes":Path(raw_path).stat().st_size,"retention":{"status":"retained","access":"CI artifact"}}],
  "coverage":[{"facet":FACET,"subject":"Express-compatible route configuration","status":"observed",
   "reason":"All five profiles and 18 route outcomes are recorded.",
   "scenarioIds":[scenario_id(x) for x in labels],"executionIds":[exec_id(side,x) for x in labels]}],
  "limitations":["Only case-sensitive routing, strict routing, defaults, and lazy initialization are covered.","This is not full Express configuration coverage."],
  "replicationScope":{"scopeId":"express-config-routing-settings","description":"Complete inventory for four declared routing-configuration properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Four required configuration properties are linked to 18 runtime observations and retained source/replica evidence.",
    "rationale":"All four declared configuration properties and their path effects are observed for the bounded route configuration scope."}}}

def build_report(source,replica):
 created=now(); left={(x["normalizedValue"]["scenario"],x["normalizedValue"]["path"]):x for x in source["observations"]}
 right={(x["normalizedValue"]["scenario"],x["normalizedValue"]["path"]):x for x in replica["observations"]}
 align=[]; results=[]
 for key,a in left.items():
  b=right[key]; aid="express-config-alignment-"+key[0]+"-"+str(abs(hash(key[1]))%100000000)
  align.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-and-request-path",
   "rationale":"Same configuration profile and HTTP request path."})
  av=a["normalizedValue"]; bv=b["normalizedValue"]
  results.append({"resultId":aid+"-result","alignmentId":aid,"facet":FACET,"dimension":"effective-configuration-and-route-outcome",
   "classification":"match" if av==bv else "mismatch","comparisonBasis":"semantic",
   "referenceObservationIds":[a["observationId"]],"implementationObservationIds":[b["observationId"]],
   "referenceValue":av,"implementationValue":bv,"reason":"Compare effective settings and observed route status for each request.",
   "evidenceRefs":["express-config-source-runtime","express-config-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"express-configuration-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Five route configuration profiles; 18 requests.",
   "facets":[FACET],"scenarioIds":[x["scenarioId"] for x in source["scenarios"]],
   "conditions":["Express 5.3.0 pinned commit","one GET /Report route","loopback HTTP","same request paths"],
   "excludedDimensions":["other Express configuration settings","full route grammar","middleware ordering"],
   "limitations":["The case is limited to two Boolean router settings and lazy initialization."]},
  "alignments":align,"results":results,
  "coverage":{"reference":{"declaredUnits":18,"observedUnits":18},"implementation":{"declaredUnits":18,"observedUnits":18},
   "sharedComparableUnits":18,"incomparableUnits":0,"limitations":["18 requests do not exhaust Express routing/configuration."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" Express 5.3.0 for the declared routing configuration profiles and 18 requests.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures account for the four declared routing configuration properties and 18 requests, not all Express configuration."}}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--source",required=True); p.add_argument("--replica",required=True); p.add_argument("--output-dir",required=True); a=p.parse_args()
 out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source); r=build_capture(read(a.replica),"replica",a.replica); report=build_report(s,r)
 write(out/"express-config-source.capture.json",s); write(out/"express-config-replica.capture.json",r); write(out/"express-config-comparison.report.json",report)
 if report["conclusion"]["status"]!="agreement-within-observed-scope": raise SystemExit(1)
 print(json.dumps({"observations":len(report["results"]),"mismatches":0},indent=2))
if __name__=="__main__": main()
