# Independent Replication Lab

This is the independent implementation area for Phase 6 cross-repository conformance.

## Principle

A source repository is studied to extract a technology-independent rule. The rule is then implemented here without depending on the source implementation. Equivalent scenarios are run against both systems, captures are compared, and a deliberate mutation must be detected.

The lab is organised by rule case, not by source stack. Each case links to an immutable source repository commit and to one or more independent replica implementations.

## Layout

- cases/<rule-id>/ — source/replica captures, probes, evidence, comparison, mutation.
- projects/<project-id>/ — independent implementations, potentially in multiple stacks.
- runners/ — shared execution and capture tooling.
- reports/ — generated case and facet coverage summaries.

## Case lifecycle

1. Register the source repository and immutable commit in examples/cross-repository/sources.
2. Define the rule and scope in the case manifest.
3. Capture source behaviour and record evidence.
4. Implement the rule independently in a different stack.
5. Run equivalent probes and capture the replica.
6. Compare captures and run the mutation test.
7. Update the facet coverage report only after evidence review.

## Current status

The living facet-by-facet evidence matrix is maintained in [FACET-COVERAGE.md](FACET-COVERAGE.md). The reviewed property classes and current gaps for all 15 facets are listed in [PHASE6-REQUIRED-PROPERTY-INVENTORY.md](PHASE6-REQUIRED-PROPERTY-INVENTORY.md). Twenty bounded cases pass: the eight original BullMQ retry/backoff, BullMQ message lifecycle, Express routing, TypeORM transaction commit/rollback, Medusa date validation, JOSE JWT verification, Casbin simple-RBAC authorization, and Redis client integration cases; plus TASKBOARD-UI-001 (independent React UI replication), EXP-CONFIG-001 (Express configuration activation), PROM-PERF-001 (Prometheus workload measurements), CASBIN-ADV-AUTHZ-001 (advanced authorization policy classes), MEDUSA-PRICE-001 (calculated-price selection), AXIOS-HTTP-001 (Axios HTTP integration), SESSION-EXPRESS-001 (session lifecycle), VIPER-CONFIG-001 (configuration precedence), TORM-PERSIST-002 (file-backed persistence durability), BMQ-RECOVERY-001 (stalled-job recovery), MEDUSA-ADJUST-001 (adjustment/tax allocation), and MEDUSA-PROMO-001 (promotion eligibility). No entire facet is claimed universally complete for the full project objective yet. The existing Task Board fixture remains separate and retains its bounded evidence status.
