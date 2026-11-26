import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { validateCapture } from "./validate-integrity.mjs";
const valid={
  target:{targetId:"target-a"},
  scenarios:[{scenarioId:"scenario-a"}],
  executions:[{executionId:"execution-a",scenarioId:"scenario-a",targetId:"target-a"}],
  observations:[{observationId:"observation-a",targetId:"target-a",executionId:"execution-a",facet:"interface",status:"observed",evidenceRefs:["evidence-a"]}],
  evidence:[{evidenceId:"evidence-a"}],
  coverage:[{scenarioIds:["scenario-a"],executionIds:["execution-a"]}],
  replicationScope:{
    scopeId:"scope-a",description:"One captured interface property.",facets:["interface"],
    propertyInventory:[{propertyId:"property-a",facet:"interface",subject:"root",dimension:"hierarchy",requirement:"required",status:"captured",observationRefs:["observation-a"],evidenceRefs:["evidence-a"]}],
    completeness:{status:"complete",assessedAt:"2026-11-26T16:00:00Z",assessmentMethod:"Inventory-to-evidence check.",rationale:"Every required property is captured."}
  }
};
assert.deepEqual(validateCapture(valid),[]);
const missing=structuredClone(valid); missing.observations[0].evidenceRefs=["missing-evidence"]; missing.executions[0].scenarioId="missing-scenario"; assert.equal(validateCapture(missing).filter(e=>e.includes("unresolved")).length,2);
const duplicate=structuredClone(valid); duplicate.scenarios.push({scenarioId:"scenario-a"}); assert.ok(validateCapture(duplicate).some(e=>e.includes("duplicate identifier")));
const mismatch=structuredClone(valid); mismatch.observations[0].targetId="other-target"; assert.ok(validateCapture(mismatch).some(e=>e.includes("targetId differs")));
const runtime=structuredClone(valid); runtime.runtimeRules=[{supportingObservationIds:["missing-observation"]}]; assert.ok(validateCapture(runtime).some(e=>e.includes("runtimeRules")));
const source=structuredClone(valid); source.sourceRules=[{sourceEvidenceRefs:["missing-source"]}]; assert.ok(validateCapture(source).some(e=>e.includes("sourceRules")));
const falseComplete=structuredClone(valid); falseComplete.replicationScope.propertyInventory[0].status="partial"; falseComplete.replicationScope.completeness.status="complete"; assert.ok(validateCapture(falseComplete).some(e=>e.includes("cannot be complete")));
const missingObservation=structuredClone(valid); missingObservation.replicationScope.propertyInventory[0].observationRefs=["missing-observation"]; assert.ok(validateCapture(missingObservation).some(e=>e.includes("unresolved observation reference")));
const missingEvidence=structuredClone(valid); missingEvidence.replicationScope.propertyInventory[0].evidenceRefs=["missing-evidence"]; assert.ok(validateCapture(missingEvidence).some(e=>e.includes("unresolved evidence reference")));
const duplicateProperty=structuredClone(valid); duplicateProperty.replicationScope.propertyInventory.push(structuredClone(duplicateProperty.replicationScope.propertyInventory[0])); assert.ok(validateCapture(duplicateProperty).some(e=>e.includes("duplicate identifier")));
for (const file of ["reference.capture.json", "independent.capture.json", "independent-mutated.capture.json"]) {
  const capture = JSON.parse(fs.readFileSync(path.resolve("examples/task-board/captures", file), "utf8"));
  assert.deepEqual(validateCapture(capture), [], file + " must have valid cross-record and replication-inventory references");
  assert.equal(capture.replicationScope.completeness.status,"incomplete",file+" must not overclaim completeness");
}
console.log("PASS cross-record integrity, replication inventory, completeness guard, and all three Task Board capture graphs");
