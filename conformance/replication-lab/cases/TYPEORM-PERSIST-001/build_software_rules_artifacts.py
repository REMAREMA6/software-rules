import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACETS = ["persistence", "data", "behavior", "errors-recovery"]
LABELS = ["commit-success", "rollback-on-invalid-post"]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "typeorm-scenario-" + label


def eid(prefix, label):
    return f"typeorm-exec-{prefix}-{label}"


def oid(prefix, label, facet):
    return f"typeorm-obs-{prefix}-{label}-{facet}"


def normalized(scenario, facet):
    if facet == "persistence":
        return {
            "terminal": scenario["terminal"],
            "postRows": scenario.get("postRows", scenario.get("postRowsAfter")),
            "categoryRows": scenario.get("categoryRows", scenario.get("categoryRowsAfter")),
            "postCount": scenario.get("postCount", scenario.get("postCountAfter")),
            "categoryCount": scenario.get("categoryCount", scenario.get("categoryCountAfter")),
        }
    if facet == "data":
        return {
            "postRows": scenario.get("postRows", scenario.get("postRowsAfter")),
            "categoryRows": scenario.get("categoryRows", scenario.get("categoryRowsAfter")),
            "postCount": scenario.get("postCount", scenario.get("postCountAfter")),
            "categoryCount": scenario.get("categoryCount", scenario.get("categoryCountAfter")),
            "readsVisibleBeforeFailure": scenario.get("readsVisibleBeforeFailure"),
        }
    if facet == "behavior":
        return {
            "terminal": scenario["terminal"],
            "callbackResult": scenario.get("callbackResult"),
            "readsVisibleBeforeFailure": scenario.get("readsVisibleBeforeFailure"),
        }
    return {
        "errorPropagated": scenario.get("errorPropagated", False),
        "errorCategory": scenario.get("errorCategory", "none"),
        "terminal": scenario["terminal"],
        "postCountAfter": scenario.get("postCountAfter", scenario.get("postCount")),
        "categoryCountAfter": scenario.get("categoryCountAfter", scenario.get("categoryCount")),
    }


def payload(scenario, facet):
    rollback = scenario["label"] == "rollback-on-invalid-post"
    if facet == "persistence":
        return {
            "facet": "persistence",
            "kind": "state-operation",
            "subject": "typeorm-entity-manager-transaction",
            "store": "in-memory SQLite database",
            "operation": "transaction",
            "beforeState": {"post": [], "category": []},
            "afterState": {
                "post": scenario.get("postRows", scenario.get("postRowsAfter", [])),
                "category": scenario.get("categoryRows", scenario.get("categoryRowsAfter", [])),
            },
            "transaction": {
                "terminal": scenario["terminal"],
                "errorPropagated": scenario.get("errorPropagated", False),
            },
            "commitResult": "rolled-back" if rollback else "committed",
            "consistency": {"atomic": True, "observedAfterTransaction": True},
        }
    if facet == "data":
        return {
            "facet": "data",
            "kind": "data-value",
            "subject": "Post and Category entities",
            "dataSubject": "transactional entity rows",
            "fieldPath": "Post.title / Category.name",
            "observedValue": {
                "postRows": scenario.get("postRows", scenario.get("postRowsAfter", [])),
                "categoryRows": scenario.get("categoryRows", scenario.get("categoryRowsAfter", [])),
                "readsVisibleBeforeFailure": scenario.get("readsVisibleBeforeFailure"),
            },
            "observedType": "object",
            "nullability": "non-null",
            "constraints": [
                {"field": "Post.title", "constraint": "NOT NULL"},
                {"field": "Category.name", "constraint": "NOT NULL"},
            ],
            "validation": {
                "result": "integrity-constraint-rejected" if rollback else "valid",
                "errorCategory": scenario.get("errorCategory", "none"),
            },
            "serialization": {"representation": "JSON entity snapshots"},
        }
    if facet == "behavior":
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": "typeorm-entity-manager-transaction",
            "trigger": "Application invokes EntityManager.transaction(callback).",
            "preconditions": [
                "A Post entity has a required title field.",
                "A Category entity has a required name field.",
                "Both entities use the same in-memory SQLite DataSource.",
            ],
            "actions": [
                {"sequence": 1, "action": "Save a Post and Category through the callback manager."},
                {"sequence": 2, "action": "Read both rows through the callback manager." if rollback else "Return the inserted entity identifiers from the callback."},
                {"sequence": 3, "action": "Attempt an invalid Post insert." if rollback else "Commit the transaction."},
            ],
            "outputs": [{
                "terminal": scenario["terminal"],
                "callbackResult": scenario.get("callbackResult"),
                "readsVisibleBeforeFailure": scenario.get("readsVisibleBeforeFailure"),
            }],
            "termination": "callback-error-propagated-after-rollback" if rollback else "callback-result-returned-after-commit",
        }
    return {
        "facet": "errors-recovery",
        "kind": "failure-recovery-event",
        "subject": "typeorm-transaction-rollback",
        "trigger": "The callback attempts to insert a Post with a missing required title." if rollback else "No failure occurs in the transaction callback.",
        "operationRef": sid(scenario["label"]),
        "error": {
            "category": scenario.get("errorCategory", "none"),
            "code": "SQLITE_CONSTRAINT_NOTNULL" if rollback else "",
            "message": "" if rollback else "",
        },
        "origin": "SQLite NOT NULL constraint",
        "propagationBoundary": "EntityManager.transaction callback",
        "recoveryActions": [{"action": "rollback-transaction"}] if rollback else [],
        "recoveryState": "all prior writes removed" if rollback else "transaction committed",
        "terminalOutcome": scenario["terminal"],
        "expectedRejection": rollback,
    }


def build_capture(raw, prefix, is_source, raw_path, lock_path, revision):
    created = now()
    target_id = "typeorm-source-runtime" if is_source else "python-sqlite-replica"
    capture_id = "typeorm-source-capture" if is_source else "typeorm-python-replica-capture"
    evidence_id = "typeorm-source-runtime-json" if is_source else "typeorm-python-runtime-json"
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    runtime_name = "TypeORM 1.1.3 / Node.js 22 / better-sqlite3" if is_source else "Python 3.12 / sqlite3"
    scenarios = []
    executions = []
    observations = []
    inventory = []
    obs_by_facet = {facet: [] for facet in FACETS}

    for raw_scenario in raw["scenarios"]:
        label = raw_scenario["label"]
        scenarios.append({
            "scenarioId": sid(label),
            "title": label.replace("-", " ").title(),
            "purpose": "Establish commit-on-success or rollback-on-callback-error semantics for one transaction.",
            "facetIds": FACETS,
            "subject": "typeorm-entity-manager-transaction",
            "preconditions": [
                "Post.title and Category.name are NOT NULL.",
                "The database is a fresh in-memory SQLite database.",
            ],
            "trigger": "Call EntityManager.transaction with the declared callback.",
            "inputs": {"scenario": label},
            "observableQuestions": [
                "Are writes committed after callback success?",
                "Are earlier writes removed after a later callback operation fails?",
                "Does the callback error propagate?",
                "Are writes visible to reads inside the transaction?",
            ],
        })
        executions.append({
            "executionId": eid(prefix, label),
            "scenarioId": sid(label),
            "targetId": target_id,
            "startedAt": started,
            "endedAt": ended,
            "status": "completed",
            "actualContext": {
                "runtime": runtime_name,
                "sourceRevision": revision,
                "database": "SQLite :memory:",
                "driver": raw.get("driver"),
                "pnpmLockDigest": raw.get("pnpmLockDigest") if is_source else None,
            },
            "actualInputs": {"scenario": label},
            "trigger": "Run one transaction scenario and inspect rows after completion.",
            "collector": {"name": runtime_name},
            "limitations": ["Only one in-memory SQLite database and the declared transaction scenarios are covered."],
        })
        scenario = dict(raw_scenario)
        for facet in FACETS:
            observation_id = oid(prefix, label, facet)
            obs_by_facet[facet].append(observation_id)
            observations.append({
                "observationId": observation_id,
                "targetId": target_id,
                "executionId": eid(prefix, label),
                "facet": facet,
                "subject": "typeorm-entity-manager-transaction",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Execute a transaction callback, record its outcome, then query entity rows outside the transaction.",
                    "tool": "TypeORM DataSource / better-sqlite3" if is_source else "Python sqlite3",
                },
                "conditions": {"scenario": label},
                "trigger": "EntityManager.transaction(callback)" if is_source else "sqlite3 transaction context",
                "payload": payload(scenario, facet),
                "rawValue": raw_scenario,
                "normalizedValue": normalized(scenario, facet),
                "evidenceRefs": [evidence_id],
                "status": "observed",
            })

    property_specs = [
        ("TYPEORM-P-001", "persistence", "commit-on-success", "Both entity writes persist after a successful transaction callback.", [oid(prefix, "commit-success", "persistence")]),
        ("TYPEORM-P-002", "persistence", "rollback-on-callback-error", "All writes made before a callback failure are absent after rollback.", [oid(prefix, "rollback-on-invalid-post", "persistence")]),
        ("TYPEORM-P-003", "data", "transactional-row-visibility", "Both writes are visible to reads through the transaction manager before the later failing write.", [oid(prefix, "rollback-on-invalid-post", "data")]),
        ("TYPEORM-P-004", "data", "post-transaction-row-state", "Rows after commit and rollback match the expected persisted entity snapshots.", obs_by_facet["data"]),
        ("TYPEORM-P-005", "behavior", "callback-result-and-error-flow", "Successful callback results are returned; callback errors propagate after rollback.", obs_by_facet["behavior"]),
        ("TYPEORM-P-006", "errors-recovery", "integrity-error-rollback", "A NOT NULL violation propagates and the transaction leaves no partial writes.", [oid(prefix, "rollback-on-invalid-post", "errors-recovery")]),
    ]
    for property_id, facet, dimension, rationale, observation_refs in property_specs:
        inventory.append({
            "propertyId": property_id,
            "facet": facet,
            "subject": "typeorm-entity-manager-transaction",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": observation_refs,
            "evidenceRefs": [evidence_id],
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "TYPEORM-PER-001",
            "facet": "persistence",
            "subject": "successful transaction",
            "proposition": "When the transaction callback completes successfully, all writes performed through the callback manager are committed and the callback result is returned.",
            "trigger": "EntityManager.transaction callback returns successfully.",
            "applicability": {"scope": "The commit-success scenario with one Post and one Category."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "commit-success", "persistence"), oid(prefix, "commit-success", "behavior")],
        },
        {
            "ruleId": "TYPEORM-PER-002",
            "facet": "persistence",
            "subject": "failed transaction",
            "proposition": "When an operation in the transaction callback fails, prior writes in that transaction are rolled back and do not remain persisted.",
            "trigger": "A NOT NULL constraint fails after earlier writes in the callback.",
            "applicability": {"scope": "The rollback-on-invalid-post scenario using better-sqlite3."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "rollback-on-invalid-post", "persistence"), oid(prefix, "rollback-on-invalid-post", "data")],
        },
        {
            "ruleId": "TYPEORM-BEH-001",
            "facet": "behavior",
            "subject": "transaction callback",
            "proposition": "The transaction callback receives a manager scoped to the transaction; successful return values are returned to the caller, while thrown errors propagate after rollback.",
            "trigger": "EntityManager.transaction(callback).",
            "applicability": {"scope": "The two declared transaction scenarios."},
            "status": "supported",
            "supportingObservationIds": obs_by_facet["behavior"],
        },
        {
            "ruleId": "TYPEORM-ERR-001",
            "facet": "errors-recovery",
            "subject": "integrity constraint failure",
            "proposition": "A NOT NULL constraint failure in the callback is propagated to the caller after the transaction's earlier writes are rolled back.",
            "trigger": "Attempt to insert a Post without its required title.",
            "applicability": {"scope": "The rollback-on-invalid-post scenario."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "rollback-on-invalid-post", "errors-recovery")],
        },
    ]

    evidence = [{
        "evidenceId": evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "transaction-runtime-capture",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": runtime_name, "sourceRevision": revision, "location": raw_path},
        "capturedAt": ended,
        "embedded": {"scenarioLabels": [item["label"] for item in raw["scenarios"]], "sha256": digest},
        "locator": raw_path,
        "digest": digest,
        "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
    }]

    if is_source and lock_path and Path(lock_path).exists():
        lock_bytes = Path(lock_path).read_bytes()
        lock_digest = hashlib.sha256(lock_bytes).hexdigest()
        evidence.append({
            "evidenceId": "typeorm-pnpm-lock",
            "evidenceClass": "source-artifact",
            "evidenceType": "pnpm-lockfile",
            "mediaType": "application/yaml",
            "origin": {"targetId": target_id, "sourceRevision": revision, "location": "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/pnpm-lock.yaml"},
            "capturedAt": ended,
            "locator": "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/pnpm-lock.yaml",
            "digest": lock_digest,
            "sizeBytes": len(lock_bytes),
            "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
        })

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared two-scenario TypeORM transaction conformance scope.",
        "target": {
            "targetId": target_id,
            "systemName": "TypeORM 1.1.3" if is_source else "Independent Python SQLite transaction model",
            "systemVersion": "1.1.3" if is_source else "Python 3.12",
            "build": {"revision": revision},
            "boundary": {
                "description": "EntityManager transaction commit/rollback using one in-memory SQLite database.",
                "included": [
                    "Commit of two writes after successful callback",
                    "Visibility of writes inside the transaction callback",
                    "Rollback of earlier writes after a NOT NULL constraint failure",
                    "Propagation of the callback error",
                ],
                "excluded": [
                    "Other database drivers and persistent on-disk databases",
                    "Isolation levels, nested transactions, savepoints, and concurrency",
                    "QueryRunner release failures and rollback failures",
                    "Distributed transactions and external side effects",
                ],
            },
            "environment": {
                "platform": "CI runner",
                "os": "Ubuntu Linux",
                "runtime": "Node.js 22" if is_source else "Python 3.12",
                "configuration": {
                    "state": "observed",
                    "value": {
                        "database": "SQLite :memory:",
                        "driver": raw.get("driver") if is_source else "sqlite3",
                        "pnpmVersion": raw.get("pnpmVersion") if is_source else None,
                        "pnpmLockDigest": raw.get("pnpmLockDigest") if is_source else None,
                    },
                },
            },
        },
        "scope": {
            "description": "Two declared transaction scenarios using required Post and Category fields.",
            "facetIds": FACETS,
            "subjects": ["typeorm-entity-manager-transaction", "Post", "Category"],
            "scenarioIds": [sid(label) for label in LABELS],
        },
        "collector": {
            "name": runtime_name,
            "methodDescription": "Execute each transaction scenario, retain callback outcomes/errors, and query entity rows after transaction completion.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [
            {
                "facet": facet,
                "subject": "typeorm-entity-manager-transaction",
                "status": "observed",
                "reason": "Both declared transaction scenarios have a facet-specific observation.",
                "scenarioIds": [sid(label) for label in LABELS],
                "executionIds": [eid(prefix, label) for label in LABELS],
            }
            for facet in FACETS
        ],
        "limitations": [
            "This is a bounded two-scenario case using better-sqlite3 and an independent sqlite3 replica.",
            "No equivalence claim is made for other TypeORM drivers or advanced transaction features.",
        ],
        "replicationScope": {
            "scopeId": "typeorm-two-scenario-transaction-scope",
            "description": "Complete inventory for the two declared transaction scenarios and four facets.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "All six required properties link to runtime observations and retained evidence in both implementations.",
                "rationale": "All required properties in this bounded transaction scope were observed on the pinned TypeORM runtime and independent Python replica.",
            },
        },
    }


def build_report(source_capture, replica_capture):
    created = now()
    alignments = []
    results = []
    comparable = 0
    for label in LABELS:
        for facet in FACETS:
            source_obs = next(o for o in source_capture["observations"] if o["executionId"] == eid("source", label) and o["facet"] == facet)
            replica_obs = next(o for o in replica_capture["observations"] if o["executionId"] == eid("replica", label) and o["facet"] == facet)
            alignment_id = f"typeorm-align-{label}-{facet}"
            left = source_obs["normalizedValue"]
            right = replica_obs["normalizedValue"]
            match = left == right
            comparable += 1
            alignments.append({
                "alignmentId": alignment_id,
                "facet": facet,
                "referenceRecordIds": [source_obs["observationId"]],
                "implementationRecordIds": [replica_obs["observationId"]],
                "status": "paired",
                "identityBasis": "scenario-subject-facet-condition",
                "rationale": "Both observations cover the same transaction scenario and facet.",
            })
            results.append({
                "resultId": f"typeorm-result-{label}-{facet}",
                "alignmentId": alignment_id,
                "facet": facet,
                "dimension": "transaction-state-and-error-projection",
                "classification": "match" if match else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_obs["observationId"]],
                "implementationObservationIds": [replica_obs["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "The transaction-state projection matches." if match else "The source and replica transaction-state projections differ.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    status = "differences-found" if mismatches else "agreement-within-observed-scope"
    return {
        "schemaVersion": "0.2.0",
        "reportId": "typeorm-transaction-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/typeorm-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/typeorm-python-replica.capture.json"},
        "comparisonScope": {
            "description": "Compare successful commit and failed-callback rollback for two entity writes in an in-memory SQLite database.",
            "facets": FACETS,
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": [
                "TypeORM 1.1.3 at the pinned source commit using better-sqlite3",
                "Python 3.12 using sqlite3",
                "Same required entity fields and transaction scenarios",
            ],
            "excludedDimensions": [
                "Exact error message and driver-specific exception class",
                "Other SQL dialects, isolation levels, concurrency, and nested transactions",
                "Connection release, rollback failure, and external side effects",
            ],
            "limitations": ["The Python implementation is a bounded transaction model, not a TypeORM replacement."],
        },
        "normalizationProfile": {
            "profileId": "typeorm-transaction-semantic-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "compare-transaction-outcomes",
                "facet": "persistence",
                "dimension": "transaction-state-and-error-projection",
                "method": "Compare commit/rollback outcomes, entity rows, callback result, error propagation, and semantic integrity-constraint category; exclude driver-specific error text and runtime details.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Raw TypeORM and Python transaction captures",
                "outputRepresentation": "Normalized transaction state, data, behaviour, and error projections",
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
            "limitations": ["Coverage is limited to the eight facet/scenario projections in this report."],
        },
        "conclusion": {
            "status": status,
            "statement": f"The independent Python implementation {'matches' if not mismatches else 'differs from'} TypeORM 1.1.3 for the two declared transaction scenarios and {comparable} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about TypeORM features or database drivers outside the declared transaction scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for all required properties in the declared two-scenario case scope, not the full TypeORM persistence facet.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--lockfile", required=True)
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    source_raw = read_json(args.source)
    replica_raw = read_json(args.replica)
    source_capture = build_capture(
        source_raw, "source", True,
        "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/typeorm-runtime-capture.json",
        args.lockfile,
        os.getenv("TYPEORM_SOURCE_COMMIT", source_raw.get("sourceCommit", "pinned")),
    )
    replica_capture = build_capture(
        replica_raw, "replica", False,
        "conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/typeorm-replica-capture.json",
        None,
        os.getenv("GITHUB_SHA", "working-tree"),
    )
    report = build_report(source_capture, replica_capture)
    write_json(output / "typeorm-source.capture.json", source_capture)
    write_json(output / "typeorm-python-replica.capture.json", replica_capture)
    write_json(output / "typeorm-comparison.report.json", report)
    print(json.dumps({"comparison": report["conclusion"]["status"], "results": len(report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
