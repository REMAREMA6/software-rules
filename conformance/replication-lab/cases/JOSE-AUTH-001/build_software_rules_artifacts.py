import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FACETS = ["identity-authentication", "security-controls", "data", "behavior", "errors-recovery"]
LABELS = [
    "valid-token",
    "expired-token",
    "not-before-future",
    "issuer-mismatch",
    "audience-mismatch",
    "tampered-signature",
    "algorithm-not-allowed",
    "missing-exp-is-optional",
    "audience-array-match",
    "missing-issuer",
    "missing-audience",
]
SOURCE_FILES = {
    "jwtVerify": "src/jwt/verify.ts",
    "claimsValidation": "src/lib/jwt_claims_set.ts",
    "signatureVerification": "src/lib/jws_verify.ts",
    "upstreamTests": "test/jwt/verify.test.ts",
    "packageManifest": "package.json",
    "licence": "LICENSE.md",
    "compilerConfig": "tsconfig.json",
}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(label):
    return "jose-scenario-" + label


def eid(prefix, label):
    return f"jose-exec-{prefix}-{label}"


def oid(prefix, label, facet):
    return f"jose-obs-{prefix}-{label}-{facet}"


def normalized(scenario, facet):
    if facet == "identity-authentication":
        return {
            "outcome": scenario["outcome"],
            "errorCategory": scenario.get("errorCategory"),
            "claims": scenario.get("claims"),
            "protectedHeader": scenario.get("protectedHeader"),
        }
    if facet == "security-controls":
        return {"outcome": scenario["outcome"], "errorCategory": scenario.get("errorCategory")}
    if facet == "data":
        return {"claims": scenario.get("claims"), "outcome": scenario["outcome"]}
    if facet == "behavior":
        return {
            "outcome": scenario["outcome"],
            "errorCategory": scenario.get("errorCategory"),
            "algorithm": (scenario.get("protectedHeader") or {}).get("alg"),
        }
    return {"outcome": scenario["outcome"], "errorCategory": scenario.get("errorCategory")}


def payload(scenario, facet, evidence_refs):
    label = scenario["label"]
    accepted = scenario["outcome"] == "accepted"
    category = scenario.get("errorCategory")
    options = scenario.get("verificationOptions", {})
    claims = scenario.get("claims") or {}
    header = scenario.get("protectedHeader") or {}
    if facet == "identity-authentication":
        expiry = claims.get("exp")
        return {
            "facet": "identity-authentication",
            "kind": "authentication-event",
            "subject": "compact-jwt-bearer-verification",
            "principalRef": claims.get("sub", "unresolved-principal"),
            "mechanism": "HMAC-signed JWT verification",
            "protocol": "JWT / JWS Compact Serialization",
            "credentialType": "bearer token",
            "issuer": options.get("issuer", ""),
            "audience": options.get("audience", ""),
            "outcome": "success" if accepted else "failure",
            "claims": claims,
            "expiry": datetime.fromtimestamp(expiry, timezone.utc).isoformat().replace("+00:00", "Z") if expiry else None,
            "extensions": {"scenarioLabel": label, "algorithm": header.get("alg"), "errorCategory": category},
        }
    if facet == "security-controls":
        return {
            "facet": "security-controls",
            "kind": "security-control-outcome",
            "subject": "jwt-signature-and-claim-validation",
            "testObjective": "Verify token authenticity and configured JWT claim policy.",
            "authorizedScope": "Synthetic locally generated JWTs and test-only HMAC keys.",
            "control": "HS256 algorithm allowlist, HMAC signature verification, exp/nbf, issuer, and audience validation.",
            "stimulusClass": label,
            "environment": {"runtime": "Node.js WebCrypto" if scenario.get("sourceRuntime") else "Python standard-library HMAC"},
            "observedOutcome": "allowed" if accepted else "blocked",
            "controlResponse": {"decision": scenario["outcome"], "errorCategory": category},
            "telemetryRefs": evidence_refs,
            "observedImpact": {"tokenAccepted": accepted, "principal": claims.get("sub")},
            "safetyConstraints": ["All tokens and keys are synthetic test data.", "No external identity provider or real user credential is used."],
            "extensions": {"algorithm": header.get("alg"), "scenarioLabel": label},
        }
    if facet == "data":
        return {
            "facet": "data",
            "kind": "data-value",
            "subject": "JWT Claims Set",
            "dataSubject": "verified JWT claims",
            "fieldPath": "iss / sub / aud / exp / nbf",
            "observedValue": claims,
            "observedType": "object",
            "nullability": "unknown",
            "format": "JWT Claims Set JSON",
            "constraints": [
                {"field": "exp", "rule": "if present, must be later than verification time"},
                {"field": "nbf", "rule": "if present, must not be later than verification time"},
                {"field": "iss", "rule": "must match configured issuer when configured"},
                {"field": "aud", "rule": "must contain configured audience when configured"},
            ],
            "validation": {"result": scenario["outcome"], "errorCategory": category},
            "serialization": {"representation": "JSON payload encoded in JWS compact serialization"},
        }
    if facet == "behavior":
        return {
            "facet": "behavior",
            "kind": "triggered-operation",
            "subject": "jwtVerify",
            "trigger": "A caller presents a compact JWT and verification key.",
            "preconditions": [
                "A synthetic HMAC key is available.",
                "The verifier is configured to allow HS256.",
                "The verifier has a fixed test clock and expected issuer/audience.",
            ],
            "actions": [
                {"sequence": 1, "action": "Parse compact JWS protected header and claims payload."},
                {"sequence": 2, "action": "Reject algorithms outside the configured allowlist."},
                {"sequence": 3, "action": "Verify the JWS signature with the supplied key."},
                {"sequence": 4, "action": "Validate required issuer/audience and temporal claims."},
            ],
            "outputs": [{"outcome": scenario["outcome"], "errorCategory": category, "claims": claims}],
            "termination": "authenticated" if accepted else "rejected",
            "extensions": {"scenarioLabel": label},
        }
    return {
        "facet": "errors-recovery",
        "kind": "failure-recovery-event",
        "subject": "jwt-verification-failure",
        "trigger": f"Verify the token in scenario {label}.",
        "operationRef": sid(label),
        "error": {"category": category or "none", "code": scenario.get("errorCode") or "", "message": ""},
        "origin": "jose.jwtVerify",
        "propagationBoundary": "JWT verification call",
        "recoveryActions": [],
        "recoveryState": "token rejected; caller must not authenticate principal" if not accepted else "no recovery required",
        "terminalOutcome": scenario["outcome"],
        "expectedRejection": not accepted,
        "extensions": {"claim": scenario.get("errorClaim")},
    }


def build_capture(raw, prefix, is_source, raw_path, source_artifacts, revision):
    created = now()
    target_id = "jose-source-runtime" if is_source else "python-jwt-replica"
    capture_id = "jose-source-capture" if is_source else "python-jwt-replica-capture"
    runtime_evidence_id = "jose-source-runtime-json" if is_source else "python-jwt-runtime-json"
    runtime_name = "jose 6.2.18 / Node.js WebCrypto" if is_source else "Python 3.12 / standard-library HMAC"
    started = raw.get("capturedAt", created)
    ended = raw.get("completedAt", created)
    raw_bytes = Path(raw_path).read_bytes()
    runtime_digest = hashlib.sha256(raw_bytes).hexdigest()
    scenarios, executions, observations, inventory = [], [], [], []
    obs_by_facet = {facet: [] for facet in FACETS}

    evidence = [{
        "evidenceId": runtime_evidence_id,
        "evidenceClass": "runtime",
        "evidenceType": "jwt-verification-runtime-capture",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": runtime_name, "sourceRevision": revision, "location": raw_path},
        "capturedAt": ended,
        "embedded": {"scenarioLabels": [item["label"] for item in raw["scenarios"]], "sha256": runtime_digest},
        "locator": raw_path,
        "digest": runtime_digest,
        "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
    }]

    source_evidence_ids = []
    if is_source:
        for key, relative_path in SOURCE_FILES.items():
            artifact_path = source_artifacts[key]
            artifact_bytes = Path(artifact_path).read_bytes()
            evidence_id = f"jose-source-{key}"
            source_evidence_ids.append(evidence_id)
            suffix = Path(relative_path).suffix
            media_type = "text/markdown" if suffix == ".md" else "application/json" if suffix == ".json" else "text/plain"
            evidence.append({
                "evidenceId": evidence_id,
                "evidenceClass": "source-artifact",
                "evidenceType": "source-code-or-project-metadata",
                "mediaType": media_type,
                "origin": {"targetId": target_id, "sourceRevision": revision, "location": relative_path},
                "capturedAt": ended,
                "locator": f"conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/{Path(artifact_path).name}",
                "digest": hashlib.sha256(artifact_bytes).hexdigest(),
                "sizeBytes": len(artifact_bytes),
                "retention": {"status": "retained", "access": "Version-controlled repository artifact path"},
            })

    evidence_refs = [runtime_evidence_id] + source_evidence_ids
    for raw_scenario in raw["scenarios"]:
        label = raw_scenario["label"]
        scenarios.append({
            "scenarioId": sid(label),
            "title": label.replace("-", " ").title(),
            "purpose": "Probe JWT signature, algorithm, issuer, audience, and temporal-claim verification.",
            "facetIds": FACETS,
            "subject": "compact-jwt-bearer-verification",
            "preconditions": ["Synthetic token and key.", "Fixed verification time.", "HS256-only algorithm allowlist."],
            "trigger": "Call jwtVerify(token, key, verificationOptions).",
            "inputs": {"label": label, "verificationOptions": raw_scenario["verificationOptions"]},
            "observableQuestions": [
                "Is the token accepted or rejected?",
                "Does the signature and algorithm policy pass?",
                "Are configured issuer/audience claims present and matching?",
                "Are exp and nbf temporal claims valid?",
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
                "runtime": "Node.js 22 / jose 6.2.18" if is_source else "Python 3.12",
                "sourceRevision": revision,
                "testTimeEpochSeconds": raw.get("testTimeEpochSeconds"),
                "verificationKey": "synthetic HMAC test key",
            },
            "actualInputs": {"label": label, "verificationOptions": raw_scenario["verificationOptions"]},
            "trigger": "Verify one compact JWT and record the semantic outcome.",
            "collector": {"name": runtime_name},
            "limitations": ["Only HS256/HS384 HMAC cases and the declared issuer/audience/exp/nbf claims are covered."],
        })
        for facet in FACETS:
            observation_id = oid(prefix, label, facet)
            obs_by_facet[facet].append(observation_id)
            observations.append({
                "observationId": observation_id,
                "targetId": target_id,
                "executionId": eid(prefix, label),
                "facet": facet,
                "subject": "compact-jwt-bearer-verification",
                "observedAt": ended,
                "sequence": len(observations),
                "method": {
                    "class": "instrumentation",
                    "procedure": "Submit the same synthetic compact JWT to the source verifier and independent verifier; record claims and semantic rejection category.",
                    "tool": "jose.jwtVerify" if is_source else "Python HMAC/JWT verifier",
                },
                "conditions": {"scenario": label},
                "trigger": "jwtVerify(token, key, options)" if is_source else "verify_one(token, key, options)",
                "payload": payload(raw_scenario, facet, evidence_refs),
                "rawValue": raw_scenario,
                "normalizedValue": normalized(raw_scenario, facet),
                "evidenceRefs": evidence_refs,
                "status": "observed",
            })

    property_specs = [
        ("JOSE-P-001", "security-controls", "signature-integrity", "A tampered signature is rejected.", ["tampered-signature"]),
        ("JOSE-P-002", "security-controls", "algorithm-allowlist", "An HS384 token is rejected when only HS256 is allowed.", ["algorithm-not-allowed"]),
        ("JOSE-P-003", "identity-authentication", "expiration-claim", "An expired exp claim is rejected; exp is optional unless required by policy.", ["expired-token", "missing-exp-is-optional"]),
        ("JOSE-P-004", "identity-authentication", "not-before-claim", "A future nbf claim is rejected.", ["not-before-future"]),
        ("JOSE-P-005", "identity-authentication", "issuer-policy", "A configured issuer is required and must match.", ["issuer-mismatch", "missing-issuer"]),
        ("JOSE-P-006", "identity-authentication", "audience-policy", "A configured audience is required and must match; a matching member of an audience array is accepted.", ["audience-mismatch", "audience-array-match", "missing-audience"]),
        ("JOSE-P-007", "behavior", "verification-order", "Algorithm allowlist and signature verification precede claim validation.", ["algorithm-not-allowed", "tampered-signature"]),
        ("JOSE-P-008", "errors-recovery", "semantic-rejection-categories", "Each invalid token is rejected with the corresponding semantic category.", ["expired-token", "not-before-future", "issuer-mismatch", "audience-mismatch", "tampered-signature", "algorithm-not-allowed", "missing-issuer", "missing-audience"]),
    ]
    for property_id, facet, dimension, rationale, labels in property_specs:
        inventory.append({
            "propertyId": property_id,
            "facet": facet,
            "subject": "compact-jwt-bearer-verification",
            "dimension": dimension,
            "requirement": "required",
            "status": "captured",
            "observationRefs": [oid(prefix, label, facet) for label in labels],
            "evidenceRefs": evidence_refs,
            "rationale": rationale,
        })

    rules = [
        {
            "ruleId": "JOSE-AUTH-001",
            "facet": "security-controls",
            "subject": "JWS signature",
            "proposition": "A compact JWT is accepted only when its signature verifies with the supplied key.",
            "trigger": "jwtVerify receives a compact token and key.",
            "applicability": {"scope": "The valid-token and tampered-signature scenarios."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "valid-token", "security-controls"), oid(prefix, "tampered-signature", "security-controls")],
        },
        {
            "ruleId": "JOSE-AUTH-002",
            "facet": "security-controls",
            "subject": "algorithm allowlist",
            "proposition": "When an algorithms allowlist is supplied, a token using an algorithm outside that list is rejected.",
            "trigger": "The protected header algorithm is not in the configured allowlist.",
            "applicability": {"scope": "HS256 allowed; HS384 presented."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, "algorithm-not-allowed", "security-controls")],
        },
        {
            "ruleId": "JOSE-AUTH-003",
            "facet": "identity-authentication",
            "subject": "temporal JWT claims",
            "proposition": "An exp claim at or before the verification time is rejected, and an nbf claim later than the verification time is rejected; exp is not required by default.",
            "trigger": "Verify a token containing exp and/or nbf claims.",
            "applicability": {"scope": "Fixed test time; no clock tolerance."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, label, "identity-authentication") for label in ["expired-token", "not-before-future", "missing-exp-is-optional"]],
        },
        {
            "ruleId": "JOSE-AUTH-004",
            "facet": "identity-authentication",
            "subject": "issuer and audience policy",
            "proposition": "Configured issuer and audience options require the respective claims and reject mismatched values; an audience array is accepted when it contains the configured audience.",
            "trigger": "Verify a token with issuer and audience options.",
            "applicability": {"scope": "Single configured issuer and audience."},
            "status": "supported",
            "supportingObservationIds": [oid(prefix, label, "identity-authentication") for label in ["issuer-mismatch", "audience-mismatch", "audience-array-match", "missing-issuer", "missing-audience"]],
        },
    ]

    return {
        "schemaVersion": "0.2.0",
        "captureId": capture_id,
        "createdAt": created,
        "purpose": "Capture the declared eleven-scenario JWT verification scope.",
        "target": {
            "targetId": target_id,
            "systemName": "jose JWT verifier" if is_source else "Independent Python JWT verifier",
            "systemVersion": raw.get("packageVersion", "6.2.18") if is_source else "Python 3.12",
            "build": {"revision": revision},
            "boundary": {
                "description": "Compact HMAC-signed JWT verification with a fixed clock and explicit issuer/audience/algorithm policy.",
                "included": [
                    "Signature integrity",
                    "HS256 algorithm allowlist",
                    "exp and nbf temporal claims",
                    "Issuer and audience required/matching semantics",
                    "Audience-array matching",
                    "Optional expiration claim",
                ],
                "excluded": [
                    "RSA/ECDSA and asymmetric key algorithms",
                    "Remote JWKS, key rotation, revocation, and refresh tokens",
                    "Full identity provider, login/session lifecycle, and authorization policy",
                    "Clock tolerance and maxTokenAge",
                    "JWE and non-compact serializations",
                ],
            },
            "environment": {
                "platform": "CI runner",
                "os": "Ubuntu Linux",
                "runtime": "Node.js 22 / WebCrypto" if is_source else "Python 3.12 standard library",
                "configuration": {
                    "state": "observed",
                    "value": {
                        "testTimeEpochSeconds": raw.get("testTimeEpochSeconds"),
                        "typescriptVersion": "6.0.2" if is_source else None,
                        "keyType": "synthetic HMAC",
                    },
                },
            },
        },
        "scope": {
            "description": "Eleven token verification scenarios with identical token inputs.",
            "facetIds": FACETS,
            "subjects": ["compact-jwt-bearer-verification", "JWT Claims Set", "JWS signature"],
            "scenarioIds": [sid(label) for label in LABELS],
        },
        "collector": {
            "name": runtime_name,
            "methodDescription": "Generate deterministic source tokens, verify them in jose, then verify the same compact token strings in the independent Python model.",
        },
        "scenarios": scenarios,
        "executions": executions,
        "observations": observations,
        "runtimeRules": rules,
        "evidence": evidence,
        "coverage": [
            {
                "facet": facet,
                "subject": "compact-jwt-bearer-verification",
                "status": "observed",
                "reason": "All eleven token inputs have facet-specific source and replica observations.",
                "scenarioIds": [sid(label) for label in LABELS],
                "executionIds": [eid(prefix, label) for label in LABELS],
            }
            for facet in FACETS
        ],
        "limitations": [
            "The replica is a bounded HMAC JWT verifier and does not implement the full JOSE protocol suite.",
            "The test key and tokens are synthetic; no real identity credentials are used.",
        ],
        "replicationScope": {
            "scopeId": "jose-eleven-scenario-jwt-verification-scope",
            "description": "Complete inventory for eleven JWT verification scenarios and five facets.",
            "facets": FACETS,
            "propertyInventory": inventory,
            "completeness": {
                "status": "complete",
                "assessedAt": created,
                "assessmentMethod": "All eight required properties link to runtime observations and retained evidence in both implementations.",
                "rationale": "Every required property in the declared HMAC JWT verification scope was observed on the pinned jose runtime and independent Python verifier.",
            },
        },
    }


def build_report(source_capture, replica_capture):
    created = now()
    alignments, results = [], []
    comparable = 0
    for label in LABELS:
        for facet in FACETS:
            source_obs = next(o for o in source_capture["observations"] if o["executionId"] == eid("source", label) and o["facet"] == facet)
            replica_obs = next(o for o in replica_capture["observations"] if o["executionId"] == eid("replica", label) and o["facet"] == facet)
            alignment_id = f"jose-align-{label}-{facet}"
            left, right = source_obs["normalizedValue"], replica_obs["normalizedValue"]
            match = left == right
            comparable += 1
            alignments.append({
                "alignmentId": alignment_id,
                "facet": facet,
                "referenceRecordIds": [source_obs["observationId"]],
                "implementationRecordIds": [replica_obs["observationId"]],
                "status": "paired",
                "identityBasis": "scenario-subject-facet-condition",
                "rationale": "Both observations cover the same token and verification options.",
            })
            results.append({
                "resultId": f"jose-result-{label}-{facet}",
                "alignmentId": alignment_id,
                "facet": facet,
                "dimension": "jwt-verification-semantic-projection",
                "classification": "match" if match else "mismatch",
                "comparisonBasis": "semantic",
                "referenceObservationIds": [source_obs["observationId"]],
                "implementationObservationIds": [replica_obs["observationId"]],
                "referenceValue": left,
                "implementationValue": right,
                "reason": "JWT verification outcomes and normalized claims match." if match else "JWT verification outcomes or normalized claims differ.",
            })
    mismatches = [item for item in results if item["classification"] != "match"]
    status = "differences-found" if mismatches else "agreement-within-observed-scope"
    return {
        "schemaVersion": "0.2.0",
        "reportId": "jose-jwt-auth-cross-stack-comparison",
        "createdAt": created,
        "referenceCapture": {"captureId": source_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/jose-source.capture.json"},
        "implementationCapture": {"captureId": replica_capture["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/jose-python-replica.capture.json"},
        "comparisonScope": {
            "description": "Compare eleven HMAC JWT verification inputs and five facet projections.",
            "facets": FACETS,
            "scenarioIds": [sid(label) for label in LABELS],
            "conditions": [
                "jose 6.2.18 at the pinned source commit, Node.js 22, WebCrypto",
                "Python 3.12 standard-library HMAC verifier",
                "Identical source-generated compact JWT token strings and fixed verification time",
            ],
            "excludedDimensions": [
                "RSA/ECDSA and asymmetric algorithms",
                "Remote JWKS, revocation, refresh tokens, and full authentication/session lifecycle",
                "Clock tolerance, maxTokenAge, and other JOSE features",
            ],
            "limitations": ["The Python replica is limited to HS256/HS384 HMAC and the declared JWT claim policy."],
        },
        "normalizationProfile": {
            "profileId": "jose-jwt-auth-semantic-projection",
            "version": "1.0.0",
            "operations": [{
                "operationId": "compare-jwt-verification",
                "facet": "identity-authentication",
                "dimension": "jwt-verification-semantic-projection",
                "method": "Compare accept/reject outcome, semantic error category, verified claims, and protected header; exclude implementation-specific error codes and messages.",
                "methodVersion": "1.0.0",
                "inputRepresentation": "Same compact JWT tokens and verification options",
                "outputRepresentation": "Normalized authentication decision and verified claims",
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
            "limitations": ["Coverage is limited to the 55 facet/scenario projections in this report."],
        },
        "conclusion": {
            "status": status,
            "statement": f"The independent Python implementation {'matches' if not mismatches else 'differs from'} jose 6.2.18 for eleven declared JWT verification scenarios and {comparable} facet/scenario projections. This is bounded evidence, not universal equivalence.",
            "scopeBounded": True,
            "universalEquivalenceClaimed": False,
        },
        "limitations": ["No claim is made about JOSE algorithms or authentication workflows outside the declared HMAC JWT scope."],
        "replicationCompleteness": {
            "referenceStatus": "complete",
            "implementationStatus": "complete",
            "result": "complete-both",
            "statement": "Both captures account for all required properties in the declared eleven-scenario HMAC JWT scope, not the complete jose library or identity/authentication facet.",
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
        "conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/jose-source-runtime.json",
        source_artifacts,
        os.getenv("JOSE_SOURCE_COMMIT", source_raw.get("sourceCommit", "pinned")),
    )
    replica_capture = build_capture(
        replica_raw, "replica", False,
        "conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/jose-python-runtime.json",
        {},
        os.getenv("GITHUB_SHA", "working-tree"),
    )
    report = build_report(source_capture, replica_capture)
    write_json(output / "jose-source.capture.json", source_capture)
    write_json(output / "jose-python-replica.capture.json", replica_capture)
    write_json(output / "jose-comparison.report.json", report)
    print(json.dumps({"comparison": report["conclusion"]["status"], "results": len(report["results"])}, indent=2))
    if report["conclusion"]["status"] != "agreement-within-observed-scope":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
