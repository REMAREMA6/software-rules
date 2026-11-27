# Evidence and Provenance

**Maturity:** Draft — Software Rules specification 0.3.0.

## 1. Three distinct levels

1. **Claim:** a rule proposition about the target.
2. **Finding:** an observation or source-derived inference.
3. **Evidence artifact:** retained material supporting inspection of the finding.

A claim without traceable support remains proposed, not an established runtime rule.

## 2. Runtime observation methods

Every runtime observation identifies one of these classes.

### External black-box observation
Interaction through the exposed system boundary without relying on internal runtime inspection. Examples: UI interaction and visible result, HTTP request/response, message delivery observed at a boundary, or generated output. Hidden state and side effects may remain unknown.

### Platform/runtime inspection
Inspection of actual state/structure exposed by the executing platform. Examples: DOM and computed styles, accessibility tree, native UI hierarchy, runtime process/job state, or authorized database state. Record platform, interface, version, access scope, and fields exposed.

### Runtime instrumentation
Evidence collected by instrumentation attached to or embedded in an executing target. Examples: traces/spans, structured events/logs, metrics, profiling, or instrumented state transitions. Record instrumentation version/configuration, sampling, collection gaps, and known observer effects.

These are all runtime methods when tied to actual execution, but they are not interchangeable. Reading source code, static configuration, or a contract is not a runtime method.

## 3. Source and declaration methods

For source-derived findings, record artifact identity/type/origin, immutable revision where possible, path and location, retrieval time/method, excerpt or digest where permitted, inference and assumptions, and whether reachability/deployment/execution was independently established.

For declared contracts, record issuer, artifact identity/version, scope, and relevant statement. Contracts may be machine-readable but remain declarations until compared with runtime evidence.

## 4. Minimum observation provenance

An observation should be traceable to:
- Capture and capture target.
- Scenario execution, or an explicitly identified runtime interval.
- Subject and facet.
- Method class and concrete tool/procedure.
- Observation time/interval and sequence where available.
- Raw value or durable evidence reference.
- Normalization/transformation, if any.
- Collector/agent identity and version where relevant.
- Known limitations, sampling, redaction, and missing data.

Unknown values remain unknown; do not invent defaults.

## 5. Evidence artifact metadata

The future evidence representation should support:
- Stable evidence ID.
- Evidence type/media type.
- Origin/target/collector/source artifact.
- Capture time.
- Related execution and observation.
- Embedded content or durable locator.
- Integrity metadata (digest/size) where useful.
- Redaction metadata.
- Retention/access status.

A URL alone may not be durable. Preserve essential evidence or use a stable access-controlled reference and integrity metadata.

## 6. Raw values and transformations

Keep raw evidence and normalized values distinct. For each transformation, identify source value, procedure/version, units, precision/rounding, timezone, ordering, and omitted fields. Preserve enough information to reproduce the normalized value. Do not erase meaningful distinctions.

Example: normalize a duration to milliseconds for comparison while retaining the original numeric value and original unit.

## 7. Time, ordering, and correlation

Record event/observation time separately from record creation time. Where relevant, preserve timezone/offset or monotonic-clock basis, sequence, clock source/uncertainty, and correlation identifiers. Wall-clock timestamps from different hosts may not align. Do not infer causality merely from close timestamps.

## 8. Integrity, privacy, and security

Captures may expose credentials, session identifiers, personal data, proprietary content, or sensitive internals. Capture procedures should minimize collection, redact secrets before sharing, record redaction, restrict access, define retention, and preserve integrity metadata.

Redacted/withheld values must not be represented as empty strings, null values, or observed absence. A capture may omit sensitive values, but coverage and limitations must disclose the omission.

## 9. Evidence quality

Do not use one unqualified numeric confidence score as a substitute for evidence description. Record relevant dimensions separately: directness, completeness/sampling, method reliability, correlation to execution, reproducibility, and integrity. No universal scoring formula is prescribed in Phase 2.
