import json
import sqlite3
from datetime import datetime, timezone


def transaction(connection, callback, rollback_on_error=True):
    connection.execute("BEGIN")
    try:
        result = callback(connection)
        connection.commit()
        return result
    except Exception:
        if rollback_on_error:
            connection.rollback()
        else:
            # Deliberate incorrect variant used by mutation tests.
            connection.commit()
        raise


def run_commit():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        "CREATE TABLE post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL);"
        "CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);"
    )

    def callback(tx):
        post = tx.execute("INSERT INTO post(title) VALUES (?)", ("Post #1",))
        category = tx.execute("INSERT INTO category(name) VALUES (?)", ("Category #1",))
        return {"postId": post.lastrowid, "categoryId": category.lastrowid}

    result = transaction(connection, callback)
    posts = [dict(row) for row in connection.execute("SELECT id, title FROM post ORDER BY id")]
    categories = [dict(row) for row in connection.execute("SELECT id, name FROM category ORDER BY id")]
    connection.close()
    return {
        "label": "commit-success",
        "terminal": "committed",
        "callbackResult": result,
        "postRows": posts,
        "categoryRows": categories,
        "postCount": len(posts),
        "categoryCount": len(categories),
    }


def run_rollback(rollback_on_error=True):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        "CREATE TABLE post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL);"
        "CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);"
    )
    reads_visible_before_failure = False

    def callback(tx):
        post = tx.execute("INSERT INTO post(title) VALUES (?)", ("Post #1",))
        category = tx.execute("INSERT INTO category(name) VALUES (?)", ("Category #1",))
        loaded_post = tx.execute("SELECT id FROM post WHERE title = ?", ("Post #1",)).fetchone()
        loaded_category = tx.execute("SELECT id FROM category WHERE name = ?", ("Category #1",)).fetchone()
        nonlocal reads_visible_before_failure
        reads_visible_before_failure = bool(loaded_post and loaded_category)
        tx.execute("INSERT INTO post(title) VALUES (?)", (None,))
        return {"postId": post.lastrowid, "categoryId": category.lastrowid}

    error = None
    try:
        transaction(connection, callback, rollback_on_error=rollback_on_error)
    except sqlite3.IntegrityError as caught:
        error = caught

    posts = [dict(row) for row in connection.execute("SELECT id, title FROM post ORDER BY id")]
    categories = [dict(row) for row in connection.execute("SELECT id, name FROM category ORDER BY id")]
    connection.close()
    return {
        "label": "rollback-on-invalid-post",
        "terminal": "rolled-back" if rollback_on_error else "incorrectly-committed",
        "errorPropagated": error is not None,
        "errorCategory": "integrity-constraint" if error else "none",
        "readsVisibleBeforeFailure": reads_visible_before_failure,
        "postRowsAfter": posts,
        "categoryRowsAfter": categories,
        "postCountAfter": len(posts),
        "categoryCountAfter": len(categories),
    }


def capture(rollback_on_error=True):
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "completedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "implementation": "Independent Python 3.12 sqlite3 transaction model",
        "driver": "sqlite3",
        "scenarios": [run_commit(), run_rollback(rollback_on_error)],
    }


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
