# Phase 6 — Cross-repository, cross-stack replication programme

**Status:** Active

## Purpose

Phase 6 validates that Software Rules can extract the underlying rules from different real software systems, express them in a technology-independent form, and reproduce them in an independent implementation using a different stack.

**One application is not expected to implement all 15 facets.** We will use multiple source repositories selected for the facets they actually demonstrate, and one separate replication project containing independent implementations. The existing Task Board remains a bounded initial fixture; it does not need to become an artificial full-stack application.

## Required validation loop

For every rule or property being validated:

1. Select a source repository and declare the exact system boundary, feature, workflow, and immutable commit.
2. Inspect and observe the source. Use runtime probes where possible; inspect source, schemas, migrations, configuration, and contracts where necessary.
3. Extract the underlying rule in technology-independent terms: entities, conditions, inputs, constraints, transitions, outputs, side effects, ordering, failure outcomes, and environment assumptions.
4. Capture the rule using the appropriate Software Rules facet payload, with provenance, scenarios, evidence, uncertainty, and stable identity.
5. Implement the rule independently in the replication project. Do not use the source implementation as the behaviour engine. Prefer a different language, framework, database, or architecture.
6. Execute semantically equivalent normal, boundary, negative, repeated, and failure scenarios against source and replica, as applicable.
7. Capture both outcomes and compare them using the Software Rules comparison model.
8. Deliberately mutate or omit a meaningful part of the replica and verify that the probes detect the difference.
9. Retain source commit, rule capture, replica commit, probes, raw evidence, comparison report, mutation result, and limitations.

A passing schema check or green CI job alone is not a successful replication. The probes must distinguish the correct rule from a meaningful incorrect implementation.

## Source/replica separation

- Use multiple source repositories; no single repository must cover every facet.
- Keep the independent replication project separate from source implementations.
- Source repositories are evidence-bearing references, not dependencies imported to perform the replicated behaviour.
- Runtime observations, source-derived inferences, and declared contracts must remain distinct.
- Source-code declarations do not prove runtime behaviour.
- A source repository may contribute cases to multiple facets, but every rule requires its own evidence and discriminating scenarios.
- Do not infer that a facet is absent from the overall project because one source repository does not implement it.
- Record when source and replica stacks are not different; such a case cannot be counted as cross-stack evidence.

## Fifteen-facet validation matrix

This matrix defines what evidence and replication must cover. Repository candidates are provisional until their commit, licence, setup, boundary, and behaviour are inspected.

| # | Facet | Source evidence to select | Independent replica probes |
|---|---|---|---|
| 1 | Interface | Real rendered screens, hierarchy, styles, geometry, assets, accessibility, responsive and interaction states | Rebuild in another UI stack; compare hierarchy, resolved presentation, geometry, semantics, and states |
| 2 | Behaviour | Real workflows, triggers, preconditions, transitions, outputs, side effects | Reproduce actions; probe normal, repeated, reordered, invalid, interrupted, and failure paths |
| 3 | Business rules | Domain decisions, calculations, constraints, defaults, precedence | Reimplement independently; test boundaries, combinations, precedence, and exceptions |
| 4 | Data | Entity shapes, fields, types, relationships, nullability, validation, transformations, serialization | Map the same conceptual model in another language/storage model; test malformed, missing, null, and round-trip cases |
| 5 | Persistence | Durable reads/writes, transactions, rollback, consistency, concurrency, retention, deletion | Use a different persistence technology; test restart durability, atomicity, rollback, visibility, and concurrent updates |
| 6 | API | Real request/response exchanges, protocol, payloads, status, headers, validation, errors | Implement in another server stack; compare successful and failed exchanges |
| 7 | Messaging | Event/message publication, consumption, delivery, acknowledgement, ordering | Use another transport/broker; test duplicate delivery, retries, ordering, acknowledgement, and idempotency |
| 8 | Identity/authentication | Principal establishment, credentials, session/token lifecycle, expiry, logout | Reproduce lifecycle independently; test valid/invalid credentials, renewal, expiry, and logout |
| 9 | Authorization | Roles, resources, actions, policy decisions, enforcement | Implement independently; execute actor × resource × action permission matrices |
| 10 | Security controls | Authorized security scenarios and observable prevention, detection, limitation, containment | Reproduce the relevant boundary/control in isolation; test allowed, blocked, bypass, and containment outcomes |
| 11 | Background processing | Queues, schedules, workers, retries, cancellation, terminal outcomes | Use another job runner; test enqueue, execution, retry, duplicate jobs, cancellation, and failure |
| 12 | Errors and recovery | Failure classes, retries, fallbacks, compensation, recovery | Inject failures at relevant boundaries; compare error outcomes and post-recovery state |
| 13 | Integrations | External dependency interactions, contracts, timeouts, rate limits, malformed responses | Reproduce boundary semantics with controlled dependencies; test success and dependency failures |
| 14 | Configuration | Effective settings, defaults, precedence, invalid/missing values, runtime changes | Recreate in another configuration mechanism; test precedence and controlled changes |
| 15 | Performance/resources | Defined workloads, latency, throughput, resource measurements and limits | Run equivalent workloads under documented conditions; compare distributions and resource behaviour, not incomparable single samples |

## Source repository register

Create one source record per repository under examples/cross-repository/sources. Each record must include:

- canonical repository URL and owner/name;
- immutable commit SHA and date;
- licence and reuse constraints;
- language, framework, storage, runtime, and relevant dependencies;
- exact modules, workflows, and system boundary selected;
- facets/rules investigated and why the source is suitable;
- reproducible setup and runtime environment;
- runtime probe procedures and source-inspection paths;
- safety constraints, known gaps, and competing interpretations.

A repository is only a candidate until these details are verified.

## Independent replication project

Create the replication lab under conformance/replication-lab, organised by rule case rather than by source technology:

- README and execution instructions;
- projects containing independent implementations;
- cases/<rule-id>/ containing a case manifest, source capture, replica capture, comparison report, probes, evidence, and mutation test;
- shared runners and generated reports.

The source repository is referenced by immutable URL and commit. Do not copy entire repositories into the replication lab unless licensing and test isolation justify it.

## Rule-level pass criteria

A rule case passes only when the source target and commit are reproducible; scope is explicit; each claimed rule has property-specific evidence; runtime/source-derived/contract classes are distinguished; the replica is independently implemented; stacks differ for cross-stack claims; equivalent scenarios cover relevant boundaries and failures; comparison has no unexplained required mismatch or coverage gap; a meaningful mutation is detected; and the process can be reproduced from documented commands.

A single case proves transfer of that rule only. It does not establish exhaustive coverage of its facet.

## Phase 6 exit gate

Phase 6 is complete only when:

1. All 15 facets have explicit, reviewed rule/property inventories.
2. Every facet has suitable source-repository evidence and at least one independent replica case. Facets with materially different rule classes require enough cases to cover them.
3. Every claimed case follows source → technology-independent rule → independent replica → equivalent probes → comparison → mutation detection.
4. Cross-stack claims use genuinely different implementation stacks.
5. Every required property is evidenced or explicitly resolved as not applicable to that case's declared scope. Required unknown/partial properties are not silently passed.
6. The format represents the discovered rules without embedding source-framework-specific implementation instructions.
7. Provenance, evidence links, cross-facet relationships, schemas, and comparison coverage validate.
8. A final report lists rule-level outcomes, facet coverage, unresolved gaps, and limitations without claiming universal equivalence beyond the tested evidence.

## Execution order

1. Create the replication-lab skeleton and case/evidence conventions.
2. Preserve the Task Board as bounded initial evidence and close its remaining in-scope audit items.
3. Select and inspect multiple immutable source repositories, facet by facet.
4. Extract technology-independent rules and create source captures.
5. Implement independent replicas and equivalent probes.
6. Run comparisons and mutation tests.
7. Review facet inventory completeness and cross-case integrity.
8. Publish the final Phase 6 evidence matrix and completion decision.

## Current status

This programme defines the corrected strategy; it does not claim that new cross-repository cases have already passed. The next task is to create the replication-lab skeleton and case manifest, then select and inspect the first source repository for a facet not adequately represented by Task Board.
