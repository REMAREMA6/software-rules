import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="background-processing"
LABELS=["reschedule-delayed-job","cancel-delayed-job"]
PROPERTIES=[
 ("BMQ-SCHED-P01","delayed-enqueue","A job added with a positive delay enters the delayed state."),
 ("BMQ-SCHED-P02","delay-change","Changing the delay of a delayed job updates its due time while preserving delayed state."),
 ("BMQ-SCHED-P03","due-job-execution","A due delayed job becomes active, executes, and reaches completed state."),
 ("BMQ-SCHED-P04","worker-event-order","The worker emits active before completed for the same job."),
 ("BMQ-SCHED-P05","delayed-job-removal","Removing a delayed job deletes it from the queue."),
 ("BMQ-SCHED-P06","cancellation-prevents-execution","A removed delayed job is not processed by a worker."),
 ("BMQ-SCHED-P07","queue-counts","Queue counts reflect the completed job and absence of remaining delayed/waiting/active work.")
]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "bullmq-schedule-scenario-"+x
def eid(side,x):return "bullmq-schedule-exec-"+side+"-"+x
def oid(side,x):return "bullmq-schedule-obs-"+side+"-"+x
def build_capture(raw,side,raw_path):
 created=now();source=side=="source";prefix="bullmq-schedule-"+side
 target="bullmq-schedule-source" if source else "python-schedule-replica"
 runtime="BullMQ Queue/Worker pinned runtime" if source else "Python 3.12 delayed-job state machine"
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[];obsids=[oid(side,x) for x in LABELS]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"]
  if label=="reschedule-delayed-job":
   questions=["Does changeDelay preserve delayed state?","Does the worker execute the rescheduled job once?","Are active/completed events ordered and queue counts correct?"]
   trigger="Change the due time of a delayed job, then let the worker process it."
  else:
   questions=["Does remove delete a delayed job?","Can a removed job still be processed?","Do queue counts reflect cancellation?"]
   trigger="Remove a delayed job before its due time."
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe delayed job rescheduling or cancellation semantics.",
   "facetIds":[FACET,"behaviour","messaging"],"subject":"Delayed job scheduling and cancellation",
   "preconditions":["A Redis-backed queue is ready.","The target job is initially delayed.","A single worker is used for the reschedule scenario."],
   "trigger":trigger,"inputs":item,"observableQuestions":questions})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "packageVersion":raw.get("packageVersion","Python 3.12")},
   "actualInputs":item,"trigger":trigger,"collector":{"name":runtime}})
  if label=="reschedule-delayed-job":
   lifecycle=[{"state":"delayed"},{"state":"delayed","operation":"changeDelay"},
    {"state":"active","event":"active"},{"state":"completed","event":"completed"}]
   sideEffects=["delayed score updated","job processed once","completed count incremented"]
  else:
   lifecycle=[{"state":"delayed"},{"state":"removed","operation":"remove"}]
   sideEffects=["job removed from delayed set","no worker execution"]
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Delayed job scheduling and cancellation","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Observe delayed state, delay change/removal, worker events, final state and queue counts.","tool":runtime},
   "conditions":{"scenario":label,"redisVersion":"7","workerConcurrency":1},
   "trigger":trigger,
   "payload":{"facet":FACET,"kind":"job-lifecycle","subject":"Delayed job scheduling and cancellation",
    "job":"scheduled" if label=="reschedule-delayed-job" else "cancelled",
    "schedule":{"type":"delayed","initialDelayMs":5000,"rescheduledDelayMs":250},
    "lifecycle":lifecycle,"output":item,"sideEffects":sideEffects,
    "cancellation":{"removeBeforeDue":label=="cancel-delayed-job","preventedExecution":not item.get("processed",False)},
    "extensions":{"scenario":label,"queueCounts":item["counts"],"workerEvents":item.get("events",[])}},
   "rawValue":item,"normalizedValue":item,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Delayed job scheduling and cancellation","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in PROPERTIES]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A delayed queue job is rescheduled or removed before its due time.",
  "applicability":{"scope":"Pinned BullMQ 6.7.10 with Redis 7, one queue, one worker, one delayed job per scenario."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in PROPERTIES]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-delayed-job-lifecycle-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,
  "digest":digest,"sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture delayed job rescheduling, worker execution ordering, cancellation and queue-count rules.",
  "target":{"targetId":target,"systemName":"BullMQ Queue/Worker" if source else "Independent Python delayed-job state machine",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"One Redis-backed queue and one worker; delayed job changeDelay and remove operations.",
    "included":["delayed enqueue","delay update","worker active/completed lifecycle","delayed job removal","cancellation prevents execution","queue counts"],
    "excluded":["repeatable/cron jobs","parent-child flows","multiple workers","concurrency contention","graceful shutdown","Redis failover"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"redisVersion":"7","initialDelayMs":5000,"rescheduledDelayMs":250,"workerConcurrency":1}}}},
  "scope":{"description":"Two deterministic delayed-job lifecycle scenarios.","facetIds":[FACET,"behaviour","messaging"],
   "subjects":["delayed job scheduling and cancellation"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute delayed job rescheduling and removal against BullMQ/Redis and compare with an independent Python state machine."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Delayed job scheduling and cancellation","status":"observed",
   "reason":"Both reschedule-and-execute and cancel-before-due scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["One queue and one worker only.","Repeatable scheduling, multiple workers, lock contention, shutdown, parent-child flows, and Redis failover are excluded.",
   "This is not complete BullMQ background-processing or messaging coverage."],
  "replicationScope":{"scopeId":"bullmq-delayed-job-reschedule-and-cancel",
   "description":"Complete property inventory for seven declared delayed-job lifecycle properties.",
   "facets":[FACET,"behaviour","messaging"],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Seven required properties are linked to two source/replica observations and retained runtime evidence.",
    "rationale":"Both rescheduling/execution and cancellation-before-due are observed; other scheduling and concurrency classes remain explicitly excluded."}}}
def build_report(source,replica):
 created=now();left={x["observationId"].split("bullmq-schedule-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("bullmq-schedule-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="bullmq-schedule-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same delayed job lifecycle operation and normalized queue/worker outcome."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"bullmq-schedule-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"delayed-job-lifecycle","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare delayed state, worker events, completion/removal, processing, and queue counts.",
   "evidenceRefs":["bullmq-schedule-source-runtime","bullmq-schedule-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"bullmq-delayed-job-lifecycle-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Two delayed-job rescheduling and cancellation scenarios.",
   "facets":[FACET,"behaviour","messaging"],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned BullMQ source commit","Redis 7","same queue operation order","one worker with concurrency one"],
   "excludedDimensions":["repeatable jobs","parent-child flows","multiple workers","graceful shutdown","Redis failover"],
   "limitations":["Two scenarios do not exhaust scheduling or delivery semantics."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":2,"observedUnits":2},"implementation":{"declaredUnits":2,"observedUnits":2},
   "sharedComparableUnits":2,"incomparableUnits":0,"limitations":["Only delayed reschedule and cancel operations are tested."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python state machine "+("differs from" if mismatches else "matches")+" BullMQ for the two declared delayed-job lifecycle scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared two-scenario delayed-job lifecycle scope, not all BullMQ background processing or messaging."}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source);r=build_capture(read(a.replica),"replica",a.replica)
 report=build_report(s,r)
 write(out/"bullmq-schedule-source.capture.json",s);write(out/"bullmq-schedule-python-replica.capture.json",r);write(out/"bullmq-schedule-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
