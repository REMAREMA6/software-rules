# Matching Rules

**Maturity:** Draft — Software Rules specification 0.3.0

## 1. Matching is an evidence-backed alignment, not a similarity guess

A record pair is aligned only when there is a defensible basis for saying the records concern the same intended scenario, subject, and observable dimension. Similar names, array positions, visual proximity, or creation order alone are insufficient.

## 2. Alignment sequence

1. Align scenario definitions by explicit scenario mapping or equivalent trigger, inputs, preconditions, actor, and expected observable questions.
2. Align executions only when scenario intent and materially relevant conditions agree.
3. Align subjects/components within the relevant facet and boundary.
4. Align observations by facet, subject, dimension, state/condition, and temporal relationship.
5. Align rules only when their propositions and applicability conditions are equivalent enough to compare.

Do not align records across different facets unless a documented cross-facet mapping defines the comparison question.

## 3. Preferred identity evidence

Use the strongest available basis in this order, while checking that it is actually stable across the two implementations:

1. Shared domain identifier in the same namespace and lifecycle.
2. Explicit reference-to-implementation mapping supplied and reviewed by a human.
3. Scenario + subject + facet + condition + dimension mapping with evidence.
4. Facet-specific semantic mapping with documented evaluator and rationale.

Capture-local IDs are links within one capture, not portable identity. Names, selectors, paths, and labels may change across implementations and require contextual evidence.

## 4. Cardinality and ambiguity

- One-to-one alignment is preferred but not mandatory.
- One-to-many or many-to-one alignment is allowed only where the facet semantics justify aggregation or decomposition; record all member IDs and the aggregation method.
- If more than one plausible candidate remains, classify alignment as ambiguous; do not choose the most similar candidate silently.
- If no counterpart exists in the declared scope, retain a reference-only or implementation-only alignment. Whether this becomes missing/additional depends on scope and coverage, not simply absence from a file.
- Unmatched records MUST remain visible in the report.

## 5. Conditions and execution context

Scenario names need not be identical, but the intent and relevant inputs must align. Differences in user role, authorization, locale, timezone, feature flags, configuration, initial state, dependency state, platform, viewport, device scale, or workload can invalidate direct comparison if they affect the dimension.

A condition mismatch should produce not-comparable or an explicit separate stratum, not a mismatch attributed to implementation behaviour.

## 6. Runtime/source/contract boundaries

Primary runtime alignment pairs runtime observations with runtime observations. Source-derived rules may be aligned with other source-derived rules as a separate analysis. Declared contracts may be compared with declared contracts. Comparing a runtime observation against a contract is a conformance question and MUST be labelled separately; it is not runtime parity.
