# Phase 6 — Fifteen-facet evidence coverage

**Overall status:** In progress. Seven bounded cross-stack cases have passed: BullMQ retry/backoff, BullMQ messaging, Express routing, TypeORM transaction commit/rollback, Medusa price-list date validation, JOSE JWT verification, and Casbin simple-RBAC authorization. No entire facet is complete for the project-wide objective.

This matrix distinguishes a facet having some validated evidence from a facet being complete. A bounded case does not establish complete facet coverage.

## Coverage matrix

| # | Facet | Source evidence / current result | Independent replica | Status |
|---|---|---|---|---|
| 1 | Interface | Task Board has a bounded 1280×800 UI capture with pixel-identical tested states and detected visual mutation; two inventory properties remain partial and broader interface environments are not covered. | Independent browser UI fixture | Partial |
| 2 | Behaviour | BullMQ retry/backoff and messaging, Express routing, TypeORM transactions, Medusa date-validation order, and JOSE verification ordering have bounded cross-stack matches. | Python retry/queue models, HTTP server, SQLite transaction model, date validator, and JWT verifier | In progress |
| 3 | Business rules | Medusa price-list date validation passes ten probes and 40 projections. Full cart, discount, tax, and price-selection rules remain uncovered. | Python ISO-8601 validator with mutation tests | In progress |
| 4 | Data | TypeORM Post/Category snapshots, BullMQ attempt counters/message payloads, Medusa date fields, and verified JWT claims have bounded evidence; Task Board data properties remain partial. | Python/SQLite, queue, date, and JWT models | Partial |
| 5 | Persistence | TypeORM 1.1.3 commit-on-success and rollback-on-callback-error match the Python/SQLite model across two scenarios and eight projections; schema and integrity validation passed. Other drivers, concurrency, isolation, and durability remain untested. | Python 3.12 / sqlite3 | In progress |
| 6 | API | Express 5.3.0 matches an independent Python HTTP implementation across seven requests and 28 facet/scenario projections. This does not cover the complete Express API surface. | Python 3.12 HTTP server | In progress |
| 7 | Messaging | BullMQ QueueEvents/message lifecycle matches the independent Python model across two scenarios and ten projections; six mutations, schema validation, comparison validation, and evidence-integrity checks passed in run [#45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126). | Python messaging model | In progress |
| 8 | Identity and authentication | JOSE 6.2.18 JWT verification matches an independent Python verifier across 11 scenarios and 55 facet/scenario projections; eight executable mutations and schema/integrity validation passed. This is bounded token verification, not a full identity provider, login/session lifecycle, or authorization system. | Python 3.12 HMAC/JWT verifier | In progress |
| 9 | Authorization and permissions | CASBIN-AUTHZ-001 matches pinned Apache Casbin Go source across ten subject/resource/action requests; four executable mutations, Software Rules 0.2.0 schema validation, comparison validation, and evidence integrity passed in run [#45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753). This covers simple RBAC only; domains, role hierarchy, ABAC, deny policies, and policy mutation remain untested. | Python 3.12 RBAC evaluator | In progress |
| 10 | Security controls | JOSE HMAC signature integrity and algorithm allowlisting match across the declared synthetic-token cases; eight mutations and schema/integrity validation passed. Broader security controls remain untested. | Python 3.12 HMAC/JWT verifier | In progress |
| 11 | Background processing | BullMQ retry/backoff and message lifecycle cases pass bounded source/replica probes. Scheduling, cancellation, concurrency, stalled jobs, and full lifecycle remain uncovered. | Python retry-decision model | In progress |
| 12 | Errors and recovery | BullMQ retry suppression/consumer failure, Express 404 fallback, TypeORM rollback, Medusa invalid_data, and JOSE semantic JWT rejection categories pass bounded cases; broader failure classes remain uncovered. | Python retry, queue, HTTP, SQLite, date, and JWT models | In progress |
| 13 | Integrations | REDIS-INT-001 is prepared: pinned go-redis Go client versus Python redis-py against an isolated Redis 7 service, seven normalized operations, five executable mutations, and schema-native capture validation. CI pending. | Python 3.12 / redis-py | In progress |
| 14 | Configuration | Express default case-sensitive/strict routing settings pass in the seven-request case. Effective configuration precedence in Grafana/Keycloak remains untested. | Python HTTP server | In progress |
| 15 | Performance and resource behaviour | Prometheus is a registered candidate; no reproducible source workload and independent measurement case has passed. | None yet | Not started |

## Accepted bounded cases

TypeORM verification: run [#45928766010](https://github.com/REMAREMA6/software-rules/actions/runs/45928766010), eight matching projections, six mutation tests, schema 0.2.0 capture/report validation and evidence-integrity validation passed; retained artifact ID `15167104492` (expires 2026-12-27).

| Case | Facets | Evidence |
|---|---|---|
| [BMQ-ER-002](cases/BMQ-ER-002/CASE.md) | Background processing; errors/recovery; data; behaviour | Source/replica runtime comparison, mutation detection, Software Rules captures, schema/integrity validation, and committed artifacts |
| [EXP-API-001](cases/EXP-API-001/CASE.md) | API; behaviour; configuration; errors/recovery | Seven HTTP requests, 28 matching projections, executable mutations, Software Rules captures, schema/integrity validation, and committed artifacts |
| [TORM-PERSIST-001](cases/TORM-PERSIST-001/CASE.md) | Persistence; data; behaviour; errors/recovery | Two transaction scenarios, eight matching projections, six mutation tests, Software Rules captures, schema/integrity validation; workflow artifact retained (not yet committed as repository files) |
| [MEDUSA-BR-001](cases/MEDUSA-BR-001/CASE.md) | Business rules; data; behaviour; errors/recovery | Ten date inputs, 40 matching projections, executable mutations, Software Rules captures, schema/integrity validation, and committed source evidence |
| [BMQ-MSG-001](cases/BMQ-MSG-001/CASE.md) | Messaging; background processing; behaviour; errors/recovery; data | Two message scenarios, ten matching projections, six executable mutations, Software Rules 0.2.0 captures, schema/integrity validation, and committed evidence; run [#45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126) |
| [JOSE-AUTH-001](cases/JOSE-AUTH-001/CASE.md) | Identity/authentication; security controls; data; behaviour; errors/recovery | Eleven JWT scenarios, 55 facet/scenario projections, eight executable mutations, Software Rules 0.2.0 captures, schema/integrity validation, committed evidence, and retained artifact; run [#45930973956](https://github.com/REMAREMA6/software-rules/actions/runs/45930973956) |
| [CASBIN-AUTHZ-001](cases/CASBIN-AUTHZ-001/CASE.md) | Authorization and permissions; behaviour; data | Ten RBAC requests, four executable mutations, Software Rules 0.2.0 captures, comparison, schema validation, evidence integrity, and retained CI artifact; run [#45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753) |


## Active cases

- [REDIS-INT-001](cases/REDIS-INT-001/CASE.md) — pinned go-redis source versus independent Python redis-py against Redis 7; seven operations, five mutations, Software Rules 0.2.0 capture/report builder, and CI validation workflow prepared. Not accepted until all source/replica and validation steps pass.

## Completion rule

Do not mark a facet complete because a repository has a similarly named feature or because one bounded case passes. Completion requires a reviewed property inventory for that facet, suitable source evidence, independent implementations in different stacks, equivalent normal/boundary/negative/failure probes, comparison, meaningful mutation detection, validated Software Rules captures, and explicit resolution of every required unknown or partial property.
