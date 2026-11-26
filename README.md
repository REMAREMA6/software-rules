# Software Rules

A technology-independent specification system for capturing, representing, and comparing software according to its observable behaviour.

## Purpose

Software Rules defines a structured way to describe what a software system does and what can be observed while it runs, independently of the language, framework, platform, or implementation used to build it.

The format is intended to support this workflow:

1. Observe a reference system under documented conditions.
2. Capture its observable rules in a standard, machine-readable format.
3. Build an independent implementation using any suitable technology.
4. Capture the implementation under equivalent conditions.
5. Compare the captures and identify differences.

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

This repository is the home of the format specification, schemas, examples, and comparison rules. The format is under development; individual documents must state their version and maturity.

## Planned specification areas

- Core vocabulary and common observation envelope
- Runtime observation and evidence model
- Separate source-derived rule model
- Facet-specific formats, including interface, behaviour, business rules, data, persistence, APIs, messaging, security, permissions, background work, and errors
- Machine-validation schemas
- Canonicalization and comparison methodology
- Reference examples and conformance fixtures

## Scope boundary

The specification describes what can be established about a running system and records source-derived information separately when necessary. It does not treat source code, design intent, or an unexecuted declaration as proof of runtime behaviour.
