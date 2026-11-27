# Core Principles

**Maturity:** Draft — Software Rules specification 0.3.0.

These principles govern captures, facet specifications, schemas, and comparisons.

1. **Describe observed behaviour, not presumed design.** Source code, diagrams, comments, and contracts may guide investigation but cannot substitute for runtime evidence.
2. **Separate claims from evidence.** A rule is a proposition; an observation is a bounded fact from an execution; evidence is the retained material supporting it. Keep them separately identifiable and linked.
3. **Preserve evidence class.** Runtime observations, source-derived inferences, and declared contracts must remain distinguishable in storage and comparison.
4. **Record the method.** Every observation identifies how it was obtained. External observation, platform/runtime inspection, and runtime instrumentation have different capabilities and limitations.
5. **Make uncertainty explicit.** Unknown, not observed, unavailable, not applicable, conflicting, and inferred are distinct. Missing data is never silently false, zero, empty, absent, or passing.
6. **Preserve raw and normalized information.** Normalization must be documented and must retain a link to the raw value/evidence.
7. **Share the core; type the facets.** Common identity, context, provenance, time, and evidence can be shared. UI geometry, HTTP exchanges, database transactions, and job lifecycles require facet-specific payloads.
8. **Declare scope and coverage.** Identify the target boundary, intended scope, and what was planned, attempted, observed, partially captured, or unavailable.
9. **Preserve ordering and causality where established.** Record time, sequence, and correlation when available. Do not infer causality from temporal proximity alone.
10. **Bound comparison claims.** Compare aligned targets, scenarios, conditions, and dimensions. Report differences and coverage limits. Finite matching captures do not prove universal equivalence.
11. **Separate behavioural identity from implementation identity.** Language, framework, architecture, and deployment details are recorded when relevant, but are not the primary basis of behavioural equivalence.
12. **Protect sensitive data.** Define minimization, redaction, access, retention, and integrity expectations. Redacted data must not appear as an observed empty value.
13. **Version the format.** Keep the common model small and extensible. Facet extensions and schema evolution must be versioned; lossless tools must preserve unknown extension data.
