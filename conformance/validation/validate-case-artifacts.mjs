import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { validateCapture } from "../integrity/validate-integrity.mjs";
import { validateComparisonCompleteness } from "./completeness.mjs";

const [sourcePath, replicaPath, reportPath] = process.argv.slice(2);
if (!sourcePath || !replicaPath || !reportPath) {
  console.error("Usage: node validate-case-artifacts.mjs <source.capture.json> <replica.capture.json> <comparison.report.json>");
  process.exit(2);
}

const root = path.resolve("schemas/v1");
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);

function loadJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function registerTree(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) registerTree(full);
    else if (entry.name.endsWith(".schema.json")) ajv.addSchema(loadJson(full));
  }
}
registerTree(root);

function validateSchema(schemaId, data, label) {
  const validate = ajv.getSchema(schemaId);
  if (!validate) throw new Error(`Schema not registered: ${schemaId}`);
  if (validate(data)) {
    console.log(`PASS schema: ${label}`);
    return true;
  }
  console.error(`FAIL schema: ${label}`);
  for (const error of validate.errors ?? []) {
    console.error(`  ${error.instancePath || "/"}: ${error.message}`);
  }
  return false;
}

let failed = false;
const source = loadJson(sourcePath);
const replica = loadJson(replicaPath);
const report = loadJson(reportPath);

for (const [label, capture] of [["source", source], ["replica", replica]]) {
  failed = !validateSchema("urn:software-rules:schema:v1:capture", capture, label) || failed;
  const integrityErrors = validateCapture(capture);
  if (integrityErrors.length) {
    failed = true;
    console.error(`FAIL cross-record integrity: ${label}`);
    for (const error of integrityErrors) console.error(`  ${error}`);
  } else {
    console.log(`PASS cross-record integrity: ${label}`);
  }
}

failed = !validateSchema("urn:software-rules:schema:v1:comparison-report", report, "comparison") || failed;

const completenessErrors = validateComparisonCompleteness(report);
if (completenessErrors.length) {
  failed = true;
  console.error("FAIL comparison completeness semantics");
  for (const error of completenessErrors) console.error(`  ${error}`);
} else {
  console.log("PASS comparison completeness semantics");
}
if (!report.results?.length || report.results.some(result => result.classification !== "match")) {
  failed = true;
  console.error("FAIL comparison outcomes: every declared result must match for this case to pass");
} else {
  console.log(`PASS comparison outcomes: ${report.results.length} matching results`);
}
if (report.conclusion?.universalEquivalenceClaimed !== false || report.conclusion?.scopeBounded !== true) {
  failed = true;
  console.error("FAIL conclusion must remain explicitly scope-bounded and make no universal equivalence claim");
}

if (failed) process.exit(1);
console.log("PASS Software Rules case artifacts and evidence integrity");
