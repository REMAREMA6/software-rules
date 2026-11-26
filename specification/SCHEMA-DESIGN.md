# Machine-Readable Schema Design

**Status:** Draft — Phase 4  
**Dialect:** JSON Schema Draft 2020-12  
**Scope:** Serialized record structure and validation boundaries for schema line v1.

## 1. Design approach

The schemas formalize the accepted common conceptual envelope while retaining typed facet payloads. The capture is the serialization root; common records are defined separately and facet payloads have one schema per facet. Schema identifiers use versioned URNs so identifiers do not depend on a mutable branch URL.

## 2. Record model

A capture contains target identity, declared scope, collector metadata, coverage, and collections of scenarios, executions, observations, runtime rules, source-derived rules, declared contracts, and evidence artifacts.

- Scenario definitions describe reusable examination intent and expected outcomes.
- Executions describe individual attempts and actual execution context.
- Observations record bounded findings from execution or an explicitly scoped runtime interval.
- Runtime rules are propositions linked to runtime observation IDs.
- Source-derived rules remain separate and require source-artifact evidence references and verification state.
- Declared contracts identify declarations without treating them as runtime facts.
- Evidence artifacts identify runtime evidence, source artifacts, contracts, or supporting context.

## 3. Runtime observation requirements

Every runtime observation requires a method class and concrete procedure, a typed facet payload, and one or more evidence references. It must be associated with an execution or an explicitly identified runtime interval. JSON Schema enforces method class, payload facet, and minimum evidence-reference cardinality. Cross-record existence and execution/target consistency require a separate validator.

## 4. Missingness

A field whose value may be unknown is represented as a field-state object with a state discriminator and an optional value. States include observed, not-observed, unknown, unavailable, not-applicable, redacted, conflicting, and partial. Ordinary optional properties are omitted when not captured; they are not set to null by convention. A facet's actual domain value may itself be null only when that null was observed and the facet meaning permits it.

## 5. Provenance

Runtime observations point to evidence artifacts whose class is runtime. Source-derived rules point to source evidence artifacts and cannot satisfy runtime observation requirements. Declared contracts have their own record type. The schemas structurally distinguish these records; semantic cross-reference checks are required to verify that an evidence reference points to an artifact of the appropriate class.

## 6. Facet payloads

Each facet payload has a fixed `facet` discriminator and facet-specific `kind` discriminator. The schema lists typed dimensions from the corresponding Phase 3 facet specification. Partial payloads are permitted because actual capture coverage can be incomplete; the capture must disclose that incompleteness through coverage and limitations. Additional unrecognized fields are not allowed at the facet root; experimental data may be placed under `extensions`.

## 7. Compatibility and extension policy

This is an initial draft schema line. No backward-compatibility guarantee is made before a stable release. Unknown core properties fail validation to prevent silent misspellings and semantic drift. Explicit `extensions` objects are available for non-core data. Consumers that preserve captures should retain extension values when reading and writing. Any change to required structure or interpretation must be assessed under the repository versioning policy.

## 8. Validation boundary

JSON Schema validates syntax, local structure, enumerations, primitive types, and local cardinality. It does not validate:
- Existence or type correctness of cross-record references.
- Whether an observation actually occurred.
- Whether evidence is genuine, complete, or unaltered.
- Whether a declared contract was issued by the named issuer.
- Whether a source-derived inference is logically sound.
- Whether coverage is truthful.
- Whether two captures match.

Those require conformance procedures and comparison semantics beyond this phase.

## 9. Comparison report boundary

The v1 comparison-report schema defines only report identity, capture references, declared scope, and linked record pairs. It intentionally does not define canonicalization, matching, tolerances, result classifications, or equivalence claims; those belong to Phase 5.
