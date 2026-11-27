import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { validateCapture } from "./validate-integrity.mjs";
const valid={
  target:{targetId:"target-a"},
  scenarios:[{scenarioId:"scenario-a"}],
  executions:[{executionId:"execution-a",scenarioId:"scenario-a",targetId:"target-a"}],
  observations:[{observationId:"observation-a",targetId:"target-a",executionId:"execution-a",facet:"interface",status:"observed",evidenceRefs:["evidence-a"]}],
  evidence:[{evidenceId:"evidence-a",evidenceClass:"runtime"}],
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
const detachedEvidence=structuredClone(valid); detachedEvidence.evidence.push({evidenceId:"evidence-b",evidenceClass:"runtime"}); detachedEvidence.replicationScope.propertyInventory[0].evidenceRefs=["evidence-b"]; assert.ok(validateCapture(detachedEvidence).some(e=>e.includes("not attached to any observation")));
const partialOnly=structuredClone(valid); partialOnly.observations[0].payload={completeness:{status:"partial"}}; assert.ok(validateCapture(partialOnly).some(e=>e.includes("explicitly marked partial")));
const sourceOnly=structuredClone(valid); sourceOnly.evidence[0].evidenceClass="source-artifact"; assert.ok(validateCapture(sourceOnly).some(e=>e.includes("runtime evidence")));
const validPartial=structuredClone(valid); validPartial.replicationScope.propertyInventory[0].status="partial"; validPartial.observations[0].payload={completeness:{status:"partial"}}; validPartial.replicationScope.completeness.status="incomplete"; assert.deepEqual(validateCapture(validPartial),[]);
const missingObservation=structuredClone(valid); missingObservation.replicationScope.propertyInventory[0].observationRefs=["missing-observation"]; assert.ok(validateCapture(missingObservation).some(e=>e.includes("unresolved observation reference")));
const missingEvidence=structuredClone(valid); missingEvidence.replicationScope.propertyInventory[0].evidenceRefs=["missing-evidence"]; assert.ok(validateCapture(missingEvidence).some(e=>e.includes("unresolved evidence reference")));
const duplicateProperty=structuredClone(valid); duplicateProperty.replicationScope.propertyInventory.push(structuredClone(duplicateProperty.replicationScope.propertyInventory[0])); assert.ok(validateCapture(duplicateProperty).some(e=>e.includes("duplicate identifier")));
for (const file of ["reference.capture.json", "independent.capture.json", "independent-mutated.capture.json"]) {
  const capture = JSON.parse(fs.readFileSync(path.resolve("examples/task-board/captures", file), "utf8"));
  assert.deepEqual(validateCapture(capture), [], file + " must have valid cross-record and replication-inventory references");
  assert.equal(capture.replicationScope.completeness.status,"incomplete",file+" must report unresolved required properties as incomplete");
  for (const property of capture.replicationScope.propertyInventory) {
    if (property.requirement === "required") {
      assert.ok(["captured","partial","not-applicable"].includes(property.status),file+" has an unaccounted required property "+property.propertyId);
    }
  }
}
const bullmqSource = JSON.parse(fs.readFileSync(path.resolve("examples/cross-repository/captures/bullmq-source.capture.json"), "utf8"));
assert.deepEqual(validateCapture(bullmqSource), [], "BullMQ source-derived capture must have valid references and an explicit incomplete inventory");
assert.equal(bullmqSource.replicationScope.completeness.status, "incomplete", "source-derived rules must not be treated as runtime-complete");
assert.ok(bullmqSource.replicationScope.propertyInventory.every(property => property.status === "source-inferred"), "BullMQ properties remain explicitly source-inferred until runtime evidence is collected");
const minimal = JSON.parse(fs.readFileSync(path.resolve("schemas/v1/fixtures/valid/minimal-capture.json"), "utf8"));
assert.deepEqual(validateCapture(minimal), [], "minimal capture fixture must have valid inventory references");
assert.equal(minimal.replicationScope.completeness.status, "incomplete", "minimal fixture must not claim replication completeness");
console.log("PASS cross-record integrity, replication completeness enforcement, minimal incomplete fixture, and all three explicitly incomplete Task Board capture graphs");
