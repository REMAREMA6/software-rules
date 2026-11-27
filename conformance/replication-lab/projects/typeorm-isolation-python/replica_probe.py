import json,os

CFG=dict(host=os.getenv("PGHOST","127.0.0.1"),port=int(os.getenv("PGPORT","5432")),
 user=os.getenv("PGUSER","postgres"),password=os.getenv("PGPASSWORD","postgres"),dbname=os.getenv("PGDATABASE","postgres"))
def connect():
 import psycopg
 from psycopg.rows import dict_row
 return psycopg.connect(**CFG,row_factory=dict_row)

def model_capture(mutation=None):
 m=mutation or {}
 read_committed={"first":100,"second":100 if m.get("read_committed_snapshot") else 150}
 repeatable={"first":150,"second":200 if m.get("repeatable_read_uses_read_committed") else 150}
 commit_b="committed" if m.get("serializable_allows_write_skew") else "aborted"
 error_code=None if commit_b=="committed" or m.get("serializable_aborts_without_error") else "40001"
 remaining=0 if commit_b=="committed" or m.get("wrong_invariant_count") else 1
 if m.get("wrong_error_code"):error_code="23505"
 return {"implementation":"Independent Python 3.12 transaction-isolation semantic model","database":"PostgreSQL",
  "scenarios":[
   {"label":"read-committed-nonrepeatable-read","output":read_committed},
   {"label":"repeatable-read-stable-snapshot","output":repeatable},
   {"label":"serializable-write-skew-prevention","output":{"countA":2,"countB":2,"commitA":"committed",
    "commitB":commit_b,"errorCode":error_code,"remainingOnCall":remaining}}
  ]}

def capture():
 with connect() as admin:
  admin.execute("DROP TABLE IF EXISTS software_rules_doctors")
  admin.execute("DROP TABLE IF EXISTS software_rules_accounts")
  admin.execute("CREATE TABLE software_rules_accounts (id INTEGER PRIMARY KEY,balance INTEGER NOT NULL)")
  admin.execute("INSERT INTO software_rules_accounts VALUES (1,100)")
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  first=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  b.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  b.execute("UPDATE software_rules_accounts SET balance=150 WHERE id=1");b.commit()
  second=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"];a.commit()
 finally:a.close();b.close()
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
  first_rr=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"]
  b.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
  b.execute("UPDATE software_rules_accounts SET balance=200 WHERE id=1");b.commit()
  second_rr=a.execute("SELECT balance FROM software_rules_accounts WHERE id=1").fetchone()["balance"];a.commit()
 finally:a.close();b.close()
 with connect() as admin:
  admin.execute("CREATE TABLE software_rules_doctors (id INTEGER PRIMARY KEY,on_call BOOLEAN NOT NULL)")
  admin.execute("INSERT INTO software_rules_doctors VALUES (1,TRUE),(2,TRUE)")
 a=connect();b=connect()
 try:
  a.execute("BEGIN ISOLATION LEVEL SERIALIZABLE");b.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
  count_a=a.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
  count_b=b.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
  a.execute("UPDATE software_rules_doctors SET on_call=FALSE WHERE id=1")
  b.execute("UPDATE software_rules_doctors SET on_call=FALSE WHERE id=2")
  a.commit();commit_b="committed";error_code=None
  try:b.commit()
  except Exception as e:
   commit_b="aborted";error_code=getattr(e,"sqlstate",None);b.rollback()
  with connect() as admin:remaining=admin.execute("SELECT COUNT(*) AS n FROM software_rules_doctors WHERE on_call=TRUE").fetchone()["n"]
 finally:a.close();b.close()
 return {"implementation":"Independent Python 3.12 psycopg/PostgreSQL runtime","database":"PostgreSQL",
  "scenarios":[
   {"label":"read-committed-nonrepeatable-read","output":{"first":first,"second":second}},
   {"label":"repeatable-read-stable-snapshot","output":{"first":first_rr,"second":second_rr}},
   {"label":"serializable-write-skew-prevention","output":{"countA":count_a,"countB":count_b,"commitA":"committed",
    "commitB":commit_b,"errorCode":error_code,"remainingOnCall":remaining}}
  ]}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
