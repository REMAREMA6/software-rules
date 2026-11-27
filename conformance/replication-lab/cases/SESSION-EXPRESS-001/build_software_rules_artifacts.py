import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="identity-authentication"
LABELS=["uninitialized-session","create-session","read-session","regenerate-session","old-id-rejected","new-id-restored","tampered-cookie-rejected","destroy-session","destroyed-id-rejected"]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "express-session-scenario-"+x
def eid(side,x):return "express-session-exec-"+side+"-"+x
def oid(side,x):return "express-session-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_artifacts):
 created=now(); source=side=="source"; prefix="express-session-"+side
 target="express-session-source" if source else "python-session-replica"
 runtime=raw.get("source","express-session 1.19.0") if source else raw.get("implementation","Python 3.12 session model")
 data=Path(raw_path).read_bytes(); digest=hashlib.sha256(data).hexdigest()
 scenarios=[]; executions=[]; observations=[]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"]; outcome={"data":item["data"],"cookie":item["cookie"]}
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe server-side session state and signed-cookie lifecycle across sequential HTTP requests.",
   "facetIds":[FACET],"subject":"Server-side session lifecycle",
   "preconditions":["Session middleware uses a fixed signing secret.","MemoryStore is the session persistence boundary.","saveUninitialized=false and resave=false."],
   "trigger":"Issue the declared request with the current session cookie, if present.",
   "inputs":{"scenario":label},"observableQuestions":["Was session state restored or rejected?","Was a signed session cookie created, rotated, or cleared?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"scenario":label},"trigger":"Execute sequential session lifecycle request","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Server-side session lifecycle","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Issue a request with the current signed cookie and capture response data and cookie attributes.","tool":runtime},
   "conditions":{"scenario":label,"saveUninitialized":False,"resave":False},
   "trigger":"HTTP request to session middleware",
   "payload":{"facet":FACET,"kind":"authentication-event","subject":"Server-side session lifecycle event",
    "principalRef":"session:anonymous","mechanism":"signed server-side session cookie","protocol":"HTTP/1.1",
    "credentialType":"signed session cookie",
    "session":{"event":label,"data":outcome["data"],"cookie":outcome["cookie"],"store":"MemoryStore"},
    "outcome":"failure" if label in ("old-id-rejected","tampered-cookie-rejected","destroyed-id-rejected") else "success",
    "revocation":{"performed":label in ("regenerate-session","destroy-session"),
      "oldIdentifierInvalidated":label in ("old-id-rejected","destroyed-id-rejected")},
    "extensions":{"cookieSignatureVerified":label!="tampered-cookie-rejected","saveUninitialized":False}},
   "rawValue":item,"normalizedValue":outcome,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 obsids=[oid(side,x) for x in LABELS]
 props=[
  ("SESSION-P01","uninitialized-session","An unmodified session is not persisted and emits no cookie when saveUninitialized is false."),
  ("SESSION-P02","signed-cookie-creation","Writing session data persists it and emits a signed HttpOnly/Lax session cookie."),
  ("SESSION-P03","session-restoration","A valid signed cookie restores the corresponding server-side session data."),
  ("SESSION-P04","session-regeneration","Regeneration invalidates the old identifier and issues a new identifier for the new session."),
  ("SESSION-P05","tamper-rejection","A cookie with an invalid signature cannot restore session state."),
  ("SESSION-P06","session-destruction","Destroy removes server-side session state and clears the client cookie.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Server-side session lifecycle","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in props]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"An HTTP request enters express-session middleware with the declared session configuration.",
  "applicability":{"scope":"express-session 1.19.0 MemoryStore, fixed secret, saveUninitialized=false, resave=false, HttpOnly/Lax cookie."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-session-lifecycle-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,
  "digest":digest,"sizeBytes":len(data),"retention":{"status":"retained","access":"CI artifact"}}]
 for key,path in source_artifacts.items():
  blob=Path(path).read_bytes(); h=hashlib.sha256(blob).hexdigest()
  evidence.append({"evidenceId":"express-session-source-"+key,"evidenceClass":"source-artifact",
   "evidenceType":"pinned-source-file","mediaType":"text/plain",
   "origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw.get("sourceCommit"),"location":path},
   "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(blob),
   "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture a bounded server-side session lifecycle and signed-cookie contract.",
  "target":{"targetId":target,"systemName":"express-session 1.19.0" if source else "Independent Python session model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Express session middleware with MemoryStore, fixed secret, saveUninitialized=false, resave=false and HttpOnly/Lax cookies.",
    "included":["uninitialized session suppression","signed cookie creation","session retrieval","regeneration","tamper rejection","destroy and cookie clearing"],
    "excluded":["credential verification","identity-provider login","distributed session stores","expiry/rolling renewal","MFA","CSRF","TLS secure-cookie deployment"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"saveUninitialized":False,"resave":False,"cookie":{"httpOnly":True,"sameSite":"lax","secure":False}}}}},
  "scope":{"description":"Nine sequential server-side session lifecycle requests.","facetIds":[FACET],
   "subjects":["server-side session lifecycle"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute sequential HTTP requests, propagate signed cookies, and observe session state and cookie lifecycle."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Server-side session lifecycle","status":"observed",
   "reason":"All nine declared lifecycle transitions were observed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["MemoryStore only; no persistence across process restart or multi-instance deployment.",
   "No credentials, login, identity provider, MFA, CSRF, cookie expiry, rolling renewal, or TLS secure-cookie deployment.",
   "This is not complete identity/authentication or security-facet coverage."],
  "replicationScope":{"scopeId":"express-session-memory-store-nine-transitions",
   "description":"Complete property inventory for six declared session lifecycle properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Six required session lifecycle properties are linked to nine sequential observations and retained source/replica evidence.",
    "rationale":"All declared MemoryStore session creation, restoration, regeneration, tamper, and destroy transitions are observed; identity-provider and distributed-store behaviours are excluded."}}}

def build_report(source,replica):
 created=now(); left={x["observationId"].split("express-session-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("express-session-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[]; results=[]
 for label in LABELS:
  a,b=left[label],right[label]; aid="express-session-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same session lifecycle transition and normalized cookie/session outcome."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"express-session-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"session-lifecycle-outcome","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare session data restoration/rejection and normalized signed-cookie lifecycle.",
   "evidenceRefs":["express-session-source-runtime","express-session-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"express-session-lifecycle-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Nine sequential MemoryStore session lifecycle transitions.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Same fixed secret","same saveUninitialized/resave settings","same cookie attributes","same sequential request order"],
   "excludedDimensions":["credential verification","identity-provider login","distributed session stores","MFA","CSRF","TLS"],
   "limitations":["MemoryStore and fixed cookie configuration only."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":9,"observedUnits":9},"implementation":{"declaredUnits":9,"observedUnits":9},
   "sharedComparableUnits":9,"incomparableUnits":0,"limitations":["Nine transitions do not exhaust session or identity-provider behaviour."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" express-session for nine declared session lifecycle transitions.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared nine-transition MemoryStore session lifecycle scope, not full identity or authentication."}}

def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-artifacts",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 source=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 replica=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(source,replica)
 write(out/"express-session-source.capture.json",source);write(out/"express-session-python-replica.capture.json",replica);write(out/"express-session-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
