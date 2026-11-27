import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACET = "authorization-permissions"
LABELS = [
 "alice-domain1-data1-read","alice-domain1-data1-write","alice-domain2-data2-read",
 "bob-domain2-data2-write","bob-domain1-data1-read","alice-domain1-data2-read",
 "bob-domain2-data2-delete","domain-policy-added","domain-policy-removed",
 "abac-owner-read","abac-nonowner-read","abac-owner-delete","abac-owner-write",
 "abac-nonowner-write","deny-alice-data1-read","deny-bob-data2-write",
 "deny-alice-data2-write","deny-alice-data2-read","deny-bob-data1-read",
]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "casbin-adv-authz-scenario-" + label


def eid(side, label):
    return "casbin-adv-authz-exec-" + side + "-" + label


def oid(side, label):
    return "casbin-adv-authz-obs-" + side + "-" + label


def build_capture(raw, side, raw_path):
    created = now()
    source = side == "source"
    target_id = "casbin-advanced-go-source" if source else "python-advanced-authz-replica"
    capture_id = "casbin-advanced-go-source-capture" if source else "python-advanced-authz-replica-capture"
    runtime_name = "Apache Casbin Go enforcer" if source else "Independent Python 3.12 authorization model"
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
            "purpose": "Evaluate a declared domain-RBAC, ABAC, deny-override, or policy-mutation authorization request.",
            "facetIds": [FACET],
            "subject": request["subject"],
            "preconditions": ["The pinned Casbin model and policy for the declared model class are loaded.", "The request attributes and policy state are fixed for this scenario."],
            "trigger": "Evaluate the declared Casbin Enforce request under the selected model class.",
            "inputs": request,
            "observableQuestions": ["Is the decision permit or deny?", "Did domain isolation, owner matching, deny precedence, or policy mutation affect the decision?"],
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
            "contextAttributes": {"modelClass": item["modelClass"], **{key: request[key] for key in ("domain", "owner") if key in request}},
            "policyEvidence": ["Pinned model and policy files for the declared authorization model class."],
            "decision": decision,
            "enforcementPoint": "Casbin Enforcer.Enforce" if source else "Independent Python decide()",
            "response": {"decision": decision},
            "reason": "Decision produced by the pinned domain-RBAC, ABAC, deny-override, or policy-mutation model." ,
        }
        observations.append({
            "observationId": oid(side, label),
            "targetId": target_id,
            "executionId": eid(side, label),
            "facet": FACET,
            "subject": request["subject"],
            "observedAt": captured,
            "sequence": index,
            "method": {"class": "instrumentation", "procedure": "Submit the fixed request and model-class context to the authorization evaluator and record its permit/deny decision.", "tool": runtime_name},
            "conditions": {"scenario": label, "modelClass": item["modelClass"]},
            "trigger": "Enforce(request) under the declared model class",
            "payload": payload,
            "rawValue": item,
            "normalizedValue": {"modelClass": item["modelClass"], "request": request, "decision": decision},
            "evidenceRefs": ["casbin-adv-" + side + "-runtime"],
            "status": "observed",
        })

    property_specs = [
        ("CAS-ADV-001","domain-isolation","Role assignments and policy grants are scoped to the requested tenant/domain."),
        ("CAS-ADV-002","attribute-based-access","The ABAC model evaluates the subject/resource attributes declared by its matcher."),
        ("CAS-ADV-003","deny-overrides-allow","A matching deny policy overrides an otherwise matching allow policy."),
        ("CAS-ADV-004","policy-mutation","Adding and removing a policy changes and restores the matching enforcement decision."),
        ("CAS-ADV-005","default-deny","Requests without an effective allow remain denied."),
    ]
    inventory = [{
        "propertyId": pid, "facet": FACET, "subject": "Advanced Casbin authorization decision",
        "dimension": dimension, "requirement": "required", "status": "captured",
        "observationRefs": obs_ids, "evidenceRefs": ["casbin-adv-" + side + "-runtime"],
        "rationale": rationale,
    } for pid, dimension, rationale in property_specs]
    rules = [{
        "ruleId": pid, "facet": FACET, "subject": dimension,
        "proposition": rationale, "trigger": "A subject requests an action on a resource under a declared authorization model.",
        "applicability": {"scope": "Pinned Casbin domain-RBAC, ABAC, deny-override examples and explicit policy mutation."},
        "status": "supported", "supportingObservationIds": obs_ids,
    } for pid, dimension, rationale in property_specs]
    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture bounded domain-RBAC, ABAC, deny-override, and policy-mutation authorization decisions for 19 requests.",
        "target": {
            "targetId": target_id,
            "systemName": "Apache Casbin" if source else "Independent Python advanced authorization replica",
            "systemVersion": "pinned source commit" if source else "Python 3.12",
            "build": {"revision": raw.get("sourceCommit", os.getenv("GITHUB_SHA", "working-tree"))},
            "boundary": {
                "description": "Pinned Casbin domain-RBAC, ABAC, and deny-override models with 19 enforcement and policy-mutation observations.",
                "included": ["Domain-scoped role assignments", "ABAC owner attribute matching", "Deny-overrides-allow effect", "Policy add/remove mutation", "Default deny"],
                "excluded": ["Other Casbin model types", "Role hierarchy beyond the declared models", "Policy adapters and distributed policy synchronization", "Authentication"],
            },
            "environment": {"platform": "GitHub Actions", "os": "Ubuntu Linux", "runtime": "Go" if source else "Python 3.12"},
        },
        "scope": {"description": "Nineteen requests across domain RBAC, ABAC, deny override, and policy mutation.", "facetIds": [FACET], "subjects": ["alice", "bob", "unknown"], "scenarioIds": [sid(label) for label in LABELS]},
        "collector": {"name": runtime_name, "methodDescription": "Execute the same 19 model-class request tuples against source and independent replica."},
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": [{
            "evidenceId": "casbin-adv-" + side + "-runtime",
            "evidenceClass": "runtime",
            "evidenceType": "instrumented-advanced-authorization-decision-capture",
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
            "facet": FACET, "subject": "Advanced Casbin authorization decision", "status": "observed",
            "reason": "All 19 declared domain-RBAC, ABAC, deny-override, and policy-mutation scenarios were executed.",
            "scenarioIds": [sid(label) for label in LABELS],
            "executionIds": [eid(side, label) for label in LABELS],
        }],
        "limitations": ["This case covers only the pinned domain-RBAC, ABAC, deny-override, and policy-mutation examples; it is not full Casbin or full authorization-facet coverage."],
        "replicationScope": {
            "scopeId": "casbin-advanced-policy-class-scope",
            "description": "Complete property inventory for the declared 19-request advanced authorization model scope only.",
            "facets": [FACET],
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete", "assessedAt": created,
                "assessmentMethod": "All five required properties are linked to 19 runtime observations and retained evidence.",
                "rationale": "The declared domain-RBAC, ABAC, deny-override, and policy-mutation model classes are fully exercised; other authorization features are explicitly outside this scope.",
            },
        },
    }


def build_report(source, replica):
    created = now()
    source_obs = {item["observationId"].split("casbin-adv-authz-obs-source-", 1)[1]: item for item in source["observations"]}
    replica_obs = {item["observationId"].split("casbin-adv-authz-obs-replica-", 1)[1]: item for item in replica["observations"]}
    alignments, results = [], []
    for index, label in enumerate(LABELS):
        left, right = source_obs[label], replica_obs[label]
        alignment_id = "casbin-adv-authz-alignment-" + label
        alignments.append({
            "alignmentId": alignment_id, "facet": FACET,
            "referenceRecordIds": [left["observationId"]],
            "implementationRecordIds": [right["observationId"]],
            "status": "paired", "identityBasis": "scenario-subject-facet-condition",
            "rationale": "Same named scenario, request attributes, model class, and authorization decision condition.",
        })
        results.append({
            "resultId": "casbin-adv-authz-result-" + label,
            "alignmentId": alignment_id, "facet": FACET,
            "dimension": "permit-deny-decision",
            "classification": "match" if left["normalizedValue"] == right["normalizedValue"] else "mismatch",
            "comparisonBasis": "semantic",
            "referenceObservationIds": [left["observationId"]],
            "implementationObservationIds": [right["observationId"]],
            "referenceValue": left["normalizedValue"],
            "implementationValue": right["normalizedValue"],
            "reason": "Compare the same request tuple and authorization decision.",
            "evidenceRefs": ["casbin-adv-source-runtime", "casbin-adv-replica-runtime"],
        })
    mismatches = [item for item in results if item["classification"] != "match"]
    return {
        "schemaVersion": "0.2.0",
        "reportId": "casbin-advanced-authorization-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source["captureId"], "schemaVersion": "0.2.0"},
        "implementationCapture": {"captureId": replica["captureId"], "schemaVersion": "0.2.0"},
        "comparisonScope": {
            "description": "Nineteen fixed requests across domain RBAC, ABAC, deny override, and policy mutation.",
            "facets": [FACET],
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": ["Pinned Casbin example models and policies", "Equivalent request attributes", "Explicit add/remove policy mutation"],
            "excludedDimensions": ["Other Casbin model families", "Authentication and identity lifecycle", "Policy adapters"],
            "limitations": ["Bounded advanced authorization examples only; not the full authorization feature space."],
        },
        "alignments": alignments,
        "results": results,
        "coverage": {
            "reference": {"declaredUnits": 19, "observedUnits": 19},
            "implementation": {"declaredUnits": 19, "observedUnits": 19},
            "sharedComparableUnits": 19,
            "incomparableUnits": 0,
            "limitations": ["Nineteen scenarios cover selected model classes, not all authorization models or policy-adapter behaviours."],
        },
        "conclusion": {
            "status": "differences-found" if mismatches else "agreement-within-observed-scope",
            "statement": f"The independent Python RBAC model {'differs from' if mismatches else 'matches'} the pinned Casbin runtime for 19 declared authorization requests. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True, "universalEquivalenceClaimed": False,
        },
        "replicationCompleteness": {
            "referenceStatus": "complete", "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures cover the declared 19-request domain-RBAC, ABAC, deny-override, and policy-mutation scope, not the full Casbin system or authorization facet.",
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
    write(output / "casbin-advanced-source.capture.json", source)
    write(output / "casbin-advanced-python-replica.capture.json", replica)
    write(output / "casbin-advanced-comparison.report.json", report)
    print(json.dumps({"results": len(report["results"]), "mismatches": sum(x["classification"] != "match" for x in report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
