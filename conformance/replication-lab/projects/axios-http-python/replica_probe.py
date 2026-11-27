import json, socket, threading, time, urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
 def send(self,status,content_type,body,headers=None):
  data=body.encode()
  self.send_response(status); self.send_header("Content-Type",content_type)
  for k,v in (headers or {}).items(): self.send_header(k,v)
  self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
 def do_GET(self):
  if self.path=="/json": return self.send(200,"application/json",json.dumps({"ok":True,"n":7}))
  if self.path=="/text": return self.send(200,"text/plain","ready")
  if self.path=="/not-found": return self.send(404,"application/json",json.dumps({"error":"missing"}))
  if self.path=="/unavailable": return self.send(503,"text/plain","down")
  if self.path=="/redirect": self.send_response(302); self.send_header("Location","/json"); self.end_headers(); return
  if self.path.startswith("/query"): return self.send(200,"application/json",json.dumps({"url":self.path}))
  if self.path=="/slow": time.sleep(.12); return self.send(200,"application/json",json.dumps({"slow":True}))
  if self.path=="/malformed": return self.send(200,"application/json","{broken")
  return self.send(404,"text/plain","unknown")
 def do_POST(self):
  if self.path.startswith("/echo"):
   n=int(self.headers.get("Content-Length","0")); body=self.rfile.read(n).decode()
   return self.send(200,"application/json",json.dumps({"body":body,"xTrace":self.headers.get("X-Trace")}))
  return self.send(404,"text/plain","unknown")
 def log_message(self,*args): pass

def parse_body(data,content_type):
 text=data.decode()
 if "application/json" in (content_type or ""):
  try:return json.loads(text)
  except ValueError:return text
 return text

def request(base,path,method="GET",body=None,headers=None,timeout=1):
 data=None if body is None else json.dumps(body,separators=(",",":")).encode()
 hdrs=dict(headers or {})
 if data is not None: hdrs.setdefault("Content-Type","application/json")
 req=urllib.request.Request(base+path,data=data,headers=hdrs,method=method)
 try:
  with urllib.request.urlopen(req,timeout=timeout) as response:
   return {"kind":"response","status":response.status,"data":parse_body(response.read(),response.headers.get("Content-Type"))}
 except urllib.error.HTTPError as e:
  return {"kind":"http-error","status":e.code,"data":parse_body(e.read(),e.headers.get("Content-Type"))}
 except (socket.timeout,TimeoutError):
  return {"kind":"timeout"}
 except urllib.error.URLError as e:
  if isinstance(e.reason,(socket.timeout,TimeoutError)): return {"kind":"timeout"}
  return {"kind":"network-error","code":type(e.reason).__name__}

def capture(mutation=None):
 m=mutation or {}
 server=ThreadingHTTPServer(("127.0.0.1",0),Handler); thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
 base=f"http://127.0.0.1:{server.server_port}"
 scenarios=[]
 def add(label,path,**kwargs):
  outcome=request(base,path,**kwargs)
  if m.get("treat_http_errors_as_success") and outcome["kind"]=="http-error": outcome["kind"]="response"
  if m.get("ignore_timeout") and label=="request-timeout": outcome={"kind":"response","status":200,"data":{"slow":True}}
  if m.get("strict_malformed_json") and label=="malformed-json-silent-fallback": outcome={"kind":"parse-error"}
  if m.get("drop_custom_header") and label=="post-json-custom-header": outcome["data"]["xTrace"]=None
  if m.get("disable_redirect") and label=="redirect-follow": outcome={"kind":"response","status":302,"data":""}
  if m.get("query_percent20") and label=="query-serialization": outcome["data"]["url"]=outcome["data"]["url"].replace("+","%20")
  scenarios.append({"label":label,"outcome":outcome})
 add("json-response","/json")
 add("text-response","/text")
 add("http-404","/not-found")
 add("http-503","/unavailable")
 add("redirect-follow","/redirect")
 add("post-json-custom-header","/echo",method="POST",body={"hello":"world"},headers={"X-Trace":"123"})
 query=urllib.parse.urlencode({"q":"a b","page":2})
 add("query-serialization","/query?"+query)
 add("request-timeout","/slow",timeout=.02)
 add("malformed-json-silent-fallback","/malformed")
 time.sleep(.15); server.shutdown(); server.server_close(); thread.join()
 return {"implementation":"Independent Python 3.12 urllib HTTP client model","scenarios":scenarios}

if __name__=="__main__": print(json.dumps(capture(),indent=2))
