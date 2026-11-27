import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { validateComparisonCompleteness } from "./completeness.mjs";

const root = path.resolve("../../schemas/v1");
const comparisonRoot = path.resolve("../../comparison/examples");
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);

function loadJson(file) { return JSON.parse(fs.readFileSync(file, "utf8")); }
function registerTree(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) registerTree(full);
    else if (entry.name.endsWith(".schema.json")) ajv.addSchema(loadJson(full));
  }
}
registerTree(root);


const suites = [
 {name:"capture",schema:loadJson(path.join(root,"capture.schema.json")),fixtures:path.join(root,"fixtures")},
 {name:"comparison",schema:loadJson(path.join(root,"comparison-report.schema.json")),fixtures:comparisonRoot}
];
let failed=false;
for(const suite of suites){
 const validate=ajv.getSchema(suite.schema.$id)??ajv.compile(suite.schema);
 for(const category of ["valid","invalid"]){
  const dir=path.join(suite.fixtures,category);
  if(!fs.existsSync(dir)) continue;
  for(const name of fs.readdirSync(dir).filter(n=>n.endsWith(".json")).sort()){
   const data=loadJson(path.join(dir,name));
   const schemaPass=Boolean(validate(data));
   const semanticErrors=suite.name==="comparison" && schemaPass ? validateComparisonCompleteness(data) : [];
   const pass=schemaPass && semanticErrors.length===0;
   const expected=category==="valid",ok=pass===expected;
   console.log(`${ok?"PASS":"FAIL"} ${suite.name}/${category}/${name} (expected ${expected?"valid":"invalid"}, got ${pass?"valid":"invalid"})`);
   if(!ok){
    failed=true;
    for(const error of validate.errors??[]) console.error(`  ${error.instancePath||"/"}: ${error.message}`);
    for(const error of semanticErrors) console.error(`  semantic: ${error}`);
   }
  }
 }
}
if(failed)process.exit(1);
