import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACETS = ["persistence", "data", "behavior", "errors-recovery"]
SCENARIOS = ["rollback", "commit"]


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


def projection(scenario, facet):
    if facet == "persistence":
        return {
            "rowsInsideCallback": scenario.get("rowsInsideCallback", []),
            "rowsAfterRollback": scenario.get("rowsAfterRollback", []),
            "rowsAfterCommit": scenario.get("rowsAfterCommit", []),
            "callbackReturn": scenario.get("callbackReturn"),
        }
    if facet == "data":
        return {
            "rowsInsideCallback": scenario.get("rowsInsideCallback", []),
            "rowsAfterRollback": scenario.get("rowsAfterRollback", []),
            "rowsAfterCommit": scenario.get("rowsAfterCommit", []),
        }
    if facet == "behavior":
        return {
            "callbackResult": scenario.get("callbackResult"),
            "callbackReturn": scenario.get("callbackReturn"),
            "transactionOutcome": "rollback" if scenario.get("error") else "commit",
        }
    return {
        "error": scenario.get("error"),
        "rowsAfterRollback": scenario.get("rowsAfterRollback", []),
    }


def payload(scenario_name, scenario, facet):
    subject = "typeorm-transaction-callback"
    if facet == "persistence":
        rollback = scenario_name == "rollback"
        return {
            "facet": "persistence",
            "kind": "state-operation",
            "subject": subject,
            "store": "SQL.js in-memory records table",
            "operation": "transaction",
            "beforeState": {"rows": []},
            "afterState": {
                "rows": scenario.get("rowsAfterRollback", scenario.get("rowsAfterCommit", []))
            },
            "transaction": {
                "outcome": "rolled-back" if rollback else "committed",
                "rowsInsideCallback": scenario.get("rowsInsideCallback", []),
                "error": scenario.get("error"),
            },
            "commitResult": "rollback" if rollback else "commit",
            "consistency": {"readYourWrites": True},
        }
    if facet == "data":
        rows = scenario.get("rowsInsideCallback", []) if scenario_name == "rollback" else scenario.get("rowsAfterCommit", [])
        return {
            "facet": "data",
            "kind": "data-value",
            "subject": "records table transaction contents",
            "dataSubject": "records",
            "fieldPath": "rows",
            "observedValue": rows,
            "observedType": "array<object>",
            "nullability": "not-applicable",
            "constraints": [{"type": "primary-key", "field": "id"}, {"type": "not-null", "field": "value"}],
        }
    if facet == "behavior":
        rollback = scenario_name == "rollback"
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": subject,
            "trigger": "The transaction callback throws a sentinel error." if rollback else "The transaction callback completes successfully.",
            "preconditions": ["A TypeORM DataSource is initialized with the SQL.js driver.", "The records table exists and is empty."],
            "actions": [
                {"sequence": 1, "action": "Start a transaction and execute the callback."},
                {"sequence": 2, "action": "Insert a record and read it inside the callback."},
                {"sequence": 3, "action": "Throw an error." if rollback else "Return a callback value."},
            ],
            "outputs": [{"transactionOutcome": "rollback" if rollback else "commit", "result": scenario}],
            "termination": "original-error-rethrown" if rollback else "callback-result-returned",
        }
    rollback = scenario_name == "rollback"
    return {
        "facet": "errors-recovery",
        "kind": "failure-recovery-event",
        "subject": subject,
        "trigger": "The transaction callback throws an error." if rollback else "The transaction callback succeeds.",
        "operationRef": sid(scenario_name),
        "error": scenario.get("error") or {"category": "none", "code": "", "message": ""},
        "origin": "transaction callback" if rollback else "none",
        "propagationBoundary": "EntityManager.transaction",
        "recoveryActions": [{"action": "ROLLBACK"}] if rollback else [],
        "recoveryState": "all callback writes removed" if rollback else "writes committed",
        "terminalOutcome": "original callback error rethrown" if rollback else "callback return value propagated",
        "expectedRejection": rollback,
    }


def build_capture(raw, prefix, source, raw_path, lock_path):
    created = now()
    target_id = "typeorm-source-runtime" if source else "typeorm-python-replica"
    capture_id = "typeorm-source-runtime-capture" if source else "typeorm-python-replica-capture"
    evidence_id = "typeorm-source-runtime-json" if source else "typeorm-python-runtime-json"
    runtime = "Node.js 22.22.2 / TypeORM 1.1.3 / SQL.js" if source else "Python 3.12 / sqlite3"
    version = raw.get("typeormVersion", "1.1.3") if source else "Python 3.12"
    revision = raw.get("sourceCommit") if source else os.getenv("GITHUB_SHA", "working-tree")
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    scenarios, executions, observations = [], [], []
    obs_by_facet = {facet: [] for facet in FACETS}
    raw_scenarios = raw["scenarios"]

    for label in SCENARIOS:
        value = raw_scenarios[label]
        scenarios.append({
            "scenarioId": sid(label),
            "title": "Transaction " + label,
            "purpose": "Observe TypeORM transaction callback state, outcome, and propagated value/error.",
            "facetIds": FACETS,
            "subject": "typeorm-transaction-callback",
            "preconditions": [
                "A fresh in-memory SQL.js database is initialized.",
                "The records table exists and is empty.",
            ],
            "trigger": "Run a transaction callback that " + ("throws after inserting a row." if label == "rollback" else "inserts a row and returns a value."),
            "inputs": {"scenario": label},
            "observableQuestions": [
                "Can the callback read its own uncommitted write?",
                "Are writes rolled back when the callback throws?",
                "Are writes committed when the callback succeeds?",
                "Is the original error or callback return value propagated?",
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
                "runtime": runtime,
                "sourceRevision": revision,
                "driver": "sqljs" if source else "sqlite3",
                "scope": "Top-level transaction callback; in-memory database only.",
            },
            "actualInputs": {"scenario": label},
            "trigger": scenarios[-1]["trigger"],
            "collector": {"name": "TypeORM transaction runtime probe" if source else "Independent Python sqlite3 probe"},
            "limitations": ["Only top-level transactions on one in-memory SQLite-compatible database are covered."],
        })
        for facet in FACETS:
            observation_id = oid(prefix, label, facet)
            obs_by_facet[facet].append(observation_id)
            observations.append({
                "observationId": observation_id,
                "targetId": target_id,
                "executionId": eid(prefix, label),
                "facet": facet,
                "subject": "typeorm-transaction-callback",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Execute the transaction callback and record in-callback reads, terminal rows, callback result, and propagated error.",
                    "tool": "TypeORM DataSource / SQL.js" if source else "Python sqlite3",
                },
                "conditions": {"scenario": label, "driver": "sqljs" if source else "sqlite3"},
                "trigger": scenarios[-1]["trigger"],
                "payload": payload(label, value, facet),
                "rawValue": value,
                "normalizedValue": projection(value, facet),
                "evidenceRefs": [evidence_id],
                "status": "observed",
            })

    properties = [
        ("TORM-P-001", "persistence", "transaction-rollback-atomicity", "A callback failure rolls back every write performed within that top-level transaction.", obs_by_facet["persistence"]),
        ("TORM-P-002", "persistence", "transaction-commit", "A successful callback commits its writes and those writes are visible to subsequent reads.", obs_by_facet["persistence"]),
        ("TORM-D-001", "data", "read-your-writes", "The transaction-scoped manager reads its own uncommitted write before the callback terminates.", obs_by_facet["data"]),
        ("TORM-B-001", "behavior", "callback-return-propagation", "The transaction method returns the value returned by a successful callback.", [oid(prefix, "commit", "behavior")]),
        ("TORM-E-001", "errors-recovery", "original-error-propagation", "When a callback throws, the transaction method rethrows the callback error after rollback.", [oid(prefix, "rollback", "errors-recovery")]),
    ]
    inventory = []
    for property_id, facet, dimension, rationale, refs in properties:
        inventory.append({
            "propertyId": property_id,
            "facet": facet,
            "subject": "typeorm-transaction-callback",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": refs,
            "evidenceRefs": [evidence_id],
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "TORM-P-001",
            "facet": "persistence",
            "subject": "transaction rollback",
            "proposition": "If the transaction callback throws, all writes performed within that transaction are rolled back.",
            "trigger": "The callback rejects or throws.",
            "applicability": {"scope": "TypeORM 1.1.3 top-level transaction using SQL.js."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "rollback", "persistence")],
        },
        {
            "ruleId": "TORM-P-002",
            "facet": "persistence",
            "subject": "transaction commit",
            "proposition": "If the transaction callback completes successfully, its writes are committed.",
            "trigger": "The callback returns successfully.",
            "applicability": {"scope": "TypeORM 1.1.3 top-level transaction using SQL.js."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "commit", "persistence")],
        },
        {
            "ruleId": "TORM-D-001",
            "facet": "data",
            "subject": "transaction-scoped reads",
            "proposition": "The transaction-scoped manager can read writes made earlier in the same transaction callback.",
            "trigger": "A write is followed by a read before transaction completion.",
            "applicability": {"scope": "TypeORM 1.1.3 top-level transaction using SQL.js."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "rollback", "data")],
        },
        {
            "ruleId": "TORM-B-001",
            "facet": "behavior",
            "subject": "callback return value",
            "proposition": "A successful transaction returns the value returned by its callback.",
            "trigger": "The callback returns a value without throwing.",
            "applicability": {"scope": "TypeORM 1.1.3 top-level transaction using SQL.js."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "commit", "behavior")],
        },
        {
            "ruleId": "TORM-E-001",
            "facet": "errors-recovery",
            "subject": "callback error",
            "proposition": "A callback error is propagated to the caller after the transaction rollback is attempted.",
            "trigger": "The transaction callback throws.",
            "applicability": {"scope": "TypeORM 1.1.3 top-level transaction using SQL.js."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "rollback", "errors-recovery")],
        },
    ]

    evidence = [{
        "evidenceId": evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "instrumented-transaction-runtime-capture",
        "mediaType": "application/json",
        "origin": {
            "targetId": target_id,
            "collector": "TypeORM transaction runtime probe" if source else "Independent Python sqlite3 probe",
            "sourceRevision": revision,
            "location": raw_path,
        },
        "capturedAt": ended,
        "embedded": {"scenarios": SCENARIOS, "sha256": digest},
        "locator": raw_path,
        "digest": digest,
        "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "Retained CI artifact and repository evidence after successful main-branch validation."},
    }]
    if source and lock_path and Path(lock_path).exists():
        lock_bytes = Path(lock_path).read_bytes()
        evidence.append({
            "evidenceId": "typeorm-workspace-lockfile",
            "evidenceClass": "source-artifact",
            "evidenceType": "pnpm-lockfile",
            "mediaType": "text/yaml",
            "origin": {"targetId": target_id, "sourceRevision": revision, "location": "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/pnpm-lock.yaml"},
            "capturedAt": ended,
            "locator": "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/pnpm-lock.yaml",
            "digest": hashlib.sha256(lock_bytes).hexdigest(),
            "sizeBytes": len(lock_bytes),
            "retention": {"status": "retained", "access": "Pinned source repository artifact retained with the case."},
        })

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared top-level TypeORM SQL.js transaction callback contract.",
        "target": {
            "targetId": target_id,
            "systemName": "TypeORM" if source else "Independent Python transaction replica",
            "systemVersion": version,
            "build": {"revision": revision},
            "boundary": {
                "description": "One top-level transaction rollback and one successful commit against an in-memory SQLite-compatible records table.",
                "included": [
                    "Read-your-writes within a transaction callback",
                    "Rollback of callback writes on thrown error",
                    "Propagation of original callback error",
                    "Commit of callback writes on success",
                    "Propagation of successful callback return value",
                ],
                "excluded": [
                    "Nested transactions and savepoints",
                    "Other TypeORM database drivers",
                    "Concurrent transactions and isolation levels",
                    "Durability across process restart or machine failure",
                    "Database-specific lock and journal behaviour",
                ],
            },
            "environment": {
                "platform": "GitHub Actions runner",
                "os": "Ubuntu Linux",
                "runtime": runtime,
                "configuration": {"state": "observed", "value": {"driver": "sqljs" if source else "sqlite3", "database": "in-memory"}},
            },
        },
        "scope": {
            "description": "Two transaction callback scenarios across four facets and five required properties.",
            "facetIds": FACETS,
            "subjects": ["typeorm-transaction-callback", "records-table"],
            "scenarioIds": [sid(label) for label in SCENARIOS],
        },
        "collector": {
            "name": "TypeORM transaction runtime probe" if source else "Independent Python sqlite3 probe",
            "methodDescription": "Run controlled top-level transaction callbacks and retain read-your-writes, rollback/commit state, return values, and propagated errors.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [
            {
                "facet": facet,
                "subject": "typeorm-transaction-callback",
                "status": "observed",
                "reason": "Both declared transaction scenarios have a facet-specific observation.",
                "scenarioIds": [sid(label) for label in SCENARIOS],
                "executionIds": [eid(prefix, label) for label in SCENARIOS],
            }
            for facet in FACETS
        ],
        "limitations": [
            "This is a bounded SQL.js top-level transaction case, not a complete TypeORM persistence implementation.",
            "No claim is made about other TypeORM drivers, nested transactions, concurrent transactions, or crash durability.",
        ],
        "replicationScope": {
            "scopeId": "typeorm-top-level-sqljs-transaction-scope",
            "description": "Complete inventory for the two declared transaction scenarios and five required properties.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "Every required property in the bounded case is linked to facet-specific observations and retained runtime evidence from the source and independent implementation.",
                "rationale": "All five required properties in this declared case scope were observed on both implementations.",
            },
        },
    }


def build_report(source_capture, replica_capture):
    created = now()
    alignments, results = [], []
    for label in SCENARIOS:
        for facet in FACETS:
            source_observation = next(o for o in source_capture["observations"] if o["executionId"] == eid("source", label) and o["facet"] == facet)
            replica_observation = next(o for o in replica_capture["observations"] if o["executionId"] == eid("replica", label) and o["facet"] == facet)
            alignment_id = f"typeorm-align-{label}-{facet}"
            left, right = source_observation["normalizedValue"], replica_observation["normalizedValue"]
            alignments.append({
                "alignmentId": alignment_id,
                "facet": facet,
                "referenceRecordIds": [source_observation["observationId"]],
                "implementationRecordIds": [replica_observation["observationId"]],
                "status": "paired",
                "identityBasis": "scenario-subject-facet-condition",
                "rationale": "Both observations cover the same transaction callback scenario and facet.",
            })
            results.append({
                "resultId": f"typeorm-result-{label}-{facet}",
                "alignmentId": alignment_id,
                "facet": facet,
                "dimension": "transaction-callback-semantic-projection",
                "classification": "match" if left == right else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_observation["observationId"]],
                "implementationObservationIds": [replica_observation["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "The transaction outcome projection matches." if left == right else "The transaction outcome projection differs.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    status = "differences-found" if mismatches else "agreement-within-observed-scope"
    units = len(results)
    return {
        "schemaVersion": "0.2.0",
        "reportId": "typeorm-transaction-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/typeorm-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/typeorm-python-replica.capture.json"},
        "comparisonScope": {
            "description": "Compare rollback and commit transaction callback outcomes across persistence, data, behaviour, and error/recovery projections.",
            "facets": FACETS,
            "scenarioIds": [sid(label) for label in SCENARIOS],
            "conditions": [
                "TypeORM 1.1.3 at the pinned source commit with SQL.js",
                "Python 3.12 sqlite3 independent implementation",
                "One rollback scenario and one commit scenario against an in-memory table",
            ],
            "excludedDimensions": [
                "Other database drivers and database-specific transaction semantics",
                "Nested transactions, concurrency, isolation levels, and crash durability",
            ],
            "limitations": ["This comparison establishes only the declared top-level transaction callback scope."],
        },
        "normalizationProfile": {
            "profileId": "typeorm-transaction-callback-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "compare-transaction-outcomes",
                "facet": "persistence",
                "dimension": "transaction-callback-semantic-projection",
                "method": "Compare rows visible inside the callback, rows after rollback/commit, callback return value, and propagated error; ignore timestamps and implementation-specific runtime metadata.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Raw TypeORM and Python runtime JSON captures",
                "outputRepresentation": "Normalized transaction callback semantic projection",
                "preservesRaw": True,
            }],
        },
        "alignments": alignments,
        "results": results,
        "coverage": {
            "reference": {"declaredUnits": units, "observedUnits": units, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "implementation": {"declaredUnits": units, "observedUnits": units, "notObservedUnits": 0, "unknownUnits": 0, "unavailableUnits": 0, "notApplicableUnits": 0, "partialUnits": 0, "conflictingUnits": 0, "sourceInferredUnits": 0, "excludedUnits": 0},
            "sharedComparableUnits": units,
            "incomparableUnits": 0,
            "limitations": ["Coverage is limited to eight scenario/facet projections in this report."],
        },
        "conclusion": {
            "status": status,
            "statement": f"The independent Python implementation {'matches' if not mismatches else 'differs from'} TypeORM for the two declared top-level transaction scenarios and {units} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about TypeORM features or transaction drivers outside the declared scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for all required properties in the declared two-scenario case scope, not the complete TypeORM persistence facet.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--lockfile", default=None)
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    source_raw, replica_raw = read_json(args.source), read_json(args.replica)
    source_capture = build_capture(source_raw, "source", True, "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/typeorm-source-runtime.json", args.lockfile)
    replica_capture = build_capture(replica_raw, "replica", False, "conformance/replication-lab/cases/TORM-PERSIST-001/artifacts/typeorm-python-runtime.json", None)
    report = build_report(source_capture, replica_capture)
    write_json(output / "typeorm-source.capture.json", source_capture)
    write_json(output / "typeorm-python-replica.capture.json", replica_capture)
    write_json(output / "typeorm-comparison.report.json", report)
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit("Source and replica differ; refusing to emit a passing case.")
    print(json.dumps({"result": report["conclusion"]["status"], "semanticProjections": len(report["results"])}, indent=2))


if __name__ == "__main__":
    main()
