'use strict';
const fs=require("node:fs");const os=require("node:os");const path=require("node:path");require("reflect-metadata");
const {DataSource,EntitySchema}=require(path.resolve(process.cwd(),"build/package/index.js"));
const Post=new EntitySchema({name:"Post",tableName:"post",columns:{id:{type:Number,primary:true,generated:true},title:{type:String,nullable:false}}});
async function open(file){const ds=new DataSource({type:"better-sqlite3",database:file,entities:[Post],synchronize:true,logging:false});await ds.initialize();return ds;}
async function reopen(file){const ds=await open(file);try{return await ds.manager.find(Post);}finally{await ds.destroy();}}
async function commitDurability(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"typeorm-durable-"));const file=path.join(dir,"commit.sqlite");
 let ds=await open(file);await ds.manager.transaction(async manager=>{await manager.save(Post,{title:"committed"});});await ds.destroy();
 const rows=await reopen(file);return {label:"commit-survives-reopen",rows:rows.map(x=>({id:x.id,title:x.title})),count:rows.length};
}
async function rollbackDurability(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"typeorm-rollback-"));const file=path.join(dir,"rollback.sqlite");
 let ds=await open(file);let error=false;
 try{await ds.manager.transaction(async manager=>{await manager.save(Post,{title:"transient"});await manager.save(Post,{});});}catch(e){error=true;}await ds.destroy();
 const rows=await reopen(file);return {label:"rollback-survives-reopen",errorPropagated:error,rows:rows.map(x=>({id:x.id,title:x.title})),count:rows.length};
}
async function updateDurability(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"typeorm-update-"));const file=path.join(dir,"update.sqlite");
 let ds=await open(file);const post=await ds.manager.save(Post,{title:"before"});await ds.manager.transaction(async manager=>{const row=await manager.findOneByOrFail(Post,{id:post.id});row.title="after";await manager.save(Post,row);});await ds.destroy();
 const rows=await reopen(file);return {label:"update-survives-reopen",rows:rows.map(x=>({id:x.id,title:x.title})),count:rows.length};
}
async function constraintRollback(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"typeorm-constraint-"));const file=path.join(dir,"constraint.sqlite");
 let ds=await open(file);let errorCategory="none";
 try{await ds.manager.transaction(async manager=>{await manager.save(Post,{title:"must-rollback"});await manager.save(Post,{});});}catch(e){errorCategory=/NOT NULL|constraint failed/i.test(String(e.message))?"integrity-constraint":e.name;}await ds.destroy();
 const rows=await reopen(file);return {label:"constraint-failure-atomicity",errorCategory,rows:rows.map(x=>({id:x.id,title:x.title})),count:rows.length};
}
async function main(){
 const scenarios=[await commitDurability(),await rollbackDurability(),await updateDurability(),await constraintRollback()];
 const report={source:"TypeORM pinned source checkout",sourceCommit:process.env.TYPEORM_SOURCE_COMMIT,packageVersion:require("./package.json").version,driver:"better-sqlite3",scenarios};
 const checks=[scenarios[0].count===1&&scenarios[0].rows[0].title==="committed",scenarios[1].errorPropagated&&scenarios[1].count===0,scenarios[2].count===1&&scenarios[2].rows[0].title==="after",scenarios[3].errorCategory==="integrity-constraint"&&scenarios[3].count===0];
 report.checks=checks;report.passed=checks.every(Boolean);console.log(JSON.stringify(report,null,2));if(!report.passed)process.exitCode=1;
}
main().catch(e=>{console.error(e.stack);process.exit(1)});
