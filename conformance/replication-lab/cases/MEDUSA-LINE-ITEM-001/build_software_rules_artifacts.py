import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="business-rules"
LABELS=["basic-no-tax","exclusive-tax-20","multiple-additive-tax-lines","inclusive-tax-20","exclusive-discount-with-tax","inclusive-discount-with-tax","multiple-exclusive-adjustments","mixed-inclusive-exclusive-adjustments","fractional-quantity","zero-quantity","empty-tax-context-with-discount","inclusive-price-with-multiple-tax-lines","returned-quantity-prorated-discount","inclusive-return-refund"]
PROPERTIES=[
 ("MEDUSA-LINE-P01","quantity-base","The line-item base amount is unit price multiplied by quantity."),
 ("MEDUSA-LINE-P02","tax-inclusive-subtotal","Tax-inclusive gross price is divided by one plus the sum of tax rates to derive its pre-tax subtotal."),
 ("MEDUSA-LINE-P03","tax-line-aggregation","Multiple tax lines contribute additively to tax totals."),
 ("MEDUSA-LINE-P04","discount-adjustment","Adjustments are normalized to pre-tax values when tax-inclusive and allocated per item to current quantity."),
 ("MEDUSA-LINE-P05","discounted-tax","Tax is recalculated on the remaining taxable amount after discounts."),
 ("MEDUSA-LINE-P06","original-current-separation","Original subtotal/tax/total remain distinct from current discounted subtotal/tax/total."),
 ("MEDUSA-LINE-P07","returned-quantity","Returned/dismissed quantities reduce current totals and refundable totals prorate discounts per original item quantity."),
 ("MEDUSA-LINE-P08","quantity-boundaries","Fractional quantities are supported; zero quantity avoids division by zero in per-unit total calculations.")
]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "medusa-line-item-scenario-"+x
def eid(side,x):return "medusa-line-item-exec-"+side+"-"+x
def oid(side,x):return "medusa-line-item-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_artifacts):
 created=now();source=side=="source";prefix="medusa-line-item-"+side
 target="medusa-line-item-source" if source else "python-line-item-replica"
 runtime="Medusa getLineItemTotals utility (TypeScript)" if source else "Python 3.12 Decimal line-item model"
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[];obsids=[oid(side,x) for x in LABELS]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"];inputs=item["inputs"];output=item["output"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Observe line-item base, subtotal, discount, tax, total, and refundable amount semantics.",
   "facetIds":[FACET],"subject":"Commerce line-item calculation",
   "preconditions":["Unit price and quantity are numeric.","Tax lines contain percentage rates.","The case excludes external tax-provider calculations."],
   "trigger":"Execute getLineItemTotals with the declared item and context.",
   "inputs":inputs,"observableQuestions":["How are original and discounted totals separated?","How are tax and adjustments calculated?","How do returned quantities affect current and refundable totals?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "sourceFiles":raw.get("sourceFiles",{})},"actualInputs":inputs,
   "trigger":"Calculate line-item totals","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Commerce line-item calculation","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Execute the pinned Medusa line-item/adjustment/tax functions or independent Decimal replica with equivalent item inputs.","tool":runtime},
   "conditions":{"scenario":label,"quantity":inputs["quantity"],"taxLines":inputs["tax_lines"],
    "isTaxInclusive":inputs["is_tax_inclusive"],"detail":inputs["detail"]},
   "trigger":"getLineItemTotals",
   "payload":{"facet":FACET,"kind":"domain-decision","subject":"Line-item price/tax/discount result",
    "decisionSubject":"commerce line-item totals","inputs":inputs,"conditions":{"scenario":label},
    "ruleIdentifier":"MEDUSA-LINE-ITEM-TOTALS-001",
    "evaluatedCriteria":[{"criterion":"line item total calculated","value":True}],
    "decision":{"totals":output},"extensions":{"scenario":label,"sourceFileHashes":raw.get("sourceFiles",{})}},
   "rawValue":item,"normalizedValue":{"inputs":inputs,"output":output},
   "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Commerce line-item calculation","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in PROPERTIES]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A line item is calculated from unit price, quantity, tax lines, adjustments, and optional return detail.",
  "applicability":{"scope":"Pinned Medusa getLineItemTotals, calculateAdjustmentTotal, and calculateTaxTotal functions; full cart orchestration excluded."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in PROPERTIES]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-line-item-total-calculation",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest,"sourceFiles":raw.get("sourceFiles",{})},
  "locator":raw_path,"digest":digest,"sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 if source:
  for key,path in source_artifacts.items():
   data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
   evidence.append({"evidenceId":"medusa-line-source-"+key,"evidenceClass":"source-artifact",
    "evidenceType":"pinned-source-file","mediaType":"text/plain",
    "origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw["sourceCommit"],"location":path},
    "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
    "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture line-item price, tax, adjustment, discount, and refundable-total rules.",
  "target":{"targetId":target,"systemName":"Medusa line-item totals" if source else "Independent Python Decimal line-item model",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Pure line-item total calculation utilities; full cart, shipping, promotion and checkout workflows excluded.",
    "included":["quantity multiplication","tax-inclusive/exclusive subtotal","multiple tax lines","discount adjustments","tax after discount","original/current totals","returned quantity/refundable total","fractional and zero quantity"],
    "excluded":["full cart aggregation","shipping","promotion discovery/eligibility","currency conversion","tax-provider calculations","persistence","checkout"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"includeTax":False,"precision":"8 decimal places","rounding":"normalized output only"}}}},
  "scope":{"description":"Fourteen deterministic line-item total scenarios.","facetIds":[FACET],
   "subjects":["commerce line-item calculation"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute pinned Medusa utility functions and independent Decimal replica against equivalent line-item inputs."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Commerce line-item calculation","status":"observed",
   "reason":"All fourteen declared pricing, tax, adjustment, quantity, and return scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["This is a line-item calculation case, not full cart or order aggregation.",
   "Promotion eligibility, discount precedence, campaign budgets, shipping, currency conversion, tax providers, and checkout are excluded.",
   "This is not complete Medusa commerce or complete business-rule facet coverage."],
  "replicationScope":{"scopeId":"medusa-line-item-totals-fourteen-scenarios",
   "description":"Complete property inventory for eight declared line-item calculation properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Eight required line-item calculation properties are linked to fourteen source/replica observations and retained source evidence.",
    "rationale":"All declared price, tax, discount, return-quantity and refundable-total rules are exercised; full cart/checkout behaviour is explicitly excluded."}}}
def build_report(source,replica):
 created=now();left={x["observationId"].split("medusa-line-item-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("medusa-line-item-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="medusa-line-item-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same line-item input, tax context, adjustments, and return-detail state."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"medusa-line-item-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"line-item-price-tax-discount-total","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare original/current subtotal, tax, discount, total, and refundable total for equivalent inputs.",
   "evidenceRefs":["medusa-line-item-source-runtime","medusa-line-item-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"medusa-line-item-totals-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Fourteen deterministic Medusa line-item calculation scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned Medusa source functions","same item price and quantity","same tax lines and adjustments","same return-detail values"],
   "excludedDimensions":["full cart aggregation","shipping","promotion lifecycle","currency conversion","tax providers","checkout"],
   "limitations":["Line-item utility only, not full cart/order semantics."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":14,"observedUnits":14},"implementation":{"declaredUnits":14,"observedUnits":14},
   "sharedComparableUnits":14,"incomparableUnits":0,"limitations":["Fourteen line-item scenarios do not exhaust commerce behaviour."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python Decimal line-item model "+("differs from" if mismatches else "matches")+" the pinned Medusa utilities for fourteen declared scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared fourteen-scenario line-item utility scope, not full cart or checkout."}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-artifacts",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"medusa-line-item-source.capture.json",s);write(out/"medusa-line-item-python-replica.capture.json",r);write(out/"medusa-line-item-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
