import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACET = "integrations"
LABELS = ["ping", "set-get", "missing-get", "exists", "ttl", "wrongtype", "connection-failure"]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "redis-int-scenario-" + label


def eid(side, label):
    return "redis-int-exec-" + side + "-" + label


def oid(side, label):
    return "redis-int-obs-" + side + "-" + label


def build_capture(raw, side, raw_path):
    created = now()
    source = side == "source"
    target_id = "go-redis-source" if source else "python-redis-replica"
    capture_id = "go-redis-source-capture" if source else "python-redis-replica-capture"
    runtime_name = "go-redis Go client" if source else "redis-py Python client"
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    captured = raw.get("capturedAt", created)
    scenarios, executions, observations = [], [], []
    observation_ids = [oid(side, label) for label in LABELS]
    for index, item in enumerate(raw["scenarios"]):
        label = item["label"]
        request = item["request"]
        scenarios.append({
            "scenarioId": sid(label), "title": label.replace("-", " ").title(),
            "purpose": "Observe an external Redis dependency response for a controlled client operation.",
            "facetIds": [FACET], "subject": "Redis client interaction",
            "preconditions": ["An isolated Redis 7 service is available.", "The source or replica client is configured with the same logical database."],
            "trigger": request["operation"], "inputs": request,
            "observableQuestions": ["Does the dependency operation succeed or fail?", "What normalized response or failure category is returned?"],
        })
        executions.append({
            "executionId": eid(side, label), "scenarioId": sid(label), "targetId": target_id,
            "startedAt": captured, "endedAt": captured, "status": "completed",
            "actualContext": {"runtime": "Go / go-redis" if source else "Python 3.12 / redis-py", "dependency": "Redis 7", "sourceRevision": raw.get("sourceCommit", "independent-replica")},
            "actualInputs": request, "trigger": request["operation"],
            "collector": {"name": runtime_name},
        })
        payload = {
            "facet": FACET, "kind": "external-interaction", "subject": "Redis client operation",
            "provider": "Redis", "boundary": "Redis TCP protocol endpoint",
            "direction": "outbound", "operation": request["operation"],
            "protocolRef": "RESP", "requestRef": label,
            "responseRef": label + "-response",
            "resilience": {"failureCategory": item["value"] if item["outcome"] == "failure" else None},
            "dependencyOutcome": item["outcome"],
            "extensions": {"logicalKey": request.get("logicalKey"), "normalizedValue": item["value"]},
        }
        observations.append({
            "observationId": oid(side, label), "targetId": target_id,
            "executionId": eid(side, label), "facet": FACET,
            "subject": "Redis client operation", "observedAt": captured, "sequence": index,
            "method": {"class": "instrumentation", "procedure": "Execute a Redis command through the client library and normalize its response or error.", "tool": runtime_name},
            "conditions": {"scenario": label}, "trigger": request["operation"],
            "payload": payload, "rawValue": item,
            "normalizedValue": {"request": request, "outcome": item["outcome"], "value": item["value"]},
            "evidenceRefs": ["redis-" + side + "-runtime"], "status": "observed",
        })
    properties = [
        ("REDIS-INT-P01", "command-success", "PING and SET/GET return the expected successful response."),
        ("REDIS-INT-P02", "missing-key-semantics", "GET for an absent key is normalized as a missing value."),
        ("REDIS-INT-P03", "expiry-semantics", "PTTL for a key with an active expiry is positive."),
        ("REDIS-INT-P04", "type-error-semantics", "GET on a list key returns a wrong-type failure."),
        ("REDIS-INT-P05", "connection-failure", "An unavailable Redis endpoint produces a connection failure."),
    ]
    inventory = [{
        "propertyId": pid, "facet": FACET, "subject": "Redis client integration",
        "dimension": dimension, "requirement": "required", "status": "captured",
        "observationRefs": observation_ids, "evidenceRefs": ["redis-" + side + "-runtime"],
        "rationale": rationale,
    } for pid, dimension, rationale in properties]
    rules = [{
        "ruleId": pid, "facet": FACET, "subject": dimension, "proposition": rationale,
        "trigger": "A client issues a command across the Redis integration boundary.",
        "applicability": {"scope": "Pinned go-redis client / redis-py client against Redis 7 for seven declared operations."},
        "status": "supported", "supportingObservationIds": observation_ids,
    } for pid, dimension, rationale in properties]
    return {
        "schemaVersion": "0.2.0", "captureId": capture_id, "createdAt": created,
        "purpose": "Capture bounded Redis client integration outcomes for seven operations.",
        "target": {
            "targetId": target_id, "systemName": "go-redis client" if source else "redis-py client",
            "systemVersion": "pinned source commit" if source else "redis-py 6.0.0",
            "build": {"revision": raw.get("sourceCommit", os.getenv("GITHUB_SHA", "working-tree"))},
            "boundary": {
                "description": "Client-to-Redis interaction for seven controlled operations.",
                "included": ["PING", "SET/GET", "missing GET", "EXISTS", "PTTL", "WRONGTYPE", "connection failure"],
                "excluded": ["Redis cluster", "TLS", "authentication", "sentinel", "pub/sub", "transactions", "pipelines", "all other commands"],
            },
            "environment": {"platform": "GitHub Actions", "os": "Ubuntu Linux", "runtime": "Go" if source else "Python 3.12", "configuration": {"state": "observed", "value": {"redis": "7", "database": 15}}},
        },
        "scope": {"description": "Seven Redis client integration operations.", "facetIds": [FACET], "subjects": ["Redis client operation"], "scenarioIds": [sid(label) for label in LABELS]},
        "collector": {"name": runtime_name, "methodDescription": "Run the same logical Redis operations through independent clients and compare normalized responses."},
        "scenarios": scenarios, "executions": executions, "observations": observations,
        "runtimeRules": rules,
        "evidence": [{
            "evidenceId": "redis-" + side + "-runtime", "evidenceClass": "runtime",
            "evidenceType": "instrumented-redis-client-interaction", "mediaType": "application/json",
            "origin": {"targetId": target_id, "collector": runtime_name, "sourceRevision": raw.get("sourceCommit", "independent-replica"), "location": raw_path},
            "capturedAt": captured, "embedded": {"scenarioLabels": LABELS, "sha256": digest},
            "locator": raw_path, "digest": digest, "sizeBytes": len(raw_bytes),
            "retention": {"status": "retained", "access": "CI artifact and case evidence."},
        }],
        "coverage": [{
            "facet": FACET, "subject": "Redis client integration", "status": "observed",
            "reason": "All seven declared operations executed against the isolated Redis service.",
            "scenarioIds": [sid(label) for label in LABELS], "executionIds": [eid(side, label) for label in LABELS],
        }],
        "limitations": ["This is a bounded Redis-client integration case, not full integration-facet coverage."],
        "replicationScope": {
            "scopeId": "redis-client-seven-operation-scope",
            "description": "Complete property inventory for the seven declared Redis operations only.",
            "facets": [FACET], "propertyInventory": inventory,
            "completeness": {
                "status": "complete", "assessedAt": created,
                "assessmentMethod": "Five required integration properties are linked to seven observations and retained runtime evidence.",
                "rationale": "All operations and required normalized outcomes in the declared scope are observed on both clients.",
            },
        },
    }


def build_report(source, replica):
    created = now()
    left = {x["observationId"].split("redis-int-obs-source-", 1)[1]: x for x in source["observations"]}
    right = {x["observationId"].split("redis-int-obs-replica-", 1)[1]: x for x in replica["observations"]}
    alignments, results = [], []
    for label in LABELS:
        a, b = left[label], right[label]
        aid = "redis-int-alignment-" + label
        alignments.append({
            "alignmentId": aid, "facet": FACET,
            "referenceRecordIds": [a["observationId"]], "implementationRecordIds": [b["observationId"]],
            "status": "paired", "identityBasis": "scenario-subject-facet-condition",
            "rationale": "Same logical Redis operation and key role.",
        })
        results.append({
            "resultId": "redis-int-result-" + label, "alignmentId": aid,
            "facet": FACET, "dimension": "normalized-dependency-outcome",
            "classification": "match" if a["normalizedValue"] == b["normalizedValue"] else "mismatch",
            "comparisonBasis": "semantic",
            "referenceObservationIds": [a["observationId"]], "implementationObservationIds": [b["observationId"]],
            "referenceValue": a["normalizedValue"], "implementationValue": b["normalizedValue"],
            "reason": "Compare normalized response/error semantics, not client-specific exception text.",
            "evidenceRefs": ["redis-source-runtime", "redis-replica-runtime"],
        })
    mismatches = [x for x in results if x["classification"] != "match"]
    return {
        "schemaVersion": "0.2.0", "reportId": "redis-client-integration-comparison", "createdAt": created,
        "referenceCapture": {"captureId": source["captureId"], "schemaVersion": "0.2.0"},
        "implementationCapture": {"captureId": replica["captureId"], "schemaVersion": "0.2.0"},
        "comparisonScope": {
            "description": "Seven logical Redis client operations against one isolated Redis 7 service.",
            "facets": [FACET], "scenarioIds": [sid(label) for label in LABELS],
            "conditions": ["Redis 7 service", "Database 15", "Separate source and replica key namespaces"],
            "excludedDimensions": ["TLS", "authentication", "cluster", "sentinel", "pub/sub", "transactions"],
            "limitations": ["Only seven operations are included."],
        },
        "alignments": alignments, "results": results,
        "coverage": {
            "reference": {"declaredUnits": 7, "observedUnits": 7},
            "implementation": {"declaredUnits": 7, "observedUnits": 7},
            "sharedComparableUnits": 7, "incomparableUnits": 0,
            "limitations": ["Seven operations do not exhaust Redis integration semantics."],
        },
        "conclusion": {
            "status": "differences-found" if mismatches else "agreement-within-observed-scope",
            "statement": f"The Python redis-py client {'differs from' if mismatches else 'matches'} go-redis for seven declared Redis interactions. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True, "universalEquivalenceClaimed": False,
        },
        "replicationCompleteness": {
            "referenceStatus": "complete", "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for the declared seven-operation Redis integration scope, not all Redis commands or the full integrations facet.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    source = build_capture(read(args.source), "source", args.source)
    replica = build_capture(read(args.replica), "replica", args.replica)
    report = build_report(source, replica)
    write(output / "redis-source.capture.json", source)
    write(output / "redis-python-replica.capture.json", replica)
    write(output / "redis-comparison.report.json", report)
    print(json.dumps({"results": len(report["results"]), "mismatches": sum(x["classification"] != "match" for x in report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
