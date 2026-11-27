const http=require("node:http");
const express=require(process.env.EXPRESS_SOURCE_ROOT+"/");
const session=require(process.env.SESSION_SOURCE_ROOT+"/");
const SECRET="software-rules-session-test-secret";

function cookieInfo(header) {
 if(!header) return {name:null,present:false,cleared:false,attributes:[]};
 const parts=header.split(";").map(x=>x.trim());
 const first=parts.shift()||"";
 const eq=first.indexOf("=");
 const name=eq<0?null:first.slice(0,eq);
 const value=eq<0?"":first.slice(eq+1);
 const attrs=parts.map(x=>x.toLowerCase()).sort();
 const cleared=attrs.some(x=>x.startsWith("expires=")&&new Date(x.slice(8)).getTime()<Date.now());
 return {name,present:value!=="",cleared,attributes:attrs.map(x=>x.split("=")[0])};
}
async function main() {
 const app=express();
 app.use(session({secret:SECRET,resave:false,saveUninitialized:false,
   cookie:{httpOnly:true,sameSite:"lax",secure:false}}));
 app.get("/empty",(req,res)=>res.json({sessionExists:Boolean(req.session),value:req.session.value??null}));
 app.get("/set",(req,res)=>{req.session.value="alpha";res.json({value:req.session.value});});
 app.get("/read",(req,res)=>res.json({value:req.session.value??null}));
 app.get("/regenerate",(req,res)=>req.session.regenerate(err=>{
   if(err)return res.status(500).json({error:"regenerate"});
   req.session.value="beta";res.json({value:req.session.value});
 }));
 app.get("/destroy",(req,res)=>req.session.destroy(err=>{
   if(err)return res.status(500).json({error:"destroy"});
   res.clearCookie("connect.sid",{path:"/",httpOnly:true,sameSite:"lax"});res.json({destroyed:true});
 }));
 const server=app.listen(0,"127.0.0.1");
 await new Promise(resolve=>server.once("listening",resolve));
 const base="http://127.0.0.1:"+server.address().port;
 async function request(path,cookie) {
   const headers={}; if(cookie)headers.Cookie=cookie;
   const response=await fetch(base+path,{headers});
   const data=await response.json();
   const setCookie=response.headers.get("set-cookie");
   return {data,setCookie,cookieInfo:cookieInfo(setCookie)};
 }
 const outcomes=[];
 let r=await request("/empty"); outcomes.push({label:"uninitialized-session",data:r.data,cookie:r.cookieInfo});
 r=await request("/set"); const firstCookie=r.setCookie?.split(";")[0]; outcomes.push({label:"create-session",data:r.data,cookie:r.cookieInfo});
 r=await request("/read",firstCookie); outcomes.push({label:"read-session",data:r.data,cookie:r.cookieInfo});
 r=await request("/regenerate",firstCookie); const secondCookie=r.setCookie?.split(";")[0]; outcomes.push({label:"regenerate-session",data:r.data,cookie:r.cookieInfo});
 r=await request("/read",firstCookie); outcomes.push({label:"old-id-rejected",data:r.data,cookie:r.cookieInfo});
 r=await request("/read",secondCookie); outcomes.push({label:"new-id-restored",data:r.data,cookie:r.cookieInfo});
 const tampered=secondCookie.replace(/.$/,"x");
 r=await request("/read",tampered); outcomes.push({label:"tampered-cookie-rejected",data:r.data,cookie:r.cookieInfo});
 r=await request("/destroy",secondCookie); outcomes.push({label:"destroy-session",data:r.data,cookie:r.cookieInfo});
 r=await request("/read",secondCookie); outcomes.push({label:"destroyed-id-rejected",data:r.data,cookie:r.cookieInfo});
 await new Promise((resolve,reject)=>server.close(err=>err?reject(err):resolve()));
 console.log(JSON.stringify({source:"express-session 1.19.0",sourceCommit:process.env.SESSION_SOURCE_COMMIT,scenarios:outcomes},null,2));
}
main().catch(e=>{console.error(e);process.exit(1)});
