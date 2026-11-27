const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),crypto=require("node:crypto");
const ts=require(process.env.TYPESCRIPT_PATH),root=process.env.MEDUSA_SOURCE_ROOT;
const files=[
 ["line","packages/core/utils/src/totals/line-item/index.ts",["getLineItemTotals"]],
 ["adjustment","packages/core/utils/src/totals/adjustment/index.ts",["calculateAdjustmentTotal"]],
 ["tax","packages/core/utils/src/totals/tax/index.ts",["calculateTaxTotal"]]
];
const declarations={},hashes={};
for(const [group,relative,names] of files){
 const p=path.join(root,relative),source=fs.readFileSync(p,"utf8");
 const sf=ts.createSourceFile(p,source,ts.ScriptTarget.Latest,true,ts.ScriptKind.TS);
 function visit(node){if(ts.isFunctionDeclaration(node)&&node.name&&names.includes(node.name.text))declarations[node.name.text]=node.getText(sf).replace(/^export\s+/,"");ts.forEachChild(node,visit)}
 visit(sf);hashes[group]=crypto.createHash("sha256").update(source).digest("hex");
 for(const name of names)if(!declarations[name])throw new Error("Missing source function "+name+" in "+relative);
}
const compiled=ts.transpileModule(Object.values(declarations).join("\n"),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.None}}).outputText;
class BigNumber {constructor(v){this.value=Number(v)}toJSON(){return this.value}toNumber(){return this.value}}
const helpers={BigNumber,isDefined:v=>v!==null&&v!==undefined,pickValueFromObject:(p,o)=>p.split(".").reduce((v,k)=>v==null?undefined:v[k],o),
 MathBN:{convert:v=>Number(v),add:(a,b)=>Number(a)+Number(b),sub:(a,b)=>Number(a)-Number(b),mult:(a,b)=>Number(a)*Number(b),
 div:(a,b)=>Number(a)/Number(b),sum:(...xs)=>xs.reduce((a,b)=>a+Number(b),0),eq:(a,b)=>Number(a)===Number(b)}};
const calculate=vm.runInNewContext(compiled+"; ({getLineItemTotals})",helpers).getLineItemTotals;
const fixtures=[
 {label:"basic-no-tax",unit_price:50,quantity:2,tax_lines:[],adjustments:[]},
 {label:"exclusive-tax-20",unit_price:50,quantity:2,tax_lines:[{rate:20}],adjustments:[]},
 {label:"multiple-additive-tax-lines",unit_price:100,quantity:1,tax_lines:[{rate:10},{rate:5}],adjustments:[]},
 {label:"inclusive-tax-20",unit_price:120,quantity:1,is_tax_inclusive:true,tax_lines:[{rate:20}],adjustments:[]},
 {label:"exclusive-discount-with-tax",unit_price:100,quantity:1,tax_lines:[{rate:20}],adjustments:[{amount:20,is_tax_inclusive:false}]},
 {label:"inclusive-discount-with-tax",unit_price:120,quantity:1,is_tax_inclusive:true,tax_lines:[{rate:20}],adjustments:[{amount:24,is_tax_inclusive:true}]},
 {label:"multiple-exclusive-adjustments",unit_price:50,quantity:2,tax_lines:[{rate:20}],adjustments:[{amount:10,is_tax_inclusive:false},{amount:5,is_tax_inclusive:false}]},
 {label:"mixed-inclusive-exclusive-adjustments",unit_price:50,quantity:2,tax_lines:[{rate:20}],adjustments:[{amount:24,is_tax_inclusive:true},{amount:10,is_tax_inclusive:false}]},
 {label:"fractional-quantity",unit_price:40,quantity:2.5,tax_lines:[{rate:10}],adjustments:[]},
 {label:"zero-quantity",unit_price:100,quantity:0,tax_lines:[{rate:20}],adjustments:[]},
 {label:"empty-tax-context-with-discount",unit_price:100,quantity:1,tax_lines:[],adjustments:[{amount:20,is_tax_inclusive:false}]},
 {label:"inclusive-price-with-multiple-tax-lines",unit_price:115,quantity:1,is_tax_inclusive:true,tax_lines:[{rate:10},{rate:5}],adjustments:[{amount:11.5,is_tax_inclusive:true}]},
 {label:"returned-quantity-prorated-discount",unit_price:25,quantity:4,tax_lines:[{rate:20}],adjustments:[{amount:40,is_tax_inclusive:false}],detail:{return_received_quantity:1}},
 {label:"inclusive-return-refund",unit_price:120,quantity:2,is_tax_inclusive:true,tax_lines:[{rate:20}],adjustments:[{amount:24,is_tax_inclusive:true}],detail:{return_dismissed_quantity:1}}
];
function round(v){return v===undefined||v===null?null:Number(Number(v).toFixed(8))}
function normalize(result,item){
 const out={};for(const k of ["quantity","unit_price","subtotal","total","original_subtotal","original_total","discount_subtotal","discount_tax_total","discount_total","tax_total","original_tax_total","refundable_total","refundable_total_per_unit"])out[k]=round(result[k]?.value??result[k]);
 out.adjustments=(item.adjustments||[]).map(a=>({amount:round(a.amount),is_tax_inclusive:a.is_tax_inclusive??null,subtotal:round(a.subtotal?.value??a.subtotal),total:round(a.total?.value??a.total)}));
 return out;
}
const scenarios=fixtures.map(f=>{const item={...f,adjustments:f.adjustments.map(a=>({...a})),tax_lines:f.tax_lines.map(t=>({...t}))};
 const result=calculate(item,{includeTax:false});
 return {label:f.label,inputs:{unit_price:f.unit_price,quantity:f.quantity,is_tax_inclusive:f.is_tax_inclusive??false,tax_lines:f.tax_lines,adjustments:f.adjustments,detail:f.detail??null},output:normalize(result,item)};
});
console.log(JSON.stringify({source:"Medusa getLineItemTotals / calculateAdjustmentTotal / calculateTaxTotal",
 sourceCommit:process.env.MEDUSA_SOURCE_COMMIT,sourceFiles:hashes,typescriptVersion:ts.version,scenarios},null,2));
