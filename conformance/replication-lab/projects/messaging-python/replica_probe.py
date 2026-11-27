import json
from datetime import datetime, timezone


def duplicate_case():
    queue = []
    seen = {}
    events = []
    processed = []

    def add(job_id, payload):
        if job_id in seen:
            return seen[job_id]
        seen[job_id] = job_id
        queue.append({"id": job_id, "payload": payload, "fail": False})
        events.append("waiting")
        return job_id

    first_id = add("stable-message-id", "first")
    second_id = add("stable-message-id", "second")
    stored_payload = queue[0]["payload"]
    job = queue.pop(0)
    events.append("active")
    processed.append(job["payload"])
    events.append("completed")
    return {
        "label": "duplicate-id-suppression",
        "setup": {"firstId": first_id, "secondId": second_id, "storedPayload": stored_payload, "storedState": "waiting"},
        "processed": processed,
        "terminal": {"state": "completed", "id": job["id"], "result": "acknowledged"},
        "eventNames": ["active", "completed"],
        "counts": {"waiting": 0, "active": 0, "completed": 1, "failed": 0},
    }


def failure_case():
    job = {"id": "failure-message-id", "payload": "failure-case", "fail": True}
    events = ["waiting", "active"]
    error = "consumer-failed"
    events.append("failed")
    return {
        "label": "consumer-failure",
        "setup": {"firstId": job["id"], "storedState": "waiting"},
        "processed": [job["payload"]],
        "terminal": {"state": "failed", "id": job["id"], "error": error},
        "eventNames": ["active", "failed"],
        "counts": {"waiting": 0, "active": 0, "completed": 0, "failed": 1},
    }


if __name__ == "__main__":
    print(json.dumps({
        "implementation": "Independent Python in-memory message queue model",
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scenarios": [duplicate_case(), failure_case()],
    }, indent=2))
