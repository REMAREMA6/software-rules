const http = require("node:http");

function send(res,status,contentType,body,headers={}) {
  res.writeHead(status,{"Content-Type":contentType,...headers});
  res.end(body);
}
const server=http.createServer((req,res)=>{
  if(req.url==="/json") return send(res,200,"application/json",JSON.stringify({ok:true,n:7}));
  if(req.url==="/text") return send(res,200,"text/plain","ready");
  if(req.url==="/not-found") return send(res,404,"application/json",JSON.stringify({error:"missing"}));
  if(req.url==="/unavailable") return send(res,503,"text/plain","down");
  if(req.url==="/redirect") { res.writeHead(302,{Location:"/json"}); return res.end(); }
  if(req.url.startsWith("/echo") && req.method==="POST") {
    let body=""; req.on("data",chunk=>body+=chunk); req.on("end",()=>send(res,200,"application/json",JSON.stringify({body,xTrace:req.headers["x-trace"]||null}))); return;
  }
  if(req.url.startsWith("/query")) return send(res,200,"application/json",JSON.stringify({url:req.url}));
  if(req.url==="/slow") return setTimeout(()=>send(res,200,"application/json",JSON.stringify({slow:true})),120);
  if(req.url==="/malformed") return send(res,200,"application/json","{broken");
  return send(res,404,"text/plain","unknown");
});
function parseOutcome(response) {
  return {kind:"response",status:response.status,data:response.data};
}
async function main() {
  const axios = (await import(process.env.AXIOS_SOURCE_ROOT + "/index.js")).default;
  await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
  const base="http://127.0.0.1:"+server.address().port;
  const scenarios=[];
  const add=async(label,fn)=>{
    try { const response=await fn(); scenarios.push({label,outcome:parseOutcome(response)}); }
    catch(error) {
      if(error.response) scenarios.push({label,outcome:{kind:"http-error",status:error.response.status,data:error.response.data}});
      else if(error.code==="ECONNABORTED"||error.code==="ETIMEDOUT") scenarios.push({label,outcome:{kind:"timeout"}});
      else scenarios.push({label,outcome:{kind:"network-error",code:error.code||null}});
    }
  };
  await add("json-response",()=>axios.get(base+"/json"));
  await add("text-response",()=>axios.get(base+"/text"));
  await add("http-404",()=>axios.get(base+"/not-found"));
  await add("http-503",()=>axios.get(base+"/unavailable"));
  await add("redirect-follow",()=>axios.get(base+"/redirect"));
  await add("post-json-custom-header",()=>axios.post(base+"/echo",{hello:"world"},{headers:{"X-Trace":"123"}}));
  await add("query-serialization",()=>axios.get(base+"/query",{params:{q:"a b",page:2}}));
  await add("request-timeout",()=>axios.get(base+"/slow",{timeout:20}));
  await add("malformed-json-silent-fallback",()=>axios.get(base+"/malformed",{responseType:"json",transitional:{silentJSONParsing:true,forcedJSONParsing:true}}));
  await new Promise(resolve=>setTimeout(resolve,150));
  await new Promise((resolve,reject)=>server.close(err=>err?reject(err):resolve()));
  console.log(JSON.stringify({source:"Axios Node HTTP adapter",sourceCommit:process.env.AXIOS_SOURCE_COMMIT,scenarios},null,2));
}
main().catch(error=>{console.error(error);process.exit(1)});
