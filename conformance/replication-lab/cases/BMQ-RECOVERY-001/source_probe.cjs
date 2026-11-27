'use strict';
const {Queue,QueueEvents,Worker}=require('./dist/cjs');
const IORedis=require('ioredis');
const {randomUUID}=require('node:crypto');
const redisOptions={host:process.env.REDIS_HOST||'127.0.0.1',port:Number(process.env.REDIS_PORT||6379),maxRetriesPerRequest:null};
async function close(client){if(!client||client.status==='end')return;try{await client.quit();}catch{client.disconnect();}}
async function runScenario(label,maxStalledCount){
 const name='software-rules-stalled-'+label+'-'+randomUUID();
 const qc=new IORedis(redisOptions),ec=new IORedis(redisOptions),w1c=new IORedis(redisOptions),w2c=new IORedis(redisOptions);
 const queue=new Queue(name,{connection:qc});const events=new QueueEvents(name,{connection:ec});
 let worker1,worker2;const eventCounts={stalled:0,completed:0,failed:0};const processed=[];
 try{
  await Promise.all([queue.waitUntilReady(),events.waitUntilReady()]);
  events.on('stalled',()=>eventCounts.stalled++);
  const job=await queue.add('work',{value:label},{jobId:'recovery-job'});
  worker1=new Worker(name,async()=>new Promise(()=>{}),{connection:w1c,lockDuration:1000,stalledInterval:100,concurrency:1});
  const active=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(new Error(label+': initial worker did not activate job')),5000);
   worker1.once('active',(activeJob)=>{clearTimeout(timer);resolve(activeJob.id);});
  });
  await worker1.close(true);worker1=null;
  await new Promise(resolve=>setTimeout(resolve,1100));
  worker2=new Worker(name,async current=>{processed.push(current.data.value);return 'recovered';},
   {connection:w2c,lockDuration:1000,stalledInterval:100,maxStalledCount,concurrency:1});
  const terminal=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(new Error(label+': stalled job did not reach terminal state')),8000);
   worker2.on('completed',(current,result)=>{eventCounts.completed++;clearTimeout(timer);resolve({state:'completed',attemptsStarted:current.attemptsStarted,attemptsMade:current.attemptsMade,stalledCounter:current.stalledCounter,result});});
   worker2.on('failed',(current,error)=>{eventCounts.failed++;clearTimeout(timer);resolve({state:'failed',attemptsStarted:current?.attemptsStarted,attemptsMade:current?.attemptsMade,stalledCounter:current?.stalledCounter,reason:error.message});});
  });
  await new Promise(resolve=>setTimeout(resolve,100));
  const counts=await queue.getJobCounts('waiting','active','completed','failed');
  return {label,initialActiveId:active,terminal,processed,eventCounts,counts};
 }finally{
  if(worker1)await worker1.close(true).catch(()=>{});
  if(worker2)await worker2.close(true).catch(()=>{});
  await events.close().catch(()=>{});await queue.obliterate({force:true}).catch(()=>{});await queue.close().catch(()=>{});
  await Promise.all([close(qc),close(ec),close(w1c),close(w2c)]);
 }
}
(async()=>{
 const recovered=await runScenario('recover-once',1);
 const limited=await runScenario('fail-at-zero-stalled-limit',0);
 const scenarios=[recovered,limited];
 const checks=[
  recovered.terminal.state==='completed'&&recovered.terminal.stalledCounter===1,
  recovered.counts.completed===1&&recovered.counts.failed===0,
  recovered.eventCounts.stalled===1&&recovered.eventCounts.completed===1,
  limited.terminal.state==='failed'&&limited.terminal.reason==='job stalled more than allowable limit',
  limited.terminal.stalledCounter===1&&limited.terminal.attemptsStarted===2&&limited.terminal.attemptsMade===1,
  limited.counts.failed===1&&limited.counts.completed===0,
 ];
 const report={source:'BullMQ pinned source checkout',sourceCommit:process.env.BULLMQ_SOURCE_COMMIT,packageVersion:require('./package.json').version,
  capturedAt:new Date().toISOString(),scenarios,checks,passed:checks.every(Boolean)};
 console.log(JSON.stringify(report,null,2));if(!report.passed)process.exitCode=1;
})().catch(e=>{console.error(e.stack);process.exit(1)});
