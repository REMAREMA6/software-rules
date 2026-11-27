import json, sys

PATHS=["/Report","/report","/Report/","/report/"]
def match(path,case_sensitive,strict):
    candidate=path
    route="/Report"
    if not strict:
        candidate=candidate.rstrip("/") or "/"
        route=route.rstrip("/") or "/"
    if not case_sensitive:
        return candidate.casefold()==route.casefold()
    return candidate==route

def run(label,case_sensitive,strict):
    return {"label":label,"config":{"caseSensitive":case_sensitive,"strict":strict,"activation":"before-first-request"},
      "decisions":[{"path":p,"status":200 if match(p,case_sensitive,strict) else 404} for p in PATHS]}

scenarios=[run("defaults",False,False),run("case-sensitive",True,False),
 run("strict",False,True),run("case-sensitive-and-strict",True,True)]
# Express lazily constructs its router on the first request. Later setting changes do not mutate it.
frozen_case_sensitive=False
late=[{"path":"/Report","status":200 if match("/Report",frozen_case_sensitive,False) else 404}]
changed_case_sensitive=True
late.append({"path":"/report","status":200 if match("/report",frozen_case_sensitive,False) else 404})
scenarios.append({"label":"late-case-sensitive-change","config":{"caseSensitive":False,"strict":False,"settingAfterInitialization":True,"activation":"after-router-initialization"},"decisions":late})
print(json.dumps({"implementation":"Independent Python 3.12 configuration model","scenarios":scenarios},indent=2))
