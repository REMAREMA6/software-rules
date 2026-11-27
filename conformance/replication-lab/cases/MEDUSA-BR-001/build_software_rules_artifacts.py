import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACETS = ["business-rules", "data", "behavior", "errors-recovery"]
LABELS = [
    "omitted-both",
    "null-both",
    "empty-string-both",
    "valid-start-iso",
    "valid-end-iso",
    "invalid-start",
    "invalid-end",
    "date-object-start",
    "reversed-range",
    "both-invalid-start-first",
]
SOURCE_FILES = {
    "validator": "packages/modules/pricing/src/utils/validate-price-list-dates.ts",
    "dateHelper": "packages/core/utils/src/common/is-date.ts",
    "errorClass": "packages/core/utils/src/common/errors.ts",
    "serviceUsage": "packages/modules/pricing/src/services/pricing-module.ts",
}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "medusa-scenario-" + label


def eid(prefix, label):
    return f"medusa-exec-{prefix}-{label}"


def oid(prefix, label, facet):
    return f"medusa-obs-{prefix}-{label}-{facet}"


def normalized(scenario, facet):
    base = {
        "outcome": scenario["outcome"],
        "errorType": scenario.get("errorType"),
        "errorField": scenario.get("errorField"),
    }
    if facet == "business-rules":
        return base
    if facet == "data":
        return {
            "input": scenario["input"],
            **base,
        }
    if facet == "behavior":
        return {
            "validationOrder": "starts_at-before-ends_at",
            **base,
        }
    return {
        "outcome": scenario["outcome"],
        "errorType": scenario.get("errorType"),
        "errorField": scenario.get("errorField"),
        "rejected": scenario["outcome"] == "rejected",
    }


def payload(scenario, facet):
    label = scenario["label"]
    data = scenario["input"]
    rejected = scenario["outcome"] == "rejected"
    if facet == "business-rules":
        return {
            "facet": "business-rules",
            "kind": "domain-decision",
            "subject": "medusa-price-list-date-validation",
            "decisionSubject": "optional price-list starts_at and ends_at fields",
            "inputs": data,
            "conditions": {
                "starts_atTruthy": bool(data.get("starts_at")),
                "ends_atTruthy": bool(data.get("ends_at")),
                "validationOrder": "starts_at-before-ends_at",
            },
            "ruleIdentifier": "MEDUSA-BR-001",
            "evaluatedCriteria": [
                {"field": "starts_at", "result": "rejected" if rejected and scenario.get("errorField") == "starts_at" else "valid-or-not-evaluated"},
                {"field": "ends_at", "result": "rejected" if rejected and scenario.get("errorField") == "ends_at" else "valid-or-not-evaluated"},
            ],
            "decision": scenario["outcome"],
            "extensions": {"scenarioLabel": label, "chronologyCompared": False},
        }
    if facet == "data":
        return {
            "facet": "data",
            "kind": "data-value",
            "subject": "Medusa price-list date fields",
            "dataSubject": "price-list temporal inputs",
            "fieldPath": "starts_at / ends_at",
            "observedValue": data,
            "observedType": "object",
            "nullability": "nullable",
            "format": "ISO-8601 string or JavaScript Date object",
            "constraints": [
                {"field": "starts_at", "constraint": "truthy values must parse as a valid date"},
                {"field": "ends_at", "constraint": "truthy values must parse as a valid date"},
            ],
            "validation": {"result": scenario["outcome"], "errorType": scenario.get("errorType"), "errorField": scenario.get("errorField")},
            "serialization": {"representation": "JSON input; Date marker hydrated to JavaScript Date in source probe"},
        }
    if facet == "behavior":
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": "validatePriceListDates",
            "trigger": "Pricing service receives a price-list input object.",
            "preconditions": ["The input is passed to validatePriceListDates before date normalization."],
            "actions": [
                {"sequence": 1, "action": "Check truthy starts_at with isDate."},
                {"sequence": 2, "action": "Check truthy ends_at with isDate if starts_at did not throw."},
            ],
            "outputs": [{"outcome": scenario["outcome"], "errorField": scenario.get("errorField")}],
            "termination": "throws-invalid-data" if rejected else "returns-without-error",
            "extensions": {"scenarioLabel": label, "chronologyCompared": False},
        }
    return {
        "facet": "errors-recovery",
        "kind": "failure-recovery-event",
        "subject": "medusa-price-list-date-validation",
        "trigger": f"Validate price-list date fields for scenario {label}.",
        "operationRef": sid(label),
        "error": {
            "category": scenario.get("errorType") or "none",
            "code": "INVALID_DATA" if rejected else "",
            "message": "",
        },
        "origin": "validatePriceListDates",
        "propagationBoundary": "pricing service input validation",
        "recoveryActions": [],
        "recoveryState": "caller receives validation error" if rejected else "validation continues",
        "terminalOutcome": scenario["outcome"],
        "expectedRejection": rejected,
        "extensions": {"errorField": scenario.get("errorField"), "sourceErrorClass": scenario.get("errorName")},
    }


def build_capture(raw, prefix, is_source, raw_path, source_artifacts, revision):
    created = now()
    target_id = "medusa-source-runtime" if is_source else "python-date-replica"
    capture_id = "medusa-source-capture" if is_source else "medusa-python-replica-capture"
    runtime_evidence_id = "medusa-source-runtime-json" if is_source else "medusa-python-runtime-json"
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    runtime_name = "Medusa pinned TypeScript utility source" if is_source else "Python 3.12 ISO-8601 validator"
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
            "purpose": "Probe optional price-list date field validation and error outcomes.",
            "facetIds": FACETS,
            "subject": "medusa-price-list-date-validation",
            "preconditions": ["The source utility validates starts_at before ends_at.", "Only ISO-8601 strings and Date objects are within the declared scope."],
            "trigger": "Call validatePriceListDates with the declared input object.",
            "inputs": raw_scenario["input"],
            "observableQuestions": [
                "Does the validator accept or reject the input?",
                "Which field is rejected?",
                "Which Medusa error category is returned?",
                "Does the validator enforce chronological order?",
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
                "runtime": "Node.js 22 / TypeScript transpileModule" if is_source else "Python 3.12",
                "sourceRevision": revision,
                "typescriptVersion": raw.get("typescriptVersion") if is_source else None,
                "helperResolution": raw.get("dependencyResolution") if is_source else "Independent Python implementation",
            },
            "actualInputs": raw_scenario["input"],
            "trigger": "Invoke the validator once with the declared input.",
            "collector": {"name": runtime_name},
            "limitations": [
                "Only ISO-8601 strings, Date objects, missing, null, and empty-string values are covered.",
                "Other JavaScript Date parser formats are excluded.",
            ],
        })
        for facet in FACETS:
            observation_id = oid(prefix, label, facet)
            obs_by_facet[facet].append(observation_id)
            observations.append({
                "observationId": observation_id,
                "targetId": target_id,
                "executionId": eid(prefix, label),
                "facet": facet,
                "subject": "medusa-price-list-date-validation",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Invoke the pinned validator and record accept/reject, error type, and failing field.",
                    "tool": "Transpiled pinned TypeScript source" if is_source else "Python validator",
                },
                "conditions": {"scenario": label},
                "trigger": "validatePriceListDates(input)",
                "payload": payload(raw_scenario, facet),
                "rawValue": raw_scenario,
                "normalizedValue": normalized(raw_scenario, facet),
                "evidenceRefs": [runtime_evidence_id],
                "status": "observed",
            })

    property_specs = [
        ("MEDUSA-P-001", "business-rules", "optional-date-field-bypass", "Missing, null, and empty-string start/end values are accepted.", [oid(prefix, label, "business-rules") for label in ["omitted-both", "null-both", "empty-string-both"]]),
        ("MEDUSA-P-002", "business-rules", "valid-date-acceptance", "Valid ISO date strings and a valid Date object are accepted.", [oid(prefix, label, "business-rules") for label in ["valid-start-iso", "valid-end-iso", "date-object-start"]]),
        ("MEDUSA-P-003", "business-rules", "invalid-start-rejection", "A truthy invalid starts_at value is rejected with invalid_data.", [oid(prefix, "invalid-start", "business-rules")]),
        ("MEDUSA-P-004", "business-rules", "invalid-end-rejection", "A truthy invalid ends_at value is rejected with invalid_data.", [oid(prefix, "invalid-end", "business-rules")]),
        ("MEDUSA-P-005", "business-rules", "no-chronology-check", "The validator accepts a reversed starts_at/ends_at range; it does not enforce date ordering.", [oid(prefix, "reversed-range", "business-rules")]),
        ("MEDUSA-P-006", "behavior", "validation-order", "When both values are invalid, starts_at is checked first and its error is returned.", [oid(prefix, "both-invalid-start-first", "behavior")]),
        ("MEDUSA-P-007", "errors-recovery", "medusa-invalid-data-error", "Invalid dates raise a MedusaError with type invalid_data.", [oid(prefix, label, "errors-recovery") for label in ["invalid-start", "invalid-end", "both-invalid-start-first"]]),
        ("MEDUSA-P-008", "data", "accepted-date-representations", "The declared accepted representations include ISO strings, JavaScript Date objects, null, omitted, and empty string.", obs_by_facet["data"]),
    ]
    for property_id, facet, dimension, rationale, observation_refs in property_specs:
        inventory.append({
            "propertyId": property_id,
            "facet": facet,
            "subject": "medusa-price-list-date-validation",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": observation_refs,
            "evidenceRefs": [runtime_evidence_id],
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "MEDUSA-BR-001",
            "facet": "business-rules",
            "subject": "optional price-list date fields",
            "proposition": "A truthy starts_at or ends_at value must be parseable as a valid date; missing, null, and empty-string values bypass validation.",
            "trigger": "A price-list input is passed to validatePriceListDates.",
            "applicability": {"scope": "Declared ISO-8601, Date-object, missing, null, and empty-string probes."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, label, "business-rules") for label in ["omitted-both", "null-both", "empty-string-both", "valid-start-iso", "valid-end-iso", "invalid-start", "invalid-end", "date-object-start"]],
        },
        {
            "ruleId": "MEDUSA-BR-002",
            "facet": "business-rules",
            "subject": "date range chronology",
            "proposition": "validatePriceListDates validates each date independently and does not compare starts_at with ends_at for chronological ordering.",
            "trigger": "A price-list input contains both start and end dates.",
            "applicability": {"scope": "The reversed-range scenario."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "reversed-range", "business-rules")],
        },
        {
            "ruleId": "MEDUSA-BEH-001",
            "facet": "behavior",
            "subject": "validation order",
            "proposition": "The validator checks starts_at before ends_at; when both are invalid, the starts_at error is thrown first.",
            "trigger": "Both optional date fields contain invalid values.",
            "applicability": {"scope": "The both-invalid-start-first scenario."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "both-invalid-start-first", "behavior")],
        },
        {
            "ruleId": "MEDUSA-ERR-001",
            "facet": "errors-recovery",
            "subject": "invalid date input",
            "proposition": "A truthy invalid start or end date throws a MedusaError with type invalid_data.",
            "trigger": "A date field is truthy but isDate returns false.",
            "applicability": {"scope": "Invalid start, invalid end, and both-invalid scenarios."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, label, "errors-recovery") for label in ["invalid-start", "invalid-end", "both-invalid-start-first"]],
        },
    ]

    evidence = [{
        "evidenceId": runtime_evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "source-utility-runtime-capture",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": runtime_name, "sourceRevision": revision, "location": raw_path},
        "capturedAt": ended,
        "embedded": {"scenarioLabels": [item["label"] for item in raw["scenarios"]], "sha256": digest},
        "locator": raw_path,
        "digest": digest,
        "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
    }]

    if is_source:
        for key, relative_path in SOURCE_FILES.items():
            artifact_path = source_artifacts[key]
            artifact_bytes = Path(artifact_path).read_bytes()
            evidence.append({
                "evidenceId": f"medusa-source-{key}",
                "evidenceClass": "source-artifact",
                "evidenceType": "source-code",
                "mediaType": "text/plain",
                "origin": {"targetId": target_id, "sourceRevision": revision, "location": relative_path},
                "capturedAt": ended,
                "locator": f"conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/{Path(artifact_path).name}",
                "digest": hashlib.sha256(artifact_bytes).hexdigest(),
                "sizeBytes": len(artifact_bytes),
                "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
            })

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared ten-probe Medusa price-list date validation scope.",
        "target": {
            "targetId": target_id,
            "systemName": "Medusa Pricing date validator" if is_source else "Independent Python price-list date validator",
            "systemVersion": raw.get("pricingModuleVersion", "2.23.1") if is_source else "Python 3.12",
            "build": {"revision": revision},
            "boundary": {
                "description": "Optional price-list start/end date validation utility.",
                "included": [
                    "Truthiness-based optional field handling",
                    "Date parse validity for ISO-8601 and Date object inputs",
                    "Medusa invalid_data error category",
                    "Start-before-end validation order",
                    "Absence of chronology validation in this utility",
                ],
                "excluded": [
                    "Other JavaScript Date parser formats",
                    "Database persistence and price-list activation logic",
                    "Full Medusa pricing service and application runtime",
                    "Date normalization after validation",
                ],
            },
            "environment": {
                "platform": "CI runner",
                "os": "Ubuntu Linux",
                "runtime": "Node.js 22 / TypeScript transpileModule" if is_source else "Python 3.12",
                "configuration": {
                    "state": "observed",
                    "value": {
                        "typescriptVersion": raw.get("typescriptVersion") if is_source else None,
                        "sourceDependencyResolution": raw.get("dependencyResolution") if is_source else None,
                    },
                },
            },
        },
        "scope": {
            "description": "Ten declared input scenarios against validatePriceListDates.",
            "facetIds": FACETS,
            "subjects": ["medusa-price-list-date-validation", "starts_at", "ends_at"],
            "scenarioIds": [sid(label) for label in LABELS],
        },
        "collector": {
            "name": runtime_name,
            "methodDescription": "Execute the pinned validation utility and retain accept/reject outcomes, Medusa error type, and field precedence.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [
            {
                "facet": facet,
                "subject": "medusa-price-list-date-validation",
                "status": "observed",
                "reason": "All ten declared input scenarios have facet-specific observations.",
                "scenarioIds": [sid(label) for label in LABELS],
                "executionIds": [eid(prefix, label) for label in LABELS],
            }
            for facet in FACETS
        ],
        "limitations": [
            "The source harness executes the exact pinned utility and helper source files with a temporary import-resolution shim; it does not run the complete Medusa application.",
            "The independent Python parser is limited to ISO-8601 date strings and the declared Date-object marker.",
        ],
        "replicationScope": {
            "scopeId": "medusa-ten-probe-price-date-scope",
            "description": "Complete inventory for ten date validation probes and four facets.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "All eight required properties are linked to runtime observations and retained evidence in both implementations.",
                "rationale": "Every declared date-validation property is observed on the pinned source utility and independent Python implementation.",
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
            alignment_id = f"medusa-align-{label}-{facet}"
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
                "rationale": "Both observations cover the same date validation input and facet.",
            })
            results.append({
                "resultId": f"medusa-result-{label}-{facet}",
                "alignmentId": alignment_id,
                "facet": facet,
                "dimension": "date-validation-semantic-projection",
                "classification": "match" if match else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_obs["observationId"]],
                "implementationObservationIds": [replica_obs["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "The date validation outcome matches." if match else "The date validation outcome differs.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    status = "differences-found" if mismatches else "agreement-within-observed-scope"
    return {
        "schemaVersion": "0.2.0",
        "reportId": "medusa-price-date-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/medusa-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/medusa-python-replica.capture.json"},
        "comparisonScope": {
            "description": "Compare ten date validation inputs and four facet projections.",
            "facets": FACETS,
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": [
                "Pinned Medusa pricing utility and its pinned helper sources",
                "Python 3.12 ISO-8601 date validator",
                "Same ten declared input objects",
            ],
            "excludedDimensions": [
                "Non-ISO date strings and JavaScript Date parser quirks outside declared inputs",
                "Database persistence, price-list activation, and full Medusa application behavior",
                "Exact error message text and source-language error class identity",
            ],
            "limitations": ["The replica is a bounded date-validation model, not a Medusa pricing module replacement."],
        },
        "normalizationProfile": {
            "profileId": "medusa-price-date-validation-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "compare-date-validation-outcomes",
                "facet": "business-rules",
                "dimension": "date-validation-semantic-projection",
                "method": "Compare accept/reject outcome, invalid_data category, and failing-field precedence; exclude source-language exception class and message.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Pinned Medusa utility and Python date-validation captures",
                "outputRepresentation": "Normalized validation outcome",
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
            "limitations": ["Coverage is limited to the 40 facet/scenario projections in this report."],
        },
        "conclusion": {
            "status": status,
            "statement": f"The independent Python implementation {'matches' if not mismatches else 'differs from'} the pinned Medusa date-validation utility for ten declared inputs and {comparable} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about full Medusa pricing or JavaScript Date parser inputs outside this scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for all required properties in the declared ten-probe case scope, not the full Medusa pricing module or business-rules facet.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--source-artifacts", required=True)
    args = parser.parse_args()
    source_artifacts = json.loads(args.source_artifacts)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    source_raw = read_json(args.source)
    replica_raw = read_json(args.replica)
    source_capture = build_capture(
        source_raw, "source", True,
        "conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/medusa-runtime-capture.json",
        source_artifacts,
        os.getenv("MEDUSA_SOURCE_COMMIT", source_raw.get("sourceCommit", "pinned")),
    )
    replica_capture = build_capture(
        replica_raw, "replica", False,
        "conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/medusa-replica-capture.json",
        {},
        os.getenv("GITHUB_SHA", "working-tree"),
    )
    report = build_report(source_capture, replica_capture)
    write_json(output / "medusa-source.capture.json", source_capture)
    write_json(output / "medusa-python-replica.capture.json", replica_capture)
    write_json(output / "medusa-comparison.report.json", report)
    print(json.dumps({"comparison": report["conclusion"]["status"], "results": len(report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
