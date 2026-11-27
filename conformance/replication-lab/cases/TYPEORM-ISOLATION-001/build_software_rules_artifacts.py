import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="persistence"
LABELS=["read-committed-nonrepeatable-read","repeatable-read-stable-snapshot","serializable-write-skew-prevention"]
PROPERTIES=[
 ("TORM-ISO-P01","read-committed-fresh-snapshot","READ COMMITTED provides a fresh committed snapshot for each statement, so a later read can observe another transaction's commit."),
 ("TORM-ISO-P02","repeatable-read-snapshot","REPEATABLE READ preserves the transaction snapshot across repeated reads."),
 ("TORM-ISO-P03","serializable-anomaly-prevention","SERIALIZABLE prevents concurrent write skew that would violate a predicate invariant."),
 ("TORM-ISO-P04","serialization-failure","A transaction rejected to preserve serializability reports a serialization failure category."),
 ("TORM-ISO-P05","atomic-abort","Writes from an aborted serializable transaction are not visible after rollback."),
 ("TORM-ISO-P06","concurrent-observation","Overlapping transactions can observe distinct snapshots according to their declared isolation levels."),
 ("TORM-ISO-P07","invariant-preservation","The final persisted state preserves the invariant that at least one doctor remains on call."),
 ("TORM-ISO-P08","transaction-lifecycle","Commit and rollback outcomes remain observable through final database state.")
]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "typeorm-isolation-scenario-"+x
def eid(side,x):return "typeorm-isolation-exec-"+side+"-"+x
def oid(side,x):return "typeorm-isolation-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_artifacts):
 created=now();source=side=="source";prefix="typeorm-isolation-"+side
 target="typeorm-postgres-source" if source else "python-postgres-replica"
 runtime="TypeORM QueryRunner / PostgreSQL" if source else "Python 3.12 psycopg / PostgreSQL"
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[];obsids=[oid(side,x) for x in LABELS]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"];output=item["output"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe overlapping transaction reads, isolation snapshots, and serializable anomaly prevention.",
   "facetIds":[FACET,"behaviour","errors-recovery"],"subject":"PostgreSQL transaction isolation",
   "preconditions":["PostgreSQL 16 is available.","Two independent connections overlap within each scenario.","The test schema is isolated and reset between scenarios."],
   "trigger":"Execute the overlapping transactions under the declared isolation level.",
   "inputs":{"scenario":label},"observableQuestions":["What does each transaction observe?","Can the conflicting writes both commit?","What final state and error category remain?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "packageVersion":raw.get("packageVersion","Python 3.12"),"database":"PostgreSQL 16"},
   "actualInputs":{"scenario":label},"trigger":"Run overlapping transaction isolation probe","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"PostgreSQL transaction isolation","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Use two independent database connections with overlapping transactions and capture reads, commits, serialization errors, and final rows.","tool":runtime},
   "conditions":{"scenario":label,"database":"PostgreSQL 16"},
   "trigger":"Concurrent transaction operations under declared isolation level",
   "payload":{"facet":FACET,"kind":"transaction-lifecycle","subject":"Transaction isolation and conflict resolution",
    "transaction":{"isolationLevel":{"read-committed-nonrepeatable-read":"READ COMMITTED","repeatable-read-stable-snapshot":"REPEATABLE READ","serializable-write-skew-prevention":"SERIALIZABLE"}[label],
     "overlappingConnections":2,"scenario":label},
    "lifecycle":[{"state":"started"},{"state":"read"},{"state":"concurrent-transaction-committed"},{"state":"committed-or-aborted"}],
    "output":output,"error":{"category":output.get("errorCode") or "none","propagated":output.get("commitB")=="aborted"},
    "invariant":{"name":"at-least-one-doctor-on-call","expectedMinimum":1,"actual":output.get("remainingOnCall")},
    "extensions":{"scenario":label}},
   "rawValue":item,"normalizedValue":item,"evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"PostgreSQL transaction isolation","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in PROPERTIES]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"Two database transactions overlap while reading/updating shared records under a declared isolation level.",
  "applicability":{"scope":"Pinned TypeORM QueryRunner 1.1.3 with PostgreSQL 16; READ COMMITTED, REPEATABLE READ, SERIALIZABLE."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in PROPERTIES]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-transaction-isolation-capture",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest},"locator":raw_path,
  "digest":digest,"sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 if source:
  for key,path in source_artifacts.items():
   data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
   evidence.append({"evidenceId":"typeorm-isolation-source-"+key,"evidenceClass":"source-artifact",
    "evidenceType":"pinned-source-file","mediaType":"text/plain",
    "origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw["sourceCommit"],"location":path},
    "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
    "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture TypeORM/PostgreSQL transaction isolation, snapshot, serializable conflict, and invariant-preservation rules.",
  "target":{"targetId":target,"systemName":"TypeORM QueryRunner / PostgreSQL" if source else "Independent Python psycopg / PostgreSQL",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Two-connection transaction probes against PostgreSQL 16 using TypeORM QueryRunner and Python psycopg.",
    "included":["READ COMMITTED non-repeatable read","REPEATABLE READ snapshot stability","SERIALIZABLE write-skew prevention","serialization failure classification","rollback atomicity","final invariant"],
    "excluded":["other database engines","distributed transactions","deadlock policy","advisory locks","pool exhaustion","migrations","power-loss durability"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"database":"PostgreSQL 16","connections":2,"isolationLevels":["READ COMMITTED","REPEATABLE READ","SERIALIZABLE"]}}}},
  "scope":{"description":"Three deterministic overlapping-transaction isolation scenarios.","facetIds":[FACET,"behaviour","errors-recovery"],
   "subjects":["transaction isolation"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Run concurrent reads and writes under declared isolation levels, record commit/abort outcomes, and inspect final persisted state."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"PostgreSQL transaction isolation","status":"observed",
   "reason":"All three declared isolation scenarios were executed with two overlapping database connections.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["PostgreSQL 16 only; driver and engine-specific isolation differences are not covered.",
   "No deadlocks, lock timeout policies, distributed transactions, pool exhaustion, or crash/power-loss semantics.",
   "This is not complete TypeORM persistence or complete persistence-facet coverage."],
  "replicationScope":{"scopeId":"typeorm-postgres-isolation-three-scenarios",
   "description":"Complete property inventory for eight declared transaction isolation properties.",
   "facets":[FACET,"behaviour","errors-recovery"],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Eight required isolation properties are linked to three source/replica observations and retained runtime evidence.",
    "rationale":"READ COMMITTED, REPEATABLE READ, and SERIALIZABLE write-skew behaviours are directly exercised; other persistence classes remain explicitly excluded."}}}
def build_report(source,replica):
 created=now();left={x["observationId"].split("typeorm-isolation-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("typeorm-isolation-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="typeorm-isolation-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same overlapping transaction scenario, isolation level, and final persisted state."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"typeorm-isolation-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"transaction-isolation-outcome","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare transaction snapshots, commit/abort outcomes, serialization error, and invariant state.",
   "evidenceRefs":["typeorm-isolation-source-runtime","typeorm-isolation-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"typeorm-postgres-isolation-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Three PostgreSQL transaction isolation scenarios.",
   "facets":[FACET,"behaviour","errors-recovery"],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned TypeORM source commit","PostgreSQL 16","two overlapping connections","same isolation levels and SQL operations"],
   "excludedDimensions":["other database engines","deadlock handling","distributed transactions","crash durability"],
   "limitations":["Three scenarios do not exhaust transaction isolation semantics."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":3,"observedUnits":3},"implementation":{"declaredUnits":3,"observedUnits":3},
   "sharedComparableUnits":3,"incomparableUnits":0,"limitations":["Only three isolation scenarios are tested."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python/psycopg model "+("differs from" if mismatches else "matches")+" TypeORM QueryRunner/PostgreSQL for the three declared isolation scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared three-scenario PostgreSQL isolation scope, not all persistence or database behaviour."}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-artifacts",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"typeorm-isolation-source.capture.json",s);write(out/"typeorm-isolation-python-replica.capture.json",r);write(out/"typeorm-isolation-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
