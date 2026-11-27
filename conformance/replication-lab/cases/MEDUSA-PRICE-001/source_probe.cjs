const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");
const ts = require(process.env.TYPESCRIPT_PATH);
const root = process.env.MEDUSA_SOURCE_ROOT;
const sourcePath = path.join(root,"packages/modules/pricing/src/services/pricing-module.ts");
const source = fs.readFileSync(sourcePath,"utf8");
const sourceFile = ts.createSourceFile(sourcePath,source,ts.ScriptTarget.Latest,true,ts.ScriptKind.TS);
let body;
function visit(node) {
  if (ts.isClassDeclaration(node) && node.name?.text === "PricingModuleService") {
    for (const member of node.members) {
      if (ts.isMethodDeclaration(member) && member.name?.getText(sourceFile).replaceAll('"',"") === "calculatePrices" && member.body) body=member.body.getText(sourceFile);
    }
  }
  ts.forEachChild(node,visit);
}
visit(sourceFile);
if (!body) throw new Error("Could not locate PricingModuleService.calculatePrices body");
const wrapper = `async function calculatePrices(pricingFilters, pricingContext = { context: {} }, sharedContext = {}) ${body}`;
const compiled = ts.transpileModule(wrapper,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.None}}).outputText;
const helpers = {
  groupBy(items,key) { const map=new Map(); for (const item of items) { const k=item[key]; if(!map.has(k)) map.set(k,[]); map.get(k).push(item); } return map; },
  PriceListType:{SALE:"sale",OVERRIDE:"override"},
  MathBN:{lte:(a,b)=>Number(a)<=Number(b)},
  deduplicate:items=>[...new Set(items)],
  isPresent:value=>value!==null && value!==undefined,
  isTaxInclusive:()=>false
};
const calculate = vm.runInNewContext(compiled+"; calculatePrices",helpers);
function price(id,set,amount,listId=null,listType=null) {
  return {id,price_set_id:set,amount:String(amount),raw_amount:{value:String(amount),precision:20},
    currency_code:"eur",price_list_id:listId,price_list_type:listType,
    min_quantity:null,max_quantity:null};
}
const fixtures=[
 {label:"default-only",ids:["ps-default"],rows:[price("default-100","ps-default",100)]},
 {label:"sale-below-default",ids:["ps-sale-low"],rows:[price("sale-80","ps-sale-low",80,"pl-sale","sale"),price("default-100","ps-sale-low",100)]},
 {label:"sale-above-default",ids:["ps-sale-high"],rows:[price("default-100","ps-sale-high",100),price("sale-120","ps-sale-high",120,"pl-sale","sale")]},
 {label:"sale-equal-default",ids:["ps-sale-equal"],rows:[price("sale-100","ps-sale-equal",100,"pl-sale","sale"),price("default-100","ps-sale-equal",100)]},
 {label:"override-only",ids:["ps-override"],rows:[price("override-90","ps-override",90,"pl-override","override"),price("default-100","ps-override",100)]},
 {label:"sale-below-override",ids:["ps-sale-under-override"],rows:[price("sale-80","ps-sale-under-override",80,"pl-sale","sale"),price("override-90","ps-sale-under-override",90,"pl-override","override"),price("default-100","ps-sale-under-override",100)]},
 {label:"override-below-sale",ids:["ps-override-under-sale"],rows:[price("override-90","ps-override-under-sale",90,"pl-override","override"),price("sale-95","ps-override-under-sale",95,"pl-sale","sale"),price("default-100","ps-override-under-sale",100)]},
 {label:"multiple-overrides-lowest-first",ids:["ps-multiple-overrides"],rows:[price("override-80","ps-multiple-overrides",80,"pl-override-low","override"),price("override-90","ps-multiple-overrides",90,"pl-override-high","override"),price("default-100","ps-multiple-overrides",100)]},
 {label:"sale-only-no-original-and-missing-set",ids:["ps-sale-only","ps-missing"],rows:[price("sale-75","ps-sale-only",75,"pl-sale","sale")]}
];
(async()=>{
 const scenarios=[];
 for(const fixture of fixtures){
  const service={
   pricingRepository_:{calculatePrices:async()=>fixture.rows},
   listPriceRules:async()=>[],
   listPricePreferences_:async()=>[]
  };
  const output=await calculate.call(service,{id:fixture.ids},{context:{currency_code:"eur"}},{});
  scenarios.push({label:fixture.label,inputs:{priceSetIds:fixture.ids,candidates:fixture.rows},output});
 }
 const bodyHash=crypto.createHash("sha256").update(body).digest("hex");
 console.log(JSON.stringify({source:"Medusa PricingModuleService.calculatePrices",sourceCommit:process.env.MEDUSA_SOURCE_COMMIT,
  sourcePath:"packages/modules/pricing/src/services/pricing-module.ts",methodBodySha256:bodyHash,typescriptVersion:ts.version,scenarios},null,2));
})().catch(error=>{console.error(error);process.exit(1)});
