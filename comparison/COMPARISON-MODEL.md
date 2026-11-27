# Comparison Model

**Maturity:** Draft — Software Rules specification 0.3.0  
**Normative terms:** MUST, MUST NOT, SHOULD, MAY are used in their ordinary specification sense.

## 1. Purpose

A comparison evaluates two independently produced captures: a reference capture and an implementation capture. It determines where their observed behaviour agrees, differs, cannot be established, conflicts, or cannot fairly be compared.

It is not a source-code diff, visual similarity score, test-suite pass rate, or proof of universal equivalence.

## 2. Inputs and preconditions

A comparison MUST identify both capture IDs and schema versions. It MUST declare the facets, scenarios, conditions, and dimensions within scope, plus known exclusions and limitations.

Before comparing a pair, the process MUST assess:
- system boundaries and target/build identities;
- scenario intent, actions, inputs, preconditions, actor/permissions, initial state, and relevant configuration;
- runtime environment and dependency conditions that materially affect the result;
- facet and dimension compatibility;
- observation method, evidence quality, time/order, and capture completeness.

A difference in implementation technology is not itself a reason to reject comparison. A difference in observable semantics or relevant conditions may be.

## 3. Pipeline

1. **Validate inputs.** Validate each capture against its declared schema version and perform cross-record integrity checks.
2. **Declare scope.** Choose the facets, scenarios, dimensions, conditions, and exclusions. Do not widen scope after seeing results without recording the change.
3. **Align scenarios and conditions.** Establish which executions represent the same intended experiment. Retain unmatched executions.
4. **Align records.** Match observations/rules only where identity and scope are sufficiently supported.
5. **Project and normalize.** Derive comparison values through versioned, documented transformations. Preserve raw values and evidence.
6. **Compare dimensions.** Apply the declared comparison basis and any justified tolerance.
7. **Classify.** Emit one classification per evaluated dimension/record relationship, including uncertainty and incomparability.
8. **Summarize coverage.** Report declared, observed, missing, unknown, unavailable, not-applicable, and comparable units for each side.
9. **Conclude narrowly.** State what the evidence establishes within the declared scope and list limitations.

## 4. Comparison unit

The comparison unit is a facet-specific observable dimension under an aligned scenario, execution condition, subject, and relevant state. A whole record may contain multiple dimensions; it MUST NOT be declared a match merely because one dimension matches.

A comparison result links to its alignment and, where applicable, the source observation IDs on both sides. A result may aggregate multiple observations only when the aggregation rule is explicit and repeatable.

## 5. Comparison bases

- **Exact:** values are equal under the facet's explicitly defined equality semantics. Raw byte equality is not implied unless the dimension says so.
- **Normalized:** values are equal after named, versioned normalization operations.
- **Semantic:** a documented facet-specific evaluator determines equivalent meaning. The evaluator, version, inputs, and rationale MUST be recorded; human review MUST be identified as such.
- **Tolerance:** numeric or measured values fall within an explicitly justified metric and tolerance.
- **None:** no valid comparison was performed; use for unknown, conflicting, or not-comparable outcomes.

A basis MUST NOT be upgraded after results are known merely to obtain a match. Semantic equivalence MUST NOT be asserted by generic string similarity or an undocumented AI judgment.

## 6. Result and overall conclusion

Every result is local to a dimension and its evidence. Overall report status is:
- `agreement-within-observed-scope`: all in-scope comparable dimensions match and no unresolved in-scope result remains;
- `differences-found`: at least one supported mismatch, missing, or additional result exists;
- `inconclusive`: evidence is insufficient or unresolved results prevent a supported conclusion;
- `not-comparable`: the declared comparison cannot establish a valid shared scope.

The report MUST set `scopeBounded` true and `universalEquivalenceClaimed` false. Agreement is never a claim that all possible inputs or states are equivalent.

## 7. Replication completeness gate

Observed agreement and replication-scope completeness are separate determinations. A report MUST retain the completeness status of the reference and implementation captures and the combined result. If either capture is incomplete or undetermined, the report MAY state that the compared observations agree within the observed scope, but MUST NOT describe the result as faithful replication, complete equivalence, or proof that the declared scope has been reproduced. Required inventory gaps remain gaps even when every available comparison result is a match. A structurally valid inventory is not proof that the inventory itself is exhaustive; that requires explicit scope review and facet/domain analysis.

## 8. Repeated and nondeterministic behaviour

Repeated executions MUST remain individually identifiable. A single run MUST NOT be treated as the complete distribution of nondeterministic behaviour. If comparing distributions, define the sampling window, sample count, aggregation/statistical method, confidence or uncertainty treatment, and environmental controls. Otherwise compare executions individually and report variability as unresolved.

## 9. Evidence classes

Primary runtime comparison MUST use runtime observations supported by runtime evidence. Source-derived rules and declared contracts MAY be shown as contextual or secondary comparisons, but MUST be labelled and MUST NOT satisfy runtime coverage. Contract-versus-runtime checks are a separate relationship from reference-runtime versus implementation-runtime comparison.

## 10. Output

The report structure is defined by `schemas/v1/comparison-report.schema.json`. The report MUST preserve capture references, normalization profile, record alignments, per-dimension results, coverage, conclusion, and limitations. It MUST remain traceable to original capture records.
