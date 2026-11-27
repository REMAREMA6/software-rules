import json, sys

def decide_domain(subject, domain, resource, action, policy_extra=False, ignore_domain=False):
    policies=[("admin","domain1","data1","read"),("admin","domain1","data1","write"),
              ("admin","domain2","data2","read"),("admin","domain2","data2","write")]
    if policy_extra: policies.append(("admin","domain1","data2","read"))
    roles=[("alice","admin","domain1"),("bob","admin","domain2")]
    for psub,pdom,pobj,pact in policies:
        role_match=any(u==subject and role==psub and (ignore_domain or dom==domain) for u,role,dom in roles)
        domain_match=ignore_domain or domain==pdom
        if (subject==psub or role_match) and domain_match and resource==pobj and action==pact:
            return "permit"
    return "deny"

def decide_abac(subject, owner, action, ignore_owner=False):
    return "permit" if ignore_owner or subject==owner else "deny"

def decide_deny(subject, resource, action, ignore_deny=False):
    allows=[("alice","data1","read"),("bob","data2","write"),("data2_admin","data2","read"),("data2_admin","data2","write")]
    denies=[("alice","data2","write")]
    roles=[("alice","data2_admin")]
    allowed=any((s==subject or (subject, s) in roles) and o==resource and a==action for s,o,a in allows)
    denied=not ignore_deny and any(s==subject and o==resource and a==action for s,o,a in denies)
    return "permit" if allowed and not denied else "deny"

def capture(mutations=None):
    m=mutations or {}; scenarios=[]
    domain=[
      ("alice-domain1-data1-read","alice","domain1","data1","read"),
      ("alice-domain1-data1-write","alice","domain1","data1","write"),
      ("alice-domain2-data2-read","alice","domain2","data2","read"),
      ("bob-domain2-data2-write","bob","domain2","data2","write"),
      ("bob-domain1-data1-read","bob","domain1","data1","read"),
      ("alice-domain1-data2-read","alice","domain1","data2","read"),
      ("bob-domain2-data2-delete","bob","domain2","data2","delete")]
    for label,sub,dom,obj,act in domain:
        req={"subject":sub,"domain":dom,"resource":obj,"action":act}
        scenarios.append({"label":label,"modelClass":"domain-rbac","request":req,
          "decision":decide_domain(sub,dom,obj,act,ignore_domain=m.get("ignore_domain",False))})
    req={"subject":"alice","domain":"domain1","resource":"data2","action":"read"}
    scenarios.append({"label":"domain-policy-added","modelClass":"policy-mutation","request":req,
      "decision":decide_domain("alice","domain1","data2","read",policy_extra=not m.get("ignore_policy_mutation",False))})
    scenarios.append({"label":"domain-policy-removed","modelClass":"policy-mutation","request":req,
      "decision":decide_domain("alice","domain1","data2","read")})
    abac=[("abac-owner-read","alice","alice","read"),("abac-nonowner-read","alice","bob","read"),
      ("abac-owner-delete","alice","alice","delete"),("abac-owner-write","bob","bob","write"),
      ("abac-nonowner-write","bob","alice","write")]
    for label,sub,owner,act in abac:
        req={"subject":sub,"resource":"record","action":act,"owner":owner}
        scenarios.append({"label":label,"modelClass":"abac-owner","request":req,
          "decision":decide_abac(sub,owner,act,ignore_owner=m.get("ignore_owner",False))})
    deny=[("deny-alice-data1-read","alice","data1","read"),("deny-bob-data2-write","bob","data2","write"),
      ("deny-alice-data2-write","alice","data2","write"),("deny-alice-data2-read","alice","data2","read"),
      ("deny-bob-data1-read","bob","data1","read")]
    for label,sub,obj,act in deny:
        req={"subject":sub,"resource":obj,"action":act}
        scenarios.append({"label":label,"modelClass":"deny-override","request":req,
          "decision":decide_deny(sub,obj,act,ignore_deny=m.get("ignore_deny",False))})
    return {"implementation":"Independent Python 3.12 authorization model","scenarios":scenarios}

if __name__=="__main__": print(json.dumps(capture(),indent=2))
