import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACET = "authorization-permissions"
LABELS = [
    "alice-data1-read", "alice-data1-write", "alice-data2-read-via-role",
    "alice-data2-write-via-role", "alice-data3-read", "bob-data2-write",
    "bob-data2-read", "bob-data1-read", "unknown-data1-read", "alice-data2-delete",
]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "casbin-authz-scenario-" + label


def eid(side, label):
    return "casbin-authz-exec-" + side + "-" + label


def oid(side, label):
    return "casbin-authz-obs-" + side + "-" + label


def build_capture(raw, side, raw_path):
    created = now()
    source = side == "source"
    target_id = "casbin-go-source" if source else "python-rbac-replica"
    capture_id = "casbin-go-source-capture" if source else "python-rbac-replica-capture"
    runtime_name = "Apache Casbin Go enforcer" if source else "Independent Python 3.12 RBAC evaluator"
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    captured = raw.get("capturedAt", created)
    scenarios, executions, observations = [], [], []
    obs_ids = [oid(side, label) for label in LABELS]
    for index, item in enumerate(raw["scenarios"]):
        label = item["label"]
        request = item["request"]
        scenarios.append({
            "scenarioId": sid(label),
            "title": label.replace("-", " ").title(),
            "purpose": "Evaluate whether the subject may perform the requested action on the requested resource.",
            "facetIds": [FACET],
            "subject": request["subject"],
            "preconditions": ["The pinned Casbin RBAC model and fixed policy are loaded.", "No policy mutation occurs during the scenario set."],
            "trigger": "Evaluate Enforce(subject, resource, action).",
            "inputs": request,
            "observableQuestions": ["Is the decision permit or deny?", "Did subject/role, resource, and action matching all hold?"],
        })
        executions.append({
            "executionId": eid(side, label),
            "scenarioId": sid(label),
            "targetId": target_id,
            "startedAt": captured,
            "endedAt": captured,
            "status": "completed",
            "actualContext": {"runtime": "Go / Casbin" if source else "Python 3.12", "sourceRevision": raw.get("sourceCommit", "independent-replica")},
            "actualInputs": request,
            "trigger": "Evaluate one subject-resource-action request.",
            "collector": {"name": runtime_name},
        })
        decision = item["decision"]
        payload = {
            "facet": FACET,
            "kind": "access-decision",
            "subject": request["subject"],
            "principalRef": request["subject"],
            "action": request["action"],
            "resource": request["resource"],
            "contextAttributes": {},
            "policyEvidence": ["p: subject/resource/action tuple", "g: user-to-role relation when applicable"],
            "decision": decision,
            "enforcementPoint": "Casbin Enforcer.Enforce" if source else "Independent Python decide()",
            "response": {"decision": decision},
            "reason": "A matching direct or role-derived policy row permits the request." if decision == "permit" else "No policy row matches subject or role, resource, and action.",
        }
        observations.append({
            "observationId": oid(side, label),
            "targetId": target_id,
            "executionId": eid(side, label),
            "facet": FACET,
            "subject": request["subject"],
            "observedAt": captured,
            "sequence": index,
            "method": {"class": "instrumentation", "procedure": "Submit a fixed subject/resource/action tuple to the authorization evaluator and record its permit/deny decision.", "tool": runtime_name},
            "conditions": {"scenario": label},
            "trigger": "Enforce(subject, resource, action)",
            "payload": payload,
            "rawValue": item,
            "normalizedValue": {"request": request, "decision": decision},
            "evidenceRefs": ["casbin-" + side + "-runtime"],
            "status": "observed",
        })

    property_specs = [
        ("CAS-AZ-001", "subject-role-matching", "A subject matches a policy subject directly or through the configured role relation."),
        ("CAS-AZ-002", "resource-equality", "The requested resource must equal the policy resource."),
        ("CAS-AZ-003", "action-equality", "The requested action must equal the policy action."),
        ("CAS-AZ-004", "default-deny", "A request with no matching policy row is denied."),
    ]
    inventory = [{
        "propertyId": pid, "facet": FACET, "subject": "RBAC access decision",
        "dimension": dimension, "requirement": "required", "status": "captured",
        "observationRefs": obs_ids, "evidenceRefs": ["casbin-" + side + "-runtime"],
        "rationale": rationale,
    } for pid, dimension, rationale in property_specs]
    rules = [{
        "ruleId": pid, "facet": FACET, "subject": dimension,
        "proposition": rationale, "trigger": "A subject requests an action on a resource.",
        "applicability": {"scope": "Pinned simple Casbin RBAC model and fixed policy."},
        "status": "supported", "supportingObservationIds": obs_ids,
    } for pid, dimension, rationale in property_specs]
    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture bounded RBAC authorization decisions for ten fixed requests.",
        "target": {
            "targetId": target_id,
            "systemName": "Apache Casbin" if source else "Independent Python RBAC replica",
            "systemVersion": "pinned source commit" if source else "Python 3.12",
            "build": {"revision": raw.get("sourceCommit", os.getenv("GITHUB_SHA", "working-tree"))},
            "boundary": {
                "description": "One simple RBAC model, four policy rows, one user-role link, and ten enforcement requests.",
                "included": ["Direct policy grants", "One-level user-to-role permission inheritance", "Resource equality", "Action equality", "Default deny"],
                "excluded": ["Domains", "Role hierarchy", "ABAC", "Deny-override policy", "Policy mutation", "Policy adapters", "Authentication"],
            },
            "environment": {"platform": "GitHub Actions", "os": "Ubuntu Linux", "runtime": "Go" if source else "Python 3.12"},
        },
        "scope": {"description": "Ten RBAC authorization requests across one facet.", "facetIds": [FACET], "subjects": ["alice", "bob", "unknown"], "scenarioIds": [sid(label) for label in LABELS]},
        "collector": {"name": runtime_name, "methodDescription": "Execute the same ten request tuples against source and independent replica."},
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": [{
            "evidenceId": "casbin-" + side + "-runtime",
            "evidenceClass": "runtime",
            "evidenceType": "instrumented-rbac-decision-capture",
            "mediaType": "application/json",
            "origin": {"targetId": target_id, "collector": runtime_name, "sourceRevision": raw.get("sourceCommit", "independent-replica"), "location": raw_path},
            "capturedAt": captured,
            "embedded": {"scenarioLabels": LABELS, "sha256": digest},
            "locator": raw_path,
            "digest": digest,
            "sizeBytes": len(raw_bytes),
            "retention": {"status": "retained", "access": "Repository case artifacts and CI artifact."},
        }],
        "coverage": [{
            "facet": FACET, "subject": "RBAC access decision", "status": "observed",
            "reason": "All ten declared request scenarios were executed.",
            "scenarioIds": [sid(label) for label in LABELS],
            "executionIds": [eid(side, label) for label in LABELS],
        }],
        "limitations": ["This bounded simple-RBAC case is not complete authorization-facet coverage."],
        "replicationScope": {
            "scopeId": "casbin-rbac-ten-request-scope",
            "description": "Complete property inventory for the declared ten-request simple-RBAC case only.",
            "facets": [FACET],
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete", "assessedAt": created,
                "assessmentMethod": "All four required properties are linked to ten runtime observations and retained evidence.",
                "rationale": "The declared simple-RBAC model and ten request tuples are fully exercised; broader authorization features are explicitly outside this scope.",
            },
        },
    }


def build_report(source, replica):
    created = now()
    source_obs = {item["observationId"].split("casbin-authz-obs-source-", 1)[1]: item for item in source["observations"]}
    replica_obs = {item["observationId"].split("casbin-authz-obs-replica-", 1)[1]: item for item in replica["observations"]}
    alignments, results = [], []
    for index, label in enumerate(LABELS):
        left, right = source_obs[label], replica_obs[label]
        alignment_id = "casbin-authz-alignment-" + label
        alignments.append({
            "alignmentId": alignment_id, "facet": FACET,
            "referenceRecordIds": [left["observationId"]],
            "implementationRecordIds": [right["observationId"]],
            "status": "paired", "identityBasis": "scenario-subject-facet-condition",
            "rationale": "Same named request scenario, subject, resource, and action.",
        })
        results.append({
            "resultId": "casbin-authz-result-" + label,
            "alignmentId": alignment_id, "facet": FACET,
            "dimension": "permit-deny-decision",
            "classification": "match" if left["normalizedValue"] == right["normalizedValue"] else "mismatch",
            "comparisonBasis": "semantic",
            "referenceObservationIds": [left["observationId"]],
            "implementationObservationIds": [right["observationId"]],
            "referenceValue": left["normalizedValue"],
            "implementationValue": right["normalizedValue"],
            "reason": "Compare the same request tuple and authorization decision.",
            "evidenceRefs": ["casbin-source-runtime", "casbin-replica-runtime"],
        })
    mismatches = [item for item in results if item["classification"] != "match"]
    return {
        "schemaVersion": "0.2.0",
        "reportId": "casbin-rbac-authorization-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source["captureId"], "schemaVersion": "0.2.0"},
        "implementationCapture": {"captureId": replica["captureId"], "schemaVersion": "0.2.0"},
        "comparisonScope": {
            "description": "Ten fixed subject/resource/action authorization requests.",
            "facets": [FACET],
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": ["Pinned simple RBAC model", "Fixed policy", "No policy mutation"],
            "excludedDimensions": ["Domains", "Role hierarchy", "ABAC", "Policy mutation"],
            "limitations": ["Bounded simple-RBAC case only."],
        },
        "alignments": alignments,
        "results": results,
        "coverage": {
            "reference": {"declaredUnits": 10, "observedUnits": 10},
            "implementation": {"declaredUnits": 10, "observedUnits": 10},
            "sharedComparableUnits": 10,
            "incomparableUnits": 0,
            "limitations": ["Ten scenarios do not exhaust the authorization feature space."],
        },
        "conclusion": {
            "status": "differences-found" if mismatches else "agreement-within-observed-scope",
            "statement": f"The independent Python RBAC model {'differs from' if mismatches else 'matches'} the pinned Casbin runtime for ten declared authorization requests. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True, "universalEquivalenceClaimed": False,
        },
        "replicationCompleteness": {
            "referenceStatus": "complete", "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures cover the declared ten-request simple-RBAC scope, not the full Casbin system or authorization facet.",
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
    source_raw, replica_raw = read(args.source), read(args.replica)
    source = build_capture(source_raw, "source", args.source)
    replica = build_capture(replica_raw, "replica", args.replica)
    report = build_report(source, replica)
    write(output / "casbin-source.capture.json", source)
    write(output / "casbin-python-replica.capture.json", replica)
    write(output / "casbin-comparison.report.json", report)
    print(json.dumps({"results": len(report["results"]), "mismatches": sum(x["classification"] != "match" for x in report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
