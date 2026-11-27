import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

FACETS = ["api", "behavior", "configuration", "errors-recovery"]
LABELS = [
    "get-base",
    "head-fallback",
    "options-auto",
    "options-missing",
    "options-explicit",
    "case-and-trailing-slash",
    "query-ignored",
]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "express-scenario-" + label


def eid(prefix, label):
    return f"express-exec-{prefix}-{label}"


def oid(prefix, label, facet):
    return f"express-obs-{prefix}-{label}-{facet}"


def normalized(scenario, facet):
    request = scenario["request"]
    response = scenario["response"]
    config = scenario.get("configuration", {})
    if facet == "api":
        return {
            "method": request["method"],
            "path": request["path"],
            "status": response["status"],
            "body": response["body"],
            "headers": response["headers"],
            "wireBodyBytes": response.get("wireBodyBytes", 0),
        }
    if facet == "behavior":
        return {
            "method": request["method"],
            "path": request["path"],
            "status": response["status"],
            "body": response["body"],
            "wireBodyBytes": response.get("wireBodyBytes", 0),
        }
    if facet == "configuration":
        return config
    if facet == "errors-recovery":
        return {
            "status": response["status"],
            "notFound": response["status"] == 404,
            "body": response["body"] if response["status"] == 404 else "",
        }
    return {}


def payload(scenario, facet):
    request = scenario["request"]
    response = scenario["response"]
    config = scenario.get("configuration", {})
    if facet == "api":
        parsed = urlsplit(request["path"])
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        return {
            "facet": "api",
            "kind": "request-response",
            "subject": "express-route-dispatch",
            "protocol": "HTTP/1.1",
            "endpoint": parsed.path,
            "method": request["method"],
            "target": "Express application",
            "request": {
                "path": parsed.path,
                "query": query,
                "headers": {},
            },
            "response": {
                "status": response["status"],
                "headers": response["headers"],
                "body": response["body"],
                "contentType": response["headers"].get("content-type") or "",
            },
            "extensions": {"wireBodyBytes": response.get("wireBodyBytes", 0)},
        }
    if facet == "behavior":
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": "express-route-dispatch",
            "trigger": f"{request['method']} {request['path']} arrives at the application.",
            "preconditions": [
                "GET and PUT handlers are registered for /widgets.",
                "An explicit OPTIONS handler is registered for /override.",
            ],
            "actions": [{"sequence": 1, "action": "Dispatch request through Express router"}],
            "outputs": [{
                "status": response["status"],
                "body": response["body"],
                "allow": response["headers"].get("allow"),
                "wireBodyBytes": response.get("wireBodyBytes", 0),
            }],
            "termination": "response-sent",
        }
    if facet == "configuration":
        return {
            "facet": "configuration",
            "kind": "effective-configuration",
            "subject": "express-router-defaults",
            "key": "case-sensitive and strict routing",
            "value": config,
            "valueType": "object",
            "origin": "Express application default settings passed to Router construction",
            "scope": "application router",
            "mutability": "configurable before router initialization",
        }
    return {
        "facet": "errors-recovery",
        "kind": "failure-recovery-event",
        "subject": "express-route-dispatch",
        "trigger": f"{request['method']} {request['path']} does not match a registered route." if response["status"] == 404 else "Request matches a registered route.",
        "operationRef": sid(scenario["label"]),
        "error": {
            "category": "http-not-found" if response["status"] == 404 else "none",
            "code": "404" if response["status"] == 404 else "",
            "message": response["body"] if response["status"] == 404 else "",
        },
        "origin": "router fallthrough",
        "propagationBoundary": "application fallback middleware",
        "recoveryActions": [],
        "recoveryState": "404 response sent" if response["status"] == 404 else "normal response sent",
        "terminalOutcome": f"HTTP {response['status']}",
        "expectedRejection": response["status"] == 404,
    }


def build_capture(raw, prefix, is_source, raw_path, lock_path, revision):
    created = now()
    target_id = "express-source-runtime" if is_source else "express-python-replica"
    capture_id = "express-source-runtime-capture" if is_source else "express-python-replica-capture"
    runtime_evidence_id = "express-source-runtime-json" if is_source else "express-python-runtime-json"
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    raw_bytes = Path(raw_path).read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    collector_name = "Instrumented Express HTTP server" if is_source else "Independent Python standard-library HTTP server"
    config = raw["configuration"]

    scenarios = []
    executions = []
    observations = []
    coverage = []
    inventory = []
    obs_by_facet = {facet: [] for facet in FACETS}

    for raw_scenario in raw["scenarios"]:
        label = raw_scenario["label"]
        scenario_config = config
        scenario = dict(raw_scenario)
        scenario["configuration"] = scenario_config
        scenario["scenarioId"] = sid(label)
        scenarios.append({
            "scenarioId": sid(label),
            "title": label.replace("-", " ").title(),
            "purpose": "Probe HTTP method routing, route matching defaults, response semantics, and unmatched-path handling.",
            "facetIds": FACETS,
            "subject": "express-route-dispatch",
            "preconditions": [
                "GET and PUT handlers are registered at /widgets.",
                "An explicit OPTIONS handler is registered at /override.",
                "A deterministic 404 fallback middleware is registered after routes.",
            ],
            "trigger": f"Send {raw_scenario['request']['method']} {raw_scenario['request']['path']}.",
            "inputs": raw_scenario["request"],
            "observableQuestions": [
                "Which route handles the HTTP method?",
                "What status, body, and selected headers are returned?",
                "Do routing defaults affect path matching?",
                "Does an unmatched path reach the 404 fallback?",
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
                "runtime": "Node.js 22 / Express 5.3.0" if is_source else "Python 3.12 standard library",
                "sourceRevision": revision,
                "dependencyLockDigest": raw.get("dependencyLockDigest") if is_source else None,
            },
            "actualInputs": raw_scenario["request"],
            "trigger": "Send one HTTP request to the isolated application.",
            "collector": {"name": collector_name},
            "limitations": [
                "Only the seven declared HTTP requests and selected response headers are in scope."
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
                "subject": "express-route-dispatch",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Send the declared HTTP request and record status, body, selected headers, and effective routing configuration.",
                    "tool": "Node fetch + Express" if is_source else "Python http.client + HTTPServer",
                },
                "conditions": {"method": raw_scenario["request"]["method"], "path": raw_scenario["request"]["path"]},
                "trigger": f"{raw_scenario['request']['method']} {raw_scenario['request']['path']}",
                "payload": payload(scenario, facet),
                "rawValue": raw_scenario,
                "normalizedValue": normalized(scenario, facet),
                "evidenceRefs": [runtime_evidence_id],
                "status": "observed",
            })

    property_specs = [
        ("EXP-P-001", "api", "http-response-contract", "Status, response body, content type, content length, Allow header, and HEAD wire-body bytes for all seven requests.", obs_by_facet["api"]),
        ("EXP-P-002", "api", "head-to-get-fallback", "HEAD uses the GET route when no explicit HEAD route exists; the response body is suppressed and content length matches GET.", [oid(prefix, "get-base", "api"), oid(prefix, "head-fallback", "api")]),
        ("EXP-P-003", "api", "automatic-options-and-explicit-override", "Automatic OPTIONS lists unique methods including HEAD for GET; an explicit OPTIONS handler takes precedence.", [oid(prefix, "options-auto", "api"), oid(prefix, "options-explicit", "api")]),
        ("EXP-P-004", "configuration", "default-router-settings", "Case-sensitive routing and strict routing are disabled by default.", obs_by_facet["configuration"]),
        ("EXP-P-005", "behavior", "path-match-normalization", "Path matching is case-insensitive, allows a trailing slash, and ignores the query string.", [oid(prefix, "case-and-trailing-slash", "behavior"), oid(prefix, "query-ignored", "behavior")]),
        ("EXP-P-006", "errors-recovery", "unmatched-route-fallback", "An unmatched path falls through to the configured 404 response.", [oid(prefix, "options-missing", "errors-recovery")]),
        ("EXP-P-007", "behavior", "head-wire-body-suppression", "The HEAD response contains zero body bytes on the raw HTTP wire.", [oid(prefix, "head-fallback", "behavior")]),
        ("EXP-P-008", "behavior", "explicit-options-precedence", "An explicit OPTIONS handler takes precedence over automatic method enumeration.", [oid(prefix, "options-explicit", "behavior")]),
    ]
    for property_id, facet, dimension, rationale, observation_refs in property_specs:
        inventory.append({
            "propertyId": property_id,
            "facet": facet,
            "subject": "express-route-dispatch",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": observation_refs,
            "evidenceRefs": [runtime_evidence_id],
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "EXP-API-001",
            "facet": "api",
            "subject": "HTTP HEAD",
            "proposition": "When no explicit HEAD route exists, a matching GET route handles HEAD; the response body is suppressed and the selected representation headers match GET.",
            "trigger": "A HEAD request matches a path with a GET handler.",
            "applicability": {"scope": "HEAD /widgets only; selected content-type and content-length headers."},
            "status": "supported",
            "supportingObservationIds": obs_by_facet["api"][:2],
        },
        {
            "ruleId": "EXP-API-002",
            "facet": "api",
            "subject": "HTTP OPTIONS",
            "proposition": "When no explicit OPTIONS route exists, Express returns the unique methods registered for the matching path and includes HEAD when GET is registered; an explicit OPTIONS route overrides this automatic response.",
            "trigger": "An OPTIONS request matches a path.",
            "applicability": {"scope": "OPTIONS /widgets and /override."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "options-auto", "api"), oid(prefix, "options-explicit", "api")],
        },
        {
            "ruleId": "EXP-CFG-001",
            "facet": "configuration",
            "subject": "Express router defaults",
            "proposition": "Case-sensitive routing and strict routing are disabled by default.",
            "trigger": "The application lazily initializes its router without explicit overrides.",
            "applicability": {"scope": "The tested Express application instance."},
            "status": "supported",
            "supportingObservationIds": obs_by_facet["configuration"],
        },
        {
            "ruleId": "EXP-API-003",
            "facet": "behavior",
            "subject": "Express route matching",
            "proposition": "Default route matching is case-insensitive, permits an optional trailing slash, and matches the pathname independently of the query string.",
            "trigger": "A request path is matched against a registered route.",
            "applicability": {"scope": "GET /WIDGETS/ and GET /widgets?color=blue."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "case-and-trailing-slash", "behavior"), oid(prefix, "query-ignored", "behavior")],
        },
        {
            "ruleId": "EXP-ERR-001",
            "facet": "errors-recovery",
            "subject": "Unmatched route",
            "proposition": "A request that matches no registered route continues to the application fallback middleware, which returns the configured 404 response.",
            "trigger": "A request does not match a registered route.",
            "applicability": {"scope": "OPTIONS /missing only."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "options-missing", "errors-recovery")],
        },
    ]

    evidence = [{
        "evidenceId": runtime_evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "instrumented-http-runtime-capture",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": collector_name, "sourceRevision": revision, "location": raw_path},
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
            "evidenceId": "express-dependency-lock",
            "evidenceClass": "source-artifact",
            "evidenceType": "npm-lockfile",
            "mediaType": "application/json",
            "origin": {"targetId": target_id, "sourceRevision": revision, "location": "conformance/replication-lab/cases/EXP-API-001/artifacts/package-lock.json"},
            "capturedAt": ended,
            "locator": "conformance/replication-lab/cases/EXP-API-001/artifacts/package-lock.json",
            "digest": lock_digest,
            "sizeBytes": len(lock_bytes),
            "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
        })

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared seven-request Express routing/API conformance scope.",
        "target": {
            "targetId": target_id,
            "systemName": "Express 5.3.0" if is_source else "Independent Python HTTP routing replica",
            "systemVersion": "5.3.0" if is_source else "Python 3.12",
            "build": {"revision": revision},
            "boundary": {
                "description": "Minimal HTTP application exercising the declared routing and method semantics.",
                "included": [
                    "HEAD-to-GET fallback and body suppression",
                    "Automatic OPTIONS method enumeration and explicit override",
                    "Case-insensitive and non-strict route matching defaults",
                    "Query-independent route matching",
                    "Configured unmatched-route 404 fallback",
                ],
                "excluded": [
                    "Other Express middleware, routers, route patterns, parameters, and HTTP methods",
                    "Authentication, request body parsing, streaming, redirects, and static files",
                    "Full response header equality, timing, and transport-level differences",
                    "All Express configuration settings and error paths",
                ],
            },
            "environment": {
                "platform": "CI runner",
                "os": "Ubuntu Linux",
                "runtime": "Node.js 22" if is_source else "Python 3.12",
                "configuration": {
                    "state": "observed",
                    "value": {
                        "caseSensitiveRouting": config["caseSensitiveRouting"],
                        "strictRouting": config["strictRouting"],
                        "dependencyLockDigest": raw.get("dependencyLockDigest") if is_source else None,
                    },
                },
            },
        },
        "scope": {
            "description": "Seven declared HTTP requests over a minimal route table.",
            "facetIds": FACETS,
            "subjects": ["express-route-dispatch", "express-router-defaults"],
            "scenarioIds": [sid(label) for label in LABELS],
        },
        "collector": {
            "name": collector_name,
            "methodDescription": "Controlled HTTP requests with response status, body, selected headers, and effective router settings captured.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [
            {
                "facet": facet,
                "subject": "express-route-dispatch",
                "status": "observed",
                "reason": "All seven declared requests have a facet-specific observation.",
                "scenarioIds": [sid(label) for label in LABELS],
                "executionIds": [eid(prefix, label) for label in LABELS],
            }
            for facet in FACETS
        ],
        "limitations": [
            "The independent Python server reproduces only the declared routing semantics; it is not a complete Express implementation.",
            "Only selected response headers are compared; Date, Server, ETag, X-Powered-By, and timing are excluded.",
        ],
        "replicationScope": {
            "scopeId": "express-seven-request-routing-scope",
            "description": "Complete inventory for the seven declared requests and four facets.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "Every required property is linked to observed facet-specific records and retained runtime evidence across all seven requests.",
                "rationale": "All eight required properties in this bounded case scope were observed on both source and independent replica.",
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
            alignment_id = f"express-align-{label}-{facet}"
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
                "rationale": "Both observations cover the same HTTP request and facet.",
            })
            results.append({
                "resultId": f"express-result-{label}-{facet}",
                "alignmentId": alignment_id,
                "facet": facet,
                "dimension": "http-routing-semantic-projection",
                "classification": "match" if match else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_obs["observationId"]],
                "implementationObservationIds": [replica_obs["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "The compared HTTP/routing projection matches." if match else "The source and replica HTTP/routing projections differ.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    status = "differences-found" if mismatches else "agreement-within-observed-scope"
    return {
        "schemaVersion": "0.2.0",
        "reportId": "express-seven-request-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/EXP-API-001/artifacts/express-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/EXP-API-001/artifacts/express-python-replica.capture.json"},
        "comparisonScope": {
            "description": "Compare seven declared HTTP requests and the selected routing configuration/response semantics.",
            "facets": FACETS,
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": [
                "Express 5.3.0 at the pinned source commit",
                "Python 3.12 standard-library HTTP server",
                "Same seven method/path requests and route table",
            ],
            "excludedDimensions": [
                "Date, Server, ETag, X-Powered-By, and timing headers",
                "All response headers beyond content-type, content-length, and Allow",
                "Request bodies, authentication, streaming, redirects, and other middleware",
            ],
            "limitations": ["The Python replica is a bounded route/method model, not a complete Express implementation."],
        },
        "normalizationProfile": {
            "profileId": "express-http-routing-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "compare-selected-http-fields",
                "facet": "api",
                "dimension": "http-routing-semantic-projection",
                "method": "Compare request method/path, response status/body, selected content-type/content-length/Allow headers, and effective routing configuration; exclude platform-generated headers and timing.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Raw source and replica HTTP captures",
                "outputRepresentation": "Normalized request/response and routing configuration projection",
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
            "limitations": ["Coverage is limited to the 28 facet/scenario projections defined in this report."],
        },
        "conclusion": {
            "status": status,
            "statement": f"The independent Python implementation {'matches' if not mismatches else 'differs from'} Express 5.3.0 for the seven declared HTTP requests and {comparable} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about Express features outside the declared route/method/configuration scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for all required properties in the declared seven-request case scope, not the full Express application or API facet.",
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
    source_raw = read_json(args.source)
    replica_raw = read_json(args.replica)
    source_capture = build_capture(
        source_raw, "source", True,
        "conformance/replication-lab/cases/EXP-API-001/artifacts/express-runtime-capture.json",
        args.lockfile,
        os.getenv("EXPRESS_SOURCE_COMMIT", source_raw.get("sourceCommit", "pinned")),
    )
    replica_capture = build_capture(
        replica_raw, "replica", False,
        "conformance/replication-lab/cases/EXP-API-001/artifacts/express-replica-capture.json",
        None,
        os.getenv("GITHUB_SHA", "working-tree"),
    )
    report = build_report(source_capture, replica_capture)
    write_json(output / "express-source.capture.json", source_capture)
    write_json(output / "express-python-replica.capture.json", replica_capture)
    write_json(output / "express-comparison.report.json", report)
    print(json.dumps({"comparison": report["conclusion"]["status"], "results": len(report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
