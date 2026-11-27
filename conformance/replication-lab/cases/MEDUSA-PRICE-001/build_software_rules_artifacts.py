import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
FACET="business-rules"
LABELS=["default-only","sale-below-default","sale-above-default","sale-equal-default","override-only","sale-below-override","override-below-sale","multiple-overrides-lowest-first","sale-only-no-original-and-missing-set"]
def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p): return json.loads(Path(p).read_text())
def write(p,v): Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(label): return "medusa-price-scenario-"+label
def eid(side,label): return "medusa-price-exec-"+side+"-"+label
def oid(side,label): return "medusa-price-obs-"+side+"-"+label

def build_capture(raw,side,raw_path,source_artifacts):
 created=now(); source=side=="source"; prefix="medusa-price-"+side
 target_id="medusa-pricing-module-source" if source else "python-price-selection-replica"
 capture_id=prefix+"-capture"
 runtime="Medusa PricingModuleService.calculatePrices (TypeScript)" if source else "Independent Python 3.12 price-selection model"
 raw_bytes=Path(raw_path).read_bytes(); digest=hashlib.sha256(raw_bytes).hexdigest()
 scenarios=[]; executions=[]; observations=[]
 obsids=[oid(side,label) for label in LABELS]
 for index,item in enumerate(raw["scenarios"]):
  label=item["label"]; inputs=item["inputs"]; output=item["output"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Select the calculated and original price for a price set from ordered candidate price records.",
   "facetIds":[FACET],"subject":"Calculated price selection",
   "preconditions":["The candidate price rows are supplied by the repository boundary.","Currency context is EUR; tax inclusivity is stubbed false.","No price-rule or price-preference records are returned."],
   "trigger":"Execute PricingModuleService.calculatePrices for the supplied price-set identifiers.",
   "inputs":inputs,
   "observableQuestions":["Which candidate becomes the calculated price?","Which candidate becomes the original/reference price?","Is a missing price set omitted?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target_id,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "methodBodySha256":raw.get("methodBodySha256","not-applicable")},
   "actualInputs":inputs,"trigger":"Calculate prices for the declared price-set identifiers.",
   "collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target_id,"executionId":eid(side,label),
   "facet":FACET,"subject":"Calculated price selection","observedAt":created,"sequence":index,
   "method":{"class":"instrumentation","procedure":"Execute the extracted source service method or independent replica against the same candidate price rows.","tool":runtime},
   "conditions":{"scenario":label,"currencyCode":"eur","taxInclusive":False},
   "trigger":"PricingModuleService.calculatePrices",
   "payload":{"facet":FACET,"kind":"domain-decision","subject":"Calculated and original price selection",
    "decisionSubject":", ".join(inputs["priceSetIds"]),"inputs":inputs,
    "conditions":{"currency_code":"eur","priceRuleRows":[],"pricePreferences":[]},
    "ruleIdentifier":"MEDUSA-PRICE-SELECT-001",
    "evaluatedCriteria":[{"criterion":"price-list candidate","value":True},{"criterion":"original-price excludes sale price","value":True}],
    "decision":output,"extensions":{"sourceMethodBodySha256":raw.get("methodBodySha256"),"scenario":label}},
   "rawValue":item,"normalizedValue":{"inputs":inputs,"output":output},
   "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 property_specs=[
  ("MEDUSA-PRICE-P01","default-price-selection","When no price-list candidate applies, the default price is both calculated and original price."),
  ("MEDUSA-PRICE-P02","sale-price-comparison","A sale price is selected as calculated price only when its amount is less than or equal to the original/reference price."),
  ("MEDUSA-PRICE-P03","override-price-selection","A selected override price becomes both calculated and original/reference price; among matching override candidates the ordered lowest candidate is used."),
  ("MEDUSA-PRICE-P04","original-price-excludes-sale","A sale price is not used as the original/reference price; the matching non-sale override or default is used."),
  ("MEDUSA-PRICE-P05","missing-price-set","A requested price set with no candidate rows is omitted from the result.")
 ]
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Calculated price selection","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in property_specs]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A pricing context requests calculated prices for one or more price sets.",
  "applicability":{"scope":"Pinned Medusa PricingModuleService.calculatePrices method with candidate rows supplied by a deterministic repository stub; no tax or SQL filtering."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in property_specs]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-price-selection-capture",
  "mediaType":"application/json","origin":{"targetId":target_id,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":raw.get("capturedAt",created),"embedded":{"scenarioLabels":LABELS,"sha256":digest,
   "methodBodySha256":raw.get("methodBodySha256")},"locator":raw_path,"digest":digest,
  "sizeBytes":len(raw_bytes),"retention":{"status":"retained","access":"CI artifact"}}]
 if source:
  for key,path in source_artifacts.items():
   data=Path(path).read_bytes(); evidence.append({"evidenceId":"medusa-price-source-"+key,
    "evidenceClass":"source","evidenceType":"pinned-source-file","mediaType":"text/plain",
    "origin":{"targetId":target_id,"collector":"GitHub immutable source checkout","sourceRevision":raw["sourceCommit"],"location":path},
    "capturedAt":created,"embedded":{"sha256":hashlib.sha256(data).hexdigest()},
    "locator":path,"digest":hashlib.sha256(data).hexdigest(),"sizeBytes":len(data),
    "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":capture_id,"createdAt":created,
  "purpose":"Capture Medusa calculated-price and original-price selection rules for nine deterministic candidate-price scenarios.",
  "target":{"targetId":target_id,"systemName":"Medusa PricingModuleService" if source else "Independent Python price-selection replica",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),
   "build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"The exact calculatePrices service method body with deterministic repository and tax/preference collaborators.",
    "included":["default price selection","sale versus original comparison","override selection","original/reference price selection","missing price-set omission"],
    "excluded":["SQL candidate filtering","quantity tiers","currency normalization","active/expired price-list filtering","tax inclusivity","database persistence","cart totals and discounts"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,"configuration":{"state":"observed","value":{"currency_code":"eur","taxInclusive":False}}}},
  "scope":{"description":"Nine fixed price-selection scenarios over ordered candidate price rows.","facetIds":[FACET],
   "subjects":["price-set"],"scenarioIds":[sid(label) for label in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute the pinned service method or independent replica with equivalent candidate rows and pricing context."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,
  "evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Calculated price selection","status":"observed",
   "reason":"All nine declared scenarios were executed and linked to source/replica observations.",
   "scenarioIds":[sid(label) for label in LABELS],"executionIds":[eid(side,label) for label in LABELS]}],
  "limitations":["The repository query that filters candidate prices is stubbed; this case begins at the ordered candidate-row boundary.",
   "Tax inclusivity and price preferences are stubbed false/empty.","This is not full Medusa commerce or complete business-rule facet coverage."],
  "replicationScope":{"scopeId":"medusa-calculated-price-selection-nine-scenarios",
   "description":"Complete property inventory for five declared calculated/original price selection properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Five required selection properties are linked to nine source/replica observations and retained method/source evidence.",
    "rationale":"All declared price-selection rules are observed; repository filtering, tax, quantity tiers, and broader commerce rules are explicitly excluded."}}}

def build_report(source,replica):
 created=now(); left={x["observationId"].split("medusa-price-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("medusa-price-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[]; results=[]
 for label in LABELS:
  a,b=left[label],right[label]; aid="medusa-price-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired",
   "identityBasis":"scenario-subject-facet-condition","rationale":"Same named price-selection scenario and ordered candidate rows."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"medusa-price-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"calculated-and-original-price-selection","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare returned calculated/original price objects and missing-set behaviour.",
   "evidenceRefs":["medusa-price-source-runtime","medusa-price-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"medusa-price-selection-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Nine fixed Medusa price-selection scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned PricingModuleService.calculatePrices method body","same candidate price rows","currency EUR","empty tax and price-preference collaborators"],
   "excludedDimensions":["SQL candidate filtering","quantity tiers","tax inclusivity","currency normalization","cart totals and discounts"],
   "limitations":["This compares the service-level selection algorithm only."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":9,"observedUnits":9},"implementation":{"declaredUnits":9,"observedUnits":9},
   "sharedComparableUnits":9,"incomparableUnits":0,"limitations":["Nine scenarios do not exhaust the full commerce pricing feature space."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python model "+("differs from" if mismatches else "matches")+" the pinned Medusa service method for nine declared price-selection scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared nine-scenario service-level price-selection scope, not the full Medusa pricing module or business-rule facet."}}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--source",required=True); p.add_argument("--replica",required=True); p.add_argument("--output-dir",required=True); p.add_argument("--source-artifacts",required=True); a=p.parse_args()
 out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"medusa-price-source.capture.json",s); write(out/"medusa-price-python-replica.capture.json",r); write(out/"medusa-price-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope": raise SystemExit(1)
if __name__=="__main__": main()
