import json
import sqlite3
from datetime import datetime, timezone

def capture():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
        rollback_error = None
        rollback_callback_result = None
        try:
            connection.execute("BEGIN")
            connection.execute("INSERT INTO records(value) VALUES (?)", ("rolled-back",))
            inside = connection.execute("SELECT value FROM records ORDER BY id").fetchall()
            if len(inside) != 1 or inside[0]["value"] != "rolled-back":
                raise RuntimeError("transaction-read-your-write-failed")
            raise RuntimeError("forced-transaction-failure")
        except Exception as error:
            connection.execute("ROLLBACK")
            rollback_error = {"name": "Error", "message": str(error)}
        after_rollback = [dict(row) for row in connection.execute("SELECT id, value FROM records ORDER BY id")]
        connection.execute("BEGIN")
        connection.execute("INSERT INTO records(value) VALUES (?)", ("committed",))
        committed_return = "callback-result"
        connection.execute("COMMIT")
        after_commit = [dict(row) for row in connection.execute("SELECT id, value FROM records ORDER BY id")]
        return {
            "implementation": "Independent Python 3 sqlite3 transaction model",
            "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "scenarios": {
                "rollback": {"error": rollback_error, "callbackResult": rollback_callback_result, "rowsAfterRollback": after_rollback},
                "commit": {"callbackReturn": committed_return, "rowsAfterCommit": after_commit}
            }
        }
    finally:
        connection.close()

if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
