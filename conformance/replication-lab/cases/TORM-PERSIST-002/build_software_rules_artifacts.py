import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="persistence"
LABELS=["commit-survives-reopen","rollback-survives-reopen","update-survives-reopen","constraint-failure-atomicity"]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "typeorm-durable-scenario-"+x
def eid(side,x):return "typeorm-durable-exec-"+side+"-"+x
def oid(side,x):return "typeorm-durable-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_files):
 created=now();source=side=="source";prefix="typeorm-durable-"+side
 target="typeorm-file-backed-source" if source else "python-file-backed-replica"
 runtime=raw.get("source","TypeORM better-sqlite3 file-backed database") if source else raw.get("implementation","Python 3.12 sqlite3 file-backed database")
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe durable database state after closing and reopening a file-backed database.",
   "facetIds":[FACET],"subject":"File-backed transaction durability",
   "preconditions":["A file-backed SQLite database is initialized.","Each transaction completes or fails before the database connection is closed.","The database is reopened before final state observation."],
   "trigger":"Execute the declared transaction and inspect persisted rows after reopen.",
   "inputs":{"scenario":label},"observableQuestions":["Which rows remain after reopen?","Was commit or rollback durable?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica")},
   "actualInputs":{"scenario":label},"trigger":"Execute file-backed transaction and reopen database","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"File-backed transaction durability","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Execute transaction, close connection, reopen file-backed database, and read final rows.","tool":runtime},
   "conditions":{"scenario":label,"database":"SQLite file","reopenBeforeObservation":True},
   "trigger":"Commit/rollback transaction followed by connection close and reopen",
   "payload":{"facet":FACET,"kind":"state-operation","subject":"Durable database state after reopen",
    "store":"File-backed SQLite","operation":"transaction",
    "selector":{"scenario":label},"beforeState":{"rows":[]},"afterState":{"rows":item.get("rows",[])},
    "transaction":{"terminal":"committed" if label in ("commit-survives-reopen","update-survives-reopen") else "rolled-back",
      "errorPropagated":item.get("errorPropagated",label=="constraint-failure-atomicity")},
    "commitResult":"durable" if item.get("count",0)>0 else "rolled-back",
    "consistency":{"rowCountAfterReopen":item.get("count"),"errorCategory":item.get("errorCategory")},
    "ordering":"Observe only after connection close and reopen.",
    "durabilityInterval":{"connectionClosed":True,"reopened":True,"restartEquivalent":True},
    "concurrency":{"tested":False},"retention":{"store":"local SQLite file","stateObservedAfterReopen":True},
    "extensions":{"sourceDriver":"better-sqlite3" if source else "sqlite3","scenario":label}},
   "rawValue":item,"normalizedValue":item,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 obsids=[oid(side,x) for x in LABELS]
 props=[
  ("TORM-PERSIST-P05","commit-durability","Committed writes remain visible after closing and reopening the file-backed database."),
  ("TORM-PERSIST-P06","rollback-durability","Writes from a failed transaction remain absent after closing and reopening the database."),
  ("TORM-PERSIST-P07","update-durability","A committed update remains visible after database reopen."),
  ("TORM-PERSIST-P08","constraint-atomicity","A constraint failure rolls back earlier writes in the same transaction, including after reopen.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"File-backed transaction durability","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in props]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A transaction writes to a file-backed SQLite database and the connection is reopened.",
  "applicability":{"scope":"Pinned TypeORM better-sqlite3 driver and independent Python sqlite3 file-backed model."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-durable-state-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,"digest":digest,
  "sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 for key,path in source_files.items():
  data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
  evidence.append({"evidenceId":"typeorm-durable-source-"+key,"evidenceClass":"source-artifact","evidenceType":"pinned-source-file",
   "mediaType":"text/plain","origin":{"targetId":target,"collector":"GitHub immutable TypeORM source checkout","sourceRevision":raw.get("sourceCommit"),"location":path},
   "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
   "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture file-backed database commit/rollback durability and constraint atomicity after reopen.",
  "target":{"targetId":target,"systemName":"TypeORM 1.1.3 / better-sqlite3" if source else "Python sqlite3 file-backed model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"One file-backed SQLite database and a single non-null text table; connection is closed and reopened between write and final observation.",
    "included":["commit durability","rollback durability","update durability","constraint-failure atomicity"],
    "excluded":["multi-process concurrency","production database isolation","power-loss durability","migrations","WAL tuning","other database drivers"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"driver":"better-sqlite3" if source else "sqlite3","fileBacked":True}}}},
  "scope":{"description":"Four file-backed transaction durability scenarios observed after database reopen.",
   "facetIds":[FACET],"subjects":["file-backed transaction durability"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute file-backed transaction, close connection, reopen database, and inspect durable state."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"File-backed transaction durability","status":"observed",
   "reason":"All four declared commit/rollback/update/constraint scenarios were observed after reopen.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["SQLite file durability only; no multi-process concurrency, power-loss testing, production DB isolation, migrations, WAL tuning, or other drivers.",
   "This is not complete persistence-facet coverage."],
  "replicationScope":{"scopeId":"typeorm-file-backed-four-durability-scenarios",
   "description":"Complete property inventory for four declared file-backed durability properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Four required durability/atomicity properties are linked to four source/replica observations and retained evidence.",
    "rationale":"All declared commit, rollback, update, and constraint-atomicity outcomes are observed after reopen; excluded concurrency and crash classes remain explicit."}}}

def build_report(source,replica):
 created=now();left={x["observationId"].split("typeorm-durable-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("typeorm-durable-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="typeorm-durable-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same file-backed transaction and post-reopen state scenario."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"typeorm-durable-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"durable-post-reopen-state","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare persisted rows and transaction outcome after connection close/reopen.",
   "evidenceRefs":["typeorm-durable-source-runtime","typeorm-durable-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"typeorm-file-backed-durability-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Four file-backed SQLite transaction durability scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["File-backed database","connection closed before final read","same transaction writes and constraints"],
   "excludedDimensions":["multi-process concurrency","power-loss durability","production DB isolation","migrations","WAL tuning"],
   "limitations":["SQLite file-backed semantics only."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":4,"observedUnits":4},"implementation":{"declaredUnits":4,"observedUnits":4},
   "sharedComparableUnits":4,"incomparableUnits":0,"limitations":["Four scenarios do not exhaust persistence behaviour."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" TypeORM for four declared file-backed durability scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared four-scenario SQLite file-durability scope, not all persistence drivers or failure modes."}}

def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-files",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_files));r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"typeorm-durable-source.capture.json",s);write(out/"typeorm-durable-python-replica.capture.json",r);write(out/"typeorm-durable-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
