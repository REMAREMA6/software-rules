import base64,hashlib,hmac,json,secrets,urllib.parse
from http.cookies import SimpleCookie

SECRET=b"software-rules-session-test-secret"
def sign(sid):
 sig=base64.b64encode(hmac.new(SECRET,sid.encode(),hashlib.sha256).digest()).decode().rstrip("=")
 return "connect.sid="+urllib.parse.quote("s:"+sid+"."+sig,safe="~()*!.'-")
def verify(cookie):
 if not cookie:return None
 jar=SimpleCookie(); jar.load(cookie)
 morsel=jar.get("connect.sid")
 if not morsel:return None
 value=urllib.parse.unquote(morsel.value)
 if not value.startswith("s:") or "." not in value[2:]:return None
 sid,sig=value[2:].rsplit(".",1)
 expected=base64.b64encode(hmac.new(SECRET,sid.encode(),hashlib.sha256).digest()).decode().rstrip("=")
 return sid if hmac.compare_digest(sig,expected) else None
def cookie_info(cookie,cleared=False):
 if not cookie:return {"name":None,"present":False,"cleared":False,"attributes":[]}
 return {"name":"connect.sid","present":not cleared,"cleared":cleared,"attributes":["expires","httponly","path","samesite"] if cleared else ["httponly","path","samesite"]}
def capture(mutation=None):
 m=mutation or {}; store={}; outcomes=[]
 def emit(label,data,set_cookie=None,cleared=False):
  outcomes.append({"label":label,"data":data,"cookie":cookie_info(set_cookie,cleared)})
 def load(cookie_value):
  sid=verify(cookie_value)
  return sid if sid in store else None
 # saveUninitialized=false: no stored session or cookie until data changes.
 emit("uninitialized-session",{"sessionExists":True,"value":None})
 sid=secrets.token_urlsafe(24); store[sid]={"value":"alpha"}; cookie=sign(sid)
 emit("create-session",{"value":"alpha"},cookie)
 loaded=load(cookie)
 emit("read-session",{"value":store[loaded]["value"] if loaded else None})
 # Regeneration destroys the prior identifier and persists a new session.
 old_cookie=cookie; old=load(old_cookie)
 if old and not m.get("keep_old_id_on_regenerate"): store.pop(old,None)
 sid2=secrets.token_urlsafe(24); store[sid2]={"value":"beta"}; cookie2=sign(sid2)
 emit("regenerate-session",{"value":"beta"},cookie2)
 old_loaded=load(old_cookie)
 emit("old-id-rejected",{"value":store[old_loaded]["value"] if old_loaded else None})
 new_loaded=load(cookie2)
 emit("new-id-restored",{"value":store[new_loaded]["value"] if new_loaded else None})
 last=cookie2[-1]; tampered=cookie2[:-1]+("x" if last!="x" else "y")
 tampered_loaded=load(tampered)
 if m.get("accept_tampered_cookie"): tampered_loaded=sid2
 emit("tampered-cookie-rejected",{"value":store[tampered_loaded]["value"] if tampered_loaded in store else None})
 destroy_loaded=load(cookie2)
 if destroy_loaded and not m.get("retain_destroyed_session"): store.pop(destroy_loaded,None)
 emit("destroy-session",{"destroyed":True},cleared=True)
 after_destroy=load(cookie2)
 emit("destroyed-id-rejected",{"value":store[after_destroy]["value"] if after_destroy else None})
 if m.get("emit_cookie_for_uninitialized"):
  outcomes[0]["cookie"]={"name":"connect.sid","present":True,"cleared":False,"attributes":["httponly","path","samesite"]}
 if m.get("omit_cookie_clear"): outcomes[7]["cookie"]={"name":None,"present":False,"cleared":False,"attributes":[]}
 return {"implementation":"Independent Python 3.12 session/cookie model","scenarios":outcomes}

if __name__=="__main__": print(json.dumps(capture(),indent=2))
