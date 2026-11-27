const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),crypto=require("node:crypto");
const ts=require(process.env.TYPESCRIPT_PATH);
const sourcePath=path.join(process.env.MEDUSA_SOURCE_ROOT,"packages/modules/promotion/src/utils/validations/promotion-rule.ts");
const source=fs.readFileSync(sourcePath,"utf8");
const sf=ts.createSourceFile(sourcePath,source,ts.ScriptTarget.Latest,true,ts.ScriptKind.TS);
const wanted=new Set(["evaluateRuleValueCondition","areRulesValidForContext"]),found={};
function visit(node){
 if(ts.isFunctionDeclaration(node)&&node.name&&wanted.has(node.name.text))found[node.name.text]=node.getText(sf).replace(/^export\s+/,"");
 ts.forEachChild(node,visit);
}
visit(sf);
for(const name of wanted)if(!found[name])throw new Error("Missing pinned source function: "+name);
const compiled=ts.transpileModule([...wanted].map(n=>found[n]).join("\n"),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.None}}).outputText;
const helpers={
 ApplicationMethodTargetType:{ITEMS:"items",SHIPPING_METHODS:"shipping_methods"},
 isString:v=>typeof v==="string",
 pickValueFromObject:(key,obj)=>key.split(".").reduce((v,k)=>v==null?undefined:v[k],obj),
 MathBN:{gt:(a,b)=>Number(a)>Number(b),gte:(a,b)=>Number(a)>=Number(b),
  lt:(a,b)=>Number(a)<Number(b),lte:(a,b)=>Number(a)<=Number(b)}
};
const funcs=vm.runInNewContext(compiled+"; ({evaluateRuleValueCondition,areRulesValidForContext})",helpers);
const cases=[
 ["eq-scalar-string","condition",["red"],"eq","red"],
 ["eq-number-coercion","condition",["42"],"eq",42],
 ["eq-array-all-match","condition",["red","blue"],"eq",["red","blue"]],
 ["eq-array-one-mismatch","condition",["red","blue"],"eq",["red","green"]],
 ["in-array-any-match","condition",["red","blue"],"in",["green","blue"]],
 ["in-array-no-match","condition",["red","blue"],"in",["green","yellow"]],
 ["ne-empty-array","condition",["red"],"ne",[]],
 ["ne-array-no-match","condition",["red","blue"],"ne",["green","yellow"]],
 ["ne-array-has-match","condition",["red","blue"],"ne",["green","red"]],
 ["gt-numeric","condition",["2"],"gt","10"],
 ["gte-boundary","condition",["10"],"gte",10],
 ["lt-numeric","condition",["10"],"lt","2"],
 ["lte-boundary","condition",["10"],"lte",10],
 ["gt-numeric-lexical-trap","condition",["2"],"gt","10"],
 ["invalid-operator","condition",["x"],"contains","x"],
 ["ne-empty-rule-values","condition",[],"ne","anything"],
 ["empty-rules","context",[],{},{}],
 ["item-prefix-strip","context",[{attribute:"items.product_id",operator:"eq",values:[{value:"shirt"}]}],{product_id:"shirt"},"items"],
 ["shipping-prefix-strip","context",[{attribute:"shipping_methods.option_id",operator:"eq",values:[{value:"express"}]}],{option_id:"express"},"shipping_methods"],
 ["nested-attribute","context",[{attribute:"customer.group.id",operator:"eq",values:[{value:"vip"}]}],{customer:{group:{id:"vip"}}},"order"],
 ["missing-attribute-ne","context",[{attribute:"customer.group",operator:"ne",values:[{value:"blocked"}]}],{},"order"],
 ["missing-attribute-eq","context",[{attribute:"customer.group",operator:"eq",values:[{value:"vip"}]}],{},"order"],
 ["empty-rule-values","context",[{attribute:"product_id",operator:"eq",values:[]}],{product_id:"shirt"},"items"],
 ["non-string-rule-values","context",[{attribute:"product_id",operator:"eq",values:[{value:42}]}],{product_id:42},"items"],
 ["all-rules-must-pass","context",[{attribute:"product_id",operator:"eq",values:[{value:"shirt"}]},{attribute:"customer.group",operator:"eq",values:[{value:"vip"}]}],{product_id:"shirt",customer:{group:"regular"}},"items"],
 ["all-rules-pass","context",[{attribute:"product_id",operator:"eq",values:[{value:"shirt"}]},{attribute:"customer.group",operator:"eq",values:[{value:"vip"}]}],{product_id:"shirt",customer:{group:"vip"}},"items"],
 ["order-scope-does-not-strip-prefix","context",[{attribute:"items.product_id",operator:"eq",values:[{value:"shirt"}]}],{product_id:"shirt"},"order"],
 ["context-eq-array-all","context",[{attribute:"tags",operator:"eq",values:[{value:"sale"},{value:"new"}]}],{tags:["sale","new"]},"items"],
 ["context-eq-array-one-mismatch","context",[{attribute:"tags",operator:"eq",values:[{value:"sale"},{value:"new"}]}],{tags:["sale","clearance"]},"items"],
 ["context-in-array-any","context",[{attribute:"tags",operator:"in",values:[{value:"sale"},{value:"new"}]}],{tags:["clearance","new"]},"items"],
 ["context-in-array-none","context",[{attribute:"tags",operator:"in",values:[{value:"sale"},{value:"new"}]}],{tags:["clearance","winter"]},"items"],
 ["context-no-rules","context",[],{product_id:"shirt"},"items"]
];
function run(c){
 const [label,mode,a,b,cx]=c;
 if(mode==="condition")return {label,inputs:{ruleValues:a,operator:b,valuesToCheck:cx},output:funcs.evaluateRuleValueCondition(a,b,cx)};
 const scope=cx;
 return {label,inputs:{rules:a,context:b,contextScope:scope},output:funcs.areRulesValidForContext(a,b,scope)};
}
const scenarios=cases.map(run);
console.log(JSON.stringify({source:"Medusa promotion-rule validation functions",sourceCommit:process.env.MEDUSA_SOURCE_COMMIT,
 sourcePath:"packages/modules/promotion/src/utils/validations/promotion-rule.ts",
 functionSha256:crypto.createHash("sha256").update([...wanted].map(n=>found[n]).join("\n")).digest("hex"),
 typescriptVersion:ts.version,scenarios},null,2));
