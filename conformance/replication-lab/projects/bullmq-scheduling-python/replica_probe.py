import json
def capture(mutation=None):
 m=mutation or {}
 events=[]
 initial="delayed"
 after="waiting" if m.get("change_delay_sets_waiting") else "delayed"
 if not m.get("ignore_change_delay"):
  events.append({"event":"active","jobId":"scheduled-job"})
  if m.get("complete_before_active"):
   events=[{"event":"completed","jobId":"scheduled-job"},{"event":"active","jobId":"scheduled-job"}]
  else:events.append({"event":"completed","jobId":"scheduled-job"})
 final="delayed" if m.get("ignore_change_delay") else "completed"
 processed=[] if m.get("ignore_change_delay") else ["scheduled"]
 if m.get("skip_active_event"):events=[e for e in events if e["event"]!="active"]
 cancel_exists=bool(m.get("ignore_remove"))
 cancel_processed=bool(m.get("process_cancelled_job"))
 if cancel_processed:processed.append("cancelled")
 return {"implementation":"Independent Python 3.12 delayed-job state machine","scenarios":[{
  "scheduled":{"initialState":initial,"afterChangeDelay":after,"events":events,"finalState":final,
   "processed":processed,"result":None if m.get("ignore_change_delay") else "processed"},
  "cancelled":{"initialState":"delayed","removed":not cancel_exists,"jobExists":cancel_exists,
   "processed":cancel_processed,"finalState":"delayed" if cancel_exists else "missing"},
  "counts":{"delayed":1 if cancel_exists or m.get("ignore_change_delay") else 0,
   "waiting":0,"active":0,"completed":0 if m.get("ignore_change_delay") else 1,
   "failed":0}
 }]}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
