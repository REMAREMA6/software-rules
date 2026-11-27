# Difference Classification

**Maturity:** Draft — Software Rules specification 0.3.0

Each result classifies one aligned facet dimension. Classifications are mutually exclusive per result.

| Classification | Meaning | Required handling |
|---|---|---|
| `match` | Comparable values agree under the declared basis. | Record basis and both source observations. |
| `mismatch` | Comparable values differ under the declared basis. | Record both values, basis, and evidence. |
| `missing` | A required in-scope observation/value is absent on one or both sides despite adequate capture opportunity. | State `missingSide`; do not use when capture completeness is unknown. |
| `additional` | One side has an in-scope observable behaviour/dimension with no counterpart on the other. | Identify which side and why it is within scope. |
| `unknown` | Evidence or state is insufficient to determine the value or result. | Preserve the specific unknown/not-observed/unavailable reason. |
| `conflicting` | Credible observations for the same aligned condition contradict one another and cannot be reconciled. | Retain all observations and describe conflict; do not select one silently. |
| `not-comparable` | A valid comparison cannot be made because scope, conditions, facet, units, or semantics are incompatible. | State the incompatibility; no pass/fail implication. |

## Decision order

1. Confirm alignment and condition compatibility. If not, use not-comparable or ambiguous alignment.
2. Determine whether evidence exists and is adequate on both sides. If not, use unknown unless absence is established under adequate coverage.
3. Check for unresolved contradictory observations. If present, use conflicting.
4. Establish whether the dimension is required/in-scope and whether a counterpart should exist.
5. If a required counterpart is absent despite adequate coverage, use missing; if one side has a genuinely extra in-scope behaviour, use additional.
6. Only then compare values and choose match or mismatch.

## Missing versus additional

Missing means an expected in-scope item is absent on a side. Additional means an observed in-scope item exists on one side without a counterpart. The report's `missingSide` field identifies reference, implementation, or both for `missing`; the rationale identifies the side for `additional`. A record outside declared scope is neither.

## No implicit pass

Unknown, conflicting, and not-comparable are not matches. Empty result sets do not imply agreement. A report with unresolved in-scope dimensions cannot conclude agreement-within-observed-scope.
