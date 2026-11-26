import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const root = path.resolve("../../schemas/v1");
const fixtureRoot = path.join(root, "fixtures");
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);

function loadJson(file) { return JSON.parse(fs.readFileSync(file, "utf8")); }
function registerTree(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) registerTree(full);
    else if (entry.name.endsWith(".schema.json")) {
      const document = loadJson(full);
      ajv.addSchema(document);
    }
  }
}
registerTree(root);
const captureSchema = loadJson(path.join(root, "capture.schema.json"));
const validate = ajv.getSchema(captureSchema.$id) ?? ajv.compile(captureSchema);
let failed = false;

for (const category of ["valid", "invalid"]) {
  const dir = path.join(fixtureRoot, category);
  for (const name of fs.readdirSync(dir).filter(n => n.endsWith(".json")).sort()) {
    const data = loadJson(path.join(dir, name));
    const pass = Boolean(validate(data));
    const expected = category === "valid";
    const ok = pass === expected;
    console.log(`${ok ? "PASS" : "FAIL"} ${category}/${name} (expected ${expected ? "valid" : "invalid"}, got ${pass ? "valid" : "invalid"})`);
    if (!ok) {
      failed = true;
      for (const error of validate.errors ?? []) console.error(`  ${error.instancePath || "/"}: ${error.message}`);
    }
  }
}
if (failed) process.exit(1);
