import os,sqlite3,tempfile
def create(path):
 c=sqlite3.connect(path);c.execute("CREATE TABLE post(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL)");c.commit();return c
def rows(path):
 c=sqlite3.connect(path);r=[{"id":x[0],"title":x[1]} for x in c.execute("SELECT id,title FROM post ORDER BY id")];c.close();return r
def capture(mutation=None):
 m=mutation or {};out=[]
 with tempfile.TemporaryDirectory() as d:
  p=os.path.join(d,"commit.sqlite");c=create(p)
  if not m.get("lose_commit"):c.execute("INSERT INTO post(title) VALUES(?)",("committed",));c.commit()
  c.close();r=rows(p);out.append({"label":"commit-survives-reopen","rows":r,"count":len(r)})
  p=os.path.join(d,"rollback.sqlite");c=create(p);error=False
  try:
   c.execute("BEGIN");c.execute("INSERT INTO post(title) VALUES(?)",("transient",))
   c.execute("INSERT INTO post(title) VALUES(?)",(None,))
   c.commit()
  except sqlite3.IntegrityError:
   error=True
   if m.get("leak_rollback"):c.commit()
   else:c.rollback()
  c.close();r=rows(p);out.append({"label":"rollback-survives-reopen","errorPropagated":error,"rows":r,"count":len(r)})
  p=os.path.join(d,"update.sqlite");c=create(p);c.execute("INSERT INTO post(title) VALUES(?)",("before",));c.commit()
  if not m.get("lose_update"):c.execute("UPDATE post SET title=? WHERE id=1",("after",));c.commit()
  c.close();r=rows(p);out.append({"label":"update-survives-reopen","rows":r,"count":len(r)})
  p=os.path.join(d,"constraint.sqlite");c=create(p);error_category="none"
  try:
   c.execute("BEGIN");c.execute("INSERT INTO post(title) VALUES(?)",("must-rollback",))
   c.execute("INSERT INTO post(title) VALUES(?)",(None,));c.commit()
  except sqlite3.IntegrityError:
   error_category="integrity-constraint"
   if m.get("partial_constraint_commit"):c.commit()
   else:c.rollback()
  c.close();r=rows(p);out.append({"label":"constraint-failure-atomicity","errorCategory":error_category,"rows":r,"count":len(r)})
 return {"implementation":"Independent Python 3.12 sqlite3 file-backed model","scenarios":out}
if __name__=="__main__":
 import json;print(json.dumps(capture(),indent=2))
