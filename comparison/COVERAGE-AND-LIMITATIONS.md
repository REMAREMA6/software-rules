# Coverage and Limitations

**Status:** Draft — Phase 5

## 1. Coverage denominator

Coverage is meaningful only relative to declared scope. Each capture must identify the scenarios, facets, subjects, and observable dimensions it intended to examine. Reports summarize both sides independently and identify their shared comparable subset.

Do not calculate a percentage without a defensible denominator. If the declared units are unknown or not enumerable, report counts/statuses and explain why no percentage is available.

## 2. Required coverage distinctions

Keep separate:
- declared units;
- observed units;
- not observed;
- unknown;
- unavailable (tool/platform/retention limitation);
- not applicable;
- partial;
- conflicting;
- shared comparable units;
- incomparable units.

A unit is not covered merely because a capture file contains a record for the same facet. The relevant dimension and conditions must have been examined.

## 3. Bounded conclusions

- **Agreement within observed scope** is permitted only when every in-scope comparable dimension is matched and no in-scope missing, additional, unknown, conflicting, or not-comparable result remains unresolved.
- **Differences found** applies when at least one supported mismatch, missing, or additional result exists.
- **Inconclusive** applies when evidence gaps or unresolved results prevent either conclusion.
- **Not comparable** applies when no defensible common scope can be established.

A conclusion must identify capture IDs, schema versions, profile, scope, and limitations. It MUST NOT claim that the systems are equivalent in general, universally equivalent, or identical for untested inputs.

## 4. Repeated executions

Report execution counts and variability. Averages or representative samples MUST NOT conceal outliers or inconsistent outcomes. If sampling is insufficient to characterize nondeterministic behaviour, say so.

## 5. Coverage is not quality

High coverage does not prove evidence quality, correct scenario design, or semantic completeness. Low coverage does not prove a mismatch. Coverage and comparison results are separate report dimensions.

## 6. Threats to validity

Common threats include different builds/configurations, environmental drift, different initial states, hidden external dependencies, clocks, locale, actor permissions, data fixtures, unstable IDs, sampling bias, flaky execution, instrumentation effects, lossy normalization, and incomplete evidence retention. Record threats that could materially alter the result.
