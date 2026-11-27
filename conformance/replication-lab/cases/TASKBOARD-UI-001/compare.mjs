import { createServer } from "node:http";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import { setTimeout as sleep } from "node:timers/promises";
import { pathToFileURL } from "node:url";

const require = createRequire(new URL("../../../runtime/package.json", import.meta.url));
const { chromium } = require("playwright");
const { PNG } = require("pngjs");
const pixelmatch = (await import(pathToFileURL(require.resolve("pixelmatch")))).default;
const root = process.cwd();
const sourceHtml = await readFile(root + "/examples/task-board/reference/index.html");
const sourceServer = createServer((req, res) => { res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(sourceHtml); });
await new Promise(resolve => sourceServer.listen(4172, "127.0.0.1", resolve));
const replicaDir = root + "/conformance/replication-lab/projects/task-board-react";
const replica = spawn("npm", ["run", "preview", "--", "--host", "127.0.0.1", "--port", "4173", "--strictPort", "--outDir", "dist-baseline"], { cwd: replicaDir, stdio: "inherit" });
const mutation = spawn("npm", ["run", "preview", "--", "--host", "127.0.0.1", "--port", "4174", "--strictPort", "--outDir", "dist-mutated"], { cwd: replicaDir, stdio: "inherit" });
async function ready(url) {
  for (let i=0;i<80;i++) { try { const r=await fetch(url); if(r.ok)return; } catch {} await sleep(250); }
  throw new Error("Server did not become ready: "+url);
}
await Promise.all([ready("http://127.0.0.1:4172"),ready("http://127.0.0.1:4173"),ready("http://127.0.0.1:4174")]);
const browser=await chromium.launch({headless:true});
const output={caseId:"TASKBOARD-UI-001",source:"plain HTML/CSS/browser JavaScript",replica:"React 19.1.1/Vite 7.1.7",viewportResults:[],workflowResults:[],mutationDetected:false};
const failures=[];
function assert(ok,message){if(!ok)failures.push(message);}
async function installApi(page){
 const db=new Map();let nextId=1;const requests=[];
 await page.route("**/api/tasks**",async route=>{
  const req=route.request(),method=req.method(),url=new URL(req.url()),id=url.pathname.split("/").pop(),body=req.postDataJSON?.()??{};
  requests.push({method,path:url.pathname,body});
  if(method==="POST"){const item={id:String(nextId++),title:body.title,completed:false};db.set(item.id,item);await route.fulfill({status:201,contentType:"application/json",body:JSON.stringify(item)});}
  else if(method==="PATCH"){const old=db.get(id);if(!old)return route.fulfill({status:404,body:"{}"});const item={...old,...body};db.set(id,item);await route.fulfill({status:200,contentType:"application/json",body:JSON.stringify(item)});}
  else if(method==="DELETE"){db.delete(id);await route.fulfill({status:200,contentType:"application/json",body:JSON.stringify({ok:true})});}
  else await route.fulfill({status:405,body:"{}"});
 });
 return requests;
}
async function open(url,viewport){const page=await browser.newPage({viewport});const requests=await installApi(page);await page.goto(url);await page.locator("#task-input").waitFor();return{page,requests};}
function diff(a,b){const x=PNG.sync.read(a),y=PNG.sync.read(b);if(x.width!==y.width||x.height!==y.height)return{width:x.width,height:x.height,otherWidth:y.width,otherHeight:y.height,differentPixels:-1};const delta=new PNG({width:x.width,height:x.height});const differentPixels=pixelmatch(x.data,y.data,delta.data,x.width,x.height,{threshold:0.1});return{width:x.width,height:x.height,differentPixels,diffImage:PNG.sync.write(delta)};}
async function snapshot(page){return page.locator("main").evaluate(root=>({text:root.innerText,roles:[...root.querySelectorAll("h1,form,input,button,nav,ul,li,p")].map(el=>({tag:el.tagName.toLowerCase(),text:(el.innerText||"").trim(),role:el.getAttribute("role"),label:el.getAttribute("aria-label"),pressed:el.getAttribute("aria-pressed"),live:el.getAttribute("aria-live"),required:el.required??false,type:el.type??null}))}));}
try{
 for(const viewport of [{width:1280,height:800},{width:768,height:900},{width:320,height:720}]){
  const a=await open("http://127.0.0.1:4172",viewport),b=await open("http://127.0.0.1:4173",viewport);
  const shotA=await a.page.screenshot({fullPage:true}),shotB=await b.page.screenshot({fullPage:true});
  const result=diff(shotA,shotB);
  await mkdir(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence",{recursive:true});
  await writeFile(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/viewport-"+viewport.width+"-source.png",shotA);
  await writeFile(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/viewport-"+viewport.width+"-react.png",shotB);
  await writeFile(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/viewport-"+viewport.width+"-diff.png",result.diffImage);
  output.viewportResults.push({name:"viewport-"+viewport.width,viewport,width:result.width,height:result.height,differentPixels:result.differentPixels,sourceSnapshot:await snapshot(a.page),implementationSnapshot:await snapshot(b.page),sourceImage:"viewport-"+viewport.width+"-source.png",implementationImage:"viewport-"+viewport.width+"-react.png"});
  assert(result.differentPixels===0,"Initial viewport mismatch at "+viewport.width+"px: "+result.differentPixels);
  assert(JSON.stringify(await snapshot(a.page))===JSON.stringify(await snapshot(b.page)),"Initial semantic snapshot mismatch at "+viewport.width+"px");
  await a.page.close();await b.page.close();
 }
 const a=await open("http://127.0.0.1:4172",{width:1280,height:800}),b=await open("http://127.0.0.1:4173",{width:1280,height:800});
 async function compareState(name){const shotA=await a.page.screenshot({fullPage:true}),shotB=await b.page.screenshot({fullPage:true});const d=diff(shotA,shotB);await writeFile(root+"/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/"+name+"-source.png",shotA);await writeFile(root+"/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/"+name+"-react.png",shotB);await writeFile(root+"/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/"+name+"-diff.png",d.diffImage);const same=JSON.stringify(await snapshot(a.page))===JSON.stringify(await snapshot(b.page));output.workflowResults.push({state:name,width:d.width,height:d.height,differentPixels:d.differentPixels,semanticMatch:same,sourceSnapshot:await snapshot(a.page),implementationSnapshot:await snapshot(b.page),sourceImage:name+"-source.png",implementationImage:name+"-react.png"});assert(d.differentPixels===0,name+" visual mismatch: "+d.differentPixels);assert(same,name+" semantic mismatch");}
 await a.page.locator("#task-input").fill("Write specification");await b.page.locator("#task-input").fill("Write specification");
 await Promise.all([a.page.getByRole("button",{name:"Add task"}).click(),b.page.getByRole("button",{name:"Add task"}).click()]);
 await Promise.all([a.page.locator("#task-list li").nth(0).waitFor(),b.page.locator("#task-list li").nth(0).waitFor()]);
 await a.page.locator("#task-input").fill("Review evidence");await b.page.locator("#task-input").fill("Review evidence");
 await Promise.all([a.page.getByRole("button",{name:"Add task"}).click(),b.page.getByRole("button",{name:"Add task"}).click()]);
 await Promise.all([a.page.locator("#task-list li").nth(1).waitFor(),b.page.locator("#task-list li").nth(1).waitFor()]);
 await compareState("populated");
 await Promise.all([a.page.getByRole("checkbox",{name:"Complete Write specification"}).click(),b.page.getByRole("checkbox",{name:"Complete Write specification"}).click()]);
 await Promise.all([a.page.locator(".task.done").waitFor(),b.page.locator(".task.done").waitFor()]);
 await compareState("completed");
 await Promise.all([a.page.getByRole("button",{name:"Active",exact:true}).click(),b.page.getByRole("button",{name:"Active",exact:true}).click()]);await compareState("active-filter");
 await Promise.all([a.page.getByRole("button",{name:"Completed",exact:true}).click(),b.page.getByRole("button",{name:"Completed",exact:true}).click()]);await compareState("completed-filter");
 await Promise.all([a.page.getByRole("checkbox",{name:"Complete Write specification"}).click(),b.page.getByRole("checkbox",{name:"Complete Write specification"}).click()]);
 await Promise.all([a.page.locator("#task-list li").waitFor({state:"detached"}),b.page.locator("#task-list li").waitFor({state:"detached"})]);
 await compareState("toggle-back");
 await Promise.all([a.page.getByRole("button",{name:"Active",exact:true}).click(),b.page.getByRole("button",{name:"Active",exact:true}).click()]);
 await Promise.all([a.page.getByRole("button",{name:"Delete Review evidence"}).click(),b.page.getByRole("button",{name:"Delete Review evidence"}).click()]);
 await Promise.all([a.page.getByText("Review evidence").waitFor({state:"detached"}),b.page.getByText("Review evidence").waitFor({state:"detached"})]);
 await compareState("delete");
 assert(JSON.stringify(a.requests)===JSON.stringify(b.requests),"Source and React API request traces differ");
 assert(a.requests.map(x=>x.method).join(",")==="POST,POST,PATCH,PATCH,DELETE","Unexpected API operation trace");
 await a.page.close();await b.page.close();
 const m=await open("http://127.0.0.1:4174",{width:1280,height:800});
 await m.page.locator("#task-input").fill("One");await m.page.getByRole("button",{name:"Add task"}).click();
 await m.page.locator("#task-list li").nth(0).waitFor();
 await m.page.locator("#task-input").fill("Two");await m.page.getByRole("button",{name:"Add task"}).click();
 await m.page.locator("#task-list li").nth(1).waitFor();
 await m.page.getByRole("checkbox",{name:"Complete One"}).click();
 await m.page.waitForFunction(()=>document.querySelector("#task-list input[type=checkbox]")?.checked===true);
 const mutatedSummary=await m.page.locator("#summary").innerText();
 output.mutationDetected=mutatedSummary==="2 tasks · 2 active";
 output.mutatedSummary=mutatedSummary;assert(output.mutationDetected,"Deliberate active-count mutation was not detected");
 await m.page.close();
}finally{await browser.close();sourceServer.close();replica.kill("SIGTERM");mutation.kill("SIGTERM");}
output.failures=failures;
await mkdir(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence",{recursive:true});
await writeFile(root + "/conformance/replication-lab/cases/TASKBOARD-UI-001/evidence/runtime-comparison.json",JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify(output,null,2));
if(failures.length)process.exitCode=1;
