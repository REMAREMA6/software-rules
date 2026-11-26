# Replication Completeness Rule

**Status:** Draft — accepted project requirement; Phase 6 conformance implementation in progress.  
**Applies to:** Capture planning, facet specifications, capture records, conformance, and comparison.

## 1. Purpose

Software Rules exists to express software in a technology- and stack-independent form so that an independent implementation can reproduce the software's relevant properties across different technologies.

A capture that records only convenient, visible, or easily measurable properties does not fulfil that purpose when omitted properties are necessary to reproduce the declared target.

## 2. Normative rule

> **A capture MUST contain a sufficiently complete, technology-independent specification of every in-scope rule and property necessary to reproduce the declared software scope. A capture MUST NOT be treated as replication-sufficient, and a comparison MUST NOT claim faithful replication or equivalence for that scope, while relevant rules or properties remain uncaptured, unknown, unverified, or otherwise unresolved.**

This requirement applies to every in-scope facet and every relevant state, scenario, condition, and environment in the declared replication scope. It is not satisfied by capturing only a sample of convenient properties and comparing those samples.

## 3. Completeness is relative to an explicit replication scope

Completeness cannot be asserted without first defining what is to be reproduced. Every replication-oriented capture MUST declare:

- the target system and boundary;
- the facets and sub-facets included;
- the components, workflows, states, and outputs included;
- relevant scenarios, triggers, inputs, conditions, and environment constraints;
- the required states, variants, and supported viewport/platform conditions, where applicable;
- exclusions and their rationale;
- the evidence and inspection methods used to establish the rules.

The declared scope MUST be detailed enough to determine what information is required to reproduce the target. A narrow scope can be complete for that narrow scope; it MUST NOT be presented as a complete capture of the entire system.

## 4. Capture every relevant property, not merely a convenient subset

For each in-scope facet, the capture process MUST identify and record all properties and rules that can materially affect reproduction.

Examples include, but are not limited to:

- **Interface:** rendered hierarchy; content and text; typography; fonts; colours; backgrounds; borders; shadows; spacing; sizing; alignment; responsive behaviour; geometry; positioning; clipping; stacking; icons; images and other assets; accessibility semantics; focus and interaction states; loading, empty, error, and populated states; and transitions between relevant UI states.
- **Behaviour and functionality:** triggers; available actions; preconditions; state transitions; outputs; side effects; validation; error handling; and relevant ordering or timing.
- **Business rules and data:** decision conditions; calculations; constraints; data shapes; values; relationships; validation; transformations; and relevant defaults.
- **Persistence and integrations:** durable effects; transaction outcomes; external interactions; and relevant failure/recovery behaviour.
- **System and runtime constraints:** configuration, platform assumptions, permissions, resource constraints, and other conditions that materially affect the declared replication scope.

These are examples, not a closed list. Facet specifications MUST define the applicable property inventory and how investigators determine whether a property is relevant.

For an interface, matching a container's dimensions or a few selected CSS values is not sufficient if other visual, structural, semantic, responsive, asset, or state properties affect the rendered screen. The same principle applies to every other facet.

## 5. Unknowns and gaps prevent a completeness claim

The capture MUST preserve the distinction between:

- captured and supported by adequate evidence;
- partially captured;
- not observed;
- unknown;
- unavailable;
- conflicting;
- inferred from source;
- explicitly excluded from the declared scope; and
- not applicable.

An unknown, unobserved, unavailable, conflicting, or source-inferred property MUST NOT silently be treated as captured, verified, absent, or satisfied.

If a relevant property cannot be observed or established, the capture MUST record the gap and its impact. The capture may still be useful, but it MUST be labelled incomplete for any replication scope that depends on that property.

An exclusion only removes a property from the completeness obligation when it is explicitly declared outside the replication scope. Exclusions MUST NOT be used to conceal a known gap while still claiming whole-scope replication.

## 6. Completeness and comparison are separate determinations

A comparison MUST report at least two independent determinations:

1. **Observed agreement:** whether the properties actually captured on both implementations match under aligned conditions.
2. **Replication-scope completeness:** whether the captures cover all required properties and rules in the declared scope with adequate evidence.

A comparison may report that all captured properties match while also reporting that the capture is incomplete. In that case, the result MUST NOT be described as faithful replication, complete equivalence, or proof that the screens/systems are the same.

A mismatch in any required property is a mismatch. A missing or unresolved required property is a coverage gap or inconclusive result, not a match.

## 7. Required reporting

A replication-oriented capture and comparison MUST make it possible to identify:

- the declared replication scope;
- the required property/rule inventory for that scope;
- which required properties were captured and their evidence;
- which were partially captured, unknown, unobserved, unavailable, conflicting, inferred, or excluded;
- the reason for each gap or exclusion;
- the completeness result and the criteria used to reach it; and
- the difference between agreement among captured properties and completeness for the declared scope.

A completeness result MUST be traceable to the inventory and evidence. A percentage alone is insufficient because it can hide a single critical missing rule among many trivial matches.

## 8. Conformance rule

A capture MUST NOT pass a replication-completeness check merely because its schema is valid, its records are internally linked, or its captured properties compare successfully.

Conformance MUST test both structural validity and whether the declared replication scope has a sufficiently complete, evidence-backed property inventory. Automated validation may check required metadata, references, status accounting, and declared coverage; expert review or additional runtime inspection may still be needed to determine whether the inventory itself omits relevant properties.

## 9. Phase 6 Task Board qualification

The Phase 6 Task Board result establishes agreement only for the interface properties and scenarios actually captured. In particular, the matching main-container geometry at 1280×800 does not establish that the complete screens were captured or that the applications are visually identical in every detail or state.

The existing baseline comparison MUST therefore not be used as evidence of replication completeness or full interface equivalence. Phase 7 MUST review and, where needed, revise the capture model, completeness reporting, comparison model, schemas, examples, and conformance checks to enforce this rule.

## 10. Relationship to existing principles

This rule strengthens, rather than replaces:

- explicit scope and coverage;
- evidence and provenance;
- explicit uncertainty and missingness;
- facet-specific property inventories; and
- bounded comparison claims.

Technology independence is the means; faithful reproduction of the declared software scope is the purpose. A format that cannot express the rules necessary for that reproduction is incomplete for that purpose.
