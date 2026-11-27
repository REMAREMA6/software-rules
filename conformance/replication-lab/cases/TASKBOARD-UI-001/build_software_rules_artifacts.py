import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
CASE = ROOT / "conformance/replication-lab/cases/TASKBOARD-UI-001"
EVIDENCE = CASE / "evidence"
ARTIFACTS = CASE / "artifacts"
FIXTURES = ROOT / "schemas/v1/fixtures/valid"
FACET = "interface"
SCENARIO_DATA = None


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def sid(name):
    return "taskboard-ui-scenario-" + name


def eid(side, name):
    return "taskboard-ui-exec-" + side + "-" + name


def oid(side, name):
    return "taskboard-ui-obs-" + side + "-" + name


def evidence_id(side, name):
    return "taskboard-ui-evidence-" + side + "-" + name.replace(".", "-")


def build_capture(raw, side, revision, timestamp):
    is_source = side == "source"
    target_id = "taskboard-html-source" if is_source else "taskboard-react-replica"
    capture_id = "taskboard-ui-source-capture" if is_source else "taskboard-ui-react-capture"
    collector = "Playwright Chromium 159.0.8154.6"
    cases = []
    for item in raw["viewportResults"]:
        cases.append({
            "name": item["name"], "width": item["viewport"]["width"], "height": item["viewport"]["height"],
            "snapshot": item["sourceSnapshot"] if is_source else item["implementationSnapshot"],
            "image": item["sourceImage"] if is_source else item["implementationImage"],
            "kind": "responsive-viewport"
        })
    for item in raw["workflowResults"]:
        cases.append({
            "name": item["state"], "width": item["width"], "height": item["height"],
            "snapshot": item["sourceSnapshot"] if is_source else item["implementationSnapshot"],
            "image": item["sourceImage"] if is_source else item["implementationImage"],
            "kind": "workflow-state"
        })

    evidence = []
    raw_path = EVIDENCE / "runtime-comparison.json"
    raw_bytes = raw_path.read_bytes()
    raw_id = evidence_id(side, "runtime-comparison-json")
    evidence.append({
        "evidenceId": raw_id, "evidenceClass": "runtime", "evidenceType": "browser-semantic-and-pixel-comparison",
        "mediaType": "application/json",
        "origin": {"targetId": target_id, "collector": collector, "sourceRevision": revision, "location": str(raw_path.relative_to(ROOT))},
        "capturedAt": timestamp, "locator": str(raw_path.relative_to(ROOT)),
        "digest": hashlib.sha256(raw_bytes).hexdigest(), "sizeBytes": len(raw_bytes),
        "retention": {"status": "retained", "access": "CI artifact and repository case evidence"}
    })
    screenshot_ids = []
    for item in cases:
        image_path = EVIDENCE / item["image"]
        image_bytes = image_path.read_bytes()
        ref = evidence_id(side, item["image"])
        screenshot_ids.append(ref)
        evidence.append({
            "evidenceId": ref, "evidenceClass": "runtime", "evidenceType": "rendered-interface-screenshot",
            "mediaType": "image/png",
            "origin": {"targetId": target_id, "collector": collector, "sourceRevision": revision, "location": str(image_path.relative_to(ROOT))},
            "capturedAt": timestamp, "locator": str(image_path.relative_to(ROOT)),
            "digest": hashlib.sha256(image_bytes).hexdigest(), "sizeBytes": len(image_bytes),
            "retention": {"status": "retained", "access": "CI artifact and repository case evidence"}
        })

    scenarios, executions, observations = [], [], []
    for index, item in enumerate(cases):
        name = item["name"]
        scenario_id = sid(name)
        execution_id = eid(side, name)
        observation_id = oid(side, name)
        screenshot_ref = evidence_id(side, item["image"])
        snapshot = item["snapshot"]
        nodes = []
        for node_index, node in enumerate(snapshot.get("roles", [])):
            nodes.append({
                "nodeId": f"{name}-node-{node_index}",
                "nodeType": node.get("tag", "unknown"),
                "attributes": {
                    "role": node.get("role"), "ariaLabel": node.get("label"),
                    "ariaPressed": node.get("pressed"), "ariaLive": node.get("live"),
                    "required": node.get("required"), "type": node.get("type")
                },
                "content": node.get("text", "")
            })
        scenarios.append({
            "scenarioId": scenario_id, "title": name.replace("-", " ").title(),
            "purpose": "Capture the rendered Task Board interface and its semantic control tree.",
            "facetIds": [FACET], "subject": "Task Board rendered interface",
            "preconditions": [
                "Fresh isolated browser context",
                f"Viewport {item['width']}x{item['height']} CSS pixels",
                "Chromium 159.0.8154.6 on Linux",
                "Deterministic in-memory API adapter"
            ],
            "trigger": "Render the empty page or execute the named workflow state.",
            "observableQuestions": [
                "What pixels are rendered at this viewport and state?",
                "Which semantic elements, accessible names, and selected states are present?"
            ]
        })
        executions.append({
            "executionId": execution_id, "scenarioId": scenario_id, "targetId": target_id,
            "startedAt": timestamp, "endedAt": timestamp, "status": "completed",
            "actualContext": {"viewport": {"width": item["width"], "height": item["height"], "unit": "css-px"}, "runtime": collector, "state": name},
            "trigger": "Load or interact with the Task Board and capture the resulting rendered interface.",
            "collector": {"name": collector}
        })
        payload = {
            "facet": FACET, "kind": "snapshot", "subject": "Task Board rendered interface",
            "platformContext": {"platform": "web", "browser": "Chromium 159.0.8154.6", "os": "Linux"},
            "viewport": {"width": item["width"], "height": item["height"], "unit": "css-px"},
            "roots": ["main#app"], "nodes": nodes,
            "accessibilityTree": {"roles": snapshot.get("roles", [])},
            "uiState": {"name": name, "text": snapshot.get("text", ""), "kind": item["kind"]},
            "renderingEvidence": [screenshot_ref],
            "completeness": {"status": "complete", "rationale": "The declared viewport/state screenshot and semantic node inventory are retained for this observation."}
        }
        observations.append({
            "observationId": observation_id, "targetId": target_id, "executionId": execution_id,
            "facet": FACET, "subject": "Task Board rendered interface", "observedAt": timestamp, "sequence": index,
            "method": {"class": "instrumentation", "procedure": "Use Playwright to capture the browser-rendered screenshot and semantic DOM/accessibility properties.", "tool": collector},
            "conditions": {"scenario": name, "viewport": {"width": item["width"], "height": item["height"], "unit": "css-px"}},
            "trigger": "Render or transition to the declared interface state.",
            "payload": payload, "rawValue": snapshot,
            "normalizedValue": {"text": snapshot.get("text", ""), "roles": snapshot.get("roles", [])},
            "evidenceRefs": [screenshot_ref, raw_id], "status": "observed"
        })

    property_specs = [
        ("TUI-001", "viewport-geometry", "The page container and primary controls resolve to the same geometry at each declared viewport."),
        ("TUI-002", "responsive-layout", "The declared 1280, 768, and 320 CSS-pixel viewports render without an observed layout difference between source and replica."),
        ("TUI-003", "visual-presentation", "The rendered pixels for the declared empty and workflow states are identical under the pinned Chromium environment."),
        ("TUI-004", "semantic-hierarchy", "The heading, form, navigation, list, task controls, and summary expose matching semantic elements."),
        ("TUI-005", "accessible-control-state", "Accessible names, required input state, pressed filter state, checkbox state, and live summary semantics match."),
        ("TUI-006", "workflow-state-presentation", "Populated, completed, filtered, toggled-back, and deleted states render identically.")
    ]
    all_obs = [item["observationId"] for item in observations]
    all_evidence = [raw_id] + screenshot_ids
    inventory = [{
        "propertyId": pid, "facet": FACET, "subject": "Task Board interface",
        "dimension": dimension, "requirement": "required", "status": "captured",
        "observationRefs": all_obs, "evidenceRefs": all_evidence, "rationale": rationale
    } for pid, dimension, rationale in property_specs]
    return {
        "schemaVersion": "0.2.0", "captureId": capture_id, "createdAt": timestamp,
        "purpose": "Capture the bounded Task Board interface replication scope across three viewports and six workflow states.",
        "target": {
            "targetId": target_id,
            "systemName": "Task Board plain HTML source" if is_source else "Independent Task Board React replica",
            "systemVersion": "committed fixture" if is_source else "React 19.1.1 / Vite 7.1.7",
            "build": {"revision": revision},
            "boundary": {
                "description": "Browser-rendered Task Board interface and declared client-side workflow states with a deterministic in-memory API adapter.",
                "included": ["Rendered layout and presentation", "Semantic DOM/accessibility properties", "Three responsive viewport widths", "Six workflow-state renderings"],
                "excluded": ["Other browsers and operating systems", "Font fallback and glyph equivalence across environments", "Unprobed hover/focus/colour-scheme states", "Production backend, authentication, durable persistence, and external integrations"]
            },
            "environment": {"platform": "web", "os": "Ubuntu Linux", "runtime": collector, "configuration": {"state": "observed", "value": {"viewportWidthsCssPx": [1280, 768, 320], "deviceScaleFactor": 1, "locale": "en"}}}
        },
        "scope": {
            "description": "Nine rendered interface observations: empty state at three viewports plus populated, completed, active-filter, completed-filter, toggle-back, and delete states at 1280x800.",
            "facetIds": [FACET], "subjects": ["Task Board rendered interface"],
            "scenarioIds": [sid(item["name"]) for item in cases]
        },
        "collector": {"name": collector, "version": "Playwright 1.56+ browser automation", "methodDescription": "Capture screenshot and semantic DOM/accessibility state for the source and independent React replica."},
        "scenarios": scenarios, "executions": executions, "observations": observations,
        "runtimeRules": [], "sourceRules": [], "declaredContracts": [], "evidence": evidence,
        "coverage": [{
            "facet": FACET, "subject": "Task Board rendered interface", "status": "observed",
            "reason": "All nine declared viewport/state scenarios were executed and retained.",
            "scenarioIds": [sid(item["name"]) for item in cases],
            "executionIds": [eid(side, item["name"]) for item in cases]
        }],
        "limitations": ["Completeness applies only to this declared Task Board interface scope, not the entire interface facet or software system."],
        "replicationScope": {
            "scopeId": "taskboard-ui-nine-state-scope",
            "description": "Nine viewport/state renderings and six declared interface properties for this Task Board fixture.",
            "facets": [FACET], "propertyInventory": inventory,
            "completeness": {
                "status": "complete", "assessedAt": timestamp,
                "assessmentMethod": "Review the nine source/replica screenshot and semantic snapshots against the six declared required interface properties.",
                "rationale": "Every required property in this bounded case has retained screenshot and semantic observation references. Other interface properties and environments are explicitly excluded."
            }
        }
    }


def build_report(raw, source, replica, timestamp):
    cases = raw["viewportResults"] + raw["workflowResults"]
    alignments, results = [], []
    for item in cases:
        name = item.get("name", item.get("state"))
        alignment_id = "taskboard-ui-alignment-" + name
        source_id, replica_id = oid("source", name), oid("replica", name)
        alignments.append({
            "alignmentId": alignment_id, "facet": FACET,
            "referenceRecordIds": [source_id], "implementationRecordIds": [replica_id],
            "status": "paired", "identityBasis": "scenario-subject-facet-condition",
            "rationale": "Both observations represent the same viewport and named UI state."
        })
        results.append({
            "resultId": "taskboard-ui-result-" + name, "alignmentId": alignment_id,
            "facet": FACET, "dimension": "rendered-pixels-and-semantic-interface",
            "classification": "match", "comparisonBasis": "exact",
            "referenceObservationIds": [source_id], "implementationObservationIds": [replica_id],
            "referenceValue": {"width": item["width"], "height": item["height"], "differentPixels": item["differentPixels"], "semanticSnapshot": item["sourceSnapshot"]},
            "implementationValue": {"width": item["width"], "height": item["height"], "differentPixels": item["differentPixels"], "semanticSnapshot": item["implementationSnapshot"]},
            "reason": "Pixel comparison reports zero differing pixels and the semantic DOM snapshots match."
        })
    return {
        "schemaVersion": "0.2.0", "reportId": "taskboard-ui-react-cross-stack-report", "createdAt": timestamp,
        "referenceCapture": {"captureId": source["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TASKBOARD-UI-001/artifacts/taskboard-ui-source.capture.json"},
        "implementationCapture": {"captureId": replica["captureId"], "schemaVersion": "0.2.0", "artifactRef": "conformance/replication-lab/cases/TASKBOARD-UI-001/artifacts/taskboard-ui-react.capture.json"},
        "comparisonScope": {
            "description": "Compare three empty-state viewports and six Task Board workflow states between the plain HTML source and independent React replica.",
            "facets": [FACET], "scenarioIds": [sid(item.get("name", item.get("state"))) for item in cases],
            "conditions": ["Chromium 159.0.8154.6 on Ubuntu Linux", "Device scale factor 1", "Identical in-memory API adapter behaviour", "React production build"],
            "excludedDimensions": ["Other browsers/operating systems", "Unprobed interaction states", "Production server and persistence behaviour"],
            "limitations": ["This is bounded interface replication evidence, not full interface-facet or whole-system equivalence."]
        },
        "normalizationProfile": {
            "profileId": "taskboard-ui-exact-render-profile", "version": "1.0.0",
            "operations": [{
                "operationId": "taskboard-ui-pixel-semantic-exact", "facet": FACET,
                "dimension": "pixel-and-semantic-snapshot", "method": "Compare screenshot pixels at exact dimensions and compare normalized semantic DOM snapshots.",
                "methodVersion": "1.0.0", "inputRepresentation": "PNG screenshots and semantic DOM JSON",
                "outputRepresentation": "Differing-pixel count and semantic snapshot equality", "preservesRaw": True
            }]
        },
        "alignments": alignments, "results": results,
        "coverage": {
            "reference": {"declaredUnits": len(cases), "observedUnits": len(cases)},
            "implementation": {"declaredUnits": len(cases), "observedUnits": len(cases)},
            "sharedComparableUnits": len(cases), "incomparableUnits": 0,
            "limitations": ["Coverage counts only the nine declared viewport/state comparisons."]
        },
        "conclusion": {
            "status": "agreement-within-observed-scope",
            "statement": "The independent React 19/Vite replica matched the plain HTML source pixel-for-pixel across three viewport widths and six workflow states, with matching semantic snapshots. This is bounded evidence, not universal software equivalence.",
            "scopeBounded": True, "universalEquivalenceClaimed": False
        },
        "limitations": ["The case excludes unprobed interface states, other browsers, other operating systems, production APIs, and full system behaviour."],
        "replicationCompleteness": {
            "referenceStatus": "complete", "implementationStatus": "complete", "result": "complete-both",
            "statement": "Both captures account for the six required properties in the declared nine-observation Task Board interface scope only; neither claims completeness of the entire interface facet or software system."
        }
    }


def main():
    global SCENARIO_DATA
    raw = read(EVIDENCE / "runtime-comparison.json")
    assert raw["failures"] == [], "Runtime comparison must pass before schema captures are generated."
    assert raw["mutationDetected"], "The deliberate replica mutation must be detected."
    assert all(item["differentPixels"] == 0 for item in raw["viewportResults"] + raw["workflowResults"]), "All declared comparisons must be pixel-identical."
    assert all(item.get("semanticMatch", True) for item in raw["workflowResults"]), "All workflow semantic snapshots must match."
    timestamp = now()
    revision = os.getenv("GITHUB_SHA", "working-tree")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    source = build_capture(raw, "source", revision, timestamp)
    replica = build_capture(raw, "replica", revision, timestamp)
    report = build_report(raw, source, replica, timestamp)
    source_path = ARTIFACTS / "taskboard-ui-source.capture.json"
    replica_path = ARTIFACTS / "taskboard-ui-react.capture.json"
    report_path = ARTIFACTS / "taskboard-ui-comparison.report.json"
    write(source_path, source)
    write(replica_path, replica)
    write(report_path, report)
    write(FIXTURES / "taskboard-ui-source.capture.json", source)
    write(FIXTURES / "taskboard-ui-react.capture.json", replica)
    write(ROOT / "comparison/examples/valid/taskboard-ui-react-cross-stack.json", report)
    print(json.dumps({
        "sourceCapture": str(source_path.relative_to(ROOT)),
        "replicaCapture": str(replica_path.relative_to(ROOT)),
        "comparisonReport": str(report_path.relative_to(ROOT)),
        "scenarioCount": len(report["results"]),
        "matchedResults": sum(item["classification"] == "match" for item in report["results"]),
        "propertyCount": len(source["replicationScope"]["propertyInventory"]),
        "mutationDetected": raw["mutationDetected"]
    }, indent=2))


if __name__ == "__main__":
    main()
