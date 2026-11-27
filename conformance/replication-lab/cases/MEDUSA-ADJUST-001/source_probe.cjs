const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),crypto=require("node:crypto");
const ts=require(process.env.TYPESCRIPT_PATH);
const root=process.env.MEDUSA_SOURCE_ROOT;
const sourcePath=path.join(root,"packages/core/utils/src/totals/adjustment/index.ts");
const source=fs.readFileSync(sourcePath,"utf8");
const sf=ts.createSourceFile(sourcePath,source,ts.ScriptTarget.Latest,true,ts.ScriptKind.TS);
let declaration;
function visit(node){
 if(ts.isFunctionDeclaration(node)&&node.name?.text==="calculateAdjustmentTotal") declaration=node.getText(sf).replace(/^export\s+/,"");
 ts.forEachChild(node,visit);
}
visit(sf);
if(!declaration)throw new Error("calculateAdjustmentTotal not found in pinned Medusa source");
const compiled=ts.transpileModule(declaration,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.None}}).outputText;
class BigNumber {constructor(value){this.value=Number(value)} toJSON(){return this.value}}
const helpers={
 BigNumber,isDefined:value=>value!==null&&value!==undefined,
 MathBN:{
  convert:value=>Number(value),
  add:(a,b)=>Number(a)+Number(b),
  div:(a,b)=>Number(a)/Number(b),
  mult:(a,b)=>Number(a)*Number(b),
  eq:(a,b)=>Number(a)===Number(b)
 }
};
const calculate=vm.runInNewContext(compiled+"; calculateAdjustmentTotal",helpers);
const fixtures=[
 {label:"no-adjustments",quantity:1,taxRate:0.2,adjustments:[]},
 {label:"single-exclusive",quantity:2,taxRate:0.2,adjustments:[{amount:20,is_tax_inclusive:false}]},
 {label:"multiple-exclusive",quantity:4,taxRate:0.2,adjustments:[{amount:20,is_tax_inclusive:false},{amount:10,is_tax_inclusive:false}]},
 {label:"inclusive-single",quantity:2,taxRate:0.2,adjustments:[{amount:24,is_tax_inclusive:true}]},
 {label:"mixed-inclusive-exclusive",quantity:2,taxRate:0.2,adjustments:[{amount:24,is_tax_inclusive:true},{amount:10,is_tax_inclusive:false}]},
 {label:"missing-adjustment-amount",quantity:2,taxRate:0.2,adjustments:[{amount:undefined,is_tax_inclusive:false},{amount:10,is_tax_inclusive:false}]},
 {label:"zero-quantity",quantity:0,taxRate:0.2,adjustments:[{amount:20,is_tax_inclusive:false}]},
 {label:"fractional-quantity",quantity:2.5,taxRate:0.2,adjustments:[{amount:10,is_tax_inclusive:false}]},
 {label:"no-tax-context",quantity:2,taxRate:undefined,adjustments:[{amount:20,is_tax_inclusive:true}]}
];
function round(v){return v===undefined?null:Number(Number(v).toFixed(8))}
function normalize(result,adjustments){
 return {
  adjustmentsTotal:round(result.adjustmentsTotal),
  adjustmentsSubtotal:round(result.adjustmentsSubtotal),
  adjustmentsTaxTotal:round(result.adjustmentsTaxTotal),
  adjustmentPerItem:round(result.adjustmentPerItem),
  adjustmentSubtotalPerItem:round(result.adjustmentSubtotalPerItem),
  adjustmentTaxTotalPerItem:round(result.adjustmentTaxTotalPerItem),
  adjustments:adjustments.map(a=>({amount:round(a.amount),is_tax_inclusive:a.is_tax_inclusive??null,subtotal:round(a.subtotal?.value??a.subtotal),total:round(a.total?.value??a.total)}))
 };
}
const scenarios=fixtures.map(f=>{
 const adjustments=f.adjustments.map(a=>({...a}));
 const result=calculate({item:{quantity:f.quantity},adjustments,taxRate:f.taxRate});
 return {label:f.label,inputs:{quantity:f.quantity,taxRate:f.taxRate??null,adjustments:f.adjustments.map(a=>({amount:a.amount??null,is_tax_inclusive:a.is_tax_inclusive??null}))},output:normalize(result,adjustments)};
});
console.log(JSON.stringify({source:"Medusa calculateAdjustmentTotal",sourceCommit:process.env.MEDUSA_SOURCE_COMMIT,
 sourcePath:"packages/core/utils/src/totals/adjustment/index.ts",functionSha256:crypto.createHash("sha256").update(declaration).digest("hex"),
 typescriptVersion:ts.version,scenarios},null,2));
