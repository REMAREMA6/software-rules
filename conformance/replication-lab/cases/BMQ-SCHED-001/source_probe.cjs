'use strict';
const {Queue,Worker}=require('./dist/cjs');
const IORedis=require('ioredis');
const {randomUUID}=require('node:crypto');
const redisOptions={host:process.env.REDIS_HOST||'127.0.0.1',port:Number(process.env.REDIS_PORT||6379),maxRetriesPerRequest:null};
async function close(c){if(!c||c.status==='end')return;try{await c.quit()}catch{c.disconnect()}}
async function main(){
 const name='software-rules-schedule-'+randomUUID();
 const qc=new IORedis(redisOptions),wc=new IORedis(redisOptions);
 const queue=new Queue(name,{connection:qc});let worker;
 const processed=[],events=[];
 try{
  await queue.waitUntilReady();
  const job=await queue.add('scheduled',{value:1},{jobId:'scheduled-job',delay:5000});
  const initialState=await job.getState();
  await job.changeDelay(250);
  const afterChangeDelay=await job.getState();
  worker=new Worker(name,async current=>{processed.push(current.name);return 'processed';},{connection:wc,concurrency:1});
  const completed=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(new Error('rescheduled delayed job did not complete')),7000);
   worker.on('active',current=>events.push({event:'active',jobId:current.id}));
   worker.on('completed',(current,result)=>{events.push({event:'completed',jobId:current.id});clearTimeout(timer);resolve(result)});
   worker.on('failed',(current,error)=>{clearTimeout(timer);reject(error)});
  });
  const finalState=await job.getState();
  const cancelled=await queue.add('cancelled',{value:2},{jobId:'cancelled-job',delay:5000});
  const cancelInitialState=await cancelled.getState();
  await cancelled.remove();
  const cancelledJob=await queue.getJob('cancelled-job');
  await new Promise(resolve=>setTimeout(resolve,350));
  const counts=await queue.getJobCounts('delayed','waiting','active','completed','failed');
  const output={
   scheduled:{initialState,afterChangeDelay,events,finalState,processed,result:completed},
   cancelled:{initialState:cancelInitialState,removed:cancelledJob===undefined||cancelledJob===null,
    jobExists:!!cancelledJob,processed:processed.includes('cancelled'),finalState:cancelledJob?await cancelledJob.getState():'missing'},
   counts
  };
  const checks=[
   initialState==='delayed',afterChangeDelay==='delayed',
   events.length===2&&events[0].event==='active'&&events[1].event==='completed',
   finalState==='completed'&&completed==='processed',
   cancelInitialState==='delayed'&&(cancelledJob===undefined||cancelledJob===null),
   !processed.includes('cancelled')&&counts.delayed===0&&counts.completed===1
  ];
  console.log(JSON.stringify({source:'BullMQ pinned source checkout',sourceCommit:process.env.BULLMQ_SOURCE_COMMIT,
   packageVersion:require('./package.json').version,scenarios:[output],checks,passed:checks.every(Boolean)},null,2));
  if(!checks.every(Boolean))process.exitCode=1;
 }finally{
  if(worker)await worker.close(true).catch(()=>{});
  await queue.obliterate({force:true}).catch(()=>{});await queue.close().catch(()=>{});
  await Promise.all([close(qc),close(wc)]);
 }
}
main().catch(e=>{console.error(e.stack);process.exit(1)});
