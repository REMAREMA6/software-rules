'use strict';
require('reflect-metadata');
const path=require('node:path');
const {DataSource}=require(path.resolve(process.cwd(),'build/package/index.js'));
const config={type:'postgres',host:process.env.PGHOST||'127.0.0.1',port:Number(process.env.PGPORT||5432),
 username:process.env.PGUSER||'postgres',password:process.env.PGPASSWORD||'postgres',
 database:process.env.PGDATABASE||'postgres',logging:false};
async function runner(ds){const r=ds.createQueryRunner();await r.connect();return r}
async function main(){
 const ds=new DataSource(config);await ds.initialize();
 try{
  await ds.query('DROP TABLE IF EXISTS software_rules_doctors');
  await ds.query('DROP TABLE IF EXISTS software_rules_accounts');
  await ds.query('CREATE TABLE software_rules_accounts (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL)');
  await ds.query('INSERT INTO software_rules_accounts(id,balance) VALUES (1,100)');
  const rcA=await runner(ds),rcB=await runner(ds);
  let readCommitted;
  try{
   await rcA.startTransaction('READ COMMITTED');
   const first=Number((await rcA.query('SELECT balance FROM software_rules_accounts WHERE id=1'))[0].balance);
   await rcB.startTransaction('READ COMMITTED');
   await rcB.query('UPDATE software_rules_accounts SET balance=150 WHERE id=1');
   await rcB.commitTransaction();
   const second=Number((await rcA.query('SELECT balance FROM software_rules_accounts WHERE id=1'))[0].balance);
   await rcA.commitTransaction();
   readCommitted={first,second};
  }finally{if(rcA.isTransactionActive)await rcA.rollbackTransaction().catch(()=>{});if(rcB.isTransactionActive)await rcB.rollbackTransaction().catch(()=>{});await rcA.release();await rcB.release()}
  const rrA=await runner(ds),rrB=await runner(ds);let repeatableRead;
  try{
   await rrA.startTransaction('REPEATABLE READ');
   const first=Number((await rrA.query('SELECT balance FROM software_rules_accounts WHERE id=1'))[0].balance);
   await rrB.startTransaction('READ COMMITTED');
   await rrB.query('UPDATE software_rules_accounts SET balance=200 WHERE id=1');
   await rrB.commitTransaction();
   const second=Number((await rrA.query('SELECT balance FROM software_rules_accounts WHERE id=1'))[0].balance);
   await rrA.commitTransaction();
   repeatableRead={first,second};
  }finally{if(rrA.isTransactionActive)await rrA.rollbackTransaction().catch(()=>{});if(rrB.isTransactionActive)await rrB.rollbackTransaction().catch(()=>{});await rrA.release();await rrB.release()}
  await ds.query('CREATE TABLE software_rules_doctors (id INTEGER PRIMARY KEY, on_call BOOLEAN NOT NULL)');
  await ds.query('INSERT INTO software_rules_doctors(id,on_call) VALUES (1,TRUE),(2,TRUE)');
  const sA=await runner(ds),sB=await runner(ds);
  let serializable;
  try{
   await sA.startTransaction('SERIALIZABLE');await sB.startTransaction('SERIALIZABLE');
   const countA=Number((await sA.query('SELECT COUNT(*)::int AS n FROM software_rules_doctors WHERE on_call=TRUE'))[0].n);
   const countB=Number((await sB.query('SELECT COUNT(*)::int AS n FROM software_rules_doctors WHERE on_call=TRUE'))[0].n);
   await sA.query('UPDATE software_rules_doctors SET on_call=FALSE WHERE id=1');
   await sB.query('UPDATE software_rules_doctors SET on_call=FALSE WHERE id=2');
   let commitA='committed',commitB='committed',errorCode=null;
   await sA.commitTransaction();
   try{await sB.commitTransaction()}catch(error){commitB='aborted';errorCode=error.driverError?.code||error.code||null;await sB.rollbackTransaction().catch(()=>{})}
   const remaining=Number((await ds.query('SELECT COUNT(*)::int AS n FROM software_rules_doctors WHERE on_call=TRUE'))[0].n);
   serializable={countA,countB,commitA,commitB,errorCode,remainingOnCall:remaining};
  }finally{if(sA.isTransactionActive)await sA.rollbackTransaction().catch(()=>{});if(sB.isTransactionActive)await sB.rollbackTransaction().catch(()=>{});await sA.release();await sB.release()}
  const scenarios=[
   {label:'read-committed-nonrepeatable-read',output:readCommitted},
   {label:'repeatable-read-stable-snapshot',output:repeatableRead},
   {label:'serializable-write-skew-prevention',output:serializable}
  ];
  const checks=[
   readCommitted.first===100&&readCommitted.second===150,
   repeatableRead.first===150&&repeatableRead.second===150,
   serializable.countA===2&&serializable.countB===2,
   serializable.commitA==='committed'&&serializable.commitB==='aborted',
   serializable.errorCode==='40001',
   serializable.remainingOnCall===1
  ];
  console.log(JSON.stringify({source:'TypeORM QueryRunner / PostgreSQL',sourceCommit:process.env.TYPEORM_SOURCE_COMMIT,
   packageVersion:require('./package.json').version,database:'PostgreSQL',scenarios,checks,passed:checks.every(Boolean)},null,2));
  if(!checks.every(Boolean))process.exitCode=1;
 }finally{await ds.destroy()}
}
main().catch(e=>{console.error(e.stack);process.exit(1)});
