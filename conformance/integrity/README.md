# Cross-record integrity validation

**Maturity:** Draft — Software Rules specification 0.3.0

JSON Schema validates each record's local shape. It cannot establish that IDs referenced by one record exist elsewhere in the same capture. This validator checks that graph-level layer.

## Run

```sh
node conformance/integrity/test.mjs
node conformance/integrity/validate-integrity.mjs path/to/capture.json
```

## Checks

- Duplicate scenario, execution, observation, and evidence IDs.
- Execution → scenario and target references.
- Observation → target, execution, and evidence references.
- Observation target consistency with its linked execution.
- Runtime rule → supporting, qualifying, and contradicting observations.
- Source-derived rule → source evidence.
- Coverage → scenario and execution references.
- Replication property inventory IDs are unique and facets are declared.
- Captured/partial properties link to existing observations and evidence; inventory evidence must also be attached to at least one of that property's linked observations.
- A property marked captured must have at least one observed linked record with runtime-class evidence and must not rely only on an observation explicitly marked partial.
- These checks improve machine-verifiable evidence linkage, but do not prove semantic sufficiency, exhaustive probing, or inventory completeness.
- Completeness status is checked against every required inventory property; a capture cannot claim `complete` while a required property is partial, unobserved, unknown, unavailable, conflicting, or source-inferred.
- This is a structural/reference check only. It does not establish that the linked evidence actually proves the property, that the observation is sufficiently comprehensive, or that the inventory is exhaustive.

This validator checks consistency of the declared inventory. It cannot prove that the inventory itself lists every property needed to reproduce the target; that requires scope review and facet/domain expertise.

## Boundaries

This is not a JSON Schema replacement. Run schema validation first, then this validator. It does not verify evidence authenticity, source revision reachability, semantic alignment between captures, contract correctness, or comparison result correctness. Human review is still required to determine whether evidence actually establishes the proposition and whether the inventory is exhaustive. It also does not infer missing references: unresolved links are errors, not implicit absence.
