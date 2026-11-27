import argparse
import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


FACETS = ["background-processing", "errors-recovery", "data", "behavior"]
LABELS = {
    "positive-backoff-completes": "positive",
    "minus-one-suppresses-retry": "minus-one",
    "zero-delay-respects-attempt-limit": "zero-delay",
}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def scenario_id(label):
    return "bmq-scenario-" + LABELS[label]


def execution_id(prefix, label):
    return f"bmq-exec-{prefix}-{LABELS[label]}"


def observation_id(prefix, label, facet):
    short = {
        "background-processing": "background",
        "errors-recovery": "errors",
        "data": "data",
        "behavior": "behavior",
    }[facet]
    return f"bmq-obs-{prefix}-{LABELS[label]}-{short}"


def transitions(scenario):
    return [
        event["event"].removeprefix("queue:")
        for event in scenario.get("trace", [])
        if event.get("event") in {
            "queue:delayed",
            "queue:waiting",
            "queue:failed",
            "queue:completed",
        }
    ] if "trace" in scenario else scenario["stateTransitions"]


def processor_attempt_values(scenario):
    if "trace" in scenario:
        return [
            event["attemptsMade"]
            for event in scenario["trace"]
            if event.get("event") == "processor"
        ]
    return scenario["processorAttemptsMade"]


def projection(scenario, facet):
    base = {
        "configuredAttempts": scenario["configuredAttempts"],
        "processorAttempts": scenario["processorAttempts"],
        "processorAttemptsMade": processor_attempt_values(scenario),
        "strategyAttempts": scenario["strategyAttempts"],
        "backoffResults": scenario["backoffResults"] if "backoffResults" in scenario else [
            event["delayMs"] for event in scenario["trace"]
            if event.get("event") == "backoff-result"
        ],
        "stateTransitions": transitions(scenario),
        "terminal": scenario["outcome"]["terminal"],
        "attemptsMade": scenario["outcome"]["attemptsMade"],
        "finalState": scenario["finalState"],
    }
    if facet == "background-processing":
        return {k: base[k] for k in [
            "configuredAttempts", "processorAttempts", "strategyAttempts",
            "backoffResults", "stateTransitions", "terminal", "finalState"
        ]}
    if facet == "errors-recovery":
        return {
            "backoffResults": base["backoffResults"],
            "stateTransitions": base["stateTransitions"],
            "terminal": base["terminal"],
            "finalState": base["finalState"],
        }
    if facet == "data":
        return {
            "processorAttemptsMade": base["processorAttemptsMade"],
            "attemptsMade": base["attemptsMade"],
        }
    return {
        "processorAttemptsMade": base["processorAttemptsMade"],
        "stateTransitions": base["stateTransitions"],
        "terminal": base["terminal"],
        "finalState": base["finalState"],
    }


def payload_for(scenario, facet):
    label = scenario["label"]
    terminal = scenario["outcome"]["terminal"]
    result = scenario["outcome"]
    if facet == "background-processing":
        return {
            "facet": "background-processing",
            "kind": "job-lifecycle",
            "subject": "job-retry-policy",
            "job": "probe",
            "trigger": "The worker processor returns successfully or throws an error.",
            "worker": {
                "processorAttempts": scenario["processorAttempts"],
                "strategyAttempts": scenario["strategyAttempts"],
            },
            "lifecycle": [{"state": state} for state in transitions(scenario)],
            "attemptCount": scenario["processorAttempts"],
            "inputs": {
                "configuredAttempts": scenario["configuredAttempts"],
                "backoffResults": scenario["backoffResults"] if "backoffResults" in scenario else [
                    event["delayMs"] for event in scenario["trace"]
                    if event.get("event") == "backoff-result"
                ],
            },
            "retry": {
                "strategyAttempts": scenario["strategyAttempts"],
                "backoffResults": scenario["backoffResults"] if "backoffResults" in scenario else [
                    event["delayMs"] for event in scenario["trace"]
                    if event.get("event") == "backoff-result"
                ],
            },
            "terminalResult": terminal,
            "output": {
                "finalState": scenario["finalState"],
                "attemptsMade": result["attemptsMade"],
                "result": result.get("result"),
            },
        }
    if facet == "errors-recovery":
        error_message = result.get("error")
        return {
            "facet": "errors-recovery",
            "kind": "failure-recovery-event",
            "subject": "job-retry-policy",
            "trigger": "The processor throws and BullMQ evaluates retry eligibility and backoff.",
            "operationRef": scenario_id(label),
            "error": {
                "category": "processor-error" if error_message else "none",
                "message": error_message or "",
            },
            "origin": "worker processor",
            "propagationBoundary": "BullMQ Job.moveToFailed retry decision",
            "recoveryActions": [
                {"action": "backoff-evaluated", "result": value}
                for value in (
                    scenario["backoffResults"] if "backoffResults" in scenario else [
                        event["delayMs"] for event in scenario["trace"]
                        if event.get("event") == "backoff-result"
                    ]
                )
            ],
            "recoveryState": scenario["finalState"],
            "terminalOutcome": terminal,
            "expectedRejection": terminal == "failed",
        }
    if facet == "data":
        return {
            "facet": "data",
            "kind": "data-value",
            "subject": "job-attempt-counter",
            "dataSubject": "BullMQ Job",
            "fieldPath": "attemptsMade",
            "observedValue": result["attemptsMade"],
            "observedType": "integer",
            "nullability": "non-null",
            "serialization": {"representation": "JSON number"},
        }
    return {
        "facet": "behavior",
        "kind": "triggered-operation",
        "subject": "job-retry-lifecycle",
        "trigger": "A worker processor attempt returns or throws.",
        "preconditions": [f"Configured attempts limit is {scenario['configuredAttempts']}"],
        "actions": [
            {"sequence": i, "action": f"Processor attempt {i}", "input": {"attemptsMadeBeforeAttempt": value}}
            for i, value in enumerate(processor_attempt_values(scenario), start=1)
        ],
        "stateTransitions": [
            {"from": "active", "to": state}
            for state in transitions(scenario)
        ],
        "outputs": [
            {"terminalState": scenario["finalState"], "attemptsMade": result["attemptsMade"]}
        ],
        "termination": terminal,
    }


def build_capture(raw, prefix, is_source, raw_path, replica_revision):
    created = now()
    target_id = "bullmq-source-runtime" if is_source else "bullmq-python-replica"
    capture_id = "bullmq-source-runtime-capture" if is_source else "bullmq-python-replica-capture"
    evidence_id = "bmq-source-runtime-json" if is_source else "bmq-python-replica-json"
    package_version = raw.get("packageVersion", "independent-model")
    revision = raw.get("sourceCommit") if is_source else replica_revision
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    collector_name = "Instrumented BullMQ worker, QueueEvents, and Job state" if is_source else "Independent Python retry-policy model execution"

    scenarios = []
    executions = []
    observations = []
    coverage = []
    inventory = []
    observation_ids_by_facet = {facet: [] for facet in FACETS}

    for raw_scenario in raw["scenarios"]:
        label = raw_scenario["label"]
        sid = scenario_id(label)
        eid = execution_id(prefix, label)
        scenarios.append({
            "scenarioId": sid,
            "title": label.replace("-", " ").title(),
            "purpose": "Probe custom retry eligibility, backoff routing, attempt counters, and terminal state.",
            "facetIds": FACETS,
            "subject": "job-retry-policy",
            "preconditions": [
                "A fresh isolated queue and worker are used for the scenario.",
                f"Configured attempts limit is {raw_scenario['configuredAttempts']}.",
                "The worker uses a deterministic custom backoff strategy.",
            ],
            "trigger": "Add a job and let its processor return or throw according to the scenario.",
            "inputs": {
                "configuredAttempts": raw_scenario["configuredAttempts"],
                "scenario": label,
            },
            "observableQuestions": [
                "How many processor attempts occur?",
                "Which attempt numbers are passed to the backoff strategy?",
                "How are backoff results routed?",
                "What are the terminal state and attemptsMade value?",
            ],
        })
        executions.append({
            "executionId": eid,
            "scenarioId": sid,
            "targetId": target_id,
            "startedAt": started,
            "endedAt": ended,
            "status": "completed",
            "actualContext": {
                "runtime": "Node.js with Redis 7" if is_source else "Python 3.12",
                "sourcePackageVersion": package_version if is_source else None,
                "sourceRevision": revision if is_source else None,
                "independentReplica": not is_source,
                "scope": "Three deterministic retry/backoff scenarios only",
            },
            "actualInputs": {
                "configuredAttempts": raw_scenario["configuredAttempts"],
                "backoffResults": raw_scenario.get("backoffResults", []),
            },
            "trigger": "Enqueue and process one job in a fresh queue/model instance.",
            "collector": {"name": collector_name},
            "limitations": [
                "Does not cover every BullMQ retry option, scheduler condition, or deployment configuration."
            ],
        })

        for facet in FACETS:
            oid = observation_id(prefix, label, facet)
            observation_ids_by_facet[facet].append(oid)
            observations.append({
                "observationId": oid,
                "targetId": target_id,
                "executionId": eid,
                "facet": facet,
                "subject": "job-retry-policy",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Execute the declared scenario and retain processor attempts, backoff inputs/results, ordered state events, and terminal job/model state.",
                    "tool": "BullMQ runtime probe" if is_source else "Python replica simulator",
                },
                "conditions": {
                    "scenario": label,
                    "configuredAttempts": raw_scenario["configuredAttempts"],
                },
                "trigger": "A job processor attempt returns or throws.",
                "payload": payload_for(raw_scenario, facet),
                "rawValue": copy.deepcopy(raw_scenario),
                "normalizedValue": projection(raw_scenario, facet),
                "evidenceRefs": [evidence_id],
                "status": "observed",
            })

    property_specs = [
        ("BMQ-P-001", "background-processing", "processor-attempt-count", "Total processor attempts in each scenario."),
        ("BMQ-P-002", "background-processing", "backoff-decision-and-routing", "Backoff attempt numbers, return values, and ordered queue transitions."),
        ("BMQ-P-003", "errors-recovery", "retry-suppression-and-terminal-outcome", "Whether retry is suppressed or the job reaches completion/failure."),
        ("BMQ-P-004", "behavior", "ordered-state-transitions", "The ordered delayed/waiting/failed/completed transitions."),
        ("BMQ-P-005", "data", "attemptsMade-counter", "The terminal attemptsMade value, including successful completion."),
        ("BMQ-P-006", "data", "attempt-counter-before-processing", "The attemptsMade value observed at the beginning of each processor attempt."),
    ]
    for pid, facet, dimension, rationale in property_specs:
        inventory.append({
            "propertyId": pid,
            "facet": facet,
            "subject": "job-retry-policy",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": observation_ids_by_facet[facet],
            "evidenceRefs": [evidence_id],
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "BMQ-ER-004",
            "facet": "background-processing",
            "subject": "job-retry-policy",
            "proposition": "A job is retried after a processor failure only while the configured attempts limit permits another attempt; when the limit is reached, the job transitions to failed.",
            "trigger": "A processor attempt throws.",
            "applicability": {"scope": "The configured attempts=2 boundary in this case."},
            "status": "supported",
            "supportingObservationIds": observation_ids_by_facet["background-processing"],
        },
        {
            "ruleId": "BMQ-ER-005",
            "facet": "background-processing",
            "subject": "job-retry-policy",
            "proposition": "A custom backoff result of -1 suppresses retry, a positive delay routes through delayed state, and zero routes immediately back to waiting.",
            "trigger": "A processor attempt throws and the custom backoff strategy returns a value.",
            "applicability": {"scope": "The tested deterministic custom strategy results -1, 0, 40, and 80 milliseconds."},
            "status": "supported",
            "supportingObservationIds": observation_ids_by_facet["background-processing"],
        },
        {
            "ruleId": "BMQ-ER-006",
            "facet": "data",
            "subject": "job-attempt-counter",
            "proposition": "BullMQ increments attemptsMade after each failed attempt and also after a successful completion; the value observed at the start of processing is the number of prior failures.",
            "trigger": "A processor attempt fails or completes.",
            "applicability": {"scope": "The tested two-failure-then-success, suppressed-retry, and attempt-limit scenarios."},
            "status": "supported",
            "supportingObservationIds": observation_ids_by_facet["data"],
        },
    ]

    for facet in FACETS:
        coverage.append({
            "facet": facet,
            "subject": "job-retry-policy",
            "status": "observed",
            "reason": "All declared scenario executions produced an observation for this facet.",
            "scenarioIds": [scenario_id(item["label"]) for item in raw["scenarios"]],
            "executionIds": [execution_id(prefix, item["label"]) for item in raw["scenarios"]],
        })

    evidence = [{
        "evidenceId": evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "instrumented-runtime-capture" if is_source else "independent-model-execution-capture",
        "mediaType": "application/json",
        "origin": {
            "targetId": target_id,
            "collector": collector_name,
            "sourceRevision": revision,
            "location": raw_path,
        },
        "capturedAt": ended,
        "embedded": {
            "scenarioLabels": [item["label"] for item in raw["scenarios"]],
            "rawCaptureDigest": digest,
        },
        "locator": raw_path,
        "digest": digest,
        "sizeBytes": len(raw_bytes),
        "retention": {
            "status": "retained",
            "access": "GitHub Actions artifact bullmq-cross-stack-captures",
        },
    }]

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared three-scenario BullMQ retry/backoff conformance scope in the Software Rules format.",
        "target": {
            "targetId": target_id,
            "systemName": "BullMQ" if is_source else "Independent Python retry-policy model",
            "systemVersion": package_version if is_source else "Python 3.12 model",
            "build": {"revision": revision},
            "boundary": {
                "description": "A bounded retry/backoff decision and terminal-state probe; not a complete capture of BullMQ or a full queue implementation.",
                "included": [
                    "Three declared processor/retry scenarios",
                    "Processor attempt count and attemptsMade values",
                    "Custom backoff strategy inputs and results",
                    "Observed delayed/waiting/failed/completed transitions",
                ],
                "excluded": [
                    "Other retry options and unrecoverable-error variants",
                    "Queue scheduler, rate limiting, stalled jobs, and worker shutdown",
                    "Production deployment and external application behaviour",
                    "Exact processor error-message equality between source and replica",
                ],
            },
            "environment": {
                "platform": "CI runner",
                "os": "Ubuntu Linux",
                "runtime": "Node.js and Redis 7" if is_source else "Python 3.12",
                "configuration": {
                    "state": "observed",
                    "value": {"scenarioCount": len(raw["scenarios"]), "sourceCommit": revision if is_source else None},
                },
            },
        },
        "scope": {
            "description": "Three deterministic retry/backoff scenarios: positive delays then completion; -1 suppression; zero-delay retry followed by attempts-limit failure.",
            "facetIds": FACETS,
            "subjects": ["job-retry-policy", "job-attempt-counter"],
            "scenarioIds": [scenario_id(item["label"]) for item in raw["scenarios"]],
        },
        "collector": {
            "name": collector_name,
            "methodDescription": "Controlled scenario execution with instrumentation of processor calls, backoff strategy arguments/results, queue lifecycle events, and terminal job state.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": coverage,
        "limitations": [
            "The replica is a narrow independent decision-model simulation, not a BullMQ replacement or Redis-backed queue.",
            "The comparison is limited to the declared scenarios and semantic fields; error-message text and scheduler timing are excluded.",
        ],
        "replicationScope": {
            "scopeId": "bullmq-three-scenario-retry-scope",
            "description": "Complete property inventory for the three explicitly declared retry/backoff scenarios only.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "Every required property is linked to observed facet-specific records and retained runtime evidence for all three declared scenarios.",
                "rationale": "All six required properties in this bounded case scope were observed in every declared scenario. This does not imply complete coverage of BullMQ retry behaviour or any entire facet.",
            },
        },
    }


def build_report(source_capture, replica_capture):
    created = now()
    alignments = []
    results = []
    comparable = 0
    for label in LABELS:
        sid = scenario_id(label)
        source_scenario = next(s for s in source_capture["scenarios"] if s["scenarioId"] == sid)
        replica_scenario = next(s for s in replica_capture["scenarios"] if s["scenarioId"] == sid)
        for facet in FACETS:
            source_obs = next(o for o in source_capture["observations"] if o["executionId"] == execution_id("source", label) and o["facet"] == facet)
            replica_obs = next(o for o in replica_capture["observations"] if o["executionId"] == execution_id("replica", label) and o["facet"] == facet)
            aid = f"bmq-align-{LABELS[label]}-{facet}"
            left = source_obs["normalizedValue"]
            right = replica_obs["normalizedValue"]
            match = left == right
            comparable += 1
            alignments.append({
                "alignmentId": aid,
                "facet": facet,
                "referenceRecordIds": [source_obs["observationId"]],
                "implementationRecordIds": [replica_obs["observationId"]],
                "status": "paired",
                "identityBasis": "scenario-subject-facet-condition",
                "rationale": "Both records are observations of the same declared retry scenario and facet.",
            })
            results.append({
                "resultId": f"bmq-result-{LABELS[label]}-{facet}",
                "alignmentId": aid,
                "facet": facet,
                "dimension": "retry-policy-semantic-projection",
                "classification": "match" if match else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_obs["observationId"]],
                "implementationObservationIds": [replica_obs["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "The declared semantic projection matches." if match else "The source and independent replica semantic projections differ.",
            })

    mismatches = [item for item in results if item["classification"] != "match"]
    conclusion_status = "differences-found" if mismatches else "agreement-within-observed-scope"
    statement = (
        f"The independent Python model {'matches' if not mismatches else 'differs from'} the pinned BullMQ runtime for the three declared retry/backoff scenarios and {comparable} facet/scenario projections. "
        "This is bounded evidence for these rules and inputs, not universal equivalence or proof for all BullMQ behaviours or all technology stacks."
    )
    return {
        "schemaVersion": "0.2.0",
        "reportId": "bullmq-three-scenario-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {
            "captureId": source_capture["captureId"],
            "schemaVersion": "0.2.0",
            "artifactRef": "bullmq-source.capture.json",
        },
        "implementationCapture": {
            "captureId": replica_capture["captureId"],
            "schemaVersion": "0.2.0",
            "artifactRef": "bullmq-python-replica.capture.json",
        },
        "comparisonScope": {
            "description": "Compare the retry decision, attempt counters, ordered state transitions, and terminal outcomes for the three declared scenarios.",
            "facets": FACETS,
            "scenarioIds": [scenario_id(label) for label in LABELS],
            "conditions": [
                "BullMQ 6.7.10 at the pinned source commit with Redis 7",
                "Python 3.12 independent retry-policy model",
                "Deterministic custom backoff results: 40/80 ms, -1, and 0 ms",
            ],
            "excludedDimensions": [
                "Exact processor error-message and stack-trace equality",
                "Redis scheduler timing and internal implementation details",
                "UnrecoverableError and maxStartedAttempts branches",
                "Other retry/backoff strategies and the full BullMQ worker lifecycle",
            ],
            "limitations": [
                "The Python replica models the decision semantics and does not implement BullMQ, Redis, queue storage, or the worker scheduler.",
            ],
        },
        "normalizationProfile": {
            "profileId": "bmq-retry-semantic-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "project-retry-semantics",
                "facet": "background-processing",
                "dimension": "retry-policy-semantic-projection",
                "method": "Compare configured attempt limit, processor attempts, backoff attempt numbers/results, ordered queue transitions, terminal state, and attemptsMade while excluding error text and wall-clock values.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Raw instrumented source and independent replica JSON captures",
                "outputRepresentation": "Ordered semantic retry-policy projection",
                "preservesRaw": True,
            }],
        },
        "alignments": alignments,
        "results": results,
        "coverage": {
            "reference": {"declaredUnits": comparable, "observedUnits": comparable, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "implementation": {"declaredUnits": comparable, "observedUnits": comparable, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "sharedComparableUnits": comparable,
            "incomparableUnits": 0,
            "limitations": ["Coverage is limited to the 12 facet/scenario projections defined in this report."],
        },
        "conclusion": {
            "status": conclusion_status,
            "statement": statement,
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": [
            "A match for this finite probe matrix does not prove compatibility with every BullMQ option, workload, or technology stack.",
        ],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for every required property in the declared three-scenario case scope; neither capture claims full BullMQ or full-facet completeness.",
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
    source_raw = read_json(args.source)
    replica_raw = read_json(args.replica)
    source_capture = build_capture(source_raw, "source", True, "bullmq-runtime-capture.json", os.getenv("BULLMQ_SOURCE_COMMIT", source_raw.get("sourceCommit", "pinned")))
    replica_capture = build_capture(replica_raw, "replica", False, "bullmq-replica-capture.json", os.getenv("GITHUB_SHA", "working-tree"))
    report = build_report(source_capture, replica_capture)
    write_json(output / "bullmq-source.capture.json", source_capture)
    write_json(output / "bullmq-python-replica.capture.json", replica_capture)
    write_json(output / "bullmq-comparison.report.json", report)
    print(json.dumps({
        "sourceCapture": source_capture["captureId"],
        "replicaCapture": replica_capture["captureId"],
        "comparison": report["conclusion"]["status"],
        "resultCount": len(report["results"]),
        "outputDirectory": str(output),
    }, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
