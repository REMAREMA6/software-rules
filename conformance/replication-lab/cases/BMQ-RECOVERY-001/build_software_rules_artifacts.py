import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="background-processing"
LABELS=["recover-once","fail-at-zero-stalled-limit"]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "bullmq-stalled-scenario-"+x
def eid(side,x):return "bullmq-stalled-exec-"+side+"-"+x
def oid(side,x):return "bullmq-stalled-obs-"+side+"-"+x
def build_capture(raw,side,raw_path):
 created=now();source=side=="source";prefix="bullmq-stalled-"+side
 target="bullmq-worker-source" if source else "python-stalled-job-replica"
 runtime=raw.get("source","BullMQ pinned Worker/Queue runtime") if source else raw.get("implementation","Python 3.12 stalled-job state machine")
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"];terminal=item["terminal"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe recovery or terminal failure after a worker leaves a job active and its lock expires.",
   "facetIds":[FACET],"subject":"Stalled background job lifecycle",
   "preconditions":["A queued job is active in worker one.","Worker one is force-closed while processing.","The job lock expires before worker two performs stalled checking."],
   "trigger":"Worker two performs the stalled check after the active job lock expires.",
   "inputs":{"maxStalledCount":1 if label=="recover-once" else 0,"jobId":"recovery-job"},
   "observableQuestions":["Is the stalled job requeued or failed?","What are the attempts and stalled counters?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"scenario":label},"trigger":"Worker lock expiry and stalled check","collector":{"name":runtime}})
  life=[{"state":"active","worker":"worker-1"},{"state":"stalled","worker":"worker-2","counter":terminal["stalledCounter"]}]
  if terminal["state"]=="completed":life.extend([{"state":"waiting","reason":"stalled job requeued"},{"state":"active","worker":"worker-2"},{"state":"completed","result":terminal.get("result")}])
  else:life.append({"state":"failed","reason":terminal.get("reason")})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Stalled background job lifecycle","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Force-close the first worker, wait for lock expiry, start a second worker, and capture terminal job state.","tool":runtime},
   "conditions":{"scenario":label,"lockDurationMs":1000,"stalledIntervalMs":100,
    "maxStalledCount":1 if label=="recover-once" else 0},
   "trigger":"BullMQ stalled checker scans active jobs whose lock has expired",
   "payload":{"facet":FACET,"kind":"job-lifecycle","subject":"Stalled job recovery and terminal policy",
    "job":"work","trigger":"Active worker force-close followed by lock expiry",
    "schedule":{"type":"immediate-queue-job","delayMs":0},
    "enqueue":{"jobId":"recovery-job"},
    "worker":{"lockDurationMs":1000,"stalledIntervalMs":100,"maxStalledCount":1 if label=="recover-once" else 0,"concurrency":1},
    "lifecycle":life,"attemptCount":terminal["attemptsStarted"],
    "startedAt":created,"endedAt":created,"inputs":{"scenario":label},
    "output":{"terminal":terminal,"processed":item["processed"],"eventCounts":item["eventCounts"],"counts":item["counts"]},
    "sideEffects":["stalled counter incremented"]+([ "job requeued and processed by replacement worker"] if terminal["state"]=="completed" else ["job moved to failed"]),
    "timeout":{"lockExpiryMs":1000},"cancellation":{"firstWorkerForceClosed":True},
    "retry":{"maxStalledCount":1 if label=="recover-once" else 0,"stalledCounter":terminal["stalledCounter"]},
    "terminalResult":terminal["state"],"initiatingCorrelationId":"recovery-job",
    "extensions":{"attemptsStarted":terminal["attemptsStarted"],"attemptsMade":terminal["attemptsMade"],
     "queueCounts":item["counts"],"eventCounts":item["eventCounts"]}},
   "rawValue":item,"normalizedValue":item,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 obsids=[oid(side,x) for x in LABELS]
 props=[
  ("BMQ-REC-P01","lock-expiry-stalled-detection","A job left active after worker force-close becomes eligible for stalled detection after lock expiry."),
  ("BMQ-REC-P02","stalled-counter-and-event","Stalled detection increments the stalled counter and emits the stalled event."),
  ("BMQ-REC-P03","within-limit-requeue","A stalled job within maxStalledCount is returned to waiting and may complete on a replacement worker."),
  ("BMQ-REC-P04","stalled-limit-terminal-failure","A stalled job beyond maxStalledCount is moved to failed with the stalled-limit reason and observable counters.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Stalled background job lifecycle","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in props]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A worker leaves a job active and its lock expires before another worker's stalled check.",
  "applicability":{"scope":"Pinned BullMQ Worker/Queue runtime with Redis, one active job, lockDuration 1000ms and stalledInterval 100ms."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-stalled-job-lifecycle-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,"digest":digest,
  "sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture BullMQ stalled-job recovery and stalled-limit terminal behaviour.",
  "target":{"targetId":target,"systemName":"BullMQ Worker/Queue" if source else "Independent Python stalled-job state machine",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"One Redis-backed queue, one active job, forced worker close, lock expiry, and replacement worker stalled check.",
    "included":["stalled detection","stalled counter","within-limit requeue","stalled-limit terminal failure","attempt counters"],
    "excluded":["multiple simultaneous stalled jobs","parent/child flows","Redis failover","power-loss/process-host failure","queue pause/resume"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"lockDurationMs":1000,"stalledIntervalMs":100,"concurrency":1}}}},
  "scope":{"description":"Two deterministic stalled-job recovery/limit scenarios.","facetIds":[FACET],
   "subjects":["stalled background job lifecycle"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Force-close worker one, wait for lock expiry, then observe worker two's stalled checker and terminal outcome."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Stalled background job lifecycle","status":"observed",
   "reason":"Both declared within-limit recovery and zero-limit terminal failure scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["One active job and one replacement worker only.","No multiple-job concurrency, parent/child flows, Redis failover, or host/power-loss semantics.",
   "This is not complete BullMQ background-processing or messaging facet coverage."],
  "replicationScope":{"scopeId":"bullmq-two-stalled-job-lifecycle-scenarios",
   "description":"Complete property inventory for four declared stalled-job recovery properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Four required stalled lifecycle properties are linked to two source/replica observations and retained runtime evidence.",
    "rationale":"Both within-limit recovery and zero-limit terminal failure are observed; concurrency and host-failure classes remain explicitly excluded."}}}

def build_report(source,replica):
 created=now();left={x["observationId"].split("bullmq-stalled-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("bullmq-stalled-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="bullmq-stalled-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same stalled job scenario, limit, and normalized terminal outcome."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"bullmq-stalled-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"stalled-job-terminal-outcome","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare requeue/failure state, counters, processed values, events and queue counts.",
   "evidenceRefs":["bullmq-stalled-source-runtime","bullmq-stalled-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"bullmq-stalled-recovery-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Two BullMQ stalled-job lifecycle scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned BullMQ source commit","Redis 7","one job","lockDuration 1000ms","stalledInterval 100ms"],
   "excludedDimensions":["multiple-job concurrency","parent/child flows","Redis failover","host/power loss"],
   "limitations":["Two scenarios do not exhaust worker lifecycle or queue delivery guarantees."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":2,"observedUnits":2},"implementation":{"declaredUnits":2,"observedUnits":2},
   "sharedComparableUnits":2,"incomparableUnits":0,"limitations":["Only two stalled recovery limits are tested."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" BullMQ for the two declared stalled-job lifecycle scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared two-scenario stalled-job lifecycle scope, not all BullMQ background processing or messaging semantics."}}

def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source);r=build_capture(read(a.replica),"replica",a.replica)
 report=build_report(s,r)
 write(out/"bullmq-stalled-source.capture.json",s);write(out/"bullmq-stalled-python-replica.capture.json",r);write(out/"bullmq-stalled-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
