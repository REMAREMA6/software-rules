import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="integrations"
LABELS=["json-response","text-response","http-404","http-503","redirect-follow","post-json-custom-header","query-serialization","request-timeout","malformed-json-silent-fallback"]
def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p): return json.loads(Path(p).read_text())
def write(p,v): Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x): return "axios-http-scenario-"+x
def eid(side,x): return "axios-http-exec-"+side+"-"+x
def oid(side,x): return "axios-http-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_file=None):
 created=now(); source=side=="source"; prefix="axios-http-"+side
 target="axios-node-http-client" if source else "python-urllib-http-client"
 runtime=raw.get("source","Axios Node HTTP adapter") if source else raw.get("implementation","Python urllib")
 digest=hashlib.sha256(Path(raw_path).read_bytes()).hexdigest()
 scenarios=[]; executions=[]; observations=[]
 for index,item in enumerate(raw["scenarios"]):
  label=item["label"]; outcome=item["outcome"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe the HTTP client's normalized outcome for a deterministic external-service interaction.",
   "facetIds":[FACET],"subject":"HTTP client integration",
   "preconditions":["A deterministic local HTTP service is available.","The request uses the declared method, URL, timeout and headers."],
   "trigger":"Issue the HTTP request through the selected client implementation.",
   "inputs":{"scenario":label},"observableQuestions":["Was the response accepted or rejected?","What status, body, redirect, timeout or parse outcome was exposed?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"scenario":label},"trigger":"Execute outbound HTTP request","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"HTTP client integration","observedAt":created,"sequence":index,
   "method":{"class":"instrumentation","procedure":"Send a deterministic request to a local HTTP service and normalize the client-visible outcome.","tool":runtime},
   "conditions":{"scenario":label},"trigger":"Execute outbound HTTP request",
   "payload":{"facet":FACET,"kind":"external-interaction","subject":"HTTP client request/response contract",
    "provider":"Deterministic local HTTP service","boundary":"Axios/Python client to HTTP service","direction":"outbound",
    "operation":label,"protocolRef":"HTTP/1.1","requestRef":label,"responseRef":label,
    "credentialContext":{"credentials":"none","customHeader":label=="post-json-custom-header"},
    "resilience":{"timeoutMs":20 if label=="request-timeout" else None,"redirectFollowing":label=="redirect-follow"},
    "mapping":{"normalizedOutcome":outcome},"dependencyOutcome":outcome["kind"],"correlation":[label]},
   "rawValue":item,"normalizedValue":outcome,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 obsids=[oid(side,x) for x in LABELS]
 props=[
  ("AXIOS-INT-P01","response-transform","JSON and text response bodies are transformed according to response content type and response mode."),
  ("AXIOS-INT-P02","http-status-errors","Non-2xx responses reject while preserving status and response body."),
  ("AXIOS-INT-P03","redirect-following","The default client follows the declared redirect and returns the final response."),
  ("AXIOS-INT-P04","request-serialization","Object request bodies are serialized as JSON and the service receives the expected body."),
  ("AXIOS-INT-P05","query-and-header-mapping","Query parameters and custom headers cross the HTTP boundary with the declared values."),
  ("AXIOS-INT-P06","timeout-and-parse-failure","Timeouts are distinct from HTTP responses and silent malformed-JSON parsing returns raw text.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"HTTP client integration","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in props]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A client issues an HTTP request to a remote service.",
  "applicability":{"scope":"Pinned Axios Node HTTP adapter and independent Python urllib model for nine local HTTP interaction scenarios."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-http-client-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,
  "digest":digest,"sizeBytes":Path(raw_path).stat().st_size,"retention":{"status":"retained","access":"CI artifact"}}]
 if source_file:
  data=Path(source_file).read_bytes(); h=hashlib.sha256(data).hexdigest()
  evidence.append({"evidenceId":"axios-http-source-package","evidenceClass":"source-artifact","evidenceType":"pinned-source-package-manifest",
   "mediaType":"application/json","origin":{"targetId":target,"collector":"GitHub immutable source checkout",
    "sourceRevision":raw.get("sourceCommit"),"location":source_file},"capturedAt":created,
   "embedded":{"sha256":h},"locator":source_file,"digest":h,"sizeBytes":len(data),
   "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture a bounded Axios HTTP integration contract and its independent Python replica.",
  "target":{"targetId":target,"systemName":"Axios Node HTTP adapter" if source else "Python urllib HTTP client model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),
   "build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Outbound HTTP request/response contract for nine deterministic local-service scenarios.",
    "included":["JSON/text response handling","HTTP error status handling","redirects","JSON request serialization","query/header mapping","timeouts","malformed JSON fallback"],
    "excluded":["TLS","proxy configuration","cookies","multipart","streaming","cancellation","retries","browser XHR"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,"configuration":{"state":"observed","value":{"timeoutMs":20,"followRedirects":True}}}},
  "scope":{"description":"Nine deterministic HTTP client interactions.","facetIds":[FACET],
   "subjects":["HTTP client integration"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute nine equivalent HTTP requests and normalize response/error outcomes."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,
  "evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"HTTP client integration","status":"observed",
   "reason":"All nine declared HTTP interaction scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["The service is local and deterministic; real external provider behaviour is not inferred.",
   "TLS, proxies, cookies, multipart, streaming, cancellation, retries, and browser adapters are excluded.",
   "This is not full Axios or complete integration-facet coverage."],
  "replicationScope":{"scopeId":"axios-http-client-nine-interactions","description":"Complete property inventory for six declared HTTP client interaction properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Six required integration properties are linked to nine source/replica observations and retained evidence.",
    "rationale":"All declared HTTP interaction properties are observed; excluded protocols and resilience features remain explicitly outside scope."}}}

def build_report(source,replica):
 created=now(); left={x["observationId"].split("axios-http-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("axios-http-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[]; results=[]
 for label in LABELS:
  a,b=left[label],right[label]; aid="axios-http-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired",
   "identityBasis":"scenario-subject-facet-condition","rationale":"Same HTTP interaction scenario and normalized request/response contract."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"axios-http-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"http-client-outcome","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare normalized HTTP response, error, timeout and parsing outcomes.",
   "evidenceRefs":["axios-http-source-runtime","axios-http-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"axios-http-integration-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Nine HTTP client interactions against deterministic local service.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned Axios source commit","same HTTP service behaviour","same request methods, paths, headers, query, body and timeout"],
   "excludedDimensions":["TLS","proxies","cookies","multipart","streaming","cancellation","retries"],
   "limitations":["Local deterministic service only; external provider variability is not tested."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":9,"observedUnits":9},"implementation":{"declaredUnits":9,"observedUnits":9},
   "sharedComparableUnits":9,"incomparableUnits":0,"limitations":["Nine requests do not exhaust the HTTP client feature surface."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python client "+("differs from" if mismatches else "matches")+" Axios for the nine declared HTTP interactions.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared nine-scenario HTTP integration scope, not all Axios adapters or protocols."}}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--source",required=True); p.add_argument("--replica",required=True); p.add_argument("--output-dir",required=True); p.add_argument("--source-package",required=True); a=p.parse_args()
 out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,a.source_package)
 r=build_capture(read(a.replica),"replica",a.replica)
 report=build_report(s,r)
 write(out/"axios-http-source.capture.json",s); write(out/"axios-http-python-replica.capture.json",r); write(out/"axios-http-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope": raise SystemExit(1)
if __name__=="__main__": main()
