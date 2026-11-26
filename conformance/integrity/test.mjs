import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { validateCapture } from "./validate-integrity.mjs";
const valid={target:{targetId:"target-a"},scenarios:[{scenarioId:"scenario-a"}],executions:[{executionId:"execution-a",scenarioId:"scenario-a",targetId:"target-a"}],observations:[{observationId:"observation-a",targetId:"target-a",executionId:"execution-a",evidenceRefs:["evidence-a"]}],evidence:[{evidenceId:"evidence-a"}],coverage:[{scenarioIds:["scenario-a"],executionIds:["execution-a"]}]};
assert.deepEqual(validateCapture(valid),[]);
const missing=structuredClone(valid); missing.observations[0].evidenceRefs=["missing-evidence"]; missing.executions[0].scenarioId="missing-scenario"; assert.equal(validateCapture(missing).length,2);
const duplicate=structuredClone(valid); duplicate.scenarios.push({scenarioId:"scenario-a"}); assert.ok(validateCapture(duplicate).some(e=>e.includes("duplicate identifier")));
const mismatch=structuredClone(valid); mismatch.observations[0].targetId="other-target"; assert.ok(validateCapture(mismatch).some(e=>e.includes("targetId differs")));
const runtime=structuredClone(valid); runtime.runtimeRules=[{supportingObservationIds:["missing-observation"]}]; assert.ok(validateCapture(runtime).some(e=>e.includes("runtimeRules")));
const source=structuredClone(valid); source.sourceRules=[{sourceEvidenceRefs:["missing-source"]}]; assert.ok(validateCapture(source).some(e=>e.includes("sourceRules")));
for (const file of ["reference.capture.json", "independent.capture.json"]) {
  const capture = JSON.parse(fs.readFileSync(path.resolve("examples/task-board/captures", file), "utf8"));
  assert.deepEqual(validateCapture(capture), [], file + " must have valid cross-record references");
}
console.log("PASS cross-record integrity unit tests and both empirical Task Board capture graphs");
