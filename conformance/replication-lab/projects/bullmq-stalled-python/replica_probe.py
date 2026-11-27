def capture(mutation=None):
 m=mutation or {}
 def run(label,limit):
  stalled=0;attempts_started=1;attempts_made=0;processed=[]
  stalled+=0 if m.get("omit_stalled_counter") else 1
  if label=="recover-once":
   if m.get("do_not_requeue"):
    state="failed";reason="job stalled more than allowable limit";attempts_started=2;attempts_made=1;counts={"waiting":0,"active":0,"completed":0,"failed":1};processed=[]
   else:
    attempts_started=2
    attempts_made=0 if m.get("omit_attempts_on_requeue") else 1
    state="completed";reason=None;processed=[label];counts={"waiting":0,"active":0,"completed":1,"failed":0}
  else:
   if m.get("ignore_stalled_limit"):
    state="completed";reason=None;attempts_started=2;attempts_made=0;processed=[label];counts={"waiting":0,"active":0,"completed":1,"failed":0}
   else:
    state="failed";reason="job stalled more than allowable limit";attempts_started=2;attempts_made=1;counts={"waiting":0,"active":0,"completed":0,"failed":1}
  return {"label":label,"initialActiveId":"recovery-job",
   "terminal":{"state":state,"attemptsStarted":attempts_started,"attemptsMade":attempts_made,"stalledCounter":stalled,
    **({"result":"recovered"} if state=="completed" else {"reason":reason})},
   "processed":processed,"eventCounts":{"stalled":1,"completed":1 if state=="completed" else 0,"failed":1 if state=="failed" else 0},
   "counts":counts}
 return {"implementation":"Independent Python 3.12 stalled-job state-machine model",
  "scenarios":[run("recover-once",1),run("fail-at-zero-stalled-limit",0)]}
if __name__=="__main__":
 import json;print(json.dumps(capture(),indent=2))
