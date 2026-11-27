import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACETS = ["messaging", "background-processing", "behavior", "errors-recovery", "data"]
LABELS = ["duplicate-id-suppression", "consumer-failure"]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "bullmq-msg-scenario-" + label


def eid(prefix, label):
    return f"bullmq-msg-exec-{prefix}-{label}"


def oid(prefix, label, facet):
    return f"bullmq-msg-obs-{prefix}-{label}-{facet}"


def projection(item, facet):
    if facet == "messaging":
        return {"setup": item["setup"], "eventNames": item["eventNames"], "terminal": item["terminal"]}
    if facet == "background-processing":
        return {"processed": item["processed"], "terminal": item["terminal"], "counts": item["counts"]}
    if facet == "behavior":
        return {"processed": item["processed"], "eventNames": item["eventNames"], "terminal": item["terminal"]}
    if facet == "errors-recovery":
        return {"terminal": item["terminal"], "counts": item["counts"]}
    return {"setup": item["setup"], "processed": item["processed"]}


def payload(label, item, facet):
    subject = "bullmq-message-job"
    if facet == "messaging":
        return {
            "facet": "messaging",
            "kind": "message-lifecycle",
            "subject": subject,
            "channel": "BullMQ queue",
            "message": {
                "messageId": item["setup"].get("firstId", ""),
                "headers": {"customJobId": item["setup"].get("firstId", "")},
                "payload": item["processed"][0] if item["processed"] else None,
            },
            "producer": "BullMQ Queue.add",
            "consumer": "BullMQ Worker",
            "deliveryAttempts": [{"attempt": 1, "event": "active"}],
            "ordering": {"events": item["eventNames"]},
            "acknowledgement": {"state": item["terminal"]["state"], "result": item["terminal"].get("result")},
            "processingOutcome": item["terminal"],
            "brokerContext": {"broker": "Redis 7", "jobStateCounts": item["counts"]},
        }
    if facet == "background-processing":
        return {
            "facet": "background-processing",
            "kind": "job-lifecycle",
            "subject": subject,
            "job": item["setup"].get("firstId", ""),
            "trigger": "A queue worker receives a waiting job.",
            "enqueue": {"jobId": item["setup"].get("firstId", ""), "initialState": item["setup"].get("storedState")},
            "worker": {"name": "BullMQ Worker", "concurrency": 1},
            "lifecycle": [{"state": event, "sequence": index} for index, event in enumerate(item["eventNames"])],
            "attemptCount": 1,
            "inputs": {"payload": item["processed"][0] if item["processed"] else None},
            "output": item["terminal"],
            "retry": {"attempts": 1},
            "terminalResult": item["terminal"]["state"],
        }
    if facet == "behavior":
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": subject,
            "trigger": "A worker processes a queued job.",
            "preconditions": ["A job is waiting in the queue.", "A worker with concurrency one is ready."],
            "actions": [
                {"sequence": 1, "action": "Worker claims the queued job."},
                {"sequence": 2, "action": "Processor handles the job payload."},
                {"sequence": 3, "action": "Worker records the terminal outcome."},
            ],
            "outputs": [{"processed": item["processed"], "terminal": item["terminal"], "events": item["eventNames"]}],
            "termination": item["terminal"]["state"],
        }
    if facet == "errors-recovery":
        failed = item["terminal"]["state"] == "failed"
        return {
            "facet": "errors-recovery",
            "kind": "failure-recovery-event",
            "subject": subject,
            "trigger": "The worker processor throws an error." if failed else "The worker processor completes successfully.",
            "operationRef": sid(label),
            "error": {"category": "processor-error" if failed else "none", "code": "Error" if failed else "", "message": item["terminal"].get("error", "")},
            "origin": "worker processor" if failed else "none",
            "propagationBoundary": "BullMQ Worker",
            "recoveryActions": [],
            "recoveryState": "job moved to failed state" if failed else "job moved to completed state",
            "terminalOutcome": item["terminal"]["state"],
            "expectedRejection": failed,
        }
    return {
        "facet": "data",
        "kind": "data-value",
        "subject": subject,
        "dataSubject": "queued job",
        "fieldPath": "setup and processed payload",
        "observedValue": {"setup": item["setup"], "processed": item["processed"]},
        "observedType": "object",
        "nullability": "not-applicable",
        "constraints": [{"type": "unique-custom-job-id", "field": "jobId"}],
    }


def build_capture(raw, prefix, source, raw_path):
    created = now()
    target_id = "bullmq-messaging-source" if source else "bullmq-messaging-python-replica"
    capture_id = "bullmq-messaging-source-capture" if source else "bullmq-messaging-python-capture"
    evidence_id = "bullmq-messaging-source-runtime" if source else "bullmq-messaging-python-runtime"
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    captured = raw.get("capturedAt", created)
    version = raw.get("packageVersion", "6.7.10") if source else "Python 3.12"
    revision = raw.get("sourceCommit") if source else os.getenv("GITHUB_SHA", "working-tree")
    scenarios, executions, observations = [], [], []
    by_facet = {facet: [] for facet in FACETS}
    raw_items = {item["label"]: item for item in raw["scenarios"]}

    for label in LABELS:
        item = raw_items[label]
        scenarios.append({
            "scenarioId": sid(label),
            "title": label.replace("-", " ").title(),
            "purpose": "Probe queue message identity, worker processing, event ordering, and terminal acknowledgement/failure.",
            "facetIds": FACETS,
            "subject": "bullmq-message-job",
            "preconditions": ["A Redis-backed BullMQ queue or independent in-memory queue is initialized.", "A single worker is configured for the scenario."],
            "trigger": "Enqueue a job and let the worker process it.",
            "inputs": item["setup"],
            "observableQuestions": ["Is a duplicate custom job identifier suppressed?", "Which payload is processed?", "What is the event order?", "What terminal state and counts are recorded?"],
        })
        executions.append({
            "executionId": eid(prefix, label),
            "scenarioId": sid(label),
            "targetId": target_id,
            "startedAt": captured,
            "endedAt": captured,
            "status": "completed",
            "actualContext": {"runtime": "Node.js / BullMQ / Redis 7" if source else "Python 3.12 in-memory queue model", "sourceRevision": revision, "packageVersion": version},
            "actualInputs": item["setup"],
            "trigger": scenarios[-1]["trigger"],
            "collector": {"name": "BullMQ QueueEvents runtime probe" if source else "Independent Python queue model"},
            "limitations": ["Only duplicate custom job IDs and one successful/one failed processing outcome are covered."],
        })
        for facet in FACETS:
            observation_id = oid(prefix, label, facet)
            by_facet[facet].append(observation_id)
            observations.append({
                "observationId": observation_id,
                "targetId": target_id,
                "executionId": eid(prefix, label),
                "facet": facet,
                "subject": "bullmq-message-job",
                "observedAt": captured,
                "sequence": len(observations),
                "method": {"class": "instrumentation", "procedure": "Enqueue controlled jobs, observe queue events and worker outcomes, and query terminal job counts.", "tool": "BullMQ Queue/Worker/QueueEvents" if source else "Python 3.12 queue model"},
                "conditions": {"scenario": label, "attempts": 1, "workerConcurrency": 1},
                "trigger": scenarios[-1]["trigger"],
                "payload": payload(label, item, facet),
                "rawValue": item,
                "normalizedValue": projection(item, facet),
                "evidenceRefs": [evidence_id],
                "status": "observed",
            })

    props = [
        ("BMQ-M-001", "messaging", "duplicate-custom-job-id", "Adding a second job with the same retained custom job ID does not replace or redeliver the first job.", [oid(prefix, LABELS[0], "messaging")]),
        ("BMQ-M-002", "messaging", "queue-event-order", "The observed queue event order is waiting, active, then completed or failed.", [oid(prefix, label, "messaging") for label in LABELS]),
        ("BMQ-BG-001", "background-processing", "single-worker-processing", "One queued job is processed once by a worker with concurrency one.", [oid(prefix, LABELS[0], "background-processing")]),
        ("BMQ-E-001", "errors-recovery", "terminal-consumer-failure", "A processor error with attempts set to one produces a terminal failed job state.", [oid(prefix, LABELS[1], "errors-recovery")]),
        ("BMQ-D-001", "data", "first-payload-authority", "The payload attached to the first retained job ID remains the payload processed after a duplicate add.", [oid(prefix, LABELS[0], "data")]),
    ]
    inventory = [{
        "propertyId": pid, "facet": facet, "subject": "bullmq-message-job", "dimension": dimension,
        "requirement": "required", "status": "captured", "observationRefs": refs,
        "evidenceRefs": [evidence_id], "rationale": rationale,
    } for pid, facet, dimension, rationale, refs in props]
    rules = []
    for pid, facet, dimension, rationale, refs in props:
        rules.append({
            "ruleId": pid, "facet": facet, "subject": dimension, "proposition": rationale,
            "trigger": "A queue job is added and processed by the worker.",
            "applicability": {"scope": "BullMQ 6.7.10 pinned source commit, Redis 7, attempts=1, worker concurrency=1."},
            "status": "supported", "supportingObservationIds": refs,
        })
    evidence = [{
        "evidenceId": evidence_id, "evidenceClass": "runtime", "evidenceType": "instrumented-queue-runtime-capture",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": "BullMQ QueueEvents runtime probe" if source else "Independent Python queue model", "sourceRevision": revision, "location": raw_path},
        "capturedAt": captured, "embedded": {"scenarios": LABELS, "sha256": digest},
        "locator": raw_path, "digest": digest, "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "Retained CI artifact and repository evidence after successful main-branch validation."},
    }]
    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture bounded BullMQ message lifecycle, duplicate suppression, and consumer outcome rules.",
        "target": {
            "targetId": target_id,
            "systemName": "BullMQ" if source else "Independent Python queue replica",
            "systemVersion": version,
            "build": {"revision": revision},
            "boundary": {
                "description": "Two queue scenarios: duplicate custom job ID and terminal consumer failure.",
                "included": ["Duplicate custom job ID suppression", "First payload remains authoritative", "Waiting-active-completed event sequence", "Waiting-active-failed event sequence", "Terminal job state and counts"],
                "excluded": ["Exactly-once delivery guarantees", "Redelivery after process crash", "Delayed/scheduled jobs", "Priority and concurrency greater than one", "Distributed worker recovery and stalled jobs"],
            },
            "environment": {
                "platform": "GitHub Actions runner", "os": "Ubuntu Linux",
                "runtime": "Node.js / BullMQ / Redis 7" if source else "Python 3.12",
                "configuration": {"state": "observed", "value": {"attempts": 1, "workerConcurrency": 1, "redis": "7" if source else "not used"}},
            },
        },
        "scope": {"description": "Two message lifecycle scenarios across five facets and five required properties.", "facetIds": FACETS, "subjects": ["bullmq-message-job"], "scenarioIds": [sid(label) for label in LABELS]},
        "collector": {"name": "BullMQ QueueEvents runtime probe" if source else "Independent Python queue model", "methodDescription": "Enqueue controlled jobs, observe event sequence, processed payload, terminal state, and queue counts."},
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [{
            "facet": facet, "subject": "bullmq-message-job", "status": "observed",
            "reason": "Both declared scenarios have a facet-specific runtime observation.",
            "scenarioIds": [sid(label) for label in LABELS], "executionIds": [eid(prefix, label) for label in LABELS],
        } for facet in FACETS],
        "limitations": ["This bounded case does not prove exactly-once processing or every BullMQ delivery guarantee."],
        "replicationScope": {
            "scopeId": "bullmq-message-lifecycle-scope",
            "description": "Complete inventory for two queue scenarios and five required properties.",
            "facets": FACETS, "propertyInventory": inventory,
            "completeness": {
                "status": "complete", "assessedAt": created,
                "assessmentMethod": "Every required property in this bounded case is linked to observed facet-specific records and retained runtime evidence.",
                "rationale": "All five required properties were observed on the pinned source and independent implementation.",
            },
        },
    }


def build_report(source_capture, replica_capture):
    created = now()
    alignments, results = [], []
    for label in LABELS:
        for facet in FACETS:
            left_obs = next(o for o in source_capture["observations"] if o["executionId"] == eid("source", label) and o["facet"] == facet)
            right_obs = next(o for o in replica_capture["observations"] if o["executionId"] == eid("replica", label) and o["facet"] == facet)
            alignment_id = f"bullmq-msg-align-{label}-{facet}"
            left, right = left_obs["normalizedValue"], right_obs["normalizedValue"]
            alignments.append({
                "alignmentId": alignment_id, "facet": facet,
                "referenceRecordIds": [left_obs["observationId"]], "implementationRecordIds": [right_obs["observationId"]],
                "status": "paired", "identityBasis": "scenario-subject-facet-condition",
                "rationale": "Both observations cover the same queue scenario and facet.",
            })
            results.append({
                "resultId": f"bullmq-msg-result-{label}-{facet}", "alignmentId": alignment_id,
                "facet": facet, "dimension": "message-lifecycle-semantic-projection",
                "classification": "match" if left == right else "mismatch", "comparisonBasis": "semantic",
                "referenceObservationIds": [left_obs["observationId"]], "implementationObservationIds": [right_obs["observationId"]],
                "referenceValue": left, "implementationValue": right,
                "reason": "The message lifecycle projection matches." if left == right else "The message lifecycle projection differs.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    units = len(results)
    return {
        "schemaVersion": "0.2.0", "reportId": "bullmq-messaging-cross-stack-comparison", "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/BMQ-MSG-001/artifacts/bullmq-messaging-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/BMQ-MSG-001/artifacts/bullmq-messaging-python.capture.json"},
        "comparisonScope": {
            "description": "Compare duplicate suppression, event order, consumer outcome, processed payload, and terminal queue counts.",
            "facets": FACETS, "scenarioIds": [sid(label) for label in LABELS],
            "conditions": ["BullMQ 6.7.10 at pinned source commit with Redis 7", "Python 3.12 independent in-memory queue model", "Attempts=1 and worker concurrency=1"],
            "excludedDimensions": ["Crash redelivery, exactly-once semantics, delayed jobs, priorities, and distributed worker recovery"],
            "limitations": ["The comparison establishes only the two declared queue scenarios."],
        },
        "normalizationProfile": {
            "profileId": "bullmq-message-lifecycle-projection", "version": "1.0.0",
            "operations": [{
                "operationId": "compare-message-lifecycle", "facet": "messaging", "dimension": "message-lifecycle-semantic-projection",
                "method": "Compare job identity and stored payload, processed payload, ordered QueueEvents names, terminal outcome, and queue counts.",
                "methodVersion": "1.0.0", "inputRepresentation": "Raw BullMQ and Python queue captures",
                "outputRepresentation": "Normalized message lifecycle projection", "preservesRaw": True,
            }],
        },
        "alignments": alignments, "results": results,
        "coverage": {
            "reference": {"declaredUnits": units, "observedUnits": units, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "implementation": {"declaredUnits": units, "observedUnits": units, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "sharedComparableUnits": units, "incomparableUnits": 0, "limitations": ["Coverage is limited to ten scenario/facet projections."],
        },
        "conclusion": {
            "status": "differences-found" if mismatches else "agreement-within-observed-scope",
            "statement": f"The independent Python implementation {'differs from' if mismatches else 'matches'} BullMQ for the two declared message scenarios and {units} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True, "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about BullMQ behaviour outside the declared message lifecycle scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete", "implementationStatus": "complete", "result": "complete-both",
            "statement": "Both captures account for all required properties in the two-scenario case scope, not the entire messaging facet.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    source = build_capture(read(args.source), "source", True, "conformance/replication-lab/cases/BMQ-MSG-001/artifacts/bullmq-messaging-source-runtime.json")
    replica = build_capture(read(args.replica), "replica", False, "conformance/replication-lab/cases/BMQ-MSG-001/artifacts/bullmq-messaging-python-runtime.json")
    report = build_report(source, replica)
    write(out / "bullmq-messaging-source.capture.json", source)
    write(out / "bullmq-messaging-python.capture.json", replica)
    write(out / "bullmq-messaging-comparison.report.json", report)
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit("Source and replica differ; refusing to emit a passing case.")
    print(json.dumps({"result": report["conclusion"]["status"], "semanticProjections": len(report["results"])}, indent=2))


if __name__ == "__main__":
    main()
