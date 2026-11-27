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

The living facet-by-facet evidence matrix is maintained in [FACET-COVERAGE.md](FACET-COVERAGE.md). The reviewed property classes and current gaps for all 15 facets are listed in [PHASE6-REQUIRED-PROPERTY-INVENTORY.md](PHASE6-REQUIRED-PROPERTY-INVENTORY.md). Twelve bounded cases pass, including EXP-CONFIG-001 (Express configuration activation), PROM-PERF-001 (Prometheus workload measurements), and CASBIN-ADV-AUTHZ-001 (advanced authorization policy classes). BullMQ retry/backoff, BullMQ message lifecycle, Express routing, TypeORM transaction commit/rollback, Medusa price-list date validation, JOSE JWT verification, Casbin simple-RBAC authorization, and Redis client integration. No entire facet is complete for the full project objective yet. The existing Task Board fixture remains separate and retains its bounded evidence status.
