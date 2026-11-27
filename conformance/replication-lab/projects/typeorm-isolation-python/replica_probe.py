import json,os,psycopg
from psycopg.rows import dict_row
CFG=dict(host=os.getenv("PGHOST","127.0.0.1"),port=int(os.getenv("PGPORT","5432")),
 user=os.getenv("PGUSER","postgres"),password=os.getenv("PGPASSWORD","postgres"),dbname=os.getenv("PGDATABASE","postgres"))
def connect():return psycopg.connect(**CFG,row_factory=dict_row)
def capture(mutation=None):
 m=mutation or {}
 with connect() as admin:
  admin.execute("DROP TABLE IF EXISTS software_rules_doctors")
  admin.execute("DROP TABLE IF EXISTS software_rules_accounts")
  admin.execute("CREATE TABLE software_rules_accounts (id INTEGER PRIMARY KEY,balance INTEGER NOT NULL)")
  admin.execute("INSERT INTO software_rules_accounts VALUES (1,100)")
 # READ COMMITTED: second statement sees the concurrent committed update.
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  first=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  b.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  b.execute("UPDATE software_rules_accounts SET balance=150 WHERE id=1");b.commit()
  second=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  a.commit()
 finally:a.close();b.close()
 # REPEATABLE READ: both reads use the same transaction snapshot.
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
  first_rr=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  b.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  b.execute("UPDATE software_rules_accounts SET balance=200 WHERE id=1");b.commit()
  second_rr=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  if m.get("repeatable_read_uses_read_committed"):second_rr=200
  a.commit()
 finally:a.close();b.close()
 with connect() as admin:
  admin.execute("CREATE TABLE software_rules_doctors (id INTEGER PRIMARY KEY,on_call BOOLEAN NOT NULL)")
  admin.execute("INSERT INTO software_rules_doctors VALUES (1,TRUE),(2,TRUE)")
 # Two serializable transactions both observe two on-call doctors, then update different rows.
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL SERIALIZABLE");b.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
  count_a=a.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
  count_b=b.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
  a.execute("UPDATE software_rules_doctors SET on_call=FALSE WHERE id=1")
  b.execute("UPDATE software_rules_doctors SET on_call=FALSE WHERE id=2")
  a.commit()
  commit_b="committed";error_code=None
  try:b.commit()
  except psycopg.Error as e:
   commit_b="aborted";error_code=e.sqlstate;b.rollback()
  if m.get("serializable_allows_write_skew"):
   with connect() as admin:admin.execute("UPDATE software_rules_doctors SET on_call=FALSE WHERE id=2")
  if m.get("wrong_error_code") and error_code:error_code="23505"
  with connect() as admin:
   remaining=admin.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
  if m.get("wrong_invariant_count"):remaining=0
 finally:a.close();b.close()
 return {"implementation":"Independent Python 3.12 psycopg/PostgreSQL transaction model","database":"PostgreSQL",
  "scenarios":[
   {"label":"read-committed-nonrepeatable-read","output":{"first":first,"second":second}},
   {"label":"repeatable-read-stable-snapshot","output":{"first":first_rr,"second":second_rr}},
   {"label":"serializable-write-skew-prevention","output":{"countA":count_a,"countB":count_b,"commitA":"committed",
    "commitB":commit_b,"errorCode":error_code,"remainingOnCall":remaining}}
  ]}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
