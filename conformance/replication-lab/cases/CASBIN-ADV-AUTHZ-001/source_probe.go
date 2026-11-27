package main

import (
  "crypto/sha256"
  "encoding/hex"
  "encoding/json"
  "fmt"
  "os"
  "path/filepath"
  "time"

  "github.com/casbin/casbin/v3"
)

type Request struct {
  Subject string `json:"subject"`
  Domain string `json:"domain,omitempty"`
  Resource string `json:"resource"`
  Action string `json:"action"`
  Owner string `json:"owner,omitempty"`
}
type Scenario struct {
  Label string `json:"label"`
  ModelClass string `json:"modelClass"`
  Request Request `json:"request"`
  Decision string `json:"decision"`
}
type Resource struct { Owner string }

func digest(path string) string {
  b,err:=os.ReadFile(path); if err!=nil { panic(err) }
  h:=sha256.Sum256(b); return hex.EncodeToString(h[:])
}
func decision(e *casbin.Enforcer,args ...interface{}) string {
  ok,err:=e.Enforce(args...); if err!=nil { panic(err) }
  if ok { return "permit" }; return "deny"
}
func main() {
  root:=os.Getenv("CASBIN_SOURCE_ROOT"); if root=="" { panic("CASBIN_SOURCE_ROOT required") }
  examples:=filepath.Join(root,"examples")
  var out []Scenario
  files:=map[string]string{}
  add:=func(label,class string,req Request,d string) { out=append(out,Scenario{label,class,req,d}) }

  domainModel:=filepath.Join(examples,"rbac_with_domains_model.conf")
  domainPolicy:=filepath.Join(examples,"rbac_with_domains_policy.csv")
  de,err:=casbin.NewEnforcer(domainModel,domainPolicy); if err!=nil { panic(err) }
  files["domainModel"]=digest(domainModel); files["domainPolicy"]=digest(domainPolicy)
  domainRequests:=[]struct{label string; req Request}{
    {"alice-domain1-data1-read",Request{"alice","domain1","data1","read",""}},
    {"alice-domain1-data1-write",Request{"alice","domain1","data1","write",""}},
    {"alice-domain2-data2-read",Request{"alice","domain2","data2","read",""}},
    {"bob-domain2-data2-write",Request{"bob","domain2","data2","write",""}},
    {"bob-domain1-data1-read",Request{"bob","domain1","data1","read",""}},
    {"alice-domain1-data2-read",Request{"alice","domain1","data2","read",""}},
    {"bob-domain2-data2-delete",Request{"bob","domain2","data2","delete",""}},
  }
  for _,x:=range domainRequests { add(x.label,"domain-rbac",x.req,decision(de,x.req.Subject,x.req.Domain,x.req.Resource,x.req.Action)) }
  mutationReq:=Request{"alice","domain1","data2","read",""}
  added,err:=de.AddPolicy("admin","domain1","data2","read"); if err!=nil || !added { panic(fmt.Sprintf("AddPolicy failed: %v %v",added,err)) }
  add("domain-policy-added","policy-mutation",mutationReq,decision(de,mutationReq.Subject,mutationReq.Domain,mutationReq.Resource,mutationReq.Action))
  removed,err:=de.RemovePolicy("admin","domain1","data2","read"); if err!=nil || !removed { panic(fmt.Sprintf("RemovePolicy failed: %v %v",removed,err)) }
  add("domain-policy-removed","policy-mutation",mutationReq,decision(de,mutationReq.Subject,mutationReq.Domain,mutationReq.Resource,mutationReq.Action))

  abacModel:=filepath.Join(examples,"abac_model.conf")
  ae,err:=casbin.NewEnforcer(abacModel); if err!=nil { panic(err) }
  files["abacModel"]=digest(abacModel)
  abacRequests:=[]struct{label,subject,owner,action string}{
    {"abac-owner-read","alice","alice","read"},
    {"abac-nonowner-read","alice","bob","read"},
    {"abac-owner-delete","alice","alice","delete"},
    {"abac-owner-write","bob","bob","write"},
    {"abac-nonowner-write","bob","alice","write"},
  }
  for _,x:=range abacRequests {
    req:=Request{Subject:x.subject,Resource:"record",Action:x.action,Owner:x.owner}
    add(x.label,"abac-owner",req,decision(ae,x.subject,Resource{Owner:x.owner},x.action))
  }

  denyModel:=filepath.Join(examples,"rbac_with_deny_model.conf")
  denyPolicy:=filepath.Join(examples,"rbac_with_deny_policy.csv")
  ne,err:=casbin.NewEnforcer(denyModel,denyPolicy); if err!=nil { panic(err) }
  files["denyModel"]=digest(denyModel); files["denyPolicy"]=digest(denyPolicy)
  denyRequests:=[]struct{label,subject,resource,action string}{
    {"deny-alice-data1-read","alice","data1","read"},
    {"deny-bob-data2-write","bob","data2","write"},
    {"deny-alice-data2-write","alice","data2","write"},
    {"deny-alice-data2-read","alice","data2","read"},
    {"deny-bob-data1-read","bob","data1","read"},
  }
  for _,x:=range denyRequests {
    req:=Request{Subject:x.subject,Resource:x.resource,Action:x.action}
    add(x.label,"deny-override",req,decision(ne,x.subject,x.resource,x.action))
  }

  result:=map[string]any{"capturedAt":time.Now().UTC().Format(time.RFC3339Nano),
    "source":"Apache Casbin pinned Go runtime","sourceCommit":os.Getenv("CASBIN_SOURCE_COMMIT"),
    "sourceFiles":files,"scenarios":out}
  b,err:=json.MarshalIndent(result,"","  "); if err!=nil { panic(err) }; fmt.Println(string(b))
}
