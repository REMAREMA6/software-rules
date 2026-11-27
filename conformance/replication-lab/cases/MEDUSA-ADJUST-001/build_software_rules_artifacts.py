import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="business-rules"
LABELS=["no-adjustments","single-exclusive","multiple-exclusive","inclusive-single","mixed-inclusive-exclusive","missing-adjustment-amount","zero-quantity","fractional-quantity","no-tax-context"]
PROPERTIES=[
 ("MEDUSA-ADJUST-P01","missing-adjustment","An adjustment with an undefined amount is skipped."),
 ("MEDUSA-ADJUST-P02","inclusive-adjustment","When a tax rate exists, a tax-inclusive adjustment is divided by one plus the tax rate to obtain its subtotal."),
 ("MEDUSA-ADJUST-P03","exclusive-adjustment-tax","When a tax rate exists, tax is calculated on the adjustment subtotal and added to obtain the total."),
 ("MEDUSA-ADJUST-P04","no-tax-context","Without a tax rate, an adjustment amount remains both subtotal and total, regardless of its tax-inclusive flag."),
 ("MEDUSA-ADJUST-P05","aggregate-adjustments","Aggregate subtotal, tax, and total are the sums of all defined adjustments."),
 ("MEDUSA-ADJUST-P06","per-adjustment-values","Each adjustment receives its own subtotal and total rather than cumulative running aggregates."),
 ("MEDUSA-ADJUST-P07","quantity-allocation","Aggregate amounts are divided by quantity; a missing or zero quantity falls back to one.")
]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "medusa-adjust-scenario-"+x
def eid(side,x):return "medusa-adjust-exec-"+side+"-"+x
def oid(side,x):return "medusa-adjust-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_artifacts):
 created=now();source=side=="source";prefix="medusa-adjust-"+side
 target="medusa-adjustment-source" if source else "python-adjustment-replica"
 runtime="Medusa calculateAdjustmentTotal (TypeScript)" if source else "Python 3.12 Decimal adjustment model"
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[]
 obsids=[oid(side,x) for x in LABELS]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"];inputs=item["inputs"];output=item["output"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe discount/adjustment amount, tax conversion, aggregation, and quantity allocation.",
   "facetIds":[FACET],"subject":"Line-item adjustment allocation",
   "preconditions":["Adjustment records are provided at the utility-function boundary.","Amounts are non-negative numeric values.","Tax rate, when present, is a decimal fraction."],
   "trigger":"Execute calculateAdjustmentTotal with the supplied quantity, tax rate, and adjustment records.",
   "inputs":inputs,"observableQuestions":["How are adjustment subtotal, tax, and total calculated?","How are aggregate amounts allocated per item?","Are missing amounts ignored and individual adjustments kept distinct?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "functionSha256":raw.get("functionSha256","not-applicable")},
   "actualInputs":inputs,"trigger":"Calculate adjustment totals","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Line-item adjustment allocation","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Execute the pinned function or independent Decimal model against equivalent adjustment records.","tool":runtime},
   "conditions":{"scenario":label,"quantity":inputs["quantity"],"taxRate":inputs["taxRate"]},
   "trigger":"calculateAdjustmentTotal",
   "payload":{"facet":FACET,"kind":"domain-decision","subject":"Adjustment and tax allocation",
    "decisionSubject":"Line-item discount/adjustment","inputs":inputs,
    "conditions":{"taxRate":inputs["taxRate"],"quantity":inputs["quantity"]},
    "ruleIdentifier":"MEDUSA-ADJUSTMENT-ALLOCATION-001",
    "evaluatedCriteria":[{"criterion":"tax context present","value":inputs["taxRate"] is not None},
      {"criterion":"adjustment amounts defined","value":all(a["amount"] is not None for a in inputs["adjustments"])}],
    "decision":output,
    "calculation":{"operands":[inputs["quantity"],inputs["taxRate"],inputs["adjustments"]],
      "result":output["adjustmentsTotal"],"unit":"currency amount","precision":"8 decimal places","rounding":"normalized to 8 decimal places for cross-runtime comparison"},
    "extensions":{"sourceFunctionSha256":raw.get("functionSha256"),"scenario":label}},
   "rawValue":item,"normalizedValue":{"inputs":inputs,"output":output},
   "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Line-item adjustment allocation","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in PROPERTIES]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A line item is evaluated with adjustment records, quantity, and optional tax rate.",
  "applicability":{"scope":"Pinned Medusa calculateAdjustmentTotal utility function and the declared nine deterministic scenarios."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in PROPERTIES]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-adjustment-calculation",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest,"functionSha256":raw.get("functionSha256")},
  "locator":raw_path,"digest":digest,"sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 if source:
  for key,path in source_artifacts.items():
   data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
   evidence.append({"evidenceId":"medusa-adjust-source-"+key,"evidenceClass":"source-artifact",
    "evidenceType":"pinned-source-file","mediaType":"text/plain",
    "origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw["sourceCommit"],"location":path},
    "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
    "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture line-item adjustment, tax conversion, aggregation, and quantity-allocation rules.",
  "target":{"targetId":target,"systemName":"Medusa calculateAdjustmentTotal" if source else "Independent Python Decimal adjustment model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Pure adjustment-total utility; repository filtering and complete cart/discount eligibility orchestration are excluded.",
    "included":["missing adjustment filtering","inclusive/exclusive tax conversion","aggregate adjustment totals","per-adjustment subtotal and total","per-item allocation","zero/missing quantity fallback"],
    "excluded":["promotion eligibility","discount precedence/stacking rules","line-item tax calculation","cart and shipping totals","currency conversion","persistence and checkout"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"precision":"8 decimal places","rounding":"normalized output only"}}}},
  "scope":{"description":"Nine deterministic adjustment calculation scenarios.","facetIds":[FACET],
   "subjects":["line-item adjustment allocation"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute pinned Medusa source function and independent Decimal replica with equivalent inputs."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Line-item adjustment allocation","status":"observed",
   "reason":"All nine declared adjustment and tax scenarios were executed and linked to retained evidence.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["Only the adjustment utility is executed; tax and cart total utilities are outside scope.",
   "No discount eligibility, stacking precedence, promotion rules, shipping, or checkout workflow is covered.",
   "This is not full Medusa commerce or complete business-rule facet coverage."],
  "replicationScope":{"scopeId":"medusa-adjustment-allocation-nine-scenarios",
   "description":"Complete property inventory for seven declared adjustment allocation properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Seven required properties are linked to nine source/replica observations and retained source evidence.",
    "rationale":"All declared adjustment conversion, aggregation, per-adjustment, and quantity-allocation rules are exercised; broader commerce rules are explicitly excluded."}}}
def build_report(source,replica):
 created=now();left={x["observationId"].split("medusa-adjust-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("medusa-adjust-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="medusa-adjust-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same adjustment scenario, quantity, tax context, and input records."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"medusa-adjust-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"adjustment-tax-and-allocation","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare aggregate and per-adjustment subtotals, taxes, totals, and quantity allocations.",
   "evidenceRefs":["medusa-adjust-source-runtime","medusa-adjust-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"medusa-adjustment-allocation-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Nine deterministic Medusa adjustment utility scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned calculateAdjustmentTotal function","same adjustment records","same quantity and tax rate","normalized to eight decimal places"],
   "excludedDimensions":["promotion eligibility","discount precedence","cart totals","shipping","currency conversion","persistence"],
   "limitations":["Utility-level calculation only, not full commerce workflow."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":9,"observedUnits":9},"implementation":{"declaredUnits":9,"observedUnits":9},
   "sharedComparableUnits":9,"incomparableUnits":0,"limitations":["Nine utility scenarios do not exhaust Medusa business rules."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python Decimal model "+("differs from" if mismatches else "matches")+" the pinned Medusa adjustment function for nine declared scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared nine-scenario adjustment utility scope, not full commerce."}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-artifacts",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"medusa-adjust-source.capture.json",s);write(out/"medusa-adjust-python-replica.capture.json",r);write(out/"medusa-adjust-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
