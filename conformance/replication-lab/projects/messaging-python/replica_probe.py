import json
from datetime import datetime, timezone


def duplicate_case(suppress_duplicate=True, preserve_first_payload=True, complete_after_processing=True, event_order_mutation=False):
    queue = []
    seen = {}
    events = []
    processed = []

    def add(job_id, payload):
        if job_id in seen and suppress_duplicate:
            return seen[job_id]
        if job_id not in seen:
            seen[job_id] = job_id
        queue.append({"id": job_id, "payload": payload, "fail": False})
        events.append("waiting")
        return job_id

    first_id = add("stable-message-id", "first")
    second_id = add("stable-message-id", "second")
    if suppress_duplicate and not preserve_first_payload:
        queue[0]["payload"] = "second"
    stored_payload = queue[0]["payload"]
    queued_count = len(queue)
    while queue:
        job = queue.pop(0)
        events.append("active")
        processed.append(job["payload"])
        if complete_after_processing:
            events.append("completed")
    if event_order_mutation and len(events) >= 3:
        events[1], events[2] = events[2], events[1]
    terminal_state = "completed" if complete_after_processing else "active"
    return {
        "label": "duplicate-id-suppression",
        "setup": {
            "firstId": first_id,
            "secondId": second_id,
            "storedPayload": stored_payload,
            "storedState": "waiting",
            "queuedCount": queued_count,
        },
        "processed": processed,
        "terminal": {"state": terminal_state, "id": "stable-message-id", "result": "acknowledged" if complete_after_processing else None},
        "eventNames": events,
        "counts": {
            "waiting": 0,
            "active": 0 if complete_after_processing else 1,
            "completed": len(processed) if complete_after_processing else 0,
            "failed": 0,
        },
    }


def failure_case(failure_state="failed"):
    job = {"id": "failure-message-id", "payload": "failure-case", "fail": True}
    events = ["waiting", "active", failure_state]
    terminal = {"state": failure_state, "id": job["id"], "error": "consumer-failed" if failure_state == "failed" else None}
    return {
        "label": "consumer-failure",
        "setup": {"firstId": job["id"], "storedState": "waiting", "queuedCount": 1},
        "processed": [job["payload"]],
        "terminal": terminal,
        "eventNames": events,
        "counts": {
            "waiting": 0,
            "active": 0,
            "completed": 1 if failure_state == "completed" else 0,
            "failed": 1 if failure_state == "failed" else 0,
        },
    }


def capture(suppress_duplicate=True, preserve_first_payload=True, complete_after_processing=True, event_order_mutation=False, failure_state="failed"):
    return {
        "implementation": "Independent Python in-memory message queue model",
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scenarios": [
            duplicate_case(suppress_duplicate, preserve_first_payload, complete_after_processing, event_order_mutation),
            failure_case(failure_state),
        ],
    }


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
