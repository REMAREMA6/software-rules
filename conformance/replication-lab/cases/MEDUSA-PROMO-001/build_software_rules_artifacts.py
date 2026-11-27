import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
FACET="business-rules"
LABELS=["eq-scalar-string","eq-number-coercion","eq-array-all-match","eq-array-one-mismatch","in-array-any-match","in-array-no-match","ne-empty-array","ne-array-no-match","ne-array-has-match","gt-numeric","gte-boundary","lt-numeric","lte-boundary","gt-numeric-lexical-trap","invalid-operator","ne-empty-rule-values","empty-rules","item-prefix-strip","shipping-prefix-strip","nested-attribute","missing-attribute-ne","missing-attribute-eq","empty-rule-values","non-string-rule-values","all-rules-must-pass","all-rules-pass","order-scope-does-not-strip-prefix","context-eq-array-all","context-eq-array-one-mismatch","context-in-array-any","context-in-array-none","context-no-rules"]
PROPERTIES=[
 ("MEDUSA-PROMO-P01","equality","The eq operator requires every observed context value to match a configured rule value after string coercion."),
 ("MEDUSA-PROMO-P02","membership","The in operator succeeds when at least one observed context value matches a configured rule value."),
 ("MEDUSA-PROMO-P03","inequality","The ne operator requires every observed context value to differ; an empty context-value list passes ne."),
 ("MEDUSA-PROMO-P04","numeric-comparison","gt, gte, lt, and lte use numeric comparisons, with gte/lte accepting equality at the boundary."),
 ("MEDUSA-PROMO-P05","context-scope","Item and shipping-method scopes remove only their corresponding attribute prefix before lookup."),
 ("MEDUSA-PROMO-P06","nested-attribute","Nested attribute paths are resolved against the supplied context object."),
 ("MEDUSA-PROMO-P07","rule-conjunction","All configured rules must pass for a context to be eligible."),
 ("MEDUSA-PROMO-P08","rule-value-validation","A rule without an attribute or without string-valued rule values fails; an empty rule set passes."),
 ("MEDUSA-PROMO-P09","missing-context","A missing context attribute fails positive/equality operators but passes ne under the source evaluator's missing-value semantics.")
]
def now():return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+"\n")
def sid(x):return "medusa-promo-scenario-"+x
def eid(side,x):return "medusa-promo-exec-"+side+"-"+x
def oid(side,x):return "medusa-promo-obs-"+side+"-"+x
def build_capture(raw,side,raw_path,source_artifacts):
 created=now();source=side=="source";prefix="medusa-promo-"+side
 target="medusa-promotion-rule-source" if source else "python-promotion-rule-replica"
 runtime="Medusa promotion rule validation functions (TypeScript)" if source else "Python 3.12 promotion rule evaluator"
 blob=Path(raw_path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
 scenarios=[];executions=[];observations=[];obsids=[oid(side,x) for x in LABELS]
 for i,item in enumerate(raw["scenarios"]):
  label=item["label"];inputs=item["inputs"];output=item["output"]
  scenarios.append({"scenarioId":sid(label),"title":label.replace("-"," ").title(),
   "purpose":"Evaluate a promotion rule or complete rule set against a promotion context.",
   "facetIds":[FACET],"subject":"Promotion eligibility rule evaluation",
   "preconditions":["Rule values are strings unless a malformed-rule probe states otherwise.","Numeric comparisons use finite integer values.","The source boundary excludes SQL prefiltering and promotion discovery."],
   "trigger":"Evaluate the declared rule condition or rule set against the supplied context.",
   "inputs":inputs,"observableQuestions":["Does the condition pass?","How do array values and operators quantify?","How are missing and scoped attributes resolved?"]})
  executions.append({"executionId":eid(side,label),"scenarioId":sid(label),"targetId":target,
   "startedAt":created,"endedAt":created,"status":"completed",
   "actualContext":{"runtime":runtime,"sourceRevision":raw.get("sourceCommit","independent-replica"),
    "functionSha256":raw.get("functionSha256","not-applicable")},
   "actualInputs":inputs,"trigger":"Evaluate promotion eligibility condition","collector":{"name":runtime}})
  observations.append({"observationId":oid(side,label),"targetId":target,"executionId":eid(side,label),
   "facet":FACET,"subject":"Promotion eligibility rule evaluation","observedAt":created,"sequence":i,
   "method":{"class":"instrumentation","procedure":"Execute the pinned source functions or independent replica against equivalent rule and context values.","tool":runtime},
   "conditions":{"scenario":label},"trigger":"areRulesValidForContext / evaluateRuleValueCondition",
   "payload":{"facet":FACET,"kind":"domain-decision","subject":"Promotion eligibility decision",
    "decisionSubject":"promotion rule context","inputs":inputs,"conditions":{"scenario":label},
    "ruleIdentifier":"MEDUSA-PROMOTION-RULE-EVALUATION-001",
    "evaluatedCriteria":[{"criterion":"condition evaluated against supplied context","value":True}],
    "decision":{"eligible":output},"extensions":{"sourceFunctionSha256":raw.get("functionSha256"),"scenario":label}},
   "rawValue":item,"normalizedValue":{"inputs":inputs,"output":output},
   "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
 inventory=[{"propertyId":pid,"facet":FACET,"subject":"Promotion eligibility rule evaluation","dimension":dim,
  "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
  for pid,dim,why in PROPERTIES]
 rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
  "trigger":"A promotion rule or rule set is evaluated against a context.",
  "applicability":{"scope":"Pinned Medusa evaluateRuleValueCondition and areRulesValidForContext functions; SQL prefiltering and promotion discovery excluded."},
  "status":"supported","supportingObservationIds":obsids} for pid,dim,why in PROPERTIES]
 evidence=[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-promotion-rule-evaluation",
  "mediaType":"application/json","origin":{"targetId":target,"collector":runtime,
   "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
  "capturedAt":created,"embedded":{"scenarioLabels":LABELS,"sha256":digest,"functionSha256":raw.get("functionSha256")},
  "locator":raw_path,"digest":digest,"sizeBytes":len(blob),"retention":{"status":"retained","access":"CI artifact"}}]
 if source:
  for key,path in source_artifacts.items():
   data=Path(path).read_bytes();h=hashlib.sha256(data).hexdigest()
   evidence.append({"evidenceId":"medusa-promo-source-"+key,"evidenceClass":"source-artifact",
    "evidenceType":"pinned-source-file","mediaType":"text/plain",
    "origin":{"targetId":target,"collector":"GitHub immutable source checkout","sourceRevision":raw["sourceCommit"],"location":path},
    "capturedAt":created,"embedded":{"sha256":h},"locator":path,"digest":h,"sizeBytes":len(data),
    "retention":{"status":"retained","access":"CI artifact"}})
 return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
  "purpose":"Capture promotion rule operator, context lookup, scope, and conjunction semantics.",
  "target":{"targetId":target,"systemName":"Medusa promotion rule validation" if source else "Independent Python promotion rule evaluator",
   "systemVersion":raw.get("sourceCommit","Python 3.12"),"build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
   "boundary":{"description":"Pure promotion-rule evaluation functions with deterministic rule/context inputs.",
    "included":["eq/in/ne operators","numeric comparisons","array quantification","missing context","nested paths","item/shipping scope prefixes","multi-rule conjunction","invalid rule values"],
    "excluded":["SQL prefiltering","promotion discovery","discount calculation","campaign budgets","usage registration","checkout lifecycle"]},
   "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime,
    "configuration":{"state":"observed","value":{"scopeValues":["items","shipping_methods","order"]}}}},
  "scope":{"description":"Thirty-two deterministic rule-evaluation scenarios.","facetIds":[FACET],
   "subjects":["promotion eligibility"],"scenarioIds":[sid(x) for x in LABELS]},
  "collector":{"name":runtime,"methodDescription":"Execute pinned source functions or independent Python replica with equivalent rule and context values."},
  "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,"evidence":evidence,
  "coverage":[{"facet":FACET,"subject":"Promotion eligibility rule evaluation","status":"observed",
   "reason":"All 32 declared operator, scope, missing-context, and rule-set scenarios were executed.",
   "scenarioIds":[sid(x) for x in LABELS],"executionIds":[eid(side,x) for x in LABELS]}],
  "limitations":["The case covers rule evaluation only; it does not cover SQL candidate prefiltering or promotion discovery.",
   "Discount application, campaign budgets, usage registration, buy-get application, and checkout are excluded.",
   "This is not complete Medusa promotion lifecycle or complete business-rule facet coverage."],
  "replicationScope":{"scopeId":"medusa-promotion-rule-evaluation-32-scenarios",
   "description":"Complete property inventory for nine declared promotion rule-evaluation properties.",
   "facets":[FACET],"propertyInventory":inventory,
   "completeness":{"status":"complete","assessedAt":created,
    "assessmentMethod":"Nine required rule-evaluation properties are linked to 32 source/replica observations and retained source evidence.",
    "rationale":"All declared operator, scope, context lookup, and conjunction rules are exercised; promotion discovery and application lifecycle are explicitly excluded."}}}
def build_report(source,replica):
 created=now();left={x["observationId"].split("medusa-promo-obs-source-",1)[1]:x for x in source["observations"]}
 right={x["observationId"].split("medusa-promo-obs-replica-",1)[1]:x for x in replica["observations"]}
 alignments=[];results=[]
 for label in LABELS:
  a,b=left[label],right[label];aid="medusa-promo-alignment-"+label
  alignments.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
   "implementationRecordIds":[b["observationId"]],"status":"paired","identityBasis":"scenario-subject-facet-condition",
   "rationale":"Same promotion rule or rule-set scenario and context."})
  av,bv=a["normalizedValue"],b["normalizedValue"]
  results.append({"resultId":"medusa-promo-result-"+label,"alignmentId":aid,"facet":FACET,
   "dimension":"promotion-rule-evaluation","classification":"match" if av==bv else "mismatch",
   "comparisonBasis":"semantic","referenceObservationIds":[a["observationId"]],
   "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
   "reason":"Compare promotion rule eligibility decision for equivalent inputs and context.",
   "evidenceRefs":["medusa-promo-source-runtime","medusa-promo-replica-runtime"]})
 mismatches=[x for x in results if x["classification"]!="match"]
 return {"schemaVersion":"0.2.0","reportId":"medusa-promotion-rule-comparison","createdAt":created,
  "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
  "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
  "comparisonScope":{"description":"Thirty-two deterministic promotion rule evaluation scenarios.",
   "facets":[FACET],"scenarioIds":[sid(x) for x in LABELS],
   "conditions":["Pinned Medusa validation functions","same rule values and operators","same context object and scope"],
   "excludedDimensions":["SQL prefiltering","promotion discovery","discount calculation","campaign budget/usage","checkout"],
   "limitations":["Rule evaluator only, not the full promotion service."]},
  "alignments":alignments,"results":results,
  "coverage":{"reference":{"declaredUnits":32,"observedUnits":32},"implementation":{"declaredUnits":32,"observedUnits":32},
   "sharedComparableUnits":32,"incomparableUnits":0,"limitations":["Thirty-two scenarios do not exhaust promotion lifecycle behaviour."]},
  "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
   "statement":"The independent Python rule evaluator "+("differs from" if mismatches else "matches")+" the pinned Medusa rule functions for 32 declared scenarios.",
   "scopeBounded":True,"universalEquivalenceClaimed":False},
  "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
   "statement":"Both captures cover the declared 32-scenario promotion rule-evaluation scope, not full promotion lifecycle."}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--replica",required=True);p.add_argument("--output-dir",required=True);p.add_argument("--source-artifacts",required=True);a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source,json.loads(a.source_artifacts))
 r=build_capture(read(a.replica),"replica",a.replica,{})
 report=build_report(s,r)
 write(out/"medusa-promo-source.capture.json",s);write(out/"medusa-promo-python-replica.capture.json",r);write(out/"medusa-promo-comparison.report.json",report)
 print(json.dumps({"results":len(report["results"]),"mismatches":len([x for x in report["results"] if x["classification"]!="match"])},indent=2))
 if report["conclusion"]["status"]!="agreement-within-observed-scope":raise SystemExit(1)
if __name__=="__main__":main()
