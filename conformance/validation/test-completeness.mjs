import assert from "node:assert/strict";
import { validateComparisonCompleteness } from "./completeness.mjs";

const cases = [
  ["complete", "complete", "complete-both"],
  ["incomplete", "complete", "incomplete-reference"],
  ["complete", "incomplete", "incomplete-implementation"],
  ["incomplete", "incomplete", "incomplete-both"],
  ["undetermined", "complete", "undetermined"],
  ["complete", "undetermined", "undetermined"],
  ["incomplete", "undetermined", "undetermined"],
  ["undetermined", "incomplete", "undetermined"],
  ["undetermined", "undetermined", "undetermined"]
];

for (const [referenceStatus, implementationStatus, result] of cases) {
  const report = {
    replicationCompleteness: { referenceStatus, implementationStatus, result, statement: "Completeness states are reported independently." },
    conclusion: { statement: "Observed agreement is limited to the compared dimensions." }
  };
  assert.deepEqual(validateComparisonCompleteness(report), [], `${referenceStatus}/${implementationStatus} must map to ${result}`);
}

const wrongCombination = {
  replicationCompleteness: { referenceStatus: "incomplete", implementationStatus: "complete", result: "undetermined", statement: "wrong mapping" },
  conclusion: { statement: "Only observed agreement." }
};
assert.ok(validateComparisonCompleteness(wrongCombination).some(error => error.includes("incomplete-reference")));

for (const result of ["incomplete-reference", "incomplete-implementation", "incomplete-both", "undetermined"]) {
  const report = {
    replicationCompleteness: { referenceStatus: "incomplete", implementationStatus: "incomplete", result, statement: "Not complete." },
    conclusion: { statement: "Faithful replication is established." }
  };
  assert.ok(validateComparisonCompleteness(report).some(error => error.includes("cannot claim faithful replication")), `${result} must block a faithful replication claim`);
}

assert.ok(validateComparisonCompleteness({ conclusion: {} }).some(error => error.includes("required")));
assert.ok(validateComparisonCompleteness({
  replicationCompleteness: { referenceStatus: "unknown", implementationStatus: "complete", result: "undetermined" },
  conclusion: {}
}).some(error => error.includes("statuses must be")));

console.log("PASS comparison completeness status matrix and claim guards");
