# Coverage and Limitations

**Status:** Draft — Phase 5

## 1. Coverage denominator

Coverage is meaningful only relative to declared scope. Each capture must identify the scenarios, facets, subjects, and observable dimensions it intended to examine. Reports summarize both sides independently and identify their shared comparable subset.

Do not calculate a percentage without a defensible denominator. If the declared units are unknown or not enumerable, report counts/statuses and explain why no percentage is available.

## 2. Replication-scope completeness

For replication-oriented work, each capture MUST declare its replication scope and carry an explicit property inventory. Every required property is identified by facet, subject, and dimension, with a capture state and evidence/observation references where available.

Completeness MUST be reported separately from observed agreement. A comparison may find that every captured property matches while both captures remain incomplete. Such a result MUST NOT be described as faithful replication, complete equivalence, or proof that the rendered screens/systems are the same.

A required property marked partial, not observed, unknown, unavailable, conflicting, or source-inferred prevents a complete status. A source-derived inference does not satisfy a runtime capture requirement. Optional exclusions require a reason and remain visibly outside the declared replication obligation.

A completeness percentage alone is insufficient: one missing critical property can invalidate reproduction even when many low-impact properties are captured. Completeness must be traceable to individual inventory entries and their evidence.

## 3. Required coverage distinctions

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

## 4. Bounded conclusions

- **Agreement within observed scope** is permitted only when every in-scope comparable dimension is matched and no in-scope missing, additional, unknown, conflicting, or not-comparable result remains unresolved.
- **Differences found** applies when at least one supported mismatch, missing, or additional result exists.
- **Inconclusive** applies when evidence gaps or unresolved results prevent either conclusion.
- **Not comparable** applies when no defensible common scope can be established.

A conclusion must identify capture IDs, schema versions, profile, scope, and limitations. It MUST NOT claim that the systems are equivalent in general, universally equivalent, or identical for untested inputs.

## 5. Repeated executions

Report execution counts and variability. Averages or representative samples MUST NOT conceal outliers or inconsistent outcomes. If sampling is insufficient to characterize nondeterministic behaviour, say so.

## 6. Coverage is not quality

High coverage does not prove evidence quality, correct scenario design, or semantic completeness. Low coverage does not prove a mismatch. Coverage and comparison results are separate report dimensions.

## 7. Threats to validity

Common threats include different builds/configurations, environmental drift, different initial states, hidden external dependencies, clocks, locale, actor permissions, data fixtures, unstable IDs, sampling bias, flaky execution, instrumentation effects, lossy normalization, and incomplete evidence retention. Record threats that could materially alter the result.


## Replication inventory status accounting

Coverage reports should preserve the distinct inventory states rather than collapsing them into a single observed/not-observed count. In addition to captured/observed units, report partial, not observed, unknown, unavailable, conflicting, source-inferred, not-applicable, and excluded units where present. These counts summarize the inventory; they do not prove that the inventory itself is exhaustive or that its evidence is semantically adequate. A partial unit remains unresolved for replication completeness even when it contains useful observations.
