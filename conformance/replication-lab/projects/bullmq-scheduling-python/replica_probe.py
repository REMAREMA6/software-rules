import json
def capture(mutation=None):
 m=mutation or {}
 events=[{"event":"active","jobId":"scheduled-job"},{"event":"completed","jobId":"scheduled-job"}]
 final_state="completed";processed=["scheduled"];result="processed";scheduled_completed=1
 if m.get("ignore_change_delay"):
  events=[];final_state="delayed";processed=[];result=None;scheduled_completed=0
 if m.get("complete_before_active"):events=list(reversed(events))
 if m.get("skip_active_event"):events=[e for e in events if e["event"]!="active"]
 scheduled={
  "label":"reschedule-delayed-job","initialState":"delayed",
  "afterChangeDelay":"waiting" if m.get("change_delay_sets_waiting") else "delayed",
  "events":events,"finalState":final_state,"processed":processed,"result":result,
  "counts":{"delayed":1 if not scheduled_completed else 0,"waiting":0,"active":0,
   "completed":scheduled_completed,"failed":0}
 }
 cancel_exists=bool(m.get("ignore_remove"))
 cancel_processed=bool(m.get("process_cancelled_job"))
 cancelled={
  "label":"cancel-delayed-job","initialState":"delayed","removed":not cancel_exists,
  "jobExists":cancel_exists,"processed":cancel_processed,
  "finalState":"delayed" if cancel_exists else "missing",
  "counts":{"delayed":1 if cancel_exists else 0,"waiting":0,"active":0,
   "completed":scheduled_completed+(1 if cancel_processed else 0),"failed":0}
 }
 return {"implementation":"Independent Python 3.12 delayed-job state machine","scenarios":[scheduled,cancelled]}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
