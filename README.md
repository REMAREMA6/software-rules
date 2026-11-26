# Software Rules

A technology-independent specification system for capturing, representing, and comparing software according to its observable behaviour.

## Project navigation

- [Project plan and target repository structure](PLAN.md)
- [Progress tracker and handoff context](TRACKER.md)
- [Contribution workflow](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Design decisions](research/DESIGN-DECISIONS.md)
- [Maturity and versioning policy](specification/VERSIONING.md)
- [Standards and prior-art review](research/STANDARDS-REVIEW.md)
- [Research references](research/REFERENCES.md)
- [Core model](specification/CORE.md)
- [Terminology](specification/TERMINOLOGY.md)
- [Core principles](specification/PRINCIPLES.md)
- [Replication completeness rule](specification/REPLICATION-COMPLETENESS.md)
- [Rule classification](specification/RULE-CLASSIFICATION.md)
- [Observation model](specification/OBSERVATION-MODEL.md)
- [Evidence and provenance](specification/EVIDENCE-AND-PROVENANCE.md)
- [Source-derived rules](specification/SOURCE-DERIVED-RULES.md)
- [Facet catalogue](facets/README.md)
- [Facet boundaries](facets/FACET-BOUNDARIES.md)
- [Interface facet](facets/interface/README.md)
- [Schema design](specification/SCHEMA-DESIGN.md)
- [Draft schema index](schemas/v1/README.md)
- [Validation instructions](conformance/validation/README.md)
- [Cross-record integrity validation](conformance/integrity/README.md)
- [Capture-agent guidance](examples/CAPTURE-AGENT-GUIDE.md)
- [Phase 6 Task Board conformance system](examples/task-board/README.md)
- [Empirical reference capture](examples/task-board/captures/reference.capture.json)
- [Empirical independent capture](examples/task-board/captures/independent.capture.json)
- [Deliberate-difference capture](examples/task-board/captures/independent-mutated.capture.json)
- [Comparison specification](comparison/README.md)
- [Comparison model](comparison/COMPARISON-MODEL.md)
- [Normalization rules](comparison/NORMALIZATION.md)
- [Matching rules](comparison/MATCHING-RULES.md)
- [Difference classification](comparison/DIFFERENCE-CLASSIFICATION.md)
- [Coverage and limitations](comparison/COVERAGE-AND-LIMITATIONS.md)

When resuming work in a new chat, read `PLAN.md` and `TRACKER.md` after this introduction. The tracker records the current phase, completed work, blockers, and next action.

## Purpose

Software Rules exists to capture the complete, technology-independent rules needed to reproduce a declared scope of software in an independent implementation, regardless of language, framework, platform, or stack. Runtime observation and comparison provide the evidence and conformance process for that replication purpose; matching a limited set of captured properties is not sufficient.

The format is intended to support this workflow:

1. Observe a reference system under documented conditions.
2. Capture its observable rules in a standard, machine-readable format.
3. Build an independent implementation using any suitable technology.
4. Capture the implementation under equivalent conditions.
5. Compare the captures and identify differences.

## Core model

The common model separates scenario definitions, individual scenario executions, observations, evidence artifacts, and rules. A rule is a scoped claim supported or challenged by observations; it is not the observation itself. The shared model provides common identity, context, provenance, and coverage while each facet retains a typed payload.

See the [observation model](specification/OBSERVATION-MODEL.md) and [core model](specification/CORE.md).

## Rule evidence classes

- **Runtime rules** are established by observing the system while it is running. Each observation must identify its trigger, conditions, result, and supporting evidence.
- **Source-derived rules** are inferred from source code when runtime observation cannot establish a fact. They must remain explicitly labelled as source-derived and must not be presented as verified runtime behaviour.

These classes must remain distinguishable in storage and comparison.

## Design principles

- **Technology independence:** describe observable meaning, not framework-specific implementation.
- **Evidence and provenance:** every captured rule records how it was established.
- **Facet-specific structure:** different parts of software require appropriate typed representations, not one generic collection of prose.
- **Comparable output:** equivalent observations should have canonical representations that can be compared by tools.
- **Explicit uncertainty:** unknown, unobserved, inferred, and verified are distinct states.
- **Bounded claims:** matching captures establish agreement only for the scenarios and conditions actually covered; they do not prove universal equivalence.

## Specification status

This repository is the home of the format specification, schemas, examples, and comparison rules. The format is under development; individual documents must state their version and maturity. See the [maturity and versioning policy](specification/VERSIONING.md).

## Facet specifications

The current draft defines 15 observation facets. See the [facet catalogue](facets/README.md) for the full list and [boundary matrix](facets/FACET-BOUNDARIES.md) for overlap rules. Each facet has its own conceptual payload inventory and a corresponding draft JSON Schema payload under `schemas/v1/facets/`. The schemas formalize structure but are not a stable release or empirical captures.

## Remaining specification work

- [x] Empirical end-to-end captures and conformance examples (Phase 6 complete; see [Task Board test system](examples/task-board/README.md))
- [ ] Final review, versioned release, and maintenance process (Phase 7)

The draft capture schemas, comparison-report schema, structural fixtures, and comparison methodology are available under `schemas/v1/`, `conformance/validation/`, and `comparison/`.

## Scope boundary

The specification describes what can be established about a running system and records source-derived information separately when necessary. It does not treat source code, design intent, or an unexecuted declaration as proof of runtime behaviour.
